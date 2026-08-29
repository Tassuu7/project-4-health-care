"""
AegisCare Enterprise Patient Management System - Master API v1 Router Aggregator
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    appointments,
    audit,
    auth,
    billing,
    doctors,
    fhir,
    laboratory,
    patients,
    prescriptions,
    reports,
    triage,
    wards,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(patients.router)
api_router.include_router(doctors.router)
api_router.include_router(appointments.router)
api_router.include_router(triage.router)
api_router.include_router(prescriptions.router)
api_router.include_router(laboratory.router)
api_router.include_router(billing.router)
api_router.include_router(wards.router)
api_router.include_router(reports.router)
api_router.include_router(audit.router)
api_router.include_router(fhir.router)
