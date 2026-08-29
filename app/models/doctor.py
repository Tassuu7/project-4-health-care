"""
AegisCare Enterprise Patient Management System - Physician & Specialty Models
Defines medical practitioners, credentials, department links, and scheduling slots.
"""

from datetime import time
from sqlalchemy import Boolean, Column, Date, Enum as SQLEnum, ForeignKey, Integer, Numeric, String, Text, Time
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin, SoftDeleteMixin


class Specialization(Base, TimestampMixin):
    """Medical specialty classification (e.g. Cardiology, Neurology, Orthopedics)."""
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
    code = Column(String(16), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    doctors = relationship("Doctor", back_populates="specialization")


class Doctor(Base, TimestampMixin, SoftDeleteMixin):
    """Physician entity containing license number, department, fee, and consultations."""
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False, index=True)
    specialization_id = Column(Integer, ForeignKey("specializations.id"), nullable=False, index=True)
    
    medical_license_number = Column(String(64), unique=True, nullable=False, doc="State medical board license ID")
    qualification = Column(String(128), nullable=False, doc="Degrees (e.g. MD, MBBS, FACS)")
    years_of_experience = Column(Integer, default=0, nullable=False)
    consultation_fee = Column(Numeric(10, 2), default=150.00, nullable=False)
    bio = Column(Text, nullable=True)
    is_available_for_telehealth = Column(Boolean, default=True, nullable=False)
    is_on_call = Column(Boolean, default=False, nullable=False)
    max_daily_patients = Column(Integer, default=30, nullable=False)

    # Relationships
    user = relationship("User", back_populates="doctor_profile")
    department = relationship("Department", back_populates="doctors")
    specialization = relationship("Specialization", back_populates="doctors")
    schedules = relationship("DoctorSchedule", back_populates="doctor", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="doctor")
    prescriptions = relationship("Prescription", back_populates="doctor")
    clinical_notes = relationship("ClinicalNote", back_populates="doctor")

    @property
    def full_name(self) -> str:
        return f"Dr. {self.user.full_name}" if self.user else "Dr. Unknown"


class DoctorSchedule(Base, TimestampMixin):
    """Weekly recurring or date-specific doctor shift and consultation availability hours."""
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False, doc="0=Monday, 6=Sunday")
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    slot_duration_minutes = Column(Integer, default=30, nullable=False)
    max_patients_per_slot = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    doctor = relationship("Doctor", back_populates="schedules")
