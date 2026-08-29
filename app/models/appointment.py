"""
AegisCare Enterprise Patient Management System - Appointment Scheduling Models
Defines patient visits, doctor allocations, visit reasons, and status workflows.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from app.core.constants import AppointmentStatus, AppointmentType
from app.db.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin


class Appointment(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Clinical consultation appointment schedule record."""
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    appointment_number = Column(String(32), unique=True, index=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    
    appointment_type = Column(SQLEnum(AppointmentType), default=AppointmentType.ROUTINE_CHECKUP, nullable=False)
    status = Column(SQLEnum(AppointmentStatus), default=AppointmentStatus.SCHEDULED, nullable=False, index=True)
    
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False)
    
    chief_complaint = Column(Text, nullable=False, doc="Primary patient complaint or reason for consultation")
    symptoms = Column(Text, nullable=True)
    cancellation_reason = Column(String(255), nullable=True)
    
    fee_amount = Column(Numeric(10, 2), default=150.00, nullable=False)
    is_telehealth = Column(String(8), default="NO", nullable=False)
    telehealth_room_id = Column(String(64), nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    department = relationship("Department")
    consultation_note = relationship("ConsultationNote", back_populates="appointment", uselist=False, cascade="all, delete-orphan")


class ConsultationNote(Base, TimestampMixin):
    """Doctor clinical notes, subjective/objective findings, and assessment plan."""
    __tablename__ = "consultation_notes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="CASCADE"), unique=True, nullable=False)
    subjective = Column(Text, nullable=True, doc="Patient described symptoms and timeline")
    objective = Column(Text, nullable=True, doc="Physician physical examination findings")
    assessment = Column(Text, nullable=True, doc="Clinical diagnostic impression")
    plan = Column(Text, nullable=True, doc="Diagnostic, therapeutic, and follow-up plan")
    follow_up_date = Column(DateTime(timezone=True), nullable=True)

    appointment = relationship("Appointment", back_populates="consultation_note")
