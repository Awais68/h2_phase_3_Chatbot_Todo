# Phase 2 Authentication System Specification

**Feature:** phase2-authentication
**Date:** 2026-01-01
**Status:** Draft

---

## Overview

This document defines the authentication system for Phase 2 of the web application. The system uses a two-part authentication strategy: Better Auth for frontend session management and JWT tokens for securing API requests to the backend.

## Authentication Architecture

### System Overview

The authentication flow follows this pattern:

```
User → Better Auth → JWT Token → API Requests → FastAPI Validation
```

### Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| Better Auth | Frontend session management | Node.js library |
| JWT Tokens | API request authentication | JSON Web Tokens (HS256) |
| Password Hashing | Secure credential storage | bcrypt (12 rounds) |
| FastAPI Middleware | Token validation | Python fastapi-security |

---

## Authentication Endpoints

### 1. Sign Up

**Endpoint:** `POST /api/auth/signup`

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response (201 Created):**

```json
{
  "user": {
    "id": "user-123-abc",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2025-12-26T10:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Account created successfully"
}
```

**Validation Rules:**

| Field | Rule |
|-------|------|
| email | Valid email format, unique, not already registered |
| password | Minimum 8 characters, contains letter and number |
| name | 1-100 characters, non-empty |

**Process Flow:**

1. Validate input format and requirements
2. Check email uniqueness in database
3. Hash password with bcrypt (12 rounds)
4. Create user record in database
5. Generate JWT token with user claims
6. Return user data and token

**Error Responses:**

| Status | Condition |
|--------|-----------|
| 400 | Invalid input format or missing fields |
| 409 | Email already registered |

---

### 2. Login

**Endpoint:** `POST /api/auth/login`

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**

```json
{
  "user": {
    "id": "user-123-abc",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login successful"
}
```

**Validation Rules:**

| Field | Rule |
|-------|------|
| email | Must exist in database |
| password | Must match hashed password |

**Process Flow:**

1. Find user by email in database
2. Verify password using bcrypt
3. Generate JWT token with user claims
4. Return user data and token

**Error Responses:**

| Status | Condition |
|--------|-----------|
| 400 | Invalid input format or missing fields |
| 401 | Invalid credentials |

---

### 3. Logout

**Endpoint:** `POST /api/auth/logout`

**Request Body:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**

```json
{
  "message": "Logged out successfully"
}
```

**Process Flow:**

1. Invalidate token (add to blacklist if implemented)
2. Clear session on client side

---

### 4. Get Current User

**Endpoint:** `GET /api/auth/me`

**Headers:**

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**

```json
{
  "user": {
    "id": "user-123-abc",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2025-12-26T10:00:00Z"
  }
}
```

**Process Flow:**

1. Extract JWT from Authorization header
2. Validate JWT signature
3. Extract user_id from token claims
4. Fetch user from database
5. Return user data

**Error Responses:**

| Status | Condition |
|--------|-----------|
| 401 | Invalid or expired token |
| 500 | Server error |

---

## JWT Token Structure

### Token Payload

```json
{
  "sub": "user-123-abc",
  "email": "user@example.com",
  "name": "John Doe",
  "iat": 1703592000,
  "exp": 1704196800
}
```

### Token Claims

| Claim | Type | Description |
|-------|------|-------------|
| sub | string | Subject (user_id) |
| email | string | User email address |
| name | string | User full name |
| iat | integer | Issued at (Unix timestamp) |
| exp | integer | Expires at (Unix timestamp) |

### Token Configuration

| Setting | Value |
|---------|-------|
| Expiry | 7 days (604800 seconds) |
| Algorithm | HS256 |
| Secret | Shared between Better Auth and FastAPI |

---

## Password Security

### Hashing Configuration

| Setting | Value |
|---------|-------|
| Library | bcrypt (passlib wrapper) |
| Rounds | 12 |

### Password Requirements

| Requirement | Details |
|-------------|---------|
| Minimum length | 8 characters |
| Character types | Letter + number required |
| Storage | bcrypt hash (never plain text) |
| API responses | Password never returned |

---

## Frontend Integration

### Auth Context Features

The authentication context provides:

| Feature | Description |
|---------|-------------|
| user | Current logged-in user (null if not authenticated) |
| token | JWT token for API requests |
| login | Async function to authenticate user |
| signup | Async function to create new account |
| logout | Function to clear session |
| isLoading | Loading state during initialization |

### Protected Routes

Routes can be protected by wrapping components with a protected route component that:

- Redirects unauthenticated users to login page
- Shows loading state while checking authentication
- Prevents access to protected content without valid session

### API Client Integration

The API client automatically includes JWT tokens in requests:

- Adds `Authorization: Bearer {token}` header
- Handles 401 responses by redirecting to login
- Manages token refresh on expiration

---

## Security Measures

### Password Security

- Minimum 8 characters with letter and number
- bcrypt hashing with 12 rounds
- Never store plain text passwords
- Never return passwords in API responses

### Token Security

- HTTPS required in production
- Optional HttpOnly cookies for enhanced security
- 7-day expiry with automatic expiration
- Signed with strong shared secret
- Validated on every API request

### Session Security

- User isolation enforced on all endpoints
- No shared sessions between users
- Logout invalidates token
- XSS protection via React escaping

### API Security

- CORS properly configured
- Rate limiting available (future enhancement)
- Input validation on all endpoints
- SQL injection prevention via ORM

---

## Error Handling

### HTTP Status Codes

| Status | Meaning | Usage |
|--------|---------|-------|
| 400 | Bad Request | Invalid input, missing fields |
| 401 | Unauthorized | Invalid credentials, expired token |
| 403 | Forbidden | User mismatch on protected resource |
| 409 | Conflict | Email already exists (signup) |
| 500 | Server Error | Internal server error |

### User-Friendly Messages

| Scenario | Message |
|----------|---------|
| Invalid credentials | "Invalid email or password" |
| Email taken | "Email already registered" |
| Token expired | "Session expired, please login again" |
| Weak password | "Password must be at least 8 characters" |

---

## Environment Variables

### Frontend Configuration

| Variable | Description |
|----------|-------------|
| BETTER_AUTH_SECRET | Secret key (minimum 32 characters) |
| BETTER_AUTH_URL | Frontend URL |
| NEXT_PUBLIC_API_URL | Backend API URL |

### Backend Configuration

| Variable | Description |
|----------|-------------|
| JWT_SECRET_KEY | Same secret as Better Auth |
| JWT_ALGORITHM | Token signing algorithm |
| JWT_EXPIRE_MINUTES | Token expiry time |

### Secret Generation

```bash
openssl rand -hex 32
```

---

## Testing Requirements

### Unit Tests

| Test | Description |
|------|-------------|
| Password hashing | Verify hash and verify functions work correctly |
| JWT validation | Token generation and validation logic |
| Input validation | All validation rules enforced correctly |

### Integration Tests

| Test | Description |
|------|-------------|
| Signup flow | Complete signup process end-to-end |
| Login flow | Complete login process end-to-end |
| Protected routes | Access control enforced correctly |
| Token expiry | Expired tokens properly rejected |

### End-to-End Tests

| Test | Description |
|------|-------------|
| User signup | User can create new account |
| User login | User can authenticate successfully |
| Protected pages | Authenticated user can access protected content |
| User logout | User can log out successfully |
| Invalid credentials | Invalid login attempts are rejected |

---

## Authentication Flow Diagram

```
                                    ┌─────────────────────┐
                                    │      User           │
                                    └──────────┬──────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │   Better Auth       │
                                    │   (Frontend)        │
                                    └──────────┬──────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │  Login/Signup API   │
                                    │  /api/auth/login    │
                                    │  /api/auth/signup   │
                                    └──────────┬──────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │  JWT Token          │
                                    │  (7 day expiry)     │
                                    └──────────┬──────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │  API Requests       │
                                    │  Authorization:     │
                                    │  Bearer {token}     │
                                    └──────────┬──────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │  FastAPI Middleware │
                                    │  JWT Validation     │
                                    └──────────┬──────────┘
                                               │
                                    ┌──────────▼──────────┐
                                    │  Protected Routes   │
                                    │  /api/{user_id}/... │
                                    └─────────────────────┘
```

---

## Considerations

### Better Auth Integration

- Better Auth manages frontend session state
- JWT tokens bridge frontend and backend authentication
- Shared secret ensures compatibility between systems

### Performance

- Token validation is stateless (no database lookup required)
- Password hashing uses 12 rounds (secure but performant)
- JWT claims cached after initial validation

### Future Enhancements

- Token refresh mechanism
- Multi-factor authentication
- Social login providers
- Rate limiting for auth endpoints
- Token blacklisting for immediate logout
