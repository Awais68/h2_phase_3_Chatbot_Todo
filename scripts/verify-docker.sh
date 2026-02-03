#!/bin/bash

# Docker Desktop Verification Script
# Purpose: Verify Docker Desktop installation and configuration
# Author: Phase IV Deployment Team
# Date: 2024

set -e

echo "=========================================="
echo "Docker Desktop Verification Script"
echo "=========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Function to print success
print_success() {
    echo -e "${GREEN}✓${NC} $1"
    PASSED=$((PASSED + 1))
}

# Function to print error
print_error() {
    echo -e "${RED}✗${NC} $1"
    FAILED=$((FAILED + 1))
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

# Function to print info
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check 1: Docker Installation
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Checking Docker Installation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_success "Docker is installed: $DOCKER_VERSION"
else
    print_error "Docker is not installed"
    echo ""
    echo "Installation instructions:"
    echo "  macOS:   https://docs.docker.com/desktop/install/mac-install/"
    echo "  Windows: https://docs.docker.com/desktop/install/windows-install/"
    echo "  Linux:   https://docs.docker.com/desktop/install/linux-install/"
    echo ""
    exit 1
fi

# Check 2: Docker Version
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. Checking Docker Version"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DOCKER_VERSION_NUMBER=$(docker version --format '{{.Server.Version}}' 2>/dev/null || echo "")

if [ -n "$DOCKER_VERSION_NUMBER" ]; then
    print_success "Docker version: $DOCKER_VERSION_NUMBER"

    # Check if version is adequate (24.0.0+)
    MAJOR_VERSION=$(echo $DOCKER_VERSION_NUMBER | cut -d. -f1)
    MINOR_VERSION=$(echo $DOCKER_VERSION_NUMBER | cut -d. -f2)

    if [ "$MAJOR_VERSION" -ge 24 ]; then
        print_success "Docker version is adequate (24.0.0+)"
    else
        print_warning "Docker version should be 24.0.0 or higher"
        echo "  Current: $DOCKER_VERSION_NUMBER"
        echo "  Please update Docker Desktop"
    fi
else
    print_error "Cannot determine Docker version. Is Docker daemon running?"
    echo "  Please start Docker Desktop application"
    exit 1
fi

# Check 3: Docker Daemon Status
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. Checking Docker Daemon"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if docker info &> /dev/null; then
    print_success "Docker daemon is running"

    # Get daemon info
    DOCKER_ROOT=$(docker info --format '{{.DockerRootDir}}' 2>/dev/null)
    print_info "Docker root directory: $DOCKER_ROOT"
else
    print_error "Docker daemon is not running"
    echo ""
    echo "Please start Docker Desktop:"
    echo "  macOS:   Open Docker from Applications"
    echo "  Windows: Open Docker Desktop from Start menu"
    echo "  Linux:   Run 'systemctl --user start docker-desktop'"
    echo ""
    exit 1
fi

# Check 4: Docker Compose
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. Checking Docker Compose"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version --short)
    print_success "Docker Compose is available: v$COMPOSE_VERSION"

    # Check version (should be 2.20.0+)
    COMPOSE_MAJOR=$(echo $COMPOSE_VERSION | cut -d. -f1)
    COMPOSE_MINOR=$(echo $COMPOSE_VERSION | cut -d. -f2)

    if [ "$COMPOSE_MAJOR" -ge 2 ] && [ "$COMPOSE_MINOR" -ge 20 ]; then
        print_success "Docker Compose version is adequate (2.20.0+)"
    else
        print_warning "Docker Compose should be version 2.20.0 or higher"
    fi
else
    print_error "Docker Compose is not available"
    echo "  Please update Docker Desktop to get latest Compose"
    exit 1
fi

# Check 5: Container Execution Test
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. Testing Container Execution"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

print_info "Running test container (hello-world)..."
if docker run --rm hello-world &> /dev/null; then
    print_success "Can run containers successfully"
else
    print_error "Cannot run containers"
    echo "  This may indicate a permissions or configuration issue"
    exit 1
fi

# Check 6: Docker Resources
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. Checking Docker Resources"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Get system info
TOTAL_MEMORY=$(docker info --format '{{.MemTotal}}' 2>/dev/null)
CPUS=$(docker info --format '{{.NCPU}}' 2>/dev/null)

if [ -n "$TOTAL_MEMORY" ] && [ -n "$CPUS" ]; then
    # Convert memory to GB
    MEMORY_GB=$((TOTAL_MEMORY / 1024 / 1024 / 1024))

    print_info "Available CPUs: $CPUS"
    print_info "Available Memory: ${MEMORY_GB}GB"

    # Check if resources are adequate
    if [ "$CPUS" -ge 4 ]; then
        print_success "CPU allocation is adequate (4+ cores)"
    else
        print_warning "Consider allocating at least 4 CPUs in Docker Desktop settings"
        echo "  Current: $CPUS CPUs"
        echo "  Recommended: 4+ CPUs"
    fi

    if [ "$MEMORY_GB" -ge 8 ]; then
        print_success "Memory allocation is adequate (8GB+)"
    elif [ "$MEMORY_GB" -ge 4 ]; then
        print_warning "Memory allocation is minimal (4GB)"
        echo "  Current: ${MEMORY_GB}GB"
        echo "  Recommended: 8GB+"
    else
        print_error "Insufficient memory allocation"
        echo "  Current: ${MEMORY_GB}GB"
        echo "  Minimum required: 4GB"
        echo "  Recommended: 8GB+"
    fi
fi

# Check 7: Kubernetes Support
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. Checking Kubernetes Support"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Capture docker info output to avoid multiple calls and exit on grep failure
DOCKER_INFO_OUTPUT=$(docker info 2>/dev/null)
if echo "$DOCKER_INFO_OUTPUT" | grep -qi "kubernetes"; then
    print_success "Kubernetes is available in Docker Desktop"

    # Check if Kubernetes is enabled
    if kubectl version --client &> /dev/null; then
        print_info "kubectl is available"

        # Try to get cluster info
        if kubectl cluster-info &> /dev/null; then
            print_success "Kubernetes is enabled and running"
            K8S_VERSION=$(kubectl version --client -o json 2>/dev/null | grep -o '"gitVersion":"[^"]*' | cut -d'"' -f4 || echo "unknown")
            print_info "Kubernetes version: $K8S_VERSION"
        else
            print_warning "Kubernetes is available but not enabled"
            echo "  Enable in: Docker Desktop → Settings → Kubernetes → Enable Kubernetes"
        fi
    else
        print_warning "kubectl not found"
        echo "  Install kubectl or enable Kubernetes in Docker Desktop"
    fi
else
    print_warning "Kubernetes support not detected"
    echo "  This is required for Phase IV deployment"
    echo "  Enable in: Docker Desktop → Settings → Kubernetes"
fi

# Check 8: Disk Space
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "8. Checking Disk Space"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DISK_USAGE=$(docker system df --format "{{.Size}}" 2>/dev/null | head -1 || echo "unknown")
print_info "Docker disk usage: $DISK_USAGE"

# Get available space on Docker root
if command -v df &> /dev/null && [ -n "$DOCKER_ROOT" ]; then
    AVAILABLE_SPACE=$(df -h "$DOCKER_ROOT" 2>/dev/null | awk 'NR==2 {print $4}' || echo "unknown")
    print_info "Available space: $AVAILABLE_SPACE"
fi

# Summary
echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "${GREEN}Passed:${NC}   $PASSED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo -e "${RED}Failed:${NC}   $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Docker Desktop is properly installed and configured${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Ensure Kubernetes is enabled (if not already)"
    echo "     Docker Desktop → Settings → Kubernetes → Enable Kubernetes"
    echo "  2. Ensure at least 4GB RAM allocated (8GB recommended)"
    echo "     Docker Desktop → Settings → Resources"
    echo "  3. Proceed to Task P4-T002: Install Minikube"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Docker Desktop verification failed${NC}"
    echo ""
    echo "Please fix the errors above before proceeding."
    echo "See docs/TROUBLESHOOTING_DOCKER.md for help."
    echo ""
    exit 1
fi