# Claude Code Instructions — BerkeleyStats Tutor (Fisher App)

## START HERE

You are picking up development of this project at **Phase 4: API and Database**. Phases 1-3 are complete. Read this document fully before beginning any work.

---

## Project Summary

**BerkeleyStats Tutor** is an open-source, adaptive learning app that helps UC Berkeley undergraduate statistics students build foundational skills from algebra through mathematical statistics. It presents randomly generated problems, manages cognitive load through evidence-based instructional sequencing, and tracks mastery over time using spaced repetition.

**License:** MIT (Copyright 2026, John Jacobsen)

---

## Architecture

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Core logic** | R package | Problem generation, answer checking, adaptive algorithms, spaced repetition, knowledge graph |
| **API** | Plumber (R) | RESTful JSON endpoints exposing R package functionality |
| **Frontend** | React (JS/TS) | Student-facing UI, math rendering (KaTeX/MathJax), dashboard |
| **Database** | PostgreSQL | Students, sessions, attempts, mastery, spaced repetition schedules |
| **DevOps** | Docker + Docker Compose | Orchestrates PostgreSQL, Plumber API, React dev server |

**Key principles:**
- Clean separation of concerns (R package / API / frontend / database are independent)
- Problem templates are **data, not hardcoded functions** — a generic engine reads templates and produces problems
- All API responses return structured JSON (problem statement, solution steps, answer, topic ID, difficulty, prerequisites)
- R package must be usable **standalone from the R console** (no web app required)
- Database schema includes `course_id` and `institution_id` from day one (future-proofing)

---

## What's Done (Phase 1 - COMPLETE)

### Files that exist:
- `PROJECT_BRIEF.md` — Full project specification (read this for complete details)
- `r-package/inst/knowledge_graph/algebra.yml` — Complete algebra knowledge graph
- `.gitignore` — Configured for R, Node.js, Docker, PostgreSQL, IDEs
- `LICENSE` — MIT
- `README.md` — Placeholder

### Algebra Knowledge Graph (algebra.yml):
**8 active topic nodes** with full definitions (prerequisites, skills, 5 difficulty levels with examples):
1. **Fraction Arithmetic** — no prerequisites
2. **Exponent Rules** — requires: fraction_arithmetic
3. **Order of Operations** — requires: fraction_arithmetic, exponent_rules
4. **Summation Notation** — requires: order_of_operations
5. **Solving Equations** — requires: fraction_arithmetic, exponent_rules
6. **Logarithms & Exponentials** — requires: exponent_rules, solving_equations
7. **Combinatorics** — requires: fraction_arithmetic, exponent_rules
8. **Geometric Series** — requires: fraction_arithmetic, exponent_rules

**5 planned nodes** (graph structure only, no content yet):
- Binomial Theorem, Double Sums, Product Notation, Taylor Series Recognition, Variance Formula Manipulation, Delta Method Chain

### Difficulty levels (all 8 nodes use these):
1. **Recognition** — identify/recall
2. **Routine** — straightforward 1-2 step problems
3. **Multi-step** — chains several skills
4. **Transfer** — applies skill in unfamiliar context
5. **Synthesis** — combines multiple topics

---

## What's Done (Phase 2 - COMPLETE)

### Problem Engine R Package (`fisherapp`):
- **40 problem templates** (8 topics × 5 difficulties) — all declarative, template-driven
- Generic `generate_problem(topic_id, difficulty)` engine reads templates and produces randomized problems
- Answer checker with equivalence detection (fractions, decimals, LaTeX)
- Math utilities (GCD, LCM, fraction arithmetic, combinatorics)
- LaTeX formatting utilities
- JSON serialization for API layer
- 266 tests passing

### R Package files:
- `R/problem_engine.R` — `generate_problem()`, `draw_params()`, `problem_to_json()`
- `R/answer_checker.R` — `check_answer()`, `compare_answers()`, `parse_student_answer()`
- `R/template_registry.R` — `register_template()`, `get_templates()`, `list_templates()`
- `R/knowledge_graph.R` — `load_knowledge_graph()`, `get_topic()`, `get_prerequisites()`, `get_active_topics()`, `get_topic_order()`
- `R/math_utils.R` — `gcd()`, `lcd()`, `simplify_fraction()`, `frac_add/sub/mul/div()`, `choose_safe()`, `perm()`
- `R/latex_utils.R` — `latex_frac()`, `latex_exp()`, `latex_sum()`
- `R/templates_*.R` — 8 template files (one per topic)

---

## What's Done (Phase 3 - COMPLETE)

### Student Model & Adaptive Logic:
- **Modified SM-2 spaced repetition** — per-topic ease factor, interval, and review scheduling
- **Mastery criteria** — 85%+ accuracy over last 10 problems, across 2+ sessions, at difficulty 3+
- **Adaptive difficulty** — promotes on 75%+ recent accuracy, demotes on 25%- accuracy
- **Next-problem selection** — prioritizes: due reviews > in-progress topics > new topics with prereqs met
- **Computer-Adaptive Placement Test** — 15-25 questions, walks knowledge graph in topological order
- **Stuck-loop detection** — 3+ consecutive wrong triggers: reduce difficulty, route to prerequisite, or offer worked example
- **Session management** — start/end sessions, submit answers, full orchestration pipeline
- **Simulation** — `simulate_session()` for testing, `interactive_session()` for console use
- 426 total tests passing (160 new Phase 3 tests)

### Phase 3 R Package files:
- `R/student_model.R` — `create_student_model()`, `get_topic_state()`, `student_progress()`
- `R/sm2_engine.R` — `sm2_update()`, `map_quality()`, `is_due_for_review()`
- `R/mastery.R` — `evaluate_mastery()`, `prerequisites_met()`
- `R/adaptive_difficulty.R` — `adjust_difficulty()`
- `R/next_problem.R` — `select_next_topic()`, `next_problem_for_student()`
- `R/cat_placement.R` — `run_placement_test()`, `interactive_placement()`
- `R/session.R` — `start_session()`, `get_next_problem()`, `submit_answer()`, `end_session()`, `simulate_session()`, `interactive_session()`

---

## What to Build Now (Phase 2: Problem Engine)

### Goal
Build the core R package so that a call like:
```r
generate_problem("fraction_arithmetic", difficulty = 3)
```
returns a structured problem object with:
- Randomized problem statement (LaTeX format)
- Full worked solution (step by step, LaTeX format)
- Correct final answer
- Topic ID and difficulty level
- Prerequisite skills

### Deliverables

1. **R Package Structure**
   - `DESCRIPTION`, `NAMESPACE`, `R/` directory
   - Package name: `fisherapp` (or similar)
   - Must be installable via `devtools::install()`

2. **Problem Template System**
   - Templates are **declarative data structures** (not individual hardcoded functions)
   - A generic engine reads templates and produces randomized problem instances
   - Each of the 8 active algebra topics needs templates for all 5 difficulty levels
   - That's 40 template types total (8 topics x 5 difficulties)

3. **For each generated problem, return a structured list:**
   ```r
   list(
     problem_id = "uuid",
     topic_id = "fraction_arithmetic",
     difficulty = 3,
     statement = "Compute \\frac{3}{4} - \\frac{1}{6} \\times \\frac{2}{5} and simplify.",
     solution_steps = c(
       "Step 1: ...",
       "Step 2: ...",
       "Step 3: ..."
     ),
     answer = "\\frac{13}{20}",
     prerequisites = c()
   )
   ```

4. **Answer-checking logic**
   - Compare student answer to correct answer
   - Handle equivalent forms (e.g., 1/2 = 2/4 = 0.5)
   - Return TRUE/FALSE plus the worked solution

5. **Unit tests**
   - Every problem template generates valid problems
   - Generated solutions are mathematically correct
   - Answer checking works for equivalent forms
   - Use `testthat` framework

### Important Design Constraints

- **Problems must be representative** of what Berkeley stats students actually encounter
- **All math in LaTeX format** (will be rendered by KaTeX/MathJax in frontend)
- **Randomized parameters** — same template, different numbers each time
- **Worked solutions must be step-by-step** — not just the final answer
- **The R package must work standalone** from the R console without any web infrastructure
- **Start with the 8 active topics only** — don't build templates for planned nodes yet

---

## Development Phases (Full Roadmap)

| Phase | Description | Status |
|-------|------------|--------|
| 1 | Knowledge Graph | COMPLETE |
| 2 | Problem Engine (R Package) | COMPLETE |
| 3 | Student Model & Adaptive Logic (R Package) | COMPLETE |
| 4 | API and Database | **START HERE** |
| 5 | Frontend (React) | Not started |
| 6 | Testing and Polish | Not started |

### Phase 3 Preview (so you can design Phase 2 with it in mind):
- Modified SM-2 spaced repetition algorithm
- Mastery criteria: 85%+ accuracy over last N problems, across 2+ spaced sessions, at difficulty 3+
- Next-problem selection logic
- Computer-adaptive placement test (15-25 questions)
- Stuck-loop detection (offer worked examples, route to prerequisites)

### Phase 4 Preview:
- Plumber API wrapping R package
- PostgreSQL tables: students, sessions, problem_attempts, mastery_states, spaced_repetition_schedules, courses, institutions
- Endpoints: create student, start session, get problem, submit answer, get next problem, check progress

---

## Feedback & Error Handling Philosophy

When a student answers incorrectly:
- Mark as wrong
- Present full worked solution (step by step)
- Do NOT attempt to pinpoint the exact error step (deliberate design choice)
- May offer a simpler scaffolded version of the same problem type
- Hints degrade gracefully: nudge -> bigger hint -> full solution

---

## Git Info

Repository has 3 commits. Main branch. Use conventional, descriptive commit messages.

---

## How to Start

1. Read `PROJECT_BRIEF.md` for the complete specification
2. Read `r-package/inst/knowledge_graph/algebra.yml` to understand the 8 topics and their difficulty levels
3. Set up the R package structure in `r-package/`
4. Build the template engine and problem generator
5. Start with the simplest topic (fraction_arithmetic) and get the full pipeline working before expanding to all 8 topics
6. Write tests as you go (TDD preferred)

**Use the superpowers plugin** — it will help with brainstorming, planning, and structured development.
