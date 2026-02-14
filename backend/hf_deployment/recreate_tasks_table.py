#!/usr/bin/env python3
"""Drop and recreate tasks table with correct schema."""
from sqlalchemy import text
from src.db.session import engine
from sqlmodel import SQLModel
from src.models.user import User
from src.models.task import Task
from src.models.task_history import TaskHistory
from src.models.notification_preference import NotificationPreference
import src.models.recurring_task
import src.models.sync_operation
import src.models.push_subscription

print("Dropping tasks table...")
with engine.connect() as conn:
    conn.execute(text('DROP TABLE IF EXISTS tasks CASCADE'))
    conn.commit()
print("✓ Tasks table dropped")

print("\nRecreating tables...")
SQLModel.metadata.create_all(engine)
print("✓ Tables recreated successfully!")

print("\nVerifying tasks table schema...")
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'tasks' AND column_name = 'user_id'
    """))
    for row in result:
        print(f"  user_id column type: {row[1]}")
