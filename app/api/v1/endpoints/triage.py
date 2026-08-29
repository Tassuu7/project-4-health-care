"""
AegisCare Enterprise Patient Management System - Emergency Triage API Router
"""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.constants import TriageLevel
from app.db.session import get_db
from app.models.triage import TriageAssessment
from app.schemas.common import ResponseEnvelope
from app.schemas.triage import TriageAssessmentResponse, TriageInput
from app.services.triage_engine import TriageEngine

router = APIRouter(prefix="/triage", tags=["Emergency Triage"])


@router.post("/evaluate", response_model=ResponseEnvelope[Dict[str, Any]])
def evaluate_triage_score(intake: TriageInput):
    """Real-time ESI scoring calculator without database persistence."""
    level, zone, reason = TriageEngine.calculate_esi_level(intake)
    return ResponseEnvelope(data={
        "triage_level": level.value,
        "triage_label": level.label,
        "color_code": level.color_code,
        "assigned_zone": zone,
        "clinical_reason": reason
    })


@router.post("/assess", response_model=ResponseEnvelope[TriageAssessmentResponse], status_code=status.HTTP_201_CREATED)
def submit_triage_assessment(intake: TriageInput, nurse_user_id: int = Query(1), db: Session = Depends(get_db)):
    """Submit and save official Emergency Department triage intake assessment."""
    level, zone, _ = TriageEngine.calculate_esi_level(intake)
    triage_num = f"TRG-{int(datetime.utcnow().timestamp())}"
    
    assessment = TriageAssessment(
        triage_number=triage_num,
        patient_id=intake.patient_id,
        nurse_id=nurse_user_id,
        triage_level=level,
        chief_complaint=intake.chief_complaint,
        pain_score=intake.pain_score,
        heart_rate=intake.heart_rate,
        systolic_bp=intake.systolic_bp,
        diastolic_bp=intake.diastolic_bp,
        respiratory_rate=intake.respiratory_rate,
        oxygen_saturation=intake.oxygen_saturation,
        temperature_celsius=intake.temperature_celsius,
        is_resuscitation_required=intake.is_resuscitation_required,
        is_high_risk_situation=intake.is_high_risk_situation,
        estimated_resource_count=intake.estimated_resource_count,
        assigned_zone=zone,
        triage_notes=intake.triage_notes,
        is_active=True
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return ResponseEnvelope(data=TriageAssessmentResponse.model_validate(assessment), message="Triage registered")


@router.get("/queue", response_model=ResponseEnvelope[List[TriageAssessmentResponse]])
def get_triage_queue(db: Session = Depends(get_db)):
    """Retrieve active emergency waiting list prioritized by acuity score."""
    from app.repositories.triage_repo import TriageRepository
    repo = TriageRepository(db)
    items = repo.get_active_emergency_queue()
    return ResponseEnvelope(data=[TriageAssessmentResponse.model_validate(i) for i in items])
