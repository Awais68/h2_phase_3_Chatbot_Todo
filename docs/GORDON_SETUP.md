# Gordon (Docker AI) Setup Guide

## Overview
Gordon is Docker's built-in AI assistant that helps with Dockerfile creation, optimization, and troubleshooting.

## Checking Availability

### Prerequisites
- Docker Desktop installed
- Docker version 4.26.0 or higher (with AI features)

### Check if Gordon is Available
Run the following script to check availability:
```bash
chmod +x scripts/check-gordon.sh
./scripts/check-gordon.sh
```

## Enabling Gordon (If Available)

### In Docker Desktop
1. Open Docker Desktop
2. Go to Settings (Cmd/Ctrl + ,)
3. Navigate to "Features in development" or "Experimental Features"
4. Enable "Docker AI" or "Gordon" option
5. Restart Docker Desktop if prompted

### Using Gordon
Once enabled, you can use Gordon through Docker Desktop UI or CLI:
```bash
# Example Docker AI commands (when available)
docker ai create Dockerfile --help
docker ai optimize Dockerfile
```

## If Gordon is Not Available

If Gordon is not available in your Docker version:

1. Follow manual Dockerfile optimization techniques (see DOCKERFILE_OPTIMIZATION.md)
2. Consider upgrading to Docker Desktop with AI features
3. Use online Dockerfile generators and optimizers

## Troubleshooting

### Docker AI Commands Not Available
- Check if your Docker Desktop version supports AI features
- Verify Docker AI is enabled in settings
- Restart Docker Desktop after enabling features

### Gordon Not Responding
- Ensure you have a stable internet connection
- Check Docker Desktop status in the system tray
- Restart Docker Desktop if needed