#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════════
# COMMON TEST LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════

# Colors
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export CYAN='\033[0;36m'
export MAGENTA='\033[0;35m'
export WHITE='\033[1;37m'
export GRAY='\033[0;90m'
export NC='\033[0m'

# Bold variants
export BOLD='\033[1m'
export DIM='\033[2m'

# URLs
# URLs / Ports
export BACKEND_PORT="${BACKEND_PORT:-18000}"
export BRAIN_PORT="${BRAIN_PORT:-18001}"

export BACKEND_URL="${BACKEND_URL:-http://localhost:${BACKEND_PORT}}"
export BASE_URL="${BASE_URL:-${BACKEND_URL}/api/v1}"
export BRAIN_URL="${BRAIN_URL:-http://localhost:${BRAIN_PORT}}"
export BACKEND_HEALTH_URL="${BACKEND_HEALTH_URL:-${BACKEND_URL}/health}"
# Test state
export TESTS_PASSED=0
export TESTS_FAILED=0
export TESTS_SKIPPED=0
export TOKEN=""

# Results file
export RESULTS_DIR="tests/results"
export RESULTS_FILE="$RESULTS_DIR/test_results_$(date +%Y%m%d_%H%M%S).json"

# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

print_header() {
    local title="$1"
    local width=60
    echo ""
    echo -e "${BLUE}╔$(printf '═%.0s' $(seq 1 $width))╗${NC}"
    printf "${BLUE}║${WHITE}${BOLD}%*s${NC}${BLUE}%*s║${NC}\n" $(((width + ${#title}) / 2)) "$title" $(((width - ${#title}) / 2)) ""
    echo -e "${BLUE}╚$(printf '═%.0s' $(seq 1 $width))╝${NC}"
    echo ""
}

print_section() {
    local title="$1"
    echo ""
    echo -e "${YELLOW}┏━━━ ${WHITE}${BOLD}$title${NC}${YELLOW} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓${NC}"
}

print_subsection() {
    local title="$1"
    echo -e "${CYAN}  ┌─ ${title}${NC}"
}

print_test() {
    local name="$1"
    echo -ne "${GRAY}  │ Testing: ${WHITE}$name${NC}... "
}

print_pass() {
    local msg="${1:-}"
    echo -e "${GREEN}✓ PASS${NC} ${DIM}$msg${NC}"
    ((TESTS_PASSED++))
}

print_fail() {
    local msg="${1:-}"
    echo -e "${RED}✗ FAIL${NC} ${RED}$msg${NC}"
    ((TESTS_FAILED++))
}

print_skip() {
    local msg="${1:-}"
    echo -e "${YELLOW}⊘ SKIP${NC} ${DIM}$msg${NC}"
    ((TESTS_SKIPPED++))
}

print_info() {
    local msg="$1"
    echo -e "${GRAY}  │ ${CYAN}ℹ${NC} $msg"
}

print_json() {
    local json="$1"
    local indent="${2:-  │   }"
    echo "$json" | jq -C '.' 2>/dev/null | sed "s/^/${indent}/" || echo "${indent}$json"
}

print_json_compact() {
    local json="$1"
    local fields="$2"
    echo "$json" | jq -C "$fields" 2>/dev/null || echo "$json"
}

print_divider() {
    echo -e "${GRAY}  └────────────────────────────────────────────────────────${NC}"
}

print_summary() {
    local total=$((TESTS_PASSED + TESTS_FAILED + TESTS_SKIPPED))
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}                    ${BOLD}TEST SUMMARY${NC}                            ${BLUE}║${NC}"
    echo -e "${BLUE}╠════════════════════════════════════════════════════════════╣${NC}"
    printf "${BLUE}║${NC}   ${GREEN}✓ Passed:${NC}  %-5s                                       ${BLUE}║${NC}\n" "$TESTS_PASSED"
    printf "${BLUE}║${NC}   ${RED}✗ Failed:${NC}  %-5s                                       ${BLUE}║${NC}\n" "$TESTS_FAILED"
    printf "${BLUE}║${NC}   ${YELLOW}⊘ Skipped:${NC} %-5s                                       ${BLUE}║${NC}\n" "$TESTS_SKIPPED"
    printf "${BLUE}║${NC}   ${WHITE}Total:${NC}    %-5s                                       ${BLUE}║${NC}\n" "$total"
    echo -e "${BLUE}╠════════════════════════════════════════════════════════════╣${NC}"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${BLUE}║${NC}              ${GREEN}${BOLD}🎉 ALL TESTS PASSED! 🎉${NC}                      ${BLUE}║${NC}"
    else
        echo -e "${BLUE}║${NC}              ${RED}${BOLD}⚠️  SOME TESTS FAILED ⚠️${NC}                     ${BLUE}║${NC}"
    fi
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
}

# ─────────────────────────────────────────────────────────────────────────────
# HTTP FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

http_get() {
    local url="$1"
    local auth="${2:-true}"
    
    if [ "$auth" = "true" ] && [ -n "$TOKEN" ]; then
        curl -s -w "\n%{http_code}" "$url" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json"
    else
        curl -s -w "\n%{http_code}" "$url" \
            -H "Content-Type: application/json"
    fi
}

http_post() {
    local url="$1"
    local data="$2"
    local auth="${3:-true}"
    
    if [ "$auth" = "true" ] && [ -n "$TOKEN" ]; then
        curl -s -w "\n%{http_code}" -X POST "$url" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -w "\n%{http_code}" -X POST "$url" \
            -H "Content-Type: application/json" \
            -d "$data"
    fi
}

http_put() {
    local url="$1"
    local data="$2"
    
    curl -s -w "\n%{http_code}" -X PUT "$url" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d "$data"
}

http_delete() {
    local url="$1"
    
    curl -s -w "\n%{http_code}" -X DELETE "$url" \
        -H "Authorization: Bearer $TOKEN"
}

# Parse response and status code
parse_response() {
    local response="$1"
    local body=$(echo "$response" | sed '$d')
    local status=$(echo "$response" | tail -n 1)
    echo "$body"
    return $status
}

get_status_code() {
    local response="$1"
    echo "$response" | tail -n 1
}

get_body() {
    local response="$1"
    echo "$response" | sed '$d'
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSERTION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

assert_status() {
    local response="$1"
    local expected="$2"
    local actual=$(get_status_code "$response")
    
    if [ "$actual" = "$expected" ]; then
        return 0
    else
        return 1
    fi
}

assert_json_field() {
    local json="$1"
    local field="$2"
    local expected="$3"
    local actual=$(echo "$json" | jq -r "$field" 2>/dev/null)
    
    if [ "$actual" = "$expected" ]; then
        return 0
    else
        return 1
    fi
}

assert_json_exists() {
    local json="$1"
    local field="$2"
    local value=$(echo "$json" | jq -r "$field" 2>/dev/null)
    
    if [ -n "$value" ] && [ "$value" != "null" ]; then
        return 0
    else
        return 1
    fi
}

assert_json_array_not_empty() {
    local json="$1"
    local field="${2:-.}"
    local length=$(echo "$json" | jq -r "$field | length" 2>/dev/null)
    
    if [ "$length" -gt 0 ] 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
# AUTH FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

login() {
    local username="${1:-admin}"
    local password="${2:-Admin123!}"
    
    local response=$(http_post "$BASE_URL/auth/login" \
        "{\"username\": \"$username\", \"password\": \"$password\"}" false)
    
    local body=$(get_body "$response")
    TOKEN=$(echo "$body" | jq -r '.tokens.access_token // .access_token // empty' 2>/dev/null)
    
    if [ -n "$TOKEN" ]; then
        return 0
    else
        return 1
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

wait_for_service() {
    local url="$1"
    local max_attempts="${2:-30}"
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" > /dev/null 2>&1; then
            return 0
        fi
        sleep 1
        ((attempt++))
    done
    return 1
}

generate_uuid() {
    cat /proc/sys/kernel/random/uuid 2>/dev/null || \
    python3 -c "import uuid; print(uuid.uuid4())" 2>/dev/null || \
    echo "test-$(date +%s)-$RANDOM"
}

# Check dependencies
check_dependencies() {
    local missing=()
    
    if ! command -v jq &> /dev/null; then
        missing+=("jq")
    fi
    
    if ! command -v curl &> /dev/null; then
        missing+=("curl")
    fi
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${RED}Missing dependencies: ${missing[*]}${NC}"
        echo "Installing..."
        sudo apt-get update && sudo apt-get install -y "${missing[@]}"
    fi
}

# Initialize test environment
init_tests() {
    check_dependencies
    mkdir -p "$RESULTS_DIR"
    
    # Reset counters
    TESTS_PASSED=0
    TESTS_FAILED=0
    TESTS_SKIPPED=0
}

export -f print_header print_section print_subsection print_test
export -f print_pass print_fail print_skip print_info print_json
export -f print_json_compact print_divider print_summary
export -f http_get http_post http_put http_delete
export -f parse_response get_status_code get_body
export -f assert_status assert_json_field assert_json_exists assert_json_array_not_empty
export -f login wait_for_service generate_uuid check_dependencies init_tests
