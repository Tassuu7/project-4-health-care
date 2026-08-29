"""
AegisCare Enterprise Patient Management System - Notification & Alert Models
Defines in-app alerts, clinical emergency notifications, and broadcast messages.
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Notification(Base, TimestampMixin):
    """User in-app notification for appointments, lab results, and triage alerts."""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(128), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(32), default="INFO", nullable=False, doc="INFO, WARNING, CRITICAL, APPOINTMENT, LAB")
    action_url = Column(String(255), nullable=True)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="notifications")


class NotificationTemplate(Base, TimestampMixin):
    """Standardized email and SMS reminder templates."""
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    template_key = Column(String(64), unique=True, nullable=False)
    subject_template = Column(String(255), nullable=False)
    body_template = Column(Text, nullable=False)


class AlertQueue(Base, TimestampMixin):
    """Emergency high-priority physician paging queue."""
    __tablename__ = "alert_queues"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    target_role = Column(String(32), nullable=False)
    priority_level = Column(Integer, default=1, nullable=False)
    alert_message = Column(Text, nullable=False)
    is_acknowledged = Column(Boolean, default=False, nullable=False)
    acknowledged_by_user_id = Column(Integer, nullable=True)
