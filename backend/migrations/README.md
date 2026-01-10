# Database Migrations

This directory contains SQL migrations for the Todo Evolution application.

## Migration Files

| File | Description |
|------|-------------|
| `001_initial_schema.sql` | Initial database schema (users, tasks, sync, push) |

## Running Migrations

### Option 1: Via psql (Command Line)

```bash
# Connect to your Neon database
psql "postgresql://username:password@ep-xxx.region.aws.neon.tech/neon?sslmode=require"

# Run the migration
\i migrations/001_initial_schema.sql
```

### Option 2: Via Neon Console

1. Open https://console.neon.tech
2. Navigate to your project → SQL Editor
3. Copy contents of `001_initial_schema.sql`
4. Execute the SQL

### Option 3: Via Alembic (Python)

If using Alembic for migrations:

```bash
cd backend
alembic upgrade head
```

## Rollback

To rollback (drop all tables):

```sql
DROP TABLE IF EXISTS push_subscriptions CASCADE;
DROP TABLE IF EXISTS sync_operations CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;
DROP EXTENSION IF EXISTS "uuid-ossp" CASCADE;
```

## Schema Overview

```
users (id, email, username, hashed_password, is_active, is_superuser, created_at, updated_at)
   ↑
   │ foreign key (ON DELETE CASCADE)
   ↓
tasks (id, user_id, title, description, completed, created_at, updated_at, client_id, version)
   ↑
   │ foreign key (ON DELETE CASCADE)
   ↓
sync_operations (id, user_id, operation_type, entity_type, entity_id, client_id, payload, synced_at, synced)

push_subscriptions (id, user_id, endpoint, p256dh, auth, created_at)
```

## Connection String Format

```
postgresql://username:password@host/database?sslmode=require
```

Example:
```
postgresql://awais:secret123@ep-old-bread-12345.us-east-1.aws.neon.tech/neon?sslmode=require
```

## Environment Variables

Set `DATABASE_URL` in your `.env` file:

```bash
DATABASE_URL="postgresql://username:password@ep-xxx.region.aws.neon.tech/neon?sslmode=require"
```
