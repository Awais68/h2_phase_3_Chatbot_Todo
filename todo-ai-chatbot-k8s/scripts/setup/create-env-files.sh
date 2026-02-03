#!/bin/bash
# Script to create .env files from templates

set -e

echo "Creating .env files from templates..."

# Define source and destination directories
SOURCE_CONFIG_DIR="../config"
SOURCE_DOCKER_DIR="../docker"
SOURCE_K8S_DIR="../k8s"

# Create local .env file from template
if [[ -f "$SOURCE_CONFIG_DIR/local/.env.example" ]]; then
    if [[ ! -f "$SOURCE_CONFIG_DIR/local/.env" ]]; then
        cp "$SOURCE_CONFIG_DIR/local/.env.example" "$SOURCE_CONFIG_DIR/local/.env"
        echo "✅ Created: config/local/.env from template"
    else
        echo "ℹ️  config/local/.env already exists, skipping"
    fi
else
    echo "❌ Template file config/local/.env.example not found"
    exit 1
fi

# Create production .env file from template
if [[ -f "$SOURCE_CONFIG_DIR/prod/.env.example" ]]; then
    if [[ ! -f "$SOURCE_CONFIG_DIR/prod/.env" ]]; then
        cp "$SOURCE_CONFIG_DIR/prod/.env.example" "$SOURCE_CONFIG_DIR/prod/.env"
        echo "✅ Created: config/prod/.env from template"
    else
        echo "ℹ️  config/prod/.env already exists, skipping"
    fi
else
    echo "❌ Template file config/prod/.env.example not found"
    exit 1
fi

# Create Docker .env file from template
if [[ -f "$SOURCE_DOCKER_DIR/.env.docker.example" ]]; then
    if [[ ! -f "$SOURCE_DOCKER_DIR/.env.docker" ]]; then
        cp "$SOURCE_DOCKER_DIR/.env.docker.example" "$SOURCE_DOCKER_DIR/.env.docker"
        echo "✅ Created: docker/.env.docker from template"
    else
        echo "ℹ️  docker/.env.docker already exists, skipping"
    fi
else
    echo "❌ Template file docker/.env.docker.example not found"
    exit 1
fi

# Create K8s .env file from template
if [[ -f "$SOURCE_K8S_DIR/.env.k8s.example" ]]; then
    if [[ ! -f "$SOURCE_K8S_DIR/.env.k8s" ]]; then
        cp "$SOURCE_K8S_DIR/.env.k8s.example" "$SOURCE_K8S_DIR/.env.k8s"
        echo "✅ Created: k8s/.env.k8s from template"
    else
        echo "ℹ️  k8s/.env.k8s already exists, skipping"
    fi
else
    echo "❌ Template file k8s/.env.k8s.example not found"
    exit 1
fi

echo "✅ All .env files created from templates!"
echo ""
echo "📝 Remember to update the .env files with your actual values before deployment."
echo "   Do not commit .env files to version control."