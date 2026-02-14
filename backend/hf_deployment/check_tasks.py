#!/usr/bin/env python3
"""Check tasks in database."""
from sqlalchemy import text
from src.db.session import engine

with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) FROM tasks'))
    count = result.fetchone()[0]
    print(f'\n✓ Total tasks in database: {count}')
    
    result = conn.execute(text('SELECT id, title, user_id FROM tasks ORDER BY created_at DESC LIMIT 5'))
    print(f'\nRecent tasks:')
    for row in result:
        print(f'  Task #{row[0]}: {row[1]} (user_id: {row[2]})')
