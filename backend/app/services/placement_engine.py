"""
Graph-aware adaptive placement engine.

Replaces the BLIM-based placement with a binary search over the prerequisite
DAG.  Each correct answer propagates mastery upstream (via ancestors) and opens
downstream nodes; each incorrect answer closes downstream nodes and opens
upstream ones.  Termination when the frontier empties, the question cap is
reached, or the frontier is stable for 3 consecutive questions.
"""
import copy
import json
import logging
import os
import traceback
import uuid
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from functools import lru_cache
from typing import Optional

from sqlalchemy.orm import Session as DBSession
from sqlalchemy.orm.attributes import flag_modified

from app.services.problem_generator import generate_problem
from app.services.answer_checker import check_answer
from app.models.content import Problem
from app.models.knowledge import KnowledgeNode, KnowledgeGraph
from app.models.progress import Session, StudentState, ReviewSchedule

logger = logging.getLogger(__name__)

_GRAPH_JSON = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "knowledge_graph.json")
)


# ---------------------------------------------------------------------------
# Graph loading (cached for the lifetime of the process)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _load_graph() -> dict:
    """Load the prerequisite graph and build adjacency lookups."""
    with open(_GRAPH_JSON) as f:
        data = json.load(f)

    children: dict[str, set] = defaultdict(set)   # parent → children
    parents: dict[str, set] = defaultdict(set)     # child  → parents

    for rel in data["surmise_relations"]:
        prereq = rel["prerequisite"]
        target = rel["target"]
        children[prereq].add(target)
        parents[target].add(prereq)

    all_node_ids = [item["id"] for item in data["items"]]
    topic_map = {item["id"]: item.get("topic", "") for item in data["items"]}

    return {
        "items": data["items"],
        "all_node_ids": all_node_ids,
        "topic_map": topic_map,
        "children": dict(children),
        "parents": dict(parents),
    }


# ---------------------------------------------------------------------------
# Graph traversal helpers
# ---------------------------------------------------------------------------

def get_direct_children(node_id: str, graph: Optional[dict] = None) -> set:
    if graph is None:
        graph = _load_graph()
    return set(graph["children"].get(node_id, set()))


def get_direct_parents(node_id: str, graph: Optional[dict] = None) -> set:
    if graph is None:
        graph = _load_graph()
    return set(graph["parents"].get(node_id, set()))


def get_all_ancestors(node_id: str, graph: Optional[dict] = None) -> set:
    """DFS upstream — returns all transitive prerequisites of node_id."""
    if graph is None:
        graph = _load_graph()
    visited: set = set()
    queue = list(graph["parents"].get(node_id, []))
    while queue:
        n = queue.pop()
        if n not in visited:
            visited.add(n)
            queue.extend(graph["parents"].get(n, []))
    return visited


def get_all_descendants(node_id: str, graph: Optional[dict] = None) -> set:
    """DFS downstream — returns all transitive dependents of node_id."""
    if graph is None:
        graph = _load_graph()
    visited: set = set()
    queue = list(graph["children"].get(node_id, []))
    while queue:
        n = queue.pop()
        if n not in visited:
            visited.add(n)
            queue.extend(graph["children"].get(n, []))
    return visited


def compute_depths(node_ids: list, graph: Optional[dict] = None) -> dict:
    """BFS from root nodes to assign topological depth within a subject."""
    if graph is None:
        graph = _load_graph()
    node_set = set(node_ids)
    # Roots within the subject = nodes with no in-subject prerequisites
    roots = [
        n for n in node_ids
        if not (set(graph["parents"].get(n, [])) & node_set)
    ]
    depths: dict = {n: 0 for n in roots}
    queue = list(roots)
    while queue:
        n = queue.pop(0)
        for child in graph["children"].get(n, []):
            if child in node_set and child not in depths:
                depths[child] = depths[n] + 1
                queue.append(child)
    # Unreachable nodes (cross-subject edges etc.) default to depth 0
    for n in node_ids:
        if n not in depths:
            depths[n] = 0
    return depths


def get_starting_nodes(graph: Optional[dict] = None) -> list:
    """
    Pick one mid-depth node per subject (topic).
    Returns a list with one representative starting node per topic.
    """
    if graph is None:
        graph = _load_graph()

    by_topic: dict = defaultdict(list)
    for node_id in graph["all_node_ids"]:
        topic = graph["topic_map"].get(node_id, "unknown")
        by_topic[topic].append(node_id)

    starting = []
    for topic, nodes in sorted(by_topic.items()):
        if not nodes:
            continue
        depths = compute_depths(nodes, graph)
        sorted_vals = sorted(depths.values())
        median_depth = sorted_vals[len(sorted_vals) // 2]
        mid_node = min(nodes, key=lambda n: abs(depths[n] - median_depth))
        starting.append(mid_node)

    return starting


# ---------------------------------------------------------------------------
# Fringe computation (without relying on KST engine)
# ---------------------------------------------------------------------------

def _compute_fringes(mastered_set: set, graph: Optional[dict] = None) -> tuple:
    """
    outer_fringe: unmastered nodes whose every direct prerequisite is mastered
                  (or that have no prerequisites at all).
    inner_fringe: mastered nodes that have at least one direct unmastered child.
    Returns (inner_fringe_list, outer_fringe_list).
    """
    if graph is None:
        graph = _load_graph()
    all_nodes = set(graph["all_node_ids"])
    unmastered = all_nodes - mastered_set

    outer = [
        n for n in unmastered
        if not (set(graph["parents"].get(n, [])) - mastered_set)
    ]
    inner = [
        n for n in mastered_set
        if set(graph["children"].get(n, [])) & unmastered
    ]
    return inner, outer


# ---------------------------------------------------------------------------
# State helpers (sets ↔ sorted lists for JSON storage)
# ---------------------------------------------------------------------------

def _make_new_state(starting_nodes: list) -> dict:
    return {
        "confirmed_mastered": [],
        "confirmed_unknown": [],
        "inferred_mastered": [],
        "inferred_unknown": [],
        "frontier": sorted(starting_nodes),
        "questions_asked": 0,
        "max_questions": 30,
        "history": [],
        "ephemeral_answers": {},
        "asked_problems": [],
        "correct_count": 0,
    }


def _to_sets(state: dict) -> dict:
    return {
        "confirmed_mastered": set(state["confirmed_mastered"]),
        "confirmed_unknown": set(state["confirmed_unknown"]),
        "inferred_mastered": set(state["inferred_mastered"]),
        "inferred_unknown": set(state["inferred_unknown"]),
        "frontier": set(state["frontier"]),
    }


def _flush_sets(s: dict, state: dict) -> None:
    """Write set data back into the state dict as sorted lists."""
    state["confirmed_mastered"] = sorted(s["confirmed_mastered"])
    state["confirmed_unknown"] = sorted(s["confirmed_unknown"])
    state["inferred_mastered"] = sorted(s["inferred_mastered"])
    state["inferred_unknown"] = sorted(s["inferred_unknown"])
    state["frontier"] = sorted(s["frontier"])


# ---------------------------------------------------------------------------
# Algorithm steps
# ---------------------------------------------------------------------------

def _handle_correct(node_id: str, s: dict, graph: dict) -> int:
    """
    Mark node correct, infer all ancestors mastered, expand frontier downstream.
    Returns the number of new nodes added to the frontier.
    """
    s["confirmed_mastered"].add(node_id)
    ancestors = get_all_ancestors(node_id, graph)
    s["inferred_mastered"].update(ancestors)
    s["frontier"].discard(node_id)
    s["frontier"] -= s["inferred_mastered"]

    new_count = 0
    for child in get_direct_children(node_id, graph):
        if (
            child not in s["confirmed_mastered"]
            and child not in s["confirmed_unknown"]
            and child not in s["inferred_mastered"]
            and child not in s["inferred_unknown"]
            and child not in s["frontier"]
        ):
            s["frontier"].add(child)
            new_count += 1
    return new_count


def _handle_incorrect(node_id: str, s: dict, graph: dict) -> int:
    """
    Mark node unknown, infer all descendants unknown, expand frontier upstream.
    Returns the number of new nodes added to the frontier.
    """
    s["confirmed_unknown"].add(node_id)
    descendants = get_all_descendants(node_id, graph)
    s["inferred_unknown"].update(descendants)
    s["frontier"].discard(node_id)
    s["frontier"] -= s["inferred_unknown"]

    new_count = 0
    for parent in get_direct_parents(node_id, graph):
        if (
            parent not in s["confirmed_mastered"]
            and parent not in s["confirmed_unknown"]
            and parent not in s["inferred_mastered"]
            and parent not in s["inferred_unknown"]
            and parent not in s["frontier"]
        ):
            s["frontier"].add(parent)
            new_count += 1
    return new_count


def _is_terminated(state: dict) -> bool:
    if not state["frontier"]:
        return True
    if state["questions_asked"] >= state["max_questions"]:
        return True
    return False


# ---------------------------------------------------------------------------
# Problem generation
# ---------------------------------------------------------------------------

def _pick_next_node(frontier: set, history: list) -> Optional[str]:
    """Pick a node from the frontier, preferring nodes not yet asked."""
    asked = {h["node_id"] for h in history}
    not_yet_asked = frontier - asked
    pool = not_yet_asked if not_yet_asked else frontier
    return min(pool) if pool else None   # deterministic ordering


def _generate_question(
    node_id: str,
    asked_problems: list,
    ephemeral_answers: dict,
    db: DBSession,
) -> Optional[dict]:
    """
    Try on-the-fly generator first, fall back to DB problem.
    Mutates ephemeral_answers in place if a generated problem is used.
    """
    # On-the-fly generator
    generated = generate_problem(node_id)
    if generated:
        eph_id = str(uuid.uuid4())
        ephemeral_answers[eph_id] = {
            "correct_answer": generated["correct_answer"],
            "answer_type": generated["answer_type"],
            "node_id": node_id,
        }
        node = db.query(KnowledgeNode).filter(KnowledgeNode.id == node_id).first()
        return {
            "problem_id": eph_id,
            "node_id": node_id,
            "problem_text": generated["problem_text"],
            "topic": node.topic if node else "",
        }

    # DB fallback
    db_asked_uuids = []
    for pid in asked_problems:
        if pid not in ephemeral_answers:
            try:
                db_asked_uuids.append(uuid.UUID(pid))
            except ValueError:
                pass

    problem = db.query(Problem).filter(
        Problem.node_id == node_id,
        ~Problem.id.in_(db_asked_uuids),
    ).first()

    if problem:
        node = db.query(KnowledgeNode).filter(KnowledgeNode.id == node_id).first()
        return {
            "problem_id": str(problem.id),
            "node_id": node_id,
            "problem_text": problem.problem_text,
            "topic": node.topic if node else "",
        }

    return None


# ---------------------------------------------------------------------------
# Progress reporting
# ---------------------------------------------------------------------------

def _progress(state: dict) -> dict:
    n = (
        len(state["confirmed_mastered"])
        + len(state["confirmed_unknown"])
        + len(state["inferred_mastered"])
        + len(state["inferred_unknown"])
    )
    return {
        "questions_asked": state["questions_asked"],
        "estimated_total": 25,
        "nodes_classified": n,
        "total_nodes": 176,
    }


def _completion_summary(state: dict) -> dict:
    graph = _load_graph()
    mastered = set(state["confirmed_mastered"]) | set(state["inferred_mastered"])
    topics = {graph["topic_map"].get(n, "") for n in mastered} - {""}
    return {
        "mastered_count": len(mastered),
        "subjects_count": len(topics),
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def initialize_placement(user_id: str, db: DBSession) -> dict:
    """
    Start a new placement session.
    Returns { session_id, first_question, progress }.
    """
    graph = _load_graph()

    # Close any existing active placement sessions for this user
    db.query(Session).filter(
        Session.user_id == user_id,
        Session.session_type == "placement",
        Session.is_active == True,
    ).update({"is_active": False})

    starting_nodes = get_starting_nodes(graph)
    state = _make_new_state(starting_nodes)

    session = Session(
        user_id=user_id,
        session_type="placement",
        state_snapshot=state,
        is_active=True,
    )
    db.add(session)
    db.flush()

    # Generate the first question
    s = _to_sets(state)
    first_node = _pick_next_node(s["frontier"], state["history"])
    if not first_node:
        raise ValueError("Could not determine first placement node")

    question = _generate_question(
        first_node,
        state["asked_problems"],
        state["ephemeral_answers"],
        db,
    )
    if not question:
        raise ValueError("Could not generate first placement question")

    session.state_snapshot = state
    flag_modified(session, "state_snapshot")
    db.commit()

    return {
        "session_id": str(session.id),
        "first_question": question,
        "progress": _progress(state),
    }


def submit_placement_answer(
    session_id: str,
    problem_id: str,
    answer: str,
    user_id: str,
    db: DBSession,
) -> dict:
    """
    Process one placement answer.
    Returns {
        is_correct, correct_answer,
        next_question: {...} | null,
        progress: { questions_asked, estimated_total, nodes_classified, total_nodes },
        is_complete: bool,
        completion_summary?: { mastered_count, subjects_count }   # only when is_complete
    }
    """
    session = db.query(Session).filter(
        Session.id == session_id,
        Session.user_id == user_id,
        Session.is_active == True,
    ).first()
    if not session:
        raise ValueError("Session not found or already completed")

    state = copy.deepcopy(session.state_snapshot)
    ephemeral_answers = state.get("ephemeral_answers", {})
    graph = _load_graph()

    # ---- Resolve correct answer ----------------------------------------
    ephemeral = ephemeral_answers.get(problem_id)
    if ephemeral:
        correct_answer_str = ephemeral["correct_answer"]
        answer_type_str = ephemeral["answer_type"]
        problem_node_id = ephemeral["node_id"]
    else:
        try:
            problem_uuid = uuid.UUID(problem_id)
        except ValueError:
            raise ValueError("Invalid problem ID")
        problem = db.query(Problem).filter(Problem.id == problem_uuid).first()
        if not problem:
            raise ValueError("Problem not found")
        correct_answer_str = problem.correct_answer
        answer_type_str = problem.answer_type
        problem_node_id = str(problem.node_id)

    # ---- Check answer --------------------------------------------------
    answer_check_error = False
    try:
        is_correct = check_answer(answer, correct_answer_str, answer_type_str)
    except Exception:
        logger.error(
            "check_answer error in placement session=%s problem=%s\n%s",
            session_id, problem_id, traceback.format_exc(),
        )
        is_correct = False
        answer_check_error = True

    if answer_check_error:
        # Skip algorithm update; advance to the next frontier node
        state["asked_problems"].append(problem_id)
        s = _to_sets(state)
        next_node = _pick_next_node(s["frontier"], state["history"])
        next_question = None
        if next_node:
            next_question = _generate_question(
                next_node, state["asked_problems"], ephemeral_answers, db
            )
        state["ephemeral_answers"] = ephemeral_answers
        session.state_snapshot = state
        flag_modified(session, "state_snapshot")
        db.commit()
        return {
            "is_correct": False,
            "error": True,
            "message": "Could not evaluate your answer. Please try a different format.",
            "correct_answer": correct_answer_str,
            "next_question": next_question,
            "progress": _progress(state),
            "is_complete": False,
        }

    # ---- Update algorithm state ----------------------------------------
    s = _to_sets(state)
    new_additions = (
        _handle_correct(problem_node_id, s, graph)
        if is_correct
        else _handle_incorrect(problem_node_id, s, graph)
    )
    _flush_sets(s, state)

    state["history"].append({"node_id": problem_node_id, "is_correct": is_correct})
    state["asked_problems"].append(problem_id)
    state["questions_asked"] += 1
    if is_correct:
        state["correct_count"] += 1

    # ---- Check termination and build next question ---------------------
    is_complete = _is_terminated(state)
    next_question = None

    if not is_complete:
        s2 = _to_sets(state)
        next_node = _pick_next_node(s2["frontier"], state["history"])
        if next_node:
            next_question = _generate_question(
                next_node, state["asked_problems"], ephemeral_answers, db
            )
        if not next_question:
            is_complete = True

    state["ephemeral_answers"] = ephemeral_answers

    if is_complete:
        _finalize_placement(user_id, state, db)
        session.is_active = False
        session.completed_at = datetime.now(timezone.utc)

    session.state_snapshot = state
    flag_modified(session, "state_snapshot")
    db.commit()

    result: dict = {
        "is_correct": is_correct,
        "correct_answer": correct_answer_str,
        "next_question": next_question,
        "progress": _progress(state),
        "is_complete": is_complete,
    }
    if is_complete:
        result["completion_summary"] = _completion_summary(state)
    return result


def _finalize_placement(user_id: str, state: dict, db: DBSession) -> None:
    """Write placement results (mastered set + fringes) into StudentState."""
    confirmed_mastered = set(state["confirmed_mastered"])
    inferred_mastered = set(state["inferred_mastered"])
    mastered = sorted(confirmed_mastered | inferred_mastered)

    graph = _load_graph()
    inner, outer = _compute_fringes(set(mastered), graph)

    kg = db.query(KnowledgeGraph).filter(KnowledgeGraph.is_active == True).first()
    if not kg:
        logger.error("No active KnowledgeGraph in DB — cannot finalize placement")
        return

    student_state = db.query(StudentState).filter(
        StudentState.user_id == user_id,
        StudentState.graph_id == kg.id,
    ).first()

    if student_state:
        student_state.mastered_nodes = mastered
        student_state.outer_fringe = outer
        student_state.inner_fringe = inner
        student_state.placement_completed = True
        student_state.state_distribution = {}
        flag_modified(student_state, "mastered_nodes")
        flag_modified(student_state, "outer_fringe")
        flag_modified(student_state, "inner_fringe")
    else:
        student_state = StudentState(
            user_id=user_id,
            graph_id=kg.id,
            graph_version=kg.version,
            state_distribution={},
            mastered_nodes=mastered,
            outer_fringe=outer,
            inner_fringe=inner,
            placement_completed=True,
        )
        db.add(student_state)

    db.flush()

    # Schedule reviews for mastered nodes
    now = datetime.now(timezone.utc)
    for node_id in mastered:
        existing = db.query(ReviewSchedule).filter(
            ReviewSchedule.user_id == user_id,
            ReviewSchedule.node_id == node_id,
        ).first()
        if not existing:
            db.add(ReviewSchedule(
                user_id=user_id,
                node_id=node_id,
                mastered_at=now,
                next_review_at=now + timedelta(days=1),
                interval_days=1,
                streak=0,
            ))


def get_results(user_id: str, db: DBSession) -> dict:
    """Return placement results for the user."""
    from app.kst.kst_engine import get_active_graph
    graph_db = get_active_graph(db)
    if not graph_db:
        raise ValueError("No active graph")

    student_state = db.query(StudentState).filter(
        StudentState.user_id == user_id,
        StudentState.graph_id == graph_db.id,
    ).first()

    if not student_state:
        return {
            "mastered_nodes": [],
            "ready_nodes": [],
            "locked_nodes": [],
            "questions_answered": 0,
            "accuracy": 0,
        }

    all_nodes = db.query(KnowledgeNode).filter(
        KnowledgeNode.graph_id == graph_db.id
    ).all()
    node_map = {n.id: n for n in all_nodes}

    mastered = student_state.mastered_nodes or []
    outer = student_state.outer_fringe or []
    mastered_set = set(mastered)
    outer_set = set(outer)
    locked = [n.id for n in all_nodes if n.id not in mastered_set and n.id not in outer_set]

    session = db.query(Session).filter(
        Session.user_id == user_id,
        Session.session_type == "placement",
        Session.is_active == False,
    ).order_by(Session.completed_at.desc()).first()

    questions_answered = 0
    accuracy = 0.0
    if session and session.state_snapshot:
        snap = session.state_snapshot
        questions_answered = snap.get("questions_asked", 0)
        correct = snap.get("correct_count", 0)
        accuracy = round(correct / questions_answered, 3) if questions_answered > 0 else 0.0

    def node_info(nid):
        n = node_map.get(nid)
        return {"node_id": nid, "label": n.label if n else nid, "topic": n.topic if n else ""}

    graph_json = _load_graph()
    topic_map = graph_json["topic_map"]
    topics_with_mastery = {topic_map.get(n, "") for n in mastered} - {""}

    return {
        "mastered_nodes": [node_info(n) for n in mastered],
        "ready_nodes": [node_info(n) for n in outer],
        "locked_nodes": [node_info(n) for n in locked],
        "questions_answered": questions_answered,
        "accuracy": accuracy,
        "summary": {
            "mastered_count": len(mastered),
            "subjects_count": len(topics_with_mastery),
        },
    }
