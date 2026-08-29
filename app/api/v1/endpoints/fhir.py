"""
AegisCare Enterprise Patient Management System - FHIR R4 Interoperability API Router
"""

from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.clinical import VitalSign
from app.models.patient import Patient
from app.services.fhir_service import FhirConverterService

router = APIRouter(prefix="/fhir", tags=["HL7 FHIR Interoperability"])


@router.get("/Patient/{patient_id}", response_model=Dict[str, Any])
def get_fhir_patient(patient_id: int, db: Session = Depends(get_db)):
    """Export patient record in HL7 FHIR Release 4 JSON format."""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return FhirConverterService.patient_to_fhir_resource(patient)


@router.get("/Observation/{vital_id}", response_model=Dict[str, Any])
def get_fhir_vital_observation(vital_id: int, db: Session = Depends(get_db)):
    """Export vital signs observation in HL7 FHIR Release 4 JSON format."""
    vital = db.query(VitalSign).filter(VitalSign.id == vital_id).first()
    if not vital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Observation not found")
    return FhirConverterService.vitals_to_fhir_observation(vital)
