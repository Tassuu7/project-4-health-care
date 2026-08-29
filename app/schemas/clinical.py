"""
AegisCare Enterprise Patient Management System - Clinical & Vitals Schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class VitalSignBase(BaseModel):
    patient_id: int
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    temperature_celsius: Optional[float] = None
    oxygen_saturation: Optional[float] = None
    blood_glucose_mg_dl: Optional[float] = None
    pain_score: int = Field(default=0, ge=0, le=10)


class VitalSignCreate(VitalSignBase):
    pass


class VitalSignResponse(VitalSignBase):
    id: int
    is_abnormal: bool
    alert_notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    encounter_type: str = "OUTPATIENT"
    admission_date: datetime = Field(default_factory=datetime.utcnow)
    discharge_date: Optional[datetime] = None
    primary_diagnosis: str
    icd10_code: str
    clinical_summary: str
    discharge_summary: Optional[str] = None


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordResponse(MedicalRecordBase):
    id: int
    record_number: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
