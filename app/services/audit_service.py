"""
AegisCare Enterprise Patient Management System - Audit Service
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from app.repositories.audit_repo import AuditRepository


class AuditService:
    """Security audit queries and HIPAA access compliance reporting."""

    def __init__(self, db: Session):
        self.db = db
        self.audit_repo = AuditRepository(db)

    def get_compliance_audit_trail(self, limit: int = 100) -> List[AuditLog]:
        """Fetch audit log events for compliance inspection."""
        return self.audit_repo.get_recent_logs(limit=limit)
