# Agent 1: Phase 3 Finalization - Docker & CI/CD Implementation Guide

**Agent Role:** Finalization & Deployment Agent  
**Duration:** 3-4 hours  
**Target Completion:** By end of November 3, 2025

---

## 🎯 Mission

Transform the production-ready core system into a containerized, automatically-tested, deployable application.

**Deliverables:**
- ✅ Working Dockerfile
- ✅ docker-compose.yml for local development
- ✅ GitHub Actions CI/CD workflows
- ✅ Performance validation scripts
- ✅ Deployment documentation

---

## 📋 Pre-Flight Checklist (5 minutes)

Before starting, verify:

```bash
# 1. Check project structure
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis
ls -la | grep -E "backend|tests|requirements"

# 2. Verify tests pass
source .venv/bin/activate
pytest test_calculation_service.py test_auth_system.py -v --tb=no

# 3. Check Python version
python --version  # Should be 3.11+

# 4. Verify git is ready
git status
```

**Expected:** All tests passing, clean working directory

---

## 🐳 Task 1: Docker Containerization (1-2 hours)

### Step 1.1: Create Dockerfile

**Location:** `/Dockerfile` (project root)

```dockerfile
# Base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Action:** Create the file:
```bash
cat > Dockerfile << 'DOCKERFILE_EOF'
# [paste content above]
DOCKERFILE_EOF
```

### Step 1.2: Create docker-compose.yml

**Location:** `/docker-compose.yml` (project root)

```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: astrology-synthesis-api
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - DATABASE_URL=sqlite:///./astrology.db
      - JWT_SECRET_KEY=${JWT_SECRET_KEY:-change-me-in-production}
    volumes:
      - ./backend:/app/backend
      - ./astrology.db:/app/astrology.db
    command: python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:14-alpine
    container_name: astrology-synthesis-db
    environment:
      - POSTGRES_USER=astrology
      - POSTGRES_PASSWORD=${DB_PASSWORD:-dev-password}
      - POSTGRES_DB=astrology_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U astrology"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

**Action:** Create the file:
```bash
cat > docker-compose.yml << 'COMPOSE_EOF'
# [paste content above]
COMPOSE_EOF
```

### Step 1.3: Build and Test Docker Image

```bash
# Build image
docker build -t astrology-synthesis:latest .

# Verify build succeeded
docker images | grep astrology-synthesis

# Test image runs
docker run --rm -p 8000:8000 astrology-synthesis:latest &

# Wait for startup
sleep 5

# Test health endpoint
curl -v http://localhost:8000/health

# Kill container
docker stop $(docker ps -q --filter ancestor=astrology-synthesis:latest)
```

**Expected Output:**
```
Successfully tagged astrology-synthesis:latest
{"status": "ok"}
```

### Step 1.4: Test docker-compose

```bash
# Start stack
docker-compose up -d

# Check services
docker-compose ps

# Check logs
docker-compose logs -f api

# Test API
curl http://localhost:8000/health

# Stop stack
docker-compose down
```

**Deliverable Checklist:**
- [ ] Dockerfile created and builds successfully
- [ ] docker-compose.yml created
- [ ] Image runs and responds to health checks
- [ ] Services start/stop cleanly with docker-compose

---

## 🚀 Task 2: CI/CD Pipeline Setup (1-2 hours)

### Step 2.1: Create GitHub Actions Directory

```bash
mkdir -p .github/workflows
```

### Step 2.2: Create Testing Workflow

**File:** `.github/workflows/test.yml`

```yaml
name: Tests

on:
  push:
    branches: [ master, develop ]
  pull_request:
    branches: [ master, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest test_calculation_service.py test_auth_system.py test_app_functionality.py -v --tb=short
    
    - name: Generate coverage
      run: |
        pytest --cov=backend test_calculation_service.py test_auth_system.py -v
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
```

**Action:** Create file:
```bash
cat > .github/workflows/test.yml << 'YAML_EOF'
# [paste content above]
YAML_EOF
```

### Step 2.3: Create Docker Build Workflow

**File:** `.github/workflows/docker.yml`

```yaml
name: Docker Build

on:
  push:
    branches: [ master ]
    tags: [ 'v*' ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/astrology-synthesis:latest
          ${{ secrets.DOCKER_USERNAME }}/astrology-synthesis:${{ github.sha }}
        cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/astrology-synthesis:buildcache
        cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/astrology-synthesis:buildcache,mode=max
```

**Action:** Create file:
```bash
cat > .github/workflows/docker.yml << 'YAML_EOF'
# [paste content above]
YAML_EOF
```

### Step 2.4: Create Deployment Workflow

**File:** `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    tags: [ 'v*' ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deployment steps:"
        echo "1. Pull latest image from Docker Hub"
        echo "2. Stop current container"
        echo "3. Start new container"
        echo "4. Run health checks"
        echo "5. Update DNS/Load balancer if needed"
    
    - name: Health check
      run: |
        echo "Pinging deployed service..."
        curl -f https://api.example.com/health || exit 1
```

**Action:** Create file:
```bash
cat > .github/workflows/deploy.yml << 'YAML_EOF'
# [paste content above]
YAML_EOF
```

### Step 2.5: Configure GitHub Secrets

In GitHub repository settings, add secrets:

```
DOCKER_USERNAME: [your Docker Hub username]
DOCKER_PASSWORD: [your Docker Hub token]
JWT_SECRET_KEY: [generate a secure key]
DB_PASSWORD: [generate a secure password]
```

**How to generate secrets:**
```bash
# Generate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate DB password
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

### Step 2.6: Test Workflows Locally

Install act to test GitHub Actions locally:

```bash
# Install act
brew install act

# Run tests workflow
act -j test

# Run docker workflow
act -j build
```

**Deliverable Checklist:**
- [ ] .github/workflows/test.yml created
- [ ] .github/workflows/docker.yml created
- [ ] .github/workflows/deploy.yml created
- [ ] GitHub secrets configured
- [ ] Workflows pass when pushed

---

## ⚡ Task 3: Performance Validation (1-2 hours)

### Step 3.1: Create Performance Test Script

**File:** `scripts/performance_test.py`

```python
#!/usr/bin/env python
"""Performance validation script."""

import time
import requests
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
BASE_URL = "http://localhost:8000"
ENDPOINTS = [
    "/health",
    "/api/v1/auth/login",  # Will fail auth but measures endpoint speed
]
NUM_REQUESTS = 100
NUM_THREADS = 10

def test_endpoint(url: str) -> float:
    """Test single endpoint, return response time in ms."""
    start = time.time()
    try:
        response = requests.get(url, timeout=5)
        elapsed_ms = (time.time() - start) * 1000
        return elapsed_ms
    except Exception as e:
        print(f"Error: {e}")
        return None

def run_performance_test():
    """Run performance validation."""
    print(f"Performance Test: {NUM_REQUESTS} requests per endpoint")
    print(f"Threads: {NUM_THREADS}")
    print("=" * 60)
    
    for endpoint in ENDPOINTS:
        url = f"{BASE_URL}{endpoint}"
        print(f"\nTesting: {endpoint}")
        
        times = []
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = [executor.submit(test_endpoint, url) for _ in range(NUM_REQUESTS)]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    times.append(result)
        
        if times:
            avg = statistics.mean(times)
            p95 = sorted(times)[int(len(times) * 0.95)]
            p99 = sorted(times)[int(len(times) * 0.99)]
            
            print(f"  Avg:     {avg:.2f}ms")
            print(f"  P95:     {p95:.2f}ms")
            print(f"  P99:     {p99:.2f}ms")
            print(f"  Min:     {min(times):.2f}ms")
            print(f"  Max:     {max(times):.2f}ms")
            
            # Validate SLA
            if p95 < 500:
                print("  ✅ SLA PASS (P95 < 500ms)")
            else:
                print("  ❌ SLA FAIL (P95 >= 500ms)")

if __name__ == "__main__":
    run_performance_test()
```

**Action:** Create script:
```bash
mkdir -p scripts
cat > scripts/performance_test.py << 'PYTHON_EOF'
# [paste content above]
PYTHON_EOF
chmod +x scripts/performance_test.py
```

### Step 3.2: Create Load Test Script

**File:** `scripts/load_test.sh`

```bash
#!/bin/bash
# Load testing script using Apache Bench

API_URL="http://localhost:8000/health"
NUM_REQUESTS=1000
CONCURRENCY=50

echo "Load Test Configuration:"
echo "URL: $API_URL"
echo "Requests: $NUM_REQUESTS"
echo "Concurrency: $CONCURRENCY"
echo "================================"

# Check if ab is installed
if ! command -v ab &> /dev/null; then
    echo "Apache Bench not found. Installing..."
    brew install httpd  # macOS
    # For Linux: sudo apt-get install apache2-utils
fi

# Run load test
ab -n $NUM_REQUESTS -c $CONCURRENCY -q $API_URL

echo ""
echo "Load test complete!"
```

**Action:** Create script:
```bash
cat > scripts/load_test.sh << 'BASH_EOF'
# [paste content above]
BASH_EOF
chmod +x scripts/load_test.sh
```

### Step 3.3: Run Performance Tests

```bash
# Start API in background
docker-compose up -d api
sleep 5

# Run performance test
python scripts/performance_test.py

# Run load test
bash scripts/load_test.sh

# Stop API
docker-compose down
```

**Expected Results:**
```
Performance Test: 100 requests per endpoint
Threads: 10
============================================================

Testing: /health
  Avg:     45.23ms
  P95:     78.45ms
  P99:     95.12ms
  Min:     12.34ms
  Max:     156.78ms
  ✅ SLA PASS (P95 < 500ms)
```

**Deliverable Checklist:**
- [ ] Performance test script created and runs
- [ ] Load test script created and runs
- [ ] P95 latency < 500ms ✅
- [ ] Throughput > 100 req/s ✅
- [ ] No errors in results ✅

---

## 📚 Verification Checklist

### Docker
- [ ] Dockerfile builds without errors
- [ ] Image runs successfully
- [ ] Health checks pass
- [ ] docker-compose starts all services
- [ ] Services communicate correctly

### CI/CD
- [ ] GitHub Actions workflows created
- [ ] Workflows execute on push
- [ ] Tests run automatically
- [ ] Docker image builds in CI/CD
- [ ] Deployment workflow configured

### Performance
- [ ] API responds in <500ms (P95)
- [ ] Can handle 100+ concurrent requests
- [ ] No errors under load
- [ ] Health checks pass consistently

### Documentation
- [ ] Dockerfile documented
- [ ] docker-compose.yml documented
- [ ] CI/CD workflows documented
- [ ] Performance results recorded

---

## 🎯 Final Validation

```bash
# 1. Verify all files created
ls -la Dockerfile docker-compose.yml .github/workflows/

# 2. Run complete test suite
docker-compose up -d
pytest -v
docker-compose down

# 3. Verify git status
git status

# 4. Commit changes
git add .
git commit -m "Phase 3 Final: Docker, CI/CD, and performance validation"
git push origin master
```

---

## 📞 Troubleshooting

### Docker build fails
```bash
# Check Docker version
docker --version

# Rebuild with no cache
docker build --no-cache -t astrology-synthesis:latest .
```

### Tests fail in Docker
```bash
# Run with verbose output
docker-compose run api pytest -vvv

# Check logs
docker-compose logs api
```

### Performance tests show high latency
```bash
# Check CPU/Memory
docker stats

# Verify no other services using ports
lsof -i :8000

# Increase Docker resources in Docker Desktop settings
```

---

## ✅ Success Criteria

- [x] Docker image builds successfully
- [x] docker-compose runs all services
- [x] GitHub Actions workflows execute
- [x] Tests pass automatically on push
- [x] Performance meets SLA (P95 <500ms)
- [x] Load testing passes (100+ req/s)
- [x] All documentation complete

**Expected Completion Time:** 3-4 hours  
**Difficulty Level:** Medium  
**Success Rate:** High (all prerequisites complete)

---

**Next Step:** Commit to GitHub and pass to Phase 4 Knowledge Base Agent

