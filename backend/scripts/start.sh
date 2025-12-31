#!/bin/bash

echo "=========================================="
echo "Persian Social Analytics - Docker Setup"
echo "=========================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting all services...${NC}"

# Start with development overrides
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d

echo ""
echo -e "${GREEN}Services started!${NC}"
echo ""
echo "Available endpoints:"
echo "  - Backend API:    http://localhost:8000"
echo "  - Swagger Docs:   http://localhost:8000/docs"
echo "  - ReDoc:          http://localhost:8000/redoc"
echo "  - Health Check:   http://localhost:8000/health"
echo ""
echo "Database connections:"
echo "  - PostgreSQL:     localhost:5432"
echo "  - Redis:          localhost:6379"
echo ""
echo "Useful commands:"
echo "  - View logs:      docker-compose logs -f"
echo "  - Stop services:  docker-compose down"
echo "  - Rebuild:        docker-compose up --build -d"
echo ""
