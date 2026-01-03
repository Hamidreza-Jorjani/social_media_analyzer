#!/bin/bash
set -e

PROJECT_ROOT="$HOME/projects/social_media_analyzer"
BACKEND_PORT=18000
BRAIN_PORT=18001
BACKEND_URL="http://localhost:${BACKEND_PORT}"
BRAIN_URL="http://localhost:${BRAIN_PORT}"
API_URL="${BACKEND_URL}/api/v1"

cd "$PROJECT_ROOT"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

pass() { echo -e "${GREEN}✅ $1${NC}"; }
fail() { echo -e "${RED}❌ $1${NC}"; }

check_docker() {
  echo -e "${YELLOW}--- Docker status ---${NC}"
  docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep sma || echo "No sma_* containers"
  echo ""
  docker network ls | grep sma_network || echo "No sma_network found"
  echo ""
}

check_ports() {
  echo -e "${YELLOW}--- Port bindings ---${NC}"
  if command -v ss >/dev/null 2>&1; then
    ss -tulpn | grep -E ':18000|:18001' || echo "No 18000/18001 listeners (Linux side)"
  elif command -v netstat >/dev/null 2>&1; then
    netstat -tulpn | grep -E ':18000|:18001' || echo "No 18000/18001 listeners (Linux side)"
  else
    echo "Neither ss nor netstat found."
  fi
  echo ""
}

check_health() {
  echo -e "${YELLOW}--- Health checks ---${NC}"
  echo -n "Backend: "
  H_B=$(curl -s "${BACKEND_URL}/health" || true)
  if echo "$H_B" | grep -q '"status":"healthy"'; then
    pass "healthy"
  else
    fail "not healthy"
    echo "$H_B"
  fi

  echo -n "BRAIN:   "
  H_R=$(curl -s "${BRAIN_URL}/health" || true)
  if echo "$H_R" | grep -q '"status":"healthy"'; then
    pass "healthy"
  else
    fail "not healthy"
    echo "$H_R"
  fi
  echo ""
}

check_auth() {
  echo -e "${YELLOW}--- Admin login test ---${NC}"
  RESP=$(curl -s -X POST "${API_URL}/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"Admin123!"}' || true)
  TOKEN=$(echo "$RESP" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
  if [ -n "$TOKEN" ]; then
    pass "login ok"
  else
    fail "login failed"
    echo "$RESP"
  fi
  echo ""
}

run_integration() {
  echo -e "${YELLOW}--- Running full integration test ---${NC}"
  if [ -x "./fulltest.sh" ]; then
    ./fulltest.sh
  elif [ -x "./full_test.sh" ]; then
    ./full_test.sh
  elif [ -x "./backend/scripts/test_full_flow.sh" ]; then
    ./backend/scripts/test_full_flow.sh
  else
    echo "No full test script found"
  fi
}

case "${1:-all}" in
  docker)
    check_docker
    ;;
  ports)
    check_ports
    ;;
  health)
    check_docker
    check_ports
    check_health
    ;;
  auth)
    check_auth
    ;;
  integration)
    run_integration
    ;;
  all)
    check_docker
    check_ports
    check_health
    check_auth
    ;;
  *)
    echo "Usage: $0 [docker|ports|health|auth|integration|all]"
    exit 1
    ;;
esac
