"""
AegisCare Enterprise Patient Management System - Doctor Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.doctor import Doctor, DoctorSchedule, Specialization
from app.repositories.base import BaseRepository


class DoctorRepository(BaseRepository[Doctor]):
    """Data access repository for Physicians, Specialties, and Shift Schedules."""

    def __init__(self, db: Session):
        super().__init__(Doctor, db)

    def get_with_user(self, doctor_id: int) -> Optional[Doctor]:
        """Fetch doctor with joined user credentials and department information."""
        return self.db.query(Doctor).options(
            joinedload(Doctor.user),
            joinedload(Doctor.department),
            joinedload(Doctor.specialization),
            joinedload(Doctor.schedules)
        ).filter(
            Doctor.id == doctor_id,
            Doctor.is_deleted == False
        ).first()

    def list_by_department(self, department_id: int) -> List[Doctor]:
        """List all active physicians assigned to a department."""
        return self.db.query(Doctor).options(
            joinedload(Doctor.user),
            joinedload(Doctor.specialization)
        ).filter(
            Doctor.department_id == department_id,
            Doctor.is_deleted == False
        ).all()

    def get_available_doctors(self) -> List[Doctor]:
        """List all active doctors open for consultations."""
        return self.db.query(Doctor).options(
            joinedload(Doctor.user),
            joinedload(Doctor.department),
            joinedload(Doctor.specialization)
        ).filter(Doctor.is_deleted == False).all()
