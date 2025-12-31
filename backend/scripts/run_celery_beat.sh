#!/bin/bash

echo "Starting Celery Beat Scheduler"
echo "=============================="

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Celery beat
celery -A app.services.celery_app beat --loglevel=info
