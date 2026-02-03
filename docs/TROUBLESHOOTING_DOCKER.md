# Docker Troubleshooting Guide

This guide has been updated and replaced with a more comprehensive version. Please refer to the [Docker Desktop Troubleshooting Guide](DOCKER_DESKTOP_TROUBLESHOOTING_GUIDE.md) for complete information on troubleshooting Docker Desktop issues across all platforms.

## Quick Reference

### Common Commands
```bash
# Check Docker status
docker info

# Check version
docker version

# Test Docker
docker run --rm hello-world

# View running containers
docker ps

# View all containers
docker ps -a

# View images
docker images

# Check disk usage
docker system df

# Clean up
docker system prune -a --volumes

# Check logs
docker logs <container_id>
```

For comprehensive troubleshooting steps, please see [DOCKER_DESKTOP_TROUBLESHOOTING_GUIDE.md](DOCKER_DESKTOP_TROUBLESHOOTING_GUIDE.md)