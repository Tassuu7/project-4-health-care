"""
AegisCare Enterprise Patient Management System - Triage Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.core.constants import TriageLevel


class TriageInput(BaseModel):
    patient_id: int
    chief_complaint: str = Field(..., min_length=3)
    pain_score: int = Field(default=0, ge=0, le=10)
    heart_rate: Optional[int] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    respiratory_rate: Optional[int] = None
    oxygen_saturation: Optional[float] = None
    temperature_celsius: Optional[float] = None
    is_resuscitation_required: bool = False
    is_high_risk_situation: bool = False
    estimated_resource_count: int = 1
    triage_notes: Optional[str] = None


class TriageAssessmentResponse(TriageInput):
    id: int
    triage_number: str
    triage_level: TriageLevel
    assigned_zone: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
