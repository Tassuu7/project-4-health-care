"""
AegisCare Enterprise Patient Management System - Laboratory & Diagnostics Models
Defines diagnostic test catalogue, orders, specimen tracking, and validated lab results.
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from app.core.constants import LabOrderStatus, LabResultFlag
from app.db.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin


class LabTestCatalog(Base, TimestampMixin, SoftDeleteMixin):
    """Catalog of available laboratory diagnostic tests, normal reference ranges, and fees."""
    __tablename__ = "lab_test_catalogs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    test_code = Column(String(32), unique=True, index=True, nullable=False, doc="LOINC or hospital test code")
    name = Column(String(128), nullable=False)
    category = Column(String(64), default="BIOCHEMISTRY", nullable=False, doc="HEMATOLOGY, BIOCHEMISTRY, MICROBIOLOGY, IMMUNOLOGY")
    sample_type_required = Column(String(64), default="SERUM", nullable=False)
    standard_unit = Column(String(32), nullable=False, doc="e.g. mg/dL, mmol/L, g/dL, %")
    
    reference_range_low = Column(Float, nullable=True)
    reference_range_high = Column(Float, nullable=True)
    critical_low = Column(Float, nullable=True)
    critical_high = Column(Float, nullable=True)
    
    standard_fee = Column(Numeric(10, 2), default=45.00, nullable=False)
    turnaround_hours = Column(Integer, default=4, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class LabOrder(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Physician test requisition order."""
    __tablename__ = "lab_orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_number = Column(String(32), unique=True, index=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    
    status = Column(SQLEnum(LabOrderStatus), default=LabOrderStatus.ORDERED, nullable=False, index=True)
    priority = Column(String(16), default="ROUTINE", nullable=False, doc="ROUTINE, URGENT, STAT")
    clinical_notes = Column(Text, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="lab_orders")
    doctor = relationship("Doctor")
    results = relationship("LabResult", back_populates="order", cascade="all, delete-orphan")
    specimens = relationship("SpecimenSample", back_populates="order", cascade="all, delete-orphan")


class SpecimenSample(Base, TimestampMixin, AuditMixin):
    """Physical biological sample collected from patient."""
    __tablename__ = "specimen_samples"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lab_order_id = Column(Integer, ForeignKey("lab_orders.id", ondelete="CASCADE"), nullable=False)
    barcode_identifier = Column(String(64), unique=True, index=True, nullable=False)
    specimen_type = Column(String(64), nullable=False)
    collected_at = Column(DateTime(timezone=True), nullable=True)
    collector_staff_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_received_in_lab = Column(Boolean, default=False, nullable=False)

    order = relationship("LabOrder", back_populates="specimens")


class LabResult(Base, TimestampMixin, AuditMixin):
    """Measured quantitative or qualitative diagnostic result."""
    __tablename__ = "lab_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lab_order_id = Column(Integer, ForeignKey("lab_orders.id", ondelete="CASCADE"), nullable=False)
    test_id = Column(Integer, ForeignKey("lab_test_catalogs.id"), nullable=False)
    
    measured_value = Column(String(64), nullable=False, doc="Numeric value or positive/negative string")
    numeric_value = Column(Float, nullable=True)
    flag = Column(SQLEnum(LabResultFlag), default=LabResultFlag.NORMAL, nullable=False)
    
    technician_notes = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    verified_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)

    order = relationship("LabOrder", back_populates="results")
    test = relationship("LabTestCatalog")


class DiagnosticReport(Base, TimestampMixin):
    """Compiled clinical pathologist diagnostic report."""
    __tablename__ = "diagnostic_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_number = Column(String(32), unique=True, index=True, nullable=False)
    lab_order_id = Column(Integer, ForeignKey("lab_orders.id", ondelete="CASCADE"), nullable=False)
    summary_impression = Column(Text, nullable=False)
    pathologist_signature = Column(String(128), nullable=False)
    is_finalized = Column(Boolean, default=False, nullable=False)
