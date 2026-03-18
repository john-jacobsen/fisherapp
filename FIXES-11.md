# FIXES-11: Placement Algorithm Rewrite

**Date:** 2026-03-16
**Scope:** Backend placement logic, frontend placement UI

---

## Problem

The current placement test uses per-topic BKT with a 3-question minimum and 0.85 posterior threshold. This results in:
- Underplacement: 3 correct answers on easy questions is enough to "master" a topic, even if the student got lucky or the questions were trivially easy
- Too many questions: testing every topic independently would need hundreds of questions
- No use of the prerequisite graph: knowing calculus derivatives implies knowing algebra, but the current system tests them independently

## Goal

Replace the placement test with a **graph-aware adaptive assessment** that determines a student's knowledge frontier in 25–30 questions total, leveraging the prerequisite structure to infer mastery of upstream topics.

## Algorithm: Graph-Aware Binary Search

### Data structures

```python
# The assessment maintains:
placement_state = {
    "confirmed_mastered": set(),   # nodes confirmed by correct answers
    "confirmed_unknown": set(),    # nodes confirmed by wrong answers
    "inferred_mastered": set(),    # nodes inferred from downstream mastery
    "inferred_unknown": set(),     # nodes inferred from upstream failure
    "frontier": set(),             # boundary nodes still being explored
    "questions_asked": 0,
    "max_questions": 30,
    "history": [],                 # list of {node_id, is_correct}
}
```

### Algorithm steps

**1. Initialize — pick starting nodes**

Choose one node per subject at roughly the midpoint of the prerequisite chain. For each of the 6 subjects, find the node whose depth in the prerequisite DAG is closest to the median depth for that subject. These 6 nodes form the initial frontier.

```python
def get_starting_nodes(graph_edges, subjects):
    """Pick one mid-depth node per subject."""
    starting = []
    for subject_prefix in ['frac-', 'alg-', 'calc-', 'linalg-', 'prob-', 'stat-']:
        subject_nodes = [n for n in all_nodes if n.startswith(subject_prefix)]
        # Compute depth of each node in the DAG
        depths = compute_depths(subject_nodes, graph_edges)
        median_depth = sorted(depths.values())[len(depths) // 2]
        # Pick the node closest to median depth
        mid_node = min(subject_nodes, key=lambda n: abs(depths[n] - median_depth))
        starting.append(mid_node)
    return starting
```

Note: for Foundations, use `eq-` as the prefix (most Foundations nodes are very early and using `frac-` would start too low).

**2. Present a question**

Select the next node from the frontier. For each frontier node, generate one problem and present it. After the student answers:

**3. If correct → explore downstream**

```python
def handle_correct(node_id, state, graph):
    state["confirmed_mastered"].add(node_id)
    state["history"].append({"node_id": node_id, "is_correct": True})

    # Infer: all prerequisites of this node are also mastered
    ancestors = get_all_ancestors(node_id, graph)
    state["inferred_mastered"].update(ancestors)

    # Remove inferred nodes from frontier (no need to test them)
    state["frontier"].discard(node_id)
    state["frontier"] -= state["inferred_mastered"]

    # Add downstream nodes to frontier (if not already confirmed/inferred)
    children = get_direct_children(node_id, graph)
    for child in children:
        if child not in state["confirmed_mastered"] and \
           child not in state["confirmed_unknown"] and \
           child not in state["inferred_mastered"] and \
           child not in state["inferred_unknown"]:
            state["frontier"].add(child)
```

**4. If incorrect → explore upstream**

```python
def handle_incorrect(node_id, state, graph):
    state["confirmed_unknown"].add(node_id)
    state["history"].append({"node_id": node_id, "is_correct": False})

    # Infer: all descendants of this node are also unknown
    descendants = get_all_descendants(node_id, graph)
    state["inferred_unknown"].update(descendants)

    # Remove inferred nodes from frontier
    state["frontier"].discard(node_id)
    state["frontier"] -= state["inferred_unknown"]

    # Add parent nodes to frontier (if not already confirmed/inferred)
    parents = get_direct_parents(node_id, graph)
    for parent in parents:
        if parent not in state["confirmed_mastered"] and \
           parent not in state["confirmed_unknown"] and \
           parent not in state["inferred_mastered"] and \
           parent not in state["inferred_unknown"]:
            state["frontier"].add(parent)
```

**5. Termination**

The test ends when:
- The frontier is empty (all nodes are classified), OR
- `questions_asked >= max_questions` (hard cap), OR
- The frontier has been stable for 3 consecutive questions (no new nodes added)

**6. Apply results**

After termination, the student's mastered set = `confirmed_mastered ∪ inferred_mastered`. Write this to `StudentState.mastered_nodes`. Compute fringes. The outer fringe of this set becomes the recommended starting point.

### Edge cases

- **Student gets everything right:** The frontier keeps moving downstream until hitting leaf nodes. Student is placed at the most advanced level. Should take ~8–10 questions.
- **Student gets everything wrong:** The frontier moves upstream to the earliest nodes. Student starts from the beginning. Should take ~6–8 questions.
- **Mixed results:** The frontier converges to the boundary between known and unknown. The prerequisite graph inference prevents redundant testing. Should take ~20–25 questions.
- **Subject isolation:** A student might know statistics but not calculus. The algorithm handles this because each subject has its own branch in the frontier. Getting calc wrong doesn't affect stat nodes.

### Confidence boost (optional, recommended)

For nodes at the confirmed boundary (directly adjacent to both mastered and unknown), ask a second question to confirm. This catches lucky guesses and unlucky mistakes. Only do this for the 3–5 nodes right at the boundary, not for every node.

```python
# After initial traversal, identify boundary nodes
boundary = set()
for node in state["confirmed_mastered"]:
    children = get_direct_children(node, graph)
    if any(c in state["confirmed_unknown"] or c in state["inferred_unknown"] for c in children):
        boundary.add(node)
for node in state["confirmed_unknown"]:
    parents = get_direct_parents(node, graph)
    if any(p in state["confirmed_mastered"] or p in state["inferred_mastered"] for p in parents):
        boundary.add(node)

# Re-test boundary nodes (max 5)
for node in list(boundary)[:5]:
    if state["questions_asked"] >= state["max_questions"]:
        break
    # Generate and present one more question for this node
    # If the result contradicts the original, ask a third tiebreaker
```

## Implementation

### Backend

**New file: `backend/app/services/placement_engine.py`**

Contains:
- `initialize_placement(user_id, db)` → returns initial state + first question
- `submit_placement_answer(user_id, state, node_id, is_correct, db)` → returns updated state + next question or completion
- `complete_placement(user_id, state, db)` → writes mastered_nodes to StudentState
- Helper functions: `get_all_ancestors`, `get_all_descendants`, `get_direct_children`, `get_direct_parents`, `compute_depths`, `get_starting_nodes`

**Modify: `backend/app/routers/placement.py`**

Update the placement endpoints to use `placement_engine` instead of the current BKT-based approach. Keep the same API shape if possible so the frontend changes are minimal:
- `POST /placement/start` → returns first question + progress
- `POST /placement/submit` → returns next question + progress + is_complete
- `GET /placement/results` → returns final mastered set

**Progress reporting:**

The frontend needs to show progress. Report:
```python
{
    "questions_asked": state["questions_asked"],
    "estimated_total": 25,  # fixed estimate
    "nodes_classified": len(confirmed_mastered) + len(confirmed_unknown) + len(inferred_mastered) + len(inferred_unknown),
    "total_nodes": 176,
}
```

### Frontend

**Modify: `frontend/src/pages/PlacementQuestion.jsx`**

The placement page should work the same as before — show a question, accept an answer, show the next question. The only changes:
- Progress text: "Question N of ~25" (fixed estimate of 25)
- Progress bar: based on `nodes_classified / total_nodes` (not questions asked)
- After completion: show a summary of how many topics were placed ("You've demonstrated mastery of N topics across M subjects")

### Graph utilities

The prerequisite graph is already in `backend/data/knowledge_graph.json` as `edges: [[from, to], ...]`. Build the ancestor/descendant functions from this. Cache the graph structure on first load (it doesn't change at runtime).

```python
from functools import lru_cache

@lru_cache(maxsize=1)
def _load_graph():
    """Load the prerequisite graph and build adjacency lookups."""
    with open("backend/data/knowledge_graph.json") as f:
        data = json.load(f)
    children = defaultdict(set)  # parent → set of children
    parents = defaultdict(set)   # child → set of parents
    for frm, to in data["edges"]:
        children[frm].add(to)
        parents[to].add(frm)
    return {"items": data["items"], "children": dict(children), "parents": dict(parents)}

def get_all_ancestors(node_id, graph=None):
    """BFS/DFS upstream to find all ancestors."""
    if graph is None:
        graph = _load_graph()
    visited = set()
    queue = list(graph["parents"].get(node_id, []))
    while queue:
        n = queue.pop()
        if n not in visited:
            visited.add(n)
            queue.extend(graph["parents"].get(n, []))
    return visited

def get_all_descendants(node_id, graph=None):
    """BFS/DFS downstream to find all descendants."""
    if graph is None:
        graph = _load_graph()
    visited = set()
    queue = list(graph["children"].get(node_id, []))
    while queue:
        n = queue.pop()
        if n not in visited:
            visited.add(n)
            queue.extend(graph["children"].get(n, []))
    return visited
```

## Verification

1. Create a fresh user
2. Start placement test — should begin with ~6 questions (one per subject at mid-depth)
3. Answer all correctly — test should explore downstream, asking progressively harder questions
4. Should complete in 20–30 questions
5. Dashboard should show a reasonable number of mastered topics (not just the ones directly tested)
6. Check that the mastered set is a valid knowledge state (closed under prerequisites — if node X is mastered, all prereqs of X should also be mastered)

### Automated validation:

```python
# After placement, verify the mastered set is prerequisite-closed
mastered = student_state.mastered_nodes
for node in mastered:
    ancestors = get_all_ancestors(node)
    missing = ancestors - set(mastered)
    assert not missing, f"Node {node} is mastered but prereq {missing} is not"
```
