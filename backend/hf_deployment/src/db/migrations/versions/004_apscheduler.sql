-- Migration 004: Create APScheduler Job Store Table
-- Feature: 012-advanced-todo-features
-- Date: 2026-02-05
-- Purpose: Enable stateless backend with persistent background job storage

-- APScheduler requires this table structure for PostgreSQL jobstore
CREATE TABLE apscheduler_jobs (
    id VARCHAR(191) PRIMARY KEY,
    next_run_time DOUBLE PRECISION,
    job_state BYTEA NOT NULL
);

-- Index for efficient job retrieval by next run time
CREATE INDEX idx_apscheduler_jobs_next_run_time ON apscheduler_jobs(next_run_time);

-- Comments for documentation
COMMENT ON TABLE apscheduler_jobs IS 'Persistent storage for APScheduler background jobs (notifications, cleanup)';
COMMENT ON COLUMN apscheduler_jobs.id IS 'Unique job identifier';
COMMENT ON COLUMN apscheduler_jobs.next_run_time IS 'Unix timestamp of next scheduled execution';
COMMENT ON COLUMN apscheduler_jobs.job_state IS 'Serialized job state (pickle format)';
