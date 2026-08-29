"""
AegisCare Enterprise Patient Management System - Ward & Bed API Router
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.exceptions import BedUnavailableException
from app.db.session import get_db
from app.models.ward import Bed, Ward
from app.schemas.common import ResponseEnvelope
from app.schemas.ward import BedAllocationCreate, BedAllocationResponse
from app.services.ward_service import WardService

router = APIRouter(prefix="/wards", tags=["Wards & Beds"])


@router.get("", response_model=ResponseEnvelope[List[dict]])
def list_wards(db: Session = Depends(get_db)):
    """List inpatient wards with capacity and floor details."""
    wards = db.query(Ward).filter(Ward.is_active == True).all()
    data = [
        {"id": w.id, "name": w.name, "type": w.ward_type.value, "capacity": w.total_capacity, "daily_rate": float(w.daily_rate)}
        for w in wards
    ]
    return ResponseEnvelope(data=data)


@router.get("/beds/available", response_model=ResponseEnvelope[List[dict]])
def list_available_beds(db: Session = Depends(get_db)):
    """List all available hospital beds ready for admission."""
    service = WardService(db)
    beds = service.ward_repo.get_available_beds()
    data = [
        {"id": b.id, "identifier": b.bed_identifier, "room": b.room.room_number if b.room else "N/A", "ward": b.room.ward.name if b.room and b.room.ward else "N/A"}
        for b in beds
    ]
    return ResponseEnvelope(data=data)


@router.post("/beds/admit", response_model=ResponseEnvelope[BedAllocationResponse])
def admit_patient(alloc_in: BedAllocationCreate, db: Session = Depends(get_db)):
    """Allocate inpatient bed to patient."""
    service = WardService(db)
    try:
        alloc = service.admit_patient_to_bed(alloc_in.bed_id, alloc_in.patient_id, alloc_in.admission_reason)
        return ResponseEnvelope(data=BedAllocationResponse.model_validate(alloc), message="Patient admitted")
    except BedUnavailableException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.post("/beds/discharge/{allocation_id}", response_model=ResponseEnvelope[BedAllocationResponse])
def discharge_patient(allocation_id: int, db: Session = Depends(get_db)):
    """Discharge inpatient and free bed."""
    service = WardService(db)
    alloc = service.discharge_patient(allocation_id)
    return ResponseEnvelope(data=BedAllocationResponse.model_validate(alloc), message="Patient discharged")
