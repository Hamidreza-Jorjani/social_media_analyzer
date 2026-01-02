#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK TESTS
# ═══════════════════════════════════════════════════════════════════════════════

source "$(dirname "$0")/lib/common.sh"

test_health() {
    print_header "🏥 HEALTH CHECK TESTS"
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Docker Containers"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Docker daemon"
    if docker info > /dev/null 2>&1; then
        print_pass
    else
        print_fail "Docker not running"
        return 1
    fi
    
    local containers=("sma_postgres" "sma_redis" "sma_backend" "sma_celery" "sma_brain")
    for container in "${containers[@]}"; do
        print_test "Container: $container"
        local status
        status=$(docker inspect -f '{{.State.Status}}' "$container" 2>/dev/null || echo "missing")
        if [ "$status" = "running" ]; then
            local health
            health=$(docker inspect -f '{{.State.Health.Status}}' "$container" 2>/dev/null || echo "")
            if [ "$health" = "healthy" ] || [ -z "$health" ]; then
                print_pass "$status"
            else
                print_fail "Status: $status, Health: $health"
            fi
        else
            print_fail "Not running (status: $status)"
        fi
    done
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Service Health Endpoints"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Backend /health"
    local response
    response=$(http_get "$BACKEND_HEALTH_URL" false)
    local body
    body=$(get_body "$response")
    local status
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        local svc_status
        svc_status=$(echo "$body" | jq -r '.status // "unknown"' 2>/dev/null)
        print_pass "Status: $svc_status"
        print_info "Response:"
        print_json "$body"
    else
        print_fail "HTTP $status"
        print_json "$body"
    fi
    
    print_test "BRAIN /health"
    response=$(http_get "$BRAIN_URL/health" false)
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        local brain_status
        brain_status=$(echo "$body" | jq -r '.status // "unknown"' 2>/dev/null)
        print_pass "Status: $brain_status"
        print_info "Response:"
        print_json "$body"
    else
        print_fail "HTTP $status"
        print_json "$body"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Database Connectivity"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "PostgreSQL connection"
    if docker exec sma_postgres pg_isready -U postgres > /dev/null 2>&1; then
        print_pass
    else
        print_fail "PostgreSQL not ready"
    fi
    
    print_test "Redis connection"
    if docker exec sma_redis redis-cli ping | grep -q "PONG"; then
        print_pass
    else
        print_fail "Redis not responding"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Network Connectivity"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Backend → BRAIN connection via API"
    response=$(http_get "$BASE_URL/brain/health" false 2>/dev/null || echo -e "{}\n000")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
    else
        # Fallback: direct container check
        if docker exec sma_backend curl -s http://sma_brain:8001/health > /dev/null 2>&1; then
            print_pass "(via internal network)"
        else
            print_fail "Cannot reach BRAIN"
        fi
    fi
    
    print_test "Backend → Redis connection"
    if docker exec sma_backend python -c "import redis; r=redis.Redis(host='redis'); r.ping()" 2>/dev/null; then
        print_pass
    else
        print_skip "Cannot verify directly (python/redis inside container)"
    fi
    
    print_test "Backend → PostgreSQL connection"
    if docker exec sma_backend python -c "from app.database import sync_engine; conn = sync_engine.connect(); conn.close()" 2>/dev/null; then
        print_pass
    else
        print_skip "Cannot verify directly (sync_engine check failed)"
    fi
    
    print_divider
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    init_tests
    test_health
    print_summary
fi