"""
AegisCare Enterprise Patient Management System - Audit Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.core.constants import AuditAction


class AuditLogResponse(BaseModel):
    id: int
    timestamp: datetime
    user_id: Optional[int] = None
    username: Optional[str] = None
    user_role: Optional[str] = None
    action: AuditAction
    resource_type: str
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    details: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
