#!/bin/bash
echo "🧹 Cleaning up SMA containers and images..."

PROJECT_ROOT=~/projects/social_media_analyzer
cd "$PROJECT_ROOT"

# Stop and remove containers
docker stop sma_brain sma_celery sma_backend sma_redis sma_postgres 2>/dev/null
docker rm sma_brain sma_celery sma_backend sma_redis sma_postgres 2>/dev/null

echo ""
echo "Current SMA images:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep sma

echo ""
echo "Options:"
echo "  1) Keep all images"
echo "  2) Keep only latest 3 versions"
echo "  3) Remove ALL SMA images"
echo ""
read -p "Choose option [1]: " option
option=${option:-1}

case $option in
    2)
        echo "Keeping latest 3 versions..."
        docker images --format "{{.Repository}}:{{.Tag}}" | grep "^sma_" | sort -r | tail -n +4 | xargs -r docker rmi
        ;;
    3)
        echo "Removing all SMA images..."
        docker images --format "{{.Repository}}:{{.Tag}}" | grep "^sma_" | xargs -r docker rmi
        rm -f .sma_tag
        ;;
    *)
        echo "Keeping all images."
        ;;
esac

# Remove network
docker network rm sma_network 2>/dev/null || true

# Prune dangling images
docker image prune -f

echo ""
echo "✅ Cleanup complete"
