-- Migration 001: Extend Task Table with Advanced Features
-- Feature: 012-advanced-todo-features
-- Date: 2026-02-05
-- Purpose: Add due dates, recurrence, and reminder support to tasks table

-- Add new columns to existing tasks table
ALTER TABLE tasks
    ADD COLUMN due_date TIMESTAMP WITH TIME ZONE,
    ADD COLUMN recurrence_pattern VARCHAR(20),
    ADD COLUMN is_recurring BOOLEAN DEFAULT FALSE,
    ADD COLUMN reminder_minutes INTEGER DEFAULT 15,
    ADD COLUMN next_occurrence TIMESTAMP WITH TIME ZONE;

-- Add new indexes for performance
CREATE INDEX idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX idx_tasks_user_due ON tasks(user_id, due_date);
CREATE INDEX idx_tasks_recurring ON tasks(user_id, is_recurring) WHERE is_recurring = TRUE;
CREATE INDEX idx_tasks_overdue ON tasks(user_id, due_date, completed) WHERE completed = FALSE;

-- Add constraints for data integrity
ALTER TABLE tasks
    ADD CONSTRAINT chk_reminder_minutes CHECK (reminder_minutes >= 0 AND reminder_minutes <= 1440),
    ADD CONSTRAINT chk_recurring_has_pattern CHECK (
        (is_recurring = FALSE) OR
        (is_recurring = TRUE AND recurrence_pattern IS NOT NULL AND due_date IS NOT NULL)
    );

-- Comments for documentation
COMMENT ON COLUMN tasks.due_date IS 'Task deadline in UTC timezone';
COMMENT ON COLUMN tasks.recurrence_pattern IS 'Recurrence type: daily/weekly/bi-weekly/monthly/yearly';
COMMENT ON COLUMN tasks.is_recurring IS 'Whether task auto-creates next instance on completion';
COMMENT ON COLUMN tasks.reminder_minutes IS 'Minutes before due_date to send reminder (0-1440)';
COMMENT ON COLUMN tasks.next_occurrence IS 'Auto-calculated next due date for recurring tasks';
