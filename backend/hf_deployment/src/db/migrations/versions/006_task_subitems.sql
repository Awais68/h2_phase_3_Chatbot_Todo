-- Migration: Add subitems field to tasks table
-- Version: 006
-- Description: Adds subitems/checklist support to tasks as JSON array

-- Add subitems column (JSON array for checklist items) if not exists
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='tasks' AND column_name='subitems') THEN
        ALTER TABLE tasks ADD COLUMN subitems JSONB;
    END IF;
END $$;

-- Convert existing json column to jsonb if needed
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='tasks' AND column_name='subitems' AND data_type='json'
    ) THEN
        ALTER TABLE tasks ALTER COLUMN subitems TYPE JSONB USING subitems::jsonb;
    END IF;
END $$;

-- Create index for better query performance (using jsonb_path_ops for JSONB)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_tasks_subitems') THEN
        CREATE INDEX idx_tasks_subitems ON tasks USING GIN (subitems jsonb_path_ops) WHERE subitems IS NOT NULL;
    END IF;
END $$;

COMMENT ON COLUMN tasks.subitems IS 'Task subitems/checklist as JSON array';
