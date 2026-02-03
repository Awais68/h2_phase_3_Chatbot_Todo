#!/bin/bash

# Docker Resources Configuration Script
# Purpose: Guide user through Docker Desktop resource configuration
# Author: Phase IV Deployment Team

echo "=========================================="
echo "Docker Desktop Resource Configuration"
echo "=========================================="
echo ""

echo "For Kubernetes deployment, we recommend:"
echo "  - CPUs: 4 cores (minimum 2)"
echo "  - Memory: 8GB (minimum 4GB)"
echo "  - Swap: 2GB"
echo "  - Disk: 60GB"
echo ""

echo "To configure these resources:"
echo ""
echo "macOS:"
echo "  1. Click Docker icon in menu bar"
echo "  2. Select 'Preferences' or 'Settings'"
echo "  3. Go to 'Resources' section"
echo "  4. Adjust sliders for CPU, Memory, Swap, Disk"
echo "  5. Click 'Apply & Restart'"
echo ""

echo "Windows:"
echo "  1. Click Docker icon in system tray"
echo "  2. Select 'Settings'"
echo "  3. Go to 'Resources' section"
echo "  4. Adjust sliders for CPU, Memory, Swap, Disk"
echo "  5. Click 'Apply & Restart'"
echo ""

echo "Linux:"
echo "  1. Open Docker Desktop application"
echo "  2. Click Settings icon"
echo "  3. Go to 'Resources' section"
echo "  4. Adjust sliders for CPU, Memory, Swap, Disk"
echo "  5. Click 'Apply & Restart'"
echo ""

echo "After configuring resources, run:"
echo "  ./scripts/verify-docker.sh"
echo ""