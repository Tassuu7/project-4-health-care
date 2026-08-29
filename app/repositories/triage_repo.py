"""
AegisCare Enterprise Patient Management System - Triage Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.triage import TriageAssessment
from app.repositories.base import BaseRepository


class TriageRepository(BaseRepository[TriageAssessment]):
    """Data access repository for Emergency Department triage records and waiting queues."""

    def __init__(self, db: Session):
        super().__init__(TriageAssessment, db)

    def get_active_emergency_queue(self) -> List[TriageAssessment]:
        """Retrieve active emergency patients sorted by clinical acuity (ESI 1 to 5)."""
        return self.db.query(TriageAssessment).options(
            joinedload(TriageAssessment.patient),
            joinedload(TriageAssessment.nurse)
        ).filter(
            TriageAssessment.is_active == True
        ).order_by(
            TriageAssessment.triage_level.asc(),
            TriageAssessment.created_at.asc()
        ).all()
