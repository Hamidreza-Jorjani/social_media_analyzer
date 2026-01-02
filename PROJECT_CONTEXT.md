# Persian Social Media Analyzer - Project Context

**Status:** Backend ✅ | BRAIN Mock ✅ | Frontend 🔄

## Architecture

Frontend:3000 → Backend:8000 → BRAIN:8001
Backend uses: PostgreSQL:5432, Redis:6379, Celery

## Stack

- Backend: FastAPI + SQLAlchemy + Celery
- BRAIN: FastAPI Mock (RAPIDS planned)
- Database: PostgreSQL 16
- Cache: Redis 7
- Auth: JWT + bcrypt

## Models

- User: email, username, role (admin/analyst/viewer)
- Post: content, platform, hashtags, is_processed
- Analysis: name, type, status, results
- AnalysisResult: sentiment, emotions, keywords
- Author: username, followers, pagerank
- Trend: name, volume, hashtags
- GraphNode: node_id, type, pagerank
- GraphEdge: source_id, target_id, weight

## Main API Endpoints

- POST /auth/login - Login
- POST /posts/bulk - Create posts
- POST /analysis - Create analysis
- POST /analysis/{id}/start - Run analysis
- GET /analysis/{id}/results - Get results
- GET /dashboard/overview - Dashboard stats
- POST /brain/analyze/text - NLP analysis

## Quick Start

cd backend && docker-compose up -d
cd brain && docker-compose up -d
docker network connect backend_app_network persian_analytics_brain

## Credentials

Admin: admin / Admin123!
Backend: http://localhost:8000/docs
BRAIN: http://localhost:8001/docs

## Key Directories

backend/app/api/v1/endpoints/ - REST endpoints
backend/app/models/ - Database models
backend/app/services/tasks.py - Celery tasks
brain/app/mock_data.py - Persian NLP mock
