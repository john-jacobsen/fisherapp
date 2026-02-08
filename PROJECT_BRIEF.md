# BerkeleyStats Tutor — Project Brief

## Project Overview

BerkeleyStats Tutor is an open-source, adaptive learning application designed to help undergraduate statistics students at UC Berkeley build and maintain the foundational skills they need to succeed — from algebra through mathematical statistics. The app presents students with randomly generated, representative problems, manages cognitive load through evidence-based instructional sequencing, and tracks mastery over time using spaced repetition.

The project is intended to be open-source and accessible to the Berkeley statistics community for use, contribution, and extension.

---

## Architecture

**R package + Plumber API backend, React (JavaScript/TypeScript) frontend, PostgreSQL database.**

### Why this architecture:

- **R package**: The heart of the project. Handles all problem generation, answer checking, adaptive algorithms, spaced repetition logic, knowledge graph operations, and statistical computation. R is the natural home for this work and is the language the Berkeley stats community knows best. The R package should be usable standalone from the R console (without the web app), which increases adoption and makes it easy for the community to contribute.
- **Plumber API**: Exposes the R package's functionality as RESTful JSON endpoints. This is the bridge between the R logic and the frontend.
- **React frontend (JavaScript/TypeScript)**: Handles the student-facing UI — math rendering (KaTeX or MathJax), problem display, answer input, feedback presentation, the progress dashboard, and the placement test interface. React provides responsive design for mobile and desktop, and supports future progressive web app (PWA) capabilities.
- **PostgreSQL**: Stores student accounts, session history, problem attempt records, mastery states, spaced repetition schedules, and course/section metadata.

### Key architectural principles:

- **Clean separation of concerns**: The R package, API, frontend, and database are independent layers. Each can be developed, tested, and replaced independently.
- **Problem templates as data, not hardcoded functions**: Problem generation is template-driven and declarative. A problem template defines what parameters vary, what the solution procedure is, and what common errors look like. A generic engine reads templates and produces problems. This makes the system extensible by non-programmers.
- **Structured API responses**: Every problem endpoint returns structured JSON (problem statement, solution steps, final answer, topic ID, difficulty level, prerequisite skills). This supports future integrations (LLM tutoring, instructor dashboards, etc.).
- **Future-proof database schema**: Include `course_id` and `institution_id` fields from day one, even though version 1 only serves one course at one institution.

### Development and deployment tools:

- **GitHub**: Version control (monorepo with subdirectories for R package, API, and frontend)
- **RStudio**: R package and API development
- **VS Code**: React frontend development
- **Docker + Docker Compose**: Orchestrates PostgreSQL, the Plumber API, and the React dev server locally
- **Node.js/npm**: React build tooling

---

## Version 1 Scope

**Version 1 focuses exclusively on algebra content.** Algebra is the prerequisite foundation for everything else in the curriculum. Building version 1 around algebra lets us construct and debug the entire infrastructure — the API, frontend, adaptive algorithms, database, and dashboard — before adding the complexity of calculus, probability, or statistical concepts. Once the system works for algebra, adding new content areas is mostly about writing new problem templates and extending the knowledge graph.

---

## Version 1 Required Features

### 1. Knowledge Graph / Content Taxonomy

A formal, structured map of all algebra topics, their prerequisite relationships, and their internal difficulty levels. This graph is the single source of truth for content sequencing and drives the placement test, the adaptive problem selection, and the dashboard. Format: a structured data file (JSON or YAML) consumable by the R package.

Example relationships: order of operations → simplifying expressions → solving linear equations → solving systems of equations; factoring integers → factoring polynomials → rational expressions.

### 2. Problem Generation Engine

For each node in the knowledge graph, a problem template that can generate randomized instances at each difficulty level. Each generated problem includes:

- The problem statement (with randomized parameters)
- The full worked solution (step by step)
- The correct final answer
- The topic ID and difficulty level
- Prerequisite skills

Problems must be representative of what students encounter in actual Berkeley coursework.

### 3. Problem Difficulty Gradations Within Each Topic

Each topic has 3–5 difficulty levels:

1. **Recognition** — identify or recall (e.g., "Which of these is a quadratic equation?")
2. **Routine application** — straightforward single-step or two-step problems
3. **Multi-step** — requires chaining several skills within the topic
4. **Transfer** — applies the skill in an unfamiliar context
5. **Synthesis** — combines this topic with other topics

### 4. Feedback and Error Handling

When a student answers incorrectly:

- The system marks the answer as wrong
- The system presents the full worked solution (step by step)
- The system does NOT attempt to pinpoint the exact error step (this is a deliberate design choice — showing the correct worked solution and letting the student compare is simpler and pedagogically effective)
- The system may offer a simpler scaffolded version of the same problem type
- Hints degrade gracefully: first a nudge, then a bigger hint, then the full solution

### 5. Cognitive Load Management and Instructional Sequencing

The app must:

- Sequence content from simple to complex (within and across topics)
- Provide worked examples before independent practice (the worked example effect)
- Build automaticity in foundational skills before demanding their application
- Ensure high success rates during initial instruction (target ~85% correct during learning phases)
- Never present a topic before its prerequisites are mastered

### 6. Spaced Repetition

A modified SM-2 algorithm (adapted for problem-solving rather than flashcard recall) governs review scheduling. Each topic gets an ease factor and review interval that adjusts based on performance. Mastered topics resurface at increasing intervals to maintain long-term retention.

### 7. Adaptive Difficulty and Mastery Criteria

**Mastery definition**: 85%+ accuracy over the last N problems, across at least 2 spaced sessions, with problems at difficulty level 3+.

The system must:

- Adjust problem difficulty based on student performance within a session
- Detect when a student is stuck in a loop and change approach (e.g., offer a worked example, route to a prerequisite topic)
- Promote students to harder problems as they demonstrate competence
- Demote students to easier problems or prerequisite topics when they struggle

### 8. Computer-Adaptive Placement Test (CAT)

An initial diagnostic test that efficiently determines where a student falls in the curriculum. Uses adaptive testing logic: starts with medium-difficulty items and branches up or down based on responses. Should accurately place a student in approximately 15–25 questions (not a long exhaustive test). Placement maps to the knowledge graph — the student begins practice at the appropriate nodes.

### 9. Progress Dashboard

A dedicated student-facing dashboard showing:

- **Mastery by topic**: Visual map of which topics are mastered, in progress, or not yet started
- **Streak tracking**: Current streak of consecutive days with practice sessions
- **Session summaries**: Post-session feedback (e.g., "You mastered 2 new topics today," "You practiced 15 problems with 87% accuracy")
- **Clear visual of progress through the curriculum**: The student should be able to see where they are in the overall algebra sequence and what's ahead

### 10. Student Authentication and Persistence

Basic authentication so students can log in, and their progress, mastery states, and spaced repetition schedules persist across sessions. Does not need to be sophisticated — email/password or university SSO integration are both fine.

---

## Future Features (Not in Version 1, But Inform Architecture Decisions)

These features are explicitly out of scope for version 1 but should influence structural decisions made now.

### AI / LLM Integration

- Natural-language hints ("I don't understand why we take the derivative here")
- Conversational tutoring for conceptual topics
- Generating novel problem variations on the fly
- **Architectural implication**: Clean, well-documented API endpoints returning structured JSON. If problem data is well-structured, plugging an LLM in later is just adding a new endpoint.

### Collaborative Features

- Study groups, leaderboards, shared progress within a class section
- TA/instructor dashboard showing aggregate class struggles ("70% of the class is failing conditional probability")
- **Architectural implication**: Include `course_id` and `section_id` in the database schema from day one.

### Problem Authoring by Instructors

- A professor or GSI adds their own problem templates for specific exam topics or new courses
- **Architectural implication**: Problem generation must be template-driven and declarative (data, not code). A generic engine reads templates and produces problems.

### Multiple Input Modalities

- Handwritten math input (tablet/phone)
- Photo upload of student work
- Graphical interfaces (drag to sketch a distribution, click to place critical values)
- **Architectural implication**: Answer-checking logic must be completely decoupled from input method. The API accepts a structured answer object and returns a grade; how the answer is created is purely a frontend concern.

### Content Beyond Berkeley

- Other universities use the system with their own curriculum
- Community colleges with different prerequisites, graduate programs starting at a higher level
- **Architectural implication**: The knowledge graph should be configurable. A different institution supplies their own graph (or modifies the default) without touching the problem engine.

### Offline / Low-Connectivity Use

- Progressive web app (PWA) caching: problems cached locally, answers sync when connectivity returns
- **Architectural implication**: Purely a frontend decision. React supports this path. No impact on R backend.

### Additional Content Areas (Post-Algebra)

The full curriculum sequence planned for future versions:

1. ~~Algebra~~ *(version 1)*
2. Calculus 1 (limits, derivatives, basic integration)
3. Calculus 2 (integration techniques, series)
4. Calculus 3 (multivariable calculus)
5. Introduction to Statistics
6. Probability
7. Mathematical Statistics

Each new content area requires: extending the knowledge graph, writing new problem templates, and connecting prerequisite edges to existing topics.

---

## Development Phases (Version 1)

### Phase 1: Knowledge Graph

Map all algebra topic nodes, prerequisite relationships, and difficulty levels using UC Berkeley course materials. Deliverable: a complete algebra knowledge graph as a structured JSON/YAML file.

### Phase 2: Problem Engine (R Package)

Build the core R package. For each knowledge graph node, create a problem template that generates randomized instances at each difficulty level, with worked solutions and correct answers. Include answer-checking logic. Deliverable: an installable R package where `generate_problem("factoring_quadratics", difficulty = 3)` returns a structured problem object.

### Phase 3: Student Model and Adaptive Logic (R Package)

Implement the spaced repetition algorithm (modified SM-2), mastery criteria (85% rule), next-problem selection logic, and CAT placement test logic. This layer consumes the knowledge graph and sits on top of the problem engine. Deliverable: simulate a complete student session in R — the system picks a problem, accepts an answer, updates the student model, and picks the next problem.

### Phase 4: API and Database

Wrap the R package in Plumber endpoints. Set up PostgreSQL with tables for students, sessions, problem attempts, mastery states, spaced repetition schedules, courses, and institutions. Deliverable: a running API testable with curl/Postman — create student, start session, get problem, submit answer, get next problem, check progress.

### Phase 5: Frontend

React app with: placement test flow, practice session interface (problem display, answer input, feedback with worked solutions), progress dashboard (mastery by topic, streaks, session summaries), and basic auth. Deliverable: a working end-to-end web app.

### Phase 6: Testing and Polish

User testing, bug fixes, edge case handling, UI refinement. Deliverable: a version suitable for sharing with a class.

**Iterative approach**: We don't need all algebra topics complete before moving to Phase 3. Build 5–8 core topics, move through Phases 3–5 to get the full loop working, then circle back to fill in remaining algebra topics.

---

## Technical Notes

### Error Diagnosis Approach

The system provides full worked solutions when a student answers incorrectly. It does NOT attempt to pinpoint the exact step where the student made an error. This is a deliberate design choice: showing the correct worked solution and letting the student compare is simpler to implement and pedagogically effective.

### Math Rendering

Use KaTeX or MathJax in the React frontend for rendering mathematical expressions. All problem statements and worked solutions should be stored in LaTeX format.

### Database Schema Considerations

- Include `course_id` and `institution_id` from day one
- Track every problem attempt (student, topic, difficulty, answer given, correct answer, timestamp, time spent)
- Store spaced repetition state per student per topic (ease factor, interval, next review date)
- Store mastery state per student per topic (mastery level, last N attempts, session count)

### R Package Design

- All problem templates should be declarative data structures, not individual hardcoded functions
- The package should be usable standalone from the R console without the web app
- Thorough documentation of all exported functions
- Unit tests for problem generation (verify solutions are correct) and adaptive logic

---

## Content Source

UC Berkeley undergraduate course materials will be provided by the developer to define the knowledge graph and ensure problem representativeness. These materials cover algebra prerequisites through mathematical statistics.
