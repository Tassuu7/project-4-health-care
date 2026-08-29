"""
Unit Tests for Invoicing, Hospital Tax Calculations, and Payment Settlements
"""

import pytest
from datetime import date
from app.models.patient import Patient
from app.core.constants import Gender, BloodGroup
from app.schemas.billing import InvoiceCreate, InvoiceItemSchema, PaymentCreate
from app.services.billing_service import BillingService


def test_invoice_creation_and_payment(db_session):
    """Test calculation of line items, 5% healthcare tax, and payment balance."""
    # Create patient
    p = Patient(
        mrn="MRN-TEST-01",
        first_name="Alice",
        last_name="Smith",
        date_of_birth=date(1990, 1, 1),
        gender=Gender.FEMALE,
        blood_group=BloodGroup.A_POSITIVE,
        phone_number="555-0192"
    )
    db_session.add(p)
    db_session.commit()

    service = BillingService(db_session)
    inv_in = InvoiceCreate(
        patient_id=p.id,
        due_date=date(2026, 10, 1),
        items=[
            InvoiceItemSchema(item_description="Cardiology Consult", unit_price=100.0, total_price=100.0),
            InvoiceItemSchema(item_description="Diagnostic ECG", unit_price=100.0, total_price=100.0)
        ],
        discount_amount=0.0
    )
    invoice = service.create_invoice(inv_in)
    
    # Subtotal 200 + 5% tax (10) = 210
    assert float(invoice.subtotal_amount) == 200.0
    assert float(invoice.tax_amount) == 10.0
    assert float(invoice.total_amount) == 210.0
    assert float(invoice.balance_due) == 210.0

    # Pay full amount
    payment = service.process_payment(PaymentCreate(invoice_id=invoice.id, amount_paid=210.0))
    assert payment.id is not None
    assert float(invoice.paid_amount) == 210.0
    assert float(invoice.balance_due) == 0.0
    assert invoice.status.value == "PAID"
