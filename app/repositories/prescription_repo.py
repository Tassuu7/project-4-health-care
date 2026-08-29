"""
AegisCare Enterprise Patient Management System - Prescription & Pharmacy Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.core.constants import PrescriptionStatus
from app.models.prescription import Medication, Prescription, PrescriptionItem
from app.repositories.base import BaseRepository


class PrescriptionRepository(BaseRepository[Prescription]):
    """Data access repository for Prescriptions and Medication Inventory."""

    def __init__(self, db: Session):
        super().__init__(Prescription, db)

    def get_with_items(self, prescription_id: int) -> Optional[Prescription]:
        """Fetch prescription with all medication line items and drug metadata."""
        return self.db.query(Prescription).options(
            joinedload(Prescription.items).joinedload(PrescriptionItem.medication),
            joinedload(Prescription.patient),
            joinedload(Prescription.doctor)
        ).filter(
            Prescription.id == prescription_id,
            Prescription.is_deleted == False
        ).first()

    def get_patient_prescriptions(self, patient_id: int) -> List[Prescription]:
        """List all active and past prescriptions for a patient."""
        return self.db.query(Prescription).options(
            joinedload(Prescription.items).joinedload(PrescriptionItem.medication),
            joinedload(Prescription.doctor)
        ).filter(
            Prescription.patient_id == patient_id,
            Prescription.is_deleted == False
        ).order_by(Prescription.issue_date.desc()).all()

    def get_all_medications(self) -> List[Medication]:
        """List full formulary drug catalogue."""
        return self.db.query(Medication).filter(Medication.is_deleted == False).order_by(Medication.brand_name.asc()).all()

    def get_medication_by_id(self, med_id: int) -> Optional[Medication]:
        """Lookup medication by ID."""
        return self.db.query(Medication).filter(Medication.id == med_id, Medication.is_deleted == False).first()
