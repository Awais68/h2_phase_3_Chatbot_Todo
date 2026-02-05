#!/usr/bin/env python3
"""Check actual database schema"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Get all columns in tasks table
cur.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'tasks'
    ORDER BY ordinal_position;
""")

print("📋 Current 'tasks' table schema:")
print("-" * 60)
for row in cur.fetchall():
    print(f"  {row[0]:<25} {row[1]:<20} {'NULL' if row[2] == 'YES' else 'NOT NULL'}")

cur.close()
conn.close()
