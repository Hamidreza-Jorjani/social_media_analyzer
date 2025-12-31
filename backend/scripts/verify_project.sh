#!/bin/bash

echo "=========================================="
echo "Persian Social Analytics - Project Verification"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 (missing)"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/ (missing)"
        return 1
    fi
}

echo "Checking project structure..."
echo ""

echo "=== Root Files ==="
check_file "requirements.txt"
check_file "Dockerfile"
check_file "docker-compose.yml"
check_file "docker-compose.dev.yml"
check_file ".env.example"
check_file ".gitignore"
check_file ".dockerignore"
check_file "alembic.ini"
check_file "pytest.ini"
check_file "README.md"

echo ""
echo "=== App Directory ==="
check_dir "app"
check_file "app/__init__.py"
check_file "app/main.py"
check_file "app/database.py"

echo ""
echo "=== Core ==="
check_dir "app/core"
check_file "app/core/__init__.py"
check_file "app/core/config.py"
check_file "app/core/security.py"

echo ""
echo "=== API ==="
check_dir "app/api"
check_file "app/api/__init__.py"
check_file "app/api/deps.py"
check_dir "app/api/v1"
check_file "app/api/v1/__init__.py"
check_file "app/api/v1/router.py"
check_dir "app/api/v1/endpoints"
check_file "app/api/v1/endpoints/__init__.py"
check_file "app/api/v1/endpoints/auth.py"
check_file "app/api/v1/endpoints/users.py"
check_file "app/api/v1/endpoints/data_sources.py"
check_file "app/api/v1/endpoints/authors.py"
check_file "app/api/v1/endpoints/posts.py"
check_file "app/api/v1/endpoints/analysis.py"
check_file "app/api/v1/endpoints/trends.py"
check_file "app/api/v1/endpoints/graph.py"
check_file "app/api/v1/endpoints/dashboard.py"
check_file "app/api/v1/endpoints/brain.py"

echo ""
echo "=== Models ==="
check_dir "app/models"
check_file "app/models/__init__.py"
check_file "app/models/base.py"
check_file "app/models/user.py"
check_file "app/models/data_source.py"
check_file "app/models/author.py"
check_file "app/models/post.py"
check_file "app/models/analysis.py"
check_file "app/models/analysis_result.py"
check_file "app/models/trend.py"
check_file "app/models/graph.py"
check_file "app/models/dashboard.py"

echo ""
echo "=== Schemas ==="
check_dir "app/schemas"
check_file "app/schemas/__init__.py"
check_file "app/schemas/base.py"
check_file "app/schemas/user.py"
check_file "app/schemas/auth.py"
check_file "app/schemas/data_source.py"
check_file "app/schemas/author.py"
check_file "app/schemas/post.py"
check_file "app/schemas/analysis.py"
check_file "app/schemas/analysis_result.py"
check_file "app/schemas/trend.py"
check_file "app/schemas/graph.py"
check_file "app/schemas/dashboard.py"
check_file "app/schemas/brain.py"

echo ""
echo "=== CRUD ==="
check_dir "app/crud"
check_file "app/crud/__init__.py"
check_file "app/crud/base.py"
check_file "app/crud/crud_user.py"
check_file "app/crud/crud_data_source.py"
check_file "app/crud/crud_author.py"
check_file "app/crud/crud_post.py"
check_file "app/crud/crud_analysis.py"
check_file "app/crud/crud_analysis_result.py"
check_file "app/crud/crud_trend.py"
check_file "app/crud/crud_graph.py"
check_file "app/crud/crud_dashboard.py"

echo ""
echo "=== Services ==="
check_dir "app/services"
check_file "app/services/__init__.py"
check_file "app/services/base.py"
check_file "app/services/redis_service.py"
check_file "app/services/brain_service.py"
check_file "app/services/analysis_service.py"
check_file "app/services/graph_service.py"
check_file "app/services/trend_service.py"
check_file "app/services/auth_service.py"
check_file "app/services/dashboard_service.py"
check_file "app/services/celery_app.py"
check_file "app/services/tasks.py"

echo ""
echo "=== Utils ==="
check_dir "app/utils"
check_file "app/utils/__init__.py"
check_file "app/utils/text.py"
check_file "app/utils/datetime.py"
check_file "app/utils/pagination.py"
check_file "app/utils/validators.py"
check_file "app/utils/security.py"
check_file "app/utils/json.py"

echo ""
echo "=== Alembic ==="
check_dir "alembic"
check_file "alembic/env.py"
check_file "alembic/script.py.mako"
check_dir "alembic/versions"

echo ""
echo "=== Scripts ==="
check_dir "scripts"
check_file "scripts/start.sh"
check_file "scripts/stop.sh"
check_file "scripts/init_db.py"
check_file "scripts/seed_data.py"
check_file "scripts/run_dev.sh"
check_file "scripts/run_celery.sh"
check_file "scripts/run_celery_beat.sh"
check_file "scripts/migrate.sh"
check_file "scripts/run_tests.sh"

echo ""
echo "=== Tests ==="
check_dir "tests"
check_file "tests/__init__.py"
check_file "tests/conftest.py"
check_file "tests/test_utils.py"
check_file "tests/test_models.py"
check_file "tests/test_crud.py"
check_file "tests/test_api.py"
check_file "tests/test_schemas.py"

echo ""
echo "=========================================="
echo "Verification Complete!"
echo "=========================================="
