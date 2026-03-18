# Fisher App 3.0 — Phase 3+4 Integration

## What this task is

We have completed a major curriculum expansion offline. You need to integrate it into the app
and push everything to GitHub. This is a file deployment + wiring task — **no architecture changes**.

---

## Files to deploy

All files are in the same folder as this prompt. Here is exactly where each one goes:

### Generator files (6 Python files → 1 new directory)

Create the directory if it doesn't exist:
```
backend/app/services/generators/
```

Deploy these files into it:

| Source file | Destination |
|-------------|-------------|
| `__init__.py` | `backend/app/services/generators/__init__.py` |
| `algebra.py` | `backend/app/services/generators/algebra.py` |
| `precalculus.py` | `backend/app/services/generators/precalculus.py` |
| `calculus.py` | `backend/app/services/generators/calculus.py` |
| `linear_algebra.py` | `backend/app/services/generators/linear_algebra.py` |
| `probability.py` | `backend/app/services/generators/probability.py` |
| `statistics.py` | `backend/app/services/generators/statistics.py` |

### Knowledge graph

| Source file | Destination |
|-------------|-------------|
| `knowledge_graph.json` | `backend/data/knowledge_graph.json` |

This **replaces** the existing file. The new file has 176 nodes and 276 edges (up from ~30 nodes).

### Hierarchy (frontend display graph)

| Source file | Destination |
|-------------|-------------|
| `hierarchy.json` | `frontend/src/data/hierarchy.json` |

This **replaces** the existing file.

---

## Wiring: patch `problem_generator.py`

File: `backend/app/services/problem_generator.py`

### Step 1 — Add imports

Find the existing import block at the top of the file and add these 6 lines after the
existing imports (but before the `GENERATORS` dict):

```python
from .generators.algebra import GENERATORS as ALGEBRA_GENERATORS
from .generators.precalculus import GENERATORS as PRECALC_GENERATORS
from .generators.calculus import GENERATORS as CALC_GENERATORS
from .generators.linear_algebra import GENERATORS as LINALG_GENERATORS
from .generators.probability import GENERATORS as PROB_GENERATORS
from .generators.statistics import GENERATORS as STAT_GENERATORS
```

### Step 2 — Merge into GENERATORS dict

Find the line where the `GENERATORS` dict is defined (it looks like `GENERATORS = { ... }`).
Immediately after the closing `}` of that dict, add:

```python
GENERATORS.update(ALGEBRA_GENERATORS)
GENERATORS.update(PRECALC_GENERATORS)
GENERATORS.update(CALC_GENERATORS)
GENERATORS.update(LINALG_GENERATORS)
GENERATORS.update(PROB_GENERATORS)
GENERATORS.update(STAT_GENERATORS)
```

Do not remove any existing entries from the `GENERATORS` dict.

---

## Verification

After making changes, run:

```bash
python3 -c "
import sys
sys.path.insert(0, 'backend')
# Quick import check (no DB needed)
from app.services.generators.algebra import GENERATORS as A
from app.services.generators.precalculus import GENERATORS as P
from app.services.generators.calculus import GENERATORS as C
from app.services.generators.linear_algebra import GENERATORS as L
from app.services.generators.probability import GENERATORS as PR
from app.services.generators.statistics import GENERATORS as S
total = len(A) + len(P) + len(C) + len(L) + len(PR) + len(S)
print(f'New generators loaded: {total}')
for gen_dict, name in [(A,'algebra'),(P,'precalc'),(C,'calculus'),(L,'linalg'),(PR,'prob'),(S,'stat')]:
    sample = list(gen_dict.values())[0]()
    print(f'  {name}: {len(gen_dict)} nodes — sample answer: {sample[\"correct_answer\"]}')
print('All OK' if total == 146 else f'WARNING: expected 146, got {total}')
"
```

Expected output: `New generators loaded: 146` with no errors.

---

## Seed the database

After verification, run the seed script to push the new knowledge graph into the database:

```bash
docker compose run --rm backend python scripts/seed_knowledge_graph.py
```

Expected output: `Seeded graph with 176 nodes and 276 edges.`

If the Docker environment isn't running, note this for later and move on.

---

## Git

Commit and push everything:

```bash
git add \
  backend/app/services/generators/ \
  backend/app/services/problem_generator.py \
  backend/data/knowledge_graph.json \
  frontend/src/data/hierarchy.json

git commit -m "Phase 3+4: 146 new problem generators + 176-node knowledge graph

- Added backend/app/services/generators/ package with 6 generator modules
  covering algebra (12), precalculus (5), calculus (20), linear algebra (21),
  probability (39), and statistics (49) nodes
- Updated knowledge_graph.json: 176 nodes, 276 edges, full labels and topics
- Updated hierarchy.json: matching 176-node frontend display graph
- Wired generators into problem_generator.py via GENERATORS.update() calls"

git push
```

---

## What NOT to change

- Do not modify any existing entries in `GENERATORS` in `problem_generator.py`
- Do not modify `seed_knowledge_graph.py`, `generate_problems.py`, or any other seed scripts
- Do not modify any frontend components
- Do not modify `answer_checker.py`
- The `__init__.py` in the generators directory should remain empty (it just marks the directory as a Python package)

---

## Summary of what was built

| File | Nodes | Topics covered |
|------|-------|----------------|
| `algebra.py` | 12 | Linear graphs, slope, systems, inequalities, polynomials, factoring, radicals |
| `precalculus.py` | 5 | Functions, domain/range, composition, inverses, polynomials |
| `calculus.py` | 20 | Limits, derivatives (5 rules), optimization, integration (5 techniques), series, multivariable |
| `linear_algebra.py` | 21 | Vectors through SVD |
| `probability.py` | 39 | Sample spaces through CLT |
| `statistics.py` | 49 | Sampling distributions through causal inference |
| `knowledge_graph.json` | 176 nodes, 276 edges | Full curriculum graph for DB seeding |

Each generator: zero-argument function, returns `{problem_text, correct_answer, answer_type, difficulty, hints[3]}`.
All answers are numeric or simple fractions compatible with the existing `answer_checker.py`.
