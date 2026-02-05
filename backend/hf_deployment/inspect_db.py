#!/usr/bin/env python3
"""
Database inspection script to check tables and data.
"""
from sqlmodel import Session, select, text
from src.db.session import engine
from src.models.task import Task


def inspect_database():
    """Inspect database tables and show task data."""
    print("📊 Database Inspection Report")
    print("=" * 60)

    with Session(engine) as session:
        # Check if tasks table exists
        print("\n1. Checking database schema...")
        try:
            result = session.exec(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = result.all()
            print(f"   Found {len(tables)} tables:")
            for table in tables:
                print(f"      - {table[0]}")
        except Exception as e:
            print(f"   ⚠️  Could not list tables: {e}")

        # Check tasks table structure
        print("\n2. Tasks table structure...")
        try:
            result = session.exec(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'tasks'
                ORDER BY ordinal_position;
            """))
            columns = result.all()
            print(f"   Found {len(columns)} columns:")
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                print(f"      - {col[0]}: {col[1]} ({nullable})")
        except Exception as e:
            print(f"   ⚠️  Could not describe tasks table: {e}")

        # Count tasks
        print("\n3. Task counts...")
        try:
            statement = select(Task)
            all_tasks = session.exec(statement).all()
            print(f"   Total tasks: {len(all_tasks)}")

            # Count by completion status
            completed = [t for t in all_tasks if t.completed]
            pending = [t for t in all_tasks if not t.completed]
            print(f"   Completed: {len(completed)}")
            print(f"   Pending: {len(pending)}")

            # Count tasks with due dates
            with_due = [t for t in all_tasks if t.due_date]
            print(f"   With due dates: {len(with_due)}")

            # Count recurring tasks
            recurring = [t for t in all_tasks if t.is_recurring]
            print(f"   Recurring tasks: {len(recurring)}")

        except Exception as e:
            print(f"   ⚠️  Could not count tasks: {e}")

        # Show sample tasks
        print("\n4. Sample tasks (first 10)...")
        try:
            statement = select(Task).limit(10)
            tasks = session.exec(statement).all()

            if tasks:
                for task in tasks:
                    status = "✅" if task.completed else "⏳"
                    due = f"📅 {task.due_date.strftime('%Y-%m-%d %H:%M')}" if task.due_date else "No due date"
                    recur = f"🔄 {task.recurrence_pattern}" if task.is_recurring else ""
                    print(f"   {status} [{task.id}] {task.title}")
                    print(f"      {due} {recur}")
            else:
                print("   No tasks found in database")

        except Exception as e:
            print(f"   ⚠️  Could not list tasks: {e}")

    print("\n" + "=" * 60)
    print("✅ Inspection complete!")


if __name__ == "__main__":
    inspect_database()
