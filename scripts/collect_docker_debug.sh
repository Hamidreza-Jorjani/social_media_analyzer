#!/usr/bin/env bash
set -euo pipefail

echo "========== SYSTEM INFO =========="
echo "PWD: $(pwd)"
echo
echo "uname -a:"
uname -a || true
echo
echo "docker version:"
docker version || true
echo
echo "docker compose version:"
docker compose version 2>/dev/null || docker-compose --version || true
echo

echo "========== DOCKER STATUS =========="
echo "docker ps:"
docker ps --format 'table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}'
echo

echo "docker ps -a:"
docker ps -a --format 'table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}'
echo

echo "docker network ls:"
docker network ls || true
echo

echo "========== LISTENING PORTS (backend/brain) =========="
if command -v ss >/dev/null 2>&1; then
  ss -tulpn | grep -E ':18000|:18001' || echo "No processes listening on 18000/18001 (Linux side)"
elif command -v netstat >/dev/null 2>&1; then
  netstat -tulpn | grep -E ':18000|:18001' || echo "No processes listening on 18000/18001 (Linux side)"
else
  echo "Neither ss nor netstat found."
fi
echo

echo "========== DOCKER COMPOSE CONFIGS =========="
# Root-level docker-compose
if [ -f docker-compose.yml ]; then
  echo "--- FILE: ./docker-compose.yml ---"
  cat docker-compose.yml
  echo
fi

if [ -f docker-compose.dev.yml ]; then
  echo "--- FILE: ./docker-compose.dev.yml ---"
  cat docker-compose.dev.yml
  echo
fi

# Backend docker-compose + Dockerfile + env
if [ -d backend ]; then
  echo "----- BACKEND CONFIGS -----"
  if [ -f backend/docker-compose.yml ]; then
    echo "--- FILE: backend/docker-compose.yml ---"
    cat backend/docker-compose.yml
    echo
  fi

  if [ -f backend/docker-compose.dev.yml ]; then
    echo "--- FILE: backend/docker-compose.dev.yml ---"
    cat backend/docker-compose.dev.yml
    echo
  fi

  if [ -f backend/Dockerfile ]; then
    echo "--- FILE: backend/Dockerfile ---"
    cat backend/Dockerfile
    echo
  fi

  if [ -f backend/.env ]; then
    echo "--- FILE: backend/.env (WARNING: may contain secrets) ---"
    cat backend/.env
    echo
  fi

  if [ -f backend/.env.docker ]; then
    echo "--- FILE: backend/.env.docker (WARNING: may contain secrets) ---"
    cat backend/.env.docker
    echo
  fi

  if [ -f backend/scripts/start.sh ]; then
    echo "--- FILE: backend/scripts/start.sh ---"
    cat backend/scripts/start.sh
    echo
  fi

  if [ -f backend/scripts/stop.sh ]; then
    echo "--- FILE: backend/scripts/stop.sh ---"
    cat backend/scripts/stop.sh
    echo
  fi
fi

# Brain docker-compose + Dockerfile + env
if [ -d brain ]; then
  echo "----- BRAIN CONFIGS -----"
  if [ -f brain/docker-compose.yml ]; then
    echo "--- FILE: brain/docker-compose.yml ---"
    cat brain/docker-compose.yml
    echo
  fi

  if [ -f brain/Dockerfile ]; then
    echo "--- FILE: brain/Dockerfile ---"
    cat brain/Dockerfile
    echo
  fi

  if [ -f brain/.env ]; then
    echo "--- FILE: brain/.env (WARNING: may contain secrets) ---"
    cat brain/.env
    echo
  fi

  if [ -f brain/.env.docker ]; then
    echo "--- FILE: brain/.env.docker (WARNING: may contain secrets) ---"
    cat brain/.env.docker
    echo
  fi
fi

echo "========== BACKEND CONTAINER INSPECT (IF PRESENT) =========="
# Try to inspect containers that match your names
for name in sma_backend persian_analytics_backend backend-backend; do
  if docker ps -a --format '{{.Names}}' | grep -q "^${name}\$"; then
    echo "--- docker inspect ${name} (network + ports) ---"
    docker inspect "${name}" | sed 's/"Env": \[.*\]/"Env": [ ...REDACTED... ]/' || true
    echo
  fi
done

echo "========== BRAIN CONTAINER INSPECT (IF PRESENT) =========="
for name in sma_brain persian_analytics_brain brain-brain; do
  if docker ps -a --format '{{.Names}}' | grep -q "^${name}\$"; then
    echo "--- docker inspect ${name} (network + ports) ---"
    docker inspect "${name}" | sed 's/"Env": \[.*\]/"Env": [ ...REDACTED... ]/' || true
    echo
  fi
done

echo "========== DONE =========="
echo "Review output and redact any passwords/secret keys before sharing."
