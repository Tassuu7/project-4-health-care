"""
AegisCare Enterprise Patient Management System - Audit Repository
"""

from typing import List, Optional, Tuple
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.core.constants import AuditAction
from app.models.audit import AuditLog


class AuditRepository:
    """Data access repository for HIPAA Compliance Audit Logs."""

    def __init__(self, db: Session):
        self.db = db

    def log_event(
        self,
        action: AuditAction,
        resource_type: str,
        resource_id: Optional[str] = None,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        user_role: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[str] = None
    ) -> AuditLog:
        """Persist an immutable audit log entry."""
        entry = AuditLog(
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id else None,
            user_id=user_id,
            username=username,
            user_role=user_role,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_recent_logs(self, limit: int = 100) -> List[AuditLog]:
        """Fetch most recent audit log entries for security oversight."""
        return self.db.query(AuditLog).order_by(desc(AuditLog.timestamp)).limit(limit).all()
