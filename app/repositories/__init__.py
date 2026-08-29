"""
AegisCare Enterprise Patient Management System - Repository Layer Registry
"""
from app.repositories.base import BaseRepository
from app.repositories.user_repo import UserRepository
from app.repositories.patient_repo import PatientRepository
from app.repositories.doctor_repo import DoctorRepository
from app.repositories.appointment_repo import AppointmentRepository
from app.repositories.clinical_repo import ClinicalRepository
from app.repositories.triage_repo import TriageRepository
from app.repositories.prescription_repo import PrescriptionRepository
from app.repositories.lab_repo import LaboratoryRepository
from app.repositories.billing_repo import BillingRepository
from app.repositories.ward_repo import WardRepository
from app.repositories.audit_repo import AuditRepository

__all__ = [
    "BaseRepository", "UserRepository", "PatientRepository", "DoctorRepository",
    "AppointmentRepository", "ClinicalRepository", "TriageRepository",
    "PrescriptionRepository", "LaboratoryRepository", "BillingRepository",
    "WardRepository", "AuditRepository"
]
