#!/bin/bash
set -e

THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔════════════════════════════════════════════╗"
echo "║   Persian Analytics - Modular Test Suite  ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Each script runs with its own counters & summaries

"${THIS_DIR}/test_health.sh"
"${THIS_DIR}/test_auth.sh"
"${THIS_DIR}/test_posts.sh"
"${THIS_DIR}/test_brain.sh"

# Optionally run your existing full pipeline test if present at repo root
if [ -x "${THIS_DIR}/../full_test.sh" ]; then
  echo ""
  echo "Now running full pipeline test (full_test.sh)..."
  "${THIS_DIR}/../full_test.sh"
fi

echo ""
echo "✅ All modular tests executed."
