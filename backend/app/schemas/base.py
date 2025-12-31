from datetime import datetime
from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel, ConfigDict

# Generic type for pagination
T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields."""
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class IDSchema(BaseSchema):
    """Schema with ID field."""
    
    id: int


class PaginationParams(BaseSchema):
    """Pagination parameters."""
    
    page: int = 1
    page_size: int = 20
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponse(BaseSchema, Generic[T]):
    """Generic paginated response."""
    
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class MessageResponse(BaseSchema):
    """Simple message response."""
    
    message: str
    success: bool = True


class ErrorResponse(BaseSchema):
    """Error response schema."""
    
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
