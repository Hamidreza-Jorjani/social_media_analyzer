#!/bin/bash
echo "=== Verifying Existing Content ==="
echo ""

# Check lib/api/client.ts
echo "📄 lib/api/client.ts (first 30 lines):"
echo "----------------------------------------"
head -30 lib/api/client.ts 2>/dev/null || echo "❌ File not found"
echo ""

# Check lib/stores/auth-store.ts
echo "📄 lib/stores/auth-store.ts (first 30 lines):"
echo "----------------------------------------"
head -30 lib/stores/auth-store.ts 2>/dev/null || echo "❌ File not found"
echo ""

# Check providers/index.tsx
echo "📄 providers/index.tsx (first 30 lines):"
echo "----------------------------------------"
head -30 providers/index.tsx 2>/dev/null || echo "❌ File not found"
echo ""

# Check types/index.ts
echo "📄 types/index.ts (first 30 lines):"
echo "----------------------------------------"
head -30 types/index.ts 2>/dev/null || echo "❌ File not found"
echo ""

# Check app/layout.tsx
echo "📄 app/layout.tsx:"
echo "----------------------------------------"
cat app/layout.tsx 2>/dev/null || echo "❌ File not found"
echo ""

# Check app/page.tsx
echo "📄 app/page.tsx (first 50 lines):"
echo "----------------------------------------"
head -50 app/page.tsx 2>/dev/null || echo "❌ File not found"
echo ""

# Check .env.local
echo "📄 .env.local:"
echo "----------------------------------------"
cat .env.local 2>/dev/null || echo "❌ File not found"
echo ""

# Check lib/utils.ts
echo "📄 lib/utils.ts (first 20 lines):"
echo "----------------------------------------"
head -20 lib/utils.ts 2>/dev/null || echo "❌ File not found"
echo ""

# List all API files
echo "📁 lib/api/ contents:"
echo "----------------------------------------"
ls -la lib/api/ 2>/dev/null || echo "❌ Directory not found"
echo ""

echo "=== Done ==="
