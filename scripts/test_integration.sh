#!/bin/bash
# Complete integration test

echo "🚀 Persian Analytics Integration Test"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check services
echo -e "\n${YELLOW}📦 Checking Docker containers...${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep persian_analytics

# 2. BRAIN Health
echo -e "\n${YELLOW}🧠 Testing BRAIN...${NC}"
BRAIN_HEALTH=$(curl -s http://localhost:8001/health)
if echo "$BRAIN_HEALTH" | jq -e '.status == "healthy"' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ BRAIN is healthy${NC}"
else
    echo -e "${RED}❌ BRAIN is unhealthy${NC}"
    echo "$BRAIN_HEALTH" | jq
    exit 1
fi

# 3. Backend Health
echo -e "\n${YELLOW}🔧 Testing Backend...${NC}"
BACKEND_HEALTH=$(curl -s http://localhost:8000/health)
if echo "$BACKEND_HEALTH" | jq -e '.status == "healthy"' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend is unhealthy${NC}"
    echo "$BACKEND_HEALTH" | jq
    exit 1
fi

# 4. Login
echo -e "\n${YELLOW}🔐 Logging in...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}')

TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.tokens.access_token')

if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
    echo -e "${RED}❌ Login failed${NC}"
    echo "$LOGIN_RESPONSE" | jq
    exit 1
fi

echo -e "${GREEN}✅ Logged in successfully${NC}"

# 5. Test BRAIN via Backend
echo -e "\n${YELLOW}🔗 Testing Backend → BRAIN connection...${NC}"
BRAIN_VIA_BACKEND=$(curl -s http://localhost:8000/api/v1/brain/health \
  -H "Authorization: Bearer $TOKEN")

if echo "$BRAIN_VIA_BACKEND" | jq -e '.status == "healthy"' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend → BRAIN connection OK${NC}"
else
    echo -e "${RED}❌ Backend cannot reach BRAIN${NC}"
    echo "$BRAIN_VIA_BACKEND" | jq
fi

# 6. Test direct sentiment analysis
echo -e "\n${YELLOW}🧪 Testing sentiment analysis...${NC}"
SENTIMENT=$(curl -s -X POST http://localhost:8000/api/v1/brain/analyze/sentiment \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["سلام دنیا خوب است"]}')

if echo "$SENTIMENT" | jq -e '.results[0].sentiment.label' > /dev/null 2>&1; then
    LABEL=$(echo "$SENTIMENT" | jq -r '.results[0].sentiment.label')
    echo -e "${GREEN}✅ Sentiment analysis works: $LABEL${NC}"
else
    echo -e "${RED}❌ Sentiment analysis failed${NC}"
    echo "$SENTIMENT" | jq
fi

# 7. Create test post
echo -e "\n${YELLOW}📝 Creating test post...${NC}"
POST_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/posts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "integration_test_001",
    "platform": "twitter",
    "content": "سلام! این یک تست سیستم است. تهران شهر زیبایی است.",
    "language": "fa",
    "posted_at": "2024-01-15T12:00:00"
  }')

POST_ID=$(echo "$POST_RESPONSE" | jq -r '.id')
if [ "$POST_ID" != "null" ]; then
    echo -e "${GREEN}✅ Post created: ID=$POST_ID${NC}"
else
    echo -e "${YELLOW}⚠️  Post might already exist${NC}"
fi

# 8. Create analysis
echo -e "\n${YELLOW}📊 Creating analysis job...${NC}"
ANALYSIS_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/analysis \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Integration Test",
    "analysis_type": "sentiment",
    "query_filters": {"platform": "twitter"}
  }')

ANALYSIS_ID=$(echo "$ANALYSIS_RESPONSE" | jq -r '.id')
echo -e "${GREEN}✅ Analysis created: ID=$ANALYSIS_ID${NC}"

# 9. Start analysis
echo -e "\n${YELLOW}▶️  Starting analysis...${NC}"
START_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/analysis/$ANALYSIS_ID/start \
  -H "Authorization: Bearer $TOKEN")

echo "$START_RESPONSE" | jq

# 10. Monitor progress
echo -e "\n${YELLOW}⏳ Monitoring progress...${NC}"
for i in {1..10}; do
    sleep 2
    PROGRESS=$(curl -s http://localhost:8000/api/v1/analysis/$ANALYSIS_ID/progress \
      -H "Authorization: Bearer $TOKEN")
    
    STATUS=$(echo "$PROGRESS" | jq -r '.status')
    PERCENT=$(echo "$PROGRESS" | jq -r '.progress')
    
    echo "  Progress: $STATUS - $PERCENT%"
    
    if [ "$STATUS" == "completed" ] || [ "$STATUS" == "failed" ]; then
        break
    fi
done

# 11. Check final status
echo -e "\n${YELLOW}✓ Checking final status...${NC}"
FINAL_STATUS=$(curl -s http://localhost:8000/api/v1/analysis/$ANALYSIS_ID \
  -H "Authorization: Bearer $TOKEN")

STATUS=$(echo "$FINAL_STATUS" | jq -r '.status')
ERROR=$(echo "$FINAL_STATUS" | jq -r '.error_message')

if [ "$STATUS" == "completed" ]; then
    echo -e "${GREEN}✅ Analysis completed successfully!${NC}"
    
    # Get results
    echo -e "\n${YELLOW}📈 Fetching results...${NC}"
    RESULTS=$(curl -s "http://localhost:8000/api/v1/analysis/$ANALYSIS_ID/results" \
      -H "Authorization: Bearer $TOKEN")
    
    echo "$RESULTS" | jq '.[0] | {sentiment_label, sentiment_score, emotions, keywords}' 2>/dev/null || echo "$RESULTS"
    
elif [ "$STATUS" == "failed" ]; then
    echo -e "${RED}❌ Analysis failed${NC}"
    echo "Error: $ERROR"
else
    echo -e "${YELLOW}⚠️  Analysis status: $STATUS${NC}"
fi

echo -e "\n${GREEN}======================================"
echo "🏁 Integration test completed!"
echo -e "======================================${NC}"
