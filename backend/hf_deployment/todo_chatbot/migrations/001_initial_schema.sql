-- ============================================
-- Initial Database Schema for Phase II
-- Todo Evolution - Full Stack Web Application
-- Database: PostgreSQL (Neon)
-- ============================================
-- This script creates the initial schema for the Todo application.
-- Run this after creating your Neon database.
-- ============================================

-- Enable UUID extension for generating secure IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- USERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for email lookups (login performance)
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Index for username lookups (authentication)
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- ============================================
-- TASKS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    -- Offline sync support
    client_id VARCHAR(100),
    version INTEGER NOT NULL DEFAULT 1
);

-- Index for user task lookups (most common query)
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);

-- Index for completed status filtering
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed) WHERE completed = FALSE;

-- Index for offline sync operations
CREATE INDEX IF NOT EXISTS idx_tasks_client_id ON tasks(client_id) WHERE client_id IS NOT NULL;

-- Composite index for user's pending tasks (common view)
CREATE INDEX IF NOT EXISTS idx_tasks_user_pending
    ON tasks(user_id, completed) WHERE completed = FALSE;

-- ============================================
-- SYNC OPERATIONS TABLE (Offline Support)
-- ============================================
CREATE TABLE IF NOT EXISTS sync_operations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    operation_type VARCHAR(50) NOT NULL, -- 'create', 'update', 'delete'
    entity_type VARCHAR(50) NOT NULL, -- 'task', 'user'
    entity_id INTEGER NOT NULL,
    client_id VARCHAR(100) NOT NULL,
    payload JSONB,
    synced_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    synced BOOLEAN NOT NULL DEFAULT FALSE
);

-- Index for sync queue processing
CREATE INDEX IF NOT EXISTS idx_sync_operations_pending
    ON sync_operations(synced) WHERE synced = FALSE;

-- Index for user-specific sync
CREATE INDEX IF NOT EXISTS idx_sync_operations_user ON sync_operations(user_id);

-- ============================================
-- PUSH SUBSCRIPTIONS (Web Push Notifications)
-- ============================================
CREATE TABLE IF NOT EXISTS push_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    endpoint VARCHAR(500) NOT NULL,
    p256dh VARCHAR(255) NOT NULL,
    auth VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for user subscription lookup
CREATE INDEX IF NOT EXISTS idx_push_subscriptions_user ON push_subscriptions(user_id);

-- ============================================
-- FUNCTION: Updated_at Trigger
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ============================================
-- TRIGGERS: Auto-update updated_at
-- ============================================
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_tasks_updated_at ON tasks;
CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================
COMMENT ON TABLE users IS 'User accounts for authentication and task ownership';
COMMENT ON TABLE tasks IS 'Todo items owned by users';
COMMENT ON TABLE sync_operations IS 'Offline sync operation queue';
COMMENT ON TABLE push_subscriptions IS 'Web Push notification subscriptions';

COMMENT ON COLUMN users.hashed_password IS 'Argon2 hashed password';
COMMENT ON COLUMN tasks.client_id IS 'Offline client identifier for sync';
COMMENT ON COLUMN sync_operations.operation_type IS 'Type of sync operation: create, update, delete';
