"""
CRUD operations for Persian Social Analytics.
"""

from app.crud.base import CRUDBase
from app.crud.crud_user import user
from app.crud.crud_data_source import data_source
from app.crud.crud_author import author
from app.crud.crud_post import post
from app.crud.crud_analysis import analysis
from app.crud.crud_analysis_result import analysis_result
from app.crud.crud_trend import trend
from app.crud.crud_graph import graph_node, graph_edge
from app.crud.crud_dashboard import dashboard

__all__ = [
    "CRUDBase",
    "user",
    "data_source",
    "author",
    "post",
    "analysis",
    "analysis_result",
    "trend",
    "graph_node",
    "graph_edge",
    "dashboard",
]
