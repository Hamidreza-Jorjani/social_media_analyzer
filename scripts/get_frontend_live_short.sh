#!/usr/bin/env bash
set -euo pipefail

# frontend_min.sh
# Minimal live backend/BRAIN snapshot for frontend planning.
#
# Usage:
#   cd ~/projects/social_media_analyzer
#   chmod +x frontend_min.sh
#   ./frontend_min.sh > frontend_live_context_min.txt

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

BACKEND_PORT="${BACKEND_PORT:-18000}"
BRAIN_PORT="${BRAIN_PORT:-18001}"

BACKEND_URL="http://localhost:${BACKEND_PORT}"
API_BASE="${BACKEND_URL}/api/v1"
OPENAPI_URL="${API_BASE}/openapi.json"
BRAIN_URL="http://localhost:${BRAIN_PORT}"

echo "=== FRONTEND LIVE CONTEXT (MINIMAL) ==="
echo
echo "Backend:"
echo "  URL:      $BACKEND_URL"
echo "  API base: $API_BASE"
echo
echo "BRAIN:"
echo "  URL:      $BRAIN_URL"
echo
echo "Frontend .env.local (dev):"
echo "  NEXT_PUBLIC_API_URL=$API_BASE"
echo

echo "=== LIVE HEALTH CHECKS ==="
echo
echo "-- Backend /health --"
curl -sS "$BACKEND_URL/health" || echo "FAILED"
echo
echo
echo "-- /api/v1/status --"
curl -sS "$API_BASE/status" || echo "FAILED"
echo
echo
echo "-- BRAIN /health --"
curl -sS "$BRAIN_URL/health" || echo "FAILED"
echo
echo

echo "=== OPENAPI SUMMARY (LIVE) ==="
echo "Source: $OPENAPI_URL"
echo

OPENAPI_RAW="$(curl -sS "$OPENAPI_URL" || echo '')"

if [ -z "$OPENAPI_RAW" ]; then
  echo "!! Could not fetch OpenAPI JSON from $OPENAPI_URL"
else
  if command -v jq >/dev/null 2>&1; then
    echo "-- Basic info --"
    echo "$OPENAPI_RAW" | jq '{title: .info.title, version: .info.version}' 2>/dev/null || echo "N/A"
    echo

    echo "-- Paths (method -> path) --"
    echo "$OPENAPI_RAW" | jq '
      .paths
      | to_entries
      | map({
          path: .key,
          methods: ( .value | keys )
        })
    ' 2>/dev/null || echo "N/A"
    echo
  else
    echo "jq not available; showing raw OpenAPI:"
    echo "$OPENAPI_RAW"
  fi
fi

echo "=== END FRONTEND LIVE CONTEXT (MINIMAL) ==="