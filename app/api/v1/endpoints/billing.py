"""
AegisCare Enterprise Patient Management System - Billing API Router
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.billing import InvoiceCreate, InvoiceResponse, PaymentCreate, PaymentResponse
from app.schemas.common import ResponseEnvelope
from app.services.billing_service import BillingService

router = APIRouter(prefix="/billing", tags=["Billing & Invoicing"])


@router.post("/invoices", response_model=ResponseEnvelope[InvoiceResponse], status_code=status.HTTP_201_CREATED)
def create_invoice(invoice_in: InvoiceCreate, db: Session = Depends(get_db)):
    """Create itemized patient bill with taxes and discounts."""
    service = BillingService(db)
    invoice = service.create_invoice(invoice_in)
    return ResponseEnvelope(data=InvoiceResponse.model_validate(invoice), message="Invoice issued")


@router.post("/payments", response_model=ResponseEnvelope[PaymentResponse])
def submit_payment(payment_in: PaymentCreate, db: Session = Depends(get_db)):
    """Record payment receipt and settle invoice balance."""
    service = BillingService(db)
    payment = service.process_payment(payment_in)
    return ResponseEnvelope(data=PaymentResponse.model_validate(payment), message="Payment successful")


@router.get("/patient/{patient_id}", response_model=ResponseEnvelope[List[InvoiceResponse]])
def get_patient_invoices(patient_id: int, db: Session = Depends(get_db)):
    """List billing invoices for a specific patient."""
    service = BillingService(db)
    invoices = service.billing_repo.get_patient_invoices(patient_id)
    return ResponseEnvelope(data=[InvoiceResponse.model_validate(i) for i in invoices])
