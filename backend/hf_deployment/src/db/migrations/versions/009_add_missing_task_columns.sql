-- Migration 009: Add missing columns to tasks table
--
-- Adds columns that the backend Task model needs but are missing from the database

-- Add completed column if it doesn't exist
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS completed BOOLEAN DEFAULT FALSE;

-- Add client_id and version for offline sync support
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS client_id VARCHAR(100);
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;

-- Add reminder_minutes if it doesn't exist
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS reminder_minutes INTEGER DEFAULT 15;

-- Add recurrence-related columns
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE;
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(20);
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS next_occurrence TIMESTAMP WITH TIME ZONE;

-- Add shopping_list if it doesn't exist (from migration 005)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS shopping_list JSONB;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_tasks_client_id ON tasks(client_id);
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
CREATE INDEX IF NOT EXISTS idx_tasks_user_completed ON tasks(user_id, completed);
