"""
AegisCare Enterprise Patient Management System - SQLAlchemy Declarative Base & Mixins
Provides audit timestamps, UUID primary keys, soft-deletion, and helper utilities.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Root declarative base class for all SQLAlchemy ORM models."""
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Generate table name automatically from class name (pluralized lowercase)
        name = cls.__name__.lower()
        if name.endswith("y"):
            return name[:-1] + "ies"
        elif not name.endswith("s"):
            return name + "s"
        return name


class TimestampMixin:
    """Mixin adding created_at and updated_at timestamp columns with automatic triggers."""
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        doc="Timestamp when the record was initially created"
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        doc="Timestamp when the record was last modified"
    )


class SoftDeleteMixin:
    """Mixin enabling soft deletion without destructive database purging."""
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        """Mark record as soft-deleted."""
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        """Restore soft-deleted record."""
        self.is_deleted = False
        self.deleted_at = None


class AuditMixin:
    """Mixin tracking creator and modifier user identifiers for HIPAA traceability."""
    created_by_id = Column(Integer, nullable=True)
    updated_by_id = Column(Integer, nullable=True)
