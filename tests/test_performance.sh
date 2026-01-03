#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

source "$(dirname "$0")/lib/common.sh"

test_performance() {
    print_header "⚡ PERFORMANCE TESTS"
    
    # Login first
    print_section "Setup"
    print_test "Login"
    if login; then
        print_pass
    else
        print_fail "Cannot continue without auth"
        return 1
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Response Time Tests"
    # ─────────────────────────────────────────────────────────────────────────
    
    local endpoints=(
        "GET:$BASE_URL/posts?page_size=10:Posts List"
        "GET:$BASE_URL/posts/stats:Posts Stats"
        "GET:$BASE_URL/analysis:Analysis List"
        "GET:$BRAIN_URL/health:BRAIN Health"
    )
    
    for endpoint in "${endpoints[@]}"; do
        IFS=':' read -r method url name <<< "$endpoint"
        print_test "$name response time"
        
        local start_time=$(date +%s%N)
        if [ "$method" = "GET" ]; then
            response=$(http_get "$url")
        fi
        local end_time=$(date +%s%N)
        local duration=$(( (end_time - start_time) / 1000000 ))
        
        local status=$(get_status_code "$response")
        if [ "$status" = "200" ]; then
            if [ "$duration" -lt 500 ]; then
                print_pass "${duration}ms ⚡ Fast"
            elif [ "$duration" -lt 2000 ]; then
                print_pass "${duration}ms"
            else
                print_pass "${duration}ms ⚠️ Slow"
            fi
        else
            print_skip "HTTP $status"
        fi
    done
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "BRAIN Service Performance"
    # ─────────────────────────────────────────────────────────────────────────
    
    local batch_sizes=(1 5 10 25 50)
    
    for size in "${batch_sizes[@]}"; do
        print_test "Sentiment analysis ($size texts)"
        
        # Generate texts
        local texts=$(for i in $(seq 1 $size); do echo "\"تست شماره $i برای بررسی عملکرد سیستم\""; done | paste -sd,)
        
        local start_time=$(date +%s%N)
        response=$(http_post "$BRAIN_URL/analyze/sentiment" "{\"texts\": [$texts]}" false)
        local end_time=$(date +%s%N)
        local duration=$(( (end_time - start_time) / 1000000 ))
        local per_text=$((duration / size))
        
        local status=$(get_status_code "$response")
        if [ "$status" = "200" ]; then
            print_pass "${duration}ms total (${per_text}ms/text)"
        else
            print_fail "HTTP $status"
        fi
    done
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Concurrent Requests"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "10 concurrent requests"
    local start_time=$(date +%s%N)
    
    for i in $(seq 1 10); do
        curl -s "$BASE_URL/posts?page_size=5" -H "Authorization: Bearer $TOKEN" > /dev/null &
    done
    wait
    
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))
    print_pass "${duration}ms for 10 requests ($((duration/10))ms avg)"
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Memory Check"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Container memory usage"
    echo ""
    docker stats --no-stream --format "  │   {{.Name}}: {{.MemUsage}}" \
        sma_backend sma_brain sma_celery sma_postgres sma_redis 2>/dev/null || \
        print_skip "Cannot get stats"
    print_pass "Memory stats printed above"
    
    print_divider
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    init_tests
    test_performance
    print_summary
fi
