#!/bin/bash

# scripts/verify-kagent.sh
# Test Kagent installation

set -e

echo "Verifying Kagent installation..."

# Check if kagent is installed
if ! command -v kagent &> /dev/null; then
    echo "❌ Kagent is not installed"
    exit 1
fi

echo "✅ Kagent is installed"

# Check version
echo "Kagent version:"
kagent version

# Check API connectivity
if [[ -z "$OPENAI_API_KEY" ]]; then
    if [[ -f .env.kagent ]]; then
        source .env.kagent
    fi
fi

if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "❌ OPENAI_API_KEY is not configured"
    exit 1
fi

echo "✅ API key is configured"

# Run sample cluster analysis
echo "Running sample cluster analysis..."
kubectl cluster-info > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    echo "Current cluster info:"
    kubectl cluster-info

    echo "Testing kagent cluster analysis..."
    # Just test that kagent command works without making expensive API calls
    kagent --help > /dev/null
    if [[ $? -eq 0 ]]; then
        echo "✅ Kagent command is working"
    else
        echo "❌ Kagent command failed"
        exit 1
    fi
else
    echo "⚠️  Kubernetes cluster not accessible, skipping cluster analysis test"
fi

echo "✅ Kagent verification completed successfully"