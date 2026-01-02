#!/bin/bash
cd ~/projects/social_media_analyzer
docker compose -f brain/docker-compose.yml down
docker compose -f backend/docker-compose.yml down
echo "✅ Stopped"
