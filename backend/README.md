# Persian Social Media Analysis System - Backend

A powerful backend API for Persian social media analysis with NLP, sentiment analysis, graph analytics, and more.

## Architecture

- **Backend**: FastAPI (this service)
- **Frontend**: Separate service (React/Vue)
- **BRAIN**: RAPIDS Docker container for AI/ML processing

## Tech Stack

- FastAPI 0.115+
- PostgreSQL with AsyncPG
- Redis for caching and Celery broker
- SQLAlchemy 2.0+ (async)
- Celery for background tasks

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/WSL
