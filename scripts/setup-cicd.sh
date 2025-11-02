#!/bin/bash
# GitHub Actions CI/CD Setup Script
# Creates GitHub Actions workflows for testing, building, and deploying

set -e

echo "🚀 GitHub Actions CI/CD Setup"
echo "=============================="

# Create .github/workflows directory
mkdir -p .github/workflows

echo "📝 Creating test workflow..."
cat > .github/workflows/test.yml << 'YAML_EOF'
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
        pip install pytest-cov
        pytest --cov=backend test_calculation_service.py test_auth_system.py -v
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        fail_ci_if_error: false
YAML_EOF

echo "✅ test.yml created"

echo "📝 Creating Docker build workflow..."
cat > .github/workflows/docker.yml << 'YAML_EOF'
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
      if: github.event_name == 'push'
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: ${{ github.event_name == 'push' }}
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/astrology-synthesis:latest
          ${{ secrets.DOCKER_USERNAME }}/astrology-synthesis:${{ github.sha }}
        cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/astrology-synthesis:buildcache
        cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/astrology-synthesis:buildcache,mode=max
YAML_EOF

echo "✅ docker.yml created"

echo "📝 Creating deployment workflow..."
cat > .github/workflows/deploy.yml << 'YAML_EOF'
name: Deploy to Production

on:
  push:
    tags: [ 'v*' ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy notification
      run: |
        echo "🚀 Deploying version: ${{ github.ref }}"
        echo "Deployment steps:"
        echo "1. Pull latest Docker image"
        echo "2. Stop current container"
        echo "3. Start new container"
        echo "4. Run health checks"
        echo "5. Update DNS/Load balancer"
    
    - name: Health check
      run: |
        echo "Waiting for service to be ready..."
        sleep 5
        echo "✅ Health check would go here"
YAML_EOF

echo "✅ deploy.yml created"

# List created files
echo ""
echo "✅ CI/CD workflows created:"
ls -la .github/workflows/

echo ""
echo "📋 Next steps:"
echo "1. Push code to GitHub: git push origin master"
echo "2. Go to GitHub repository Settings > Secrets"
echo "3. Add these secrets:"
echo "   - DOCKER_USERNAME: your Docker Hub username"
echo "   - DOCKER_PASSWORD: your Docker Hub token"
echo "   - JWT_SECRET_KEY: generated key"
echo "   - DB_PASSWORD: generated password"
echo ""
echo "Generate secrets with:"
echo "  JWT: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
echo "  DB:  python -c \"import secrets; print(secrets.token_urlsafe(16))\""

