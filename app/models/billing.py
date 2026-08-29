"""
AegisCare Enterprise Patient Management System - Billing, Invoicing & Insurance Models
Defines hospital fee ledger, patient invoices, payments, insurance claims, and receipts.
"""

from datetime import date, datetime
from sqlalchemy import Boolean, Column, Date, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from app.core.constants import InsuranceClaimStatus, InvoiceStatus, PaymentMethod
from app.db.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin


class FeeSchedule(Base, TimestampMixin):
    """Standardized hospital charge master price list for medical services."""
    __tablename__ = "fee_schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    service_code = Column(String(32), unique=True, index=True, nullable=False)
    service_name = Column(String(128), nullable=False)
    category = Column(String(64), default="CONSULTATION", nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    tax_rate_percent = Column(Float, default=0.0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Invoice(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Itemized patient bill covering consultations, lab tests, beds, and medications."""
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    invoice_number = Column(String(32), unique=True, index=True, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    
    status = Column(SQLEnum(InvoiceStatus), default=InvoiceStatus.ISSUED, nullable=False, index=True)
    issue_date = Column(Date, default=date.today, nullable=False)
    due_date = Column(Date, nullable=False)
    
    subtotal_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    discount_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    tax_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    insurance_covered_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    total_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    paid_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    balance_due = Column(Numeric(10, 2), default=0.00, nullable=False)
    
    notes = Column(Text, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")
    insurance_claims = relationship("InsuranceClaim", back_populates="invoice")


class InvoiceItem(Base, TimestampMixin):
    """Specific line item charged on an invoice."""
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    item_description = Column(String(255), nullable=False)
    service_code = Column(String(32), nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    invoice = relationship("Invoice", back_populates="items")


class Payment(Base, TimestampMixin, AuditMixin):
    """Financial settlement transaction recorded against an invoice."""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    receipt_number = Column(String(32), unique=True, index=True, nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    
    payment_method = Column(SQLEnum(PaymentMethod), default=PaymentMethod.CREDIT_CARD, nullable=False)
    amount_paid = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    transaction_reference = Column(String(64), nullable=True)
    is_successful = Column(Boolean, default=True, nullable=False)

    invoice = relationship("Invoice", back_populates="payments")


class InsuranceClaim(Base, TimestampMixin, AuditMixin):
    """Medical insurance claim submission tracking."""
    __tablename__ = "insurance_claims"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    claim_number = Column(String(32), unique=True, index=True, nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    insurance_provider = Column(String(128), nullable=False)
    policy_number = Column(String(64), nullable=False)
    
    claimed_amount = Column(Numeric(10, 2), nullable=False)
    approved_amount = Column(Numeric(10, 2), default=0.00, nullable=False)
    status = Column(SQLEnum(InsuranceClaimStatus), default=InsuranceClaimStatus.SUBMITTED, nullable=False)
    submission_date = Column(Date, default=date.today, nullable=False)
    adjudication_date = Column(Date, nullable=True)
    rejection_reason = Column(String(255), nullable=True)

    invoice = relationship("Invoice", back_populates="insurance_claims")


class PaymentReceipt(Base, TimestampMixin):
    """Formal printable tax invoice receipt."""
    __tablename__ = "payment_receipts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    receipt_code = Column(String(32), unique=True, index=True, nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    tax_identifier = Column(String(64), default="AEGIS-TAX-2026-US", nullable=False)
    issued_by = Column(String(128), nullable=False)
