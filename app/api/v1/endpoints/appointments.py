"""
AegisCare Enterprise Patient Management System - Appointment API Router
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.constants import AppointmentStatus
from app.core.exceptions import AppointmentConflictException, ResourceNotFoundError
from app.db.session import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.schemas.common import ResponseEnvelope
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("", response_model=ResponseEnvelope[List[AppointmentResponse]])
def list_appointments(
    doctor_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    today_only: bool = False,
    db: Session = Depends(get_db)
):
    """Retrieve appointment queue or patient appointment history."""
    service = AppointmentService(db)
    if today_only:
        items = service.appointment_repo.get_today_queue(doctor_id=doctor_id)
    elif patient_id:
        items = service.appointment_repo.get_patient_appointments(patient_id=patient_id)
    else:
        items = service.appointment_repo.get_all(limit=100)
    return ResponseEnvelope(data=[AppointmentResponse.model_validate(a) for a in items])


@router.post("", response_model=ResponseEnvelope[AppointmentResponse], status_code=status.HTTP_201_CREATED)
def create_appointment(appt_in: AppointmentCreate, db: Session = Depends(get_db)):
    """Book a new consultation appointment with schedule conflict check."""
    service = AppointmentService(db)
    try:
        appt = service.book_appointment(appt_in)
        return ResponseEnvelope(data=AppointmentResponse.model_validate(appt), message="Appointment scheduled")
    except AppointmentConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.put("/{appointment_id}/check-in", response_model=ResponseEnvelope[AppointmentResponse])
def check_in(appointment_id: int, db: Session = Depends(get_db)):
    """Mark patient arrival and check-in for consultation."""
    service = AppointmentService(db)
    try:
        appt = service.check_in_patient(appointment_id)
        return ResponseEnvelope(data=AppointmentResponse.model_validate(appt), message="Patient checked in")
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.put("/{appointment_id}/cancel", response_model=ResponseEnvelope[AppointmentResponse])
def cancel_appointment(appointment_id: int, reason: str = "Patient request", db: Session = Depends(get_db)):
    """Cancel scheduled consultation."""
    service = AppointmentService(db)
    appt = service.appointment_repo.get_by_id(appointment_id)
    if not appt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    appt.status = AppointmentStatus.CANCELLED
    appt.cancellation_reason = reason
    db.commit()
    return ResponseEnvelope(data=AppointmentResponse.model_validate(appt), message="Appointment cancelled")
