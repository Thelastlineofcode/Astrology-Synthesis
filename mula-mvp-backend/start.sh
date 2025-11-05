#!/bin/bash

# Mula MVP Backend - Startup Script

echo "🚀 Starting Mula Dasha Timer API..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please copy .env.example to .env and configure it"
    exit 1
fi

# Start uvicorn server
echo "✅ Starting FastAPI server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
