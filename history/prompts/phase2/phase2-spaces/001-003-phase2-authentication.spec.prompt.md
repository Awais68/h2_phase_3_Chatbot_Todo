---
id: "001-003-phase2-authentication"
title: Phase 2 Authentication Specification
stage: spec
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase2-authentication
branch: 005-deployment-architecture
user: Awais
command: /sp.specify phase2-authentication Create Phase II authentication system specification
labels: ["authentication","jwt","better-auth","security","frontend","backend"]
links:
  spec: /media/data/hackathon series/hackathon-2/phase-ii_Web_App_Full Stack/specs/phase2-spaces/phase2-authentication.md
  ticket: null
  adr: null
  pr: null
files:
  - /media/data/hackathon series/hackathon-2/phase-ii_Web_App_Full Stack/specs/phase2-spaces/phase2-authentication.md
tests: []
---

## Prompt

phase2-authentication
Create Phase II authentication system specification

AUTHENTICATION STRATEGY: Better Auth (Frontend) + JWT (API)

OVERVIEW:

Two-part authentication system:
1. Better Auth: Manages user sessions on frontend
2. JWT Tokens: Secures API requests to backend

Flow:
User → Better Auth → JWT Token → API Requests → FastAPI Validation

BETTER AUTH SETUP (Frontend):

Installation:
```bash
npm install better-auth
```

Configuration:
```typescript
// lib/auth.ts
import { BetterAuth } from "better-auth"
import { nextAuthAdapter } from "better-auth/adapters/next"

export const auth = new BetterAuth({
  adapter: nextAuthAdapter(),
  secret: process.env.BETTER_AUTH_SECRET!,
  jwt: {
    enabled: true,
    expiresIn: "7d",
    algorithm: "HS256"
  },
  providers: {
    credentials: {
      async authorize(credentials) {
        // Call backend to verify credentials
        const response = await fetch(`${API_URL}/api/auth/login`, {
          method: "POST",
          body: JSON.stringify(credentials)
        })

        if (response.ok) {
          const user = await response.json()
          return user
        }
        return null
      }
    }
  }
})
```

AUTHENTICATION ENDPOINTS (Backend):

1. POST /api/auth/signup
Request:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

Response (201 Created):
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

Validation:
- Email: Valid format, unique, not already registered
- Password: Minimum 8 characters, contains letter + number
- Name: 1-100 characters, non-empty

Process:
1. Validate input
2. Check email uniqueness
3. Hash password with bcrypt (12 rounds)
4. Create user in database
5. Generate JWT token
6. Return user + token

2. POST /api/auth/login
Request:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

Response (200 OK):
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

Validation:
- Email: Must exist in database
- Password: Must match hashed password

Process:
1. Find user by email
2. Verify password with bcrypt
3. Generate JWT token
4. Return user + token

3. POST /api/auth/logout
Request:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Response (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

Process:
1. Invalidate token (add to blacklist if needed)
2. Clear session

4. GET /api/auth/me
Headers:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Response (200 OK):
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

Process:
1. Extract JWT from Authorization header
2. Validate JWT signature
3. Extract user_id from token
4. Fetch user from database
5. Return user data

JWT TOKEN STRUCTURE:

Payload:
```json
{
  "sub": "user-123-abc",
  "email": "user@example.com",
  "name": "John Doe",
  "iat": 1703592000,
  "exp": 1704196800
}
```

Expiry: 7 days (604800 seconds)
Algorithm: HS256
Secret: Shared between Better Auth and FastAPI

JWT MIDDLEWARE (Backend):
```python
# backend/middleware/auth.py
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    Validate JWT token and return user_id
    Raises 401 if token invalid
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Check expiry
        exp = payload.get("exp")
        if datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token expired")

        return user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

Usage in Routes:
```python
from middleware.auth import get_current_user

@app.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user)
):
    # Verify user_id in URL matches authenticated user
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Proceed with query
    tasks = await get_user_tasks(user_id)
    return tasks
```

PASSWORD HASHING:

Library: bcrypt (passlib wrapper)
Rounds: 12 (secure, performant)

Hash Password:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

Verify Password:
```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

FRONTEND INTEGRATION:

Auth Context:
```typescript
// contexts/AuthContext.tsx
'use client'

import { createContext, useContext, useState, useEffect } from 'react'

interface User {
  id: string
  email: string
  name: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string, name: string) => Promise<void>
  logout: () => void
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Load token from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      setToken(storedToken)
      // Fetch user data
      fetchUser(storedToken)
    }
    setIsLoading(false)
  }, [])

  const login = async (email: string, password: string) => {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })

    if (!response.ok) throw new Error('Login failed')

    const data = await response.json()
    setToken(data.token)
    setUser(data.user)
    localStorage.setItem('token', data.token)
  }

  const signup = async (email: string, password: string, name: string) => {
    const response = await fetch(`${API_URL}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name })
    })

    if (!response.ok) throw new Error('Signup failed')

    const data = await response.json()
    setToken(data.token)
    setUser(data.user)
    localStorage.setItem('token', data.token)
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
  }

  return (
    <AuthContext.Provider value={{ user, token, login, signup, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
```

Protected Routes:
```typescript
// components/ProtectedRoute.tsx
'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/login')
    }
  }, [user, isLoading, router])

  if (isLoading) return <div>Loading...</div>
  if (!user) return null

  return <>{children}</>
}
```

API Client with JWT:
```typescript
// lib/api-client.ts
export class APIClient {
  private baseURL: string
  private getToken: () => string | null

  constructor(baseURL: string, getToken: () => string | null) {
    this.baseURL = baseURL
    this.getToken = getToken
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const token = this.getToken()

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options?.headers
      }
    })

    if (response.status === 401) {
      // Token expired, logout
      throw new Error('Unauthorized')
    }

    if (!response.ok) {
      throw new Error('Request failed')
    }

    return response.json()
  }

  async getTasks(userId: string) {
    return this.request(`/api/${userId}/tasks`)
  }

  async createTask(userId: string, data: any) {
    return this.request(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }
}
```

SECURITY MEASURES:

1. Password Security:
   - Minimum 8 characters
   - Bcrypt hashing (12 rounds)
   - Never store plain passwords
   - Never return passwords in API

2. Token Security:
   - HTTPS only in production
   - HttpOnly cookies (optional enhancement)
   - 7-day expiry
   - Signed with strong secret
   - Validated on every request

3. Session Security:
   - User isolation enforced
   - No shared sessions
   - Logout invalidates token
   - XSS protection (React escaping)

4. API Security:
   - CORS configured properly
   - Rate limiting (future)
   - Input validation
   - SQL injection prevention

ERROR HANDLING:

Authentication Errors:
- 400: Invalid input (missing fields, bad format)
- 401: Invalid credentials, expired token
- 403: Forbidden (user mismatch)
- 409: Email already exists (signup)
- 500: Server error

User-Friendly Messages:
- "Invalid email or password" (don't reveal which)
- "Email already registered"
- "Session expired, please login again"
- "Password must be at least 8 characters"

ENVIRONMENT VARIABLES:

Required:
Frontend
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
Backend
JWT_SECRET_KEY=same-as-better-auth-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080
Secret Generation:
```bash
# Generate secure secret
openssl rand -hex 32
```

TESTING REQUIREMENTS:

Unit Tests:
- Password hashing/verification
- JWT token generation/validation
- Input validation

Integration Tests:
- Signup flow end-to-end
- Login flow end-to-end
- Protected route access
- Token expiry handling

E2E Tests:
- User can signup
- User can login
- User can access protected pages
- User can logout
- Invalid credentials rejected

Include in authentication.md:
- Complete auth flow diagram
- All endpoints with examples
- JWT structure and validation
- Frontend integration code
- Security measures
- Error handling
- Testing requirements

## Response snapshot

Created Phase 2 authentication system specification with the following sections:

1. **Authentication Architecture**: Two-part system (Better Auth + JWT) with flow diagram
2. **Authentication Endpoints**: Detailed documentation for signup, login, logout, and get current user
3. **JWT Token Structure**: Token payload, claims, and configuration (7-day expiry, HS256)
4. **Password Security**: Hashing configuration (bcrypt, 12 rounds) and requirements
5. **Frontend Integration**: Auth context features, protected routes, and API client integration
6. **Security Measures**: Password, token, session, and API security guidelines
7. **Error Handling**: HTTP status codes and user-friendly error messages
8. **Environment Variables**: Frontend and backend configuration requirements
9. **Testing Requirements**: Unit, integration, and E2E test specifications
10. **Authentication Flow Diagram**: ASCII diagram showing the complete auth flow

## Outcome

- ✅ Impact: Created comprehensive authentication specification covering Better Auth frontend integration, JWT-based API security, password hashing, protected routes, error handling, and testing requirements
- 🧪 Tests: None (specification only)
- 📁 Files: 1 file created (specs/phase2-spaces/phase2-authentication.md)
- 🔁 Next prompts: Create implementation plan (plan.md), Generate tasks (tasks.md)
- 🧠 Reflection: User specified a complete two-part auth strategy with Better Auth for frontend and JWT for backend API security

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
