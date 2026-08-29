"""
AegisCare Enterprise Patient Management System - Clinical & Medical Record Service
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.constants import AuditAction
from app.models.clinical import MedicalRecord, VitalSign
from app.repositories.audit_repo import AuditRepository
from app.repositories.clinical_repo import ClinicalRepository
from app.schemas.clinical import MedicalRecordCreate, VitalSignCreate


class ClinicalService:
    """Business workflows for clinical consultations, vital signs recording, and EHR."""

    def __init__(self, db: Session):
        self.db = db
        self.clinical_repo = ClinicalRepository(db)
        self.audit_repo = AuditRepository(db)

    def record_vitals(self, vitals_in: VitalSignCreate, actor_user_id: Optional[int] = None) -> VitalSign:
        """Record patient vital signs and evaluate abnormal thresholds."""
        is_abnormal = False
        alerts = []
        
        if vitals_in.heart_rate and (vitals_in.heart_rate > 100 or vitals_in.heart_rate < 60):
            is_abnormal = True
            alerts.append("Tachycardia/Bradycardia")
        if vitals_in.systolic_bp and (vitals_in.systolic_bp > 140 or vitals_in.systolic_bp < 90):
            is_abnormal = True
            alerts.append("Abnormal BP")
        if vitals_in.oxygen_saturation and vitals_in.oxygen_saturation < 95.0:
            is_abnormal = True
            alerts.append("Hypoxemia (Low SpO2)")
            
        vital = VitalSign(
            patient_id=vitals_in.patient_id,
            systolic_bp=vitals_in.systolic_bp,
            diastolic_bp=vitals_in.diastolic_bp,
            heart_rate=vitals_in.heart_rate,
            respiratory_rate=vitals_in.respiratory_rate,
            temperature_celsius=vitals_in.temperature_celsius,
            oxygen_saturation=vitals_in.oxygen_saturation,
            blood_glucose_mg_dl=vitals_in.blood_glucose_mg_dl,
            pain_score=vitals_in.pain_score,
            is_abnormal=is_abnormal,
            alert_notes=", ".join(alerts) if alerts else None
        )
        saved = self.clinical_repo.record_vital_signs(vital)
        return saved

    def create_medical_record(self, record_in: MedicalRecordCreate, actor_user_id: Optional[int] = None) -> MedicalRecord:
        """Create and persist a formal medical record encounter."""
        record_number = f"REC-{record_in.patient_id}-{int(datetime.now().timestamp())}"
        data = record_in.model_dump()
        data["record_number"] = record_number
        record = self.clinical_repo.create(data)
        
        self.audit_repo.log_event(
            action=AuditAction.MEDICAL_RECORD_CREATE,
            resource_type="MEDICAL_RECORD",
            resource_id=str(record.id),
            user_id=actor_user_id,
            details=f"Created clinical record {record.record_number} with ICD-10 {record.icd10_code}"
        )
        return record
