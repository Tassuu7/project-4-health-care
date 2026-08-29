"""
AegisCare Enterprise Patient Management System - Doctor API Router
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.common import ResponseEnvelope
from app.schemas.doctor import DoctorResponse
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("", response_model=ResponseEnvelope[List[DoctorResponse]])
def list_doctors(department_id: Optional[int] = None, db: Session = Depends(get_db)):
    """List all active physicians filtered optionally by clinical department."""
    service = AppointmentService(db)
    if department_id:
        doctors = service.doctor_repo.list_by_department(department_id)
    else:
        doctors = service.doctor_repo.get_available_doctors()
    return ResponseEnvelope(data=[DoctorResponse.model_validate(d) for d in doctors])
