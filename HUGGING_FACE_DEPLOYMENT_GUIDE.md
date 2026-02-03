# Quick Start: Deploy Todo AI Chatbot

## Using Your Hugging Face Token

Store your Hugging Face token in Space secrets (do not commit tokens). Here's how to deploy your application:

## Step 1: Prepare the Backend for Hugging Face Spaces

```bash
# Navigate to the project directory
cd /path/to/your/project

# Prepare backend files for Hugging Face deployment
./deploy.sh backend
```

This will create the necessary files in `backend/hf_deployment/`:
- `app.py` - The main application
- `requirements_hf.txt` - Dependencies
- `space.yaml` - Space configuration
- `src/` - Source code

## Step 2: Create Your Hugging Face Space

1. Go to [https://huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Select:
   - **SDK**: Gradio (our FastAPI app will run with Gradio)
   - **Hardware**: CPU Basic (or higher based on needs)
   - **Storage**: Large
   - **Visibility**: Public or Private

## Step 3: Configure Space Secrets

In your Space settings, add these secrets:
- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `SECRET_KEY`: Your JWT secret (generate with `openssl rand -hex 32`)
- `OPENAI_API_KEY`: Your OpenAI API key

Note: Your Hugging Face token should be stored securely in Space secrets if needed - never commit tokens to the repository.

## Step 4: Upload Backend Files

Upload the files from `backend/hf_deployment/` to your Hugging Face Space.

## Step 5: Deploy Frontend to Vercel

```bash
# Prepare frontend for Vercel deployment
./deploy.sh frontend
```

Then:
1. Push your frontend code to a Git repository
2. Go to [https://vercel.com](https://vercel.com) and import your project
3. Add the environment variables listed in `frontend/vercel_deployment_notes.txt`

## Step 6: Connect Frontend to Backend

Set `NEXT_PUBLIC_API_URL` in Vercel to your Hugging Face Space URL.

## Verification

Run `./verify_deployment.sh` to confirm all files are properly prepared.

## Complete Guide

For detailed instructions, see `DEPLOYMENT_INSTRUCTIONS.md`.

Your application will be available as:
- Backend: `https://YOUR_USERNAME-space-name.hf.space`
- Frontend: `https://your-project.vercel.app`