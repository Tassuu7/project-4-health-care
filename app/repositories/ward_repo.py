"""
AegisCare Enterprise Patient Management System - Ward & Bed Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.core.constants import BedStatus
from app.models.ward import Bed, BedAllocation, Room, Ward
from app.repositories.base import BaseRepository


class WardRepository(BaseRepository[Ward]):
    """Data access repository for Inpatient Wards, Rooms, and Bed Allocations."""

    def __init__(self, db: Session):
        super().__init__(Ward, db)

    def get_all_wards_with_beds(self) -> List[Ward]:
        """Retrieve all active wards with rooms and bed statuses."""
        return self.db.query(Ward).options(
            joinedload(Ward.rooms).joinedload(Room.beds)
        ).filter(Ward.is_active == True, Ward.is_deleted == False).all()

    def get_available_beds(self) -> List[Bed]:
        """List all hospital beds currently ready for patient admission."""
        return self.db.query(Bed).options(
            joinedload(Bed.room).joinedload(Room.ward)
        ).filter(Bed.status == BedStatus.AVAILABLE).all()

    def get_active_allocation_by_patient(self, patient_id: int) -> Optional[BedAllocation]:
        """Check if patient is currently admitted to an active hospital bed."""
        return self.db.query(BedAllocation).options(
            joinedload(BedAllocation.bed).joinedload(Bed.room).joinedload(Room.ward)
        ).filter(
            BedAllocation.patient_id == patient_id,
            BedAllocation.is_active == True
        ).first()
