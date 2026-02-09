# BerkeleyStats Tutor (Fisher App)

An open-source, adaptive learning app that helps UC Berkeley undergraduate statistics students build foundational skills from algebra through mathematical statistics. It presents randomly generated problems, manages cognitive load through evidence-based instructional sequencing, and tracks mastery over time using spaced repetition.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   React UI  │────>│  Plumber API │────>│  PostgreSQL   │
│  (Vite/TS)  │<────│   (R/JSON)   │<────│   Database    │
└─────────────┘     └──────┬───────┘     └──────────────┘
                           │
                    ┌──────┴───────┐
                    │  fisherapp   │
                    │  R Package   │
                    └──────────────┘
```

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Core logic | R package (`fisherapp`) | Problem generation, answer checking, adaptive algorithms, spaced repetition, knowledge graph |
| API | Plumber (R) | RESTful JSON endpoints exposing R package functionality |
| Frontend | React + TypeScript + Tailwind CSS | Student-facing UI with KaTeX math rendering |
| Database | PostgreSQL 16 | Students, sessions, attempts, mastery states, spaced repetition schedules |
| DevOps | Docker Compose | Orchestrates all services |

## Features

- **40 problem templates** across 8 algebra topics, each with 5 difficulty levels
- **Randomized problems** with step-by-step worked solutions in LaTeX
- **Adaptive difficulty** that promotes on success and demotes on struggle
- **SM-2 spaced repetition** for long-term retention
- **Computer-Adaptive Placement Test** (15-25 questions) to determine starting levels
- **Stuck-loop detection** with automatic scaffolding interventions
- **Mastery tracking** with per-topic progress visualization

## Topics

1. Fraction Arithmetic
2. Exponent Rules
3. Order of Operations
4. Summation Notation
5. Solving Equations
6. Logarithms & Exponentials
7. Combinatorics
8. Geometric Series

## Quick Start (Docker)

```bash
# Clone the repository
git clone https://github.com/your-username/fisherapp.git
cd fisherapp

# Copy environment config
cp .env.example .env

# Start all services
docker compose up --build
```

Services:
- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **Database**: localhost:5432

## Development Setup

### Prerequisites

- R 4.2+ with `devtools` installed
- Node.js 20+
- PostgreSQL 16 (or use Docker)

### R Package

```bash
cd r-package

# Install dependencies and package
Rscript -e "devtools::install()"

# Run tests (581 tests)
Rscript -e "devtools::test()"

# Use from R console
Rscript -e "library(fisherapp); p <- generate_problem('fraction_arithmetic', difficulty = 3); print(p)"
```

### API

```bash
# Requires PostgreSQL running (use Docker or local install)
cd api
Rscript run.R
```

### Frontend

```bash
cd frontend
npm install
npm run dev        # Dev server on :5173
npm test           # Run tests (46 tests)
npm run build      # Production build
```

## Project Structure

```
.
├── r-package/               # Core R package (fisherapp)
│   ├── R/                   # Source code
│   │   ├── problem_engine.R       # generate_problem(), draw_params()
│   │   ├── answer_checker.R       # check_answer(), compare_answers()
│   │   ├── template_registry.R    # Template registration system
│   │   ├── templates_*.R          # 8 topic template files (40 templates)
│   │   ├── knowledge_graph.R      # Topic graph with prerequisites
│   │   ├── student_model.R        # Student state management
│   │   ├── sm2_engine.R           # SM-2 spaced repetition
│   │   ├── mastery.R              # Mastery evaluation
│   │   ├── adaptive_difficulty.R  # Difficulty adjustment
│   │   ├── next_problem.R         # Topic selection algorithm
│   │   ├── cat_placement.R        # Adaptive placement test
│   │   ├── session.R              # Session orchestration
│   │   └── db_adapter.R           # PostgreSQL persistence
│   ├── inst/knowledge_graph/      # YAML topic definitions
│   └── tests/testthat/            # 581 R tests
├── api/                     # Plumber REST API
│   ├── plumber.R                  # 11 endpoints
│   ├── run.R                      # Entry point
│   └── R/                         # Handlers, middleware, caching
├── frontend/                # React frontend
│   ├── src/
│   │   ├── pages/                 # Login, Placement, Practice, Dashboard
│   │   ├── components/            # 11 reusable components
│   │   ├── api/client.ts          # Typed API client
│   │   └── context/AuthContext.tsx # Auth state
│   └── src/**/*.test.*            # 46 frontend tests
├── db/                      # Database
│   ├── schema.sql                 # 6 tables
│   └── seed.sql                   # UC Berkeley + STAT 20 seed data
├── docker-compose.yml       # Full stack orchestration
└── Dockerfile               # API container
```

## License

MIT License. Copyright 2026, John Jacobsen.
