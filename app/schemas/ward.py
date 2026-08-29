"""
AegisCare Enterprise Patient Management System - Ward & Bed Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.core.constants import BedStatus, WardType


class WardCreate(BaseModel):
    name: str
    ward_type: WardType = WardType.GENERAL_MALE
    department_id: int
    floor_number: int = 1
    total_capacity: int = 20
    daily_rate: float = 250.00


class WardResponse(WardCreate):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class BedAllocationCreate(BaseModel):
    bed_id: int
    patient_id: int
    admission_reason: str


class BedAllocationResponse(BaseModel):
    id: int
    bed_id: int
    patient_id: int
    admitted_at: datetime
    discharged_at: Optional[datetime] = None
    admission_reason: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
