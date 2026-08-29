"""
AegisCare Enterprise Patient Management System - Appointment Repository
"""

from datetime import datetime, time
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.core.constants import AppointmentStatus
from app.models.appointment import Appointment
from app.repositories.base import BaseRepository


class AppointmentRepository(BaseRepository[Appointment]):
    """Data access repository for Appointment booking and schedule conflict detection."""

    def __init__(self, db: Session):
        super().__init__(Appointment, db)

    def get_doctor_schedule_conflicts(
        self,
        doctor_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_appointment_id: Optional[int] = None
    ) -> List[Appointment]:
        """Identify overlapping appointments for a doctor during requested slot."""
        query = self.db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status.in_([AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED, AppointmentStatus.CHECKED_IN]),
            Appointment.is_deleted == False,
            Appointment.start_time < end_time,
            Appointment.end_time > start_time
        )
        if exclude_appointment_id:
            query = query.filter(Appointment.id != exclude_appointment_id)
        return query.all()

    def get_today_queue(self, doctor_id: Optional[int] = None) -> List[Appointment]:
        """Fetch all active appointments scheduled for today."""
        today_start = datetime.combine(datetime.utcnow().date(), time.min)
        today_end = datetime.combine(datetime.utcnow().date(), time.max)
        
        query = self.db.query(Appointment).options(
            joinedload(Appointment.patient),
            joinedload(Appointment.doctor)
        ).filter(
            Appointment.start_time >= today_start,
            Appointment.start_time <= today_end,
            Appointment.is_deleted == False
        )
        if doctor_id:
            query = query.filter(Appointment.doctor_id == doctor_id)
        return query.order_by(Appointment.start_time.asc()).all()

    def get_patient_appointments(self, patient_id: int) -> List[Appointment]:
        """List historical and upcoming appointments for a patient."""
        return self.db.query(Appointment).options(
            joinedload(Appointment.doctor),
            joinedload(Appointment.department)
        ).filter(
            Appointment.patient_id == patient_id,
            Appointment.is_deleted == False
        ).order_by(Appointment.start_time.desc()).all()
