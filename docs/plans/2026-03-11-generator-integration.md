# Generator Integration Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire 6 pre-written generator modules into `problem_generator.py`, then seed the database with all 176 nodes so Fisher App can generate practice problems for the full curriculum.

**Architecture:** All 6 generator files (algebra, precalculus, calculus, linear_algebra, probability, statistics) already exist at `backend/app/services/generators/` with correctly formatted GENERATORS dicts. The `knowledge_graph.json` (176 nodes, 276 edges) and `hierarchy.json` (176 node IDs) are already complete. The DB currently has 30 nodes; `seed_knowledge_graph.py` re-seeds from `knowledge_graph.json`.

**Tech Stack:** Python/FastAPI, PostgreSQL, Docker Compose

---

## Fact Check (pre-flight)

| Artifact | Status |
|---|---|
| `knowledge_graph.json` | ✅ 176 nodes, 276 surmise_relations |
| `hierarchy.json` | ✅ 176 node IDs, edges |
| `generators/algebra.py` | ✅ 12 nodes, correct format |
| `generators/precalculus.py` | ✅ 5 nodes |
| `generators/calculus.py` | ✅ 20 nodes (calc-* + mv-*) |
| `generators/linear_algebra.py` | ✅ 21 nodes |
| `generators/probability.py` | ✅ 39 nodes |
| `generators/statistics.py` | ✅ 49 nodes |
| Total generator coverage | ✅ 30 + 12 + 5 + 20 + 21 + 39 + 49 = 176 |
| DB | ❌ 30 nodes — needs re-seed |
| `problem_generator.py` GENERATORS | ❌ 30 nodes — needs 6 imports |

---

## Task 1: Wire Generator Modules into problem_generator.py

**Files:**
- Modify: `backend/app/services/problem_generator.py:685` (after closing brace of GENERATORS dict)

- [ ] **Step 1: Add 6 imports + GENERATORS.update() calls after the GENERATORS dict**

Insert after line 685 (the closing `}` of GENERATORS):

```python
# ─── Extended generators (146 additional nodes) ───────────────────────────────
from .generators.algebra import GENERATORS as _ALGEBRA_GENERATORS
from .generators.precalculus import GENERATORS as _PRECALC_GENERATORS
from .generators.calculus import GENERATORS as _CALC_GENERATORS
from .generators.linear_algebra import GENERATORS as _LINALG_GENERATORS
from .generators.probability import GENERATORS as _PROB_GENERATORS
from .generators.statistics import GENERATORS as _STAT_GENERATORS

GENERATORS.update(_ALGEBRA_GENERATORS)
GENERATORS.update(_PRECALC_GENERATORS)
GENERATORS.update(_CALC_GENERATORS)
GENERATORS.update(_LINALG_GENERATORS)
GENERATORS.update(_PROB_GENERATORS)
GENERATORS.update(_STAT_GENERATORS)
```

- [ ] **Step 2: Verify generator count in container**

```bash
docker compose exec backend python -c "
from app.services.problem_generator import GENERATORS
print('Total generators:', len(GENERATORS))
assert len(GENERATORS) == 176, f'Expected 176, got {len(GENERATORS)}'
print('OK')
"
```
Expected: `Total generators: 176`

- [ ] **Step 3: Spot-check 3 generators (one per new group)**

```bash
docker compose exec backend python -c "
from app.services.problem_generator import generate_problem
for node in ['alg-slope', 'calc-deriv-power', 'prob-bayes', 'stat-ci-z', 'linalg-eigenvalues']:
    p = generate_problem(node)
    assert p is not None, f'No generator for {node}'
    assert 'problem_text' in p
    assert 'correct_answer' in p
    assert 'hints' in p
    print(f'{node}: OK — {p[\"problem_text\"][:60]}')
"
```

---

## Task 2: Seed the Database

- [ ] **Step 4: Run the seed script**

```bash
docker compose exec backend python scripts/seed_knowledge_graph.py
```
Expected output ends with: `Seeded graph with 176 nodes and 276 edges.`

- [ ] **Step 5: Confirm DB node count**

```bash
docker compose exec backend python -c "
from app.database import SessionLocal
from app.models.knowledge import KnowledgeNode
db = SessionLocal()
count = db.query(KnowledgeNode).count()
db.close()
print('DB nodes:', count)
assert count == 176
"
```

---

## Task 3: Commit and Push

- [ ] **Step 6: Commit**

```bash
git add backend/app/services/problem_generator.py
git commit -m "feat: wire 6 generator modules into problem_generator (176 nodes total)"
```

- [ ] **Step 7: Push**

```bash
git push origin main
```
