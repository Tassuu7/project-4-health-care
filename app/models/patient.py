"""
AegisCare Enterprise Patient Management System - Patient Demographics & Health Profile
Defines core patient entity, emergency contacts, insurance policies, allergies, and history.
"""

from datetime import date
from sqlalchemy import Boolean, Column, Date, Enum as SQLEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.constants import BloodGroup, Gender
from app.db.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin


class Patient(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Patient primary record containing Medical Record Number (MRN) and demographics."""
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)
    mrn = Column(String(32), unique=True, index=True, nullable=False, doc="Medical Record Number (e.g. MRN-2026-0001)")
    
    first_name = Column(String(64), nullable=False, index=True)
    last_name = Column(String(64), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(SQLEnum(Gender), default=Gender.UNKNOWN, nullable=False)
    blood_group = Column(SQLEnum(BloodGroup), default=BloodGroup.UNKNOWN, nullable=False)
    
    national_id = Column(String(32), nullable=True, doc="Government identification or SSN")
    phone_number = Column(String(32), nullable=False, index=True)
    email = Column(String(128), nullable=True)
    
    address_street = Column(String(128), nullable=True)
    address_city = Column(String(64), nullable=True)
    address_state = Column(String(64), nullable=True)
    address_postal_code = Column(String(16), nullable=True)
    address_country = Column(String(64), default="United States", nullable=False)
    
    marital_status = Column(String(32), default="SINGLE", nullable=False)
    occupation = Column(String(64), nullable=True)
    primary_language = Column(String(32), default="English", nullable=False)
    is_vip = Column(Boolean, default=False, nullable=False)
    risk_notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="patient_profile")
    emergency_contacts = relationship("EmergencyContact", back_populates="patient", cascade="all, delete-orphan")
    insurance_policies = relationship("InsurancePolicy", back_populates="patient", cascade="all, delete-orphan")
    allergies = relationship("Allergy", back_populates="patient", cascade="all, delete-orphan")
    medical_histories = relationship("MedicalHistory", back_populates="patient", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="patient")
    medical_records = relationship("MedicalRecord", back_populates="patient")
    vitals = relationship("VitalSign", back_populates="patient")
    triage_assessments = relationship("TriageAssessment", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")
    lab_orders = relationship("LabOrder", back_populates="patient")
    invoices = relationship("Invoice", back_populates="patient")
    bed_allocations = relationship("BedAllocation", back_populates="patient")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        today = date.today()
        if self.date_of_birth:
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return 0


class EmergencyContact(Base, TimestampMixin):
    """Emergency next-of-kin or guardian contact records."""
    __tablename__ = "emergency_contacts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    relationship_to_patient = Column(String(64), nullable=False)
    phone_number = Column(String(32), nullable=False)
    alt_phone_number = Column(String(32), nullable=True)
    email = Column(String(128), nullable=True)
    is_primary = Column(Boolean, default=True, nullable=False)

    patient = relationship("Patient", back_populates="emergency_contacts")


class InsurancePolicy(Base, TimestampMixin):
    """Patient medical insurance coverage policy."""
    __tablename__ = "insurance_policies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    provider_name = Column(String(128), nullable=False)
    policy_number = Column(String(64), nullable=False, index=True)
    group_number = Column(String(64), nullable=True)
    subscriber_name = Column(String(128), nullable=False)
    relationship_to_subscriber = Column(String(32), default="SELF", nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_thru = Column(Date, nullable=False)
    copay_percentage = Column(Integer, default=20, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    patient = relationship("Patient", back_populates="insurance_policies")


class Allergy(Base, TimestampMixin):
    """Patient allergy registry (e.g. Penicillin, Peanuts, Latex) with severity ratings."""
    __tablename__ = "allergies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    allergen = Column(String(128), nullable=False, index=True)
    allergy_type = Column(String(32), default="DRUG", nullable=False, doc="DRUG, FOOD, ENVIRONMENTAL")
    severity = Column(String(32), default="MODERATE", nullable=False, doc="MILD, MODERATE, SEVERE, LIFE_THREATENING")
    reaction_description = Column(Text, nullable=True)
    diagnosed_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    patient = relationship("Patient", back_populates="allergies")


class MedicalHistory(Base, TimestampMixin):
    """Past chronic conditions, surgical operations, or familial disorders."""
    __tablename__ = "medical_histories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    condition_name = Column(String(128), nullable=False)
    icd10_code = Column(String(16), nullable=True)
    diagnosed_date = Column(Date, nullable=True)
    status = Column(String(32), default="CHRONIC", nullable=False, doc="CHRONIC, RESOLVED, IN_TREATMENT")
    notes = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="medical_histories")
