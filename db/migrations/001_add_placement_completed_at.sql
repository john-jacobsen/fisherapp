-- Add placement_completed_at column to track whether a student has completed
-- (or skipped) the placement diagnostic test.
ALTER TABLE students
  ADD COLUMN IF NOT EXISTS placement_completed_at TIMESTAMPTZ;
