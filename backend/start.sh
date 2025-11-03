#!/bin/bash
# Start script for Railway deployment

# Use Railway's PORT environment variable, default to 8000 for local dev
PORT=${PORT:-8000}

# Start uvicorn with the specified port
uvicorn main:app --host 0.0.0.0 --port $PORT
