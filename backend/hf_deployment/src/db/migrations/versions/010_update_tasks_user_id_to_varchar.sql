-- Migration 010: Update tasks.user_id from integer to VARCHAR(255)
-- This migration changes user_id in tasks table to match backend_users.id type
-- Reason: Better Auth uses VARCHAR user IDs, we need consistency across tables

BEGIN;

-- Step 1: Migrate existing integer user IDs to backend_users table as strings
-- This ensures we don't lose any data when we change the type
INSERT INTO backend_users (id, email, username, hashed_password, is_active, is_superuser, created_at, updated_at)
SELECT DISTINCT t.user_id::VARCHAR(255), 
                CONCAT('user_', t.user_id, '@migrated.local'),
                CONCAT('user_', t.user_id),
                '$2b$12$DUMMY_HASH_MIGRATED_USER_NO_PASSWORD',
                TRUE,
                FALSE,
                NOW(),
                NOW()
FROM tasks t
WHERE NOT EXISTS (
    SELECT 1 FROM backend_users bu WHERE bu.id = t.user_id::VARCHAR(255)
)
ON CONFLICT (email) DO NOTHING;

-- Step 2: Drop foreign key constraint if it exists (it shouldn't exist yet, but safe to try)
DO $$
BEGIN
    ALTER TABLE IF EXISTS tasks DROP CONSTRAINT IF EXISTS tasks_user_id_fkey;
EXCEPTION
    WHEN undefined_object THEN
        NULL; -- Ignore error if constraint doesn't exist
END $$;

-- Step 3: Change user_id column type from integer to VARCHAR(255)
ALTER TABLE tasks 
ALTER COLUMN user_id TYPE VARCHAR(255) USING user_id::VARCHAR(255);

-- Step 4: Ensure the column is NOT NULL and indexed
ALTER TABLE tasks ALTER COLUMN user_id SET NOT NULL;
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);

-- Step 5: Add foreign key constraint to backend_users table
ALTER TABLE tasks 
ADD CONSTRAINT tasks_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES backend_users(id) ON DELETE CASCADE;

COMMIT;
