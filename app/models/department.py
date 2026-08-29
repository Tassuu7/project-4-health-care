"""
AegisCare Enterprise Patient Management System - Department & Facility Models
Defines hospital operational departments, clinical units, and consultation rooms.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin, SoftDeleteMixin


class Department(Base, TimestampMixin, SoftDeleteMixin):
    """Hospital clinical department (e.g. Cardiology, Pediatrics, Emergency, Oncology)."""
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(16), unique=True, index=True, nullable=False, doc="Department code (e.g., CARD-01)")
    name = Column(String(128), unique=True, nullable=False, doc="Department name")
    description = Column(Text, nullable=True)
    head_of_department_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    location_building = Column(String(64), nullable=True)
    location_floor = Column(String(16), nullable=True)
    phone_extension = Column(String(16), nullable=True)
    emergency_capable = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    doctors = relationship("Doctor", back_populates="department")
    rooms = relationship("ClinicRoom", back_populates="department", cascade="all, delete-orphan")
    wards = relationship("Ward", back_populates="department")


class ClinicRoom(Base, TimestampMixin):
    """Physical consultation room or examination station within a department."""
    __tablename__ = "clinic_rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    room_number = Column(String(32), nullable=False, index=True)
    room_type = Column(String(32), default="CONSULTATION", nullable=False)
    is_operational = Column(Boolean, default=True, nullable=False)

    department = relationship("Department", back_populates="rooms")
