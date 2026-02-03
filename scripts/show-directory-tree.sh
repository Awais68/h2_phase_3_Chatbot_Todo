#!/bin/bash

# scripts/show-directory-tree.sh
# Shows the directory structure in tree format

set -e

PROJECT_ROOT="todo-ai-chatbot-k8s"
if [[ ! -d "$PROJECT_ROOT" ]]; then
    echo "Project root directory $PROJECT_ROOT does not exist"
    echo "Run create-directory-structure.sh first"
    exit 1
fi

echo "Directory structure for Todo AI Chatbot Kubernetes Deployment:"
echo ""

cd "$PROJECT_ROOT"

if command -v tree &> /dev/null; then
    # Use tree command if available
    tree -a -I ".git|.gitignore|*.log|*.tmp" .
else
    # Fallback to find command to show directory structure
    echo "Using find to show directory structure:"
    find . -type d | sed 's/[^/]*\//|/g' | sed 's/^|//' | sed 's/|/  |/g'

    echo ""
    echo "All files in structure:"
    find . -type f -not -path "./.git/*" -not -name "*.log" -not -name "*.tmp" | sed 's/[^/]*\//|/g' | sed 's/^|//' | sed 's/|/  |/g'
fi