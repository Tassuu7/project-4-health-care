"""
AegisCare Enterprise Patient Management System - Patient API Router
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.exceptions import ResourceNotFoundError
from app.db.session import get_db
from app.models.clinical import VitalSign
from app.schemas.clinical import VitalSignCreate, VitalSignResponse
from app.schemas.common import PaginatedResponse, ResponseEnvelope
from app.schemas.patient import PatientCreate, PatientResponse, PatientSummary, PatientUpdate
from app.services.clinical_service import ClinicalService
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("", response_model=ResponseEnvelope[PaginatedResponse[PatientSummary]])
def list_patients(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve paginated patient list with keyword search."""
    service = PatientService(db)
    items, total = service.patient_repo.get_paginated(
        page=page,
        limit=limit,
        search_query=search,
        search_fields=["first_name", "last_name", "mrn", "phone_number"]
    )
    total_pages = (total + limit - 1) // limit if total > 0 else 1
    summaries = [PatientSummary.model_validate(p) for p in items]
    
    paginated = PaginatedResponse(
        items=summaries,
        total_count=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
    return ResponseEnvelope(data=paginated)


@router.post("", response_model=ResponseEnvelope[PatientResponse], status_code=status.HTTP_201_CREATED)
def create_patient(patient_in: PatientCreate, db: Session = Depends(get_db)):
    """Register a new patient and allocate unique MRN."""
    service = PatientService(db)
    patient = service.register_patient(patient_in)
    return ResponseEnvelope(data=PatientResponse.model_validate(patient), message="Patient created")


@router.get("/{patient_id}", response_model=ResponseEnvelope[PatientResponse])
def get_patient_detail(patient_id: int, db: Session = Depends(get_db)):
    """Retrieve complete patient demographics, emergency contacts, and allergies."""
    service = PatientService(db)
    try:
        patient = service.get_patient(patient_id)
        return ResponseEnvelope(data=PatientResponse.model_validate(patient))
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.put("/{patient_id}", response_model=ResponseEnvelope[PatientResponse])
def update_patient_info(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    """Update patient demographic information."""
    service = PatientService(db)
    try:
        patient = service.update_patient(patient_id, patient_update)
        return ResponseEnvelope(data=PatientResponse.model_validate(patient), message="Patient updated")
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.post("/{patient_id}/vitals", response_model=ResponseEnvelope[VitalSignResponse], status_code=status.HTTP_201_CREATED)
def add_patient_vitals(patient_id: int, vitals_in: VitalSignCreate, db: Session = Depends(get_db)):
    """Record patient physiological vital signs with automated anomaly threshold check."""
    clinical_service = ClinicalService(db)
    vitals_in.patient_id = patient_id
    saved = clinical_service.record_vitals(vitals_in)
    return ResponseEnvelope(data=VitalSignResponse.model_validate(saved), message="Vitals logged")


@router.get("/{patient_id}/vitals", response_model=ResponseEnvelope[List[VitalSignResponse]])
def get_patient_vitals_history(patient_id: int, limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    """Retrieve chronological vital signs timeseries for graphing."""
    clinical_service = ClinicalService(db)
    vitals = clinical_service.clinical_repo.get_patient_vitals_history(patient_id, limit=limit)
    return ResponseEnvelope(data=[VitalSignResponse.model_validate(v) for v in vitals])
