"""
AegisCare Enterprise Patient Management System - Domain Model Registry
Aggregates and registers all SQLAlchemy ORM models for metadata discovery.
"""

from app.models.user import User, UserProfile, UserSession, PasswordResetToken
from app.models.department import Department, ClinicRoom
from app.models.doctor import Doctor, Specialization, DoctorSchedule
from app.models.patient import Patient, EmergencyContact, InsurancePolicy, Allergy, MedicalHistory
from app.models.appointment import Appointment, ConsultationNote
from app.models.clinical import MedicalRecord, VitalSign, Diagnosis, ClinicalNote, TreatmentPlan, Immunization
from app.models.triage import TriageAssessment, RapidAssessment
from app.models.prescription import Prescription, PrescriptionItem, Medication, DosageSchedule, MedicationDispenseLog
from app.models.laboratory import LabTestCatalog, LabOrder, LabResult, SpecimenSample, DiagnosticReport
from app.models.billing import Invoice, InvoiceItem, Payment, InsuranceClaim, FeeSchedule, PaymentReceipt
from app.models.ward import Ward, Room, Bed, BedAllocation, WardTransferLog
from app.models.audit import AuditLog, SecurityEvent, AccessLog
from app.models.notification import Notification, NotificationTemplate, AlertQueue

__all__ = [
    "User", "UserProfile", "UserSession", "PasswordResetToken",
    "Department", "ClinicRoom",
    "Doctor", "Specialization", "DoctorSchedule",
    "Patient", "EmergencyContact", "InsurancePolicy", "Allergy", "MedicalHistory",
    "Appointment", "ConsultationNote",
    "MedicalRecord", "VitalSign", "Diagnosis", "ClinicalNote", "TreatmentPlan", "Immunization",
    "TriageAssessment", "RapidAssessment",
    "Prescription", "PrescriptionItem", "Medication", "DosageSchedule", "MedicationDispenseLog",
    "LabTestCatalog", "LabOrder", "LabResult", "SpecimenSample", "DiagnosticReport",
    "Invoice", "InvoiceItem", "Payment", "InsuranceClaim", "FeeSchedule", "PaymentReceipt",
    "Ward", "Room", "Bed", "BedAllocation", "WardTransferLog",
    "AuditLog", "SecurityEvent", "AccessLog",
    "Notification", "NotificationTemplate", "AlertQueue",
]
