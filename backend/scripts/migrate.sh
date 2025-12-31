#!/bin/bash

echo "Running Database Migrations"
echo "==========================="

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run migrations
alembic upgrade head

echo "Migrations completed!"
