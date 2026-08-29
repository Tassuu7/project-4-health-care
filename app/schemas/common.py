"""
AegisCare Enterprise Patient Management System - Common Pydantic Schemas
Provides standard response envelopes, pagination schemas, and error structures.
"""

from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ResponseEnvelope(BaseModel, Generic[T]):
    """Standardized API response wrapper."""
    success: bool = Field(default=True)
    message: str = Field(default="Operation completed successfully")
    data: Optional[T] = None
    code: str = Field(default="OK")


class PaginationParams(BaseModel):
    """Query parameters for paginated database listing."""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    search: Optional[str] = None
    sort_by: str = Field(default="id")
    sort_desc: bool = Field(default=True)


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated collection envelope."""
    items: List[T]
    total_count: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_prev: bool
