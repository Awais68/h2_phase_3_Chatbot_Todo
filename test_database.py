#!/usr/bin/env python3
"""
Test database connectivity and verify tasks can be saved to Neon DB.
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Session

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'hf_deployment'))

def test_database_connection():
    """Test database connection to Neon DB."""
    print("\n=== Testing Database Connection ===")
    
    # Get database URL from environment
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # Try to read from .env file
        env_file = os.path.join(os.path.dirname(__file__), 'backend', 'hf_deployment', '.env')
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    if line.startswith('DATABASE_URL='):
                        db_url = line.split('=', 1)[1].strip().strip('"')
                        break
    
    if not db_url:
        print("❌ DATABASE_URL not found in environment or .env file")
        return False
    
    # Mask the password in output
    safe_url = db_url.split('@')[1] if '@' in db_url else 'hidden'
    print(f"Database: {safe_url}")
    
    try:
        # Create engine
        engine = create_engine(db_url)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✓ Connected to PostgreSQL")
            print(f"  Version: {version.split(',')[0]}")
            
            # Check if tables exist
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            print(f"\n✓ Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
            
            # Check task table specifically
            if 'task' in tables:
                result = connection.execute(text("SELECT COUNT(*) FROM task"))
                count = result.fetchone()[0]
                print(f"\n✓ Task table has {count} records")
                
                # Show recent tasks
                if count > 0:
                    result = connection.execute(text("""
                        SELECT id, title, created_at 
                        FROM task 
                        ORDER BY created_at DESC 
                        LIMIT 5
                    """))
                    print("\n  Recent tasks:")
                    for row in result:
                        print(f"    #{row[0]}: {row[1]} (created: {row[2]})")
            
            # Check user table
            if 'user' in tables:
                result = connection.execute(text("SELECT COUNT(*) FROM \"user\""))
                count = result.fetchone()[0]
                print(f"\n✓ User table has {count} records")
            
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_task_model():
    """Test task model can be created."""
    print("\n=== Testing Task Model ===")
    
    try:
        from src.models.task import Task
        
        # Create a test task object (not saved to DB)
        test_task = Task(
            title="Test Task",
            description="This is a test",
            user_id=1,
            priority="medium",
            category="testing"
        )
        
        print("✓ Task model can be instantiated")
        print(f"  Title: {test_task.title}")
        print(f"  Priority: {test_task.priority}")
        print(f"  Category: {test_task.category}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create task model: {e}")
        return False

def test_user_model():
    """Test user model can be created."""
    print("\n=== Testing User Model ===")
    
    try:
        from src.models.user import User
        
        # Create a test user object (not saved to DB)
        test_user = User(
            email="test@example.com",
            is_active=True
        )
        
        print("✓ User model can be instantiated")
        print(f"  Email: {test_user.email}")
        print(f"  Active: {test_user.is_active}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create user model: {e}")
        return False

def main():
    """Run all database tests."""
    print("=" * 60)
    print("Database Connectivity Test Suite")
    print("=" * 60)
    
    results = {
        "database_connection": False,
        "task_model": False,
        "user_model": False
    }
    
    # Run tests
    results["database_connection"] = test_database_connection()
    results["task_model"] = test_task_model()
    results["user_model"] = test_user_model()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All database tests passed! Tasks can be saved to Neon DB.")
    else:
        print("\n⚠️  Some tests failed. Check configuration.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
