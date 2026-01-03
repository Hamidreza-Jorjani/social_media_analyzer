=== FRONTEND LIVE CONTEXT (MINIMAL) ===

Backend:
  URL:      http://localhost:18000
  API base: http://localhost:18000/api/v1

BRAIN:
  URL:      http://localhost:18001

Frontend .env.local (dev):
  NEXT_PUBLIC_API_URL=http://localhost:18000/api/v1

=== LIVE HEALTH CHECKS ===

-- Backend /health --
{"status":"healthy","service":"Persian Social Analytics","version":"1.0.0","redis":"connected"}

-- /api/v1/status --
{"api_version":"v1","status":"operational","endpoints":["/auth","/users","/data-sources","/authors","/posts","/analysis","/trends","/graph","/dashboard","/brain"]}

-- BRAIN /health --
{"status":"healthy","service":"BRAIN Mock Service","version":"1.0.0","gpu_available":true,"gpu_memory_used":2048,"gpu_memory_total":8192,"mode":"mock"}

=== OPENAPI SUMMARY (LIVE) ===
Source: http://localhost:18000/api/v1/openapi.json

-- Basic info --
{
  "title": "Persian Social Analytics",
  "version": "1.0.0"
}

-- Paths (method -> path) --
[
  {
    "path": "/health",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/auth/login",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/auth/register",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/auth/refresh",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/auth/me",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/auth/logout",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/auth/change-password",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/users",
    "methods": [
      "get",
      "post"
    ]
  },
  {
    "path": "/api/v1/users/{user_id}",
    "methods": [
      "delete",
      "get",
      "put"
    ]
  },
  {
    "path": "/api/v1/users/{user_id}/activate",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/users/{user_id}/deactivate",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/data-sources",
    "methods": [
      "get",
      "post"
    ]
  },
  {
    "path": "/api/v1/data-sources/{source_id}",
    "methods": [
      "delete",
      "get",
      "put"
    ]
  },
  {
    "path": "/api/v1/data-sources/{source_id}/stats",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/data-sources/{source_id}/activate",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/data-sources/{source_id}/deactivate",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/authors",
    "methods": [
      "get",
      "post"
    ]
  },
  {
    "path": "/api/v1/authors/top/followers",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/authors/top/pagerank",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/authors/top/influence",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/authors/stats",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/authors/{author_id}",
    "methods": [
      "delete",
      "get",
      "put"
    ]
  },
  {
    "path": "/api/v1/posts",
    "methods": [
      "get",
      "post"
    ]
  },
  {
    "path": "/api/v1/posts/stats",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/posts/unprocessed",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/posts/search",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/posts/by-hashtag/{hashtag}",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/posts/{post_id}",
    "methods": [
      "delete",
      "get",
      "put"
    ]
  },
  {
    "path": "/api/v1/posts/bulk",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/analysis",
    "methods": [
      "get",
      "post"
    ]
  },
  {
    "path": "/api/v1/analysis/stats",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/analysis/pending",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/analysis/{analysis_id}",
    "methods": [
      "delete",
      "get",
      "put"
    ]
  },
  {
    "path": "/api/v1/analysis/{analysis_id}/progress",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/analysis/{analysis_id}/results",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/analysis/{analysis_id}/summary",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/analysis/{analysis_id}/start",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/analysis/{analysis_id}/cancel",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/trends",
    "methods": [
      "get",
      "post"
    ]
  },
  {
    "path": "/api/v1/trends/summary",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/trends/hashtags",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/trends/keywords",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/trends/sentiment",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/trends/volume",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/trends/top/volume",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/trends/top/growth",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/trends/stats",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/trends/{trend_id}",
    "methods": [
      "delete",
      "get",
      "put"
    ]
  },
  {
    "path": "/api/v1/trends/detect",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/graph/data",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/graph/stats",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/graph/nodes",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/graph/nodes/top/pagerank",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/graph/nodes/top/degree",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/graph/nodes/top/betweenness",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/graph/nodes/community/{community_id}",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/graph/nodes/{node_id}",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/graph/edges",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/graph/build/hashtag-network",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/graph/calculate/pagerank",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/graph/detect/communities",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/graph/clear",
    "methods": [
      "delete"
    ]
  },
  {
    "path": "/api/v1/dashboard/overview",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/dashboard/sentiment",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/dashboard/emotions",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/dashboard/platforms",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/dashboard/widget/{widget_type}",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/dashboard",
    "methods": [
      "get",
      "post"
    ]
  },
  {
    "path": "/api/v1/dashboard/public",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/dashboard/default",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/dashboard/{dashboard_id}",
    "methods": [
      "delete",
      "get",
      "put"
    ]
  },
  {
    "path": "/api/v1/dashboard/{dashboard_id}/set-default",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/dashboard/{dashboard_id}/duplicate",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/brain/health",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/brain/available",
    "methods": [
      "get"
    ]
  },
  {
    "path": "/api/v1/brain/analyze/sentiment",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/brain/analyze/emotions",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/brain/analyze/text",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/brain/summarize",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/brain/extract/keywords",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/brain/extract/entities",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/brain/detect/topics",
    "methods": [
      "post"
    ]
  },
  {
    "path": "/api/v1/status",
    "methods": [
      "get"
    ]
  }
]

=== END FRONTEND LIVE CONTEXT (MINIMAL) ===
