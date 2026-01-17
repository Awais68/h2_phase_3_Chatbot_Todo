# API Documentation

## Overview

This document provides comprehensive documentation for all API endpoints in the Todo AI Chatbot backend.

**Base URL**: `http://localhost:8000`

**API Version**: 1.0

**Authentication**: User ID-based (to be replaced with Better Auth)

## Table of Contents

1. [Chat Endpoints](#chat-endpoints)
2. [Analytics Endpoints](#analytics-endpoints)
3. [Recurring Tasks Endpoints](#recurring-tasks-endpoints)
4. [Task Endpoints](#task-endpoints)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)

---

## Chat Endpoints

### POST /api/{user_id}/chat

Send a message to the AI chatbot and receive a response.

**URL**: `/api/{user_id}/chat`

**Method**: `POST`

**URL Parameters**:
- `user_id` (integer, required): The ID of the user sending the message

**Request Body**:
```json
{
  "conversation_id": 1,  // Optional: existing conversation ID
  "message": "Add a task to buy groceries"  // Required: user message
}
```

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "conversation_id": 1,
  "response": "✓ Task created successfully! I've added 'Buy groceries' to your task list.",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {
        "user_id": 1,
        "title": "Buy groceries",
        "description": ""
      },
      "result": {
        "task_id": 42,
        "status": "pending",
        "title": "Buy groceries"
      }
    }
  ]
}
```

**Error Responses**:

**Code**: `400 BAD REQUEST`
```json
{
  "detail": "Message cannot be empty"
}
```

**Code**: `404 NOT FOUND`
```json
{
  "detail": "Conversation not found"
}
```

**Example Usage**:

```bash
# Create new conversation
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'

# Continue existing conversation
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 1,
    "message": "Show me all my tasks"
  }'
```

**Notes**:
- If `conversation_id` is not provided, a new conversation is created
- The AI agent automatically invokes appropriate MCP tools based on the message
- Tool calls are returned for transparency and debugging

---

## Analytics Endpoints

### GET /api/{user_id}/analytics/overview

Get overall task statistics for a user.

**URL**: `/api/{user_id}/analytics/overview`

**Method**: `GET`

**URL Parameters**:
- `user_id` (integer, required): The ID of the user

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "total_tasks": 10,
  "completed_tasks": 6,
  "pending_tasks": 4,
  "completion_rate": 60.0
}
```

**Example Usage**:
```bash
curl http://localhost:8000/api/1/analytics/overview
```

---

### GET /api/{user_id}/analytics/timeline

Get task creation and completion trends over time.

**URL**: `/api/{user_id}/analytics/timeline`

**Method**: `GET`

**URL Parameters**:
- `user_id` (integer, required): The ID of the user
- `days` (integer, optional): Number of days to look back (default: 30)

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "timeline": [
    {
      "date": "2026-01-01",
      "created": 3,
      "completed": 2
    },
    {
      "date": "2026-01-02",
      "created": 5,
      "completed": 4
    }
  ],
  "days": 30
}
```

**Example Usage**:
```bash
# Last 30 days (default)
curl http://localhost:8000/api/1/analytics/timeline

# Last 7 days
curl http://localhost:8000/api/1/analytics/timeline?days=7
```

---

### GET /api/{user_id}/analytics/completion

Get detailed completion analytics.

**URL**: `/api/{user_id}/analytics/completion`

**Method**: `GET`

**URL Parameters**:
- `user_id` (integer, required): The ID of the user

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "total": 10,
  "completed": 6,
  "pending": 4,
  "completion_rate": 60.0,
  "avg_completion_time_hours": 24.5
}
```

**Example Usage**:
```bash
curl http://localhost:8000/api/1/analytics/completion
```

---

### GET /api/{user_id}/analytics/productivity

Get productivity statistics by hour of day.

**URL**: `/api/{user_id}/analytics/productivity`

**Method**: `GET`

**URL Parameters**:
- `user_id` (integer, required): The ID of the user

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "productivity_by_hour": [
    {"hour": 0, "tasks_completed": 0},
    {"hour": 1, "tasks_completed": 0},
    {"hour": 9, "tasks_completed": 5},
    {"hour": 10, "tasks_completed": 8},
    {"hour": 14, "tasks_completed": 6},
    {"hour": 23, "tasks_completed": 1}
  ]
}
```

**Example Usage**:
```bash
curl http://localhost:8000/api/1/analytics/productivity
```

---

## Recurring Tasks Endpoints

### POST /api/{user_id}/recurring

Create a new recurring task.

**URL**: `/api/{user_id}/recurring`

**Method**: `POST`

**URL Parameters**:
- `user_id` (integer, required): The ID of the user

**Request Body**:
```json
{
  "title": "Daily standup",
  "description": "Team standup meeting",
  "frequency": "daily",  // "daily", "weekly", or "monthly"
  "frequency_value": null  // Optional: day of week (0-6) or day of month (1-31)
}
```

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "recurring_task_id": 1,
  "status": "created",
  "title": "Daily standup",
  "frequency": "daily"
}
```

**Error Responses**:

**Code**: `400 BAD REQUEST`
```json
{
  "detail": "Frequency must be 'daily', 'weekly', or 'monthly'"
}
```

**Example Usage**:
```bash
# Daily recurring task
curl -X POST http://localhost:8000/api/1/recurring \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Daily standup",
    "frequency": "daily"
  }'

# Weekly recurring task (every Monday)
curl -X POST http://localhost:8000/api/1/recurring \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team meeting",
    "frequency": "weekly",
    "frequency_value": 1
  }'

# Monthly recurring task (1st of month)
curl -X POST http://localhost:8000/api/1/recurring \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Monthly report",
    "frequency": "monthly",
    "frequency_value": 1
  }'
```

---

### GET /api/{user_id}/recurring

List all recurring tasks for a user.

**URL**: `/api/{user_id}/recurring`

**Method**: `GET`

**URL Parameters**:
- `user_id` (integer, required): The ID of the user

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "recurring_tasks": [
    {
      "recurring_task_id": 1,
      "title": "Daily standup",
      "description": "Team standup meeting",
      "frequency": "daily",
      "frequency_value": null,
      "is_active": true,
      "last_generated": "2026-01-10T10:00:00Z",
      "created_at": "2026-01-01T09:00:00Z"
    }
  ],
  "count": 1
}
```

**Example Usage**:
```bash
curl http://localhost:8000/api/1/recurring
```

---

### PATCH /api/{user_id}/recurring/{recurring_task_id}/pause

Pause a recurring task.

**URL**: `/api/{user_id}/recurring/{recurring_task_id}/pause`

**Method**: `PATCH`

**URL Parameters**:
- `user_id` (integer, required): The ID of the user
- `recurring_task_id` (integer, required): The ID of the recurring task

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "status": "paused",
  "recurring_task_id": 1
}
```

**Example Usage**:
```bash
curl -X PATCH http://localhost:8000/api/1/recurring/1/pause
```

---

### PATCH /api/{user_id}/recurring/{recurring_task_id}/resume

Resume a paused recurring task.

**URL**: `/api/{user_id}/recurring/{recurring_task_id}/resume`

**Method**: `PATCH`

**URL Parameters**:
- `user_id` (integer, required): The ID of the user
- `recurring_task_id` (integer, required): The ID of the recurring task

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "status": "resumed",
  "recurring_task_id": 1
}
```

**Example Usage**:
```bash
curl -X PATCH http://localhost:8000/api/1/recurring/1/resume
```

---

### DELETE /api/{user_id}/recurring/{recurring_task_id}

Delete a recurring task.

**URL**: `/api/{user_id}/recurring/{recurring_task_id}`

**Method**: `DELETE`

**URL Parameters**:
- `user_id` (integer, required): The ID of the user
- `recurring_task_id` (integer, required): The ID of the recurring task

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "status": "deleted",
  "recurring_task_id": 1
}
```

**Example Usage**:
```bash
curl -X DELETE http://localhost:8000/api/1/recurring/1
```

---

## Task Endpoints

### GET /api/tasks

List all tasks for a user (existing endpoint).

**URL**: `/api/tasks`

**Method**: `GET`

**Query Parameters**:
- `user_id` (integer, required): The ID of the user
- `status` (string, optional): Filter by status ("pending", "completed", "all")

**Success Response**:

**Code**: `200 OK`

**Content**:
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-10T10:00:00Z",
      "updated_at": "2026-01-10T10:00:00Z"
    }
  ]
}
```

---

## Error Handling

### Standard Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters or body |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

### Common Error Scenarios

**1. Invalid User ID**:
```json
{
  "detail": "User not found"
}
```

**2. Invalid Task ID**:
```json
{
  "detail": "Task with ID 999 not found"
}
```

**3. Validation Error**:
```json
{
  "detail": "Title must be between 1 and 200 characters"
}
```

**4. Missing Required Field**:
```json
{
  "detail": "Message cannot be empty"
}
```

---

## Rate Limiting

**Current Status**: Not implemented

**Future Implementation**:
- Rate limit: 100 requests per minute per user
- Burst limit: 20 requests per second
- Headers returned:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Time when limit resets

---

## Authentication

**Current Status**: User ID-based (development)

**Future Implementation**: Better Auth integration
- JWT tokens
- OAuth2 support
- Session management
- Token refresh

**Headers** (future):
```
Authorization: Bearer <jwt-token>
```

---

## Swagger UI

Interactive API documentation available at:

**URL**: http://localhost:8000/docs

Features:
- Try out endpoints directly
- View request/response schemas
- Test authentication
- Download OpenAPI spec

---

## Postman Collection

Import this collection to test all endpoints:

```json
{
  "info": {
    "name": "Todo AI Chatbot API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Chat",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/1/chat",
        "body": {
          "mode": "raw",
          "raw": "{\"message\": \"Add a task to buy groceries\"}"
        }
      }
    }
  ]
}
```

---

## WebSocket Support

**Status**: Not implemented

**Future Enhancement**: Real-time updates
- Task creation notifications
- Completion notifications
- Recurring task generation alerts

---

## Versioning

**Current Version**: 1.0

**Future Versions**:
- v2.0: Better Auth integration
- v2.1: WebSocket support
- v3.0: GraphQL API

**Version Header** (future):
```
API-Version: 1.0
```

---

## Support

For API issues or questions:
- Check Swagger UI: http://localhost:8000/docs
- Review error messages in response
- Check backend logs
- Consult implementation documentation

---

**Last Updated**: 2026-01-10
**Version**: 1.0
**Status**: Production Ready
