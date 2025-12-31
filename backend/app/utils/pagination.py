from typing import TypeVar, Generic, List, Any, Optional
from pydantic import BaseModel
from math import ceil

T = TypeVar('T')


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PaginatedResult(BaseModel, Generic[T]):
    """Paginated result container."""
    
    items: List[Any]
    meta: PaginationMeta


def paginate(
    items: List[T],
    page: int = 1,
    page_size: int = 20,
    total: Optional[int] = None
) -> PaginatedResult:
    """
    Create paginated result from items list.
    """
    if total is None:
        total = len(items)
    
    total_pages = ceil(total / page_size) if page_size > 0 else 0
    
    meta = PaginationMeta(
        page=page,
        page_size=page_size,
        total_items=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    
    return PaginatedResult(items=items, meta=meta)


def get_pagination_params(
    page: int = 1,
    page_size: int = 20,
    max_page_size: int = 100
) -> tuple[int, int]:
    """
    Validate and return skip/limit values for database queries.
    """
    page = max(1, page)
    page_size = max(1, min(page_size, max_page_size))
    
    skip = (page - 1) * page_size
    limit = page_size
    
    return skip, limit


def paginate_list(
    items: List[T],
    page: int = 1,
    page_size: int = 20
) -> List[T]:
    """
    Paginate a list in memory.
    """
    skip, limit = get_pagination_params(page, page_size)
    return items[skip:skip + limit]
