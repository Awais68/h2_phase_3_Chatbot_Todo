#!/bin/bash

# Deployment Script for Todo AI Chatbot
# This script helps prepare and deploy the application to Hugging Face and Vercel

set -e  # Exit on any error

echo "Todo AI Chatbot Deployment Script"
echo "=================================="

# Function to display usage
usage() {
    echo "Usage: $0 [backend|frontend|both]"
    echo "  backend  - Prepare backend for Hugging Face deployment"
    echo "  frontend - Prepare frontend for Vercel deployment"
    echo "  both     - Prepare both for deployment"
    exit 1
}

# Check if argument is provided
if [ $# -eq 0 ]; then
    usage
fi

ACTION=$1

case $ACTION in
    "backend")
        echo "Preparing backend for Hugging Face deployment..."

        cd backend/todo_chatbot

        # Create deployment package
        echo "Creating backend deployment package..."
        mkdir -p ../hf_deployment
        cp app.py requirements_hf.txt space.yaml ../hf_deployment/
        cp -r src ../hf_deployment/

        echo "Backend preparation complete!"
        echo "Files prepared in backend/hf_deployment/"
        echo ""
        echo "Next steps:"
        echo "1. Create a Hugging Face Space: https://huggingface.co/spaces"
        echo "2. Add the following secrets in Space settings:"
        echo "   - DATABASE_URL: your_neon_postgres_connection_string"
        echo "   - SECRET_KEY: your_jwt_secret_key"
        echo "   - OPENAI_API_KEY: your_openai_api_key"
        echo "3. Upload the files in hf_deployment/ to your Space"
        ;;

    "frontend")
        echo "Preparing frontend for Vercel deployment..."

        cd frontend

        # Create deployment notes
        echo "Creating frontend deployment notes..."
        cat > vercel_deployment_notes.txt << EOF
Frontend Deployment for Vercel
=============================

Environment Variables Required:
- NEXT_PUBLIC_API_URL: Your Hugging Face Space URL (e.g., https://username-space-name.hf.space)
- NEXT_PUBLIC_APP_URL: Your Vercel project URL (e.g., https://your-project.vercel.app)
- NEXT_PUBLIC_APP_NAME: Todo Evolution
- NEXT_PUBLIC_ENABLE_VOICE_COMMANDS: true
- NEXT_PUBLIC_ENABLE_MULTI_LANGUAGE: true
- NEXT_PUBLIC_USER_ID: 1
- NEXT_PUBLIC_ENABLE_VOICE: true
- NEXT_PUBLIC_ENABLE_ANALYTICS: true
- NEXT_PUBLIC_ENABLE_RECURRING: true
- NEXT_PUBLIC_ANALYTICS_DEFAULT_DAYS: 30
- NEXT_PUBLIC_VOICE_LANG: en-US
- NEXT_PUBLIC_VOICE_AUTO_SPEAK: true
- DATABASE_URL: Your Neon PostgreSQL connection string
- PRISMA_DB_PROVIDER: sqlite
- BETTER_AUTH_SECRET: Your better auth secret
- BETTER_AUTH_URL: Your Vercel project URL

Steps:
1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Go to https://vercel.com and import your project
3. Add the environment variables above in the Vercel dashboard
4. Click Deploy
EOF

        echo "Frontend preparation complete!"
        echo "Check frontend/vercel_deployment_notes.txt for deployment instructions"
        ;;

    "both")
        echo "Preparing both backend and frontend for deployment..."

        # Prepare backend
        echo "Preparing backend..."
        cd backend/todo_chatbot
        mkdir -p ../hf_deployment
        cp app.py requirements_hf.txt space.yaml ../hf_deployment/
        cp -r src ../hf_deployment/
        cd ../..

        # Prepare frontend
        echo "Preparing frontend..."
        cd frontend
        cat > vercel_deployment_notes.txt << EOF
Frontend Deployment for Vercel
=============================

Environment Variables Required:
- NEXT_PUBLIC_API_URL: Your Hugging Face Space URL (e.g., https://username-space-name.hf.space)
- NEXT_PUBLIC_APP_URL: Your Vercel project URL (e.g., https://your-project.vercel.app)
- NEXT_PUBLIC_APP_NAME: Todo Evolution
- NEXT_PUBLIC_ENABLE_VOICE_COMMANDS: true
- NEXT_PUBLIC_ENABLE_MULTI_LANGUAGE: true
- NEXT_PUBLIC_USER_ID: 1
- NEXT_PUBLIC_ENABLE_VOICE: true
- NEXT_PUBLIC_ENABLE_ANALYTICS: true
- NEXT_PUBLIC_ENABLE_RECURRING: true
- NEXT_PUBLIC_ANALYTICS_DEFAULT_DAYS: 30
- NEXT_PUBLIC_VOICE_LANG: en-US
- NEXT_PUBLIC_VOICE_AUTO_SPEAK: true
- DATABASE_URL: Your Neon PostgreSQL connection string
- PRISMA_DB_PROVIDER: sqlite
- BETTER_AUTH_SECRET: Your better auth secret
- BETTER_AUTH_URL: Your Vercel project URL

Steps:
1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Go to https://vercel.com and import your project
3. Add the environment variables above in the Vercel dashboard
4. Click Deploy
EOF
        cd ..

        echo "Both preparations complete!"
        echo "Backend files prepared in backend/hf_deployment/"
        echo "Frontend notes in frontend/vercel_deployment_notes.txt"
        ;;

    *)
        usage
        ;;
esac

echo ""
echo "For complete deployment instructions, see DEPLOYMENT_INSTRUCTIONS.md"