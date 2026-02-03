# Kagent Setup Guide

## Overview
Kagent is an AI-powered Kubernetes assistant that helps with cluster management, health analysis, and troubleshooting.

## Installation

### Prerequisites
- kubectl installed and configured
- OpenAI API key
- Internet access

### Installation Steps

1. Run the installation script:
```bash
chmod +x scripts/install-kagent.sh
./scripts/install-kagent.sh
```

2. Verify installation:
```bash
kagent version
```

## Configuration

1. Copy the environment template:
```bash
cp .env.kagent.example .env.kagent
```

2. Edit `.env.kagent` and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

3. Run the configuration script:
```bash
chmod +x scripts/configure-kagent.sh
./scripts/configure-kagent.sh
```

## Verification

Run the verification script:
```bash
chmod +x scripts/verify-kagent.sh
./scripts/verify-kagent.sh
```

## Usage

Once configured, you can use Kagent to analyze your cluster:
```bash
kagent analyze
```

## Troubleshooting

### Kagent command not found
- Ensure it's installed in your PATH
- Check if installation was successful

### API key issues
- Verify your OpenAI API key is valid
- Check that the key is properly set in environment