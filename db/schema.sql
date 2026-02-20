-- =============================================================================
-- BerkeleyStats Tutor (Fisher App) — Database Schema
-- Phase 4: PostgreSQL 16+
-- =============================================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- -----------------------------------------------------------------------------
-- Future-proofing tables
-- -----------------------------------------------------------------------------

CREATE TABLE institutions (
  institution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name           TEXT NOT NULL,
  domain         TEXT,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE courses (
  course_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  course_code    TEXT NOT NULL,
  title          TEXT NOT NULL,
  institution_id UUID REFERENCES institutions(institution_id),
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -----------------------------------------------------------------------------
-- Core tables
-- -----------------------------------------------------------------------------

CREATE TABLE students (
  student_id            UUID PRIMARY KEY,
  email                 TEXT UNIQUE NOT NULL,
  password_hash         TEXT NOT NULL,
  display_name          TEXT,
  institution_id        UUID REFERENCES institutions(institution_id),
  course_id             UUID REFERENCES courses(course_id),
  total_attempts        INTEGER NOT NULL DEFAULT 0,
  total_correct         INTEGER NOT NULL DEFAULT 0,
  placement_completed_at TIMESTAMPTZ,
  ai_provider           TEXT CHECK (ai_provider IN ('anthropic', 'openai', 'gemini', 'deepseek')),
  ai_api_key_encrypted  TEXT,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE sessions (
  session_id      UUID PRIMARY KEY,
  student_id      UUID NOT NULL REFERENCES students(student_id),
  started_at      TIMESTAMPTZ NOT NULL,
  ended_at        TIMESTAMPTZ,
  is_placement    BOOLEAN NOT NULL DEFAULT FALSE,
  problems_served INTEGER NOT NULL DEFAULT 0,
  problems_correct INTEGER NOT NULL DEFAULT 0,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE problem_attempts (
  attempt_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id     UUID NOT NULL REFERENCES sessions(session_id),
  student_id     UUID NOT NULL REFERENCES students(student_id),
  problem_id     UUID NOT NULL,
  topic_id       TEXT NOT NULL,
  difficulty     INTEGER NOT NULL CHECK (difficulty BETWEEN 1 AND 5),
  template_id    TEXT,
  student_answer TEXT,
  correct_answer TEXT NOT NULL,
  is_correct     BOOLEAN NOT NULL,
  attempt_number INTEGER NOT NULL,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Combined mastery + spaced repetition (same PK, always read/written together)
CREATE TABLE mastery_states (
  student_id       UUID NOT NULL REFERENCES students(student_id),
  topic_id         TEXT NOT NULL,
  mastery_state    TEXT NOT NULL DEFAULT 'not_started'
                   CHECK (mastery_state IN ('not_started', 'in_progress', 'mastered')),
  difficulty       INTEGER NOT NULL DEFAULT 1 CHECK (difficulty BETWEEN 1 AND 5),
  attempt_count    INTEGER NOT NULL DEFAULT 0,
  correct_count    INTEGER NOT NULL DEFAULT 0,
  session_count    INTEGER NOT NULL DEFAULT 0,
  consecutive_wrong INTEGER NOT NULL DEFAULT 0,
  last_n_results   INTEGER[] NOT NULL DEFAULT '{}',
  -- SM-2 spaced repetition fields
  ease_factor      NUMERIC(4,2) NOT NULL DEFAULT 2.50,
  sm2_interval     NUMERIC NOT NULL DEFAULT 0,
  repetition       INTEGER NOT NULL DEFAULT 0,
  next_review      TIMESTAMPTZ,
  updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (student_id, topic_id)
);

-- In-progress placement test state (persists across server restarts)
CREATE TABLE placement_sessions (
  student_id  UUID PRIMARY KEY REFERENCES students(student_id) ON DELETE CASCADE,
  state       JSONB NOT NULL,
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -----------------------------------------------------------------------------
-- Indexes
-- -----------------------------------------------------------------------------

CREATE INDEX idx_sessions_student    ON sessions(student_id);
CREATE INDEX idx_sessions_active     ON sessions(student_id) WHERE ended_at IS NULL;
CREATE INDEX idx_attempts_session    ON problem_attempts(session_id);
CREATE INDEX idx_attempts_student    ON problem_attempts(student_id);
CREATE INDEX idx_attempts_topic      ON problem_attempts(student_id, topic_id);
CREATE INDEX idx_attempts_template   ON problem_attempts(student_id, template_id)
  WHERE template_id IS NOT NULL;
CREATE INDEX idx_mastery_review      ON mastery_states(next_review)
                                     WHERE mastery_state = 'mastered';
