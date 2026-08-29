"""
AegisCare Enterprise Patient Management System - Role-Based Access Control (RBAC)
Defines permission matrices, role hierarchies, and authorization check helpers.
"""

from typing import Dict, List, Set
from app.core.constants import UserRole
from app.core.exceptions import AuthorizationError


class Permission:
    """Permission identifiers in AegisCare clinical platform."""
    # Patient Demographics
    PATIENT_VIEW = "patient:view"
    PATIENT_CREATE = "patient:create"
    PATIENT_UPDATE = "patient:update"
    PATIENT_DELETE = "patient:delete"
    
    # Clinical & Medical Records
    RECORD_VIEW = "record:view"
    RECORD_CREATE = "record:create"
    RECORD_UPDATE = "record:update"
    RECORD_EXPORT = "record:export"
    
    # Triage & Emergency
    TRIAGE_ASSESS = "triage:assess"
    TRIAGE_OVERRIDE = "triage:override"
    
    # Appointments
    APPOINTMENT_VIEW = "appointment:view"
    APPOINTMENT_BOOK = "appointment:book"
    APPOINTMENT_CANCEL = "appointment:cancel"
    APPOINTMENT_MANAGE_ALL = "appointment:manage_all"
    
    # Prescriptions
    PRESCRIPTION_WRITE = "prescription:write"
    PRESCRIPTION_VIEW = "prescription:view"
    PRESCRIPTION_DISPENSE = "prescription:dispense"
    
    # Laboratory & Diagnostics
    LAB_ORDER = "lab:order"
    LAB_ENTER_RESULT = "lab:enter_result"
    LAB_VERIFY = "lab:verify"
    LAB_VIEW = "lab:view"
    
    # Wards & Bed Allocation
    BED_ALLOCATE = "bed:allocate"
    BED_MANAGE = "bed:manage"
    BED_VIEW = "bed:view"
    
    # Billing & Finance
    INVOICE_CREATE = "invoice:create"
    INVOICE_PAY = "invoice:pay"
    INVOICE_VIEW = "invoice:view"
    FINANCIAL_REPORT = "finance:report"
    
    # System Administration & Auditing
    USER_MANAGE = "user:manage"
    AUDIT_VIEW = "audit:view"
    CONFIG_MANAGE = "config:manage"
    ANALYTICS_VIEW = "analytics:view"


# Role-Permission Mapping Matrix
ROLE_PERMISSIONS: Dict[UserRole, Set[str]] = {
    UserRole.ADMIN: {
        Permission.PATIENT_VIEW, Permission.PATIENT_CREATE, Permission.PATIENT_UPDATE, Permission.PATIENT_DELETE,
        Permission.RECORD_VIEW, Permission.RECORD_CREATE, Permission.RECORD_UPDATE, Permission.RECORD_EXPORT,
        Permission.TRIAGE_ASSESS, Permission.TRIAGE_OVERRIDE,
        Permission.APPOINTMENT_VIEW, Permission.APPOINTMENT_BOOK, Permission.APPOINTMENT_CANCEL, Permission.APPOINTMENT_MANAGE_ALL,
        Permission.PRESCRIPTION_WRITE, Permission.PRESCRIPTION_VIEW, Permission.PRESCRIPTION_DISPENSE,
        Permission.LAB_ORDER, Permission.LAB_ENTER_RESULT, Permission.LAB_VERIFY, Permission.LAB_VIEW,
        Permission.BED_ALLOCATE, Permission.BED_MANAGE, Permission.BED_VIEW,
        Permission.INVOICE_CREATE, Permission.INVOICE_PAY, Permission.INVOICE_VIEW, Permission.FINANCIAL_REPORT,
        Permission.USER_MANAGE, Permission.AUDIT_VIEW, Permission.CONFIG_MANAGE, Permission.ANALYTICS_VIEW,
    },
    UserRole.CHIEF_MEDICAL_OFFICER: {
        Permission.PATIENT_VIEW, Permission.PATIENT_CREATE, Permission.PATIENT_UPDATE,
        Permission.RECORD_VIEW, Permission.RECORD_CREATE, Permission.RECORD_UPDATE, Permission.RECORD_EXPORT,
        Permission.TRIAGE_ASSESS, Permission.TRIAGE_OVERRIDE,
        Permission.APPOINTMENT_VIEW, Permission.APPOINTMENT_BOOK, Permission.APPOINTMENT_CANCEL, Permission.APPOINTMENT_MANAGE_ALL,
        Permission.PRESCRIPTION_WRITE, Permission.PRESCRIPTION_VIEW,
        Permission.LAB_ORDER, Permission.LAB_VERIFY, Permission.LAB_VIEW,
        Permission.BED_ALLOCATE, Permission.BED_VIEW,
        Permission.ANALYTICS_VIEW, Permission.AUDIT_VIEW,
    },
    UserRole.DOCTOR: {
        Permission.PATIENT_VIEW, Permission.PATIENT_CREATE, Permission.PATIENT_UPDATE,
        Permission.RECORD_VIEW, Permission.RECORD_CREATE, Permission.RECORD_UPDATE,
        Permission.TRIAGE_ASSESS,
        Permission.APPOINTMENT_VIEW, Permission.APPOINTMENT_BOOK, Permission.APPOINTMENT_CANCEL,
        Permission.PRESCRIPTION_WRITE, Permission.PRESCRIPTION_VIEW,
        Permission.LAB_ORDER, Permission.LAB_VIEW,
        Permission.BED_VIEW,
    },
    UserRole.SPECIALIST: {
        Permission.PATIENT_VIEW, Permission.PATIENT_UPDATE,
        Permission.RECORD_VIEW, Permission.RECORD_CREATE, Permission.RECORD_UPDATE,
        Permission.APPOINTMENT_VIEW,
        Permission.PRESCRIPTION_WRITE, Permission.PRESCRIPTION_VIEW,
        Permission.LAB_ORDER, Permission.LAB_VIEW,
        Permission.BED_VIEW,
    },
    UserRole.HEAD_NURSE: {
        Permission.PATIENT_VIEW, Permission.PATIENT_CREATE, Permission.PATIENT_UPDATE,
        Permission.RECORD_VIEW, Permission.RECORD_CREATE,
        Permission.TRIAGE_ASSESS, Permission.TRIAGE_OVERRIDE,
        Permission.APPOINTMENT_VIEW,
        Permission.PRESCRIPTION_VIEW,
        Permission.LAB_ORDER, Permission.LAB_VIEW,
        Permission.BED_ALLOCATE, Permission.BED_MANAGE, Permission.BED_VIEW,
    },
    UserRole.TRIAGE_NURSE: {
        Permission.PATIENT_VIEW, Permission.PATIENT_CREATE, Permission.PATIENT_UPDATE,
        Permission.RECORD_VIEW, Permission.RECORD_CREATE,
        Permission.TRIAGE_ASSESS,
        Permission.APPOINTMENT_VIEW,
        Permission.BED_VIEW,
    },
    UserRole.STAFF_NURSE: {
        Permission.PATIENT_VIEW,
        Permission.RECORD_VIEW, Permission.RECORD_CREATE,
        Permission.TRIAGE_ASSESS,
        Permission.PRESCRIPTION_VIEW,
        Permission.LAB_VIEW,
        Permission.BED_VIEW,
    },
    UserRole.PHARMACIST: {
        Permission.PATIENT_VIEW,
        Permission.PRESCRIPTION_VIEW, Permission.PRESCRIPTION_DISPENSE,
        Permission.RECORD_VIEW,
    },
    UserRole.LAB_TECHNICIAN: {
        Permission.PATIENT_VIEW,
        Permission.LAB_VIEW, Permission.LAB_ENTER_RESULT, Permission.LAB_VERIFY,
    },
    UserRole.BILLING_OFFICER: {
        Permission.PATIENT_VIEW,
        Permission.INVOICE_CREATE, Permission.INVOICE_PAY, Permission.INVOICE_VIEW, Permission.FINANCIAL_REPORT,
    },
    UserRole.RECEPTIONIST: {
        Permission.PATIENT_VIEW, Permission.PATIENT_CREATE, Permission.PATIENT_UPDATE,
        Permission.APPOINTMENT_VIEW, Permission.APPOINTMENT_BOOK, Permission.APPOINTMENT_CANCEL,
        Permission.BED_VIEW,
    },
    UserRole.PATIENT: {
        Permission.PATIENT_VIEW,
        Permission.RECORD_VIEW,
        Permission.APPOINTMENT_VIEW, Permission.APPOINTMENT_BOOK, Permission.APPOINTMENT_CANCEL,
        Permission.PRESCRIPTION_VIEW,
        Permission.LAB_VIEW,
        Permission.INVOICE_VIEW, Permission.INVOICE_PAY,
    },
    UserRole.AUDITOR: {
        Permission.PATIENT_VIEW,
        Permission.RECORD_VIEW,
        Permission.AUDIT_VIEW,
        Permission.ANALYTICS_VIEW,
    },
}


def check_permission(user_role: str, required_permission: str) -> bool:
    """Evaluate if a role possesses the specified permission."""
    try:
        role_enum = UserRole(user_role)
    except ValueError:
        return False
    role_perms = ROLE_PERMISSIONS.get(role_enum, set())
    return required_permission in role_perms


def require_permission(user_role: str, required_permission: str):
    """Enforce permission check, raising AuthorizationError if denied."""
    if not check_permission(user_role, required_permission):
        raise AuthorizationError(
            f"User role '{user_role}' lacks required permission '{required_permission}'"
        )
