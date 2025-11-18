#!/bin/bash
# QA Test Suite for Mula: The Root
# Tests frontend, backend, and integration

set -e  # Exit on error

echo "🧪 MULA: THE ROOT - QA TEST SUITE"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -n "Testing: $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "📦 1. CHECKING DEPENDENCIES"
echo "----------------------------"

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js not found"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓${NC} npm: $NPM_VERSION"
else
    echo -e "${RED}✗${NC} npm not found"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python not found"
    exit 1
fi

echo ""
echo "🎨 2. FRONTEND TESTS"
echo "----------------------------"

cd /workspaces/Astrology-Synthesis/frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠${NC} Installing dependencies..."
    npm install --silent
fi

# Test TypeScript compilation
echo -n "TypeScript compilation... "
if npx tsc --noEmit --skipLibCheck 2>&1 | grep -q "error"; then
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
else
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
fi

# Check critical files exist
echo -n "Fortune page exists... "
if [ -f "src/app/fortune/page.tsx" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "Consultant page exists... "
if [ -f "src/app/consultant/page.tsx" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "CardDraw component exists... "
if [ -f "src/components/fortune/CardDraw.tsx" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "Cosmic Midnight CSS exists... "
if [ -f "src/styles/variables.css" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Check CSS contains new design system
echo -n "Cosmic Midnight colors defined... "
if grep -q "bg-cosmic-dark" src/styles/variables.css; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Check fonts are configured
echo -n "Google Fonts configured... "
if grep -q "next/font/google" src/app/layout.tsx; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "🐍 3. BACKEND TESTS"
echo "----------------------------"

cd /workspaces/Astrology-Synthesis/backend

# Check Python files exist
echo -n "Consultant API exists... "
if [ -f "api/v1/consultant.py" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "Fortune API exists... "
if [ -f "api/v1/fortune.py" ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Check Python syntax
echo -n "Consultant API syntax... "
if python3 -m py_compile api/v1/consultant.py 2>/dev/null; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "Fortune API syntax... "
if python3 -m py_compile api/v1/fortune.py 2>/dev/null; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "Main app syntax... "
if python3 -m py_compile main.py 2>/dev/null; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Check routers are registered
echo -n "Consultant router registered... "
if grep -q "consultant_router" main.py; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "Fortune router registered... "
if grep -q "fortune_router" main.py; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "🔗 4. INTEGRATION TESTS"
echo "----------------------------"

# Check API endpoints are defined
echo -n "Consultant chat endpoint... "
if grep -q 'POST.*consultant/chat' api/v1/consultant.py; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "Fortune draw endpoint... "
if grep -q 'POST.*fortune/draw' api/v1/fortune.py; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Check frontend calls backend
cd /workspaces/Astrology-Synthesis/frontend
echo -n "Frontend calls consultant API... "
if grep -q "localhost:8000/api/v1/consultant/chat" src/app/consultant/page.tsx; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "📊 5. COMPONENT TESTS"
echo "----------------------------"

# Check CardDraw has all required methods
echo -n "CardDraw shuffle animation... "
if grep -q "handleDrawCard" src/components/fortune/CardDraw.tsx; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo -n "CardDraw CSS animations... "
if grep -q "@keyframes shuffle" src/components/fortune/CardDraw.css; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

# Check navigation links
echo -n "Fortune page navigation... "
if grep -q "window.location.href = '/consultant'" src/app/fortune/page.tsx; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "=================================="
echo "📈 TEST RESULTS"
echo "=================================="
echo -e "${GREEN}✓ Passed: $TESTS_PASSED${NC}"
echo -e "${RED}✗ Failed: $TESTS_FAILED${NC}"
echo "Total: $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    exit 1
fi
