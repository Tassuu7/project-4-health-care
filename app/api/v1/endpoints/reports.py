"""
AegisCare Enterprise Patient Management System - Executive Reports API Router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.common import ResponseEnvelope
from app.schemas.reports import ClinicalKPIs, RevenueReport
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/reports", tags=["Executive Reports"])


@router.get("/kpis", response_model=ResponseEnvelope[ClinicalKPIs])
def get_hospital_kpis(db: Session = Depends(get_db)):
    """Retrieve real-time hospital clinical performance indicators."""
    service = AnalyticsService(db)
    kpis = service.get_clinical_kpis()
    return ResponseEnvelope(data=kpis)


@router.get("/revenue", response_model=ResponseEnvelope[RevenueReport])
def get_revenue_summary(db: Session = Depends(get_db)):
    """Retrieve hospital billing revenue analytics."""
    service = AnalyticsService(db)
    report = service.get_revenue_report()
    return ResponseEnvelope(data=report)
