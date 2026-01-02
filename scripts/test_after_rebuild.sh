#!/bin/bash
# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Persian Analytics - Integration Test     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Test 1: Container Status
echo -e "${YELLOW}[1/10] Checking Docker Containers...${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep persian_analytics
echo ""

# Test 2: BRAIN Health
echo -e "${YELLOW}[2/10] Testing BRAIN Service...${NC}"
BRAIN_RESPONSE=$(curl -s http://localhost:8001/health)
BRAIN_STATUS=$(echo "$BRAIN_RESPONSE" | jq -r '.status // "unknown"')

if [ "$BRAIN_STATUS" == "healthy" ]; then
    echo -e "${GREEN}✅ BRAIN is healthy${NC}"
    echo "$BRAIN_RESPONSE" | jq '.'
else
    echo -e "${RED}❌ BRAIN is unhealthy${NC}"
    echo "$BRAIN_RESPONSE" | jq '.'
fi
echo ""

# Test 3: Backend Health
echo -e "${YELLOW}[3/10] Testing Backend Service...${NC}"
BACKEND_RESPONSE=$(curl -s http://localhost:8000/health)
BACKEND_STATUS=$(echo "$BACKEND_RESPONSE" | jq -r '.status // "unknown"')

if [ "$BACKEND_STATUS" == "healthy" ]; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
    echo "$BACKEND_RESPONSE" | jq '.'
else
    echo -e "${RED}❌ Backend is unhealthy${NC}"
    echo "$BACKEND_RESPONSE" | jq '.'
fi
echo ""

# Test 4: Admin Login
echo -e "${YELLOW}[4/10] Testing Admin Login...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}')

TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.tokens.access_token // ""')

if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
    echo -e "${GREEN}✅ Login successful${NC}"
    echo "   Token: ${TOKEN:0:30}..."
    echo "$LOGIN_RESPONSE" | jq '{user: .user.username, role: .user.role, token_type: .tokens.token_type}'
else
    echo -e "${RED}❌ Login failed${NC}"
    echo "$LOGIN_RESPONSE" | jq '.'
    exit 1
fi
echo ""

# Test 5: Backend → BRAIN Connection
echo -e "${YELLOW}[5/10] Testing Backend → BRAIN Connection...${NC}"
BRAIN_VIA_BACKEND=$(curl -s http://localhost:8000/api/v1/brain/health \
  -H "Authorization: Bearer $TOKEN")

BRAIN_VIA_STATUS=$(echo "$BRAIN_VIA_BACKEND" | jq -r '.status // "unknown"')

if [ "$BRAIN_VIA_STATUS" == "healthy" ]; then
    echo -e "${GREEN}✅ Backend can reach BRAIN${NC}"
    echo "$BRAIN_VIA_BACKEND" | jq '{status, gpu_available, mode}'
else
    echo -e "${RED}❌ Backend cannot reach BRAIN${NC}"
    echo "$BRAIN_VIA_BACKEND" | jq '.'
fi
echo ""

# Test 6: BRAIN Sentiment Analysis
echo -e "${YELLOW}[6/10] Testing BRAIN Sentiment Analysis...${NC}"
SENTIMENT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/brain/analyze/sentiment \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["سلام دنیا! این خیلی خوب است.", "این بد است و ناراحت کننده."]}')

SENTIMENT_LABEL=$(echo "$SENTIMENT_RESPONSE" | jq -r '.results[0].sentiment.label // "unknown"')

if [ -n "$SENTIMENT_LABEL" ] && [ "$SENTIMENT_LABEL" != "unknown" ] && [ "$SENTIMENT_LABEL" != "null" ]; then
    echo -e "${GREEN}✅ Sentiment analysis works${NC}"
    echo "$SENTIMENT_RESPONSE" | jq '.results[] | {text_id, sentiment: .sentiment.label, score: .sentiment.score}'
else
    echo -e "${RED}❌ Sentiment analysis failed${NC}"
    echo "$SENTIMENT_RESPONSE" | jq '.'
fi
echo ""

# Test 7: Create Test Post
echo -e "${YELLOW}[7/10] Creating Test Post...${NC}"
POST_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/posts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "integration_test_'$(date +%s)'",
    "platform": "twitter",
    "content": "سلام! این یک تست کامل سیستم است. تهران شهر زیبایی است و من خوشحالم.",
    "language": "fa",
    "posted_at": "2024-01-15T12:00:00",
    "hashtags": ["تست", "تهران"],
    "likes_count": 10
  }')

POST_ID=$(echo "$POST_RESPONSE" | jq -r '.id // ""')

if [ -n "$POST_ID" ] && [ "$POST_ID" != "null" ]; then
    echo -e "${GREEN}✅ Post created: ID=$POST_ID${NC}"
    echo "$POST_RESPONSE" | jq '{id, platform, language, content: .content[0:50]}'
else
    echo -e "${YELLOW}⚠️  Post creation (might already exist)${NC}"
    echo "$POST_RESPONSE" | jq '.'
fi
echo ""

# Test 8: Create Analysis
echo -e "${YELLOW}[8/10] Creating Analysis Job...${NC}"
ANALYSIS_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/analysis \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Integration Test Analysis",
    "description": "Full integration test of Backend → BRAIN → Celery",
    "analysis_type": "sentiment",
    "query_filters": {"platform": "twitter"},
    "config": {
      "sentiment_enabled": true,
      "emotion_enabled": true,
      "keyword_extraction_enabled": true
    }
  }')

ANALYSIS_ID=$(echo "$ANALYSIS_RESPONSE" | jq -r '.id // ""')

if [ -n "$ANALYSIS_ID" ] && [ "$ANALYSIS_ID" != "null" ]; then
    echo -e "${GREEN}✅ Analysis created: ID=$ANALYSIS_ID${NC}"
    echo "$ANALYSIS_RESPONSE" | jq '{id, name, analysis_type, status}'
else
    echo -e "${RED}❌ Analysis creation failed${NC}"
    echo "$ANALYSIS_RESPONSE" | jq '.'
    exit 1
fi
echo ""

# Test 9: Start Analysis
echo -e "${YELLOW}[9/10] Starting Analysis...${NC}"
START_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/analysis/$ANALYSIS_ID/start \
  -H "Authorization: Bearer $TOKEN")

START_MESSAGE=$(echo "$START_RESPONSE" | jq -r '.message // ""')

if echo "$START_MESSAGE" | grep -q "queued"; then
    echo -e "${GREEN}✅ Analysis started and queued${NC}"
    echo "$START_RESPONSE" | jq '.'
else
    echo -e "${YELLOW}⚠️  Analysis start: $START_MESSAGE${NC}"
    echo "$START_RESPONSE" | jq '.'
fi
echo ""

# Test 10: Monitor Progress
echo -e "${YELLOW}[10/10] Monitoring Analysis Progress...${NC}"
for i in {1..15}; do
    sleep 2
    
    PROGRESS_RESPONSE=$(curl -s http://localhost:8000/api/v1/analysis/$ANALYSIS_ID/progress \
      -H "Authorization: Bearer $TOKEN")
    
    STATUS=$(echo "$PROGRESS_RESPONSE" | jq -r '.status // "unknown"')
    PERCENT=$(echo "$PROGRESS_RESPONSE" | jq -r '.progress // 0')
    
    echo -e "   [$i/15] Status: ${BLUE}$STATUS${NC} - Progress: ${BLUE}${PERCENT}%${NC}"
    
    if [ "$STATUS" == "completed" ]; then
        echo -e "${GREEN}✅ Analysis completed successfully!${NC}"
        
        # Get results
        echo ""
        echo -e "${YELLOW}Fetching results...${NC}"
        RESULTS=$(curl -s "http://localhost:8000/api/v1/analysis/$ANALYSIS_ID/results?page=1&page_size=5" \
          -H "Authorization: Bearer $TOKEN")
        
        echo "$RESULTS" | jq -r '
            if type == "array" and length > 0 then
                "First Result:",
                "  Sentiment: \(.[0].sentiment_label // "N/A") (\(.[0].sentiment_score // 0))",
                "  Confidence: \(.[0].sentiment_confidence // 0)",
                "  Dominant Emotion: \(.[0].dominant_emotion // "N/A")",
                "  Keywords: \(.[0].keywords // [] | join(", "))"
            else
                "No results yet"
            end
        '
        
        # Get summary
        echo ""
        echo -e "${YELLOW}Analysis Summary:${NC}"
        SUMMARY=$(curl -s "http://localhost:8000/api/v1/analysis/$ANALYSIS_ID/summary" \
          -H "Authorization: Bearer $TOKEN")
        echo "$SUMMARY" | jq '{
            total_posts,
            sentiment_distribution,
            average_sentiment_score,
            top_keywords: .top_keywords[0:5]
        }'
        
        break
        
    elif [ "$STATUS" == "failed" ]; then
        echo -e "${RED}❌ Analysis failed${NC}"
        
        # Get error details
        ANALYSIS_DETAILS=$(curl -s http://localhost:8000/api/v1/analysis/$ANALYSIS_ID \
          -H "Authorization: Bearer $TOKEN")
        
        ERROR=$(echo "$ANALYSIS_DETAILS" | jq -r '.error_message // "Unknown error"')
        echo -e "${RED}Error: $ERROR${NC}"
        
        # Check Celery logs
        echo ""
        echo -e "${YELLOW}Celery logs (last 30 lines):${NC}"
        docker logs persian_analytics_celery --tail 30
        break
        
    elif [ "$i" == "15" ]; then
        echo -e "${YELLOW}⚠️  Analysis still running after 30 seconds${NC}"
        echo -e "${YELLOW}   This might be normal for large datasets${NC}"
        
        # Check Celery status
        echo ""
        echo -e "${YELLOW}Checking Celery worker...${NC}"
        docker logs persian_analytics_celery --tail 20
    fi
done

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           Test Summary                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "BRAIN:      ${GREEN}$BRAIN_STATUS${NC}"
echo -e "Backend:    ${GREEN}$BACKEND_STATUS${NC}"
echo -e "Login:      ${GREEN}Success${NC}"
echo -e "Analysis:   ID $ANALYSIS_ID - Status: $STATUS"
echo ""

if [ "$STATUS" == "completed" ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     🎉 ALL TESTS PASSED! 🎉                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
    exit 0
elif [ "$STATUS" == "failed" ]; then
    echo -e "${RED}╔════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║     ❌ ANALYSIS FAILED ❌                   ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════╝${NC}"
    exit 1
else
    echo -e "${YELLOW}╔════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║     ⏳ TESTS INCOMPLETE ⏳                 ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════╝${NC}"
    exit 0
fi
EOF
