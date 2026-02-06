#!/usr/bin/env python3
"""Run SQL migrations against the database"""

import os
import sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Load environment
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env")
    sys.exit(1)

# Migration files in order
MIGRATIONS = [
    "src/db/migrations/versions/001_extend_tasks.sql",
    "src/db/migrations/versions/002_task_history.sql",
    "src/db/migrations/versions/003_notif_prefs.sql",
    "src/db/migrations/versions/004_apscheduler.sql",
    "src/db/migrations/versions/005_task_metadata_fields.sql",
]

def run_migration(conn, migration_file):
    """Run a single migration file"""
    print(f"🔄 Running {migration_file}...")

    with open(migration_file, 'r') as f:
        sql = f.read()

    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        print(f"✅ {migration_file} applied successfully")
        return True
    except psycopg2.errors.DuplicateColumn as e:
        conn.rollback()
        print(f"⚠️  {migration_file} - columns already exist (skipping)")
        return True
    except psycopg2.errors.DuplicateTable as e:
        conn.rollback()
        print(f"⚠️  {migration_file} - table already exists (skipping)")
        return True
    except psycopg2.errors.DuplicateObject as e:
        conn.rollback()
        print(f"⚠️  {migration_file} - object already exists (skipping)")
        return True
    except Exception as e:
        conn.rollback()
        print(f"❌ {migration_file} failed: {e}")
        return False

def main():
    print("🗄️  Starting database migrations...")
    print(f"📍 Database: {DATABASE_URL.split('@')[1].split('/')[0]}")

    # Connect to database
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("✅ Connected to database\n")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        sys.exit(1)

    # Run each migration
    success_count = 0
    for migration in MIGRATIONS:
        if Path(migration).exists():
            if run_migration(conn, migration):
                success_count += 1
        else:
            print(f"⚠️  {migration} not found (skipping)")

    conn.close()

    print(f"\n🎉 Migrations complete! {success_count}/{len(MIGRATIONS)} applied")

if __name__ == "__main__":
    main()
