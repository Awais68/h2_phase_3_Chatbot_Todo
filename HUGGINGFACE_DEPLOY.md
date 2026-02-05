# HuggingFace Backend Deployment Guide

## 🚀 Live URLs

| Service | URL |
|---------|-----|
| **Backend API** | https://awais68-todo-chatbot.hf.space |
| **API Docs** | https://awais68-todo-chatbot.hf.space/docs |
| **Frontend** | https://h2-phase-3-chatbot-todo-ixau.vercel.app |

---

## 📁 HuggingFace Space Location

```
~/hf_space_check/
```

---

## 🔄 Backend Update Karna

### Step 1: Changes karo backend files mein
```bash
# Edit files in:
backend/todo_chatbot/app.py
backend/todo_chatbot/src/
```

### Step 2: HF folder mein copy karo
```bash
cp -r backend/todo_chatbot/app.py ~/hf_space_check/
cp -r backend/todo_chatbot/src ~/hf_space_check/
```

### Step 3: Push karo
```bash
cd ~/hf_space_check
git add -A && git commit -m "Update backend" && git push
```

**Auto rebuild hoga - 2-3 min wait karo. Done! ✅**

---

## 🔐 Environment Variables (HuggingFace Secrets)

Go to: https://huggingface.co/spaces/Awais68/todo_chatbot/settings

Add these secrets:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `postgresql://neondb_owner:npg_uH9gTMsmGw6p@ep-royal-dust-ah4nrunw-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require` |
| `SECRET_KEY` | `d49562d5264090f969d41904fa556f695d621c4d08f36575c538ee9f6b5c70b1` |
| `OPENAI_API_KEY` | `sk-proj-...` (your key) |
| `CORS_ORIGINS` | `https://h2-phase-3-chatbot-todo-ixau.vercel.app,http://localhost:3000` |

---

## 📦 Files in HuggingFace Space

```
~/hf_space_check/
├── app.py              # FastAPI entry point
├── Dockerfile          # Docker build config
├── README.md           # HF Space metadata
├── requirements.txt    # Python dependencies
└── src/                # Backend source code
    ├── api/            # API routes
    ├── core/           # Config & security
    ├── db/             # Database session
    ├── mcp/            # MCP server
    ├── middleware/     # CORS, auth, errors
    ├── models/         # SQLAlchemy models
    └── services/       # Business logic
```

---

## 🔧 Vercel Frontend Config

Add environment variable in Vercel dashboard:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://awais68-todo-chatbot.hf.space` |

---

## 📋 Quick Commands

```bash
# Clone HF space (if needed)
git clone https://huggingface.co/spaces/Awais68/todo_chatbot ~/hf_space_check

# Sync all backend files
cp -r backend/todo_chatbot/app.py ~/hf_space_check/
cp -r backend/todo_chatbot/src ~/hf_space_check/
cp backend/todo_chatbot/requirements_hf.txt ~/hf_space_check/requirements.txt

# Deploy
cd ~/hf_space_check && git add -A && git commit -m "Update" && git push
```

---

## ⚠️ Troubleshooting

### Build Failed?
- Check `requirements.txt` formatting (each package on new line)
- Check HuggingFace build logs

### API Not Working?
- Verify secrets are set in HuggingFace Settings
- Check if Space is running (green status)

### CORS Error?
- Add frontend URL to `CORS_ORIGINS` secret
- Restart Space after adding secrets
