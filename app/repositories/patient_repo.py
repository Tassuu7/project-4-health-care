"""
AegisCare Enterprise Patient Management System - Patient Repository
"""

from typing import List, Optional, Tuple
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload
from app.models.patient import Allergy, EmergencyContact, InsurancePolicy, Patient
from app.repositories.base import BaseRepository


class PatientRepository(BaseRepository[Patient]):
    """Data access repository for Patient profiles and demographic queries."""

    def __init__(self, db: Session):
        super().__init__(Patient, db)

    def get_by_mrn(self, mrn: str) -> Optional[Patient]:
        """Find patient by Medical Record Number (MRN)."""
        return self.db.query(Patient).filter(
            Patient.mrn == mrn.strip().upper(),
            Patient.is_deleted == False
        ).first()

    def get_with_details(self, patient_id: int) -> Optional[Patient]:
        """Fetch patient with eager-loaded allergies, emergency contacts, and insurance."""
        return self.db.query(Patient).options(
            joinedload(Patient.emergency_contacts),
            joinedload(Patient.allergies),
            joinedload(Patient.insurance_policies)
        ).filter(
            Patient.id == patient_id,
            Patient.is_deleted == False
        ).first()

    def search_patients(self, query_str: str, limit: int = 20) -> List[Patient]:
        """Search patients by name, MRN, phone number, or email."""
        term = f"%{query_str.strip()}%"
        return self.db.query(Patient).filter(
            or_(
                Patient.mrn.ilike(term),
                Patient.first_name.ilike(term),
                Patient.last_name.ilike(term),
                Patient.phone_number.ilike(term),
                Patient.email.ilike(term)
            ),
            Patient.is_deleted == False
        ).limit(limit).all()

    def get_patient_allergies(self, patient_id: int) -> List[Allergy]:
        """List active drug, food, and environmental allergies for a patient."""
        return self.db.query(Allergy).filter(
            Allergy.patient_id == patient_id,
            Allergy.is_active == True
        ).all()
