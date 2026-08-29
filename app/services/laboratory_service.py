"""
AegisCare Enterprise Patient Management System - Laboratory Service
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.constants import AuditAction, LabOrderStatus, LabResultFlag
from app.models.laboratory import LabOrder, LabResult, SpecimenSample
from app.repositories.audit_repo import AuditRepository
from app.repositories.lab_repo import LaboratoryRepository
from app.schemas.laboratory import LabOrderCreate, LabResultCreate


class LaboratoryService:
    """Diagnostic order processing, specimen tracking, and lab result verification."""

    def __init__(self, db: Session):
        self.db = db
        self.lab_repo = LaboratoryRepository(db)
        self.audit_repo = AuditRepository(db)

    def place_order(self, order_in: LabOrderCreate) -> LabOrder:
        """Place new diagnostic test requisition order."""
        order_num = f"LAB-{int(datetime.utcnow().timestamp())}"
        order = LabOrder(
            order_number=order_num,
            patient_id=order_in.patient_id,
            doctor_id=order_in.doctor_id,
            status=LabOrderStatus.ORDERED,
            priority=order_in.priority,
            clinical_notes=order_in.clinical_notes
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        # Generate barcode sample placeholder
        barcode = f"SMP-{order.id}-{int(datetime.utcnow().timestamp())}"
        specimen = SpecimenSample(
            lab_order_id=order.id,
            barcode_identifier=barcode,
            specimen_type="SERUM_BLOOD"
        )
        self.db.add(specimen)
        self.db.commit()
        return order

    def record_result(self, result_in: LabResultCreate, tech_user_id: int) -> LabResult:
        """Record and evaluate laboratory test measurement against standard normal ranges."""
        catalog_test = self.db.query(LabTestCatalog).filter(LabTestCatalog.id == result_in.test_id).first()
        
        flag = LabResultFlag.NORMAL
        if catalog_test and result_in.numeric_value is not None:
            val = result_in.numeric_value
            if catalog_test.critical_high and val >= catalog_test.critical_high:
                flag = LabResultFlag.CRITICAL_HIGH
            elif catalog_test.critical_low and val <= catalog_test.critical_low:
                flag = LabResultFlag.CRITICAL_LOW
            elif catalog_test.reference_range_high and val > catalog_test.reference_range_high:
                flag = LabResultFlag.HIGH
            elif catalog_test.reference_range_low and val < catalog_test.reference_range_low:
                flag = LabResultFlag.LOW

        result = LabResult(
            lab_order_id=result_in.lab_order_id,
            test_id=result_in.test_id,
            measured_value=result_in.measured_value,
            numeric_value=result_in.numeric_value,
            flag=flag,
            technician_notes=result_in.technician_notes,
            is_verified=True,
            verified_by_id=tech_user_id,
            verified_at=datetime.utcnow()
        )
        self.db.add(result)
        
        # Update order status to COMPLETED
        order = self.lab_repo.get_by_id(result_in.lab_order_id)
        if order:
            order.status = LabOrderStatus.COMPLETED
            
        self.db.commit()
        self.db.refresh(result)
        return result
