-- Migration 004: Add template_id to problem_attempts for cross-session dedup
-- Without this, templates_served resets every server restart, allowing repeats.

ALTER TABLE problem_attempts ADD COLUMN IF NOT EXISTS template_id TEXT;
CREATE INDEX IF NOT EXISTS idx_attempts_template ON problem_attempts(student_id, template_id)
  WHERE template_id IS NOT NULL;
