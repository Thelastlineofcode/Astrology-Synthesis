#!/bin/bash
# Start script for Railway deployment

# Use Railway's PORT environment variable, default to 8000 for local dev
PORT=${PORT:-8000}

# Start uvicorn with the correct module path
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
