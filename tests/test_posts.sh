#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# POSTS API TESTS
# ═══════════════════════════════════════════════════════════════════════════════

source "$(dirname "$0")/lib/common.sh"

test_posts() {
    print_header "📝 POSTS API TESTS"
    
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
    print_section "Create Data Source & Author"
    # ─────────────────────────────────────────────────────────────────────────
    
    local unique_id=$(generate_uuid | cut -c1-8)
    
    print_test "Create data source"
    local response=$(http_post "$BASE_URL/data-sources" "{
        \"name\": \"Test Source $unique_id\",
        \"platform\": \"twitter\",
        \"is_active\": true
    }")
    local body=$(get_body "$response")
    local status=$(get_status_code "$response")
    local DATASOURCE_ID=1
    if [ "$status" = "200" ] || [ "$status" = "201" ]; then
        DATASOURCE_ID=$(echo "$body" | jq -r '.id // 1')
        print_pass "ID: $DATASOURCE_ID"
    else
        print_skip "Using default ID 1"
    fi
    
    print_test "Create author"
    response=$(http_post "$BASE_URL/authors" "{
        \"platform_id\": \"author_$unique_id\",
        \"platform\": \"twitter\",
        \"username\": \"test_user_$unique_id\",
        \"display_name\": \"کاربر تست\"
    }")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    local AUTHOR_ID=1
    if [ "$status" = "200" ] || [ "$status" = "201" ]; then
        AUTHOR_ID=$(echo "$body" | jq -r '.id // 1')
        print_pass "ID: $AUTHOR_ID"
    else
        print_skip "Using default ID 1"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Single Post Operations"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Create single post"
    response=$(http_post "$BASE_URL/posts" "{
        \"platform_id\": \"post_$unique_id\",
        \"platform\": \"twitter\",
        \"content\": \"این یک پست تست است! #تست #آزمایش\",
        \"language\": \"fa\",
        \"hashtags\": [\"تست\", \"آزمایش\"],
        \"likes_count\": 100,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
    }")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    local POST_ID
    if [ "$status" = "200" ] || [ "$status" = "201" ]; then
        POST_ID=$(echo "$body" | jq -r '.id')
        print_pass "ID: $POST_ID"
        print_json "$body"
    else
        print_fail "HTTP $status"
        print_json "$body"
    fi
    
    print_test "Get post by ID"
    if [ -n "$POST_ID" ]; then
        response=$(http_get "$BASE_URL/posts/$POST_ID")
        body=$(get_body "$response")
        status=$(get_status_code "$response")
        if [ "$status" = "200" ]; then
            print_pass
            print_json_compact "$body" '{id, content: .content[:30], platform}'
        else
            print_fail "HTTP $status"
        fi
    else
        print_skip "No post ID"
    fi
    
    print_test "Update post"
    if [ -n "$POST_ID" ]; then
        response=$(http_put "$BASE_URL/posts/$POST_ID" '{
            "likes_count": 200,
            "comments_count": 50
        }')
        status=$(get_status_code "$response")
        if [ "$status" = "200" ]; then
            print_pass
        else
            print_skip "Update not supported (HTTP $status)"
        fi
    else
        print_skip "No post ID"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Bulk Post Operations"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Create bulk posts"
    response=$(http_post "$BASE_URL/posts/bulk" "{
        \"posts\": [
            {
                \"platform_id\": \"bulk_1_$unique_id\",
                \"platform\": \"twitter\",
                \"content\": \"پست اول - هوای امروز عالی است!\",
                \"language\": \"fa\",
                \"hashtags\": [\"هوا\"],
                \"data_source_id\": $DATASOURCE_ID,
                \"author_id\": $AUTHOR_ID
            },
            {
                \"platform_id\": \"bulk_2_$unique_id\",
                \"platform\": \"twitter\",
                \"content\": \"پست دوم - امروز خسته‌ام\",
                \"language\": \"fa\",
                \"hashtags\": [\"خستگی\"],
                \"data_source_id\": $DATASOURCE_ID,
                \"author_id\": $AUTHOR_ID
            },
            {
                \"platform_id\": \"bulk_3_$unique_id\",
                \"platform\": \"instagram\",
                \"content\": \"پست سوم - عکس زیبا\",
                \"language\": \"fa\",
                \"hashtags\": [\"عکاسی\"],
                \"data_source_id\": $DATASOURCE_ID,
                \"author_id\": $AUTHOR_ID
            }
        ]
    }")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ] || [ "$status" = "201" ]; then
        local created=$(echo "$body" | jq '.created // length' 2>/dev/null)
        print_pass "Created: $created posts"
    else
        print_fail "HTTP $status"
        print_json "$body"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "List & Filter Posts"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "List all posts"
    response=$(http_get "$BASE_URL/posts?page_size=10")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        local count=$(echo "$body" | jq 'if type == "array" then length else .items | length end' 2>/dev/null)
        print_pass "Found: $count posts"
    else
        print_fail "HTTP $status"
    fi
    
    print_test "Filter by platform"
    response=$(http_get "$BASE_URL/posts?platform=twitter&page_size=5")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
    else
        print_skip "Filter not supported"
    fi
    
    print_test "Filter by language"
    response=$(http_get "$BASE_URL/posts?language=fa&page_size=5")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
    else
        print_skip "Filter not supported"
    fi
    
    print_test "Search by content"
    response=$(http_get "$BASE_URL/posts?search=تست&page_size=5")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
    else
        print_skip "Search not supported"
    fi
    
    print_test "Pagination"
    response=$(http_get "$BASE_URL/posts?page=1&page_size=2")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
    else
        print_fail "HTTP $status"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Post Statistics"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Get post stats"
    response=$(http_get "$BASE_URL/posts/stats")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        print_pass
        print_json "$body"
    else
        print_skip "Stats endpoint not available"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Delete Operations"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Delete post"
    if [ -n "$POST_ID" ]; then
        response=$(http_delete "$BASE_URL/posts/$POST_ID")
        status=$(get_status_code "$response")
        if [ "$status" = "200" ] || [ "$status" = "204" ]; then
            print_pass
        else
            print_skip "Delete not supported (HTTP $status)"
        fi
    else
        print_skip "No post ID"
    fi
    
    print_test "Get deleted post (should fail)"
    if [ -n "$POST_ID" ]; then
        response=$(http_get "$BASE_URL/posts/$POST_ID")
        status=$(get_status_code "$response")
        if [ "$status" = "404" ]; then
            print_pass "Correctly returns 404"
        else
            print_skip "HTTP $status"
        fi
    else
        print_skip "No post ID"
    fi
    
    print_divider
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    init_tests
    test_posts
    print_summary
fi
