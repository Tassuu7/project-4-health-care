"""
AegisCare Enterprise Patient Management System - Prescription Schemas
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.core.constants import PrescriptionStatus


class MedicationBase(BaseModel):
    drug_code: str
    brand_name: str
    generic_name: str
    dosage_form: str = "TABLET"
    strength: str
    unit_price: float = 10.00
    current_stock_quantity: int = 500
    requires_prescription: bool = True
    is_controlled_substance: bool = False


class MedicationCreate(MedicationBase):
    pass


class MedicationResponse(MedicationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PrescriptionItemSchema(BaseModel):
    medication_id: int
    dosage_instruction: str
    frequency: str = "BID"
    duration_days: int = 7
    quantity_prescribed: int = 14
    special_warnings: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    expiry_date: date
    diagnosis_reason: Optional[str] = None
    doctor_instructions: Optional[str] = None
    items: List[PrescriptionItemSchema]


class PrescriptionResponse(BaseModel):
    id: int
    prescription_number: str
    patient_id: int
    doctor_id: int
    status: PrescriptionStatus
    issue_date: date
    expiry_date: date
    items: List[PrescriptionItemSchema] = []

    model_config = ConfigDict(from_attributes=True)
