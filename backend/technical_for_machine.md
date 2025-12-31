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
