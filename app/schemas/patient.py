"""
AegisCare Enterprise Patient Management System - Patient Validation Schemas
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.core.constants import BloodGroup, Gender


class EmergencyContactSchema(BaseModel):
    name: str = Field(..., min_length=2)
    relationship_to_patient: str
    phone_number: str
    email: Optional[EmailStr] = None
    is_primary: bool = True

    model_config = ConfigDict(from_attributes=True)


class AllergySchema(BaseModel):
    allergen: str
    allergy_type: str = "DRUG"
    severity: str = "MODERATE"
    reaction_description: Optional[str] = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=64)
    last_name: str = Field(..., min_length=1, max_length=64)
    date_of_birth: date
    gender: Gender = Gender.UNKNOWN
    blood_group: BloodGroup = BloodGroup.UNKNOWN
    national_id: Optional[str] = None
    phone_number: str = Field(..., min_length=7)
    email: Optional[EmailStr] = None
    address_street: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_postal_code: Optional[str] = None
    address_country: str = "United States"
    marital_status: str = "SINGLE"
    occupation: Optional[str] = None
    is_vip: bool = False
    risk_notes: Optional[str] = None


class PatientCreate(PatientBase):
    emergency_contacts: Optional[List[EmergencyContactSchema]] = None
    allergies: Optional[List[AllergySchema]] = None


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address_street: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_postal_code: Optional[str] = None
    marital_status: Optional[str] = None
    occupation: Optional[str] = None
    is_vip: Optional[bool] = None
    risk_notes: Optional[str] = None


class PatientResponse(PatientBase):
    id: int
    mrn: str
    age: int
    created_at: datetime
    emergency_contacts: List[EmergencyContactSchema] = []
    allergies: List[AllergySchema] = []

    model_config = ConfigDict(from_attributes=True)


class PatientSummary(BaseModel):
    id: int
    mrn: str
    full_name: str
    age: int
    gender: Gender
    blood_group: BloodGroup
    phone_number: str

    model_config = ConfigDict(from_attributes=True)
