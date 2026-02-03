#!/bin/bash

# Verification script to check if deployment files are correctly set up

echo "Deployment Verification Script"
echo "=============================="

# Check backend files
echo "Checking backend deployment files..."
if [ -f "backend/app.py" ] && [ -f "backend/requirements_hf.txt" ] && [ -f "backend/space.yaml" ]; then
    echo "✓ Backend deployment files found"
else
    echo "✗ Missing backend deployment files"
    exit 1
fi

# Check frontend files
echo "Checking frontend deployment files..."
if [ -f "frontend/vercel.json" ]; then
    echo "✓ Frontend deployment configuration found"
else
    echo "✗ Missing frontend deployment configuration"
    exit 1
fi

# Check if deployment instructions exist
if [ -f "DEPLOYMENT_INSTRUCTIONS.md" ]; then
    echo "✓ Deployment instructions found"
else
    echo "✗ Deployment instructions not found"
    exit 1
fi

# Check if deployment script exists and is executable
if [ -f "deploy.sh" ] && [ -x deploy.sh ]; then
    echo "✓ Deployment script found and is executable"
else
    echo "✗ Deployment script not found or not executable"
    exit 1
fi

echo ""
echo "All deployment files are in place!"
echo ""
echo "To deploy:"
echo "1. Backend: Run './deploy.sh backend' then follow Hugging Face deployment instructions"
echo "2. Frontend: Run './deploy.sh frontend' then follow Vercel deployment instructions"
echo "3. Or run './deploy.sh both' to prepare both"
echo ""
echo "Full instructions are in DEPLOYMENT_INSTRUCTIONS.md"