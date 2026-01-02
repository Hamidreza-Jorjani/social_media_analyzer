#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:8000/api/v1"
BRAIN_URL="http://localhost:8001"

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}  Persian Social Analyzer - Full Test   ${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Step 1: Health Checks
echo -e "${YELLOW}Step 1: Health Checks${NC}"
echo "Checking Backend..."
BACKEND_HEALTH=$(curl -s http://localhost:8000/health)
echo "Backend: $BACKEND_HEALTH"

echo "Checking BRAIN..."
BRAIN_HEALTH=$(curl -s $BRAIN_URL/health)
echo "BRAIN: $BRAIN_HEALTH"
echo ""

# Step 2: Login
echo -e "${YELLOW}Step 2: Login as admin${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}')

echo "Login Response: $LOGIN_RESPONSE"

# Extract token
TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('tokens', {}).get('access_token', '') if 'tokens' in data else '')" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo -e "${RED}Failed to get token. Creating admin user...${NC}"
    
    # Try to register
    REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
      -H "Content-Type: application/json" \
      -d '{
        "email": "admin@example.com",
        "username": "admin",
        "password": "Admin123!",
        "full_name": "System Administrator"
      }')
    echo "Register Response: $REGISTER_RESPONSE"
    
    # Try login again
    LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
      -H "Content-Type: application/json" \
      -d '{"username": "admin", "password": "Admin123!"}')
    
    TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('tokens', {}).get('access_token', '') if 'tokens' in data else '')" 2>/dev/null)
fi

if [ -z "$TOKEN" ]; then
    echo -e "${RED}Still no token. Check the auth endpoints.${NC}"
    exit 1
fi

echo -e "${GREEN}Got token: ${TOKEN:0:50}...${NC}"
echo ""

# Step 3: Create Data Source
echo -e "${YELLOW}Step 3: Create Data Source${NC}"
DATASOURCE_RESPONSE=$(curl -s -X POST "$BASE_URL/data-sources" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Twitter Persian Test",
    "platform": "twitter",
    "description": "Test data source for Persian tweets",
    "is_active": true
  }')
echo "Data Source: $DATASOURCE_RESPONSE"

DATASOURCE_ID=$(echo $DATASOURCE_RESPONSE | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', 1))" 2>/dev/null || echo "1")
echo "Data Source ID: $DATASOURCE_ID"
echo ""

# Step 4: Create Author
echo -e "${YELLOW}Step 4: Create Author${NC}"
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
echo "Author: $AUTHOR_RESPONSE"

AUTHOR_ID=$(echo $AUTHOR_RESPONSE | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', 1))" 2>/dev/null || echo "1")
echo "Author ID: $AUTHOR_ID"
echo ""

# Step 5: Create Posts (Bulk)
echo -e "${YELLOW}Step 5: Create Posts (Bulk)${NC}"
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
echo "Posts Response: $POSTS_RESPONSE"
echo ""

# Step 6: Verify Posts
echo -e "${YELLOW}Step 6: Verify Posts${NC}"
POSTS_LIST=$(curl -s "$BASE_URL/posts?page_size=5" \
  -H "Authorization: Bearer $TOKEN")
echo "Posts List: $POSTS_LIST"
echo ""

# Step 7: Get Post Stats
echo -e "${YELLOW}Step 7: Post Statistics${NC}"
POST_STATS=$(curl -s "$BASE_URL/posts/stats" \
  -H "Authorization: Bearer $TOKEN")
echo "Post Stats: $POST_STATS"
echo ""

# Step 8: Test BRAIN directly
echo -e "${YELLOW}Step 8: Test BRAIN Service Directly${NC}"
BRAIN_TEST=$(curl -s -X POST "$BRAIN_URL/analyze/sentiment" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["امروز خیلی خوشحالم!", "وضعیت خیلی بد است."]}')
echo "BRAIN Sentiment Test: $BRAIN_TEST"
echo ""

# Step 9: Create Analysis
echo -e "${YELLOW}Step 9: Create Analysis${NC}"
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
echo "Analysis Created: $ANALYSIS_RESPONSE"

ANALYSIS_ID=$(echo $ANALYSIS_RESPONSE | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', 1))" 2>/dev/null || echo "1")
echo "Analysis ID: $ANALYSIS_ID"
echo ""

# Step 10: Start Analysis
echo -e "${YELLOW}Step 10: Start Analysis Processing${NC}"
START_RESPONSE=$(curl -s -X POST "$BASE_URL/analysis/$ANALYSIS_ID/start" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json")
echo "Start Response: $START_RESPONSE"
echo ""

# Step 11: Wait and check progress
echo -e "${YELLOW}Step 11: Checking Analysis Progress${NC}"
for i in {1..10}; do
    sleep 2
    PROGRESS=$(curl -s "$BASE_URL/analysis/$ANALYSIS_ID/progress" \
      -H "Authorization: Bearer $TOKEN")
    echo "Progress ($i): $PROGRESS"
    
    STATUS=$(echo $PROGRESS | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('status', ''))" 2>/dev/null)
    if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
        break
    fi
done
echo ""

# Step 12: Get Analysis Results
echo -e "${YELLOW}Step 12: Get Analysis Results${NC}"
RESULTS=$(curl -s "$BASE_URL/analysis/$ANALYSIS_ID/results?page_size=5" \
  -H "Authorization: Bearer $TOKEN")
echo "Results: $RESULTS"
echo ""

# Step 13: Get Analysis Summary
echo -e "${YELLOW}Step 13: Get Analysis Summary${NC}"
SUMMARY=$(curl -s "$BASE_URL/analysis/$ANALYSIS_ID/summary" \
  -H "Authorization: Bearer $TOKEN")
echo "Summary: $SUMMARY"
echo ""

# Step 14: Test Dashboard
echo -e "${YELLOW}Step 14: Dashboard Overview${NC}"
DASHBOARD=$(curl -s "$BASE_URL/dashboard/overview" \
  -H "Authorization: Bearer $TOKEN")
echo "Dashboard: $DASHBOARD"
echo ""

# Step 15: Test Trends
echo -e "${YELLOW}Step 15: Trending Hashtags${NC}"
TRENDS=$(curl -s "$BASE_URL/trends/hashtags?hours=24&limit=10" \
  -H "Authorization: Bearer $TOKEN")
echo "Trending Hashtags: $TRENDS"
echo ""

echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}  Test Complete!${NC}"
echo -e "${BLUE}=========================================${NC}"
