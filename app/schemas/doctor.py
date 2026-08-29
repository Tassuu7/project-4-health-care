"""
AegisCare Enterprise Patient Management System - Doctor Schemas
"""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserResponse


class DoctorScheduleSchema(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str
    slot_duration_minutes: int = 30
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class DoctorBase(BaseModel):
    department_id: int
    specialization_id: int
    medical_license_number: str
    qualification: str
    years_of_experience: int = 0
    consultation_fee: float = 150.00
    bio: Optional[str] = None
    is_available_for_telehealth: bool = True
    max_daily_patients: int = 30


class DoctorCreate(DoctorBase):
    user_id: int


class DoctorUpdate(BaseModel):
    department_id: Optional[int] = None
    specialization_id: Optional[int] = None
    qualification: Optional[str] = None
    years_of_experience: Optional[int] = None
    consultation_fee: Optional[float] = None
    bio: Optional[str] = None
    is_available_for_telehealth: Optional[bool] = None
    is_on_call: Optional[bool] = None


class DoctorResponse(DoctorBase):
    id: int
    user: UserResponse
    is_on_call: bool
    schedules: List[DoctorScheduleSchema] = []

    model_config = ConfigDict(from_attributes=True)
