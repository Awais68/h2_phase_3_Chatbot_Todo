#!/usr/bin/env python3
"""
Verification script to check database connection and task storage.
"""
import sys
from sqlmodel import Session, select
from src.db.session import engine
from src.models.task import Task, TaskCreate
from src.services.task_service import TaskService


def verify_database():
    """Verify database connection and task storage."""
    print("🔍 Verifying database connection and task storage...")

    try:
        # Test 1: Check database connection
        print("\n1. Testing database connection...")
        with Session(engine) as session:
            # Try a simple query
            result = session.exec(select(Task)).first()
            print("   ✅ Database connection successful")

        # Test 2: Create a test task
        print("\n2. Creating a test task...")
        with Session(engine) as session:
            test_task = TaskCreate(
                title="Test Task - Verify DB",
                description="This is a test task to verify database storage"
            )

            created_task = TaskService.create_task(
                session=session,
                user_id=1,
                task_data=test_task
            )

            print(f"   ✅ Task created with ID: {created_task.id}")
            print(f"   Title: {created_task.title}")
            print(f"   Created at: {created_task.created_at}")

        # Test 3: Retrieve the task
        print("\n3. Retrieving the task from database...")
        with Session(engine) as session:
            retrieved_task = session.get(Task, created_task.id)
            if retrieved_task:
                print(f"   ✅ Task retrieved successfully")
                print(f"   ID: {retrieved_task.id}")
                print(f"   Title: {retrieved_task.title}")
                print(f"   User ID: {retrieved_task.user_id}")
                print(f"   Completed: {retrieved_task.completed}")
            else:
                print("   ❌ Task not found in database")
                return False

        # Test 4: List all tasks
        print("\n4. Listing all tasks in database...")
        with Session(engine) as session:
            all_tasks = TaskService.get_tasks(session, user_id=1)
            print(f"   ✅ Found {len(all_tasks)} tasks for user 1")
            for task in all_tasks[:5]:  # Show first 5
                print(f"      - {task.id}: {task.title}")

        # Test 5: Create task with due date
        print("\n5. Creating task with due date...")
        with Session(engine) as session:
            task_with_due = TaskCreate(
                title="Task with Due Date",
                description="Testing due date functionality"
            )

            created_task = TaskService.create_task(
                session=session,
                user_id=1,
                task_data=task_with_due,
                due_date_text="tomorrow at 3pm",
                user_timezone="UTC"
            )

            print(f"   ✅ Task with due date created: {created_task.id}")
            print(f"   Due date: {created_task.due_date}")
            print(f"   Reminder minutes: {created_task.reminder_minutes}")

        # Test 6: Create recurring task
        print("\n6. Creating recurring task...")
        with Session(engine) as session:
            recurring_task = TaskCreate(
                title="Weekly Meeting",
                description="Recurring weekly team meeting"
            )

            created_task = TaskService.create_task(
                session=session,
                user_id=1,
                task_data=recurring_task,
                due_date_text="next Monday at 9am",
                user_timezone="UTC",
                recurrence_pattern="weekly"
            )

            print(f"   ✅ Recurring task created: {created_task.id}")
            print(f"   Due date: {created_task.due_date}")
            print(f"   Recurrence: {created_task.recurrence_pattern}")
            print(f"   Is recurring: {created_task.is_recurring}")
            print(f"   Next occurrence: {created_task.next_occurrence}")

        print("\n✅ All verification tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = verify_database()
    sys.exit(0 if success else 1)
