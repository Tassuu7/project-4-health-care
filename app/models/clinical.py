"""
AegisCare Enterprise Patient Management System - Clinical & Medical Record Models
Defines medical records, vital signs timeseries, diagnoses (ICD-10), and treatment plans.
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin


class MedicalRecord(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Comprehensive clinical encounter record summarizing a patient hospital event."""
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    record_number = Column(String(32), unique=True, index=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    
    encounter_type = Column(String(32), default="OUTPATIENT", nullable=False)
    admission_date = Column(DateTime(timezone=True), nullable=False)
    discharge_date = Column(DateTime(timezone=True), nullable=True)
    
    primary_diagnosis = Column(String(255), nullable=False)
    icd10_code = Column(String(16), nullable=False, index=True)
    clinical_summary = Column(Text, nullable=False)
    discharge_summary = Column(Text, nullable=True)
    is_confidential = Column(Boolean, default=False, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="medical_records")
    doctor = relationship("Doctor")
    diagnoses = relationship("Diagnosis", back_populates="medical_record", cascade="all, delete-orphan")
    clinical_notes = relationship("ClinicalNote", back_populates="medical_record", cascade="all, delete-orphan")
    treatment_plans = relationship("TreatmentPlan", back_populates="medical_record", cascade="all, delete-orphan")


class VitalSign(Base, TimestampMixin, AuditMixin):
    """Time-series physiological measurements (Blood Pressure, Heart Rate, SpO2, Temp)."""
    __tablename__ = "vital_signs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    recorded_at = Column(DateTime(timezone=True), nullable=False, index=True)
    
    systolic_bp = Column(Integer, nullable=True, doc="Systolic Blood Pressure (mmHg)")
    diastolic_bp = Column(Integer, nullable=True, doc="Diastolic Blood Pressure (mmHg)")
    heart_rate = Column(Integer, nullable=True, doc="Heart Rate / Pulse (BPM)")
    respiratory_rate = Column(Integer, nullable=True, doc="Respiratory Rate (Breaths/min)")
    temperature_celsius = Column(Float, nullable=True, doc="Body Temp in Celsius")
    oxygen_saturation = Column(Float, nullable=True, doc="SpO2 percentage (e.g. 98.5)")
    blood_glucose_mg_dl = Column(Float, nullable=True, doc="Blood Glucose level (mg/dL)")
    pain_score = Column(Integer, default=0, nullable=False, doc="0-10 Wong-Baker scale")
    
    is_abnormal = Column(Boolean, default=False, nullable=False)
    alert_notes = Column(String(255), nullable=True)

    patient = relationship("Patient", back_populates="vitals")


class Diagnosis(Base, TimestampMixin):
    """Formal diagnosis with ICD-10 codification and status."""
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    medical_record_id = Column(Integer, ForeignKey("medical_records.id", ondelete="CASCADE"), nullable=False)
    icd10_code = Column(String(16), nullable=False, index=True)
    description = Column(String(255), nullable=False)
    diagnosis_type = Column(String(32), default="PRIMARY", nullable=False, doc="PRIMARY, SECONDARY, DIFFERENTIAL")
    is_chronic = Column(Boolean, default=False, nullable=False)

    medical_record = relationship("MedicalRecord", back_populates="diagnoses")


class ClinicalNote(Base, TimestampMixin, AuditMixin):
    """Physician or nurse progress notes, shift handovers, and observation entries."""
    __tablename__ = "clinical_notes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    medical_record_id = Column(Integer, ForeignKey("medical_records.id", ondelete="CASCADE"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    author_role = Column(String(32), default="DOCTOR", nullable=False)
    note_type = Column(String(32), default="PROGRESS_NOTE", nullable=False)
    content = Column(Text, nullable=False)

    medical_record = relationship("MedicalRecord", back_populates="clinical_notes")
    doctor = relationship("Doctor", back_populates="clinical_notes")


class TreatmentPlan(Base, TimestampMixin):
    """Structured clinical treatment goals, interventions, and planned procedures."""
    __tablename__ = "treatment_plans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    medical_record_id = Column(Integer, ForeignKey("medical_records.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(128), nullable=False)
    goals = Column(Text, nullable=False)
    interventions = Column(Text, nullable=False)
    status = Column(String(32), default="IN_PROGRESS", nullable=False)

    medical_record = relationship("MedicalRecord", back_populates="treatment_plans")


class Immunization(Base, TimestampMixin):
    """Vaccination and immunization tracking records."""
    __tablename__ = "immunizations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    vaccine_name = Column(String(128), nullable=False)
    dose_number = Column(Integer, default=1, nullable=False)
    administered_date = Column(DateTime(timezone=True), nullable=False)
    manufacturer = Column(String(64), nullable=True)
    lot_number = Column(String(32), nullable=True)
    administering_nurse = Column(String(128), nullable=True)
