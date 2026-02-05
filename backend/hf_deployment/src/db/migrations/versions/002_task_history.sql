-- Migration 002: Create TaskHistory Table
-- Feature: 012-advanced-todo-features
-- Date: 2026-02-05
-- Purpose: Immutable record of completed and deleted tasks for audit trail and restoration

CREATE TABLE task_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    original_task_id INTEGER NOT NULL,

    -- Snapshot fields (immutable copy of task at time of action)
    title VARCHAR(200) NOT NULL,
    description TEXT DEFAULT '',
    completed BOOLEAN DEFAULT FALSE,
    due_date TIMESTAMP WITH TIME ZONE,
    recurrence_pattern VARCHAR(20),

    -- History metadata
    action_type VARCHAR(20) NOT NULL CHECK (action_type IN ('completed', 'deleted')),
    action_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    action_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    can_restore BOOLEAN DEFAULT FALSE,
    retention_until TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Indexes for efficient queries
CREATE INDEX idx_history_user_action_date ON task_history(user_id, action_date);
CREATE INDEX idx_history_action_type ON task_history(user_id, action_type);
CREATE INDEX idx_history_retention ON task_history(retention_until);
CREATE INDEX idx_history_search ON task_history USING gin(to_tsvector('english', title));

-- Comments for documentation
COMMENT ON TABLE task_history IS 'Immutable archive of completed and deleted tasks (2-year retention)';
COMMENT ON COLUMN task_history.original_task_id IS 'Reference to original task ID before archival';
COMMENT ON COLUMN task_history.action_type IS 'What happened: completed or deleted';
COMMENT ON COLUMN task_history.can_restore IS 'Whether task can be restored (true for deleted, false for completed)';
COMMENT ON COLUMN task_history.retention_until IS 'When to auto-purge (action_date + 2 years)';
