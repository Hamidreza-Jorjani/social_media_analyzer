#!/bin/bash

cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║         Persian Social Media Analyzer - Help                  ║
╚═══════════════════════════════════════════════════════════════╝

📍 QUICK START
   ./start.sh              Start all services
   ./stop.sh               Stop all services
   ./rebuild.sh            Clean rebuild (keeps data by default)

📍 URLS
   Backend API:    http://localhost:8000/docs
   BRAIN API:      http://localhost:8001/docs
   Frontend:       http://localhost:3000 (when running)

📍 CREDENTIALS
   Username: admin
   Password: Admin123!

📍 DATA LOCATION
   PostgreSQL:  ~/projects/social_media_analyzer/data/postgres/
   Redis:       ~/projects/social_media_analyzer/data/redis/

📍 SCRIPTS
   ./start.sh                    Start all services
   ./stop.sh                     Stop all services  
   ./rebuild.sh                  Rebuild containers
   ./full_test.sh                Run integration tests
   ./scripts/generate_docs.sh    Generate full documentation
   ./scripts/get_context.sh      Get project context for AI

📍 DOCKER COMMANDS
   docker ps                     Show running containers
   docker logs -f persian_analytics_backend    View backend logs
   docker logs -f persian_analytics_brain      View BRAIN logs
   docker logs -f persian_analytics_celery     View Celery logs

📍 DATABASE
   # Connect to PostgreSQL
   docker exec -it persian_analytics_db psql -U postgres -d persian_analytics

   # View Redis
   docker exec -it persian_analytics_redis redis-cli

📍 BACKUP DATA
   cp -r data/ backup_$(date +%Y%m%d)/

📍 TROUBLESHOOTING
   # Restart a specific service
   docker restart persian_analytics_backend

   # View all logs
   docker-compose -f backend/docker-compose.yml logs -f

   # Force rebuild without cache
   docker-compose -f backend/docker-compose.yml build --no-cache

EOF