#!/bin/bash

echo "Running Persian Social Analytics Tests"
echo "======================================="

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
pytest tests/ \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    -v

echo ""
echo "Coverage report generated in htmlcov/"
