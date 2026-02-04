#!/bin/bash
# Script to update the OpenAI API key in the .env file

echo "OpenAI API Key Update Helper"
echo "============================="
echo ""
echo "This script will help you update your OpenAI API key in the .env file."
echo ""

# Check if API key is provided as argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <your-openai-api-key>"
    echo ""
    echo "To get your OpenAI API key:"
    echo "1. Go to https://platform.openai.com/api-keys"
    echo "2. Create a new secret key or use an existing one"
    echo "3. Copy the key and provide it as an argument to this script"
    echo ""
    echo "Example: $0 sk-1234567890abcdefghijklmnopqrstuvwxyz"
    exit 1
fi

API_KEY=$1

# Validate that the API key looks like a real OpenAI key (starts with sk-)
if [[ ! $API_KEY =~ ^sk-[a-zA-Z0-9]+$ ]]; then
    echo "Error: API key doesn't look valid. OpenAI API keys should start with 'sk-' followed by alphanumeric characters."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="/media/awais/6372445e-8fda-42fa-9034-61babd7dafd1/150 GB DATA TRANSFER/hackathon series/hackathon-2/phase-3 chatbot_todo/backend/hf_deployment/todo_chatbot"

echo "Updating API key in $BACKEND_DIR/.env..."
echo ""

# Backup the current .env file
cp "$BACKEND_DIR/.env" "$BACKEND_DIR/.env.backup.$(date +%Y%m%d_%H%M%S)"

# Update the API key in the .env file
sed -i "s|^OPENAI_API_KEY=.*|OPENAI_API_KEY=\"$API_KEY\"|" "$BACKEND_DIR/.env"

if [ $? -eq 0 ]; then
    echo "✅ Successfully updated the OpenAI API key in the .env file!"
    echo "Backup saved as: $BACKEND_DIR/.env.backup.$(date +%Y%m%d_%H%M%S)"
    echo ""
    echo "Now restart your server to load the new API key:"
    echo "cd \"$BACKEND_DIR\" && pkill -f uvicorn && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000"
else
    echo "❌ Failed to update the API key. Please check the .env file manually."
    exit 1
fi