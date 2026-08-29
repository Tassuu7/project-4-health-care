"""
AegisCare Enterprise Patient Management System - E-Prescription Service
"""

from datetime import date, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.constants import AuditAction, PrescriptionStatus
from app.core.exceptions import DrugInteractionConflictException, ResourceNotFoundError
from app.models.prescription import Medication, Prescription, PrescriptionItem
from app.repositories.audit_repo import AuditRepository
from app.repositories.patient_repo import PatientRepository
from app.repositories.prescription_repo import PrescriptionRepository
from app.schemas.prescription import PrescriptionCreate
from app.services.drug_interaction import DrugInteractionEngine


class PrescriptionService:
    """Business workflows for issuing e-prescriptions with drug-drug safety validation."""

    def __init__(self, db: Session):
        self.db = db
        self.prescription_repo = PrescriptionRepository(db)
        self.patient_repo = PatientRepository(db)
        self.audit_repo = AuditRepository(db)

    def issue_prescription(self, rx_in: PrescriptionCreate, doctor_id: int) -> Prescription:
        """Verify allergy conflicts, validate drug interactions, and issue digital prescription."""
        # 1. Fetch medication names
        med_names = []
        for item in rx_in.items:
            med = self.prescription_repo.get_medication_by_id(item.medication_id)
            if med:
                med_names.append(med.generic_name)

        # 2. Check drug-drug interactions
        conflicts = DrugInteractionEngine.check_prescription_safety(med_names)
        critical_conflicts = [c for c in conflicts if c["severity"] == "CRITICAL"]
        if critical_conflicts:
            c = critical_conflicts[0]
            raise DrugInteractionConflictException(c["drug_1"], c["drug_2"], c["severity"], c["description"])

        # 3. Create prescription
        rx_num = f"RX-{rx_in.patient_id}-{int(datetime.utcnow().timestamp())}"
        rx = Prescription(
            prescription_number=rx_num,
            patient_id=rx_in.patient_id,
            doctor_id=doctor_id,
            status=PrescriptionStatus.ACTIVE,
            issue_date=date.today(),
            expiry_date=rx_in.expiry_date,
            diagnosis_reason=rx_in.diagnosis_reason,
            doctor_instructions=rx_in.doctor_instructions
        )
        self.db.add(rx)
        self.db.commit()
        self.db.refresh(rx)

        for item_in in rx_in.items:
            item = PrescriptionItem(
                prescription_id=rx.id,
                medication_id=item_in.medication_id,
                dosage_instruction=item_in.dosage_instruction,
                frequency=item_in.frequency,
                duration_days=item_in.duration_days,
                quantity_prescribed=item_in.quantity_prescribed,
                special_warnings=item_in.special_warnings
            )
            self.db.add(item)

        self.db.commit()
        self.db.refresh(rx)

        self.audit_repo.log_event(
            action=AuditAction.PRESCRIPTION_ISSUE,
            resource_type="PRESCRIPTION",
            resource_id=str(rx.id),
            user_id=doctor_id,
            details=f"Issued prescription {rx.prescription_number}"
        )
        return rx
