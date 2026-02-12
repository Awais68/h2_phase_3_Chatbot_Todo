-- Migration 008: Create backend_users table
--
-- Create a separate backend_users table to avoid conflicts with Better Auth's users table
-- The Better Auth users table is managed by Prisma (frontend), while this table is for backend users
-- Note: Using VARCHAR(255) for id to match tasks.user_id column type

CREATE TABLE IF NOT EXISTS backend_users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL DEFAULT '$2b$12$DUMMY_HASH_NO_PASSWORD',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS ix_backend_users_email ON backend_users(email);
CREATE INDEX IF NOT EXISTS ix_backend_users_username ON backend_users(username);

-- Migrate existing data from tasks table if any users referenced there don't exist in backend_users
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tasks') THEN
        INSERT INTO backend_users (id, email, username, is_active)
        SELECT DISTINCT t.user_id, 
                        CONCAT('user_', t.user_id, '@migrated.local'),
                        LEFT(t.user_id, 100),
                        TRUE
        FROM tasks t
        WHERE NOT EXISTS (
            SELECT 1 FROM backend_users bu WHERE bu.id = t.user_id
        )
        ON CONFLICT (email) DO NOTHING;
    END IF;
END $$;
