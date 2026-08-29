"""
AegisCare Enterprise Patient Management System - Patient Service
"""

import random
from datetime import datetime, timezone
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.core.constants import AuditAction
from app.core.exceptions import ResourceNotFoundError
from app.models.patient import Allergy, EmergencyContact, InsurancePolicy, Patient
from app.repositories.audit_repo import AuditRepository
from app.repositories.patient_repo import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    """Business workflows for patient demographics, allergy registries, and MRN issuance."""

    def __init__(self, db: Session):
        self.db = db
        self.patient_repo = PatientRepository(db)
        self.audit_repo = AuditRepository(db)

    def generate_mrn(self) -> str:
        """Generate unique Medical Record Number (MRN)."""
        year = datetime.now(timezone.utc).year
        random_suffix = random.randint(10000, 99999)
        return f"MRN-{year}-{random_suffix}"

    def register_patient(self, patient_in: PatientCreate, actor_user_id: Optional[int] = None) -> Patient:
        """Register a new patient profile and allocate MRN."""
        mrn = self.generate_mrn()
        while self.patient_repo.get_by_mrn(mrn):
            mrn = self.generate_mrn()

        patient_data = patient_in.model_dump(exclude={"emergency_contacts", "allergies"})
        patient_data["mrn"] = mrn
        
        patient = self.patient_repo.create(patient_data)

        # Save emergency contacts
        if patient_in.emergency_contacts:
            for ec in patient_in.emergency_contacts:
                contact = EmergencyContact(patient_id=patient.id, **ec.model_dump())
                self.db.add(contact)

        # Save allergies
        if patient_in.allergies:
            for al in patient_in.allergies:
                allergy = Allergy(patient_id=patient.id, **al.model_dump())
                self.db.add(allergy)

        self.db.commit()
        self.db.refresh(patient)

        self.audit_repo.log_event(
            action=AuditAction.PATIENT_CREATE,
            resource_type="PATIENT",
            resource_id=str(patient.id),
            user_id=actor_user_id,
            details=f"Registered new patient {patient.full_name} ({patient.mrn})"
        )
        return patient

    def get_patient(self, patient_id: int) -> Patient:
        """Retrieve patient details or raise 404."""
        patient = self.patient_repo.get_with_details(patient_id)
        if not patient:
            raise ResourceNotFoundError("Patient", patient_id)
        return patient

    def update_patient(self, patient_id: int, update_data: PatientUpdate, actor_user_id: Optional[int] = None) -> Patient:
        """Update demographic attributes of an existing patient profile."""
        patient = self.get_patient(patient_id)
        updated = self.patient_repo.update(patient, update_data.model_dump(exclude_unset=True))
        
        self.audit_repo.log_event(
            action=AuditAction.PATIENT_UPDATE,
            resource_type="PATIENT",
            resource_id=str(patient_id),
            user_id=actor_user_id,
            details=f"Updated profile for patient {patient.full_name}"
        )
        return updated
