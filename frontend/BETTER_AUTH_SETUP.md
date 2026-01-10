# Better-Auth Setup Guide

## 🎯 Overview

Your project now uses **better-auth** for authentication with email/password login and Prisma as the database adapter.

## 📦 What Was Set Up

### 1. **Dependencies Installed**

- `better-auth@^1.4.10` - Modern authentication library
- `prisma@^5.22.0` - Database ORM
- `@prisma/client@^5.22.0` - Prisma client library

### 2. **Files Created/Modified**

#### Database Configuration

- **`prisma/schema.prisma`** - Database schema with User, Account, Session, and VerificationToken models
- **`.env.local`** - Environment variables (DATABASE_URL)

#### Authentication Configuration

- **`src/lib/auth.ts`** - Server-side better-auth configuration
- **`src/lib/auth-client.ts`** - Client-side auth hooks (signIn, signUp, signOut, useSession)
- **`src/lib/prisma.ts`** - Prisma client singleton
- **`src/app/api/auth/[...auth]/route.ts`** - Auth API route handlers

#### Updated Components

- **`src/components/AuthPage.tsx`** - Login/Signup forms using better-auth
  - Email-based authentication (no username required for signin)
  - Password strength indicator
  - Form validation

### 3. **Database Schema**

```prisma
model User {
  id            String   @id @default(cuid())
  email         String   @unique
  emailVerified Boolean  @default(false)
  name          String?
  username      String?  @unique
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt

  accounts Account[]
  sessions Session[]
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User @relation(fields: [userId], references: [id], onDelete: Cascade)
}
```

## 🚀 Setup Instructions

### Option 1: Automated Setup (Recommended)

```bash
cd frontend
./setup-auth.sh
```

### Option 2: Manual Setup

```bash
cd frontend

# Install dependencies (if not already done)
npm install prisma@5.22.0 @prisma/client@5.22.0 better-auth

# Generate Prisma Client
npx prisma generate

# Create database and tables
npx prisma db push
```

## 🔐 How Authentication Works

### Sign Up Flow

1. User enters **email**, **username** (optional), and **password**
2. Frontend calls `signUp.email({ email, password, name: username })`
3. better-auth creates user and session
4. User is redirected to `/dashboard`

### Sign In Flow

1. User enters **email** and **password** (no username needed)
2. Frontend calls `signIn.email({ email, password })`
3. better-auth validates credentials and creates session
4. User is redirected to `/dashboard`

### Using Auth in Components

```typescript
import { useSession, signOut } from "@/lib/auth-client";

function MyComponent() {
  const { data: session, isPending } = useSession();

  if (isPending) return <div>Loading...</div>;

  if (!session) {
    return <div>Not authenticated</div>;
  }

  return (
    <div>
      <p>Welcome {session.user.email}</p>
      <button onClick={() => signOut()}>Logout</button>
    </div>
  );
}
```

## 🔧 Configuration Options

### Server Config (`src/lib/auth.ts`)

```typescript
export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "sqlite",
  }),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true for email verification
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
});
```

### Environment Variables

Add to `.env.local`:

```env
NEXT_PUBLIC_APP_URL=http://localhost:3000
DATABASE_URL="file:./dev.db"

# Optional: Email service for verification
# EMAIL_FROM=noreply@example.com
# EMAIL_SERVER=smtp://user:pass@smtp.example.com:587
```

## 🗄️ Database Location

- **Development**: `frontend/prisma/dev.db` (SQLite)
- **Production**: Update `DATABASE_URL` to your production database (PostgreSQL, MySQL, etc.)

## 🔄 Migration to Production

To switch from SQLite to PostgreSQL:

1. Update `.env.local`:

```env
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

2. Update `prisma/schema.prisma`:

```prisma
datasource db {
  provider = "postgresql"  // changed from "sqlite"
  url      = env("DATABASE_URL")
}
```

3. Run migration:

```bash
npx prisma migrate dev --name init
```

## 📚 API Endpoints

better-auth automatically creates these endpoints:

- `POST /api/auth/sign-up/email` - Email/password signup
- `POST /api/auth/sign-in/email` - Email/password signin
- `POST /api/auth/sign-out` - Sign out
- `GET /api/auth/session` - Get current session

## 🎨 Customization

### Add Email Verification

Update `src/lib/auth.ts`:

```typescript
export const auth = betterAuth({
  // ... other config
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true, // Enable verification
  },
  emailVerification: {
    sendVerificationEmail: async ({ email, token, url }) => {
      // Send email with verification link
      await sendEmail({ to: email, body: url });
    },
  },
});
```

### Add Social Providers (Google, GitHub)

```typescript
import { google, github } from "better-auth/providers";

export const auth = betterAuth({
  // ... other config
  providers: [
    google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    github({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),
  ],
});
```

## 🐛 Troubleshooting

### Error: "Module not found: Can't resolve '@prisma/client'"

```bash
cd frontend
npx prisma generate
```

### Error: "Database not found"

```bash
cd frontend
npx prisma db push
```

### Session not persisting

Check that cookies are enabled in your browser and NEXT_PUBLIC_APP_URL matches your current URL.

## 📖 Resources

- [better-auth Documentation](https://better-auth.com)
- [Prisma Documentation](https://www.prisma.io/docs)
- [Next.js Authentication](https://nextjs.org/docs/authentication)

## ✅ Testing

Run the frontend and test authentication:

```bash
cd frontend
npm run dev
```

Navigate to `http://localhost:3000/auth` and:

1. Sign up with email/password
2. Verify redirect to dashboard
3. Sign out
4. Sign in with same credentials
