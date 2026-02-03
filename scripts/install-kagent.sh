#!/bin/bash

# scripts/install-kagent.sh
# Install Kagent binary

set -e

echo "Installing Kagent..."

# Determine OS and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case $ARCH in
    x86_64)
        ARCH="amd64"
        ;;
    aarch64|arm64)
        ARCH="arm64"
        ;;
esac

# Download URL
DOWNLOAD_URL="https://github.com/sozercan/kagent/releases/latest/download/kagent_${OS}_${ARCH}.tar.gz"

echo "Downloading Kagent for ${OS}/${ARCH}..."
curl -L -o kagent.tar.gz "$DOWNLOAD_URL"

# Extract
tar -xzf kagent.tar.gz

# Install to /usr/local/bin
sudo install kagent /usr/local/bin/kagent

# Clean up
rm kagent.tar.gz

# Verify installation
if command -v kagent &> /dev/null; then
    echo "Kagent installed successfully!"
    kagent version
else
    echo "Failed to install Kagent"
    exit 1
fi