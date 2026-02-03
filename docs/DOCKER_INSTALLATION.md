# Docker Desktop Installation Guide

## Overview
This guide provides comprehensive instructions for installing and configuring Docker Desktop on all major platforms for the Todo AI Chatbot Kubernetes deployment.

## Table of Contents
- [System Requirements](#system-requirements)
- [Installation Instructions](#installation-instructions)
  - [macOS](#macos-installation)
  - [Windows](#windows-installation)
  - [Linux](#linux-installation)
- [Post-Installation Configuration](#post-installation-configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## System Requirements

### macOS
- **OS**: macOS 11 (Big Sur) or newer
- **Processor**: Apple Silicon (M1/M2/M3) or Intel processor
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 10GB free space minimum
- **Virtualization**: VT-x/AMD-v must be enabled

### Windows
- **OS**: Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
  - Or Windows 11 64-bit: Pro, Enterprise, or Education
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 10GB free space minimum
- **WSL 2**: Required (will be installed during setup)
- **Virtualization**: Hyper-V and Virtualization must be enabled in BIOS

### Linux
- **OS**: 64-bit Ubuntu 20.04+, Debian 11+, Fedora 35+, or other supported distribution
- **RAM**: 4GB minimum, 8GB recommended
- **Disk**: 10GB free space minimum
- **KVM**: KVM virtualization support required

## Installation Instructions

### macOS Installation

#### Step 1: Download Docker Desktop

**For Apple Silicon (M1/M2/M3):**
```bash
# Visit the download page
open https://desktop.docker.com/mac/main/arm64/Docker.dmg

# Or download directly
curl -L -o Docker.dmg https://desktop.docker.com/mac/main/arm64/Docker.dmg
```

**For Intel Macs:**
```bash
# Visit the download page
open https://desktop.docker.com/mac/main/amd64/Docker.dmg

# Or download directly
curl -L -o Docker.dmg https://desktop.docker.com/mac/main/amd64/Docker.dmg
```

#### Step 2: Install Docker Desktop

1. Open the downloaded `Docker.dmg` file
2. Drag the Docker icon to the Applications folder
3. Open Docker from Applications folder
4. Grant necessary permissions when prompted
5. Enter your password to allow Docker to install networking components

#### Step 3: Start Docker Desktop
```bash
# Launch Docker Desktop
open -a Docker

# Wait for Docker to start (you'll see the whale icon in the menu bar)
# The icon animation will stop when Docker is ready
```

#### Step 4: Verify Installation
```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Test Docker
docker run hello-world
```

### Windows Installation

#### Step 1: Enable WSL 2

**Using PowerShell (as Administrator):**
```powershell
# Enable WSL
wsl --install

# This will install WSL 2 and Ubuntu by default
# Restart your computer when prompted
```

**Manual WSL 2 Setup (if automatic install fails):**
```powershell
# Run as Administrator

# Enable Windows Subsystem for Linux
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine Platform
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart computer
Restart-Computer

# After restart, set WSL 2 as default
wsl --set-default-version 2

# Install Ubuntu (optional but recommended)
wsl --install -d Ubuntu
```

#### Step 2: Download Docker Desktop

1. Visit: https://docs.docker.com/desktop/install/windows-install/
2. Click "Download Docker Desktop for Windows"
3. Or use direct link: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

#### Step 3: Install Docker Desktop

1. Run the downloaded `Docker Desktop Installer.exe`
2. Ensure "Use WSL 2 instead of Hyper-V" is checked
3. Follow the installation wizard
4. Restart computer when installation completes

#### Step 4: Start Docker Desktop

1. Launch "Docker Desktop" from Start menu
2. Accept the service agreement
3. Wait for Docker to start (icon in system tray will stop animating)

#### Step 5: Verify Installation
```powershell
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Test Docker
docker run hello-world
```

### Linux Installation

#### Ubuntu/Debian Installation

**Step 1: Set up Docker's APT repository**
```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Step 2: Download Docker Desktop**
```bash
# For Ubuntu 22.04 (replace version as needed)
wget https://desktop.docker.com/linux/main/amd64/docker-desktop-4.25.0-amd64.deb

# Or visit: https://docs.docker.com/desktop/install/ubuntu/
```

**Step 3: Install Docker Desktop**
```bash
# Install the package
sudo apt-get update
sudo apt-get install ./docker-desktop-*-amd64.deb

# If there are dependency issues
sudo apt-get install -f
```

**Step 4: Start Docker Desktop**
```bash
# Start Docker Desktop
systemctl --user start docker-desktop

# Enable Docker Desktop to start on boot
systemctl --user enable docker-desktop

# Or launch from applications menu
```

**Step 5: Configure User Permissions**
```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Or log out and log back in
```

#### Fedora Installation
```bash
# Add Docker repository
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Download Docker Desktop RPM
wget https://desktop.docker.com/linux/main/amd64/docker-desktop-4.25.0-x86_64.rpm

# Install
sudo dnf install ./docker-desktop-4.25.0-x86_64.rpm

# Start Docker Desktop
systemctl --user start docker-desktop
```

## Post-Installation Configuration

### Allocate Resources

Docker Desktop needs adequate resources for Kubernetes deployment.

#### Recommended Settings:
- **CPUs**: 4 cores (minimum 2)
- **Memory**: 8GB (minimum 4GB)
- **Swap**: 2GB
- **Disk**: 60GB

#### Configuration Steps:

**macOS/Windows:**
1. Click Docker icon (menu bar/system tray)
2. Select "Settings" or "Preferences"
3. Navigate to "Resources" section
4. Adjust sliders:
   - CPUs: Set to 4 (or 2 minimum)
   - Memory: Set to 8192 MB (or 4096 MB minimum)
   - Swap: Set to 2048 MB
   - Disk image size: Set to 60 GB
5. Click "Apply & Restart"

**Linux:**
1. Open Docker Desktop application
2. Click Settings icon
3. Go to "Resources" tab
4. Adjust sliders as above
5. Click "Apply & Restart"

### Enable Kubernetes

Docker Desktop includes Kubernetes, which we'll use for local development.

#### Enable Steps:

1. Open Docker Desktop Settings
2. Navigate to "Kubernetes" tab
3. Check "Enable Kubernetes"
4. (Optional) Check "Show system containers (advanced)"
5. Click "Apply & Restart"
6. Wait 5-10 minutes for Kubernetes to initialize

#### Verify Kubernetes:
```bash
# Check if kubectl is available
kubectl version --client

# Check cluster info (after Kubernetes starts)
kubectl cluster-info

# Check nodes
kubectl get nodes
```

### Configure Docker CLI (Linux Only)

If you encounter permission errors:
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group membership
newgrp docker

# Or log out and log back in

# Verify
docker ps
# Should work without sudo
```

## Verification

### Automated Verification

Run our verification script:
```bash
# Make script executable
chmod +x scripts/verify-docker.sh

# Run verification
./scripts/verify-docker.sh
```

### Manual Verification

**Check Docker:**
```bash
# Version
docker --version
# Expected: Docker version 24.0.0 or higher

# Daemon status
docker info
# Should show server information

# Compose
docker compose version
# Expected: Docker Compose version v2.20.0 or higher
```

**Test Container Execution:**
```bash
# Run test container
docker run --rm hello-world
# Should print success message

# Run interactive container
docker run --rm -it alpine echo "Docker works!"
# Should print: Docker works!
```

**Check Resources:**
```bash
# View Docker system info
docker system df

# View running processes
docker ps

# View all containers
docker ps -a
```

**Check Kubernetes (if enabled):**
```bash
# Cluster info
kubectl cluster-info

# Nodes
kubectl get nodes

# System pods
kubectl get pods --all-namespaces
```

### Expected Verification Output
````
==========================================
Docker Desktop Verification Script
==========================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Checking Docker Installation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Docker is installed: Docker version 24.0.6, build ed223bc

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. Checking Docker Version
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Docker version: 24.0.6
✓ Docker version is adequate (24.0.0+)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. Checking Docker Daemon
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Docker daemon is running
ℹ Docker root directory: /var/lib/docker

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. Checking Docker Compose
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Docker Compose is available: v2.23.0
✓ Docker Compose version is adequate (2.20.0+)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. Testing Container Execution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ Running test container (hello-world)...
✓ Can run containers successfully

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. Checking Docker Resources
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ Available CPUs: 4
ℹ Available Memory: 8GB
✓ CPU allocation is adequate (4+ cores)
✓ Memory allocation is adequate (8GB+)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. Checking Kubernetes Support
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Kubernetes is available in Docker Desktop
ℹ kubectl is available
✓ Kubernetes is enabled and running
ℹ Kubernetes version: v1.28.2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. Checking Disk Space
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ Docker disk usage: 2.5GB
ℹ Available space: 45GB

==========================================
Verification Summary
==========================================
Passed:   11
Warnings: 0
Failed:   0

✓ Docker Desktop is properly installed and configured

Next steps:
  1. Ensure Kubernetes is enabled (if not already)
     Docker Desktop → Settings → Kubernetes → Enable Kubernetes
  2. Ensure at least 4GB RAM allocated (8GB recommended)
     Docker Desktop → Settings → Resources
  3. Proceed to Task P4-T002: Install Minikube if already requirement satistied don't run again like install docker desktop
```