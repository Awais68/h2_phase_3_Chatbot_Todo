"""
Test script to verify chatbot task creation flow.
"""
from sqlmodel import Session
from src.db.session import engine
from src.models.user import User
from src.models.task import Task
from src.mcp.mcp_server import add_task

print("=" * 60)
print("Testing Chatbot Task Creation Flow")
print("=" * 60)

with Session(engine) as session:
    # Test 1: Check if user was auto-created by chat endpoint
    print("\n1. Checking if user 'test-user-123' was auto-created...")
    user = session.query(User).filter(User.id == 'test-user-123').first()
    if user:
        print(f"   ✅ User found: {user.id} - {user.email}")
    else:
        print("   ❌ User not found (chat endpoint may not have created it)")
        print("   Creating user for test...")
        user = User(
            id='test-user-123',
            email='test-user-123@test.local',
            username='testuser123',
            hashed_password='$2b$12$DUMMY_HASH',
            is_active=True
        )
        session.add(user)
        session.commit()
        print(f"   ✅ User created: {user.id} - {user.email}")
    
    # Test 2: List existing tasks for this user
    print("\n2. Listing existing tasks for test-user-123...")
    tasks = session.query(Task).filter(Task.user_id == 'test-user-123').all()
    print(f"   Found {len(tasks)} existing tasks")
    for task in tasks:
        print(f"   - Task #{task.id}: {task.title} [{task.status}]")
    
    # Test 3: Test MCP add_task tool directly
    print("\n3. Testing MCP add_task tool directly...")
    try:
        result = add_task(
            user_id='test-user-123',
            title='Buy groceries',
            description='Milk, bread, eggs'
        )
        print(f"   ✅ Task created successfully!")
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   ❌ Error creating task: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Verify the task was saved to database
    print("\n4. Verifying task was saved to database...")
    tasks = session.query(Task).filter(Task.user_id == 'test-user-123').all()
    print(f"   Total tasks now: {len(tasks)}")
    for task in tasks:
        print(f"   - Task #{task.id}: {task.title} [{task.status}]")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
