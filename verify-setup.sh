#!/bin/bash

# Astrology Synthesis - Setup Verification Script
# This script verifies that the development environment is properly set up

set -e

echo "🔍 Astrology Synthesis - Setup Verification"
echo "============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
ALL_CHECKS_PASSED=true

# Function to print success
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print error
print_error() {
    echo -e "${RED}✗${NC} $1"
    ALL_CHECKS_PASSED=false
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "📋 Checking Prerequisites..."
echo "----------------------------"

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js installed: $NODE_VERSION"
else
    print_error "Node.js not found. Please install Node.js 18+"
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_success "npm installed: $NPM_VERSION"
else
    print_error "npm not found"
fi

# Check PostgreSQL
if command -v psql &> /dev/null; then
    PSQL_VERSION=$(psql --version)
    print_success "PostgreSQL installed: $PSQL_VERSION"
else
    print_warning "PostgreSQL not found. Install if you plan to use the database"
fi

# Check Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    print_success "Git installed: $GIT_VERSION"
else
    print_error "Git not found"
fi

echo ""
echo "📂 Checking Project Structure..."
echo "--------------------------------"

# Check backend
if [ -d "backend" ] && [ -f "backend/package.json" ]; then
    print_success "Backend directory exists"
else
    print_error "Backend directory or package.json missing"
fi

# Check frontend
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    print_success "Frontend directory exists"
else
    print_error "Frontend directory or package.json missing"
fi

# Check database
if [ -d "database" ] && [ -f "database/init.sql" ]; then
    print_success "Database directory and init.sql exist"
else
    print_error "Database directory or init.sql missing"
fi

echo ""
echo "📦 Checking Dependencies..."
echo "--------------------------"

# Check backend node_modules
if [ -d "backend/node_modules" ]; then
    print_success "Backend dependencies installed"
else
    print_warning "Backend dependencies not installed. Run: cd backend && npm install"
fi

# Check frontend node_modules
if [ -d "frontend/node_modules" ]; then
    print_success "Frontend dependencies installed"
else
    print_warning "Frontend dependencies not installed. Run: cd frontend && npm install"
fi

echo ""
echo "⚙️  Checking Environment Files..."
echo "---------------------------------"

# Check backend .env
if [ -f "backend/.env" ]; then
    print_success "Backend .env file exists"
else
    print_warning "Backend .env not found. Copy from backend/.env.example"
fi

# Check frontend .env.local
if [ -f "frontend/.env.local" ]; then
    print_success "Frontend .env.local file exists"
else
    print_warning "Frontend .env.local not found. Copy from frontend/.env.local.example"
fi

echo ""
echo "🧪 Running Tests..."
echo "------------------"

# Test backend
if [ -d "backend/node_modules" ]; then
    echo "Running backend tests..."
    cd backend
    if npm test &> /dev/null; then
        print_success "Backend tests passed"
    else
        print_error "Backend tests failed"
    fi
    cd ..
fi

# Test frontend
if [ -d "frontend/node_modules" ]; then
    echo "Running frontend tests..."
    cd frontend
    if npm test -- --passWithNoTests &> /dev/null; then
        print_success "Frontend tests passed"
    else
        print_error "Frontend tests failed"
    fi
    cd ..
fi

echo ""
echo "🔧 Checking Build Configuration..."
echo "----------------------------------"

# Check TypeScript configs
if [ -f "backend/tsconfig.json" ]; then
    print_success "Backend TypeScript config exists"
else
    print_error "Backend tsconfig.json missing"
fi

if [ -f "frontend/tsconfig.json" ]; then
    print_success "Frontend TypeScript config exists"
else
    print_error "Frontend tsconfig.json missing"
fi

# Check linting configs
if [ -f "backend/.eslintrc.json" ]; then
    print_success "Backend ESLint config exists"
else
    print_error "Backend .eslintrc.json missing"
fi

if [ -f "frontend/eslint.config.mjs" ]; then
    print_success "Frontend ESLint config exists"
else
    print_error "Frontend ESLint config missing"
fi

echo ""
echo "📚 Checking Documentation..."
echo "---------------------------"

DOCS=("README.md" "CONTRIBUTING.md" "DEVELOPMENT.md" "DATABASE_SCHEMA.md" "SETUP_SUMMARY.md")

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        print_success "$doc exists"
    else
        print_error "$doc missing"
    fi
done

echo ""
echo "============================================="

if [ "$ALL_CHECKS_PASSED" = true ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "🚀 Next steps:"
    echo "  1. Start backend:  cd backend && npm run dev"
    echo "  2. Start frontend: cd frontend && npm run dev"
    echo "  3. Visit: http://localhost:3000"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some checks failed.${NC}"
    echo ""
    echo "📖 Please review the errors above and:"
    echo "  1. Read DEVELOPMENT.md for setup instructions"
    echo "  2. Install missing dependencies"
    echo "  3. Run this script again to verify"
    echo ""
    exit 1
fi
