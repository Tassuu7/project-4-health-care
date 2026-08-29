"""
AegisCare Enterprise Patient Management System - Billing & Invoicing Service
"""

import random
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.constants import AuditAction, InvoiceStatus, PaymentMethod
from app.models.billing import Invoice, InvoiceItem, Payment
from app.repositories.audit_repo import AuditRepository
from app.repositories.billing_repo import BillingRepository
from app.schemas.billing import InvoiceCreate, PaymentCreate


class BillingService:
    """Financial calculations, itemized billing, copays, and payment receipts."""

    def __init__(self, db: Session):
        self.db = db
        self.billing_repo = BillingRepository(db)
        self.audit_repo = AuditRepository(db)

    def create_invoice(self, invoice_in: InvoiceCreate, actor_user_id: Optional[int] = None) -> Invoice:
        """Calculate subtotal, taxes, discounts, and issue hospital patient invoice."""
        subtotal = sum(item.unit_price * item.quantity for item in invoice_in.items)
        tax = subtotal * 0.05 # 5% healthcare service tax
        total = subtotal + tax - invoice_in.discount_amount
        
        inv_num = f"INV-{int(datetime.utcnow().timestamp())}-{random.randint(10, 99)}"
        invoice = Invoice(
            invoice_number=inv_num,
            patient_id=invoice_in.patient_id,
            status=InvoiceStatus.ISSUED,
            issue_date=date.today(),
            due_date=invoice_in.due_date,
            subtotal_amount=subtotal,
            discount_amount=invoice_in.discount_amount,
            tax_amount=tax,
            total_amount=total,
            paid_amount=0.00,
            balance_due=total,
            notes=invoice_in.notes
        )
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)

        for item_in in invoice_in.items:
            item = InvoiceItem(
                invoice_id=invoice.id,
                item_description=item_in.item_description,
                service_code=item_in.service_code,
                quantity=item_in.quantity,
                unit_price=item_in.unit_price,
                total_price=item_in.unit_price * item_in.quantity
            )
            self.db.add(item)

        self.db.commit()
        self.db.refresh(invoice)

        self.audit_repo.log_event(
            action=AuditAction.INVOICE_CREATE,
            resource_type="INVOICE",
            resource_id=str(invoice.id),
            user_id=actor_user_id,
            details=f"Generated invoice {invoice.invoice_number} totaling ${total:.2f}"
        )
        return invoice

    def process_payment(self, payment_in: PaymentCreate, actor_user_id: Optional[int] = None) -> Payment:
        """Record patient payment settlement and adjust remaining invoice balance."""
        invoice = self.billing_repo.get_by_id(payment_in.invoice_id)
        if not invoice:
            raise ResourceNotFoundError("Invoice", payment_in.invoice_id)

        receipt_num = f"RCP-{int(datetime.utcnow().timestamp())}"
        payment = Payment(
            receipt_number=receipt_num,
            invoice_id=invoice.id,
            payment_method=payment_in.payment_method,
            amount_paid=payment_in.amount_paid,
            transaction_reference=payment_in.transaction_reference or f"TX-{random.randint(100000, 999999)}"
        )
        self.db.add(payment)
        
        invoice.paid_amount = float(invoice.paid_amount or 0.0) + float(payment_in.amount_paid)
        invoice.balance_due = max(0.0, float(invoice.total_amount) - float(invoice.paid_amount))
        
        if invoice.balance_due <= 0.0:
            invoice.status = InvoiceStatus.PAID
        else:
            invoice.status = InvoiceStatus.PARTIALLY_PAID
            
        self.db.commit()
        self.db.refresh(payment)

        self.audit_repo.log_event(
            action=AuditAction.PAYMENT_RECEIVE,
            resource_type="PAYMENT",
            resource_id=str(payment.id),
            user_id=actor_user_id,
            details=f"Received payment ${payment.amount_paid:.2f} for Invoice {invoice.invoice_number}"
        )
        return payment
