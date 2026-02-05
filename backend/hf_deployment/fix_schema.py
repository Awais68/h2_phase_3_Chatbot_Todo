#!/usr/bin/env python3
"""Fix task schema to match the model"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = False

try:
    cur = conn.cursor()

    print("🔧 Fixing tasks table schema...")

    # Add missing columns
    alterations = [
        "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(20)",
        "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE",
        "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS reminder_minutes INTEGER DEFAULT 15",
        "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS next_occurrence TIMESTAMP WITH TIME ZONE",
    ]

    for sql in alterations:
        print(f"  Executing: {sql}")
        cur.execute(sql)

    # Add indexes
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL",
        "CREATE INDEX IF NOT EXISTS idx_tasks_user_due ON tasks(user_id, due_date)",
        "CREATE INDEX IF NOT EXISTS idx_tasks_recurring ON tasks(user_id, is_recurring) WHERE is_recurring = TRUE",
        "CREATE INDEX IF NOT EXISTS idx_tasks_overdue ON tasks(user_id, due_date, completed) WHERE completed = FALSE",
    ]

    for sql in indexes:
        print(f"  Creating index: {sql[:80]}...")
        cur.execute(sql)

    # Add constraints
    constraints = [
        """
        ALTER TABLE tasks DROP CONSTRAINT IF EXISTS chk_reminder_minutes;
        ALTER TABLE tasks ADD CONSTRAINT chk_reminder_minutes
        CHECK (reminder_minutes >= 0 AND reminder_minutes <= 1440)
        """,
        """
        ALTER TABLE tasks DROP CONSTRAINT IF EXISTS chk_recurring_has_pattern;
        ALTER TABLE tasks ADD CONSTRAINT chk_recurring_has_pattern CHECK (
            (is_recurring = FALSE) OR
            (is_recurring = TRUE AND recurrence_pattern IS NOT NULL AND due_date IS NOT NULL)
        )
        """
    ]

    for sql in constraints:
        print(f"  Adding constraint...")
        cur.execute(sql)

    conn.commit()
    print("✅ Schema fixed successfully!")

    # Verify
    cur.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'tasks'
        AND column_name IN ('recurrence_pattern', 'is_recurring', 'reminder_minutes', 'next_occurrence')
        ORDER BY column_name
    """)

    print("\n📋 New columns added:")
    for row in cur.fetchall():
        print(f"  ✓ {row[0]:<25} {row[1]}")

    cur.close()

except Exception as e:
    conn.rollback()
    print(f"❌ Error: {e}")
    raise
finally:
    conn.close()
