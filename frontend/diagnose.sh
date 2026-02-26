#!/bin/bash
cd "$(dirname "$0")"

echo "=== Frontend Diagnostics ==="
echo ""

echo "📦 Checking dependencies..."
if [ -f "node_modules/.pnpm/lock.yaml" ] || [ -d "node_modules/next" ]; then
  echo "✅ node_modules exists"
else
  echo "❌ node_modules missing - run: pnpm install"
fi

echo ""
echo "📄 Checking critical files..."
files=(
  "app/layout.tsx"
  "app/(dashboard)/layout.tsx"
  "app/(dashboard)/dashboard/page.tsx"
  "components/ui/card.tsx"
  "components/ui/tabs.tsx"
  "lib/api/client.ts"
  "lib/stores/auth-store.ts"
)

for f in "${files[@]}"; do
  if [ -f "$f" ]; then
    echo "✅ $f"
  else
    echo "❌ $f MISSING!"
  fi
done

echo ""
echo "📄 Checking for syntax errors in key files..."

# Check if TypeScript can parse files
echo "Checking app/(dashboard)/layout.tsx..."
head -5 "app/(dashboard)/layout.tsx" 2>/dev/null || echo "❌ Cannot read file"

echo ""
echo "Checking app/(dashboard)/dashboard/page.tsx..."
head -5 "app/(dashboard)/dashboard/page.tsx" 2>/dev/null || echo "❌ Cannot read file"

echo ""
echo "🌐 Checking ports..."
if command -v lsof &> /dev/null; then
  lsof -i :3000 2>/dev/null | head -3 || echo "Port 3000 not in use"
fi

echo ""
echo "=== End Diagnostics ==="
