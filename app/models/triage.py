"""
AegisCare Enterprise Patient Management System - Emergency Triage Models
Defines Emergency Severity Index (ESI) scoring, triage assessments, and acute alerts.
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.constants import TriageLevel
from app.db.base import Base, TimestampMixin, AuditMixin


class TriageAssessment(Base, TimestampMixin, AuditMixin):
    """Emergency room triage evaluation calculating clinical acuity."""
    __tablename__ = "triage_assessments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    triage_number = Column(String(32), unique=True, index=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    nurse_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    triage_level = Column(SQLEnum(TriageLevel), nullable=False, index=True)
    chief_complaint = Column(String(255), nullable=False)
    pain_score = Column(Integer, default=0, nullable=False)
    
    # Vital signs at intake
    heart_rate = Column(Integer, nullable=True)
    systolic_bp = Column(Integer, nullable=True)
    diastolic_bp = Column(Integer, nullable=True)
    respiratory_rate = Column(Integer, nullable=True)
    oxygen_saturation = Column(Float, nullable=True)
    temperature_celsius = Column(Float, nullable=True)
    
    # Clinical decision criteria
    is_resuscitation_required = Column(Boolean, default=False, nullable=False)
    is_high_risk_situation = Column(Boolean, default=False, nullable=False)
    estimated_resource_count = Column(Integer, default=1, nullable=False)
    is_danger_vital_signs = Column(Boolean, default=False, nullable=False)
    
    assigned_zone = Column(String(32), default="WAITING_ROOM", nullable=False)
    triage_notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="triage_assessments")
    nurse = relationship("User")


class RapidAssessment(Base, TimestampMixin):
    """Quick 30-second nursing assessment performed upon immediate patient arrival."""
    __tablename__ = "rapid_assessments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    airway_patent = Column(Boolean, default=True, nullable=False)
    breathing_adequate = Column(Boolean, default=True, nullable=False)
    circulation_intact = Column(Boolean, default=True, nullable=False)
    disability_neuro_score = Column(String(16), default="ALERT", nullable=False, doc="AVPU scale: Alert, Voice, Pain, Unresponsive")
    immediate_action_taken = Column(String(255), nullable=True)
