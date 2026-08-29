"""
AegisCare Enterprise Patient Management System - Ward & Inpatient Bed Service
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.constants import BedStatus
from app.core.exceptions import BedUnavailableException, ResourceNotFoundError
from app.models.ward import Bed, BedAllocation
from app.repositories.ward_repo import WardRepository


class WardService:
    """Inpatient bed management, room allocation, and patient discharge clearance."""

    def __init__(self, db: Session):
        self.db = db
        self.ward_repo = WardRepository(db)

    def admit_patient_to_bed(self, bed_id: int, patient_id: int, admission_reason: str) -> BedAllocation:
        """Assign an available inpatient hospital bed to a patient."""
        bed = self.db.query(Bed).filter(Bed.id == bed_id).first()
        if not bed:
            raise ResourceNotFoundError("Bed", bed_id)
        if bed.status != BedStatus.AVAILABLE:
            raise BedUnavailableException(bed.bed_identifier, "Ward", bed.status.value)

        bed.status = BedStatus.OCCUPIED
        allocation = BedAllocation(
            bed_id=bed.id,
            patient_id=patient_id,
            admission_reason=admission_reason,
            is_active=True
        )
        self.db.add(allocation)
        self.db.commit()
        self.db.refresh(allocation)
        return allocation

    def discharge_patient(self, allocation_id: int) -> BedAllocation:
        """Discharge patient and release bed for sanitization."""
        alloc = self.db.query(BedAllocation).filter(BedAllocation.id == allocation_id).first()
        if not alloc:
            raise ResourceNotFoundError("BedAllocation", allocation_id)
        
        alloc.is_active = False
        alloc.discharged_at = datetime.utcnow()
        
        bed = self.db.query(Bed).filter(Bed.id == alloc.bed_id).first()
        if bed:
            bed.status = BedStatus.CLEANING
            
        self.db.commit()
        return alloc
