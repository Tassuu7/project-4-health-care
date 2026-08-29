"""
AegisCare Enterprise Patient Management System - Billing & Financial Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.billing import FeeSchedule, InsuranceClaim, Invoice, Payment
from app.repositories.base import BaseRepository


class BillingRepository(BaseRepository[Invoice]):
    """Data access repository for Patient Invoices, Payments, and Insurance Claims."""

    def __init__(self, db: Session):
        super().__init__(Invoice, db)

    def get_with_items_and_payments(self, invoice_id: int) -> Optional[Invoice]:
        """Fetch invoice with line items, payments, and patient demographics."""
        return self.db.query(Invoice).options(
            joinedload(Invoice.items),
            joinedload(Invoice.payments),
            joinedload(Invoice.patient)
        ).filter(
            Invoice.id == invoice_id,
            Invoice.is_deleted == False
        ).first()

    def get_patient_invoices(self, patient_id: int) -> List[Invoice]:
        """List all invoices issued to a patient."""
        return self.db.query(Invoice).options(
            joinedload(Invoice.items),
            joinedload(Invoice.payments)
        ).filter(
            Invoice.patient_id == patient_id,
            Invoice.is_deleted == False
        ).order_by(Invoice.issue_date.desc()).all()

    def record_payment(self, payment: Payment) -> Payment:
        """Persist a payment transaction against an invoice."""
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
