"""
AegisCare Enterprise Patient Management System - Appointment Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.core.constants import AppointmentStatus, AppointmentType


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    department_id: int
    appointment_type: AppointmentType = AppointmentType.ROUTINE_CHECKUP
    start_time: datetime
    end_time: datetime
    chief_complaint: str = Field(..., min_length=3)
    symptoms: Optional[str] = None
    fee_amount: float = 150.00
    is_telehealth: str = "NO"


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    status: Optional[AppointmentStatus] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    symptoms: Optional[str] = None
    cancellation_reason: Optional[str] = None


class AppointmentResponse(AppointmentBase):
    id: int
    appointment_number: str
    status: AppointmentStatus
    cancellation_reason: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
