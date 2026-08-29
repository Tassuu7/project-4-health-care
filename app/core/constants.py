"""
AegisCare Enterprise Patient Management System - Healthcare Constants
Defines clinical codes, triage protocols, role enumerations, and system constants.
"""

from enum import Enum, IntEnum


class UserRole(str, Enum):
    """Role-based access control roles in healthcare hierarchy."""
    ADMIN = "ADMIN"
    CHIEF_MEDICAL_OFFICER = "CHIEF_MEDICAL_OFFICER"
    DOCTOR = "DOCTOR"
    SPECIALIST = "SPECIALIST"
    HEAD_NURSE = "HEAD_NURSE"
    TRIAGE_NURSE = "TRIAGE_NURSE"
    STAFF_NURSE = "STAFF_NURSE"
    PHARMACIST = "PHARMACIST"
    LAB_TECHNICIAN = "LAB_TECHNICIAN"
    BILLING_OFFICER = "BILLING_OFFICER"
    RECEPTIONIST = "RECEPTIONIST"
    PATIENT = "PATIENT"
    AUDITOR = "AUDITOR"


class Gender(str, Enum):
    """Patient gender categories."""
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"


class BloodGroup(str, Enum):
    """ABO and Rh blood group types."""
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    UNKNOWN = "UNKNOWN"


class TriageLevel(IntEnum):
    """Emergency Severity Index (ESI) 5-level triage score."""
    LEVEL_1_RESUSCITATION = 1
    LEVEL_2_EMERGENT = 2
    LEVEL_3_URGENT = 3
    LEVEL_4_LESS_URGENT = 4
    LEVEL_5_NON_URGENT = 5

    @property
    def label(self) -> str:
        labels = {
            1: "Resuscitation (Immediate Life Threat)",
            2: "Emergent (High Risk / Time Sensitive)",
            3: "Urgent (Multiple Resources Needed)",
            4: "Less Urgent (One Resource Needed)",
            5: "Non-Urgent (No Resources Needed)"
        }
        return labels.get(self.value, "Unknown")

    @property
    def color_code(self) -> str:
        colors = {
            1: "#dc2626", # Red
            2: "#ea580c", # Orange
            3: "#eab308", # Yellow
            4: "#16a34a", # Green
            5: "#2563eb"  # Blue
        }
        return colors.get(self.value, "#6b7280")


class AppointmentStatus(str, Enum):
    """Status lifecycle of clinical appointments."""
    SCHEDULED = "SCHEDULED"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    IN_CONSULTATION = "IN_CONSULTATION"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"
    RESCHEDULED = "RESCHEDULED"


class AppointmentType(str, Enum):
    """Types of patient medical visits."""
    ROUTINE_CHECKUP = "ROUTINE_CHECKUP"
    FOLLOW_UP = "FOLLOW_UP"
    SPECIALIST_CONSULT = "SPECIALIST_CONSULT"
    EMERGENCY = "EMERGENCY"
    SURGICAL_EVALUATION = "SURGICAL_EVALUATION"
    DIAGNOSTIC_REVIEW = "DIAGNOSTIC_REVIEW"
    TELEHEALTH = "TELEHEALTH"


class BedStatus(str, Enum):
    """Hospital inpatient ward bed allocation status."""
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    RESERVED = "RESERVED"
    CLEANING = "CLEANING"
    MAINTENANCE = "MAINTENANCE"
    ISOLATION = "ISOLATION"


class WardType(str, Enum):
    """Hospital department ward classifications."""
    GENERAL_MALE = "GENERAL_MALE"
    GENERAL_FEMALE = "GENERAL_FEMALE"
    ICU_INTENSIVE_CARE = "ICU_INTENSIVE_CARE"
    CCU_CORONARY_CARE = "CCU_CORONARY_CARE"
    NICU_NEONATAL = "NICU_NEONATAL"
    PEDIATRIC = "PEDIATRIC"
    MATERNITY = "MATERNITY"
    SURGICAL_POST_OP = "SURGICAL_POST_OP"
    EMERGENCY_OBSERVATION = "EMERGENCY_OBSERVATION"
    ISOLATION_INFECTIOUS = "ISOLATION_INFECTIOUS"


class PrescriptionStatus(str, Enum):
    """Prescription workflow status."""
    ACTIVE = "ACTIVE"
    DISPENSED = "DISPENSED"
    PARTIALLY_DISPENSED = "PARTIALLY_DISPENSED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    DISCONTINUED = "DISCONTINUED"


class LabOrderStatus(str, Enum):
    """Laboratory test order status."""
    ORDERED = "ORDERED"
    SAMPLE_COLLECTED = "SAMPLE_COLLECTED"
    SAMPLE_RECEIVED = "SAMPLE_RECEIVED"
    IN_ANALYSIS = "IN_ANALYSIS"
    COMPLETED = "COMPLETED"
    VERIFIED = "VERIFIED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class LabResultFlag(str, Enum):
    """Diagnostic laboratory result clinical evaluation flags."""
    NORMAL = "NORMAL"
    LOW = "LOW"
    HIGH = "HIGH"
    CRITICAL_LOW = "CRITICAL_LOW"
    CRITICAL_HIGH = "CRITICAL_HIGH"
    ABNORMAL = "ABNORMAL"


class InvoiceStatus(str, Enum):
    """Patient billing invoice status."""
    DRAFT = "DRAFT"
    ISSUED = "ISSUED"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    WRITTEN_OFF = "WRITTEN_OFF"


class PaymentMethod(str, Enum):
    """Methods of financial settlement."""
    CASH = "CASH"
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    INSURANCE_DIRECT = "INSURANCE_DIRECT"
    BANK_TRANSFER = "BANK_TRANSFER"
    ONLINE_PORTAL = "ONLINE_PORTAL"
    HEALTH_SAVINGS_ACCOUNT = "HEALTH_SAVINGS_ACCOUNT"


class InsuranceClaimStatus(str, Enum):
    """Medical insurance claim submission status."""
    PENDING_SUBMISSION = "PENDING_SUBMISSION"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    PARTIALLY_APPROVED = "PARTIALLY_APPROVED"
    REJECTED = "REJECTED"
    APPEALED = "APPEALED"
    SETTLED = "SETTLED"


class AuditAction(str, Enum):
    """HIPAA compliance security audit event actions."""
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILURE = "LOGIN_FAILURE"
    LOGOUT = "LOGOUT"
    PATIENT_VIEW = "PATIENT_VIEW"
    PATIENT_CREATE = "PATIENT_CREATE"
    PATIENT_UPDATE = "PATIENT_UPDATE"
    PATIENT_DELETE = "PATIENT_DELETE"
    MEDICAL_RECORD_VIEW = "MEDICAL_RECORD_VIEW"
    MEDICAL_RECORD_CREATE = "MEDICAL_RECORD_CREATE"
    PRESCRIPTION_ISSUE = "PRESCRIPTION_ISSUE"
    PRESCRIPTION_DISPENSE = "PRESCRIPTION_DISPENSE"
    LAB_ORDER_CREATE = "LAB_ORDER_CREATE"
    LAB_RESULT_VERIFY = "LAB_RESULT_VERIFY"
    INVOICE_CREATE = "INVOICE_CREATE"
    PAYMENT_RECEIVE = "PAYMENT_RECEIVE"
    SYSTEM_CONFIG_CHANGE = "SYSTEM_CONFIG_CHANGE"
    SECURITY_ALERT = "SECURITY_ALERT"
    EXPORT_DATA = "EXPORT_DATA"
