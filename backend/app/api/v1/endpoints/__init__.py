"""
API v1 endpoints.
"""

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

__all__ = [
    "auth",
    "users",
    "data_sources",
    "authors",
    "posts",
    "analysis",
    "trends",
    "graph",
    "dashboard",
    "brain",
]
