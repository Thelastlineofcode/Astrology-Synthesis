#!/bin/bash
# Docker Setup Script for Astrology Synthesis
# Sets up containerization with Dockerfile and docker-compose

set -e  # Exit on error

echo "🐳 Docker Setup for Astrology Synthesis"
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not installed. Please install Docker Desktop."
    exit 1
fi

echo "✅ Docker found: $(docker --version)"

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not installed. Installing..."
    # This is usually bundled with Docker Desktop now
    docker compose version || (echo "Please install Docker Compose" && exit 1)
fi

echo "✅ Docker Compose found"

# Create Dockerfile
echo "📝 Creating Dockerfile..."
cat > Dockerfile << 'DOCKERFILE_EOF'
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
DOCKERFILE_EOF

echo "✅ Dockerfile created"

# Create docker-compose.yml
echo "📝 Creating docker-compose.yml..."
cat > docker-compose.yml << 'COMPOSE_EOF'
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
COMPOSE_EOF

echo "✅ docker-compose.yml created"

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t astrology-synthesis:latest .

echo "✅ Docker image built successfully"

# Test the build
echo "🧪 Testing Docker image..."
docker run --rm --health-cmd="curl -f http://localhost:8000/health" \
    -p 8000:8000 \
    -e DATABASE_URL=sqlite:///./test.db \
    astrology-synthesis:latest &

CONTAINER_PID=$!
sleep 5

# Check if container is running
if docker ps | grep -q astrology-synthesis; then
    echo "✅ Container started successfully"
    docker stop $(docker ps -q --filter ancestor=astrology-synthesis:latest) || true
else
    echo "⚠️  Container failed to start, but image was built"
    kill $CONTAINER_PID 2>/dev/null || true
fi

echo ""
echo "✅ Docker setup complete!"
echo ""
echo "Next steps:"
echo "1. Start the stack: docker-compose up -d"
echo "2. Check status: docker-compose ps"
echo "3. View logs: docker-compose logs -f api"
echo "4. Stop: docker-compose down"

