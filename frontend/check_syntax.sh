#!/bin/bash
cd "$(dirname "$0")"

echo "=== Checking for TypeScript Errors ==="
echo ""

# Run TypeScript compiler in check mode
npx tsc --noEmit 2>&1 | head -50

echo ""
echo "=== Done ==="
