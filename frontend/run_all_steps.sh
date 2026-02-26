#!/bin/bash
set -e

echo "🚀 Running All Frontend Setup Steps..."
echo ""

cd "$(dirname "$0")"

steps=(
  "setup_step6.sh:Posts Page"
  "setup_step7.sh:Analysis Pages"
  "setup_step8.sh:Trends Page"
  "setup_step9.sh:Graph Page"
  "setup_step10.sh:Authors Page"
  "setup_step11.sh:Settings Page"
)

for step in "${steps[@]}"; do
  IFS=':' read -r script name <<< "$step"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📦 Running: $name"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  if [ -f "$script" ]; then
    ./"$script"
  else
    echo "⚠️  Script not found: $script"
  fi
  echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All steps complete!"
echo ""
echo "📁 Created pages:"
echo "  - /dashboard/posts"
echo "  - /dashboard/analysis"
echo "  - /dashboard/analysis/new"
echo "  - /dashboard/analysis/[id]"
echo "  - /dashboard/trends"
echo "  - /dashboard/graph"
echo "  - /dashboard/authors"
echo "  - /dashboard/settings"
echo ""
echo "🎯 Restart dev server: pnpm dev"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
