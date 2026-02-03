# Docker Desktop Troubleshooting Guide

## Table of Contents
- [Installation Issues](#installation-issues)
- [Startup Issues](#startup-issues)
- [Permission Issues](#permission-issues)
- [Resource Issues](#resource-issues)
- [Network Issues](#network-issues)
- [Kubernetes Issues](#kubernetes-issues)
- [Performance Issues](#performance-issues)
- [Platform-Specific Issues](#platform-specific-issues)

## Installation Issues

### Issue: Installation Fails on macOS

**Symptoms:**
- Installation hangs or crashes
- "Installation failed" error message

**Solutions:**

1. **Check System Requirements:**
```bash
   # Check macOS version
   sw_vers
   # Should be 11.0 or higher

   # Check processor type
   uname -m
   # arm64 for Apple Silicon, x86_64 for Intel
```

2. **Ensure Correct Installer:**
   - Apple Silicon: Use ARM64 installer
   - Intel: Use AMD64 installer

3. **Remove Previous Installation:**
```bash
   # Uninstall Docker Desktop
   /Applications/Docker.app/Contents/MacOS/uninstall

   # Remove config files
   rm -rf ~/Library/Group\ Containers/group.com.docker
   rm -rf ~/Library/Containers/com.docker.docker
   rm -rf ~/.docker

   # Reinstall
```

4. **Check Permissions:**
```bash
   # Ensure /Applications is writable
   ls -la /Applications | grep Docker

   # Fix permissions if needed
   sudo chown -R $(whoami):staff /Applications/Docker.app
```

### Issue: Installation Fails on Windows

**Symptoms:**
- WSL installation errors
- Hyper-V conflicts
- Installation wizard crashes

**Solutions:**

1. **Enable WSL 2:**
```powershell
   # Run as Administrator
   wsl --install

   # If already installed
   wsl --update
   wsl --set-default-version 2
```

2. **Enable Required Windows Features:**
```powershell
   # Run as Administrator

   # Enable WSL
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

   # Enable Virtual Machine Platform
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

   # Restart computer
   Restart-Computer
```

3. **Disable Conflicting Software:**
   - Disable other virtualization software (VirtualBox, VMware)
   - Temporarily disable antivirus during installation

4. **Install WSL 2 Kernel Update:**
```powershell
   # Download and install from:
   # https://aka.ms/wsl2kernel
```

### Issue: Installation Fails on Linux

**Symptoms:**
- Dependency errors
- Package conflicts

**Solutions:**

1. **Resolve Dependencies:**
```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -f

   # Fedora
   sudo dnf check-update
   sudo dnf install --best --allowerasing docker-desktop
```

2. **Check KVM Support:**
```bash
   # Check if KVM is available
   lsmod | grep kvm

   # Should show kvm_intel or kvm_amd

   # If not available, enable in BIOS
   # Reboot → BIOS → Enable Intel VT-x or AMD-V
```

3. **Remove Conflicting Docker Installations:**
```bash
   # Remove old Docker
   sudo apt-get remove docker docker-engine docker.io containerd runc

   # Remove Docker Compose V1
   sudo rm /usr/local/bin/docker-compose

   # Install Docker Desktop
```

## Startup Issues

### Issue: Docker Desktop Won't Start

**Symptoms:**
- "Docker Desktop is starting..." indefinitely
- Docker Desktop crashes on launch

**Solutions:**

**macOS:**
```bash
# Kill Docker processes
killall Docker

# Remove socket files
rm -f /var/run/docker.sock
rm -f ~/Library/Containers/com.docker.docker/Data/docker.sock

# Reset to factory defaults
# Docker Desktop → Troubleshoot → Reset to factory defaults

# Restart
open -a Docker
```

**Windows:**
```powershell
# Kill Docker processes
Get-Process "*docker*" | Stop-Process -Force

# Clear Docker data
Remove-Item $env:APPDATA\Docker -Recurse -Force

# Restart Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

**Linux:**
```bash
# Stop Docker Desktop
systemctl --user stop docker-desktop

# Clear cache
rm -rf ~/.docker/desktop

# Restart
systemctl --user start docker-desktop
```

### Issue: Docker Daemon Not Running

**Symptoms:**
- `docker info` returns "Cannot connect to the Docker daemon"
- Docker CLI commands fail

**Solutions:**

1. **Check Docker Desktop Status:**
```bash
   # macOS: Check menu bar for whale icon
   # Windows: Check system tray for whale icon
   # Linux: Check if process is running
   ps aux | grep docker
```

2. **Start Docker Desktop:**
```bash
   # macOS
   open -a Docker

   # Windows: Use Start menu

   # Linux
   systemctl --user start docker-desktop
```

3. **Check for Port Conflicts:**
```bash
   # Check if port 2375/2376 is in use
   lsof -i :2375
   lsof -i :2376

   # If in use, kill the process
   kill -9 <PID>
```

## Permission Issues

### Issue: "Permission Denied" on Linux

**Symptoms:**
- Cannot run docker commands without sudo
- "permission denied while trying to connect to the Docker daemon socket"

**Solutions:**

1. **Add User to Docker Group:**
```bash
   # Add user to docker group
   sudo usermod -aG docker $USER

   # Apply group changes
   newgrp docker

   # Or log out and log back in

   # Verify
   groups
   # Should show 'docker'
```

2. **Fix Socket Permissions:**
```bash
   # Check socket permissions
   ls -la /var/run/docker.sock

   # Fix if needed
   sudo chmod 666 /var/run/docker.sock

   # Or
   sudo chown root:docker /var/run/docker.sock
```

3. **Restart Docker Service:**
```bash
   systemctl --user restart docker-desktop
```

### Issue: "Permission Denied" on macOS

**Symptoms:**
- Cannot access Docker.app
- Cannot modify Docker files

**Solutions:**
```bash
# Fix Docker.app permissions
sudo chown -R $(whoami):staff /Applications/Docker.app

# Fix Docker data permissions
sudo chown -R $(whoami):staff ~/Library/Containers/com.docker.docker

# Restart Docker
killall Docker && open -a Docker
```

## Resource Issues

### Issue: Insufficient Memory

**Symptoms:**
- Containers crash with OOM (Out of Memory) errors
- "Cannot allocate memory" errors
- System becomes slow

**Solutions:**

1. **Increase Memory Allocation:**
```
   Docker Desktop → Settings → Resources → Memory
   Set to 8GB (or higher)
   Apply & Restart
```

2. **Check System Memory:**
```bash
   # macOS/Linux
   free -h
   # or
   vm_stat

   # Windows
   systeminfo | findstr Memory
```

3. **Clean Up Containers:**
```bash
   # Stop all containers
   docker stop $(docker ps -aq)

   # Remove stopped containers
   docker container prune -f

   # Remove unused images
   docker image prune -a -f
```

### Issue: Insufficient Disk Space

**Symptoms:**
- "No space left on device" errors
- Cannot pull images
- Cannot build images

**Solutions:**

1. **Check Docker Disk Usage:**
```bash
   docker system df -v
```

2. **Clean Up Docker Data:**
```bash
   # Remove all unused data
   docker system prune -a --volumes

   # This removes:
   # - Stopped containers
   # - Unused networks
   # - Dangling images
   # - Build cache
   # - Unused volumes
```

3. **Increase Disk Image Size:**
```
   Docker Desktop → Settings → Resources → Disk image size
   Increase to 60GB (or higher)
   Apply & Restart
```

4. **Move Docker Data (Windows):**
```powershell
   # Export existing data
   wsl --export docker-desktop D:\docker-desktop.tar
   wsl --export docker-desktop-data D:\docker-desktop-data.tar

   # Unregister current installations
   wsl --unregister docker-desktop
   wsl --unregister docker-desktop-data

   # Import to new location
   wsl --import docker-desktop D:\DockerDesktop D:\docker-desktop.tar
   wsl --import docker-desktop-data D:\DockerDesktop\data D:\docker-desktop-data.tar
```

### Issue: High CPU Usage

**Symptoms:**
- Fan running constantly
- System slowdown
- High CPU usage in Activity Monitor/Task Manager

**Solutions:**

1. **Limit CPU Allocation:**
```
   Docker Desktop → Settings → Resources → CPUs
   Reduce to 2-3 cores
   Apply & Restart
```

2. **Check Running Containers:**
```bash
   # View resource usage
   docker stats

   # Stop resource-intensive containers
   docker stop <container_id>
```

3. **Disable Unused Features:**
```
   Docker Desktop → Settings → Features in development
   Disable unused experimental features
```

## Network Issues

### Issue: Cannot Pull Images

**Symptoms:**
- Timeout errors when pulling images
- "TLS handshake timeout"
- "net/http: request canceled"

**Solutions:**

1. **Check Internet Connectivity:**
```bash
   # Test connection
   ping google.com

   # Test Docker Hub
   curl -I https://hub.docker.com
```

2. **Configure Proxy:**
```
   Docker Desktop → Settings → Resources → Proxies

   Manual proxy configuration:
   - HTTP Proxy: http://proxy.company.com:8080
   - HTTPS Proxy: http://proxy.company.com:8080
   - No Proxy: localhost,127.0.0.1

   Apply & Restart
```

3. **Use Registry Mirror:**
```
   Docker Desktop → Settings → Docker Engine

   Add registry mirror:
   {
     "registry-mirrors": [
       "https://mirror.gcr.io",
       "https://registry-1.docker.io"
     ]
   }

   Apply & Restart
```

4. **Login to Docker Hub:**
```bash
   docker login
   # Enter username and password
```

### Issue: Container Cannot Access Internet

**Symptoms:**
- apt-get update fails in container
- wget/curl commands fail
- Cannot install packages

**Solutions:**

1. **Check DNS Configuration:**
```bash
   # Test DNS inside container
   docker run --rm alpine nslookup google.com

   # If fails, configure DNS
```

2. **Configure Docker DNS:**
```
   Docker Desktop → Settings → Docker Engine

   Add DNS servers:
   {
     "dns": ["8.8.8.8", "8.8.4.4"]
   }

   Apply & Restart
```

3. **Check Firewall:**
```bash
   # macOS: Check firewall settings
   # System Preferences → Security & Privacy → Firewall
   # Allow Docker

   # Windows: Check Windows Firewall
   # Allow Docker Desktop through firewall

   # Linux: Check iptables
   sudo iptables -L
```

## Kubernetes Issues

### Issue: Kubernetes Won't Start

**Symptoms:**
- "Kubernetes is starting..." indefinitely
- kubectl commands fail
- Error: "The connection to the server was refused"

**Solutions:**

1. **Reset Kubernetes:**
```
   Docker Desktop → Settings → Kubernetes
   Click "Reset Kubernetes Cluster"
   Wait 5-10 minutes
```

2. **Disable and Re-enable:**
```
   Docker Desktop → Settings → Kubernetes
   Uncheck "Enable Kubernetes"
   Apply & Restart
   Wait 1 minute
   Check "Enable Kubernetes"
   Apply & Restart
   Wait 5-10 minutes
```

3. **Check Resources:**
```
   Ensure adequate resources:
   - Memory: 8GB minimum
   - CPUs: 4 minimum
   - Disk: 20GB available
```

4. **Check kubectl:**
```bash
   # Verify kubectl is installed
   kubectl version --client

   # Check context
   kubectl config current-context
   # Should be: docker-desktop

   # If not, set context
   kubectl config use-context docker-desktop
```

### Issue: kubectl Commands Fail

**Symptoms:**
- "The connection to the server was refused"
- "Unable to connect to the server"

**Solutions:**
```bash
# Check if Kubernetes is running
kubectl cluster-info

# Check context
kubectl config get-contexts

# Switch to docker-desktop context
kubectl config use-context docker-desktop

# Verify nodes
kubectl get nodes

# If still fails, restart Docker Desktop
```

## Performance Issues

### Issue: Slow Docker Performance

**Symptoms:**
- Slow image builds
- Slow container startup
- Slow file operations

**Solutions:**

1. **Increase Resources:**
```
   Docker Desktop → Settings → Resources
   - CPUs: 4-6
   - Memory: 8-16GB
   - Swap: 2GB
   - Disk: 60GB+
   Apply & Restart
```

2. **Enable VirtioFS (macOS):**
```
   Docker Desktop → Settings → General
   Enable "Use new Virtualization framework"
   Enable "VirtioFS" file sharing
   Apply & Restart
```

3. **Optimize Docker Images:**
```dockerfile
   # Use multi-stage builds
   # Use smaller base images (alpine)
   # Minimize layers
   # Use .dockerignore
```

4. **Clean Up Regularly:**
```bash
   # Weekly cleanup
   docker system prune -a --volumes
```

## Platform-Specific Issues

### macOS Specific

#### Issue: "osxkeychain" Credential Store Error
```bash
# Remove credential helper
rm ~/.docker/config.json

# Re-login
docker login
```

#### Issue: File Sharing Performance
```
Docker Desktop → Settings → Resources → File sharing
- Add only necessary directories
- Remove unnecessary ones
Apply & Restart
```

### Windows Specific

#### Issue: WSL 2 Integration Not Working
```powershell
# Check WSL 2 status
wsl --list --verbose

# Ensure VERSION is 2
# If not:
wsl --set-version docker-desktop 2
wsl --set-version docker-desktop-data 2

# Restart Docker Desktop
```

#### Issue: Hyper-V Conflicts
```powershell
# Disable Hyper-V (if using WSL 2)
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All

# Restart computer
Restart-Computer
```

### Linux Specific

#### Issue: AppArmor Conflicts
```bash
# Check AppArmor status
sudo aa-status

# If causing issues, disable for Docker
sudo aa-complain /etc/apparmor.d/docker

# Restart Docker
systemctl --user restart docker-desktop
```

## Getting Additional Help

### Collect Diagnostics

1. **Docker Desktop → Troubleshoot → Get Support**
2. Note the Diagnostic ID
3. Share when asking for help

### Check Logs

**macOS:**
```bash
# Docker logs
tail -f ~/Library/Containers/com.docker.docker/Data/log/host/Docker.log

# VM logs
tail -f ~/Library/Containers/com.docker.docker/Data/vms/0/console-ring
```

**Windows:**
```powershell
# Docker logs location
C:\Users\%USERNAME%\AppData\Local\Docker\log.txt

# View with PowerShell
Get-Content "$env:LOCALAPPDATA\Docker\log.txt" -Tail 50 -Wait
```

**Linux:**
```bash
# Docker Desktop logs
journalctl --user -u docker-desktop -f

# Docker daemon logs
journalctl -u docker -f
```

### Community Resources

- **Docker Forums**: https://forums.docker.com
- **Docker Community Slack**: https://dockercommunity.slack.com
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/docker
- **GitHub Issues**:
  - macOS: https://github.com/docker/for-mac/issues
  - Windows: https://github.com/docker/for-win/issues
  - Linux: https://github.com/docker/desktop-linux/issues

### Official Support

- **Docker Support**: https://www.docker.com/support
- **Documentation**: https://docs.docker.com
- **Release Notes**: https://docs.docker.com/desktop/release-notes/

## Prevention Best Practices

1. **Keep Docker Updated:**
   - Enable automatic updates
   - Check for updates weekly

2. **Regular Maintenance:**
```bash
   # Weekly cleanup
   docker system prune -a --volumes

   # Check resource usage
   docker system df
```

3. **Monitor Resources:**
   - Keep an eye on disk usage
   - Monitor CPU/memory usage
   - Ensure adequate free space

4. **Proper Shutdown:**
   - Always quit Docker Desktop properly
   - Don't force kill processes
   - Let Docker shutdown gracefully

5. **Backup Important Data:**
```bash
   # Export important images
   docker save -o backup.tar image:tag

   # Export volumes
   docker run --rm -v volume_name:/data -v $(pwd):/backup alpine tar czf /backup/volume_backup.tar.gz /data
```

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

# Restart Docker (varies by platform)
# See platform-specific sections above
```

### Emergency Reset

If all else fails:
```
Docker Desktop → Troubleshoot → Reset to factory defaults
```

**Warning**: This will delete:
- All containers
- All images
- All volumes
- All build cache
- All networks

Backup important data first!