"""
Migration script to add missing columns to Neon PostgreSQL database
Run this to update the production database schema
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Connecting to database...")
engine = create_engine(DATABASE_URL)

# SQL statements to add missing columns and create trash table
migrations = [
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recursion VARCHAR(50);",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS category VARCHAR(100) DEFAULT 'General';",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS tags TEXT;",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS is_deleted BOOLEAN DEFAULT FALSE;",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;",
    """
    CREATE TABLE IF NOT EXISTS trash (
        id VARCHAR PRIMARY KEY,
        task_id VARCHAR,
        title VARCHAR NOT NULL,
        description VARCHAR,
        status VARCHAR,
        priority VARCHAR,
        created_at TIMESTAMP,
        deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id VARCHAR,
        recursion VARCHAR(50),
        category VARCHAR(100),
        tags TEXT,
        due_date TIMESTAMP
    );
    """,
    "CREATE INDEX IF NOT EXISTS idx_trash_user_id ON trash(user_id);",
    "CREATE INDEX IF NOT EXISTS idx_trash_deleted_at ON trash(deleted_at);"
]

print("Running migrations...")
with engine.connect() as conn:
    for migration in migrations:
        try:
            print(f"Executing: {migration}")
            conn.execute(text(migration))
            conn.commit()
            print("✓ Success")
        except Exception as e:
            print(f"✗ Error: {e}")
            conn.rollback()

print("\n✅ Migration complete!")
print("\nVerifying table structure...")
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT column_name, data_type, character_maximum_length 
        FROM information_schema.columns 
        WHERE table_name = 'tasks'
        ORDER BY ordinal_position;
    """))
    print("\nCurrent table structure:")
    for row in result:
        print(f"  - {row[0]}: {row[1]}" + (f"({row[2]})" if row[2] else ""))
