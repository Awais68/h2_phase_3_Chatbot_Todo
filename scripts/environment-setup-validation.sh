#!/bin/bash

# scripts/environment-setup-validation.sh
# Validation script for environment setup completion

set -e

echo "🔍 Environment Setup Validation"
echo "==============================="

# Check if required tools are available
echo "✅ Checking for required tools..."

TOOL_ERROR=0
if command -v docker &> /dev/null; then
    echo "   ✓ Docker is installed: $(docker --version)"
else
    echo "   ❌ Docker is not installed"
    TOOL_ERROR=1
fi

if command -v kubectl &> /dev/null; then
    echo "   ✓ kubectl is installed: $(kubectl version --client --short 2>/dev/null || echo 'available')"
else
    echo "   ❌ kubectl is not installed"
    TOOL_ERROR=1
fi

if command -v helm &> /dev/null; then
    echo "   ✓ Helm is installed: $(helm version --short 2>/dev/null)"
else
    echo "   ⚠ Helm is not installed (optional for now)"
fi

if command -v kagent &> /dev/null; then
    echo "   ✓ Kagent is installed: $(kagent version 2>/dev/null || echo 'available')"
else
    echo "   ℹ Kagent is not installed (expected if not yet installed)"
fi

# Check if Kagent script exists
if [[ -f "scripts/install-kagent.sh" ]]; then
    echo "   ✓ Kagent installation script exists"
else
    echo "   ❌ Kagent installation script missing"
    TOOL_ERROR=1
fi

# Check if Gordon check script exists
if [[ -f "scripts/check-gordon.sh" ]]; then
    echo "   ✓ Gordon check script exists"
else
    echo "   ❌ Gordon check script missing"
    TOOL_ERROR=1
fi

# Check if directory structure exists
if [[ -d "todo-ai-chatbot-k8s" ]]; then
    echo "   ✓ Project directory structure created"
else
    echo "   ❌ Project directory structure missing"
    TOOL_ERROR=1
fi

# Count total directories created
DIR_COUNT=$(find todo-ai-chatbot-k8s -type d 2>/dev/null | wc -l || echo 0)
if [ "$DIR_COUNT" -gt 0 ]; then
    echo "   ✓ Found $DIR_COUNT directories in project structure"
else
    echo "   ❌ No project directories found"
    TOOL_ERROR=1
fi

# Check documentation files
DOC_COUNT=0
if [[ -f "docs/KAGENT_SETUP.md" ]]; then
    DOC_COUNT=$((DOC_COUNT + 1))
    echo "   ✓ Kagent setup documentation exists"
fi

if [[ -f "docs/KAGENT_USAGE.md" ]]; then
    DOC_COUNT=$((DOC_COUNT + 1))
    echo "   ✓ Kagent usage documentation exists"
fi

if [[ -f "docs/GORDON_SETUP.md" ]]; then
    DOC_COUNT=$((DOC_COUNT + 1))
    echo "   ✓ Gordon setup documentation exists"
fi

if [[ -f "docs/DOCKERFILE_OPTIMIZATION.md" ]]; then
    DOC_COUNT=$((DOC_COUNT + 1))
    echo "   ✓ Dockerfile optimization guide exists"
fi

if [[ -f "docs/DIRECTORY_STRUCTURE.md" ]]; then
    DOC_COUNT=$((DOC_COUNT + 1))
    echo "   ✓ Directory structure documentation exists"
fi

if [ $DOC_COUNT -ge 4 ]; then
    echo "   ✓ Created $DOC_COUNT out of 5 expected documentation files"
else
    echo "   ❌ Only $DOC_COUNT out of 5 documentation files found"
    TOOL_ERROR=1
fi

# Check script files
SCRIPT_COUNT=0
if [[ -f "scripts/install-kagent.sh" ]]; then
    SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
fi
if [[ -f "scripts/configure-kagent.sh" ]]; then
    SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
fi
if [[ -f "scripts/verify-kagent.sh" ]]; then
    SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
fi
if [[ -f "scripts/check-gordon.sh" ]]; then
    SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
fi
if [[ -f "scripts/create-directory-structure.sh" ]]; then
    SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
fi
if [[ -f "scripts/verify-directory-structure.sh" ]]; then
    SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
fi
if [[ -f "scripts/show-directory-tree.sh" ]]; then
    SCRIPT_COUNT=$((SCRIPT_COUNT + 1))
fi

if [ $SCRIPT_COUNT -ge 7 ]; then
    echo "   ✓ Created $SCRIPT_COUNT out of 7 expected utility scripts"
else
    echo "   ❌ Only $SCRIPT_COUNT out of 7 utility scripts found"
    TOOL_ERROR=1
fi

# Check environment files
if [[ -f ".env.kagent.example" ]]; then
    echo "   ✓ Kagent environment template exists"
else
    echo "   ❌ Kagent environment template missing"
    TOOL_ERROR=1
fi

if [[ -f ".gitignore" ]]; then
    echo "   ✓ .gitignore file exists"
else
    echo "   ⚠ .gitignore file missing (optional)"
fi

echo ""
if [ $TOOL_ERROR -eq 0 ]; then
    echo "🎉 All environment setup tasks completed successfully!"
    echo ""
    echo "Summary:"
    echo "- Tools verified: Docker, kubectl (with optional Helm)"
    echo "- Kagent installation and configuration scripts created"
    echo "- Gordon Docker AI check script created"
    echo "- Complete directory structure with $DIR_COUNT directories"
    echo "- $DOC_COUNT documentation files created"
    echo "- $SCRIPT_COUNT utility scripts created"
    echo "- Environment templates provided"
    echo ""
    echo "🚀 You're now ready to proceed with the next phase of Kubernetes deployment!"
    exit 0
else
    echo "❌ Some environment setup tasks are incomplete"
    exit 1
fi