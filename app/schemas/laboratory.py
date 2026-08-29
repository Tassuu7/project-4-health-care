"""
AegisCare Enterprise Patient Management System - Laboratory Schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.core.constants import LabOrderStatus, LabResultFlag


class LabOrderCreate(BaseModel):
    patient_id: int
    doctor_id: int
    test_ids: List[int]
    priority: str = "ROUTINE"
    clinical_notes: Optional[str] = None


class LabResultCreate(BaseModel):
    lab_order_id: int
    test_id: int
    measured_value: str
    numeric_value: Optional[float] = None
    technician_notes: Optional[str] = None


class LabResultResponse(BaseModel):
    id: int
    lab_order_id: int
    test_id: int
    measured_value: str
    numeric_value: Optional[float] = None
    flag: LabResultFlag
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class LabOrderResponse(BaseModel):
    id: int
    order_number: str
    patient_id: int
    doctor_id: int
    status: LabOrderStatus
    priority: str
    results: List[LabResultResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
