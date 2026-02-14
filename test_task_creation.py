#!/usr/bin/env python3
"""
Test task creation and verify it saves to database.
"""
import requests
import json
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8001"

def test_task_creation():
    """Test task creation and verify it's saved to database."""
    print("\n=== Testing Task Creation ===")
    
    # Create a test task with demo user
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    test_email = f"testuser_{timestamp}@example.com"
    
    task_data = {
        "title": f"Test Task {timestamp}",
        "description": "This is a test task to verify database saving",
        "priority": "high",
        "category": "testing",
        "tags": ["test", "api", "database"],
        "completed": False,
        "status": "pending"
    }
    
    # Create task with user query parameter and headers
    headers = {
        "X-User-Email": test_email,
        "X-User-Name": "Test User"
    }
    
    print(f"Creating task for user: {test_email}")
    response = requests.post(
        f"{BACKEND_URL}/tasks?user_id={test_email}",
        json=task_data,
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code in [200, 201]:
        task = response.json()
        task_id = task.get("id")
        print(f"\n✓ Task created successfully! ID: {task_id}")
        
        # Now try to retrieve it
        print(f"\n=== Retrieving Tasks ===")
        get_response = requests.get(
            f"{BACKEND_URL}/tasks?user_id={test_email}",
            headers=headers
        )
        
        print(f"Status Code: {get_response.status_code}")
        if get_response.status_code == 200:
            tasks = get_response.json()
            print(f"Found {len(tasks)} tasks")
            
            if tasks:
                print(f"\n✓ Task retrieved from database!")
                print(f"Task Details: {json.dumps(tasks[0], indent=2)}")
                return True
            else:
                print(f"\n✗ No tasks found in database")
                return False
        else:
            print(f"Failed to retrieve tasks: {get_response.text}")
            return False
    else:
        print(f"\n✗ Failed to create task: {response.text}")
        return False

def main():
    """Run task creation test."""
    print("=" * 60)
    print("Task Creation & Database Persistence Test")
    print("=" * 60)
    
    try:
        success = test_task_creation()
        
        print("\n" + "=" * 60)
        if success:
            print("✅ SUCCESS: Tasks are being saved to database!")
        else:
            print("❌ FAILED: Tasks are NOT being saved to database")
        print("=" * 60)
        
        return success
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
