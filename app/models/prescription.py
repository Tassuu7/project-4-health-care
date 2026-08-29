"""
AegisCare Enterprise Patient Management System - Pharmacy & E-Prescription Models
Defines prescription orders, medication catalogue, dosage rules, and pharmacy dispensing logs.
"""

from datetime import date, datetime
from sqlalchemy import Boolean, Column, Date, DateTime, Enum as SQLEnum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from app.core.constants import PrescriptionStatus
from app.db.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin


class Medication(Base, TimestampMixin, SoftDeleteMixin):
    """Drug catalogue item with dosage forms, strength, and inventory balance."""
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    drug_code = Column(String(32), unique=True, index=True, nullable=False, doc="NDC or generic drug code")
    brand_name = Column(String(128), nullable=False, index=True)
    generic_name = Column(String(128), nullable=False, index=True)
    dosage_form = Column(String(32), default="TABLET", nullable=False, doc="TABLET, CAPSULE, SYRUP, INJECTION, IV")
    strength = Column(String(32), nullable=False, doc="e.g. 500mg, 10mg/ml")
    unit_price = Column(Numeric(10, 2), default=10.00, nullable=False)
    current_stock_quantity = Column(Integer, default=500, nullable=False)
    reorder_threshold = Column(Integer, default=50, nullable=False)
    requires_prescription = Column(Boolean, default=True, nullable=False)
    is_controlled_substance = Column(Boolean, default=False, nullable=False)
    storage_conditions = Column(String(128), default="Store at room temperature", nullable=True)

    prescription_items = relationship("PrescriptionItem", back_populates="medication")


class Prescription(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Doctor authorized prescription order containing prescribed medications."""
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prescription_number = Column(String(32), unique=True, index=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    
    status = Column(SQLEnum(PrescriptionStatus), default=PrescriptionStatus.ACTIVE, nullable=False, index=True)
    issue_date = Column(Date, default=date.today, nullable=False)
    expiry_date = Column(Date, nullable=False)
    diagnosis_reason = Column(String(255), nullable=True)
    doctor_instructions = Column(Text, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")
    items = relationship("PrescriptionItem", back_populates="prescription", cascade="all, delete-orphan")
    dispense_logs = relationship("MedicationDispenseLog", back_populates="prescription")


class PrescriptionItem(Base, TimestampMixin):
    """Individual line item representing a specific medication in a prescription."""
    __tablename__ = "prescription_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False)
    medication_id = Column(Integer, ForeignKey("medications.id"), nullable=False)
    
    dosage_instruction = Column(String(128), nullable=False, doc="e.g. 1 tablet twice daily after food")
    frequency = Column(String(32), default="BID", nullable=False, doc="QD, BID, TID, QID, PRN")
    duration_days = Column(Integer, default=7, nullable=False)
    quantity_prescribed = Column(Integer, default=14, nullable=False)
    quantity_dispensed = Column(Integer, default=0, nullable=False)
    refills_allowed = Column(Integer, default=0, nullable=False)
    special_warnings = Column(String(255), nullable=True)

    prescription = relationship("Prescription", back_populates="items")
    medication = relationship("Medication", back_populates="prescription_items")


class DosageSchedule(Base, TimestampMixin):
    """Automated medication intake reminder schedule."""
    __tablename__ = "dosage_schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prescription_item_id = Column(Integer, ForeignKey("prescription_items.id", ondelete="CASCADE"), nullable=False)
    scheduled_time = Column(String(16), nullable=False, doc="e.g. 08:00 AM")
    is_taken = Column(Boolean, default=False, nullable=False)
    taken_at = Column(DateTime(timezone=True), nullable=True)


class MedicationDispenseLog(Base, TimestampMixin, AuditMixin):
    """Pharmacy audit record for fulfilled medication dispensations."""
    __tablename__ = "medication_dispense_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"), nullable=False)
    pharmacist_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dispensed_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    quantity_dispensed = Column(Integer, nullable=False)
    notes = Column(String(255), nullable=True)

    prescription = relationship("Prescription", back_populates="dispense_logs")
    pharmacist = relationship("User")
