#!/bin/bash

echo "Starting Persian Social Analytics - Development Mode"
echo "===================================================="

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
