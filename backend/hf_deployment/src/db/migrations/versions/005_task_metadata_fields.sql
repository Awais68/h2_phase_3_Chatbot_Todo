-- Migration: Add category, tags, status, priority, shopping_list, and recursion fields to tasks table
-- Version: 005
-- Description: Adds metadata fields to support task categorization, shopping lists, and other metadata

-- Add category column
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS category VARCHAR(100);

-- Add tags column (JSON array)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS tags JSONB DEFAULT '[]'::jsonb;

-- Add status column with default
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'pending';

-- Add priority column with default
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium';

-- Add shopping_list column (JSON array for categories and items)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS shopping_list JSONB;

-- Add recursion column for recurrence description
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recursion VARCHAR(50);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);

-- Add check constraints for valid values
ALTER TABLE tasks ADD CONSTRAINT IF NOT EXISTS check_status_values 
CHECK (status IN ('pending', 'active', 'completed', 'failed'));

ALTER TABLE tasks ADD CONSTRAINT IF NOT EXISTS check_priority_values 
CHECK (priority IN ('critical', 'high', 'medium', 'low'));

COMMENT ON COLUMN tasks.category IS 'Task category (e.g., shopping, work, personal)';
COMMENT ON COLUMN tasks.tags IS 'Task tags as JSON array';
COMMENT ON COLUMN tasks.status IS 'Task status (pending, active, completed, failed)';
COMMENT ON COLUMN tasks.priority IS 'Task priority (critical, high, medium, low)';
COMMENT ON COLUMN tasks.shopping_list IS 'Shopping list categories with items as JSON array';
COMMENT ON COLUMN tasks.recursion IS 'Recursion/recurrence description (e.g., Weekly, Monthly)';
