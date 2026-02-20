-- Migration 003: Add placement_sessions table for durable in-progress placement state
-- Without this, placement progress is lost on server restart.

CREATE TABLE IF NOT EXISTS placement_sessions (
  student_id  UUID PRIMARY KEY REFERENCES students(student_id) ON DELETE CASCADE,
  state       JSONB NOT NULL,
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
