"""
AegisCare Enterprise Patient Management System - Laboratory Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.core.constants import LabOrderStatus
from app.models.laboratory import LabOrder, LabResult, LabTestCatalog
from app.repositories.base import BaseRepository


class LaboratoryRepository(BaseRepository[LabOrder]):
    """Data access repository for Diagnostic Tests, Orders, and Results."""

    def __init__(self, db: Session):
        super().__init__(LabOrder, db)

    def get_order_with_results(self, order_id: int) -> Optional[LabOrder]:
        """Fetch lab order with test results and patient details."""
        return self.db.query(LabOrder).options(
            joinedload(LabOrder.results).joinedload(LabResult.test),
            joinedload(LabOrder.patient),
            joinedload(LabOrder.doctor)
        ).filter(
            LabOrder.id == order_id,
            LabOrder.is_deleted == False
        ).first()

    def get_pending_queue(self) -> List[LabOrder]:
        """Retrieve all pending diagnostic orders awaiting analysis or verification."""
        return self.db.query(LabOrder).options(
            joinedload(LabOrder.patient),
            joinedload(LabOrder.results).joinedload(LabResult.test)
        ).filter(
            LabOrder.status.in_([LabOrderStatus.ORDERED, LabOrderStatus.SAMPLE_COLLECTED, LabOrderStatus.IN_ANALYSIS]),
            LabOrder.is_deleted == False
        ).order_by(LabOrder.created_at.asc()).all()

    def get_all_catalog_tests(self) -> List[LabTestCatalog]:
        """List active diagnostic test catalogue."""
        return self.db.query(LabTestCatalog).filter(LabTestCatalog.is_active == True).order_by(LabTestCatalog.name.asc()).all()
