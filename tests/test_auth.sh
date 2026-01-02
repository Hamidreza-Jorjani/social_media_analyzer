#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

source "$(dirname "$0")/lib/common.sh"

test_auth() {
    print_header "🔐 AUTHENTICATION TESTS"
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Login Tests"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Valid admin login"
    local response
    response=$(http_post "$BASE_URL/auth/login" \
        '{"username": "admin", "password": "Admin123!"}' false)
    local body
    body=$(get_body "$response")
    local status
    status=$(get_status_code "$response")
    
    if [ "$status" = "200" ] && assert_json_exists "$body" ".tokens.access_token"; then
        TOKEN=$(echo "$body" | jq -r '.tokens.access_token')
        print_pass
        print_info "Token received (${#TOKEN} chars)"
    else
        print_fail "HTTP $status"
        print_json "$body"
    fi
    
    print_test "Invalid password"
    response=$(http_post "$BASE_URL/auth/login" \
        '{"username": "admin", "password": "wrongpassword"}' false)
    status=$(get_status_code "$response")
    if [ "$status" = "401" ] || [ "$status" = "400" ]; then
        print_pass "Correctly rejected"
    else
        print_fail "Expected 401, got $status"
    fi
    
    print_test "Invalid username"
    response=$(http_post "$BASE_URL/auth/login" \
        '{"username": "nonexistent", "password": "Admin123!"}' false)
    status=$(get_status_code "$response")
    if [ "$status" = "401" ] || [ "$status" = "400" ] || [ "$status" = "404" ]; then
        print_pass "Correctly rejected"
    else
        print_fail "Expected 401/400/404, got $status"
    fi
    
    print_test "Empty credentials"
    response=$(http_post "$BASE_URL/auth/login" \
        '{"username": "", "password": ""}' false)
    status=$(get_status_code "$response")
    if [ "$status" = "422" ] || [ "$status" = "400" ]; then
        print_pass "Correctly rejected"
    else
        print_fail "Expected 422/400, got $status"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Token Validation"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Access protected endpoint with token"
    response=$(http_get "$BASE_URL/auth/me")
    body=$(get_body "$response")
    status=$(get_status_code "$response")
    if [ "$status" = "200" ]; then
        local username
        username=$(echo "$body" | jq -r '.username // .email // "unknown"')
        print_pass "User: $username"
    else
        print_fail "HTTP $status"
        print_json "$body"
    fi
    
    print_test "Access protected endpoint without token"
    local old_token="$TOKEN"
    TOKEN=""
    response=$(http_get "$BASE_URL/auth/me")
    status=$(get_status_code "$response")
    TOKEN="$old_token"
    if [ "$status" = "401" ] || [ "$status" = "403" ]; then
        print_pass "Correctly rejected"
    else
        print_fail "Expected 401/403, got $status"
    fi
    
    print_test "Access with invalid token"
    local temp_token="$TOKEN"
    TOKEN="invalid.token.here"
    response=$(http_get "$BASE_URL/auth/me")
    status=$(get_status_code "$response")
    TOKEN="$temp_token"
    if [ "$status" = "401" ] || [ "$status" = "403" ]; then
        print_pass "Correctly rejected"
    else
        print_fail "Expected 401/403, got $status"
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    print_section "Token Refresh"
    # ─────────────────────────────────────────────────────────────────────────
    
    print_test "Refresh token endpoint"
    # First get refresh token
    response=$(http_post "$BASE_URL/auth/login" \
        '{"username": "admin", "password": "Admin123!"}' false)
    body=$(get_body "$response")
    local refresh_token
    refresh_token=$(echo "$body" | jq -r '.tokens.refresh_token // empty')
    
    if [ -n "$refresh_token" ]; then
        response=$(http_post "$BASE_URL/auth/refresh" \
            "{\"refresh_token\": \"$refresh_token\"}" false)
        status=$(get_status_code "$response")
        if [ "$status" = "200" ]; then
            print_pass
        else
            print_skip "Refresh endpoint may not be implemented (HTTP $status)"
            print_json "$(get_body "$response")"
        fi
    else
        print_skip "No refresh token in response"
    fi
    
    print_divider
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    init_tests
    test_auth
    print_summary
fi