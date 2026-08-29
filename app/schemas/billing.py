"""
AegisCare Enterprise Patient Management System - Billing & Invoicing Schemas
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.core.constants import InvoiceStatus, PaymentMethod


class InvoiceItemSchema(BaseModel):
    item_description: str
    service_code: Optional[str] = None
    quantity: int = 1
    unit_price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)


class InvoiceCreate(BaseModel):
    patient_id: int
    due_date: date
    items: List[InvoiceItemSchema]
    discount_amount: float = 0.00
    notes: Optional[str] = None


class PaymentCreate(BaseModel):
    invoice_id: int
    payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD
    amount_paid: float
    transaction_reference: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    receipt_number: str
    invoice_id: int
    payment_method: PaymentMethod
    amount_paid: float
    payment_date: datetime
    is_successful: bool

    model_config = ConfigDict(from_attributes=True)


class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    patient_id: int
    status: InvoiceStatus
    issue_date: date
    due_date: date
    subtotal_amount: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    paid_amount: float
    balance_due: float
    items: List[InvoiceItemSchema] = []
    payments: List[PaymentResponse] = []

    model_config = ConfigDict(from_attributes=True)
