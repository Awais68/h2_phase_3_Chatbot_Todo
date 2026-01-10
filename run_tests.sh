#!/bin/bash
# Run all Phase I tests with coverage reporting

set -e  # Exit on error

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "======================================"
echo "  Phase I Test Suite Runner"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Warning: Virtual environment not found at .venv${NC}"
    echo "Please create and activate virtual environment first"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source .venv/bin/activate

# Install test dependencies if not already installed
if ! python -c "import pytest" 2>/dev/null; then
    echo -e "${YELLOW}Installing test dependencies...${NC}"
    pip install -q pytest pytest-cov
fi

echo ""

# Run unit tests
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running Unit Tests${NC}"
echo -e "${BLUE}========================================${NC}"
pytest tests/unit/ -v --tb=short

echo ""

# Run integration tests
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Running Integration Tests${NC}"
echo -e "${BLUE}========================================${NC}"
pytest tests/integration/ -v --tb=short

echo ""

# Run all tests with coverage
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Full Test Suite with Coverage${NC}"
echo -e "${BLUE}========================================${NC}"
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Tests Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Coverage report saved to: htmlcov/index.html"
echo ""
