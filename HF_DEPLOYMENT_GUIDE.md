# Hugging Face Deployment Instructions

This guide will help you deploy your backend code to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (create one at https://huggingface.co/join)
2. Git installed on your system
3. Your Hugging Face token (get it from https://huggingface.co/settings/tokens)

## Step 1: Create a Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Fill in the details:
   - **Space name**: Choose a name like `todo-ai-chatbot` or `todo-app-backend`
   - **License**: Choose appropriate license (MIT recommended)
   - **Select the Space SDK**: Choose **Docker** (NOT Gradio or Streamlit)
   - **Visibility**: Choose Public or Private
   - Click **Create Space**

## Step 2: Set Up Environment Variables

After creating your Space:

1. Go to your Space settings (Settings tab)
2. Click on "Variables and secrets"  
3. Add the following secrets:

   - **DATABASE_URL**: Your Neon PostgreSQL connection string
     ```
     postgresql://username:password@hostname/database?sslmode=require
     ```
   
   - **SECRET_KEY**: Generate a secure key
     ```bash
     openssl rand -hex 32
     ```
   
   - **OPENAI_API_KEY**: Your OpenAI API key
     ```
     sk-...
     ```

   - **BETTER_AUTH_SECRET**: Generate another secure key
     ```bash
     openssl rand -hex 32
     ```

   - **BETTER_AUTH_URL**: Your Space URL (will be available after creation)
     ```
     https://USERNAME-SPACE_NAME.hf.space
     ```

## Step 3: Push Your Backend Code

### Option A: Using the Provided Script (Recommended)

```bash
# Make sure you're in the project root directory
cd "/media/awais/6372445e-8fda-42fa-9034-61babd7dafd1/150 GB DATA TRANSFER/hackathon series/hackathon-2/phase-3 chatbot_todo"

# Run the push script with your Space name
./push_to_huggingface.sh USERNAME/SPACE_NAME

# Example:
# ./push_to_huggingface.sh awais/todo-ai-chatbot
```

When prompted for credentials:
- **Username**: Your Hugging Face username
- **Password**: Your Hugging Face **token** (NOT your password!)

### Option B: Manual Push

```bash
# Navigate to the deployment directory
cd backend/hf_deployment

# Initialize git (if not already done)
git init

# Add Hugging Face remote
git remote add origin https://huggingface.co/spaces/awais68-todo-chatbot.hf.space

# Stage and commit files
git add .
git commit -m "Initial backend deployment"

# Push to Hugging Face
git push -u origin main
```

## Step 4: Run Database Migrations

After your Space is running, you need to run the migrations to set up the database:

1. Go to your Space on Hugging Face
2. Open the "Logs" tab
3. Click on "Factory reboot" to restart the Space
4. The migrations will run automatically on startup

Alternatively, you can SSH into your Space (if persistent storage is enabled) and run:

```bash
python run_migrations.py
```

## Step 5: Verify Deployment

1. Visit your Space URL: `https://USERNAME-SPACE_NAME.hf.space`
2. You should see a JSON response with the API status
3. Visit the API docs at: `https://USERNAME-SPACE_NAME.hf.space/docs`
4. Test an endpoint like `/api/tasks` to verify it's working

## Step 6: Update Frontend Configuration

Now that your backend is deployed, update your frontend to use the Hugging Face Space URL:

1. In your frontend repository, update `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=https://USERNAME-SPACE_NAME.hf.space
   ```

2. Redeploy your frontend (if on Vercel/Netlify)

## Troubleshooting

### Authentication Issues

If you get authentication errors when pushing:

```bash
# Store credentials for future use
git config --global credential.helper store

# Try pushing again
git push -u origin main
```

### Build Failures

Check the build logs in your Space:
1. Go to your Space on Hugging Face
2. Click on "Logs" tab
3. Look for error messages

Common issues:
- Missing environment variables (add them in Space settings)
- Database connection issues (check DATABASE_URL)
- Missing dependencies (check requirements.txt)

### Database Connection

If you see database connection errors:
1. Verify DATABASE_URL is correct in Space secrets
2. Check that your Neon database allows connections from Hugging Face Spaces
3. Make sure the database exists and migrations have run

### CORS Issues

If you get CORS errors when connecting from frontend:
1. Check that `BETTER_AUTH_URL` matches your frontend URL
2. Verify CORS settings in `src/middleware/cors.py`

## Updating Your Deployment

To update your deployed backend:

```bash
# Make your changes to the code
# Then push again using the script
./push_to_huggingface.sh USERNAME/SPACE_NAME
```

Or manually:

```bash
cd backend/hf_deployment
git add .
git commit -m "Update: describe your changes"
git push origin main
```

The Space will automatically rebuild and redeploy.

## Monitoring and Logs

- View real-time logs in the "Logs" tab of your Space
- Check API status at: `https://YOUR-SPACE-URL.hf.space/health`
- Monitor database queries in Neon dashboard
- Check API performance at `/docs` endpoint

## Cost Considerations

- Hugging Face Spaces offers free CPU instances
- For better performance, consider upgrading to:
  - CPU Basic: Faster processing
  - GPU: If you plan to use AI features that require GPU
  - Persistent storage: To keep data between restarts

## Support

If you encounter issues:
1. Check the Hugging Face Spaces documentation: https://huggingface.co/docs/hub/spaces
2. Review the application logs in your Space
3. Check the GitHub issues for common problems
4. Contact support through Hugging Face forums

## Next Steps

After successful deployment:
1. Test all API endpoints using the `/docs` interface
2. Update your frontend to point to the new backend URL
3. Test the complete application flow
4. Set up monitoring and alerts
5. Configure backups for your database

Your backend is now live and ready to use! 🚀
