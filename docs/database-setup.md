# Neon Database Setup Guide

This document provides step-by-step instructions for setting up the Neon PostgreSQL database for the Todo Evolution application.

## Prerequisites

- A web browser (for Neon console)
- A GitHub account (for connecting to Render)
- Command line access (psql or similar)

## Step 1: Create Neon Account

1. Navigate to https://console.neon.tech
2. Click **Sign Up** or **Sign In**
3. Choose your preferred sign-in method:
   - GitHub (recommended for easy Render integration)
   - Google
   - Email

## Step 2: Create Neon Project

1. Click **New Project** button
2. Configure the project:
   ```
   Name: Todo Evolution (or your preference)
   Region: Choose closest to your users
         - us-east-1 (Virginia) - Recommended for US users
         - eu-west-1 (Ireland) - Recommended for EU users
         - ap-southeast-1 (Singapore) - Recommended for Asia users
   PostgreSQL Version: 15 (default)
   ```
3. Click **Create Project**
4. Wait for project initialization (~30 seconds)

## Step 3: Get Connection String

1. In your Neon dashboard, click **Connection Details**
2. You'll see a connection string like:
   ```
   postgres://username:password@ep-xxx.us-east-1.aws.neon.tech/neon?sslmode=require
   ```
3. **Copy this connection string** - you'll need it for:
   - Backend `.env` file
   - Render dashboard (for environment variable)

### Connection String Format

```
postgresql://[username]:[password]@[host]/[database]?sslmode=require
```

Example:
```
postgres://awais:pq4I7xyz123@ep-ancient-12345.us-east-1.aws.neon.tech/neon?sslmode=require
```

## Step 4: Configure Environment Variables

### Local Development

1. Open `backend/.env` (copy from `.env.example` if needed)
2. Replace the `DATABASE_URL` placeholder:
   ```bash
   # Before (placeholder)
   DATABASE_URL="postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neon?sslmode=require"

   # After (your actual connection string)
   DATABASE_URL="postgres://awais:pq4I7xyz123@ep-ancient-12345.us-east-1.aws.neon.tech/neon?sslmode=require"
   ```

3. Verify the connection works:
   ```bash
   cd backend
   python -c "from src.db.database import engine; print('Connected!')"
   ```

### Render Deployment

1. Go to Render Dashboard → Your Backend Service → **Environment**
2. Click **Add Environment Variable**
3. Add:
   ```
   Key: DATABASE_URL
   Value: (paste your full connection string)
   ```
4. Click **Save Changes**

## Step 5: Run Database Migrations

### Option A: Via Neon SQL Editor (Recommended)

1. In Neon Dashboard → **SQL Editor**
2. Click **New Query**
3. Copy contents of `backend/migrations/001_initial_schema.sql`
4. Click **Run** to execute

### Option B: Via psql Command Line

```bash
# Install psql if needed (macOS)
brew install postgresql

# Connect and run migration
psql "postgres://username:password@ep-xxx.us-east-1.aws.neon.tech/neon?sslmode=require" \
  -f backend/migrations/001_initial_schema.sql
```

### Option C: Via Python (Alembic)

If using Alembic:

```bash
cd backend
alembic upgrade head
```

## Step 6: Verify Setup

1. **Check Tables Created**:
   ```sql
   SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'public';
   ```
   Expected tables: `users`, `tasks`, `sync_operations`, `push_subscriptions`

2. **Test Connection**:
   ```bash
   cd backend
   python -c "
   from sqlalchemy import create_engine, text
   engine = create_engine(os.getenv('DATABASE_URL'))
   with engine.connect() as conn:
       result = conn.execute(text('SELECT 1'))
       print('Database connection successful!')
   "

3. **Run Backend Health Check** (after Phase 3 deployment):
   ```bash
   curl https://your-backend.onrender.com/health
   ```
   Expected response: `{"status":"healthy",...}`

## Environment-Specific Setup

### Development (Local)

```bash
# Create .env from template
cd backend
cp .env.example .env

# Edit .env with your Neon connection string
nano .env

# Test connection
python -c "from src.db.database import engine; print('OK')"
```

### Production (Render)

1. Render Dashboard → Your Service → **Environment**
2. Add `DATABASE_URL` with your Neon connection string
3. Add `DATABASE_POOL_SIZE` = `5` (optional, for connection pooling)
4. Redeploy the service

## Troubleshooting

### Connection Refused

```
could not connect to server: Connection refused
```

**Solutions**:
- Verify your IP is allowed in Neon → Settings → IP Allowlist
- Check that your connection string is correct
- Ensure the Neon project is not suspended (free tier suspends after 7 days of inactivity)

### SSL Certificate Error

```
ssl_requirement) SSL connection required
```

**Solution**: Ensure `?sslmode=require` is at the end of your connection string.

### Password Authentication Failed

```
FATAL: password authentication failed for user "username"
```

**Solutions**:
- Double-check your connection string for typos
- Regenerate credentials in Neon → Settings → Password

### Database Suspended (Free Tier)

Neon's free tier suspends databases after 7 days of inactivity.

**Solutions**:
- Wake the database in Neon Dashboard
- Set up an auto-wake cron job
- Upgrade to paid tier for always-on

## Free Tier Limitations

| Resource | Limit |
|----------|-------|
| Storage | 10 GB |
| Active branches | 1 (main) |
| Compute time | 300 hours/month |
| History retention | 7 days |

## Security Best Practices

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use different databases** for development and production
3. **Rotate credentials** if accidentally exposed:
   - Neon → Settings → Reset Password
4. **Enable SSL** - Always use `sslmode=require`
5. **Limit IP access** (optional):
   - Neon → Settings → IP Allowlist

## Next Steps

After database setup is complete:

1. Proceed to **Phase 3: Backend Deployment (Render)**
2. The Render service will automatically connect to Neon using the `DATABASE_URL` environment variable
3. Run initial migrations during deployment

## Support

- **Neon Documentation**: https://neon.tech/docs
- **Neon Support**: support@neon.tech
- **Community Discord**: https://discord.gg/neon
