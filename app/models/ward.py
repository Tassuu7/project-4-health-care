"""
AegisCare Enterprise Patient Management System - Inpatient Wards & Bed Allocation Models
Defines hospital wards, rooms, physical beds, patient admissions, and bed transfers.
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from app.core.constants import BedStatus, WardType
from app.db.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin


class Ward(Base, TimestampMixin, SoftDeleteMixin):
    """Hospital inpatient ward block (e.g. ICU, Surgical Post-Op, Pediatrics)."""
    __tablename__ = "wards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
    ward_type = Column(SQLEnum(WardType), default=WardType.GENERAL_MALE, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    floor_number = Column(Integer, default=1, nullable=False)
    total_capacity = Column(Integer, default=20, nullable=False)
    daily_rate = Column(Numeric(10, 2), default=250.00, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    department = relationship("Department", back_populates="wards")
    rooms = relationship("Room", back_populates="ward", cascade="all, delete-orphan")


class Room(Base, TimestampMixin):
    """Inpatient room within a ward."""
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ward_id = Column(Integer, ForeignKey("wards.id", ondelete="CASCADE"), nullable=False)
    room_number = Column(String(32), nullable=False)
    is_isolation_room = Column(Boolean, default=False, nullable=False)

    ward = relationship("Ward", back_populates="rooms")
    beds = relationship("Bed", back_populates="room", cascade="all, delete-orphan")


class Bed(Base, TimestampMixin):
    """Physical hospital bed unit."""
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    bed_identifier = Column(String(32), unique=True, index=True, nullable=False, doc="e.g. BED-ICU-01")
    status = Column(SQLEnum(BedStatus), default=BedStatus.AVAILABLE, nullable=False, index=True)
    is_ventilator_equipped = Column(Boolean, default=False, nullable=False)
    is_telemetry_monitored = Column(Boolean, default=False, nullable=False)

    room = relationship("Room", back_populates="beds")
    allocations = relationship("BedAllocation", back_populates="bed")


class BedAllocation(Base, TimestampMixin, AuditMixin):
    """Inpatient admission record associating a patient with a specific bed."""
    __tablename__ = "bed_allocations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bed_id = Column(Integer, ForeignKey("beds.id"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    
    admitted_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    discharged_at = Column(DateTime(timezone=True), nullable=True)
    admission_reason = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    bed = relationship("Bed", back_populates="allocations")
    patient = relationship("Patient", back_populates="bed_allocations")
    transfers = relationship("WardTransferLog", back_populates="allocation")


class WardTransferLog(Base, TimestampMixin, AuditMixin):
    """Audit trail of patient bed transfers across hospital wards."""
    __tablename__ = "ward_transfer_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    allocation_id = Column(Integer, ForeignKey("bed_allocations.id"), nullable=False)
    from_bed_id = Column(Integer, ForeignKey("beds.id"), nullable=False)
    to_bed_id = Column(Integer, ForeignKey("beds.id"), nullable=False)
    transfer_reason = Column(String(255), nullable=False)
    transferred_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    allocation = relationship("BedAllocation", back_populates="transfers")
