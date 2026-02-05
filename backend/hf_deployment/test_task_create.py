#!/usr/bin/env python3
"""Quick test to verify task creation works"""

import os
from sqlmodel import Session, create_engine
from dotenv import load_dotenv
from src.models.task import Task, TaskCreate
from src.services.task_service import TaskService

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

print("🧪 Testing task creation...")

with Session(engine) as session:
    # Create a simple task
    task_data = TaskCreate(
        title="Test Task - Quick Test",
        description="Testing if tasks save to database correctly",
        client_id="test-client-123"
    )

    task = TaskService.create_task(session, user_id=1, task_data=task_data)

    print(f"✅ Task created successfully!")
    print(f"   ID: {task.id}")
    print(f"   Title: {task.title}")
    print(f"   User ID: {task.user_id}")
    print(f"   Created at: {task.created_at}")

    # Retrieve it back
    retrieved = TaskService.get_task_by_id(session, task.id, user_id=1)
    if retrieved:
        print(f"\n✅ Task retrieved from database!")
        print(f"   Title: {retrieved.title}")
        print(f"   Completed: {retrieved.completed}")
    else:
        print(f"\n❌ Could not retrieve task from database")

print("\n🎉 Test complete - database is working!")
