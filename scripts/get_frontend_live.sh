#!/usr/bin/env bash
set -euo pipefail

# frontend.sh
# Live backend/BRAIN introspection for frontend design.
# Uses only HTTP calls to running services, no local .md/.txt.
#
# Usage:
#   cd ~/projects/social_media_analyzer
#   chmod +x frontend.sh
#   ./frontend.sh > frontend_live_context.txt

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

BACKEND_PORT="${BACKEND_PORT:-18000}"
BRAIN_PORT="${BRAIN_PORT:-18001}"

BACKEND_URL="http://localhost:${BACKEND_PORT}"
API_BASE="${BACKEND_URL}/api/v1"
OPENAPI_URL="${API_BASE}/openapi.json"
BRAIN_URL="http://localhost:${BRAIN_PORT}"

echo "==================== FRONTEND LIVE CONTEXT ===================="
echo
echo "Project root: $ROOT"
echo
echo "Backend (live):"
echo "  URL:          $BACKEND_URL"
echo "  API base:     $API_BASE"
echo "  Health:       $BACKEND_URL/health"
echo "  OpenAPI JSON: $OPENAPI_URL"
echo
echo "BRAIN (live):"
echo "  URL:          $BRAIN_URL"
echo "  Health:       $BRAIN_URL/health"
echo
echo "Recommended frontend .env.local (dev):"
echo "  NEXT_PUBLIC_API_URL=$API_BASE"
echo
echo "NOTE: All information below is fetched LIVE from the running services"
echo "      (no .md or local documentation is used)."
echo

echo "================ LIVE HEALTH CHECKS ==========================="
echo

echo "--- Backend /health ---"
curl -sS "$BACKEND_URL/health" || echo "FAILED"
echo
echo

echo "--- /api/v1/status ---"
curl -sS "$API_BASE/status" || echo "FAILED"
echo
echo

echo "--- BRAIN /health ---"
curl -sS "$BRAIN_URL/health" || echo "FAILED"
echo
echo

echo "================ OPENAPI SCHEMA (LIVE) ======================="
echo
echo "Source: $OPENAPI_URL"
echo

OPENAPI_RAW="$(curl -sS "$OPENAPI_URL" || echo '')"

if [ -z "$OPENAPI_RAW" ]; then
  echo "!! Could not fetch OpenAPI JSON from $OPENAPI_URL"
else
  if command -v jq >/dev/null 2>&1; then
    echo "----- OPENAPI JSON (pretty-printed via jq) -----"
    echo "$OPENAPI_RAW" | jq .
  else
    echo "----- OPENAPI JSON (raw) -----"
    echo "$OPENAPI_RAW"
  fi
fi

echo
echo "================ SMALL SUMMARY FROM OPENAPI ==================="
echo

if command -v jq >/dev/null 2>&1 && [ -n "$OPENAPI_RAW" ]; then
  echo "--- Basic info ---"
  echo "$OPENAPI_RAW" | jq '{title: .info.title, version: .info.version}' 2>/dev/null || echo "N/A"
  echo

  echo "--- Tags (if defined) ---"
  echo "$OPENAPI_RAW" | jq '.tags // []' 2>/dev/null || echo "N/A"
  echo

  echo "--- Paths (method -> path) ---"
  echo "$OPENAPI_RAW" | jq '
    .paths
    | to_entries
    | map({path: .key, methods: ( .value | keys )})
  ' 2>/dev/null || echo "N/A"
  echo
else
  echo "jq not available or OpenAPI could not be fetched; skipping summary."
fi

echo "==================== FRONTEND LIVE CONTEXT END ================"
