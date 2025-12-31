#!/bin/bash

echo "Starting Celery Worker"
echo "======================"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Celery worker
celery -A app.services.celery_app worker --loglevel=info
