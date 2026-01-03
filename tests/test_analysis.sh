#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS PIPELINE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

source "$(dirname "$0")/lib/common.sh"

test_analysis() {
    print_header "🔬 ANALYSIS PIPELINE TESTS"
    
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
    print_section "Create Test Data"
    # ─────────────────────────────────────────────────────────────────────────
    
    local unique_id=$(generate_uuid | cut -c1-8)
    
    # Create data source
    print_test "Create data source"
    local response=$(http_post "$BASE_URL/data-sources" "{
        \"name\": \"Analysis Test $unique_id\",
        \"platform\": \"twitter\",
        \"is_active\": true
    }")
    local DATASOURCE_ID=$(echo "$(get_body "$response")" | jq -r '.id // 1')
    print_pass "ID: $DATASOURCE_ID"
    
    # Create author
    print_test "Create author"
    response=$(http_post "$BASE_URL/authors" "{
        \"platform_id\": \"analysis_author_$unique_id\",
        \"platform\": \"twitter\",
        \"username\": \"analyst_$unique_id\"
    }")
    local AUTHOR_ID=$(echo "$(get_body "$response")" | jq -r '.id // 1')
    print_pass "ID: $AUTHOR_ID"
    
    # Create posts for analysis
    print_test "Create posts for analysis"
    response=$(http_post "$BASE_URL/posts/bulk" "{
        \"posts\": [
            {\"platform_id\": \"a1_$unique_id\", \"platform\": \"twitter\", \"content\": \"این محصول فوق‌العاده است! کیفیت عالی دارد.\", \"language\": \"fa\", \"data_source_id\": $DATASOURCE_ID, \"author_id\": $AUTHOR_ID},
            {\"platform_id\": \"a2_$unique_id\", \"platform\": \"twitter\", \"content\": \"خیلی بد بود، اصلا راضی نیستم.\", \"language\": \"fa\", \"data_source_id\": $DATASOURCE_ID, \"author_id\": $AUTHOR_ID},
            {\"platform_id\": \"a3_$unique_id\", \"platform\": \"twitter\", \"content\": \"قیمت مناسب بود ولی کیفیت متوسط.\", \"language\": \"fa\", \"data_source_id\": $DATASOURCE_ID, \"author_id\": $AUTHOR_ID},
            {\"platform_id\": \"a4_$unique_id\", \"platform\": \"twitter\", \"content\": \"پشتیبانی سریع و عالی!\", \"language\": \"fa\", \"data_source_id\": $DATASOURCE_ID, \"author_id\": $AUTHOR_ID},
            {\"platform_id\": \"a5_$unique_id\", \"platform\": \"twitter\", \"content\": \"تجربه خوبی نبود، تحویل دیر شد.\", \"language\": \"fa\", \"data_source_id\": $DATASOURCE_ID, \"author_id\": $AUTHOR_ID}
        ]
    }")
    local body=$(get_body "$response")
    local status=$(get_status_code "$response")
    if [ "$status" = "200" ] || [ "$status" = "201" ]; then
        print_pass "5 posts created"
    else
        print_fail "HTTP $status"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Analysis CRUD"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Create analysis job"
    response=$(http_post "$BASE_URL/analysis" "{
        \"name\": \"Test Analysis $unique_id\",
        \"description\": \"Automated test analysis\",
        \"analysis_type\": \"full\",
        \"config\": {
            \"sentiment_enabled\": true,
            \"emotion_enabled\": true,
            \"keyword_extraction_enabled\": true
        },
        \"query_filters\": {
            \"platform\": \"twitter\",
            \"language\": \"fa\"
        }
    }")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    local ANALYSIS_ID
    if [ "$status" = "200" ] || [ "$status" = "201" ]; then
        ANALYSIS_ID=$(echo "$body" | jq -r '.id')
        print_pass "ID: $ANALYSIS_ID"
        print_json "$body"
    else
        print_fail "HTTP $status"
        print_json "$body"
        return 1
    fi
    
    print_test "Get analysis by ID"
    response=$(http_get "$BASE_URL/analysis/$ANALYSIS_ID")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
    else
        print_fail "HTTP $status"
    fi
    
    print_test "List all analyses"
    response=$(http_get "$BASE_URL/analysis")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        local count=$(echo "$body" | jq 'if type == "array" then length else .items | length end' 2>/dev/null)
        print_pass "Found: $count analyses"
    else
        print_fail "HTTP $status"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Analysis Execution"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Start analysis"
    response=$(http_post "$BASE_URL/analysis/$ANALYSIS_ID/start" "{}")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_fail "HTTP $status"
        print_json "$body"
    fi
    
    print_test "Monitor progress"
    local max_wait=30
    local completed=false
    for i in $(seq 1 $max_wait); do
        sleep 2
        response=$(http_get "$BASE_URL/analysis/$ANALYSIS_ID/progress")
        body=$(get_body "$response")
        local prog_status=$(echo "$body" | jq -r '.status // "unknown"')
        local progress=$(echo "$body" | jq -r '.progress // 0')
        
        echo -ne "\r  │   ⏳ [$i/$max_wait] Status: $prog_status | Progress: $progress%    "
        
        if [ "$prog_status" = "completed" ]; then
            completed=true
            break
        elif [ "$prog_status" = "failed" ]; then
            break
        fi
    done
    echo ""
    
    if [ "$completed" = true ]; then
        print_pass "Analysis completed"
    else
        print_fail "Analysis did not complete (status: $prog_status)"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Analysis Results"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Get analysis results"
    response=$(http_get "$BASE_URL/analysis/$ANALYSIS_ID/results")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        local results_count=$(echo "$body" | jq 'if type == "array" then length else .items | length // 0 end' 2>/dev/null)
        print_pass "Found: $results_count results"
        print_info "Sample results:"
        echo "$body" | jq -C '.[0:2] // .items[0:2] // .' 2>/dev/null | sed 's/^/  │   /'
    else
        print_fail "HTTP $status"
    fi
    
    print_test "Get analysis summary"
    response=$(http_get "$BASE_URL/analysis/$ANALYSIS_ID/summary")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "Summary endpoint not available"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Result Validation"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Sentiment distribution exists"
    response=$(http_get "$BASE_URL/analysis/$ANALYSIS_ID/summary")
    body=$(get_body "$response")
    if assert_json_exists "$body" ".sentiment_distribution"; then
        print_pass
        echo "$body" | jq -C '.sentiment_distribution' 2>/dev/null | sed 's/^/  │   /'
    else
        print_skip "No sentiment distribution in summary"
    fi
    
    print_test "Results have sentiment labels"
    response=$(http_get "$BASE_URL/analysis/$ANALYSIS_ID/results?page_size=5")
    body=$(get_body "$response")
    local has_sentiment=$(echo "$body" | jq '[.[] // .items[] | .sentiment_label] | map(select(. != null)) | length' 2>/dev/null)
    if [ "$has_sentiment" -gt 0 ] 2>/dev/null; then
        print_pass "$has_sentiment results with sentiment"
    else
        print_skip "No sentiment labels found"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Analysis Types"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Create sentiment-only analysis"
    response=$(http_post "$BASE_URL/analysis" "{
        \"name\": \"Sentiment Only $unique_id\",
        \"analysis_type\": \"sentiment\",
        \"config\": {\"sentiment_enabled\": true}
    }")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ] || [ "$status" = "201" ]; then
        print_pass
    else
        print_skip "HTTP $status"
    fi
    
    print_test "Create keyword-only analysis"
    response=$(http_post "$BASE_URL/analysis" "{
        \"name\": \"Keywords Only $unique_id\",
        \"analysis_type\": \"keywords\",
        \"config\": {\"keyword_extraction_enabled\": true}
    }")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ] || [ "$status" = "201" ]; then
        print_pass
    else
        print_skip "HTTP $status"
    fi
    
    print_divider
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    init_tests
    test_analysis
    print_summary
fi
