#!/bin/bash
set -e

PROJECT_ROOT="$HOME/projects/social_media_analyzer"
BACKEND_PORT=18000
BRAIN_PORT=18001

cd "$PROJECT_ROOT"

mkdir -p data/postgres data/redis
sudo chown -R 999:999 data/postgres data/redis 2>/dev/null || true

echo "🚀 Starting SMA stack..."

docker compose -f backend/docker-compose.yml up -d
echo "⏳ Waiting for backend stack (DB, Redis, API)..."
sleep 15

docker compose -f brain/docker-compose.yml up -d
echo "⏳ Waiting for BRAIN service..."
sleep 5

echo ""
docker ps --format "table {{.Names}}\t{{.Status}}" | grep sma || true
echo ""
echo "Backend docs:    http://localhost:${BACKEND_PORT}/docs"
echo "Backend health:  http://localhost:${BACKEND_PORT}/health"
echo "BRAIN health:    http://localhost:${BRAIN_PORT}/health"
