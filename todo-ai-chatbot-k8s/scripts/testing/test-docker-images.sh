#!/bin/bash

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0

echo "====================================="
echo "Docker Images Test Suite"
echo "====================================="
echo ""

# Test backend
echo -e "${YELLOW}Testing Backend Container...${NC}"
if ./scripts/testing/test-backend-container.sh; then
    echo -e "${GREEN}✓ Backend tests passed${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Backend tests failed${NC}"
    ((FAILED++))
fi
echo ""

# Test MCP server
echo -e "${YELLOW}Testing MCP Server Container...${NC}"
if ./scripts/testing/test-mcp-container.sh; then
    echo -e "${GREEN}✓ MCP tests passed${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ MCP tests failed${NC}"
    ((FAILED++))
fi
echo ""

# Test frontend
echo -e "${YELLOW}Testing Frontend Container...${NC}"
if ./scripts/testing/test-frontend-container.sh; then
    echo -e "${GREEN}✓ Frontend tests passed${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Frontend tests failed${NC}"
    ((FAILED++))
fi
echo ""

# Integration tests
echo -e "${YELLOW}Testing Integration...${NC}"
if ./scripts/testing/test-integration.sh; then
    echo -e "${GREEN}✓ Integration tests passed${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Integration tests failed${NC}"
    ((FAILED++))
fi
echo ""

# Summary
echo "====================================="
echo "Test Summary"
echo "====================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! Ready for Kubernetes deployment.${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Please fix before deploying.${NC}"
    exit 1
fi