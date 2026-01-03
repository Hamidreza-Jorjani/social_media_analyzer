#!/usr/bin/env bash
set -euo pipefail

# collect_frontend_context.sh
# Run from project root: ~/projects/social_media_analyzer
# Usage:
#   ./collect_frontend_context.sh > frontend_context.txt

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

BACKEND_PORT="${BACKEND_PORT:-18000}"
BRAIN_PORT="${BRAIN_PORT:-18001}"
BACKEND_URL="http://localhost:${BACKEND_PORT}"
API_BASE="${BACKEND_URL}/api/v1"
BRAIN_URL="http://localhost:${BRAIN_PORT}"

echo "==================== FRONTEND CONTEXT ===================="
echo
echo "Project root: $ROOT"
echo
echo "Backend:"
echo "  URL:          $BACKEND_URL"
echo "  API base:     $API_BASE"
echo "  Health:       $BACKEND_URL/health"
echo "  OpenAPI JSON: $API_BASE/openapi.json"
echo
echo "BRAIN:"
echo "  URL:          $BRAIN_URL"
echo "  Health:       $BRAIN_URL/health"
echo
echo "Recommended frontend .env.local:"
echo "  NEXT_PUBLIC_API_URL=$API_BASE"
echo
echo "=== LIVE HEALTH CHECKS (if backend/brain are running) ==="
echo
echo "--- Backend /health ---"
curl -s "$BACKEND_URL/health" || echo "FAILED"
echo
echo
echo "--- /api/v1/status (if implemented) ---"
curl -s "$API_BASE/status" || echo "FAILED"
echo
echo
echo "--- BRAIN /health ---"
curl -s "$BRAIN_URL/health" || echo "FAILED"
echo
echo

echo "==================== HIGH-LEVEL API SPEC ================="
echo
if [ -f "$ROOT/ai_document/API.md" ]; then
  echo "----- FILE: ai_document/API.md -----"
  cat "$ROOT/ai_document/API.md"
  echo
else
  echo "ai_document/API.md not found."
  echo
fi

echo "================ TECHNICAL BACKEND/BRAIN SPEC ============"
echo
if [ -f "$ROOT/ai_document/technical_for_machine.md" ]; then
  echo "----- FILE: ai_document/technical_for_machine.md -----"
  cat "$ROOT/ai_document/technical_for_machine.md"
  echo
elif [ -f "$ROOT/backend/technical_for_machine.md" ]; then
  echo "----- FILE: backend/technical_for_machine.md -----"
  cat "$ROOT/backend/technical_for_machine.md"
  echo
else
  echo "No technical_for_machine.md found."
  echo
fi

echo "================ BACKEND CONFIG SNIPPET =================="
echo
if [ -f "$ROOT/backend/app/core/config.py" ]; then
  echo "----- FILE: backend/app/core/config.py -----"
  cat "$ROOT/backend/app/core/config.py"
  echo
fi

echo "================ API ROUTER & ENDPOINTS =================="
echo
if [ -f "$ROOT/backend/app/api/v1/router.py" ]; then
  echo "----- FILE: backend/app/api/v1/router.py -----"
  cat "$ROOT/backend/app/api/v1/router.py"
  echo
fi

if [ -d "$ROOT/backend/app/api/v1/endpoints" ]; then
  echo "----- TREE: backend/app/api/v1/endpoints -----"
  (cd "$ROOT/backend/app/api/v1/endpoints" && ls -1)
  echo
fi

echo "==================== CONTEXT END ========================="
