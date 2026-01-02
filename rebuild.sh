#!/bin/bash
set -e

PROJECT_ROOT="$HOME/projects/social_media_analyzer"
BACKEND_PORT=18000
BRAIN_PORT=18001

cd "$PROJECT_ROOT"

echo "╔═══════════════════════════════════════╗"
echo "║   SMA Rebuild                         ║"
echo "╚═══════════════════════════════════════╝"

echo ""
echo "1) Quick (use cache)"
echo "2) Full (no cache)"
read -p "Build type [1]: " build_type
build_type=${build_type:-1}

echo ""
echo "1) Keep data"
echo "2) Fresh database"
read -p "Data [1]: " data_type
data_type=${data_type:-1}

echo ""
echo "🛑 Stopping..."
docker compose -f brain/docker-compose.yml down 2>/dev/null || true
docker compose -f backend/docker-compose.yml down 2>/dev/null || true

if [ "$data_type" = "2" ]; then
    echo "🗑️  Clearing data..."
    sudo rm -rf data/postgres/* data/redis/*
fi
mkdir -p data/postgres data/redis
sudo chown -R 999:999 data/postgres data/redis 2>/dev/null || true

echo ""
if [ "$build_type" = "2" ]; then
    echo "🔨 Building (no cache)..."
    docker compose -f backend/docker-compose.yml build --no-cache
    docker compose -f brain/docker-compose.yml build --no-cache
else
    echo "🔨 Building (with cache)..."
    docker compose -f backend/docker-compose.yml build
    docker compose -f brain/docker-compose.yml build
fi

echo ""
echo "🚀 Starting..."
docker compose -f backend/docker-compose.yml up -d
echo "⏳ Waiting for backend stack..."
sleep 15
docker compose -f brain/docker-compose.yml up -d
echo "⏳ Waiting for BRAIN..."
sleep 5

echo ""
echo "📊 Status:"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep sma || true
echo ""
echo "Backend: $(curl -s "http://localhost:${BACKEND_PORT}/health" | grep -o '"status":"[^"]*"' || echo 'starting...')"
echo "BRAIN:   $(curl -s "http://localhost:${BRAIN_PORT}/health" | grep -o '"status":"[^"]*"' || echo 'starting...')"
echo ""
echo "✅ Done! → http://localhost:${BACKEND_PORT}/docs"
echo "🔑 admin / Admin123!"
