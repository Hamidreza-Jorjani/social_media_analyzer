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
