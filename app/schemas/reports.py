"""
AegisCare Enterprise Patient Management System - Reporting & Analytics Schemas
"""

from typing import Dict, List
from pydantic import BaseModel


class ClinicalKPIs(BaseModel):
    total_active_patients: int
    today_appointments: int
    pending_lab_orders: int
    occupied_beds_count: int
    bed_occupancy_rate_percent: float
    average_triage_wait_time_minutes: float
    critical_cases_today: int


class RevenueReport(BaseModel):
    total_billed: float
    total_collected: float
    total_outstanding: float
    collection_rate_percent: float
    revenue_by_department: Dict[str, float]
