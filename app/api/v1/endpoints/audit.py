"""
AegisCare Enterprise Patient Management System - HIPAA Audit API Router
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.audit import AuditLogResponse
from app.schemas.common import ResponseEnvelope
from app.services.audit_service import AuditService

router = APIRouter(prefix="/audit", tags=["HIPAA Compliance Audit"])


@router.get("/logs", response_model=ResponseEnvelope[List[AuditLogResponse]])
def get_audit_trail(limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)):
    """Fetch immutable audit logs for HIPAA security compliance verification."""
    service = AuditService(db)
    logs = service.get_compliance_audit_trail(limit=limit)
    return ResponseEnvelope(data=[AuditLogResponse.model_validate(l) for l in logs])
