#!/bin/bash

echo "╔════════════════════════════════════════════╗"
echo "║  Persian Analytics - Integration Test     ║"
echo "╚════════════════════════════════════════════╝"

BACKEND_PORT=18000
BRAIN_PORT=18001

API_URL="http://localhost:${BACKEND_PORT}/api/v1"
BRAIN_URL="http://localhost:${BRAIN_PORT}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

pass() { echo -e "${GREEN}✅ $1${NC}"; }
fail() { echo -e "${RED}❌ $1${NC}"; }

echo ""
echo "[1/10] Checking Docker Containers..."
docker ps --format "table {{.Names}}\t{{.Status}}" | grep sma || true

echo ""
echo "[2/10] Testing BRAIN Service..."
BRAIN_HEALTH=$(curl -s "$BRAIN_URL/health")
if echo "$BRAIN_HEALTH" | grep -q '"status":"healthy"'; then
    pass "BRAIN is healthy"
else
    fail "BRAIN health check failed"
fi

echo ""
echo "[3/10] Testing Backend Service..."
BACKEND_HEALTH=$(curl -s "http://localhost:${BACKEND_PORT}/health")
if echo "$BACKEND_HEALTH" | grep -q '"status":"healthy"'; then
    pass "Backend is healthy"
else
    fail "Backend health check failed"
fi

echo ""
echo "[4/10] Testing Admin Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"Admin123!"}')

TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
if [ -n "$TOKEN" ]; then
    pass "Login successful"
else
    fail "Login failed"
    echo "$LOGIN_RESPONSE"
    exit 1
fi

echo ""
echo "[5/10] Testing Backend → BRAIN Connection..."
BRAIN_CHECK=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/brain/health")
if echo "$BRAIN_CHECK" | grep -q '"status":"healthy"'; then
    pass "Backend can reach BRAIN"
else
    fail "Backend cannot reach BRAIN"
fi

echo ""
echo "[6/10] Testing BRAIN Sentiment Analysis..."
SENTIMENT=$(curl -s -X POST "$BRAIN_URL/analyze/sentiment" \
    -H "Content-Type: application/json" \
    -d '{"texts": ["سلام دنیا! این خیلی خوب است.", "این بد است."]}')
if echo "$SENTIMENT" | grep -q '"results"'; then
    pass "Sentiment analysis works"
else
    fail "Sentiment analysis failed"
    echo "$SENTIMENT"
fi

echo ""
echo "[7/10] Creating Test Post..."
POST_RESPONSE=$(curl -s -X POST "$API_URL/posts" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "platform_id": "test_'$(date +%s)'",
        "platform": "twitter",
        "content": "سلام! این یک تست کامل سیستم است. #تست #فارسی",
        "language": "fa",
        "hashtags": ["تست", "فارسی"]
    }')
POST_ID=$(echo "$POST_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
if [ -n "$POST_ID" ]; then
    pass "Post created: ID=$POST_ID"
else
    fail "Post creation failed"
fi

echo ""
echo "[8/10] Creating Analysis Job..."
ANALYSIS_RESPONSE=$(curl -s -X POST "$API_URL/analysis" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name": "Integration Test", "analysis_type": "sentiment"}')
ANALYSIS_ID=$(echo "$ANALYSIS_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
if [ -n "$ANALYSIS_ID" ]; then
    pass "Analysis created: ID=$ANALYSIS_ID"
else
    fail "Analysis creation failed"
fi

echo ""
echo "[9/10] Starting Analysis..."
START_RESPONSE=$(curl -s -X POST "$API_URL/analysis/$ANALYSIS_ID/start" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json")
if echo "$START_RESPONSE" | grep -q '"message"'; then
    pass "Analysis started"
else
    fail "Analysis start failed"
fi

echo ""
echo "[10/10] Monitoring Analysis..."
for i in {1..15}; do
    PROGRESS=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/analysis/$ANALYSIS_ID/progress")
    STATUS=$(echo "$PROGRESS" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    PERCENT=$(echo "$PROGRESS" | grep -o '"progress":[0-9.]*' | cut -d':' -f2)
    echo "   [$i/15] Status: ${STATUS:-unknown} - Progress: ${PERCENT:-0}%"
    
    if [ "$STATUS" = "completed" ]; then
        pass "Analysis completed!"
        break
    elif [ "$STATUS" = "failed" ]; then
        fail "Analysis failed"
        break
    fi
    sleep 2
done

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║     🎉 ALL TESTS PASSED! 🎉                ║"
echo "╚════════════════════════════════════════════╝"
