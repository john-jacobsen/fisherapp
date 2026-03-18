# Fisher App — Architecture Audit for Problem Generator Expansion

I am planning to expand Fisher App's problem generator system from 27 nodes to 146 new nodes
across 6 subject groups (Algebra, Precalculus, Calculus, Linear Algebra, Probability, Statistics).
Before writing any code, I need a clear picture of how the existing system actually works.

Please do the following and paste the results back to me:

---

## 1. Directory tree

Run this from the project root and paste the full output:

```bash
find . -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/oatutor/*' \
  -not -path '*/__pycache__/*' -not -path '*/venv/*' -not -path '*/.venv/*' \
  | sort | head -200
```

---

## 2. Backend data models

Paste the full contents of these files (search if paths differ):

- `backend/app/models/content.py`   — Problem, Hint, and any related models
- `backend/app/models/knowledge.py` — KnowledgeNode, KnowledgeEdge, KnowledgeGraph

---

## 3. Answer checker

Find and paste the answer-checking logic. Search with:

```bash
grep -r "correct_answer\|check_answer\|answer_type\|symbolic\|numeric" backend/app \
  --include="*.py" -l
```

Then paste the most relevant file(s).

---

## 4. Hint system

Answer these questions:
- Do Hint rows currently exist in the database for any nodes? (`SELECT COUNT(*) FROM hints;`)
- How are hints surfaced in the frontend? (search for "hint" in the frontend src)
- Is the 3-level hint system (level 1/2/3) already wired up in the UI, or is it planned?

---

## 5. How generate_problems.py is invoked

- Is it a one-time seed script, or called at runtime when the DB is low on problems?
- Is there a scheduler, a FastAPI endpoint, or a docker-compose command that calls it?
- Paste any relevant lines from `docker-compose.yml` or a Makefile that reference it.

---

## 6. AI tutor proxy

Find and paste the AI tutor route. Search with:

```bash
grep -r "tutor\|proxy\|anthropic\|openai\|BYOK\|api_key" backend/app --include="*.py" -l
```

Paste the relevant file. I need to understand: does the tutor already have access to the
problem statement and correct answer, or does it operate blind?

---

## 7. knowledge_graph.json vs hierarchy.json

- What is the current format of `backend/data/knowledge_graph.json`? Paste the first node
  entry in full (with all fields).
- Does `hierarchy.json` need to be converted into `knowledge_graph.json` format before
  seeding, or are they the same format?

---

## 8. Any existing expanded generators

```bash
find . -name "*.py" | xargs grep -l "alg-\|calc-\|linalg-\|prob-\|stat-" 2>/dev/null
```

Paste results — I want to know if any work has already started on the new nodes.

---

That's everything. Paste all output back and I'll use it to finalize the architecture plan
before writing a single generator.
