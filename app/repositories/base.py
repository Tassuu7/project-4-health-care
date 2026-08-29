"""
AegisCare Enterprise Patient Management System - Generic Base Repository
Implements type-safe CRUD operations, pagination, search, and transactional operations.
"""

from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository providing standardized database access methods."""

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: Any) -> Optional[ModelType]:
        """Fetch a single record by primary key."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Retrieve all active records with offset and limit."""
        query = self.db.query(self.model)
        if hasattr(self.model, "is_deleted"):
            query = query.filter(self.model.is_deleted == False)
        return query.offset(skip).limit(limit).all()

    def get_paginated(
        self,
        page: int = 1,
        limit: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        search_query: Optional[str] = None,
        search_fields: Optional[List[str]] = None,
        order_by: str = "id",
        descending: bool = True
    ) -> Tuple[List[ModelType], int]:
        """Fetch paginated results with dynamic filtering and total row count."""
        query = self.db.query(self.model)
        
        # Soft delete exclusion
        if hasattr(self.model, "is_deleted"):
            query = query.filter(self.model.is_deleted == False)
            
        # Exact filters
        if filters:
            for field, val in filters.items():
                if hasattr(self.model, field) and val is not None:
                    query = query.filter(getattr(self.model, field) == val)
                    
        # Text search across multiple fields
        if search_query and search_fields:
            search_filters = []
            for field in search_fields:
                if hasattr(self.model, field):
                    search_filters.append(getattr(self.model, field).ilike(f"%{search_query}%"))
            if search_filters:
                from sqlalchemy import or_
                query = query.filter(or_(*search_filters))

        total_count = query.count()
        
        # Sorting
        if hasattr(self.model, order_by):
            sort_col = getattr(self.model, order_by)
            query = query.order_by(desc(sort_col) if descending else sort_col)
            
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()
        return items, total_count

    def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Instantiate and persist a new model record."""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        """Update existing record attributes and commit changes."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: Any) -> bool:
        """Permanently remove or soft-delete a record."""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
            
        if hasattr(db_obj, "soft_delete"):
            db_obj.soft_delete()
        else:
            self.db.delete(db_obj)
            
        self.db.commit()
        return True

    def count(self) -> int:
        """Count total active records in table."""
        query = self.db.query(func.count(self.model.id))
        if hasattr(self.model, "is_deleted"):
            query = query.filter(self.model.is_deleted == False)
        return query.scalar() or 0
