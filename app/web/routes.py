"""
AegisCare Enterprise Patient Management System - Web Page Route Handlers
Renders responsive HTML5 views for Physician, Nurse, Patient, Admin, Lab, and Pharmacy Portals.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.config import get_settings
from app.db.session import get_db
from app.services.analytics_service import AnalyticsService

settings = get_settings()
templates = Jinja2Templates(directory="app/templates")

web_router = APIRouter(include_in_schema=False)


@web_router.get("/", response_class=HTMLResponse)
def index_page(request: Request, db: Session = Depends(get_db)):
    """Landing portal and healthcare overview dashboard."""
    analytics = AnalyticsService(db)
    kpis = analytics.get_clinical_kpis()
    return templates.TemplateResponse(request=request, name="index.html", context={"app_name": settings.APP_NAME, "kpis": kpis})


@web_router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Authentication login portal with quick demo role selection."""
    return templates.TemplateResponse(request=request, name="login.html", context={"app_name": settings.APP_NAME})


@web_router.get("/doctor-dashboard", response_class=HTMLResponse)
def doctor_dashboard_page(request: Request):
    """Physician clinical workbench and patient consultation queue."""
    return templates.TemplateResponse(request=request, name="doctor_dashboard.html", context={"app_name": settings.APP_NAME})


@web_router.get("/nurse-station", response_class=HTMLResponse)
def nurse_station_page(request: Request):
    """Nurse emergency triage intake and inpatient bed ward management."""
    return templates.TemplateResponse(request=request, name="nurse_station.html", context={"app_name": settings.APP_NAME})


@web_router.get("/patient-portal", response_class=HTMLResponse)
def patient_portal_page(request: Request):
    """Patient self-service portal for appointment booking and records."""
    return templates.TemplateResponse(request=request, name="patient_portal.html", context={"app_name": settings.APP_NAME})


@web_router.get("/admin-console", response_class=HTMLResponse)
def admin_console_page(request: Request, db: Session = Depends(get_db)):
    """Hospital executive administration, user RBAC, and HIPAA audit viewer."""
    analytics = AnalyticsService(db)
    kpis = analytics.get_clinical_kpis()
    revenue = analytics.get_revenue_report()
    return templates.TemplateResponse(request=request, name="admin_console.html", context={"app_name": settings.APP_NAME, "kpis": kpis, "revenue": revenue})


@web_router.get("/pharmacy-console", response_class=HTMLResponse)
def pharmacy_console_page(request: Request):
    """Pharmacy prescription fulfillment and inventory management."""
    return templates.TemplateResponse(request=request, name="pharmacy_console.html", context={"app_name": settings.APP_NAME})


@web_router.get("/lab-console", response_class=HTMLResponse)
def lab_console_page(request: Request):
    """Diagnostic laboratory analysis and test result entry."""
    return templates.TemplateResponse(request=request, name="lab_console.html", context={"app_name": settings.APP_NAME})


@web_router.get("/billing-console", response_class=HTMLResponse)
def billing_console_page(request: Request):
    """Hospital patient invoicing, billing ledger, and insurance claims."""
    return templates.TemplateResponse(request=request, name="billing_console.html", context={"app_name": settings.APP_NAME})
