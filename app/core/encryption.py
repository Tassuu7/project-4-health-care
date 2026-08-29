"""
AegisCare Enterprise Patient Management System - Data Masking & Encryption Utilities
Provides HIPAA compliant Protected Health Information (PHI) anonymization and masking.
"""

import hashlib
import re
from typing import Optional


def mask_ssn(ssn: Optional[str]) -> str:
    """Mask Social Security Number / National ID (e.g. ***-**-1234)."""
    if not ssn:
        return "N/A"
    clean = re.sub(r"[^0-9]", "", ssn)
    if len(clean) >= 4:
        return f"***-**-{clean[-4:]}"
    return "***-**-****"


def mask_email(email: Optional[str]) -> str:
    """Mask email address for privacy display (e.g. j***n@domain.com)."""
    if not email or "@" not in email:
        return "hidden@domain.local"
    name_part, domain_part = email.split("@", 1)
    if len(name_part) <= 2:
        masked_name = name_part[0] + "***"
    else:
        masked_name = name_part[0] + "*" * (len(name_part) - 2) + name_part[-1]
    return f"{masked_name}@{domain_part}"


def mask_phone(phone: Optional[str]) -> str:
    """Mask phone number keeping only last 4 digits (e.g. (***) ***-5678)."""
    if not phone:
        return "N/A"
    clean = re.sub(r"[^0-9]", "", phone)
    if len(clean) >= 4:
        return f"(***) ***-{clean[-4:]}"
    return "(***) ***-****"


def hash_identifier(identifier: str) -> str:
    """Generate deterministic SHA-256 hash of patient identifier for anonymized lookups."""
    if not identifier:
        return ""
    return hashlib.sha256(identifier.strip().encode("utf-8")).hexdigest()
