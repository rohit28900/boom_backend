from typing import TypeVar, Generic, List
from pydantic import BaseModel
from sqlalchemy.orm import Query
from math import ceil

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = 1
    page_size: int = 10
    
    class Config:
        frozen = True
    
    def get_offset(self) -> int:
        """Calculate offset for database query"""
        return (self.page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """Get limit for database query"""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    
    class Config:
        arbitrary_types_allowed = True


class Pagination:
    """Utility class for pagination"""
    
    @staticmethod
    def paginate(query: Query, params: PaginationParams) -> tuple:
        """
        Paginate a SQLAlchemy query
        
        Args:
            query: SQLAlchemy query object
            params: Pagination parameters
            
        Returns:
            Tuple of (items, total_count)
        """
        total = query.count()
        items = query.offset(params.get_offset()).limit(params.get_limit()).all()
        return items, total
    
    @staticmethod
    def create_response(
        items: List[T],
        total: int,
        params: PaginationParams
    ) -> PaginatedResponse[T]:
        """
        Create paginated response with metadata
        
        Args:
            items: List of items for current page
            total: Total count of items
            params: Pagination parameters
            
        Returns:
            PaginatedResponse object
        """
        total_pages = ceil(total / params.page_size) if params.page_size > 0 else 0
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_prev=params.page > 1
        )
    
    @staticmethod
    def paginate_and_respond(
        query: Query,
        params: PaginationParams
    ) -> PaginatedResponse[T]:
        """
        Convenience method to paginate and create response in one call
        
        Args:
            query: SQLAlchemy query object
            params: Pagination parameters
            
        Returns:
            PaginatedResponse object
        """
        items, total = Pagination.paginate(query, params)
        return Pagination.create_response(items, total, params)