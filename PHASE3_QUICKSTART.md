# Quick Start Guide: Phase III Todo AI Chatbot

## Prerequisites

- Python 3.13+ installed
- Node.js 18+ installed
- Neon PostgreSQL database (already connected)
- OpenAI API key

## Backend Setup (5 minutes)

### 1. Install Dependencies

```bash
cd backend
source .venv/bin/activate  # Activate existing virtual environment

# Install new dependencies
pip install openai
```

### 2. Configure Environment

Add to `backend/.env`:
```bash
# OpenAI API Key (required for AI chatbot)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Database URL (already configured)
DATABASE_URL=postgresql://neondb_owner:npg_uH9gTMsmGw6p@ep-royal-dust-ah4nrunw-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### 3. Run Database Migrations

```bash
# Create new tables (conversations, messages, recurring_tasks)
python -c "
from src.db.session import engine
from sqlmodel import SQLModel
from src.models import Conversation, Message, RecurringTask

SQLModel.metadata.create_all(engine)
print('✓ Database tables created successfully')
"
```

### 4. Start Backend Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## Frontend Setup (3 minutes)

### 1. Install Dependencies

```bash
cd frontend

# Install Recharts for analytics (if not already installed)
npm install recharts
```

### 2. Configure Environment

Create/update `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Frontend Server

```bash
cd frontend
npm run dev
```

Frontend will be available at:
- App: http://localhost:3000
- Chatbot: http://localhost:3000/chatbot

## Testing the Implementation

### 1. Test Chat Interface

1. Open http://localhost:3000/chatbot
2. Click on the **💬 Chat** tab
3. Try these commands:
   - "Add a task to buy groceries"
   - "Show me all my tasks"
   - "Mark task 1 as complete"
   - "Create a daily recurring task for standup meeting"

### 2. Test Voice Commands

1. Click the 🎤 microphone button
2. Say: "Add a task to call mom"
3. The assistant will respond with voice output

### 3. Test Analytics Dashboard

1. Click on the **📊 Analytics** tab
2. View:
   - Task statistics (total, completed, pending, completion rate)
   - Pie chart (task distribution)
   - Line chart (tasks over time)
   - Bar chart (productivity by hour)

### 4. Test Recurring Tasks

1. Click on the **🔄 Recurring** tab
2. Click "+ New Recurring Task"
3. Create a task:
   - Title: "Daily standup"
   - Frequency: Daily
   - Click "Create Recurring Task"
4. Test pause/resume/delete functionality

## API Testing with Swagger UI

Visit http://localhost:8000/docs to test all endpoints:

### Chat Endpoint
```
POST /api/1/chat
Body: {
  "message": "Add a task to test the API"
}
```

### Analytics Endpoints
```
GET /api/1/analytics/overview
GET /api/1/analytics/timeline?days=30
GET /api/1/analytics/completion
GET /api/1/analytics/productivity
```

### Recurring Tasks Endpoints
```
POST /api/1/recurring
GET /api/1/recurring
PATCH /api/1/recurring/1/pause
PATCH /api/1/recurring/1/resume
DELETE /api/1/recurring/1
```

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'openai'`
```bash
# Solution: Install OpenAI package
pip install openai
```

**Issue**: `Database tables not found`
```bash
# Solution: Run migrations
python -c "from src.db.session import engine; from sqlmodel import SQLModel; from src.models import Conversation, Message, RecurringTask; SQLModel.metadata.create_all(engine)"
```

**Issue**: `OpenAI API key not found`
```bash
# Solution: Add OPENAI_API_KEY to backend/.env
echo "OPENAI_API_KEY=sk-your-key-here" >> backend/.env
```

### Frontend Issues

**Issue**: `Module not found: recharts`
```bash
# Solution: Install Recharts
cd frontend && npm install recharts
```

**Issue**: `Voice input not working`
- Check browser compatibility (Chrome, Edge, Safari support Web Speech API)
- Ensure microphone permissions are granted
- Try HTTPS (some browsers require secure context)

**Issue**: `API connection failed`
```bash
# Solution: Check NEXT_PUBLIC_API_URL in frontend/.env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
```

## Features Overview

### 1. AI Chatbot (Chat Tab)
- Natural language task management
- Voice input with Web Speech API
- Voice output (text-to-speech)
- Conversation history persistence
- Real-time message updates

### 2. Analytics Dashboard (Analytics Tab)
- Task statistics cards
- Pie chart for task distribution
- Line chart for tasks over time (30 days)
- Bar chart for productivity by hour
- Refresh button for live updates

### 3. Recurring Tasks (Recurring Tab)
- Create recurring tasks (daily/weekly/monthly)
- Pause/resume functionality
- Delete with confirmation
- Status badges (active/paused)
- Last generated timestamp

### 4. MCP Tools (14 tools)
- **Basic**: add_task, list_tasks, complete_task, delete_task, update_task
- **Recurring**: create_recurring_task, list_recurring_tasks, pause/resume/delete
- **Analytics**: get_task_statistics, get_tasks_over_time, get_completion_analytics, get_productivity_hours

## Next Steps

1. ✅ Backend running on port 8000
2. ✅ Frontend running on port 3000
3. ✅ Database tables created
4. ✅ OpenAI API key configured
5. → Test all features
6. → Deploy to production (optional)

## Production Deployment

### Backend (Railway/Render)
```bash
# Set environment variables
DATABASE_URL=<neon-postgresql-url>
OPENAI_API_KEY=<your-openai-key>
```

### Frontend (Vercel)
```bash
# Set environment variables
NEXT_PUBLIC_API_URL=<backend-url>
```

## Support

For issues or questions:
1. Check Swagger UI: http://localhost:8000/docs
2. Review implementation summary: PHASE3_IMPLEMENTATION_SUMMARY.md
3. Check browser console for frontend errors
4. Check backend logs for API errors

---

**Estimated Setup Time**: 8 minutes
**Status**: ✅ Ready to use
**Last Updated**: 2026-01-10
