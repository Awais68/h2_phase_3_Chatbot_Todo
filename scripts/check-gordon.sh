#!/bin/bash

# scripts/check-gordon.sh
# Check if Gordon (Docker AI) is available

set -e

echo "Checking Gordon (Docker AI) availability..."

# Check Docker version
echo "Docker version:"
docker version --format '{{.Server.Version}}'

# Check if Docker Desktop is being used
if command -v docker &> /dev/null; then
    DOCKER_INFO=$(docker version -f json 2>/dev/null || echo "{}")

    # Check for Docker AI features (Gordon)
    if docker help | grep -q ai; then
        echo "✅ Docker AI features detected!"
        echo "Docker AI commands available:"
        docker ai --help || echo "No specific AI commands found"

        # Check if Docker Desktop settings have AI features
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # Mac
            SETTINGS_PATH="$HOME/Library/Group Containers/group.com.docker/settings.json"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            SETTINGS_PATH="$HOME/.docker/desktop/settings.json"
        elif [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "cygwin"* ]]; then
            # Windows (via WSL)
            echo "Please check Docker Desktop settings in Windows"
            SETTINGS_PATH=""
        fi

        if [[ -n "$SETTINGS_PATH" && -f "$SETTINGS_PATH" ]]; then
            if grep -q "ai" "$SETTINGS_PATH" 2>/dev/null; then
                echo "✅ AI features detected in Docker Desktop settings"
            else
                echo "ℹ️  AI features not enabled in Docker Desktop settings"
                echo "   Enable via Docker Desktop → Settings → Features → Docker AI"
            fi
        fi
    else
        echo "ℹ️  Docker AI features not available in this version"
        echo "   Gordon AI assistant not detected"
        echo "   Consider upgrading to Docker Desktop with AI features"
    fi
else
    echo "❌ Docker is not installed or accessible"
    exit 1
fi

echo ""
echo "For Gordon AI access:"
echo "- Use Docker Desktop with AI features enabled"
echo "- Go to Settings → Features → Docker AI to enable"
echo "- Or use manual optimization techniques (see DOCKERFILE_OPTIMIZATION.md)"