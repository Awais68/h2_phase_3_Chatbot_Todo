-- ============================================
-- Migration 002: Add Advanced Task Fields
-- Adds due date, recurrence, and reminder support to tasks table
-- ============================================

-- Add due_date column (TIMESTAMP WITH TIME ZONE)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;

-- Add recurrence_pattern column (VARCHAR for storing recurrence type)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(50);

-- Add is_recurring column (BOOLEAN to indicate if task is recurring)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN NOT NULL DEFAULT FALSE;

-- Add reminder_minutes column (INTEGER for reminder timing)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS reminder_minutes INTEGER NOT NULL DEFAULT 15;

-- Add next_occurrence column (TIMESTAMP WITH TIME ZONE for next recurrence)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS next_occurrence TIMESTAMP WITH TIME ZONE;

-- Update the trigger to handle the new columns properly
-- (the trigger will handle updated_at automatically)

-- Create indexes for the new columns to optimize queries
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_tasks_recurrence_pattern ON tasks(recurrence_pattern) WHERE recurrence_pattern IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_tasks_is_recurring ON tasks(is_recurring) WHERE is_recurring = TRUE;

-- Update table comment to document new fields
COMMENT ON COLUMN tasks.due_date IS 'Optional due date for the task';
COMMENT ON COLUMN tasks.recurrence_pattern IS 'Recurrence pattern (daily, weekly, monthly, yearly)';
COMMENT ON COLUMN tasks.is_recurring IS 'Indicates if the task is recurring';
COMMENT ON COLUMN tasks.reminder_minutes IS 'Minutes before due date to send reminder';
COMMENT ON COLUMN tasks.next_occurrence IS 'Next occurrence date for recurring tasks';

-- Example usage after migration:
-- SELECT * FROM tasks WHERE due_date >= CURRENT_DATE AND completed = FALSE ORDER BY due_date;
-- SELECT * FROM tasks WHERE is_recurring = TRUE;