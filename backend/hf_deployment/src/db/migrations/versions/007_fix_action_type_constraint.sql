-- Migration 007: Fix task_history action_type constraint to include all enum values
--
-- This migration fixes the CHECK constraint on the action_type column in task_history
-- table to include all values from the HistoryActionType enum.
--
-- CREATED, UPDATED, COMPLETED, DELETED, ARCHIVED, RESTORED

-- Drop the old constraint if it exists
ALTER TABLE IF EXISTS task_history 
DROP CONSTRAINT IF EXISTS task_history_action_type_check;

-- Add new constraint with all enum values
ALTER TABLE task_history 
ADD CONSTRAINT task_history_action_type_check 
CHECK (action_type IN ('CREATED', 'UPDATED', 'COMPLETED', 'DELETED', 'ARCHIVED', 'RESTORED'));
