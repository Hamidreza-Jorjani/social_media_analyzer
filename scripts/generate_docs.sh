#!/bin/bash

PROJECT_ROOT=~/projects/social_media_analyzer
OUTPUT_FILE="$PROJECT_ROOT/PROJECT_FULL_CONTEXT.md"

echo "Generating full documentation..."

# Header
cat > "$OUTPUT_FILE" << 'HEADER'
# Persian Social Media Analyzer - Full Context

## Quick Info
- **Architecture:** Frontend:3000 -> Backend:8000 -> BRAIN:8001
- **Database:** PostgreSQL:5432, Redis:6379
- **Credentials:** admin / Admin123!
- **Docs:** http://localhost:8000/docs

HEADER

# Tree
echo "## Project Structure" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
tree -I '__pycache__|*.pyc|.git|venv|node_modules' --dirsfirst "$PROJECT_ROOT" 2>/dev/null >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Models
echo "## Database Models" >> "$OUTPUT_FILE"
for f in "$PROJECT_ROOT"/backend/app/models/*.py; do
    name=$(basename "$f" .py)
    if [ "$name" != "__init__" ] && [ "$name" != "base" ]; then
        echo "### $name.py" >> "$OUTPUT_FILE"
        echo '```python' >> "$OUTPUT_FILE"
        cat "$f" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

# Schemas
echo "## Schemas" >> "$OUTPUT_FILE"
for f in "$PROJECT_ROOT"/backend/app/schemas/*.py; do
    name=$(basename "$f" .py)
    if [ "$name" != "__init__" ] && [ "$name" != "base" ]; then
        echo "### $name.py" >> "$OUTPUT_FILE"
        echo '```python' >> "$OUTPUT_FILE"
        cat "$f" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

# Endpoints
echo "## API Endpoints" >> "$OUTPUT_FILE"
for f in "$PROJECT_ROOT"/backend/app/api/v1/endpoints/*.py; do
    name=$(basename "$f" .py)
    if [ "$name" != "__init__" ]; then
        echo "### $name.py" >> "$OUTPUT_FILE"
        echo '```python' >> "$OUTPUT_FILE"
        cat "$f" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

# Services
echo "## Services" >> "$OUTPUT_FILE"
for f in "$PROJECT_ROOT"/backend/app/services/*.py; do
    name=$(basename "$f" .py)
    if [ "$name" != "__init__" ] && [ "$name" != "base" ]; then
        echo "### $name.py" >> "$OUTPUT_FILE"
        echo '```python' >> "$OUTPUT_FILE"
        cat "$f" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

# Core
echo "## Core" >> "$OUTPUT_FILE"
for f in "$PROJECT_ROOT"/backend/app/core/*.py; do
    name=$(basename "$f" .py)
    if [ "$name" != "__init__" ]; then
        echo "### $name.py" >> "$OUTPUT_FILE"
        echo '```python' >> "$OUTPUT_FILE"
        cat "$f" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

# Main files
echo "## Main Files" >> "$OUTPUT_FILE"
echo "### main.py" >> "$OUTPUT_FILE"
echo '```python' >> "$OUTPUT_FILE"
cat "$PROJECT_ROOT/backend/app/main.py" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "### database.py" >> "$OUTPUT_FILE"
echo '```python' >> "$OUTPUT_FILE"
cat "$PROJECT_ROOT/backend/app/database.py" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# BRAIN
echo "## BRAIN Service" >> "$OUTPUT_FILE"
echo "### main.py" >> "$OUTPUT_FILE"
echo '```python' >> "$OUTPUT_FILE"
cat "$PROJECT_ROOT/brain/app/main.py" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "### config.py" >> "$OUTPUT_FILE"
echo '```python' >> "$OUTPUT_FILE"
cat "$PROJECT_ROOT/brain/app/config.py" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "### mock_data.py" >> "$OUTPUT_FILE"
echo '```python' >> "$OUTPUT_FILE"
cat "$PROJECT_ROOT/brain/app/mock_data.py" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

for f in "$PROJECT_ROOT"/brain/app/routers/*.py; do
    name=$(basename "$f" .py)
    if [ "$name" != "__init__" ]; then
        echo "### routers/$name.py" >> "$OUTPUT_FILE"
        echo '```python' >> "$OUTPUT_FILE"
        cat "$f" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    fi
done

# Docker
echo "## Docker" >> "$OUTPUT_FILE"
echo "### backend/docker-compose.yml" >> "$OUTPUT_FILE"
echo '```yaml' >> "$OUTPUT_FILE"
cat "$PROJECT_ROOT/backend/docker-compose.yml" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "### brain/docker-compose.yml" >> "$OUTPUT_FILE"
echo '```yaml' >> "$OUTPUT_FILE"
cat "$PROJECT_ROOT/brain/docker-compose.yml" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Requirements
echo "## Requirements" >> "$OUTPUT_FILE"
echo "### backend/requirements.txt" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
cat "$PROJECT_ROOT/backend/requirements.txt" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "### brain/requirements.txt" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
cat "$PROJECT_ROOT/brain/requirements.txt" >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# OpenAPI
echo "## OpenAPI Specification" >> "$OUTPUT_FILE"
echo '```json' >> "$OUTPUT_FILE"
curl -s http://localhost:8000/api/v1/openapi.json >> "$OUTPUT_FILE" 2>/dev/null || echo '{"error": "Backend not running"}' >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"

# Summary
echo ""
echo "✅ Done!"
echo "   File: $OUTPUT_FILE"
echo "   Lines: $(wc -l < "$OUTPUT_FILE")"
echo "   Size: $(du -h "$OUTPUT_FILE" | cut -f1)"
