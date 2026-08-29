"""
AegisCare Enterprise Patient Management System - Appointment Scheduling Service
"""

import random
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.constants import AppointmentStatus
from app.core.exceptions import AppointmentConflictException
from app.models.appointment import Appointment
from app.repositories.appointment_repo import AppointmentRepository
from app.repositories.doctor_repo import DoctorRepository
from app.schemas.appointment import AppointmentCreate


class AppointmentService:
    """Business logic for booking, schedule conflict resolution, and status lifecycle."""

    def __init__(self, db: Session):
        self.db = db
        self.appointment_repo = AppointmentRepository(db)
        self.doctor_repo = DoctorRepository(db)

    def book_appointment(self, appt_in: AppointmentCreate) -> Appointment:
        """Schedule appointment after verifying doctor availability without overlapping slots."""
        conflicts = self.appointment_repo.get_doctor_schedule_conflicts(
            doctor_id=appt_in.doctor_id,
            start_time=appt_in.start_time,
            end_time=appt_in.end_time
        )
        if conflicts:
            doctor = self.doctor_repo.get_by_id(appt_in.doctor_id)
            doc_name = doctor.full_name if doctor else "Physician"
            raise AppointmentConflictException(doc_name, appt_in.start_time.strftime("%Y-%m-%d %H:%M"))

        appt_num = f"APT-{int(datetime.utcnow().timestamp())}-{random.randint(100, 999)}"
        appt_data = appt_in.model_dump()
        appt_data["appointment_number"] = appt_num
        appt_data["status"] = AppointmentStatus.SCHEDULED
        
        appt = self.appointment_repo.create(appt_data)
        return appt

    def check_in_patient(self, appointment_id: int) -> Appointment:
        """Transition appointment to CHECKED_IN status."""
        appt = self.appointment_repo.get_by_id(appointment_id)
        if not appt:
            raise ResourceNotFoundError("Appointment", appointment_id)
        appt.status = AppointmentStatus.CHECKED_IN
        self.db.commit()
        return appt
