#!/bin/bash
echo "=== Frontend State Check ==="
echo ""
echo "📁 Checking key files..."

files=(
  "app/layout.tsx"
  "app/page.tsx"
  "app/globals.css"
  "lib/api/client.ts"
  "lib/stores/auth-store.ts"
  "providers/index.tsx"
  "types/index.ts"
  "next.config.ts"
  "tailwind.config.ts"
  ".env.local"
)

for f in "${files[@]}"; do
  if [ -f "$f" ]; then
    echo "✅ $f"
  else
    echo "❌ $f (missing)"
  fi
done

echo ""
echo "📁 UI Components:"
ls -la components/ui/ 2>/dev/null || echo "❌ No UI components"

echo ""
echo "📁 Current app/ structure:"
find app -name "*.tsx" -o -name "*.ts" 2>/dev/null | head -20

echo ""
echo "=== Done ==="
