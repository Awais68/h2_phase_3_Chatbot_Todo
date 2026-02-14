#!/usr/bin/env python3
"""
Test script to verify backend API, authentication, and database connectivity.
"""
import requests
import json
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8001"

def test_health():
    """Test health check endpoint."""
    print("\n=== Testing Health Check ===")
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_root():
    """Test root endpoint."""
    print("\n=== Testing Root Endpoint ===")
    try:
        response = requests.get(f"{BACKEND_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_cors():
    """Test CORS headers."""
    print("\n=== Testing CORS Configuration ===")
    try:
        headers = {
            "Origin": "http://192.168.100.7:3000"
        }
        response = requests.options(f"{BACKEND_URL}/api/tasks", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"CORS Headers:")
        for header in ['access-control-allow-origin', 'access-control-allow-credentials', 
                       'access-control-allow-methods', 'access-control-allow-headers']:
            if header in response.headers:
                print(f"  {header}: {response.headers[header]}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_signup():
    """Test user signup."""
    print("\n=== Testing User Signup ===")
    try:
        # Generate unique email
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        email = f"testuser_{timestamp}@example.com"
        password = "TestPassword123!"
        
        data = {
            "email": email,
            "password": password,
            "name": "Test User"
        }
        
        response = requests.post(f"{BACKEND_URL}/api/auth/signup", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_login(email, password):
    """Test user login."""
    print("\n=== Testing User Login ===")
    try:
        data = {
            "email": email,
            "password": password
        }
        
        response = requests.post(f"{BACKEND_URL}/api/auth/login", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_create_task(token):
    """Test task creation."""
    print("\n=== Testing Task Creation ===")
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        data = {
            "title": "Test Task from API Test",
            "description": "This is a test task to verify database connectivity",
            "priority": "medium",
            "category": "testing",
            "tags": ["test", "api"],
            "completed": False
        }
        
        response = requests.post(f"{BACKEND_URL}/api/tasks", json=data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code in [200, 201]:
            return response.json()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_get_tasks(token):
    """Test getting tasks."""
    print("\n=== Testing Get Tasks ===")
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(f"{BACKEND_URL}/api/tasks", headers=headers)
        print(f"Status: {response.status_code}")
        tasks = response.json()
        print(f"Found {len(tasks)} tasks")
        if tasks:
            print(f"Latest task: {json.dumps(tasks[0], indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Backend API Test Suite")
    print("=" * 60)
    
    results = {
        "health": False,
        "root": False,
        "cors": False,
        "signup": False,
        "login": False,
        "create_task": False,
        "get_tasks": False
    }
    
    # Basic tests
    results["health"] = test_health()
    results["root"] = test_root()
    results["cors"] = test_cors()
    
    # Authentication tests
    user = test_signup()
    if user:
        results["signup"] = True
        email = user.get("email")
        password = "TestPassword123!"
        
        token = test_login(email, password)
        if token:
            results["login"] = True
            
            # Task tests
            task = test_create_task(token)
            if task:
                results["create_task"] = True
                results["get_tasks"] = test_get_tasks(token)
    
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
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
