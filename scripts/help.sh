PROJECT_ROOT=~/projects/social_media_analyzer

show_help() {
    echo "=== Project Context Generator ==="
    echo ""
    echo "Usage: ./scripts/get_context.sh [section]"
    echo ""
    echo "OVERVIEW:"
    echo "  summary     - Quick project overview"
    echo "  status      - Live docker & health status"
    echo "  goals       - Project goals and features"
    echo "  tree        - Project directory structure"
    echo ""
    echo "API INFO:"
    echo "  api-list    - All API routes (compact)"
    echo "  api-examples- Request/response examples"
    echo "  openapi     - Full OpenAPI spec (JSON)"
    echo "  auth-flow   - Authentication flow"
    echo "  enums       - All enums and values"
    echo ""
    echo "CODE:"
    echo "  models      - Database models"
    echo "  schemas     - Pydantic schemas"
    echo "  endpoints   - API endpoint code"
    echo "  services    - Services and tasks"
    echo "  core        - Config, security"
    echo "  brain       - BRAIN service"
    echo ""
    echo "CONFIG:"
    echo "  docker      - Docker compose"
    echo "  reqs        - Requirements"
    echo ""
    echo "COMBINED:"
    echo "  frontend    - Everything for frontend dev"
    echo "  all         - Everything"
    echo ""
}

section_tree() {
    echo "# Project Structure"
    echo ""
    echo '```'
    if command -v tree &> /dev/null; then
        tree -I '__pycache__|*.pyc|.git|venv|node_modules|.pytest_cache|*.egg-info' --dirsfirst "$PROJECT_ROOT" 2>/dev/null
    else
        echo "Installing tree..."
        sudo apt-get install -y tree > /dev/null 2>&1
        tree -I '__pycache__|*.pyc|.git|venv|node_modules|.pytest_cache|*.egg-info' --dirsfirst "$PROJECT_ROOT" 2>/dev/null
    fi
    echo '```'
}

section_summary() {
    echo "# Persian Social Media Analyzer"
    echo ""
    echo "Persian (Farsi) social media analysis with NLP."
    echo ""
    echo "## Architecture"
    echo "Frontend:3000 -> Backend:8000 -> BRAIN:8001"
    echo "Database: PostgreSQL:5432, Redis:6379, Celery"
    echo ""
    echo "## Stack"
    echo "- Backend: FastAPI + SQLAlchemy + Celery"
    echo "- BRAIN: FastAPI Mock (RAPIDS planned)"
    echo "- Database: PostgreSQL 16, Redis 7"
    echo "- Auth: JWT + bcrypt"
    echo ""
    echo "## Credentials"
    echo "- Admin: admin / Admin123!"
    echo "- Docs: http://localhost:8000/docs"
    echo ""
}

section_goals() {
    echo "# Project Goals"
    echo ""
    echo "## Features"
    echo "- Sentiment analysis (positive/negative/neutral)"
    echo "- Emotion detection (joy, sadness, anger, fear, surprise, disgust)"
    echo "- Keyword extraction"
    echo "- Named entity recognition"
    echo "- Trend detection"
    echo "- Graph analysis (PageRank, communities)"
    echo ""
    echo "## Platforms"
    echo "twitter, instagram, telegram, linkedin, youtube, news, forum"
    echo ""
    echo "## User Roles"
    echo "- admin: Full access"
    echo "- analyst: CRUD + analyses"
    echo "- viewer: Read only"
    echo ""
    echo "## Frontend Features Needed"
    echo "1. Login page"
    echo "2. Dashboard with charts"
    echo "3. Posts list with filters"
    echo "4. Analysis management"
    echo "5. Trends visualization"
    echo "6. Graph visualization"
    echo "7. User management"
    echo ""
}

section_openapi() {
    echo "# OpenAPI Specification"
    echo ""
    curl -s http://localhost:8000/api/v1/openapi.json 2>/dev/null || echo '{"error": "Backend not running"}'
}

section_api_list() {
    echo "# API Routes"
    echo ""
    echo "Base: http://localhost:8000/api/v1"
    echo ""
    echo "## Auth"
    echo "POST /auth/login"
    echo "POST /auth/register"
    echo "POST /auth/refresh"
    echo "GET  /auth/me"
    echo ""
    echo "## Posts"
    echo "GET  /posts"
    echo "POST /posts"
    echo "POST /posts/bulk"
    echo "GET  /posts/stats"
    echo "GET  /posts/search?q="
    echo ""
    echo "## Analysis"
    echo "GET  /analysis"
    echo "POST /analysis"
    echo "POST /analysis/{id}/start"
    echo "GET  /analysis/{id}/results"
    echo "GET  /analysis/{id}/summary"
    echo ""
    echo "## Trends"
    echo "GET  /trends/hashtags"
    echo "GET  /trends/keywords"
    echo "POST /trends/detect"
    echo ""
    echo "## Graph"
    echo "GET  /graph/data"
    echo "GET  /graph/stats"
    echo "POST /graph/build/author-network"
    echo ""
    echo "## Dashboard"
    echo "GET  /dashboard/overview"
    echo "GET  /dashboard/sentiment"
    echo ""
}

section_api_examples() {
    echo "# API Examples"
    echo ""
    echo "## Login"
    echo 'POST /auth/login {"username":"admin","password":"Admin123!"}'
    echo 'Response: {"user":{...},"tokens":{"access_token":"..."}}'
    echo ""
    echo "## Create Analysis"
    echo 'POST /analysis {"name":"Test","analysis_type":"full","query_filters":{"platform":"twitter"}}'
    echo ""
    echo "## Start Analysis"
    echo 'POST /analysis/1/start'
    echo ""
    echo "## Get Results"
    echo 'GET /analysis/1/results'
    echo '[{"sentiment_label":"positive","emotions":{...},"keywords":[...]}]'
    echo ""
}

section_auth_flow() {
    echo "# Auth Flow"
    echo ""
    echo "1. POST /auth/login -> get access_token"
    echo "2. Add header: Authorization: Bearer {token}"
    echo "3. Token expires in 30 min"
    echo "4. POST /auth/refresh to renew"
    echo ""
}

section_enums() {
    echo "# Enums"
    echo ""
    echo "## Platforms"
    echo "twitter, instagram, telegram, linkedin, youtube, news, forum, custom"
    echo ""
    echo "## Analysis Types"
    echo "sentiment, emotion, summarization, topic_modeling, keyword_extraction, entity_recognition, trend_detection, graph_analysis, full"
    echo ""
    echo "## Analysis Status"
    echo "pending, queued, processing, completed, failed, cancelled"
    echo ""
    echo "## Sentiments"
    echo "positive, negative, neutral"
    echo ""
    echo "## Emotions"
    echo "joy, sadness, anger, fear, surprise, disgust"
    echo ""
    echo "## User Roles"
    echo "admin, analyst, viewer"
    echo ""
}

section_status() {
    echo "# Status"
    echo ""
    echo '```'
    docker ps --format "table {{.Names}}\t{{.Status}}" 2>/dev/null
    echo '```'
    echo ""
    echo "Backend:"
    echo '```json'
    curl -s http://localhost:8000/health 2>/dev/null || echo '{"status": "not running"}'
    echo '```'
    echo ""
    echo "BRAIN:"
    echo '```json'
    curl -s http://localhost:8001/health 2>/dev/null || echo '{"status": "not running"}'
    echo '```'
}

section_models() {
    echo "# Models"
    echo ""
    for f in "$PROJECT_ROOT"/backend/app/models/*.py; do
        name=$(basename "$f" .py)
        if [ "$name" != "__init__" ] && [ "$name" != "base" ]; then
            echo "## $name.py"
            echo '```python'
            cat "$f"
            echo '```'
            echo ""
        fi
    done
}

section_schemas() {
    echo "# Schemas"
    echo ""
    for f in "$PROJECT_ROOT"/backend/app/schemas/*.py; do
        name=$(basename "$f" .py)
        if [ "$name" != "__init__" ] && [ "$name" != "base" ]; then
            echo "## $name.py"
            echo '```python'
            cat "$f"
            echo '```'
            echo ""
        fi
    done
}

section_endpoints() {
    echo "# Endpoints"
    echo ""
    for f in "$PROJECT_ROOT"/backend/app/api/v1/endpoints/*.py; do
        name=$(basename "$f" .py)
        if [ "$name" != "__init__" ]; then
            echo "## $name.py"
            echo '```python'
            cat "$f"
            echo '```'
            echo ""
        fi
    done
}

section_services() {
    echo "# Services"
    echo ""
    for f in "$PROJECT_ROOT"/backend/app/services/*.py; do
        name=$(basename "$f" .py)
        if [ "$name" != "__init__" ] && [ "$name" != "base" ]; then
            echo "## $name.py"
            echo '```python'
            cat "$f"
            echo '```'
            echo ""
        fi
    done
}

section_core() {
    echo "# Core"
    echo ""
    for f in "$PROJECT_ROOT"/backend/app/core/*.py; do
        name=$(basename "$f" .py)
        if [ "$name" != "__init__" ]; then
            echo "## $name.py"
            echo '```python'
            cat "$f"
            echo '```'
            echo ""
        fi
    done
    echo "## main.py"
    echo '```python'
    cat "$PROJECT_ROOT/backend/app/main.py"
    echo '```'
}

section_brain() {
    echo "# BRAIN"
    echo ""
    echo "## main.py"
    echo '```python'
    cat "$PROJECT_ROOT/brain/app/main.py"
    echo '```'
    echo ""
    echo "## config.py"
    echo '```python'
    cat "$PROJECT_ROOT/brain/app/config.py"
    echo '```'
    echo ""
    echo "## mock_data.py"
    echo '```python'
    cat "$PROJECT_ROOT/brain/app/mock_data.py"
    echo '```'
    echo ""
    for f in "$PROJECT_ROOT"/brain/app/routers/*.py; do
        name=$(basename "$f" .py)
        if [ "$name" != "__init__" ]; then
            echo "## routers/$name.py"
            echo '```python'
            cat "$f"
            echo '```'
            echo ""
        fi
    done
}

section_docker() {
    echo "# Docker"
    echo ""
    echo "## backend/docker-compose.yml"
    echo '```yaml'
    cat "$PROJECT_ROOT/backend/docker-compose.yml"
    echo '```'
    echo ""
    echo "## brain/docker-compose.yml"
    echo '```yaml'
    cat "$PROJECT_ROOT/brain/docker-compose.yml"
    echo '```'
}

section_reqs() {
    echo "# Requirements"
    echo ""
    echo "## backend/requirements.txt"
    echo '```'
    cat "$PROJECT_ROOT/backend/requirements.txt"
    echo '```'
    echo ""
    echo "## brain/requirements.txt"
    echo '```'
    cat "$PROJECT_ROOT/brain/requirements.txt"
    echo '```'
}

section_frontend() {
    section_summary
    echo "---"
    section_tree
    echo "---"
    section_goals
    echo "---"
    section_api_list
    echo "---"
    section_api_examples
    echo "---"
    section_auth_flow
    echo "---"
    section_enums
    echo "---"
    section_status
}

section_all() {
    section_summary
    echo "---"
    section_tree
    echo "---"
    section_goals
    echo "---"
    section_api_list
    echo "---"
    section_enums
    echo "---"
    section_status
    echo "---"
    section_models
    echo "---"
    section_schemas
    echo "---"
    section_endpoints
    echo "---"
    section_services
    echo "---"
    section_core
    echo "---"
    section_brain
    echo "---"
    section_docker
    echo "---"
    section_reqs
}

case "$1" in
    summary)      section_summary ;;
    tree)         section_tree ;;
    goals)        section_goals ;;
    openapi)      section_openapi ;;
    api-list)     section_api_list ;;
    api-examples) section_api_examples ;;
    auth-flow)    section_auth_flow ;;
    enums)        section_enums ;;
    status)       section_status ;;
    models)       section_models ;;
    schemas)      section_schemas ;;
    endpoints)    section_endpoints ;;
    services)     section_services ;;
    core)         section_core ;;
    brain)        section_brain ;;
    docker)       section_docker ;;
    reqs)         section_reqs ;;
    frontend)     section_frontend ;;
    all)          section_all ;;
    *)            show_help ;;
esac
ENDSCRIPT