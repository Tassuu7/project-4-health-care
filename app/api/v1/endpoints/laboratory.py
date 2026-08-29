"""
AegisCare Enterprise Patient Management System - Laboratory API Router
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.laboratory import LabTestCatalog
from app.schemas.common import ResponseEnvelope
from app.schemas.laboratory import LabOrderCreate, LabOrderResponse, LabResultCreate, LabResultResponse
from app.services.laboratory_service import LaboratoryService

router = APIRouter(prefix="/lab", tags=["Laboratory"])


@router.get("/catalog", response_model=ResponseEnvelope[List[dict]])
def list_test_catalog(db: Session = Depends(get_db)):
    """List all available diagnostic laboratory tests."""
    tests = db.query(LabTestCatalog).filter(LabTestCatalog.is_active == True).all()
    catalog_data = [
        {"id": t.id, "test_code": t.test_code, "name": t.name, "category": t.category, "fee": float(t.standard_fee)}
        for t in tests
    ]
    return ResponseEnvelope(data=catalog_data)


@router.post("/orders", response_model=ResponseEnvelope[LabOrderResponse], status_code=status.HTTP_201_CREATED)
def place_lab_order(order_in: LabOrderCreate, db: Session = Depends(get_db)):
    """Requisition a new laboratory diagnostic test order."""
    service = LaboratoryService(db)
    order = service.place_order(order_in)
    return ResponseEnvelope(data=LabOrderResponse.model_validate(order), message="Lab order created")


@router.get("/queue", response_model=ResponseEnvelope[List[LabOrderResponse]])
def get_pending_lab_queue(db: Session = Depends(get_db)):
    """List pending lab orders awaiting sample collection or analysis."""
    service = LaboratoryService(db)
    queue = service.lab_repo.get_pending_queue()
    return ResponseEnvelope(data=[LabOrderResponse.model_validate(o) for o in queue])


@router.post("/results", response_model=ResponseEnvelope[LabResultResponse])
def enter_lab_result(result_in: LabResultCreate, tech_id: int = Query(1), db: Session = Depends(get_db)):
    """Record and evaluate laboratory test measurement against normal reference range."""
    service = LaboratoryService(db)
    result = service.record_result(result_in, tech_user_id=tech_id)
    return ResponseEnvelope(data=LabResultResponse.model_validate(result), message="Result verified")
