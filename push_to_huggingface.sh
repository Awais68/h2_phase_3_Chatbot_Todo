#!/bin/bash

# Script to push backend code to Hugging Face Space
# Usage: ./push_to_huggingface.sh <SPACE_NAME>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Push Backend to Hugging Face Space${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if space name is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Space name is required${NC}"
    echo -e "Usage: ./push_to_huggingface.sh <USERNAME/SPACE_NAME>"
    echo -e "Example: ./push_to_huggingface.sh myusername/todo-ai-chatbot"
    exit 1
fi

SPACE_NAME="$1"
HF_DEPLOYMENT_DIR="backend/hf_deployment"

# Check if deployment directory exists
if [ ! -d "$HF_DEPLOYMENT_DIR" ]; then
    echo -e "${RED}Error: Deployment directory not found at $HF_DEPLOYMENT_DIR${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Preparing to push to Hugging Face Space: $SPACE_NAME${NC}"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    exit 1
fi

# Navigate to deployment directory
cd "$HF_DEPLOYMENT_DIR"

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo -e "${BLUE}🔧 Initializing git repository...${NC}"
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}"
fi

# Check if remote exists
if git remote get-url origin &> /dev/null; then
    echo -e "${YELLOW}⚠️  Remote 'origin' already exists. Removing...${NC}"
    git remote remove origin
fi

# Add Hugging Face remote
HF_URL="https://huggingface.co/spaces/$SPACE_NAME"
echo -e "${BLUE}🔗 Adding Hugging Face remote: $HF_URL${NC}"
git remote add origin "$HF_URL"

# Stage all files
echo -e "${BLUE}📝 Staging files...${NC}"
git add .

# Commit changes
COMMIT_MSG="Update backend - $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "${BLUE}💾 Creating commit: $COMMIT_MSG${NC}"
git commit -m "$COMMIT_MSG" || echo -e "${YELLOW}⚠️  No changes to commit${NC}"

# Push to Hugging Face
echo ""
echo -e "${YELLOW}🚀 Pushing to Hugging Face...${NC}"
echo -e "${YELLOW}📌 You may be prompted for your Hugging Face credentials${NC}"
echo -e "${YELLOW}   Username: your-huggingface-username${NC}"
echo -e "${YELLOW}   Password: your-huggingface-token (not your password!)${NC}"
echo ""

git push -u origin main || {
    echo ""
    echo -e "${RED}❌ Push failed. This might be because:${NC}"
    echo -e "   1. The Space doesn't exist yet - create it first at https://huggingface.co/new-space"
    echo -e "   2. You haven't authenticated - make sure you're using your HF token as password"
    echo -e "   3. The remote URL is incorrect"
    echo ""
    echo -e "${BLUE}To authenticate with Hugging Face:${NC}"
    echo -e "   git config --global credential.helper store"
    echo -e "   Then try pushing again and enter your HF token when prompted"
    exit 1
}

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✓ Successfully pushed to Hugging Face!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Your Space URL:${NC} $HF_URL"
echo -e ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Visit $HF_URL"
echo -e "  2. Go to Settings > Variables and secrets"
echo -e "  3. Add these secrets:"
echo -e "     - DATABASE_URL: Your Neon PostgreSQL connection string"
echo -e "     - SECRET_KEY: Generate with: openssl rand -hex 32"
echo -e "     - OPENAI_API_KEY: Your OpenAI API key"
echo -e "  4. Wait for the Space to build and start"
echo -e "  5. Test your API at: $HF_URL/docs"
echo ""

cd - > /dev/null
