#!/bin/bash

# scripts/configure-kagent.sh
# Configure Kagent with API key

set -e

echo "Configuring Kagent..."

# Check if .env.kagent file exists
if [[ ! -f .env.kagent ]]; then
    echo "Please create .env.kagent file with your OpenAI API key"
    echo "Example: cp .env.kagent.example .env.kagent"
    exit 1
fi

# Source the environment file
source .env.kagent

# Verify API key is set
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo "OPENAI_API_KEY is not set in .env.kagent"
    exit 1
fi

# Set the API key in environment
export OPENAI_API_KEY

echo "Kagent configured with API key"
echo "Testing basic functionality..."

# Test basic functionality
kagent --help > /dev/null
if [[ $? -eq 0 ]]; then
    echo "Kagent is ready to use"
else
    echo "Error: Kagent not working properly"
    exit 1
fi