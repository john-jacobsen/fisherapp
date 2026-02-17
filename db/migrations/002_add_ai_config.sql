-- Add AI provider configuration columns to students table
ALTER TABLE students ADD COLUMN IF NOT EXISTS ai_provider TEXT CHECK (ai_provider IN ('anthropic', 'openai'));
ALTER TABLE students ADD COLUMN IF NOT EXISTS ai_api_key_encrypted TEXT;
