-- =============================================================================
-- Seed data for BerkeleyStats Tutor
-- =============================================================================

-- Default institution
INSERT INTO institutions (institution_id, name, domain)
VALUES (
  'a0000000-0000-0000-0000-000000000001',
  'UC Berkeley',
  'berkeley.edu'
);

-- Default course
INSERT INTO courses (course_id, course_code, title, institution_id)
VALUES (
  'b0000000-0000-0000-0000-000000000001',
  'STAT 20',
  'Introduction to Probability and Statistics',
  'a0000000-0000-0000-0000-000000000001'
);
