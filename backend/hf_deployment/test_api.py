"""
Test task creation endpoint to verify the fix
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_task():
    """Test creating a task"""
    print("Testing task creation...")
    
    # Test data
    task_data = {
        "title": "Test Task",
        "description": "Testing task creation after database fix",
        "priority": "medium",
        "status": "pending",
        "category": "work",
        "tags": ["test"]
    }
    
    # Test with user_id in query parameter
    user_id = "test@example.com"
    headers = {
        "Content-Type": "application/json",
        "X-User-Email": "test@example.com",
        "X-User-Name": "Test User"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/tasks?user_id={user_id}",
            json=task_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Task created successfully!")
            return response.json()
        else:
            print(f"❌ Failed to create task: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_delete_task(task_id: int):
    """Test deleting a task to verify history constraint fix"""
    print(f"\nTesting task deletion (ID: {task_id})...")
    
    user_id = "test@example.com"
    
    try:
        response = requests.delete(
            f"{BASE_URL}/tasks/{task_id}?user_id={user_id}"
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 204:
            print("✅ Task deleted successfully! (Database constraint fix verified)")
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Task API Test Suite")
    print("=" * 50)
    
    # Test creation
    task = test_create_task()
    
    # Test deletion if task was created
    if task and 'id' in task:
        test_delete_task(task['id'])
    
    print("\n" + "=" * 50)
    print("Test Complete")
    print("=" * 50)
