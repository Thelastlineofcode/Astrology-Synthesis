#!/bin/bash

# E2E Test Runner Script
# Usage: ./run-e2e-tests.sh [browser] [test-file]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║       Mula: The Root E2E Test Suite         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend" || exit 1

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    npm install
fi

# Check if Playwright browsers are installed
if [ ! -d "$HOME/.cache/ms-playwright" ]; then
    echo -e "${YELLOW}Installing Playwright browsers...${NC}"
    npx playwright install --with-deps
fi

# Parse arguments
BROWSER=${1:-chromium}
TEST_FILE=${2:-}

echo -e "${GREEN}Browser:${NC} $BROWSER"
if [ -n "$TEST_FILE" ]; then
    echo -e "${GREEN}Test file:${NC} $TEST_FILE"
else
    echo -e "${GREEN}Running:${NC} All tests"
fi
echo ""

# Check if dev server is running
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Dev server not detected on http://localhost:3000${NC}"
    echo -e "${YELLOW}Starting dev server in background...${NC}"
    npm run dev > /dev/null 2>&1 &
    DEV_SERVER_PID=$!
    
    # Wait for server to start
    echo -e "${YELLOW}Waiting for dev server to start...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Dev server started${NC}"
            break
        fi
        sleep 1
    done
    
    # Cleanup function
    cleanup() {
        if [ -n "$DEV_SERVER_PID" ]; then
            echo -e "${YELLOW}Stopping dev server...${NC}"
            kill $DEV_SERVER_PID 2>/dev/null || true
        fi
    }
    trap cleanup EXIT
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Running E2E Tests...${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Run tests
if [ -n "$TEST_FILE" ]; then
    npx playwright test "$TEST_FILE" --project="$BROWSER" --reporter=list,html
else
    npx playwright test --project="$BROWSER" --reporter=list,html
fi

TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}✗ Some tests failed${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
fi

echo ""
echo -e "${GREEN}Test report available at:${NC} playwright-report/index.html"
echo -e "${GREEN}To view report, run:${NC} npx playwright show-report"
echo ""

exit $TEST_EXIT_CODE
