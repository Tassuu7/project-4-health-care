"""
AegisCare Enterprise Patient Management System - Clinical & Medical Record Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.clinical import ClinicalNote, Diagnosis, MedicalRecord, VitalSign
from app.repositories.base import BaseRepository


class ClinicalRepository(BaseRepository[MedicalRecord]):
    """Data access repository for Electronic Health Records (EHR) and Vital Signs."""

    def __init__(self, db: Session):
        super().__init__(MedicalRecord, db)

    def get_patient_records(self, patient_id: int) -> List[MedicalRecord]:
        """List all clinical encounter records for a patient."""
        return self.db.query(MedicalRecord).options(
            joinedload(MedicalRecord.diagnoses),
            joinedload(MedicalRecord.clinical_notes),
            joinedload(MedicalRecord.treatment_plans)
        ).filter(
            MedicalRecord.patient_id == patient_id,
            MedicalRecord.is_deleted == False
        ).order_by(MedicalRecord.admission_date.desc()).all()

    def get_patient_vitals_history(self, patient_id: int, limit: int = 50) -> List[VitalSign]:
        """Retrieve chronological physiological vitals timeseries for a patient."""
        return self.db.query(VitalSign).filter(
            VitalSign.patient_id == patient_id
        ).order_by(VitalSign.recorded_at.desc()).limit(limit).all()

    def record_vital_signs(self, vital_sign: VitalSign) -> VitalSign:
        """Persist a new vital sign measurement entry."""
        self.db.add(vital_sign)
        self.db.commit()
        self.db.refresh(vital_sign)
        return vital_sign
