#!/bin/bash
echo "🔄 Quick code update (no rebuild)..."

cd ~/projects/social_media_analyzer

# Just restart containers (code is mounted via volumes for BRAIN)
docker restart sma_backend sma_celery

echo "✅ Backend restarted!"
echo ""
echo "Note: BRAIN auto-reloads (--reload flag)"
