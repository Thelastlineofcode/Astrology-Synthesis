#!/bin/bash

set -e

echo "🚀 Astrology Synthesis Deployment Script"
echo "=========================================="

# Configuration
COMPOSE_FILE="docker-compose.yml"
DB_WAIT_TIME=30
HEALTH_CHECK_INTERVAL=2
MAX_HEALTH_CHECKS=30

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}ℹ️  $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    log_success "Docker found"
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    log_success "Docker Compose found"
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_error "docker-compose.yml not found"
        exit 1
    fi
    log_success "docker-compose.yml found"
}

# Build images
build_images() {
    log_info "Building Docker images..."
    docker-compose build
    log_success "Images built successfully"
}

# Start services
start_services() {
    log_info "Starting services..."
    docker-compose up -d
    log_success "Services started"
}

# Wait for database (if using PostgreSQL)
wait_for_database() {
    if grep -q "postgres" "$COMPOSE_FILE"; then
        log_info "Waiting for database to be ready..."
        
        local attempt=0
        while [ $attempt -lt 30 ]; do
            if docker-compose exec -T postgres pg_isready -U astrology_user > /dev/null 2>&1; then
                log_success "Database is ready"
                return 0
            fi
            attempt=$((attempt + 1))
            sleep 2
        done
        
        log_error "Database failed to start"
        return 1
    fi
}

# Initialize database
init_database() {
    log_info "Initializing database..."
    
    # Run migrations/initialization (if applicable)
    if [ -f "database/init.sql" ]; then
        if grep -q "postgres" "$COMPOSE_FILE"; then
            docker-compose exec -T postgres psql -U astrology_user -d astrology_db -f /app/database/init.sql || true
            log_success "Database initialized from init.sql"
        fi
    fi
}

# Health check
health_check() {
    log_info "Performing health checks..."
    
    local attempt=0
    while [ $attempt -lt $MAX_HEALTH_CHECKS ]; do
        RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")
        
        if [ "$RESPONSE" = "200" ]; then
            log_success "API health check passed"
            return 0
        fi
        
        attempt=$((attempt + 1))
        if [ $attempt -lt $MAX_HEALTH_CHECKS ]; then
            sleep $HEALTH_CHECK_INTERVAL
        fi
    done
    
    log_error "API failed health check"
    return 1
}

# Show deployment summary
show_summary() {
    log_success "🎉 Deployment successful!"
    echo ""
    echo "Service Status:"
    docker-compose ps
    echo ""
    echo "API Endpoint: http://localhost:8000"
    echo "Health: http://localhost:8000/health"
    echo "Docs: http://localhost:8000/docs"
    echo ""
    echo "Useful Commands:"
    echo "  View logs:        docker-compose logs -f"
    echo "  Stop services:    docker-compose down"
    echo "  Run tests:        docker-compose exec api pytest -v"
    echo "  Database shell:   docker-compose exec postgres psql -U astrology_user -d astrology_db"
}

# Cleanup on error
cleanup_on_error() {
    log_error "Deployment failed. Cleaning up..."
    docker-compose down
    exit 1
}

trap cleanup_on_error ERR

# Main execution
main() {
    check_prerequisites
    build_images
    start_services
    wait_for_database
    init_database
    health_check || cleanup_on_error
    show_summary
}

main
