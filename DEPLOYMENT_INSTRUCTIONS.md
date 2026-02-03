# Deployment Instructions

This document provides step-by-step instructions for deploying the Todo AI Chatbot application on Hugging Face Spaces (backend) and Vercel (frontend).

## Prerequisites

1. Hugging Face account with access to Spaces
2. Vercel account
3. Neon PostgreSQL database connection string
4. OpenAI API key
5. Git repository access

## Deploying Backend on Hugging Face Spaces

### Option 1: Using the Space Interface (Recommended)

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click "Create new Space"
2. Choose the following settings:
   - **Space SDK**: Gradio (to run our FastAPI app)
   - **Hardware**: CPU Basic (or higher based on needs)
   - **Storage Tier**: Large
   - **Visibility**: Public or Private (as needed)

3. In the Space configuration, add the following secrets:
   ```
   DATABASE_URL: "your_neon_postgres_connection_string"
   SECRET_KEY: "your_jwt_secret_key_generated_with_openssl_rand_hex_32"
   OPENAI_API_KEY: "your_openai_api_key"
   ```

4. Add the following environment variables:
   ```
   APP_NAME: "Todo Evolution API"
   APP_VERSION: "2.0.0"
   DEBUG: "False"
   ALGORITHM: "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES: "30"
   LOG_LEVEL: "INFO"
   ENVIRONMENT: "production"
   ```

5. Clone your repository and copy the backend files to the Space:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/todo-backend
   cd todo-backend
   cp -r /path/to/your/backend/* .
   git add .
   git commit -m "Initial backend deployment"
   git push
   ```

### Option 2: Using Git

1. Create a new Space on Hugging Face via the UI or API
2. Clone the Space repository:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/todo-backend
   cd todo-backend
   ```

3. Copy the backend files:
   ```bash
   cp /path/to/your/backend/app.py .
   cp /path/to/your/backend/requirements_hf.txt .
   cp -r /path/to/your/backend/src .
   cp /path/to/your/backend/space.yaml .
   ```

4. Configure secrets in your Space settings:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `SECRET_KEY`: JWT secret (generate with `openssl rand -hex 32`)
   - `OPENAI_API_KEY`: Your OpenAI API key

5. Commit and push:
   ```bash
   git add .
   git commit -m "Deploy backend to Hugging Face Spaces"
   git push
   ```

## Deploying Frontend on Vercel

1. Prepare your frontend for deployment:
   ```bash
   cd frontend
   ```

2. Update the `.env.local` file with your Hugging Face Space URL:
   ```bash
   NEXT_PUBLIC_API_URL="https://YOUR_USERNAME-hf-space-name.hf.space"
   NEXT_PUBLIC_APP_URL="https://your-project.vercel.app"
   ```

3. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)

4. Go to [vercel.com](https://vercel.com) and connect your Git account

5. Import your project and configure the following environment variables in Vercel:
   ```
   NEXT_PUBLIC_API_URL: "https://YOUR_USERNAME-hf-space-name.hf.space" (your Hugging Face Space URL)
   NEXT_PUBLIC_APP_URL: "https://your-project.vercel.app" (your Vercel project URL)
   NEXT_PUBLIC_APP_NAME: "Todo Evolution"
   NEXT_PUBLIC_ENABLE_VOICE_COMMANDS: "true"
   NEXT_PUBLIC_ENABLE_MULTI_LANGUAGE: "true"
   NEXT_PUBLIC_USER_ID: "1" (temporary, replace with proper auth later)
   NEXT_PUBLIC_ENABLE_VOICE: "true"
   NEXT_PUBLIC_ENABLE_ANALYTICS: "true"
   NEXT_PUBLIC_ENABLE_RECURRING: "true"
   NEXT_PUBLIC_ANALYTICS_DEFAULT_DAYS: "30"
   NEXT_PUBLIC_VOICE_LANG: "en-US"
   NEXT_PUBLIC_VOICE_AUTO_SPEAK: "true"
   DATABASE_URL: "your_neon_postgres_connection_string" (same as backend)
   PRISMA_DB_PROVIDER: "sqlite"
   BETTER_AUTH_SECRET: "your_better_auth_secret_key"
   BETTER_AUTH_URL: "https://your-project.vercel.app"
   ```

6. Click "Deploy" and wait for the build to complete

## Alternative: Proxy Setup for API Requests

If you prefer not to expose your Hugging Face Space URL directly, you can set up API proxying in your Next.js app:

1. Create a file `frontend/src/pages/api/proxy/[...path].js`:
   ```javascript
   export default async function handler(req, res) {
     const { path } = req.query;
     const url = `https://YOUR_HF_SPACE_URL/${path.join('/')}`;

     const response = await fetch(url, {
       method: req.method,
       headers: req.headers,
       body: req.body ? JSON.stringify(req.body) : undefined
     });

     const data = await response.json();
     res.status(response.status).json(data);
   }
   ```

2. Update your frontend API calls to use `/api/proxy/` instead of the direct Hugging Face URL

## Post-Deployment Steps

1. Verify the backend is running by visiting your Hugging Face Space URL
2. Check the API documentation at `/docs` endpoint
3. Verify the frontend is accessible and can communicate with the backend
4. Test all functionality including:
   - User authentication
   - Task creation and management
   - AI chat functionality
   - Voice commands (if enabled)
   - Multi-language support

## Troubleshooting

### Common Issues:

1. **Database Connection Issues**:
   - Ensure your Neon PostgreSQL connection string is correct
   - Check that the database allows connections from Hugging Face Spaces
   - Verify SSL settings in the connection string

2. **API Communication Issues**:
   - Confirm CORS settings in the backend allow your Vercel domain
   - Check that the API URL is correctly set in frontend environment variables
   - Verify that the backend is healthy and responding

3. **Authentication Issues**:
   - Ensure JWT secret is the same in both frontend and backend
   - Check that authentication endpoints are accessible

4. **AI Functionality Issues**:
   - Verify OpenAI API key is correctly set in backend secrets
   - Check rate limits on OpenAI API usage

### Logs and Monitoring:

- Hugging Face Spaces: Access logs through the Space interface
- Vercel: Use Vercel Dashboard to view deployment logs and monitor performance

## Scaling Considerations

- For increased traffic, consider upgrading Hugging Face Space hardware
- Monitor database connection limits with Neon PostgreSQL
- Implement caching for frequently accessed data
- Consider CDN for static assets

## Security Best Practices

- Never commit secrets to version control
- Use strong, randomly generated secrets
- Regularly rotate API keys
- Monitor access logs for unusual activity
- Keep dependencies updated