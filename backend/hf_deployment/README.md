---
title: Todo Chatbot API
emoji: ✅
colorFrom: blue
colorTo: purple
sdk: docker
app_file: todo_chatbot/main.py
pinned: false
license: mit
---

# 🚀 Todo Evolution - AI-Powered Task Management API

A powerful FastAPI-based backend for an intelligent todo application with AI chat integration, recurring tasks, shopping lists, and comprehensive analytics.

## ✨ Features

- 🤖 **AI Chat Assistant** - Natural language task management using OpenAI
- 📋 **Task Management** - Full CRUD operations with categories, tags, and priorities
- 🔄 **Recurring Tasks** - Automated task generation with flexible scheduling
- 🛒 **Shopping Lists** - Integrated shopping list management within tasks
- 📊 **Analytics** - Comprehensive productivity insights and statistics
- 🔐 **Better Auth** - Secure authentication with PostgreSQL backend
- 🗃️ **Neon DB** - Serverless PostgreSQL database integration
- 📱 **Real-time Sync** - Multi-device task synchronization

## 🛠️ Tech Stack

- **Framework:** FastAPI 0.115.6
- **Database:** PostgreSQL (Neon)
- **ORM:** SQLModel
- **AI:** OpenAI GPT-4
- **Auth:** Better Auth compatible
- **Deployment:** Hugging Face Spaces (Docker)

## 🔧 Environment Variables

Configure these in your Hugging Face Space settings:

### Required Secrets
- `DATABASE_URL` - Your Neon PostgreSQL connection string
- `SECRET_KEY` - JWT secret key (generate with: `openssl rand -hex 32`)
- `OPENAI_API_KEY` - Your OpenAI API key

### Optional Variables
- `APP_NAME` - Application name (default: "Todo Evolution API")
- `APP_VERSION` - Version number (default: "2.0.0")
- `DEBUG` - Debug mode (default: "False")
- `LOG_LEVEL` - Logging level (default: "INFO")

## 📚 API Documentation

Once deployed, access the interactive API docs at:
- Swagger UI: `https://your-space.hf.space/docs`
- ReDoc: `https://your-space.hf.space/redoc`

## 🚀 Quick Start

### API Endpoints

#### Tasks
- `GET /tasks` - List all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get task by ID
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

#### Chat
- `POST /api/{user_id}/chat` - Chat with AI assistant

#### Analytics
- `GET /api/{user_id}/analytics/overview` - Get analytics overview
- `GET /api/{user_id}/analytics/timeline` - Get completion timeline
- `GET /api/{user_id}/analytics/productivity` - Get productivity metrics

#### Recurring Tasks
- `GET /api/{user_id}/recurring` - List recurring tasks
- `POST /api/{user_id}/recurring` - Create recurring task
- `POST /api/{user_id}/recurring/{id}/pause` - Pause recurring task
- `POST /api/{user_id}/recurring/{id}/resume` - Resume recurring task

## 🔗 Frontend Integration

This API is designed to work with the Todo Evolution frontend:
- Frontend Repo: [frontend_phase3_chatbot_todo](https://github.com/Awais68/frontend_phase3_chatbot_todo)
- Configure `NEXT_PUBLIC_API_URL` to point to this space

## 📝 Recent Updates

- ✅ Fixed 307 redirect issues with trailing slashes
- ✅ Improved OpenAI error handling
- ✅ Enhanced rate limit error management
- ✅ Better exception handling for API errors

## 🤝 Contributing

This project is part of a hackathon series. Contributions and feedback are welcome!

## 📄 License

MIT License - See LICENSE file for details

## 🐛 Issues & Support

For issues or questions, please open an issue on the GitHub repository.

---

**Built with ❤️ using FastAPI, OpenAI, and Neon DB**
