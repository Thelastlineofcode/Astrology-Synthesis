#!/bin/bash
# Quick Start Script for Local Development

echo "🚀 Starting Mula Astrology-Synthesis Application"
echo "================================================"
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "❌ backend/.env not found!"
    echo "Please create it from backend/.env.example"
    exit 1
fi

# Check if database exists
if [ ! -f "astrology_synthesis.db" ]; then
    echo "⚠️  Database not found. It will be created on first run."
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv .venv && .venv/bin/pip install -r backend/requirements.txt"
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  Frontend dependencies not installed. Installing..."
    cd frontend && npm install && cd ..
fi

echo "✅ Prerequisites checked"
echo ""

# Start backend in background
echo "📡 Starting backend on port 8001..."
PORT=8001 .venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8001 > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "   Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "   ✅ Backend started successfully"
else
    echo "   ❌ Backend failed to start. Check backend.log"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""

# Start frontend
echo "🎨 Starting frontend on port 3001..."
cd frontend
PORT=3001 npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ Application started successfully!"
echo ""
echo "================================================"
echo "🌐 Access your application at:"
echo "   Frontend: http://localhost:3001"
echo "   Backend:  http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo ""
echo "📋 To register your user account:"
echo "   python setup_user.py"
echo ""
echo "🛑 To stop the application:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo "================================================"
