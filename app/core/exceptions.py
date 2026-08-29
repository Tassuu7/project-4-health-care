"""
AegisCare Enterprise Patient Management System - Domain Exceptions
Custom exception hierarchy for clean error handling, logging, and HTTP mappings.
"""

from typing import Any, Dict, Optional


class AegisCareException(Exception):
    """Base exception for all domain errors in AegisCare platform."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class AuthenticationError(AegisCareException):
    """Raised when user credentials are invalid or expired."""
    def __init__(self, message: str = "Invalid authentication credentials", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="AUTHENTICATION_FAILED", details=details)


class AuthorizationError(AegisCareException):
    """Raised when user lacks required RBAC permissions."""
    def __init__(self, message: str = "Access denied: insufficient permissions", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="PERMISSION_DENIED", details=details)


class ResourceNotFoundError(AegisCareException):
    """Raised when requested entity is not found in database."""
    def __init__(self, resource_name: str, identifier: Any):
        message = f"{resource_name} with identifier '{identifier}' was not found"
        super().__init__(message, code="RESOURCE_NOT_FOUND", details={"resource": resource_name, "id": str(identifier)})


class ResourceConflictError(AegisCareException):
    """Raised when resource already exists or state transition conflicts."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="RESOURCE_CONFLICT", details=details)


class ValidationError(AegisCareException):
    """Raised when clinical data or input schema fails validation rules."""
    def __init__(self, message: str, field_errors: Optional[Dict[str, str]] = None):
        super().__init__(message, code="VALIDATION_ERROR", details={"field_errors": field_errors or {}})


class ClinicalTriageException(AegisCareException):
    """Raised when triage calculation or vitals threshold analysis fails."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="CLINICAL_TRIAGE_ERROR", details=details)


class DrugInteractionConflictException(AegisCareException):
    """Raised when prescribed medication has severe drug-drug or allergy interaction."""
    def __init__(self, drug1: str, drug2: str, severity: str, description: str):
        message = f"Severe Drug Interaction Conflict: {drug1} interacts with {drug2} ({severity})"
        super().__init__(
            message,
            code="DRUG_INTERACTION_CONFLICT",
            details={"drug1": drug1, "drug2": drug2, "severity": severity, "description": description}
        )


class AppointmentConflictException(AegisCareException):
    """Raised when requested appointment slot overlaps with existing doctor schedule."""
    def __init__(self, doctor_name: str, requested_time: str):
        message = f"Schedule Conflict: Dr. {doctor_name} is already booked at {requested_time}"
        super().__init__(
            message,
            code="APPOINTMENT_CONFLICT",
            details={"doctor": doctor_name, "requested_time": requested_time}
        )


class BedUnavailableException(AegisCareException):
    """Raised when attempting to allocate an occupied or maintenance bed."""
    def __init__(self, bed_number: str, ward_name: str, current_status: str):
        message = f"Bed {bed_number} in {ward_name} is not available (Current Status: {current_status})"
        super().__init__(
            message,
            code="BED_UNAVAILABLE",
            details={"bed_number": bed_number, "ward": ward_name, "status": current_status}
        )


class BillingCalculationException(AegisCareException):
    """Raised when invoice line items or tax calculations result in inconsistent totals."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="BILLING_CALCULATION_ERROR", details=details)


class InsuranceClaimException(AegisCareException):
    """Raised when insurance validation or claim submission fails."""
    def __init__(self, policy_number: str, reason: str):
        message = f"Insurance Claim Processing Failed for Policy {policy_number}: {reason}"
        super().__init__(
            message,
            code="INSURANCE_CLAIM_ERROR",
            details={"policy_number": policy_number, "reason": reason}
        )
