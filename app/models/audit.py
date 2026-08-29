"""
AegisCare Enterprise Patient Management System - HIPAA Compliance Audit Models
Defines immutable audit log trails, security breach alerts, and user access records.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Text
from app.core.constants import AuditAction
from app.db.base import Base


class AuditLog(Base):
    """Immutable HIPAA compliance audit entry recording every sensitive data access."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    user_id = Column(Integer, nullable=True, index=True, doc="Actor user ID")
    username = Column(String(64), nullable=True)
    user_role = Column(String(32), nullable=True)
    
    action = Column(SQLEnum(AuditAction), nullable=False, index=True)
    resource_type = Column(String(64), nullable=False, doc="e.g. PATIENT, MEDICAL_RECORD, INVOICE")
    resource_id = Column(String(64), nullable=True)
    
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    details = Column(Text, nullable=True, doc="JSON metadata or description of changes")


class SecurityEvent(Base):
    """Security anomaly event (brute force login, privilege escalation attempt)."""
    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    severity = Column(String(16), default="HIGH", nullable=False)
    ip_address = Column(String(45), nullable=True)
    description = Column(Text, nullable=False)
    is_resolved = Column(Integer, default=0, nullable=False)


class AccessLog(Base):
    """HTTP endpoint access telemetry tracking response times and status codes."""
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    method = Column(String(8), nullable=False)
    path = Column(String(255), nullable=False)
    status_code = Column(Integer, nullable=False)
    duration_ms = Column(Float, nullable=False)
    client_ip = Column(String(45), nullable=True)
