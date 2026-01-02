#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

BACKEND_PORT=18000
BRAIN_PORT=18001

BASE_URL="http://localhost:${BACKEND_PORT}/api/v1"
BRAIN_URL="http://localhost:${BRAIN_PORT}"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}jq is not installed. Installing...${NC}"
    sudo apt-get update && sudo apt-get install -y jq
fi

pretty_json() {
    echo "$1" | jq '.' 2>/dev/null || echo "$1"
}

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}  Persian Social Analyzer - Full Test    ${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

echo -e "${YELLOW}━━━ Step 1: Health Checks ━━━${NC}"
echo -e "${CYAN}Backend:${NC}"
BACKEND_HEALTH=$(curl -s "http://localhost:${BACKEND_PORT}/health")
pretty_json "$BACKEND_HEALTH"

echo -e "\n${CYAN}BRAIN:${NC}"
BRAIN_HEALTH=$(curl -s "$BRAIN_URL/health")
pretty_json "$BRAIN_HEALTH"
echo ""

# Step 2: Login
echo -e "${YELLOW}━━━ Step 2: Login as admin ━━━${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}')

echo -e "${CYAN}Login Response:${NC}"
pretty_json "$LOGIN_RESPONSE"

# Extract token
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.tokens.access_token // empty' 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo -e "${RED}❌ Failed to get token${NC}"
    exit 1
fi

echo -e "\n${GREEN}✅ Got token: ${TOKEN:0:50}...${NC}"
echo ""

# Step 3: Create Data Source
echo -e "${YELLOW}━━━ Step 3: Create Data Source ━━━${NC}"
DATASOURCE_RESPONSE=$(curl -s -X POST "$BASE_URL/data-sources" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Twitter Persian Test",
    "platform": "twitter",
    "description": "Test data source for Persian tweets",
    "is_active": true
  }')
pretty_json "$DATASOURCE_RESPONSE"

DATASOURCE_ID=$(echo $DATASOURCE_RESPONSE | jq -r '.id // 1' 2>/dev/null)
echo -e "${CYAN}Data Source ID: $DATASOURCE_ID${NC}"
echo ""

# Step 4: Create Author
echo -e "${YELLOW}━━━ Step 4: Create Author ━━━${NC}"
AUTHOR_RESPONSE=$(curl -s -X POST "$BASE_URL/authors" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": "user_12345",
    "platform": "twitter",
    "username": "ali_tehrani",
    "display_name": "علی تهرانی",
    "bio": "توسعه‌دهنده نرم‌افزار",
    "followers_count": 5000,
    "following_count": 200,
    "posts_count": 150
  }')
pretty_json "$AUTHOR_RESPONSE"

AUTHOR_ID=$(echo $AUTHOR_RESPONSE | jq -r '.id // 1' 2>/dev/null)
echo -e "${CYAN}Author ID: $AUTHOR_ID${NC}"
echo ""

# Step 5: Create Posts (Bulk)
echo -e "${YELLOW}━━━ Step 5: Create Posts (Bulk) ━━━${NC}"
POSTS_RESPONSE=$(curl -s -X POST "$BASE_URL/posts/bulk" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"posts\": [
      {
        \"platform_id\": \"tweet_001\",
        \"platform\": \"twitter\",
        \"content\": \"امروز هوای تهران عالی است! #تهران #آب_و_هوا\",
        \"language\": \"fa\",
        \"hashtags\": [\"تهران\", \"آب_و_هوا\"],
        \"likes_count\": 150,
        \"comments_count\": 23,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
      },
      {
        \"platform_id\": \"tweet_002\",
        \"platform\": \"twitter\",
        \"content\": \"فوتبال ایران امشب بازی مهمی دارد. امیدوارم ببریم! #فوتبال #تیم_ملی\",
        \"language\": \"fa\",
        \"hashtags\": [\"فوتبال\", \"تیم_ملی\"],
        \"likes_count\": 320,
        \"comments_count\": 89,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
      },
      {
        \"platform_id\": \"tweet_003\",
        \"platform\": \"twitter\",
        \"content\": \"قیمت‌ها دوباره بالا رفت. وضعیت اقتصادی خیلی بد شده. #اقتصاد #گرانی\",
        \"language\": \"fa\",
        \"hashtags\": [\"اقتصاد\", \"گرانی\"],
        \"likes_count\": 890,
        \"comments_count\": 234,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
      },
      {
        \"platform_id\": \"tweet_004\",
        \"platform\": \"twitter\",
        \"content\": \"کتاب جدیدی خریدم. خیلی جالب و آموزنده است! پیشنهاد می‌کنم بخوانید. #کتاب #مطالعه\",
        \"language\": \"fa\",
        \"hashtags\": [\"کتاب\", \"مطالعه\"],
        \"likes_count\": 67,
        \"comments_count\": 12,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
      },
      {
        \"platform_id\": \"tweet_005\",
        \"platform\": \"twitter\",
        \"content\": \"سفر به اصفهان فوق‌العاده بود. نصف جهان واقعاً زیباست! #سفر #اصفهان #گردشگری\",
        \"language\": \"fa\",
        \"hashtags\": [\"سفر\", \"اصفهان\", \"گردشگری\"],
        \"likes_count\": 445,
        \"comments_count\": 56,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
      },
      {
        \"platform_id\": \"tweet_006\",
        \"platform\": \"twitter\",
        \"content\": \"ترافیک تهران امروز وحشتناک بود. دو ساعت در راه ماندم! #ترافیک #تهران\",
        \"language\": \"fa\",
        \"hashtags\": [\"ترافیک\", \"تهران\"],
        \"likes_count\": 234,
        \"comments_count\": 78,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
      },
      {
        \"platform_id\": \"tweet_007\",
        \"platform\": \"twitter\",
        \"content\": \"موسیقی ایرانی را خیلی دوست دارم. صدای شجریان بی‌نظیر است. #موسیقی #شجریان\",
        \"language\": \"fa\",
        \"hashtags\": [\"موسیقی\", \"شجریان\"],
        \"likes_count\": 678,
        \"comments_count\": 123,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
      },
      {
        \"platform_id\": \"tweet_008\",
        \"platform\": \"twitter\",
        \"content\": \"دانشگاه تهران بهترین دانشگاه کشور است. افتخار می‌کنم اینجا درس می‌خوانم. #دانشگاه_تهران\",
        \"language\": \"fa\",
        \"hashtags\": [\"دانشگاه_تهران\"],
        \"likes_count\": 345,
        \"comments_count\": 67,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
      },
      {
        \"platform_id\": \"tweet_009\",
        \"platform\": \"twitter\",
        \"content\": \"غذای ایرانی بهترین غذای دنیاست! چلوکباب عشق است. #غذای_ایرانی #چلوکباب\",
        \"language\": \"fa\",
        \"hashtags\": [\"غذای_ایرانی\", \"چلوکباب\"],
        \"likes_count\": 567,
        \"comments_count\": 89,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
      },
      {
        \"platform_id\": \"tweet_010\",
        \"platform\": \"twitter\",
        \"content\": \"امروز خیلی خسته‌ام. کار زیاد آدم را از پا درمیاورد. #خستگی #کار\",
        \"language\": \"fa\",
        \"hashtags\": [\"خستگی\", \"کار\"],
        \"likes_count\": 123,
        \"comments_count\": 34,
        \"data_source_id\": $DATASOURCE_ID,
        \"author_id\": $AUTHOR_ID
      }
    ]
  }")
pretty_json "$POSTS_RESPONSE"
echo ""

# Step 6: Verify Posts
echo -e "${YELLOW}━━━ Step 6: Verify Posts ━━━${NC}"
POSTS_LIST=$(curl -s "$BASE_URL/posts?page_size=3" \
  -H "Authorization: Bearer $TOKEN")
echo -e "${CYAN}First 3 Posts:${NC}"
echo "$POSTS_LIST" | jq '[.[:3][] | {id, platform, content: .content[:50], hashtags}]' 2>/dev/null || echo "$POSTS_LIST"
echo ""

# Step 7: Get Post Stats
echo -e "${YELLOW}━━━ Step 7: Post Statistics ━━━${NC}"
POST_STATS=$(curl -s "$BASE_URL/posts/stats" \
  -H "Authorization: Bearer $TOKEN")
pretty_json "$POST_STATS"
echo ""

# Step 8: Test BRAIN directly
echo -e "${YELLOW}━━━ Step 8: Test BRAIN Service ━━━${NC}"
BRAIN_TEST=$(curl -s -X POST "$BRAIN_URL/analyze/sentiment" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["امروز خیلی خوشحالم!", "وضعیت خیلی بد است."]}')
pretty_json "$BRAIN_TEST"
echo ""

# Step 9: Create Analysis
echo -e "${YELLOW}━━━ Step 9: Create Analysis ━━━${NC}"
ANALYSIS_RESPONSE=$(curl -s -X POST "$BASE_URL/analysis" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Persian Sentiment Analysis",
    "description": "Testing full analysis pipeline with Persian tweets",
    "analysis_type": "full",
    "config": {
      "sentiment_enabled": true,
      "emotion_enabled": true,
      "keyword_extraction_enabled": true
    },
    "query_filters": {
      "platform": "twitter",
      "language": "fa"
    },
    "post_count": 100
  }')
pretty_json "$ANALYSIS_RESPONSE"

ANALYSIS_ID=$(echo $ANALYSIS_RESPONSE | jq -r '.id // 1' 2>/dev/null)
echo -e "${CYAN}Analysis ID: $ANALYSIS_ID${NC}"
echo ""

# Step 10: Start Analysis
echo -e "${YELLOW}━━━ Step 10: Start Analysis Processing ━━━${NC}"
START_RESPONSE=$(curl -s -X POST "$BASE_URL/analysis/$ANALYSIS_ID/start" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json")
pretty_json "$START_RESPONSE"
echo ""

# Step 11: Wait and check progress
echo -e "${YELLOW}━━━ Step 11: Checking Analysis Progress ━━━${NC}"
for i in {1..10}; do
    sleep 2
    PROGRESS=$(curl -s "$BASE_URL/analysis/$ANALYSIS_ID/progress" \
      -H "Authorization: Bearer $TOKEN")
    
    STATUS=$(echo $PROGRESS | jq -r '.status // "unknown"' 2>/dev/null)
    PROG_PCT=$(echo $PROGRESS | jq -r '.progress // 0' 2>/dev/null)
    
    if [ "$STATUS" = "completed" ]; then
        echo -e "${GREEN}✅ Analysis completed! (Progress: $PROG_PCT%)${NC}"
        break
    elif [ "$STATUS" = "failed" ]; then
        echo -e "${RED}❌ Analysis failed!${NC}"
        pretty_json "$PROGRESS"
        break
    else
        echo -e "   ⏳ Status: $STATUS | Progress: $PROG_PCT%"
    fi
done
echo ""

# Step 12: Get Analysis Results
echo -e "${YELLOW}━━━ Step 12: Analysis Results (First 3) ━━━${NC}"
RESULTS=$(curl -s "$BASE_URL/analysis/$ANALYSIS_ID/results?page_size=3" \
  -H "Authorization: Bearer $TOKEN")
echo "$RESULTS" | jq '[.[:3][] | {id, post_id, sentiment_label, sentiment_score: (.sentiment_score | tonumber | . * 100 | round / 100), dominant_emotion, keywords: .keywords[:3]}]' 2>/dev/null || echo "$RESULTS"
echo ""

# Step 13: Get Analysis Summary
echo -e "${YELLOW}━━━ Step 13: Analysis Summary ━━━${NC}"
SUMMARY=$(curl -s "$BASE_URL/analysis/$ANALYSIS_ID/summary" \
  -H "Authorization: Bearer $TOKEN")
pretty_json "$SUMMARY"
echo ""

# Step 14: Dashboard Overview
echo -e "${YELLOW}━━━ Step 14: Dashboard Overview ━━━${NC}"
DASHBOARD=$(curl -s "$BASE_URL/dashboard/overview" \
  -H "Authorization: Bearer $TOKEN")
pretty_json "$DASHBOARD"
echo ""

# Step 15: Trending Hashtags
echo -e "${YELLOW}━━━ Step 15: Trending Hashtags ━━━${NC}"
TRENDS=$(curl -s "$BASE_URL/trends/hashtags?hours=24&limit=10" \
  -H "Authorization: Bearer $TOKEN")
if [ "$TRENDS" = "[]" ]; then
    echo -e "${CYAN}No trending hashtags yet (need more data)${NC}"
else
    pretty_json "$TRENDS"
fi
echo ""

# Final Summary
echo -e "${BLUE}==========================================${NC}"
echo -e "${GREEN}  ✅ Test Complete!${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""
echo -e "${CYAN}Quick Stats:${NC}"
echo "$POST_STATS" | jq -r '"  📝 Total Posts: \(.total)\n  ✅ Processed: \(.processed)\n  ⏳ Unprocessed: \(.unprocessed)"' 2>/dev/null
echo ""
echo "$SUMMARY" | jq -r '"  😊 Positive: \(.sentiment_distribution.positive // 0)\n  😐 Neutral: \(.sentiment_distribution.neutral // 0)\n  😞 Negative: \(.sentiment_distribution.negative // 0)"' 2>/dev/null
echo ""
