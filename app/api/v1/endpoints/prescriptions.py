"""
AegisCare Enterprise Patient Management System - Prescription API Router
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.exceptions import DrugInteractionConflictException
from app.db.session import get_db
from app.models.prescription import Medication
from app.schemas.common import ResponseEnvelope
from app.schemas.prescription import MedicationResponse, PrescriptionCreate, PrescriptionResponse
from app.services.prescription_service import PrescriptionService

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


@router.get("/medications", response_model=ResponseEnvelope[List[MedicationResponse]])
def list_medications(db: Session = Depends(get_db)):
    """List hospital formulary medication catalogue."""
    meds = db.query(Medication).filter(Medication.is_deleted == False).all()
    return ResponseEnvelope(data=[MedicationResponse.model_validate(m) for m in meds])


@router.post("", response_model=ResponseEnvelope[PrescriptionResponse], status_code=status.HTTP_201_CREATED)
def create_prescription(rx_in: PrescriptionCreate, doctor_id: int = Query(1), db: Session = Depends(get_db)):
    """Issue digital prescription with automated drug safety cross-check."""
    service = PrescriptionService(db)
    try:
        rx = service.issue_prescription(rx_in, doctor_id=doctor_id)
        return ResponseEnvelope(data=PrescriptionResponse.model_validate(rx), message="Prescription issued")
    except DrugInteractionConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.get("/patient/{patient_id}", response_model=ResponseEnvelope[List[PrescriptionResponse]])
def get_patient_prescriptions(patient_id: int, db: Session = Depends(get_db)):
    """Retrieve all prescriptions issued to a patient."""
    service = PrescriptionService(db)
    rxs = service.prescription_repo.get_patient_prescriptions(patient_id)
    return ResponseEnvelope(data=[PrescriptionResponse.model_validate(r) for r in rxs])
