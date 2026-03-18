# Fisher App 3.0 — Implementation Specification

## For Claude Code: Read this entire document before writing any code.

---

## 1. PROJECT OVERVIEW

**Fisher App 3.0** is an adaptive algebra tutoring web application for UC Berkeley statistics students. It uses Knowledge Space Theory (KST) with BLIM (Basic Local Independence Model) Bayesian updating to model student knowledge, select optimal practice problems, and navigate prerequisite-aware learning paths.

**Target Users:** Undergraduate statistics students needing algebra prerequisite review.

**Core Value Proposition:** Unlike flat quiz apps, Fisher App models the dependency structure between math skills. It knows that a student who fails logarithms may actually need to review exponent rules first, and it routes them there automatically.

### What Makes This Different from a Quiz App

1. **Knowledge Space Theory** models all feasible knowledge states (combinations of skills a student could have, respecting prerequisites)
2. **BLIM Bayesian updating** maintains a probability distribution over those states, updating after every response
3. **Fringe-based navigation** identifies exactly which skills a student is ready to learn next (outer fringe) and which are their current high points (inner fringe)
4. **Adaptive assessment** selects maximally informative placement test questions using maximum-discrimination item selection with entropy-based termination

---

## 2. TECH STACK

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | React 18+ with Vite | Single-page app, responsive design |
| Backend | Python 3.11+ with FastAPI | REST API, async support |
| Database | PostgreSQL 15+ | With SQLAlchemy ORM + Alembic migrations |
| Math Input | MathLive | LaTeX-based math keyboard, works on mobile |
| KST Engine | Vanderbilt `kst_utils.py` | Pure Python, no external deps. See Section 8. |
| Auth | bcrypt + JWT tokens | Simple email/password, no OAuth for v1 |
| Containerization | Docker Compose | Dev environment; Railway-ready for deployment |
| Content | OATutor (CC BY 4.0) | Algebra problems with structured hint pathways |

**One frontend language (JavaScript/React), one backend language (Python), one database. No R.**

---

## 3. DIRECTORY STRUCTURE

```
C:\Users\jjcas\Desktop\Fisher App\Fisher App 3.0\
├── docker-compose.yml
├── .env.example
├── README.md
├── PROMPT.md                          # This file
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/                  # Migration files
│   ├── app/
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Settings from environment
│   │   ├── database.py                # SQLAlchemy engine + session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py                # User, Instructor, Course, Enrollment
│   │   │   ├── knowledge.py           # KnowledgeGraph, KnowledgeNode, Edge
│   │   │   ├── progress.py            # StudentState, Session, ResponseLog, ReviewSchedule
│   │   │   └── content.py             # Problem, Hint, Lesson, WorkedExample
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                # Register, login, token refresh
│   │   │   ├── placement.py           # Start/submit/complete placement test
│   │   │   ├── practice.py            # Get problem, submit answer, get hints
│   │   │   ├── dashboard.py           # Knowledge map state, fringe, reviews
│   │   │   ├── lessons.py             # Lesson + worked example content
│   │   │   ├── review.py              # Review queue, submit review
│   │   │   └── settings.py            # User profile, preferences, AI key test
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── kst_engine.py          # Wrapper around kst_utils functions
│   │   │   ├── placement_service.py   # Adaptive assessment orchestration
│   │   │   ├── practice_service.py    # Problem selection, answer checking, BLIM update
│   │   │   ├── review_service.py      # SM-2 scheduling, decay logic
│   │   │   └── answer_checker.py      # Symbolic math answer verification
│   │   ├── kst/
│   │   │   ├── __init__.py
│   │   │   └── kst_utils.py           # Vanderbilt KST math engine (copied in)
│   │   └── theme.py                   # Color/style constants for consistent theming
│   └── data/
│       ├── knowledge_graph.json       # The knowledge graph definition
│       ├── problems/                  # Problem JSON files by node
│       └── lessons/                   # Lesson content by node
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── public/
│   └── src/
│       ├── main.jsx
│       ├── App.jsx                    # Router setup
│       ├── theme.js                   # All colors, fonts, spacing in one file
│       ├── api/
│       │   └── client.js              # Axios/fetch wrapper with JWT handling
│       ├── contexts/
│       │   ├── AuthContext.jsx         # User auth state
│       │   └── AIContext.jsx           # BYOK API key state (localStorage)
│       ├── components/
│       │   ├── NavBar.jsx
│       │   ├── MathInput.jsx          # MathLive wrapper component
│       │   ├── MasteryMeter.jsx       # BLIM posterior progress bar
│       │   ├── KnowledgeGraph.jsx     # Interactive graph visualization
│       │   ├── KnowledgeList.jsx      # List view of nodes by topic
│       │   ├── HintPanel.jsx          # Structured hints + AI button
│       │   ├── AIChat.jsx             # AI chat interface (BYOK)
│       │   ├── ReviewBanner.jsx       # Dashboard review notification
│       │   ├── ReviewModal.jsx        # Two-step review reminder modal
│       │   ├── VideoEmbed.jsx         # YouTube/external video player
│       │   └── ProgressSteps.jsx      # Lesson → Examples → Practice indicator
│       └── pages/
│           ├── LoginPage.jsx
│           ├── RegisterPage.jsx
│           ├── PlacementIntro.jsx
│           ├── PlacementQuestion.jsx
│           ├── PlacementResults.jsx
│           ├── Dashboard.jsx
│           ├── LessonPage.jsx
│           ├── WorkedExamplesPage.jsx
│           ├── PracticePage.jsx
│           ├── ScoreReport.jsx
│           ├── ReviewQueue.jsx
│           ├── AISetupPage.jsx
│           └── SettingsPage.jsx
│
└── scripts/
    ├── seed_knowledge_graph.py        # Load knowledge_graph.json into DB
    ├── import_oatutor_content.py      # Convert OATutor problems to our format
    └── generate_problems.py           # Python parameterized problem generators
```

---

## 4. REFERENCE CODEBASES

Previous attempts and reference projects are available at these locations. Consult them for patterns and reusable ideas, but do NOT copy code directly — this is a clean-slate build.

| Reference | Location | What to Look At |
|-----------|----------|----------------|
| Fisher App 1.0 | `C:\Users\jjcas\Desktop\Fisher App\Fisher App 1.0` | MathLive integration patterns, React component structure |
| Fisher App 2.0 | `C:\Users\jjcas\Desktop\Fisher App\Fisher App 2.0` | Problem generator logic (R → convert to Python), UI patterns |
| Vanderbilt knowledge-spaces | `C:\Users\jjcas\Desktop\Fisher App\Fisher App 2.0\projects\knowledge-spaces` | `kst_utils.py` (copy this file), JSON schema, Claude Code skills |
| KST-Learning-Path | `C:\Users\jjcas\Desktop\Fisher App\Fisher App 2.0\projects\kst-learning-path` | Session flow patterns, fringe selection UX (reference only, no license) |
| OATutor | `https://github.com/CAHLR/OATutor` | Clone into project directory if needed. CC BY 4.0 algebra content in `content/` directory. |

---

## 5. DATABASE SCHEMA

**Note on table creation order:** Tables reference each other across subsections (e.g., `courses` references `knowledge_graphs`, `response_logs` references `problems`). When creating Alembic migrations, ensure tables are created in dependency order: knowledge_graphs → knowledge_nodes → knowledge_edges → users → courses → course_enrollments → student_states → sessions → problems → hints → lessons → worked_examples → response_logs → review_schedules.

### 5.1 Users & Courses

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',  -- 'student' or 'instructor'
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Courses (instructor sections — v2 feature, but schema exists now)
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    instructor_id UUID REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,      -- e.g. "STAT-20-FA26"
    graph_id UUID REFERENCES knowledge_graphs(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enrollments
CREATE TABLE course_enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    enrolled_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(student_id, course_id)
);
```

### 5.2 Knowledge Graph

```sql
-- Versioned knowledge graph
CREATE TABLE knowledge_graphs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version INTEGER NOT NULL DEFAULT 1,
    graph_json JSONB NOT NULL,             -- Full graph per Vanderbilt schema
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Denormalized nodes for efficient querying
CREATE TABLE knowledge_nodes (
    id VARCHAR(50) PRIMARY KEY,            -- e.g. "frac-simplify"
    graph_id UUID REFERENCES knowledge_graphs(id),
    topic VARCHAR(100) NOT NULL,           -- e.g. "Fractions"
    label VARCHAR(255) NOT NULL,           -- e.g. "Simplifying Fractions"
    description TEXT,
    display_x FLOAT,                       -- Graph visualization position
    display_y FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Prerequisite edges
CREATE TABLE knowledge_edges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    graph_id UUID REFERENCES knowledge_graphs(id),
    from_node_id VARCHAR(50) REFERENCES knowledge_nodes(id),
    to_node_id VARCHAR(50) REFERENCES knowledge_nodes(id),
    UNIQUE(graph_id, from_node_id, to_node_id)
);
```

### 5.3 Student Progress

```sql
-- Student's KST state (probability distribution over knowledge states)
CREATE TABLE student_states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    graph_id UUID REFERENCES knowledge_graphs(id),
    graph_version INTEGER NOT NULL,
    state_distribution JSONB NOT NULL,     -- {state_hash: probability, ...}
    mastered_nodes JSONB NOT NULL,         -- ["frac-simplify", "frac-add-like", ...]
    outer_fringe JSONB NOT NULL,           -- ["exp-power", "eq-two", ...]
    inner_fringe JSONB NOT NULL,           -- ["frac-mult", "exp-product", ...]
    placement_completed BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, graph_id)
);

-- Every response logged for analytics and BLIM updates
CREATE TABLE response_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    session_id UUID REFERENCES sessions(id),
    node_id VARCHAR(50) REFERENCES knowledge_nodes(id),
    problem_id UUID REFERENCES problems(id),
    session_type VARCHAR(20) NOT NULL,     -- 'placement', 'practice', 'review'
    is_correct BOOLEAN NOT NULL,
    used_hint BOOLEAN DEFAULT FALSE,
    hint_level INTEGER DEFAULT 0,          -- 0=none, 1-3=structured, 4=AI
    used_ai BOOLEAN DEFAULT FALSE,
    response_time_ms INTEGER,
    student_answer TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Spaced repetition schedule per node
CREATE TABLE review_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    node_id VARCHAR(50) REFERENCES knowledge_nodes(id),
    mastered_at TIMESTAMPTZ NOT NULL,
    next_review_at TIMESTAMPTZ NOT NULL,
    interval_days INTEGER DEFAULT 1,       -- SM-2: 1, 3, 7, 14, 30
    streak INTEGER DEFAULT 0,              -- Consecutive successful reviews
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, node_id)
);

-- Sessions for placement, practice, and review
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    session_type VARCHAR(20) NOT NULL,     -- 'placement', 'practice', 'review'
    node_id VARCHAR(50) REFERENCES knowledge_nodes(id),  -- NULL for placement
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    state_snapshot JSONB,                  -- BLIM distribution at session start
    is_active BOOLEAN DEFAULT TRUE
);
```

### 5.4 Content

```sql
-- Problems linked to knowledge nodes
CREATE TABLE problems (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id VARCHAR(50) REFERENCES knowledge_nodes(id),
    problem_text TEXT NOT NULL,             -- LaTeX or plain text
    correct_answer TEXT NOT NULL,           -- Canonical form for checking
    answer_type VARCHAR(20) DEFAULT 'symbolic', -- 'symbolic', 'numeric', 'multiple_choice'
    difficulty FLOAT DEFAULT 0.5,          -- 0-1, used for BLIM params
    source VARCHAR(50),                    -- 'oatutor', 'generated', 'manual'
    metadata JSONB,                        -- Extra data (OATutor step info, etc.)
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Structured hint pathways (OATutor-style)
CREATE TABLE hints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    problem_id UUID REFERENCES problems(id),
    level INTEGER NOT NULL,                -- 1=nudge, 2=specific, 3=scaffold
    hint_text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(problem_id, level)
);

-- Lesson content per node
CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id VARCHAR(50) REFERENCES knowledge_nodes(id) UNIQUE,
    video_url TEXT,                         -- YouTube/Khan Academy embed URL
    content_markdown TEXT NOT NULL,         -- Written lesson content
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Worked examples per node
CREATE TABLE worked_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id VARCHAR(50) REFERENCES knowledge_nodes(id),
    problem_text TEXT NOT NULL,
    steps JSONB NOT NULL,                  -- [{"step": 1, "text": "...", "result": "..."}]
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 6. API ENDPOINTS

### 6.1 Authentication

```
POST /api/auth/register
  Body: { email, name, password, course_code? }
  Returns: { user, token }
  Notes: course_code is optional; if valid, creates enrollment

POST /api/auth/login
  Body: { email, password }
  Returns: { user, token }

POST /api/auth/refresh
  Headers: Authorization: Bearer <token>
  Returns: { token }
```

### 6.2 Dashboard

```
GET /api/dashboard
  Returns: {
    knowledge_map: {
      nodes: [{ id, label, topic, status, display_x, display_y }],
      edges: [{ from_node_id, to_node_id }]
    },
    stats: { mastered_count, ready_count, total_count, overall_progress },
    recommended_next: { node_id, label, topic, prereqs_met },
    reviews_due: [{ node_id, label, mastered_at, interval, streak }]
  }
  Notes: status is one of "mastered", "ready", "locked", "practicing"
         "ready" = all prerequisites mastered (outer fringe)
         "locked" = at least one prerequisite not mastered
```

### 6.3 Placement Test

```
POST /api/placement/start
  Returns: { session_id, first_question: { problem_id, node_id, problem_text } }
  Notes: Uses select_assessment_item() for maximum discrimination

POST /api/placement/submit
  Body: { session_id, problem_id, answer }
  Returns: {
    is_correct,
    correct_answer,
    next_question: { problem_id, node_id, problem_text } | null,
    progress: { questions_answered, estimated_remaining },
    is_complete: boolean
  }
  Notes: Runs blim_update() after each response.
         Terminates when entropy drops below threshold (~12-15 questions).
         Returns next_question=null and is_complete=true when done.

GET /api/placement/results
  Returns: {
    mastered_nodes: [...],
    ready_nodes: [...],
    locked_nodes: [...],
    questions_answered,
    accuracy
  }
```

### 6.4 Lessons & Worked Examples

```
GET /api/lessons/{node_id}
  Returns: {
    node: { id, label, topic },
    lesson: { video_url, content_markdown },
    worked_examples: [{ id, problem_text, steps }],
    is_prerequisites_met: boolean
  }
  Notes: Returns content even if prerequisites not met (soft gating —
         students can view lessons but can't practice locked nodes)

GET /api/lessons/{node_id}/examples
  Returns: { worked_examples: [{ id, problem_text, steps }] }
```

### 6.5 Practice

```
POST /api/practice/{node_id}/start
  Returns: {
    session_id,
    problem: { id, problem_text, answer_type },
    mastery: { current_posterior, threshold: 0.85, min_questions: 3, soft_cap: 10 }
  }
  Notes: Rejects if prerequisites not met (403).
         Returns first problem from the node's problem pool.

POST /api/practice/{node_id}/submit
  Body: { session_id, problem_id, answer }
  Returns: {
    is_correct,
    correct_answer,
    explanation?,
    mastery: { current_posterior, questions_answered, is_mastered },
    next_problem: { id, problem_text, answer_type } | null
  }
  Notes: Runs blim_update() for this node.
         next_problem is null if mastered (posterior >= 0.85) or soft cap reached.

GET /api/practice/{node_id}/hints/{problem_id}?level={1|2|3}
  Returns: { hint_text, level, max_level: 3 }

POST /api/practice/{node_id}/complete
  Body: { session_id }
  Returns: {
    summary: { questions, correct, accuracy, mastery_posterior, time_seconds },
    is_mastered,
    outer_fringe: [{ node_id, label, topic, prereqs }],
    inner_fringe: [{ node_id, label, topic }]
  }
  Notes: If mastered, creates review_schedule entry.
         Returns updated fringe for "what's next" selection.
```

### 6.6 Reviews

```
GET /api/reviews
  Returns: {
    due: [{ node_id, label, topic, mastered_at, interval_days, streak, next_review_at }],
    upcoming: [{ node_id, label, next_review_at }]
  }

POST /api/reviews/{node_id}/start
  Returns: { session_id, problem: { id, problem_text, answer_type } }
  Notes: Review sessions use 1-3 problems per node.

POST /api/reviews/{node_id}/submit
  Body: { session_id, problem_id, answer }
  Returns: {
    is_correct,
    review_result: "passed" | "failed",
    new_interval_days?,
    new_streak?
  }
  Notes: On pass — interval increases per SM-2 (1→3→7→14→30), streak++
         On fail — node drops to "needs practice", review_schedule deleted,
         BLIM posterior reduced. Student must re-master through practice.
```

### 6.7 Settings

```
GET /api/settings
  Returns: { name, email, course_code, preferences: { reminders, auto_hints } }

PUT /api/settings
  Body: { name?, email?, course_code?, preferences? }
  Returns: { updated settings }

POST /api/settings/test-ai-key
  Body: { provider }
  Returns: { test_prompt, test_url, test_headers_template }
  Notes: Returns the test request configuration for the specified provider.
         The FRONTEND makes the actual test call directly to the AI provider.
         The API key NEVER passes through our backend.
         The frontend stores the key in localStorage only.

DELETE /api/settings/reset-progress
  Returns: { success }
  Notes: Deletes all student_states, response_logs, review_schedules for this user.
```

---

## 7. KNOWLEDGE GRAPH DEFINITION

The knowledge graph is the central data structure. It defines ~35-50 atomic algebra sub-skills decomposed from 8 topics, with genuine pedagogical prerequisite relationships.

### 7.1 Topics and Sub-Skills

Decompose these 8 topics into atomic sub-skills. Each sub-skill should represent a single testable concept with clear prerequisites:

**1. Fraction Arithmetic** (~5-6 nodes)
- Simplifying fractions
- Adding/subtracting with like denominators
- Finding common denominators
- Adding/subtracting with unlike denominators
- Multiplying fractions
- Dividing fractions

**2. Exponent Rules** (~4-5 nodes)
- Product rule (x^a · x^b = x^(a+b))
- Power rule ((x^a)^b = x^(ab))
- Negative and zero exponents
- Combining multiple exponent rules

**3. Order of Operations** (~2-3 nodes)
- PEMDAS basics
- Nested expressions with grouping symbols

**4. Solving Equations** (~5-6 nodes)
- One-step linear equations
- Two-step linear equations
- Equations with fractions
- Equations with distribution
- Quadratic equations (factoring)

**5. Logarithms & Exponentials** (~4 nodes)
- Exponential functions
- Logarithm definition
- Log rules (product, quotient, power)
- Solving logarithmic equations

**6. Summation Notation** (~3 nodes)
- Sigma notation basics
- Arithmetic sums
- Nested sums

**7. Combinatorics** (~3 nodes)
- Counting principles
- Permutations
- Combinations

**8. Geometric Series** (~3 nodes)
- Geometric sequences
- Finite geometric sums
- Infinite geometric sums (convergence)

### 7.2 Cross-Topic Prerequisites

These are the critical surmise relations that connect topics:

- Fractions (add unlike + multiply) → Equations with fractions
- Order of operations (nested) → One-step equations
- Order of operations (nested) → Counting principles
- Combining exponent rules → Exponential functions
- Exponential functions → Logarithm definition
- Equations with distribution → Solving log equations
- Two-step equations → Sigma notation basics
- Two-step equations → Counting principles
- Negative/zero exponents → Geometric sequences
- Arithmetic sums → Geometric sequences
- Log rules → Infinite geometric sums
- Permutations → Combinations
- Combinations → Finite geometric sums (binomial connection)
- Geometric finite → Geometric infinite

### 7.3 JSON Schema

Use the Vanderbilt `knowledge-graph.schema.json` format. The graph JSON should be stored at `backend/data/knowledge_graph.json` and loaded into the database on startup.

The graph also includes display coordinates (x, y) for the knowledge graph visualization. Use a left-to-right flow layout where foundational skills appear on the left and advanced skills on the right.

---

## 8. KST ENGINE INTEGRATION

### 8.1 Source

Copy `kst_utils.py` from `C:\Users\jjcas\Desktop\Fisher App\Fisher App 2.0\projects\knowledge-spaces\src\kst_utils.py` into `backend/app/kst/kst_utils.py`.

This file provides these functions (all pure Python, no external dependencies):

| Function | Purpose | Used In |
|----------|---------|---------|
| `transitive_closure(relations)` | Complete the surmise relation | Graph initialization |
| `enumerate_downsets(items, relations)` | Generate all feasible knowledge states | Graph initialization |
| `compute_fringes(state, relations)` | Inner/outer fringe for a state | Dashboard, practice flow |
| `generate_learning_paths(graph)` | Breadth-first, depth-first, max-unlock paths | Future feature |
| `blim_update(prior, response, item, states, params)` | Bayesian posterior update | After every response |
| `select_assessment_item(distribution, states, items)` | Maximum discrimination selection | Placement test |
| `entropy(distribution)` | Shannon entropy of state distribution | Placement termination |
| `class_analytics(student_states)` | Aggregate mastery stats | Future instructor dashboard |
| `validate_graph(graph)` | Referential integrity, acyclicity, transitivity | Graph changes |

### 8.2 Wrapper Service

Create `backend/app/services/kst_engine.py` that wraps these functions with:

- Database integration (load graph from DB, save state to DB)
- Caching of enumerated states (compute once on startup, cache in memory)
- Error handling and logging
- BLIM parameter configuration (lucky_guess=0.1, careless_error=0.05 as defaults)

### 8.3 State Enumeration Limits

With ~35-50 nodes, the state space could theoretically be huge. The Vanderbilt code has a 10,000 state cap. For the initial graph, enumerate all downsets. If enumeration exceeds 10,000, use the approximate method: maintain a working set of the most probable states and expand as needed. Log a warning if this happens.

---

## 9. ADAPTIVE ASSESSMENT (PLACEMENT TEST)

### Flow:

1. Student clicks "Start Placement Test"
2. Backend initializes uniform prior over all knowledge states
3. `select_assessment_item()` picks the item where P(mastered) ≈ 0.5 across the current distribution — maximally informative
4. Student answers; backend runs `blim_update()` to update posterior
5. Repeat until `entropy(distribution)` drops below threshold (suggesting confident classification) or 20 questions max
6. Map the most probable state to mastered/ready/locked for each node
7. Save `student_state` and redirect to results

### Termination:

- Entropy threshold: when entropy drops below 15% of initial entropy, stop
- Hard cap: 20 questions maximum
- Typical: ~12-15 questions for a 35-40 node graph

### After Placement:

- All nodes in the most probable state → "mastered"
- Nodes whose prerequisites are all mastered but are not in the state → "ready"
- Everything else → "locked"
- Create `review_schedule` entries for all mastered nodes (first review in 1 day)

---

## 10. PRACTICE FLOW

### Session Flow:

1. **Lesson** → Video embed (YouTube/Khan Academy) at top + markdown content below + AI chat panel
2. **Worked Examples** → 2-3 examples with steps revealed one at a time
3. **Practice** → Adaptive problem set with mastery meter, hints, and AI

### Practice Session Logic:

**Important architectural note:** The full BLIM operates over the entire knowledge state space and is used during **placement** (to classify the student's overall knowledge state) and after **mastering/failing a node** (to update the global state distribution and recompute fringes). During **within-node practice**, use a simpler per-node Bayesian update (essentially BKT for that specific skill) to track whether the student has mastered this particular node. The per-node posterior starts at the student's current estimated mastery for that node (derived from the global state distribution) and updates with each response using lucky_guess and careless_error parameters.

```python
# Pseudocode for practice session (per-node mastery tracking)
session = create_session(user_id, node_id)
posterior = get_node_posterior(user_id, node_id)  # P(mastered this node) from global state
questions_asked = 0

while True:
    problem = select_problem(node_id, seen_problems=session.problems)
    answer = await_student_answer(problem)
    is_correct = check_answer(answer, problem.correct_answer)
    
    # Per-node Bayesian update (simplified BKT-style)
    if is_correct:
        # P(mastered | correct) using Bayes' rule with lucky_guess param
        posterior = (posterior * (1 - careless_error)) / \
                   (posterior * (1 - careless_error) + (1 - posterior) * lucky_guess)
    else:
        # P(mastered | incorrect)
        posterior = (posterior * careless_error) / \
                   (posterior * careless_error + (1 - posterior) * (1 - lucky_guess))
    questions_asked += 1
    
    # Log response
    log_response(user_id, node_id, problem.id, is_correct, ...)
    
    # Check termination conditions
    if posterior >= 0.85 and questions_asked >= 3:
        mark_mastered(user_id, node_id)
        update_global_state(user_id)        # Run full BLIM to recompute fringes
        schedule_review(user_id, node_id, interval=1)  # First review in 1 day
        break
    elif questions_asked >= 10:
        # Soft cap reached; suggest reviewing lesson
        break
    elif posterior <= 0.15 and questions_asked >= 3:
        # Student likely doesn't have prerequisites; suggest going back
        suggest_prerequisite_review(user_id, node_id)
        break
```

### Answer Checking:

Use SymPy for symbolic math verification:

```python
from sympy import simplify, sympify, Eq

def check_symbolic_answer(student_answer: str, correct_answer: str) -> bool:
    try:
        student = sympify(student_answer)
        correct = sympify(correct_answer)
        return simplify(student - correct) == 0
    except:
        return student_answer.strip() == correct_answer.strip()
```

For numeric answers, allow tolerance (±0.01). For multiple choice, exact string match.

---

## 11. HINT SYSTEM

### Structured Hints (Default — Always Available):

Each problem has up to 3 hint levels stored in the `hints` table:

- **Level 1 (Nudge):** A vague directional hint. "Think about what rule applies when you raise a power to another power."
- **Level 2 (Specific):** More targeted. "Split (5y⁴)³ into two parts: what is 5³? And what is (y⁴)³?"
- **Level 3 (Scaffold):** Nearly gives the answer with blanks. "5³ = ___ and (y⁴)³ = y^(4×3) = y^___. Combine them."

### AI Hints (Optional — BYOK):

- Appears as a separate button alongside the hint pathway
- Sends the problem text + student's current attempt to the student's configured AI provider
- System prompt for the AI call: "You are a math tutor helping a student with [topic]. The student is working on this problem: [problem_text]. Their current attempt: [student_answer]. Give a helpful explanation without giving the final answer directly. Be encouraging."
- The AI key is stored ONLY in the browser's localStorage. It is NEVER sent to or stored on the Fisher App backend.
- When calling the AI, the frontend makes the API call directly from the browser to the AI provider (OpenAI, Anthropic, or Google)

### AI Chat in Lessons:

Same BYOK mechanism, but with a different system prompt: "You are a math tutor. The student is reading a lesson about [topic]. Here is the lesson content: [lesson_markdown]. Answer their question helpfully."

### Logging:

Log `used_hint`, `hint_level`, and `used_ai` in `response_logs`. This data enables future research on which support mechanisms lead to better learning outcomes.

---

## 12. SPACED REPETITION (SM-2 VARIANT)

### Schedule:

When a node is mastered, create a review schedule:

| Review # | Interval | After Mastery |
|----------|----------|---------------|
| 1 | 1 day | Day 1 |
| 2 | 3 days | Day 4 |
| 3 | 7 days | Day 11 |
| 4 | 14 days | Day 25 |
| 5 | 30 days | Day 55 |
| 6+ | 30 days | Every 30 days |

### Review Session:

- 1-3 problems per review (fewer than practice, since the goal is verification not learning)
- If correct on first try → review passes, interval advances, streak++
- If incorrect → node drops back to "needs practice" status
  - Delete review schedule
  - Run `blim_update()` with is_correct=False to reduce posterior
  - Student must re-master through a full practice session

### Decay Logic:

If a review is overdue by more than 7 days:
- BLIM posterior for that node decays by 0.02 per day overdue (past the 7-day grace period)
- This is calculated on-the-fly when loading dashboard, not via a background job
- The mastery meter on the knowledge map reflects this decay
- If posterior drops below 0.5, the node visually changes from "mastered" to a dimmed/warning state

### Review Reminder Flow:

1. **Banner on Dashboard:** "2 skills are due for review" (always visible when reviews are due)
2. **Modal when starting new topic:** If reviews are overdue and student tries to start a new lesson:
   - First modal: "You have 2 skills due for review. Reviewing now takes ~3 minutes and keeps your progress solid." [Review now] [Remind me later]
   - If "Remind me later" → Second modal: "Skipping reviews can lead to skill decay. If a review is overdue by more than 7 days, the skill may drop back to 'needs practice.' Continue anyway?" [OK, I'll review now] [Skip for now]
3. Student can always skip — reviews are never mandatory, but consequences are transparent

---

## 13. FRONTEND SCREENS

### 13.1 Visual Design

All visual constants live in `frontend/src/theme.js`:

```javascript
export const theme = {
  colors: {
    bg: "#FAFAF8",
    card: "#FFFFFF",
    primary: "#2D5A3D",        // Forest green — mastered, primary actions
    primaryLight: "#E8F0EB",
    accent: "#D4A843",          // Gold — ready to learn, recommended
    accentLight: "#FDF6E3",
    practicing: "#4A90D9",      // Blue — in progress
    text: "#1A1A1A",
    textMuted: "#6B6B6B",
    border: "#E2E0DC",
    locked: "#C4C2BD",
    danger: "#C44B3F",
  },
  fonts: {
    serif: "'Georgia', 'Times New Roman', serif",    // Headings
    sans: "'Helvetica Neue', 'Segoe UI', sans-serif", // Body text
  },
  // ... spacing, border radius, shadows
};
```

These values should be easy to change later — John wants to fine-tune the visual design. Keep all colors/fonts/spacing in this one file.

### 13.2 Knowledge Graph Visualization

The dashboard has TWO view modes the student can toggle between:

1. **Graph View** — Interactive node-and-edge visualization showing prerequisite relationships. Nodes are colored by topic, bordered by status (mastered/ready/locked). Hover highlights connections. Click opens detail panel. Pan and zoom supported. This is the primary differentiating visual.

2. **List View** — Nodes grouped by topic with status chips. Faster for quick access, better on mobile.

The graph visualization uses positioned divs + SVG edges (no heavy graph library needed). Node positions are stored in the knowledge graph data and can be adjusted.

### 13.3 Responsive Design

- Desktop: Full graph visualization, side panels, comfortable spacing
- Tablet: Graph scales down, detail panel overlays instead of side-by-side
- Mobile: Default to list view (graph available but cramped). MathLive input tested for mobile keyboards. Modals become full-screen sheets.

Test MathLive on mobile — math input on phone keyboards is notoriously difficult. Ensure the MathLive virtual keyboard option is enabled on touch devices.

### 13.4 Screen-by-Screen Notes

Key implementation notes for each screen:

**Login/Register:** Simple forms. Course code field on registration is optional. After registration → placement intro.

**Placement Intro:** Explains the test (~5 min, ~12-15 questions). Two buttons: "Start" and "Skip (start from beginning)."

**Placement Question:** Progress bar (question X of ~15), topic label, problem display area, MathLive input, submit button. No hints during placement.

**Placement Results:** Full list of assessed skills with mastered/ready/locked status. "Go to Dashboard" button.

**Dashboard:** The hub. Knowledge map (graph or list view), overall progress bar, "Recommended Next" card (outer fringe suggestion), "Reviews Due" notification. Click any unlocked node to enter its lesson.

**Lesson Page:** Breadcrumb navigation. Progress indicator (Lesson → Examples → Practice). Video embed at top (YouTube iframe). Written content below (rendered markdown). AI chat panel at bottom for questions about the material. "Continue to Examples" button.

**Worked Examples:** Same progress indicator. Step-by-step reveal (show next step button). 2-3 examples per node. "Ready to Practice" button.

**Practice Page:** Mastery meter (BLIM posterior as progress bar from 0% to 85% threshold). Problem display, MathLive input, submit button. After submit: correct/incorrect feedback with explanation. Hint panel: "Need a hint?" button + "Ask AI" button. Hints appear below, escalating through levels.

**Score Report:** Stats (questions, accuracy, mastery %, time). If mastered: celebration + outer fringe displayed as clickable "what's next" cards. If not mastered: encouragement + suggestion to review lesson.

**Review Queue:** List of due/upcoming reviews with interval and streak info. "Review" button per node.

**AI Setup:** Plain-language explainer of API keys. Step-by-step instructions for OpenAI, Anthropic, Google. Password-masked input field. "Save & Test Connection" button. Key stored in localStorage only.

**Settings:** Profile (name, email, course code), learning preferences (reminders toggle, auto-hints toggle), danger zone (reset progress with confirmation).

---

## 14. CONTENT SEEDING

### 14.1 OATutor Content Import

The OATutor repository (https://github.com/CAHLR/OATutor) contains CC BY 4.0 algebra problems with structured hint pathways. Write `scripts/import_oatutor_content.py` to:

1. Clone OATutor repo to a temporary location (or reference it if already cloned)
2. Filter for Elementary Algebra 2e and Intermediate Algebra 2e content (in `content/` directory)
3. Map OATutor skill tags to Fisher App knowledge node IDs
4. Convert OATutor JSON format (problems → steps → hints) to our schema
5. Insert into `problems` and `hints` tables

Target: At least 10 problems per knowledge node, with 3 hints each.

### 14.2 Lesson Content

For v1, create basic lesson content for each node:

- **Video:** Link to relevant Khan Academy or other educational YouTube video
- **Written content:** 2-4 paragraphs explaining the concept, including the key formula/rule in a highlighted box, and 1-2 inline examples

This content can be enhanced later. The important thing is that every node has SOMETHING — no empty lessons.

### 14.3 Worked Examples

Create 2-3 worked examples per node with step-by-step solutions. Each example should have 2-4 steps. These can be generated programmatically for algebraic manipulation topics.

### 14.4 Problem Generators

For topics where OATutor doesn't have enough variety, create Python parameterized generators in `scripts/generate_problems.py`. Reference the R generators in Fisher App 2.0 for the patterns. Use SymPy to generate random problems and compute correct answers.

---

## 15. DOCKER COMPOSE

```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://fisher:fisher@db:5432/fisherapp
      - SECRET_KEY=${SECRET_KEY}
      - CORS_ORIGINS=http://localhost:5173
    depends_on:
      - db
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=fisher
      - POSTGRES_PASSWORD=fisher
      - POSTGRES_DB=fisherapp
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

## 16. IMPLEMENTATION ORDER

Build in this exact order to ensure each piece is testable before the next:

### Phase 1: Foundation
1. Docker Compose + PostgreSQL + FastAPI skeleton + React/Vite skeleton
2. Database models + Alembic migrations
3. Auth endpoints (register, login, JWT)
4. Login and Register pages

### Phase 2: Knowledge Graph
5. Copy `kst_utils.py` and create `kst_engine.py` wrapper
6. Define `knowledge_graph.json` with all nodes, edges, and display positions
7. Seed script to load graph into database
8. Dashboard API endpoint (returns nodes with placeholder statuses)
9. Dashboard page with graph visualization (all nodes "locked" initially)

### Phase 3: Placement Test
10. Placement service (assessment item selection, BLIM update, entropy termination)
11. Placement API endpoints
12. Placement intro, question, and results pages
13. After placement: student_state saved, dashboard shows real statuses

### Phase 4: Learning Flow
14. Lesson content seeding (at least stub content for every node)
15. Lesson API + page (video + markdown + AI chat placeholder)
16. Worked examples API + page (step reveal)
17. Practice service (problem selection, answer checking, BLIM update, mastery threshold)
18. Practice API + page (mastery meter, hints, submit flow)
19. Score report page (stats, fringe selection)

### Phase 5: Hints & AI
20. Hint seeding (import OATutor hints)
21. Hint API endpoint
22. HintPanel component (structured hints with level progression)
23. AI setup page with explainer
24. AI chat component (BYOK, frontend-only API calls)
25. Integrate AI into lesson page and practice page

### Phase 6: Spaced Repetition
26. Review scheduling service (SM-2 intervals)
27. Review API endpoints
28. Review queue page
29. Review reminder banner + two-step modal
30. Decay logic (overdue reviews reduce posterior)

### Phase 7: Polish
31. Settings page
32. Responsive design testing and fixes
33. MathLive mobile testing
34. Error handling, loading states, empty states
35. Knowledge map list view (alternative to graph)
36. Content gap filling (ensure every node has 10+ problems, lesson, examples)

---

## 17. TESTING STRATEGY

### Backend:
- Unit tests for `kst_engine.py` (validate BLIM updates, fringe computation, assessment selection)
- Unit tests for `answer_checker.py` (symbolic equivalence edge cases)
- Integration tests for each API endpoint
- Use pytest + httpx for async FastAPI testing

### Frontend:
- Component tests for MathInput, HintPanel, MasteryMeter, KnowledgeGraph
- Page-level tests for critical flows (placement → dashboard, practice → score report)
- Use Vitest + React Testing Library

### End-to-End:
- Full flow: register → placement → dashboard → lesson → practice → mastery → review
- Verify BLIM posterior actually changes with responses
- Verify fringe updates when a node is mastered

---

## 18. ENVIRONMENT VARIABLES

```env
# .env.example
DATABASE_URL=postgresql://fisher:fisher@db:5432/fisherapp
SECRET_KEY=change-me-to-a-random-string
JWT_EXPIRY_HOURS=24
CORS_ORIGINS=http://localhost:5173

# BLIM parameters (tunable)
BLIM_LUCKY_GUESS=0.1
BLIM_CARELESS_ERROR=0.05
BLIM_MASTERY_THRESHOLD=0.85
BLIM_ENTROPY_TERMINATION=0.15

# Review parameters
REVIEW_GRACE_DAYS=7
REVIEW_DECAY_RATE=0.02
```

---

## 19. DEPLOYMENT NOTES

V1 runs locally with Docker Compose. When ready to deploy:

1. Push to GitHub
2. Connect to Railway
3. Add PostgreSQL addon
4. Set environment variables in Railway dashboard
5. Railway auto-detects Docker Compose and deploys

No code changes needed for deployment. The same Docker containers run in both environments.

---

## 20. WHAT SUCCESS LOOKS LIKE

When complete, a student should be able to:

1. Create an account and take a 5-minute placement test that identifies their algebra strengths and gaps
2. See a visual knowledge map showing what they know, what they're ready to learn, and what's locked behind prerequisites
3. Click a recommended topic and go through a lesson (video + text), worked examples, and adaptive practice
4. Get structured hints when stuck, and optionally ask an AI for alternative explanations
5. See their mastery meter fill up as they answer correctly, and celebrate when they master a skill
6. Choose their next topic from the outer fringe after mastering each skill
7. Receive review reminders that keep mastered skills fresh
8. Feel that the app understands their learning path — not just drilling random problems, but guiding them through a coherent prerequisite structure
