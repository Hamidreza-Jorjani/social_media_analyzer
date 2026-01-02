==================== FRONTEND CONTEXT ====================

Project root: /home/great/projects/social_media_analyzer

Backend:
  URL:          http://localhost:18000
  API base:     http://localhost:18000/api/v1
  Health:       http://localhost:18000/health
  OpenAPI JSON: http://localhost:18000/api/v1/openapi.json

BRAIN:
  URL:          http://localhost:18001
  Health:       http://localhost:18001/health

Recommended frontend .env.local:
  NEXT_PUBLIC_API_URL=http://localhost:18000/api/v1

=== LIVE HEALTH CHECKS (if backend/brain are running) ===

--- Backend /health ---
{"status":"healthy","service":"Persian Social Analytics","version":"1.0.0","redis":"connected"}

--- /api/v1/status (if implemented) ---
{"api_version":"v1","status":"operational","endpoints":["/auth","/users","/data-sources","/authors","/posts","/analysis","/trends","/graph","/dashboard","/brain"]}

--- BRAIN /health ---
{"status":"healthy","service":"BRAIN Mock Service","version":"1.0.0","gpu_available":true,"gpu_memory_used":2048,"gpu_memory_total":8192,"mode":"mock"}

==================== HIGH-LEVEL API SPEC =================

----- FILE: ai_document/API.md -----
API.md - Persian Social Media Analyzer API Documentation
Markdown

# Persian Social Media Analyzer - API Documentation

**Base URL:** `http://localhost:8000`  
**API Version:** v1  
**API Prefix:** `/api/v1`

---

## Table of Contents

1. [Authentication](#1-authentication)
2. [Users](#2-users)
3. [Posts](#3-posts)
4. [Authors](#4-authors)
5. [Data Sources](#5-data-sources)
6. [Analysis](#6-analysis)
7. [Trends](#7-trends)
8. [Graph](#8-graph)
9. [Dashboard](#9-dashboard)
10. [BRAIN Service](#10-brain-service)
11. [Health & Status](#11-health--status)

---

## Authentication Header

Most endpoints require authentication. Include the JWT token in the header:
Authorization: Bearer <access_token>

text


---

## Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message here"
}
Common HTTP Status Codes:

200 - Success
201 - Created
400 - Bad Request
401 - Unauthorized
403 - Forbidden
404 - Not Found
422 - Validation Error
500 - Internal Server Error
1. Authentication
POST /api/v1/auth/register
Create a new user account.

Request:

JSON

{
  "email": "user@example.com",
  "username": "newuser",
  "password": "SecurePass123!",
  "full_name": "New User"
}
Response:

JSON

{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "newuser",
    "full_name": "New User",
    "is_active": true,
    "role": "viewer",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  },
  "tokens": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
Example:

Bash

curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "newuser",
    "password": "SecurePass123!",
    "full_name": "New User"
  }'
POST /api/v1/auth/login
Login with username/email and password.

Request:

JSON

{
  "username": "admin",
  "password": "Admin123!"
}
Response:

JSON

{
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "username": "admin",
    "full_name": "System Administrator",
    "is_active": true,
    "role": "admin",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  },
  "tokens": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
Example:

Bash

curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}'
POST /api/v1/auth/refresh
Refresh access token using refresh token.

Request:

JSON

{
  "refresh_token": "eyJ..."
}
Response:

JSON

{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 1800
}
Example:

Bash

curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'
GET /api/v1/auth/me
Get current authenticated user.

Headers: Authorization: Bearer <token>

Response:

JSON

{
  "id": 1,
  "email": "admin@example.com",
  "username": "admin",
  "full_name": "System Administrator",
  "is_active": true,
  "role": "admin",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
Example:

Bash

curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
POST /api/v1/auth/logout
Logout current user.

Headers: Authorization: Bearer <token>

Response:

JSON

{
  "message": "Successfully logged out",
  "success": true
}
2. Users
GET /api/v1/users
List all users (Admin only).

Headers: Authorization: Bearer <admin_token>

Query Parameters:

page (int): Page number, default 1
page_size (int): Items per page, default 20, max 100
Response:

JSON

[
  {
    "id": 1,
    "email": "admin@example.com",
    "username": "admin",
    "full_name": "System Administrator",
    "is_active": true,
    "role": "admin",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
Example:

Bash

curl http://localhost:8000/api/v1/users?page=1&page_size=20 \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
GET /api/v1/users/{user_id}
Get user by ID.

Response:

JSON

{
  "id": 1,
  "email": "admin@example.com",
  "username": "admin",
  "full_name": "System Administrator",
  "is_active": true,
  "role": "admin",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
POST /api/v1/users
Create new user (Admin only).

Request:

JSON

{
  "email": "analyst@example.com",
  "username": "analyst",
  "password": "Analyst123!",
  "full_name": "Data Analyst"
}
PUT /api/v1/users/{user_id}
Update user.

Request:

JSON

{
  "full_name": "Updated Name",
  "is_active": true,
  "role": "analyst"
}
DELETE /api/v1/users/{user_id}
Delete user (Admin only).

Response:

JSON

{
  "message": "User deleted successfully",
  "success": true
}
POST /api/v1/users/{user_id}/activate
Activate user account (Admin only).

POST /api/v1/users/{user_id}/deactivate
Deactivate user account (Admin only).

3. Posts
GET /api/v1/posts
List posts with filters.

Query Parameters:

page (int): Page number
page_size (int): Items per page
platform (str): Filter by platform (twitter, instagram, telegram)
language (str): Filter by language (fa, en)
data_source_id (int): Filter by data source
author_id (int): Filter by author
is_processed (bool): Filter by processed status
date_from (datetime): Filter from date
date_to (datetime): Filter to date
search (str): Search in content
Response:

JSON

[
  {
    "id": 1,
    "platform_id": "tweet_123",
    "platform": "twitter",
    "content": "سلام این یک تست است #تست",
    "language": "fa",
    "url": "https://twitter.com/...",
    "likes_count": 10,
    "comments_count": 5,
    "shares_count": 2,
    "views_count": 100,
    "posted_at": "2024-01-01T10:00:00",
    "hashtags": ["تست"],
    "mentions": ["user1"],
    "is_processed": false,
    "data_source_id": 1,
    "author_id": 1,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
Example:

Bash

curl "http://localhost:8000/api/v1/posts?platform=twitter&language=fa&page=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
GET /api/v1/posts/stats
Get post statistics.

Response:

JSON

{
  "total": 1000,
  "processed": 800,
  "unprocessed": 200,
  "by_platform": {
    "twitter": 500,
    "instagram": 300,
    "telegram": 200
  },
  "by_language": {
    "fa": 900,
    "en": 100
  }
}
GET /api/v1/posts/unprocessed
Get unprocessed posts.

GET /api/v1/posts/search
Search posts by content.

Query Parameters:

q (str, required): Search query (min 2 chars)
platform (str): Filter by platform
Example:

Bash

curl "http://localhost:8000/api/v1/posts/search?q=تهران&platform=twitter" \
  -H "Authorization: Bearer YOUR_TOKEN"
GET /api/v1/posts/by-hashtag/{hashtag}
Get posts by hashtag.

Example:

Bash

curl "http://localhost:8000/api/v1/posts/by-hashtag/تهران" \
  -H "Authorization: Bearer YOUR_TOKEN"
GET /api/v1/posts/{post_id}
Get post by ID with relations.

Response:

JSON

{
  "id": 1,
  "platform_id": "tweet_123",
  "platform": "twitter",
  "content": "سلام این یک تست است",
  "author": {
    "id": 1,
    "username": "ali_tehrani",
    "display_name": "Ali Tehrani",
    "platform": "twitter"
  },
  "data_source": {
    "id": 1,
    "name": "Twitter Persian",
    "platform": "twitter",
    "is_active": true
  }
}
POST /api/v1/posts
Create new post (Analyst+).

Request:

JSON

{
  "platform_id": "tweet_456",
  "platform": "twitter",
  "content": "محتوای جدید #تست",
  "language": "fa",
  "likes_count": 0,
  "comments_count": 0,
  "hashtags": ["تست"],
  "posted_at": "2024-01-01T12:00:00",
  "author_id": 1,
  "data_source_id": 1
}
POST /api/v1/posts/bulk
Bulk create posts (Analyst+).

Request:

JSON

{
  "posts": [
    {
      "platform_id": "tweet_001",
      "platform": "twitter",
      "content": "اولین پست"
    },
    {
      "platform_id": "tweet_002",
      "platform": "twitter",
      "content": "دومین پست"
    }
  ]
}
Response:

JSON

{
  "total": 2,
  "created": 2,
  "existing": 0
}
PUT /api/v1/posts/{post_id}
Update post (Analyst+).

DELETE /api/v1/posts/{post_id}
Delete post (Analyst+).

4. Authors
GET /api/v1/authors
List authors.

Query Parameters:

page, page_size: Pagination
platform (str): Filter by platform
search (str): Search by username/display name
Response:

JSON

[
  {
    "id": 1,
    "platform_id": "user_123",
    "platform": "twitter",
    "username": "ali_tehrani",
    "display_name": "Ali Tehrani",
    "bio": "Developer",
    "followers_count": 5000,
    "following_count": 200,
    "posts_count": 150,
    "influence_score": 0.75,
    "pagerank_score": 0.023
  }
]
GET /api/v1/authors/top/followers
Get top authors by follower count.

Query Parameters:

platform (str): Filter by platform
limit (int): Number of results, default 10, max 100
GET /api/v1/authors/top/pagerank
Get top authors by PageRank score.

GET /api/v1/authors/top/influence
Get top authors by influence score.

GET /api/v1/authors/stats
Get author statistics by platform.

Response:

JSON

{
  "total": 500,
  "by_platform": {
    "twitter": 300,
    "instagram": 150,
    "telegram": 50
  }
}
GET /api/v1/authors/{author_id}
Get author by ID.

POST /api/v1/authors
Create author.

Request:

JSON

{
  "platform_id": "user_789",
  "platform": "twitter",
  "username": "new_user",
  "display_name": "New User",
  "followers_count": 100
}
PUT /api/v1/authors/{author_id}
Update author.

DELETE /api/v1/authors/{author_id}
Delete author.

5. Data Sources
GET /api/v1/data-sources
List data sources.

Query Parameters:

platform (str): Filter by platform
active_only (bool): Only active sources
Response:

JSON

[
  {
    "id": 1,
    "name": "Twitter Persian",
    "platform": "twitter",
    "description": "Persian Twitter data",
    "is_active": true,
    "last_sync_at": "2024-01-01T00:00:00",
    "created_at": "2024-01-01T00:00:00"
  }
]
GET /api/v1/data-sources/{source_id}
Get data source by ID.

GET /api/v1/data-sources/{source_id}/stats
Get data source statistics.

Response:

JSON

{
  "id": 1,
  "name": "Twitter Persian",
  "platform": "twitter",
  "total_posts": 5000,
  "total_authors": 500,
  "last_sync_at": "2024-01-01T00:00:00"
}
POST /api/v1/data-sources
Create data source (Analyst+).

Request:

JSON

{
  "name": "Instagram Influencers",
  "platform": "instagram",
  "description": "Top Iranian influencers",
  "api_endpoint": "https://api.example.com",
  "collection_config": {
    "keywords": ["ایران", "تهران"],
    "max_posts": 1000
  }
}
PUT /api/v1/data-sources/{source_id}
Update data source (Analyst+).

DELETE /api/v1/data-sources/{source_id}
Delete data source (Analyst+).

POST /api/v1/data-sources/{source_id}/activate
Activate data source.

POST /api/v1/data-sources/{source_id}/deactivate
Deactivate data source.

6. Analysis
GET /api/v1/analysis
List analyses for current user.

Query Parameters:

status_filter (str): pending, queued, processing, completed, failed, cancelled
type_filter (str): sentiment, emotion, summarization, topic_modeling, etc.
Response:

JSON

[
  {
    "id": 1,
    "name": "January Sentiment Analysis",
    "description": "Sentiment analysis for January posts",
    "analysis_type": "sentiment",
    "status": "completed",
    "progress": 100.0,
    "post_count": 500,
    "summary": {...},
    "user_id": 1,
    "created_at": "2024-01-01T00:00:00"
  }
]
GET /api/v1/analysis/stats
Get analysis statistics.

Response:

JSON

{
  "total": 10,
  "by_status": {
    "completed": 5,
    "processing": 2,
    "pending": 3
  },
  "by_type": {
    "sentiment": 4,
    "emotion": 3,
    "full": 3
  }
}
GET /api/v1/analysis/pending
Get pending analyses (Analyst+).

GET /api/v1/analysis/{analysis_id}
Get analysis by ID.

GET /api/v1/analysis/{analysis_id}/progress
Get analysis progress.

Response:

JSON

{
  "analysis_id": 1,
  "status": "processing",
  "progress": 45.5
}
GET /api/v1/analysis/{analysis_id}/results
Get analysis results.

Query Parameters:

page, page_size: Pagination
Response:

JSON

[
  {
    "id": 1,
    "post_id": 123,
    "analysis_id": 1,
    "sentiment_label": "positive",
    "sentiment_score": 0.85,
    "sentiment_confidence": 0.92,
    "emotions": {
      "joy": 0.7,
      "sadness": 0.1,
      "anger": 0.05,
      "fear": 0.05,
      "surprise": 0.1
    },
    "dominant_emotion": "joy",
    "keywords": ["خوب", "عالی"],
    "entities": [
      {"text": "تهران", "type": "location"}
    ]
  }
]
GET /api/v1/analysis/{analysis_id}/summary
Get analysis summary.

Response:

JSON

{
  "total_posts": 500,
  "processed_posts": 500,
  "sentiment_distribution": {
    "positive": 250,
    "negative": 100,
    "neutral": 150
  },
  "emotion_distribution": {
    "joy": 200,
    "sadness": 100,
    "anger": 50
  },
  "average_sentiment_score": 0.35,
  "top_keywords": [
    {"keyword": "تهران", "count": 150},
    {"keyword": "ایران", "count": 120}
  ],
  "generated_at": "2024-01-01T12:00:00"
}
POST /api/v1/analysis
Create new analysis (Analyst+).

Request:

JSON

{
  "name": "February Analysis",
  "description": "Full analysis for February posts",
  "analysis_type": "full",
  "config": {
    "sentiment_enabled": true,
    "emotion_enabled": true,
    "keyword_extraction_enabled": true,
    "num_topics": 10
  },
  "query_filters": {
    "platform": "twitter",
    "language": "fa",
    "date_from": "2024-02-01",
    "date_to": "2024-02-28"
  },
  "post_count": 1000
}
Response:

JSON

{
  "id": 2,
  "name": "February Analysis",
  "status": "pending",
  "progress": 0.0
}
POST /api/v1/analysis/{analysis_id}/start
Start processing analysis (Analyst+).

Request (optional config):

JSON

{
  "sentiment_enabled": true,
  "emotion_enabled": true,
  "keyword_extraction_enabled": true,
  "summarization_enabled": false
}
Response:

JSON

{
  "message": "Analysis queued for processing",
  "success": true
}
Example:

Bash

curl -X POST "http://localhost:8000/api/v1/analysis/1/start" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
POST /api/v1/analysis/{analysis_id}/cancel
Cancel analysis (Analyst+).

Response:

JSON

{
  "message": "Analysis cancelled",
  "success": true
}
PUT /api/v1/analysis/{analysis_id}
Update analysis (Analyst+).

DELETE /api/v1/analysis/{analysis_id}
Delete analysis and results (Analyst+).

7. Trends
GET /api/v1/trends
List trends.

Query Parameters:

active_only (bool): Only active trends, default true
Response:

JSON

[
  {
    "id": 1,
    "name": "#تهران",
    "description": "Trending hashtag",
    "volume": 500,
    "growth_rate": 1.5,
    "velocity": 0.8,
    "keywords": ["تهران", "پایتخت"],
    "hashtags": ["تهران"],
    "is_active": "active"
  }
]
GET /api/v1/trends/summary
Get trend summary.

Query Parameters:

hours (int): Time range in hours, default 24, max 168
Response:

JSON

{
  "trending_hashtags": [
    {"hashtag": "تهران", "count": 150}
  ],
  "trending_keywords": [
    {"keyword": "ایران", "count": 200}
  ],
  "active_trends": [
    {"id": 1, "name": "#تهران", "volume": 500}
  ],
  "top_growing": [
    {"id": 2, "name": "#ورزش", "growth_rate": 2.5}
  ],
  "stats": {
    "total": 50,
    "active": 30
  }
}
GET /api/v1/trends/hashtags
Get trending hashtags.

Query Parameters:

hours (int): Time range, default 24
limit (int): Number of results, default 20
Response:

JSON

[
  {"item": "تهران", "count": 150},
  {"item": "ایران", "count": 120}
]
GET /api/v1/trends/keywords
Get trending keywords.

Query Parameters:

hours (int): Time range
limit (int): Number of results
GET /api/v1/trends/sentiment
Get sentiment trends over time.

Query Parameters:

hours (int): Time range
interval (str): 1h, 6h, or 1d
Response:

JSON

[
  {
    "time": "2024-01-01 10:00",
    "positive": 50,
    "negative": 20,
    "neutral": 30
  }
]
GET /api/v1/trends/volume
Get post volume trends.

Query Parameters:

hours (int): Time range
interval (str): 1h, 6h, or 1d
platform (str): Filter by platform
Response:

JSON

[
  {"time": "2024-01-01 10:00", "count": 150},
  {"time": "2024-01-01 11:00", "count": 180}
]
GET /api/v1/trends/top/volume
Get top trends by volume.

GET /api/v1/trends/top/growth
Get top trends by growth rate.

GET /api/v1/trends/stats
Get trend statistics.

Response:

JSON

{
  "total": 100,
  "active": 50,
  "declining": 30,
  "average_volume": 250.5
}
GET /api/v1/trends/{trend_id}
Get trend by ID with details.

POST /api/v1/trends/detect
Trigger trend detection (Analyst+).

Query Parameters:

hours (int): Time range
min_count (int): Minimum count threshold
Response:

JSON

{
  "message": "Trend detection queued",
  "success": true
}
POST /api/v1/trends
Create trend manually (Analyst+).

PUT /api/v1/trends/{trend_id}
Update trend (Analyst+).

DELETE /api/v1/trends/{trend_id}
Delete trend (Analyst+).

8. Graph
GET /api/v1/graph/data
Get graph data for visualization.

Query Parameters:

node_type (str): Filter by node type (author, hashtag, topic)
limit (int): Max nodes, default 500, max 5000
Response:

JSON

{
  "nodes": [
    {
      "id": "author_1",
      "label": "ali_tehrani",
      "type": "author",
      "pagerank": 0.05,
      "degree": 25,
      "community": 1
    }
  ],
  "edges": [
    {
      "source": "author_1",
      "target": "author_2",
      "type": "mentions",
      "weight": 5.0
    }
  ]
}
GET /api/v1/graph/stats
Get graph statistics.

Response:

JSON

{
  "total_nodes": 1000,
  "total_edges": 5000,
  "node_types": {
    "author": 500,
    "hashtag": 300,
    "mention": 200
  },
  "edge_types": {
    "mentions": 3000,
    "co_occurrence": 2000
  },
  "communities_count": 15,
  "average_degree": 10.5,
  "density": 0.01
}
GET /api/v1/graph/nodes
List graph nodes.

Query Parameters:

node_type (str): Filter by type
page, page_size: Pagination
GET /api/v1/graph/nodes/top/pagerank
Get top nodes by PageRank.

Query Parameters:

node_type (str): Filter by type
limit (int): Number of results
Response:

JSON

[
  {
    "id": 1,
    "node_id": "author_1",
    "node_type": "author",
    "label": "ali_tehrani",
    "pagerank": 0.08,
    "degree": 50
  }
]
GET /api/v1/graph/nodes/top/degree
Get top nodes by degree.

GET /api/v1/graph/nodes/top/betweenness
Get top nodes by betweenness centrality.

GET /api/v1/graph/nodes/community/{community_id}
Get nodes in a community.

GET /api/v1/graph/nodes/{node_id}
Get node by ID.

GET /api/v1/graph/edges
List graph edges.

Query Parameters:

edge_type (str): Filter by type
POST /api/v1/graph/build/author-network
Build author interaction network (Analyst+).

Response:

JSON

{
  "message": "Author network build queued",
  "success": true
}
POST /api/v1/graph/build/hashtag-network
Build hashtag co-occurrence network (Analyst+).

Response:

JSON

{
  "message": "Built hashtag network: 100 nodes, 500 edges",
  "success": true
}
POST /api/v1/graph/calculate/pagerank
Calculate PageRank (Analyst+).

Response:

JSON

{
  "message": "PageRank calculation queued",
  "success": true
}
POST /api/v1/graph/detect/communities
Detect communities (Analyst+).

Response:

JSON

{
  "communities": 12,
  "communities_data": [
    {
      "community_id": 1,
      "size": 50,
      "density": 0.3
    }
  ]
}
POST /api/v1/graph/nodes
Create graph node (Analyst+).

Request:

JSON

{
  "node_id": "author_999",
  "node_type": "author",
  "label": "new_author"
}
POST /api/v1/graph/edges
Create graph edge (Analyst+).

Request:

JSON

{
  "edge_type": "mentions",
  "source_id": 1,
  "target_id": 2,
  "weight": 1.0
}
DELETE /api/v1/graph/nodes/{node_id}
Delete graph node (Analyst+).

9. Dashboard
GET /api/v1/dashboard/overview
Get dashboard overview statistics.

Response:

JSON

{
  "posts": {
    "total": 10000,
    "processed": 8000,
    "by_platform": {
      "twitter": 5000,
      "instagram": 3000,
      "telegram": 2000
    },
    "by_language": {
      "fa": 9000,
      "en": 1000
    }
  },
  "trends": {
    "active": 25,
    "total": 100
  },
  "graph": {
    "nodes": 2000,
    "communities": 15
  },
  "analyses": {
    "total": 50,
    "by_status": {
      "completed": 40,
      "processing": 5,
      "pending": 5
    }
  }
}
GET /api/v1/dashboard/sentiment
Get sentiment analysis overview.

Response:

JSON

{
  "distribution": {
    "positive": 5000,
    "negative": 2000,
    "neutral": 3000
  },
  "percentages": {
    "positive": 50.0,
    "negative": 20.0,
    "neutral": 30.0
  },
  "average_score": 0.35,
  "total_analyzed": 10000
}
GET /api/v1/dashboard/emotions
Get emotion analysis overview.

Response:

JSON

{
  "distribution": {
    "joy": 3000,
    "sadness": 1500,
    "anger": 1000,
    "fear": 500,
    "surprise": 1000
  },
  "percentages": {
    "joy": 42.9,
    "sadness": 21.4
  },
  "total_analyzed": 7000
}
GET /api/v1/dashboard/platforms
Get statistics by platform.

Response:

JSON

[
  {
    "platform": "twitter",
    "post_count": 5000,
    "percentage": 50.0
  },
  {
    "platform": "instagram",
    "post_count": 3000,
    "percentage": 30.0
  }
]
GET /api/v1/dashboard/widget/{widget_type}
Get data for specific widget.

Widget Types:

sentiment_chart
emotion_chart
trending_hashtags
trending_keywords
volume_chart
platform_stats
overview
top_authors
recent_analyses
Query Parameters:

hours (int): Time range
limit (int): Number of items
interval (str): Time interval
Example:

Bash

curl "http://localhost:8000/api/v1/dashboard/widget/trending_hashtags?hours=24&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
GET /api/v1/dashboard
List user's dashboards.

GET /api/v1/dashboard/public
List public dashboards.

GET /api/v1/dashboard/default
Get user's default dashboard.

GET /api/v1/dashboard/{dashboard_id}
Get dashboard by ID.

POST /api/v1/dashboard
Create dashboard.

Request:

JSON

{
  "name": "My Dashboard",
  "description": "Custom analytics dashboard",
  "widgets": [
    {
      "widget_id": "sentiment-1",
      "widget_type": "sentiment_chart",
      "title": "Sentiment Distribution",
      "position": {"x": 0, "y": 0, "w": 4, "h": 2}
    },
    {
      "widget_id": "hashtags-1",
      "widget_type": "trending_hashtags",
      "title": "Trending Hashtags",
      "position": {"x": 4, "y": 0, "w": 4, "h": 2}
    }
  ],
  "refresh_interval": 300,
  "is_default": false,
  "is_public": false
}
PUT /api/v1/dashboard/{dashboard_id}
Update dashboard.

POST /api/v1/dashboard/{dashboard_id}/set-default
Set dashboard as default.

POST /api/v1/dashboard/{dashboard_id}/duplicate
Duplicate dashboard.

Query Parameters:

new_name (str, required): Name for the copy
DELETE /api/v1/dashboard/{dashboard_id}
Delete dashboard.

10. BRAIN Service
GET /api/v1/brain/health
Check BRAIN service health.

Response:

JSON

{
  "status": "healthy",
  "gpu_available": true,
  "gpu_memory_used": 2048,
  "gpu_memory_total": 8192,
  "mode": "mock"
}
GET /api/v1/brain/available
Check BRAIN availability.

Response:

JSON

{
  "available": true
}
POST /api/v1/brain/analyze/sentiment
Analyze sentiment (Analyst+).

Request:

JSON

{
  "texts": [
    "این فیلم عالی بود!",
    "امروز روز بدی بود"
  ]
}
Response:

JSON

{
  "results": [
    {
      "text_id": "0",
      "sentiment": {
        "label": "positive",
        "score": 0.85,
        "confidence": 0.92
      }
    },
    {
      "text_id": "1",
      "sentiment": {
        "label": "negative",
        "score": -0.75,
        "confidence": 0.88
      }
    }
  ]
}
Example:

Bash

curl -X POST http://localhost:8000/api/v1/brain/analyze/sentiment \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["سلام دنیا", "خیلی بد بود"]}'
POST /api/v1/brain/analyze/emotions
Analyze emotions (Analyst+).

Request:

JSON

{
  "texts": ["خیلی خوشحالم امروز!"]
}
Response:

JSON

{
  "results": [
    {
      "text_id": "0",
      "emotions": {
        "joy": 0.8,
        "sadness": 0.05,
        "anger": 0.02,
        "fear": 0.03,
        "surprise": 0.1
      },
      "dominant_emotion": "joy"
    }
  ]
}
POST /api/v1/brain/analyze/text
Full text analysis (Analyst+).

Request:

JSON

{
  "texts": ["متن برای تحلیل"],
  "text_ids": ["post_123"],
  "analysis_types": ["sentiment", "emotion", "keywords", "entities"],
  "language": "fa",
  "config": {}
}
Response:

JSON

{
  "results": [
    {
      "text_id": "post_123",
      "sentiment": {"label": "positive", "score": 0.7},
      "emotions": {"joy": 0.6, "sadness": 0.1},
      "dominant_emotion": "joy",
      "keywords": ["کلمه۱", "کلمه۲"],
      "entities": [
        {"text": "تهران", "type": "location", "start": 0, "end": 5}
      ],
      "summary": "خلاصه متن"
    }
  ]
}
POST /api/v1/brain/summarize
Summarize texts (Analyst+).

Request:

JSON

{
  "texts": ["متن طولانی برای خلاصه‌سازی..."],
  "max_length": 150,
  "min_length": 30,
  "language": "fa"
}
Response:

JSON

{
  "summaries": ["خلاصه متن"]
}
POST /api/v1/brain/extract/keywords
Extract keywords (Analyst+).

Request:

JSON

{
  "texts": ["متن برای استخراج کلمات کلیدی"],
  "max_keywords": 10
}
Response:

JSON

{
  "keywords": [
    ["کلمه۱", "کلمه۲", "کلمه۳"]
  ]
}
POST /api/v1/brain/extract/entities
Extract named entities (Analyst+).

Request:

JSON

{
  "texts": ["علی از تهران به مشهد رفت"]
}
Response:

JSON

{
  "entities": [
    [
      {"text": "علی", "type": "person"},
      {"text": "تهران", "type": "location"},
      {"text": "مشهد", "type": "location"}
    ]
  ]
}
POST /api/v1/brain/detect/topics
Detect topics (Analyst+).

Request:

JSON

{
  "texts": ["لیست متن‌ها برای موضوع‌یابی"],
  "num_topics": 10
}
Response:

JSON

{
  "global_topics": [
    {"topic": "سیاست", "score": 0.8, "keywords": ["دولت", "مجلس"]}
  ],
  "document_topics": [
    [{"topic": "سیاست", "score": 0.9}]
  ]
}
11. Health & Status
GET /health
Backend health check.

Response:

JSON

{
  "status": "healthy",
  "service": "Persian Social Analytics",
  "version": "1.0.0",
  "redis": "connected"
}
GET /
Root endpoint with API info.

Response:

JSON

{
  "message": "Welcome to Persian Social Analytics API",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc",
  "health": "/health",
  "api": "/api/v1"
}
GET /api/v1/status
API v1 status.

Response:

JSON

{
  "api_version": "v1",
  "status": "operational",
  "endpoints": [
    "/auth", "/users", "/data-sources", "/authors",
    "/posts", "/analysis", "/trends", "/graph",
    "/dashboard", "/brain"
  ]
}
Quick Start Examples
Complete Flow Example
Bash

# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['tokens']['access_token'])")

echo "Token: $TOKEN"

# 2. Create posts
curl -X POST http://localhost:8000/api/v1/posts/bulk \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [
      {"platform_id": "p1", "platform": "twitter", "content": "سلام دنیا #تست"},
      {"platform_id": "p2", "platform": "twitter", "content": "امروز هوا خوب است"}
    ]
  }'

# 3. Create analysis
curl -X POST http://localhost:8000/api/v1/analysis \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Analysis",
    "analysis_type": "sentiment",
    "query_filters": {"platform": "twitter"}
  }'

# 4. Start analysis
curl -X POST http://localhost:8000/api/v1/analysis/1/start \
  -H "Authorization: Bearer $TOKEN"

# 5. Check progress
curl http://localhost:8000/api/v1/analysis/1/progress \
  -H "Authorization: Bearer $TOKEN"

# 6. Get results
curl http://localhost:8000/api/v1/analysis/1/summary \
  -H "Authorization: Bearer $TOKEN"

# 7. Check trends
curl "http://localhost:8000/api/v1/trends/hashtags?hours=24" \
  -H "Authorization: Bearer $TOKEN"

# 8. Get dashboard overview
curl http://localhost:8000/api/v1/dashboard/overview \
  -H "Authorization: Bearer $TOKEN"
User Roles & Permissions
Role	Permissions
viewer	Read-only access to posts, analyses, trends, dashboard
analyst	All viewer permissions + create/edit/delete data + run analyses
admin	All analyst permissions + user management
Rate Limits
Currently no rate limits implemented. For production, consider:

100 requests/minute for authenticated users
10 requests/minute for unauthenticated endpoints
Versioning
API versioning is handled via URL prefix:

Current: /api/v1/...
Future: /api/v2/...
Deprecated endpoints will be marked and supported for 6 months.

Support
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
OpenAPI JSON: http://localhost:8000/api/v1/openapi.json

================ TECHNICAL BACKEND/BRAIN SPEC ============

----- FILE: backend/technical_for_machine.md -----
PERSIAN SOCIAL MEDIA ANALYZER - TECHNICAL REFERENCE
PROJECT
Name: Persian Social Media Analyzer
Purpose: NLP analysis of Persian social media (sentiment, emotion, trends, graph analysis)
Modules: Backend (FastAPI) + BRAIN (RAPIDS/GPU) + Frontend (React) - 3 separate services

ARCHITECTURE
text

[Frontend:3000] --REST--> [Backend:8000] --REST--> [BRAIN:8001]
                               |
                    [PostgreSQL:5432] [Redis:6379]
                               |
                         [Celery Worker]
Communication: REST/JSON between all services. Redis for cache/queue.

STACK
Backend
Python 3.12
FastAPI 0.115.0 (web framework)
SQLAlchemy 2.0.35 (async ORM)
asyncpg 0.29.0 (PostgreSQL driver)
Alembic 1.13.2 (migrations)
Pydantic 2.9.2 (validation)
Celery 5.4.0 (task queue)
Redis 5.0.8 (cache/broker)
python-jose 3.3.0 (JWT)
passlib 1.7.4 (password hashing)
httpx 0.27.2 (HTTP client for BRAIN)
loguru 0.7.2 (logging)
orjson 3.10.7 (fast JSON)
Database
PostgreSQL 16
Redis 7
BRAIN (To Build)
RAPIDS cuDF/cuGraph (GPU dataframes/graphs)
PyTorch + Transformers
ParsBERT (Persian BERT)
cuML (GPU ML)
Frontend (To Build)
React/Next.js
TailwindCSS
Chart.js/Recharts
PROJECT STRUCTURE
text

backend/
├── app/
│   ├── main.py                 # FastAPI app entry
│   ├── database.py             # DB connection, session
│   ├── api/
│   │   ├── deps.py             # Dependencies (auth, db session)
│   │   └── v1/
│   │       ├── router.py       # API router
│   │       └── endpoints/      # Route handlers
│   │           ├── auth.py
│   │           ├── users.py
│   │           ├── posts.py
│   │           ├── analysis.py
│   │           ├── trends.py
│   │           ├── graph.py
│   │           ├── dashboard.py
│   │           ├── authors.py
│   │           ├── data_sources.py
│   │           └── brain.py
│   ├── core/
│   │   ├── config.py           # Settings from env
│   │   └── security.py         # JWT, password hashing
│   ├── models/                 # SQLAlchemy models
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── author.py
│   │   ├── analysis.py
│   │   ├── analysis_result.py
│   │   ├── trend.py
│   │   ├── graph.py
│   │   ├── dashboard.py
│   │   └── data_source.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── analysis.py
│   │   ├── analysis_result.py
│   │   ├── trend.py
│   │   ├── graph.py
│   │   ├── dashboard.py
│   │   ├── author.py
│   │   ├── data_source.py
│   │   └── brain.py
│   ├── crud/                   # Database operations
│   │   ├── base.py             # Generic CRUD class
│   │   ├── crud_user.py
│   │   ├── crud_post.py
│   │   ├── crud_author.py
│   │   ├── crud_analysis.py
│   │   ├── crud_analysis_result.py
│   │   ├── crud_trend.py
│   │   ├── crud_graph.py
│   │   ├── crud_dashboard.py
│   │   └── crud_data_source.py
│   ├── services/               # Business logic
│   │   ├── base.py
│   │   ├── auth_service.py
│   │   ├── brain_service.py    # HTTP client for BRAIN
│   │   ├── analysis_service.py
│   │   ├── graph_service.py
│   │   ├── trend_service.py
│   │   ├── dashboard_service.py
│   │   ├── redis_service.py
│   │   ├── celery_app.py       # Celery config
│   │   └── tasks.py            # Background tasks
│   └── utils/
│       ├── text.py             # Persian text processing
│       ├── datetime.py
│       ├── pagination.py
│       ├── validators.py
│       ├── security.py
│       └── json.py
├── alembic/                    # DB migrations
├── scripts/
│   ├── init_db.py
│   └── seed_data.py
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env
DATABASE TABLES
users
id, email, username, hashed_password, full_name, is_active, is_superuser, role(admin/analyst/viewer), created_at, updated_at

data_sources
id, name, platform(twitter/instagram/telegram/linkedin/youtube/news/forum/custom), api_endpoint, credentials(JSON), collection_config(JSON), description, is_active, last_sync_at, created_at, updated_at

authors
id, platform_id, platform, username, display_name, bio, profile_url, avatar_url, followers_count, following_count, posts_count, influence_score, pagerank_score, extra_data(JSON), created_at, updated_at

posts
id, platform_id(unique), platform, content, content_normalized, language, url, media_urls(JSON), likes_count, comments_count, shares_count, views_count, posted_at, hashtags(JSON), mentions(JSON), is_processed, processing_error, data_source_id(FK), author_id(FK), created_at, updated_at

analyses
id, name, description, analysis_type(sentiment/emotion/summarization/topic_modeling/keyword_extraction/entity_recognition/trend_detection/graph_analysis/full), config(JSON), query_filters(JSON), post_count, status(pending/queued/processing/completed/failed/cancelled), progress, summary(JSON), error_message, started_at, completed_at, user_id(FK), created_at, updated_at

analysis_results
id, sentiment_label, sentiment_score, sentiment_confidence, emotions(JSON), dominant_emotion, summary, keywords(JSON), topics(JSON), entities(JSON), node_degree, centrality_score, community_id, raw_results(JSON), post_id(FK), analysis_id(FK), created_at, updated_at

trends
id, name, description, volume, growth_rate, velocity, peak_time, keywords(JSON), hashtags(JSON), sentiment_distribution(JSON), time_series(JSON), geo_distribution(JSON), top_authors(JSON), top_posts(JSON), is_active(active/declining/ended), analysis_id(FK), created_at, updated_at

graph_nodes
id, node_id(unique), node_type(author/hashtag/topic/keyword/post), label, attributes(JSON), degree, in_degree, out_degree, pagerank, betweenness_centrality, closeness_centrality, eigenvector_centrality, community_id, created_at, updated_at

graph_edges
id, edge_type(mentions/replies_to/retweets/follows/co_occurrence), weight, attributes(JSON), first_seen, last_seen, occurrence_count, source_id(FK→graph_nodes), target_id(FK→graph_nodes), created_at, updated_at

dashboards
id, name, description, layout(JSON), widgets(JSON), filters(JSON), refresh_interval, is_default, is_public, user_id(FK), created_at, updated_at

API ENDPOINTS
Auth (/api/v1/auth)
POST /login - login, returns JWT tokens
POST /register - create account
POST /refresh - refresh access token
GET /me - current user info
POST /logout - logout
POST /change-password - change password
Users (/api/v1/users)
GET / - list users (admin)
GET /{id} - get user
POST / - create user (admin)
PUT /{id} - update user
DELETE /{id} - delete user (admin)
POST /{id}/activate - activate user (admin)
POST /{id}/deactivate - deactivate user (admin)
Posts (/api/v1/posts)
GET / - list posts (filterable: platform, language, date_from, date_to, search, hashtags)
GET /stats - post statistics
GET /unprocessed - unprocessed posts
GET /search?q= - search posts
GET /by-hashtag/{hashtag} - posts by hashtag
GET /{id} - get post with relations
POST / - create post
POST /bulk - bulk create posts
PUT /{id} - update post
DELETE /{id} - delete post
Analysis (/api/v1/analysis)
GET / - list analyses
GET /stats - analysis statistics
GET /pending - pending analyses
GET /{id} - get analysis
GET /{id}/progress - get progress
GET /{id}/results - get results
GET /{id}/summary - get summary
POST / - create analysis
POST /{id}/start - start analysis (queues Celery task)
POST /{id}/cancel - cancel analysis
PUT /{id} - update analysis
DELETE /{id} - delete analysis and results
Trends (/api/v1/trends)
GET / - list trends
GET /summary - trend summary
GET /hashtags - trending hashtags
GET /keywords - trending keywords
GET /sentiment - sentiment over time
GET /volume - post volume over time
GET /top/volume - top trends by volume
GET /top/growth - top trends by growth
GET /stats - trend statistics
GET /{id} - get trend details
POST /detect - trigger trend detection
POST / - create trend
PUT /{id} - update trend
DELETE /{id} - delete trend
Graph (/api/v1/graph)
GET /data - graph data for visualization
GET /stats - graph statistics
GET /nodes - list nodes
GET /nodes/top/pagerank - top by pagerank
GET /nodes/top/degree - top by degree
GET /nodes/top/betweenness - top by betweenness
GET /nodes/community/{id} - nodes in community
GET /nodes/{id} - get node
GET /edges - list edges
POST /build/author-network - build author network
POST /build/hashtag-network - build hashtag network
POST /calculate/pagerank - calculate pagerank
POST /detect/communities - detect communities
POST /nodes - create node
POST /edges - create edge
DELETE /nodes/{id} - delete node
Dashboard (/api/v1/dashboard)
GET /overview - overview stats
GET /sentiment - sentiment overview
GET /emotions - emotion overview
GET /platforms - platform stats
GET /widget/{type} - widget data
GET / - user dashboards
GET /public - public dashboards
GET /default - default dashboard
GET /{id} - get dashboard
POST / - create dashboard
PUT /{id} - update dashboard
POST /{id}/set-default - set as default
POST /{id}/duplicate - duplicate dashboard
DELETE /{id} - delete dashboard
Authors (/api/v1/authors)
GET / - list authors
GET /top/followers - top by followers
GET /top/pagerank - top by pagerank
GET /top/influence - top by influence
GET /stats - author statistics
GET /{id} - get author
POST / - create author
PUT /{id} - update author
DELETE /{id} - delete author
Data Sources (/api/v1/data-sources)
GET / - list sources
GET /{id} - get source
GET /{id}/stats - source statistics
POST / - create source
PUT /{id} - update source
DELETE /{id} - delete source
POST /{id}/activate - activate source
POST /{id}/deactivate - deactivate source
Brain (/api/v1/brain)
GET /health - BRAIN health check
GET /available - BRAIN availability
POST /analyze/sentiment - sentiment analysis
POST /analyze/emotions - emotion analysis
POST /analyze/text - full text analysis
POST /summarize - summarization
POST /extract/keywords - keyword extraction
POST /extract/entities - NER
POST /detect/topics - topic modeling
Health
GET /health - backend health
GET / - root info
SERVICES
auth_service: authentication, JWT tokens, password management
brain_service: HTTP client to BRAIN, handles all AI requests
analysis_service: orchestrates analysis jobs, processes results
graph_service: builds networks, calculates graph metrics
trend_service: detects trends, aggregates hashtags/keywords
dashboard_service: dashboard stats, widget data
redis_service: caching, pub/sub, analysis progress
CELERY TASKS
process_analysis: main analysis job, calls BRAIN, stores results
detect_trends: finds trending hashtags/keywords
detect_trends_periodic: hourly trend detection
update_trend_status_periodic: updates trend status every 30min
build_graph: builds author/hashtag networks
calculate_pagerank: calculates PageRank via BRAIN
cleanup_old_results: deletes results older than 30 days
Queues: default, analysis, trends, graph
Broker: redis://redis:6379/1
Backend: redis://redis:6379/2

DOCKER
Containers
persian_analytics_db (postgres:16-alpine) - port 5432
persian_analytics_redis (redis:7-alpine) - internal 6379
persian_analytics_backend (custom) - port 8000
persian_analytics_celery (custom) - no port
Volumes
postgres_data
redis_data
Network
backend_app_network (bridge)
ENV VARS
text

APP_NAME, APP_VERSION, DEBUG, SECRET_KEY, API_V1_PREFIX
HOST, PORT
DATABASE_URL (postgresql+asyncpg://...)
DATABASE_SYNC_URL (postgresql://...)
REDIS_URL
BRAIN_SERVICE_URL, BRAIN_SERVICE_TIMEOUT
ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHM
CORS_ORIGINS
CELERY_BROKER_URL, CELERY_RESULT_BACKEND
BRAIN MODULE SPEC (To Build)
Endpoints to Implement
text

GET  /health                → {"status": "healthy", "gpu_available": true}
POST /analyze/sentiment     → sentiment analysis
POST /analyze/emotion       → emotion detection
POST /analyze/text          → full NLP pipeline
POST /analyze/summarize     → text summarization
POST /analyze/keywords      → keyword extraction
POST /analyze/entities      → NER
POST /analyze/topics        → topic modeling
POST /analyze/trends        → trend detection
POST /analyze/graph         → graph analysis
POST /analyze/graph/pagerank → PageRank calculation
POST /analyze/graph/communities → community detection
POST /batch/analyze         → batch analysis (async)
GET  /batch/status/{task_id} → batch status
GET  /batch/result/{task_id} → batch result
Input Format
JSON

{
  "texts": ["text1", "text2"],
  "text_ids": ["id1", "id2"],
  "analysis_types": ["sentiment", "emotion", "keywords"],
  "language": "fa",
  "config": {}
}
Output Format
JSON

{
  "results": [
    {
      "text_id": "id1",
      "sentiment": {"label": "positive", "score": 0.85, "confidence": 0.92},
      "emotions": {"joy": 0.7, "sadness": 0.1, "anger": 0.05, "fear": 0.05, "surprise": 0.1},
      "keywords": ["کلمه۱", "کلمه۲"],
      "entities": [{"text": "تهران", "type": "location", "start": 0, "end": 5}],
      "summary": "خلاصه متن",
      "topics": [{"topic": "سیاست", "score": 0.8}]
    }
  ]
}
Models to Use
ParsBERT (sentiment, emotion)
mT5 or ParsBERT (summarization)
Custom NER for Persian
BERTopic or LDA (topics)
cuGraph (PageRank, communities)
AUTH FLOW
POST /auth/login → returns access_token + refresh_token
All protected routes: Header "Authorization: Bearer {access_token}"
Token expired: POST /auth/refresh with refresh_token
Roles: admin (full access), analyst (CRUD + analysis), viewer (read only)
PATTERNS USED
Repository Pattern (CRUD layer)
Service Layer Pattern
Dependency Injection (FastAPI Depends)
Singleton (service instances)
Factory (session factory)
DTO Pattern (Pydantic schemas)
Async/Await throughout
KEY FILES FOR MODIFICATIONS
Add new model: app/models/ → app/schemas/ → app/crud/ → app/api/v1/endpoints/
Add new endpoint: app/api/v1/endpoints/{name}.py → app/api/v1/router.py
Add new service: app/services/{name}.py → app/services/init.py
Add new task: app/services/tasks.py → register in celery_app.py
Add migration: alembic revision --autogenerate -m "description"
IMPORTANT NOTES
All models use BaseModel (includes id, created_at, updated_at)
Author.extra_data (not metadata - reserved by SQLAlchemy)
Volume mount ./app:/app/app enables hot reload
BRAIN communicates via HTTP REST only
Redis used for: caching, Celery broker, analysis progress tracking
JWT tokens: access (30min), refresh (7 days)
Default admin: admin@example.com / Admin123!

================ BACKEND CONFIG SNIPPET ==================

----- FILE: backend/app/core/config.py -----
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "Persian Social Analytics"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    API_V1_PREFIX: str = "/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/persian_analytics"
    DATABASE_SYNC_URL: str = "postgresql://postgres:postgres@localhost:5432/persian_analytics"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # BRAIN Service
    BRAIN_SERVICE_URL: str = "http://localhost:8001"
    BRAIN_SERVICE_TIMEOUT: int = 300
    
    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Default Admin User (created on startup)
    DEFAULT_ADMIN_EMAIL: str = "admin@example.com"
    DEFAULT_ADMIN_USERNAME: str = "admin"
    DEFAULT_ADMIN_PASSWORD: str = "Admin123!"
    
    # Auto-initialization
    AUTO_INIT_DB: bool = True
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v


# Create global settings instance
settings = Settings()

================ API ROUTER & ENDPOINTS ==================

----- FILE: backend/app/api/v1/router.py -----
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    data_sources,
    authors,
    posts,
    analysis,
    trends,
    graph,
    dashboard,
    brain
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    data_sources.router,
    prefix="/data-sources",
    tags=["Data Sources"]
)

api_router.include_router(
    authors.router,
    prefix="/authors",
    tags=["Authors"]
)

api_router.include_router(
    posts.router,
    prefix="/posts",
    tags=["Posts"]
)

api_router.include_router(
    analysis.router,
    prefix="/analysis",
    tags=["Analysis"]
)

api_router.include_router(
    trends.router,
    prefix="/trends",
    tags=["Trends"]
)

api_router.include_router(
    graph.router,
    prefix="/graph",
    tags=["Graph Analysis"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)

api_router.include_router(
    brain.router,
    prefix="/brain",
    tags=["BRAIN Service"]
)


@api_router.get("/status")
async def api_status():
    """API v1 status check."""
    return {
        "api_version": "v1",
        "status": "operational",
        "endpoints": [
            "/auth",
            "/users",
            "/data-sources",
            "/authors",
            "/posts",
            "/analysis",
            "/trends",
            "/graph",
            "/dashboard",
            "/brain"
        ]
    }

----- TREE: backend/app/api/v1/endpoints -----
__init__.py
analysis.py
auth.py
authors.py
brain.py
dashboard.py
data_sources.py
graph.py
graph.py.backup
posts.py
trends.py
users.py

==================== CONTEXT END =========================
