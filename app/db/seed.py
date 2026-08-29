"""
AegisCare Enterprise Patient Management System - Clinical Database Seed Engine
Populates embedded SQLite database with realistic departments, staff, 100+ patients,
vital signs, triage queues, appointments, e-prescriptions, lab tests, and invoices.
"""

import random
from datetime import date, datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.core.constants import (
    AppointmentStatus, AppointmentType, AuditAction, BedStatus, BloodGroup,
    Gender, LabOrderStatus, LabResultFlag, PaymentMethod, PrescriptionStatus,
    TriageLevel, UserRole, WardType
)
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models import (
    Allergy, Appointment, AuditLog, Bed, BedAllocation, ClinicRoom,
    Department, Doctor, DoctorSchedule, EmergencyContact, FeeSchedule,
    InsurancePolicy, Invoice, InvoiceItem, LabOrder, LabResult,
    LabTestCatalog, MedicalHistory, MedicalRecord, Medication,
    Payment, Patient, Prescription, PrescriptionItem, Room,
    Specialization, SpecimenSample, TriageAssessment, User, UserProfile,
    VitalSign, Ward
)


def seed_database():
    """Execute complete database seeding with clinical datasets."""
    db: Session = SessionLocal()
    try:
        # 1. Check if database is already seeded
        if db.query(Department).count() > 0 or db.query(User).count() > 0:
            print("[*] Database already contains records. Skipping seed.")
            return

        print("[*] Seeding System Departments & Specializations...")
        depts = [
            Department(code="EMERG-01", name="Emergency Medicine", description="24/7 Acute Trauma & Resuscitation", emergency_capable=True),
            Department(code="CARD-01", name="Cardiology", description="Heart, Vascular & Coronary Care"),
            Department(code="PED-01", name="Pediatrics", description="Infant, Child & Adolescent Healthcare"),
            Department(code="ORTHO-01", name="Orthopedics", description="Musculoskeletal & Joint Reconstruction"),
            Department(code="NEURO-01", name="Neurology", description="Brain, Spine & Nervous System"),
            Department(code="SURG-01", name="General Surgery", description="Minimally Invasive & Open Surgical Unit"),
            Department(code="ONCOL-01", name="Oncology", description="Medical & Hematological Oncology"),
            Department(code="NEPH-01", name="Nephrology", description="Renal Care & Dialysis Unit"),
            Department(code="GASTRO-01", name="Gastroenterology", description="Digestive Health & Endoscopy"),
            Department(code="DERM-01", name="Dermatology", description="Skin & Cutaneous Health")
        ]
        db.add_all(depts)
        db.commit()

        specs = [
            Specialization(code="CARD", name="Cardiology"),
            Specialization(code="EMERG", name="Emergency Medicine"),
            Specialization(code="PED", name="Pediatrics"),
            Specialization(code="ORTHO", name="Orthopedics"),
            Specialization(code="NEURO", name="Neurology"),
            Specialization(code="GENSURG", name="General Surgery"),
            Specialization(code="INTMED", name="Internal Medicine")
        ]
        db.add_all(specs)
        db.commit()

        print("[*] Seeding Hospital Inpatient Wards & Beds...")
        wards = [
            Ward(name="ICU Alpha", ward_type=WardType.ICU_INTENSIVE_CARE, department_id=depts[0].id, floor_number=2, total_capacity=10, daily_rate=1200.00),
            Ward(name="Coronary Care Unit", ward_type=WardType.CCU_CORONARY_CARE, department_id=depts[1].id, floor_number=3, total_capacity=8, daily_rate=950.00),
            Ward(name="General Medical Male", ward_type=WardType.GENERAL_MALE, department_id=depts[1].id, floor_number=4, total_capacity=15, daily_rate=350.00),
            Ward(name="General Medical Female", ward_type=WardType.GENERAL_FEMALE, department_id=depts[2].id, floor_number=4, total_capacity=15, daily_rate=350.00),
            Ward(name="Pediatric Ward", ward_type=WardType.PEDIATRIC, department_id=depts[2].id, floor_number=5, total_capacity=12, daily_rate=400.00),
            Ward(name="Post-Op Recovery", ward_type=WardType.SURGICAL_POST_OP, department_id=depts[5].id, floor_number=3, total_capacity=10, daily_rate=600.00),
        ]
        db.add_all(wards)
        db.commit()

        for ward in wards:
            for r_idx in range(1, 4):
                room = Room(ward_id=ward.id, room_number=f"W{ward.id}-F{ward.floor_number}-R{r_idx}")
                db.add(room)
                db.commit()
                for b_idx in range(1, 4):
                    status = BedStatus.AVAILABLE if (r_idx + b_idx) % 3 != 0 else BedStatus.OCCUPIED
                    bed = Bed(
                        room_id=room.id,
                        bed_identifier=f"BED-W{ward.id}-R{r_idx}-B{b_idx}",
                        status=status,
                        is_ventilator_equipped=(ward.ward_type == WardType.ICU_INTENSIVE_CARE)
                    )
                    db.add(bed)
        db.commit()

        print("[*] Seeding Diagnostic Laboratory Test Catalog...")
        lab_tests = [
            LabTestCatalog(test_code="CBC-01", name="Complete Blood Count (CBC)", category="HEMATOLOGY", standard_unit="K/uL", reference_range_low=4.5, reference_range_high=11.0, critical_low=2.0, critical_high=30.0, standard_fee=45.00),
            LabTestCatalog(test_code="BMP-01", name="Basic Metabolic Panel", category="BIOCHEMISTRY", standard_unit="mg/dL", reference_range_low=70.0, reference_range_high=99.0, critical_low=50.0, critical_high=400.0, standard_fee=55.00),
            LabTestCatalog(test_code="LIPID-01", name="Lipid Profile Panel", category="BIOCHEMISTRY", standard_unit="mg/dL", reference_range_low=0.0, reference_range_high=200.0, critical_high=350.0, standard_fee=65.00),
            LabTestCatalog(test_code="TROP-I", name="High-Sensitivity Troponin I", category="CARDIOLOGY", standard_unit="ng/mL", reference_range_low=0.0, reference_range_high=0.04, critical_high=0.10, standard_fee=85.00),
            LabTestCatalog(test_code="A1C-01", name="Hemoglobin A1c", category="ENDOCRINOLOGY", standard_unit="%", reference_range_low=4.0, reference_range_high=5.6, critical_high=10.0, standard_fee=50.00),
            LabTestCatalog(test_code="TSH-01", name="Thyroid Stimulating Hormone", category="ENDOCRINOLOGY", standard_unit="uIU/mL", reference_range_low=0.4, reference_range_high=4.0, critical_low=0.1, critical_high=10.0, standard_fee=60.00),
            LabTestCatalog(test_code="CREAT-01", name="Serum Creatinine", category="NEPHROLOGY", standard_unit="mg/dL", reference_range_low=0.7, reference_range_high=1.3, critical_high=4.0, standard_fee=40.00),
            LabTestCatalog(test_code="CRP-01", name="C-Reactive Protein (CRP)", category="IMMUNOLOGY", standard_unit="mg/L", reference_range_low=0.0, reference_range_high=3.0, critical_high=100.0, standard_fee=45.00),
        ]
        db.add_all(lab_tests)
        db.commit()

        print("[*] Seeding Formulary Medications...")
        meds = [
            Medication(drug_code="NDC-001", brand_name="Amoxil", generic_name="Amoxicillin", dosage_form="CAPSULE", strength="500mg", unit_price=12.50, current_stock_quantity=800),
            Medication(drug_code="NDC-002", brand_name="Zithromax", generic_name="Azithromycin", dosage_form="TABLET", strength="250mg", unit_price=24.00, current_stock_quantity=450),
            Medication(drug_code="NDC-003", brand_name="Prinivil", generic_name="Lisinopril", dosage_form="TABLET", strength="10mg", unit_price=8.00, current_stock_quantity=1200),
            Medication(drug_code="NDC-004", brand_name="Lipitor", generic_name="Atorvastatin", dosage_form="TABLET", strength="20mg", unit_price=18.00, current_stock_quantity=950),
            Medication(drug_code="NDC-005", brand_name="Glucophage", generic_name="Metformin", dosage_form="TABLET", strength="500mg", unit_price=10.00, current_stock_quantity=1500),
            Medication(drug_code="NDC-006", brand_name="Norvasc", generic_name="Amlodipine", dosage_form="TABLET", strength="5mg", unit_price=9.50, current_stock_quantity=600),
            Medication(drug_code="NDC-007", brand_name="Ventolin", generic_name="Salbutamol", dosage_form="INHALER", strength="100mcg", unit_price=35.00, current_stock_quantity=300),
            Medication(drug_code="NDC-008", brand_name="Coumadin", generic_name="Warfarin", dosage_form="TABLET", strength="5mg", unit_price=15.00, current_stock_quantity=400),
            Medication(drug_code="NDC-009", brand_name="Bayer Aspirin", generic_name="Aspirin", dosage_form="TABLET", strength="81mg", unit_price=5.00, current_stock_quantity=2000),
            Medication(drug_code="NDC-010", brand_name="Advil", generic_name="Ibuprofen", dosage_form="TABLET", strength="400mg", unit_price=7.50, current_stock_quantity=1800),
            Medication(drug_code="NDC-011", brand_name="Tylenol", generic_name="Paracetamol", dosage_form="TABLET", strength="500mg", unit_price=6.00, current_stock_quantity=2500),
            Medication(drug_code="NDC-012", brand_name="Prilosec", generic_name="Omeprazole", dosage_form="CAPSULE", strength="20mg", unit_price=14.00, current_stock_quantity=700),
        ]
        db.add_all(meds)
        db.commit()

        print("[*] Seeding Staff & User Accounts...")
        users = [
            User(username="admin", email="admin@aegiscarehealth.com", hashed_password=hash_password("Admin@123"), role=UserRole.ADMIN, first_name="Alexander", last_name="Hamilton", phone_number="(555) 019-2831", is_active=True, is_verified=True),
            User(username="dr.smith", email="dr.smith@aegiscarehealth.com", hashed_password=hash_password("Doctor@123"), role=UserRole.DOCTOR, first_name="Marcus", last_name="Vance", phone_number="(555) 019-3829", is_active=True, is_verified=True),
            User(username="nurse.clara", email="nurse.clara@aegiscarehealth.com", hashed_password=hash_password("Nurse@123"), role=UserRole.TRIAGE_NURSE, first_name="Clara", last_name="Barton", phone_number="(555) 019-4819", is_active=True, is_verified=True),
            User(username="patient.john", email="patient.john@example.com", hashed_password=hash_password("Patient@123"), role=UserRole.PATIENT, first_name="John", last_name="Doe", phone_number="(555) 019-5820", is_active=True, is_verified=True),
            User(username="pharma.elena", email="pharma.elena@aegiscarehealth.com", hashed_password=hash_password("Pharma@123"), role=UserRole.PHARMACIST, first_name="Elena", last_name="Rostova", phone_number="(555) 019-6721", is_active=True, is_verified=True),
            User(username="lab.david", email="lab.david@aegiscarehealth.com", hashed_password=hash_password("Lab@123"), role=UserRole.LAB_TECHNICIAN, first_name="David", last_name="Kovacs", phone_number="(555) 019-7612", is_active=True, is_verified=True),
            User(username="billing.sarah", email="billing.sarah@aegiscarehealth.com", hashed_password=hash_password("Billing@123"), role=UserRole.BILLING_OFFICER, first_name="Sarah", last_name="Jenkins", phone_number="(555) 019-8901", is_active=True, is_verified=True),
        ]
        db.add_all(users)
        db.commit()

        # Doctor profile
        doc = Doctor(
            user_id=users[1].id,
            department_id=depts[1].id,
            specialization_id=specs[0].id,
            medical_license_number="MD-NY-2018-9842",
            qualification="MD, FACC (Harvard Medical)",
            years_of_experience=14,
            consultation_fee=185.00
        )
        db.add(doc)
        db.commit()

        # Doctor weekly schedule
        for day in range(5):
            sched = DoctorSchedule(
                doctor_id=doc.id,
                day_of_week=day,
                start_time=datetime.strptime("09:00", "%H:%M").time(),
                end_time=datetime.strptime("17:00", "%H:%M").time()
            )
            db.add(sched)
        db.commit()

        print("[*] Seeding 100+ Realistic Patients with Demographics...")
        first_names = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda", "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
        
        patients_list = []
        # First patient linked to patient.john user
        p_primary = Patient(
            user_id=users[3].id,
            mrn="MRN-2026-0001",
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1985, 4, 12),
            gender=Gender.MALE,
            blood_group=BloodGroup.O_POSITIVE,
            phone_number="(555) 019-5820",
            email="patient.john@example.com",
            address_street="742 Evergreen Terrace",
            address_city="Springfield",
            address_state="OR",
            address_postal_code="97477"
        )
        patients_list.append(p_primary)

        for i in range(2, 105):
            fn = random.choice(first_names)
            ln = random.choice(last_names)
            bg = random.choice(list(BloodGroup))
            gen = Gender.MALE if fn in ["James", "Robert", "John", "Michael", "David", "William", "Richard", "Joseph", "Thomas", "Charles"] else Gender.FEMALE
            birth_year = random.randint(1945, 2015)
            
            p = Patient(
                mrn=f"MRN-2026-{i:04d}",
                first_name=fn,
                last_name=ln,
                date_of_birth=date(birth_year, random.randint(1, 12), random.randint(1, 28)),
                gender=gen,
                blood_group=bg,
                phone_number=f"(555) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                email=f"{fn.lower()}.{ln.lower()}{i}@example.com",
                address_street=f"{random.randint(100, 999)} Maple Ave",
                address_city="Metropolis",
                address_state="NY",
                address_postal_code="10001"
            )
            patients_list.append(p)

        db.add_all(patients_list)
        db.commit()

        print("[*] Seeding Patient Allergies & Emergency Contacts...")
        for p in patients_list[:25]:
            ec = EmergencyContact(
                patient_id=p.id,
                name=f"{p.last_name} Guardian",
                relationship_to_patient="SPOUSE",
                phone_number="(555) 999-0000"
            )
            db.add(ec)
            if p.id % 2 == 0:
                al = Allergy(
                    patient_id=p.id,
                    allergen="Penicillin",
                    allergy_type="DRUG",
                    severity="SEVERE",
                    reaction_description="Cutaneous urticaria and mild wheezing"
                )
                db.add(al)
        db.commit()

        print("[*] Seeding Physiological Vital Signs Timeseries...")
        for p in patients_list[:30]:
            for v_idx in range(3):
                t_offset = datetime.now(timezone.utc) - timedelta(days=v_idx * 7)
                v = VitalSign(
                    patient_id=p.id,
                    recorded_at=t_offset,
                    systolic_bp=random.randint(110, 145),
                    diastolic_bp=random.randint(70, 90),
                    heart_rate=random.randint(62, 88),
                    respiratory_rate=random.randint(12, 18),
                    temperature_celsius=round(random.uniform(36.5, 37.4), 1),
                    oxygen_saturation=round(random.uniform(96.0, 99.5), 1),
                    pain_score=random.randint(0, 3)
                )
                db.add(v)
        db.commit()

        print("[*] Seeding Clinical Appointments & Encounters...")
        for idx, p in enumerate(patients_list[:20]):
            appt_time = datetime.now(timezone.utc) + timedelta(hours=idx + 1)
            appt = Appointment(
                appointment_number=f"APT-2026-{idx+1:04d}",
                patient_id=p.id,
                doctor_id=doc.id,
                department_id=depts[1].id,
                appointment_type=AppointmentType.ROUTINE_CHECKUP,
                status=AppointmentStatus.SCHEDULED if idx > 3 else AppointmentStatus.COMPLETED,
                start_time=appt_time,
                end_time=appt_time + timedelta(minutes=30),
                chief_complaint=f"Routine clinical checkup and blood pressure monitoring for {p.full_name}"
            )
            db.add(appt)
        db.commit()

        print("[*] Seeding Emergency Triage Assessments...")
        for idx, p in enumerate(patients_list[20:30]):
            esi = (idx % 4) + 2 # ESI 2, 3, 4, 5
            triage = TriageAssessment(
                triage_number=f"TRG-2026-{idx+1:04d}",
                patient_id=p.id,
                nurse_id=users[2].id,
                triage_level=TriageLevel(esi),
                chief_complaint="Chest pressure with moderate shortness of breath upon exertion",
                pain_score=random.randint(4, 8),
                heart_rate=random.randint(75, 110),
                systolic_bp=random.randint(120, 160),
                oxygen_saturation=round(random.uniform(94.0, 98.0), 1),
                assigned_zone="ORANGE_ACUTE_CARE" if esi <= 2 else "YELLOW_URGENT_CARE",
                is_active=True
            )
            db.add(triage)
        db.commit()

        print("[*] Seeding Invoices & Payments...")
        for idx, p in enumerate(patients_list[:15]):
            inv = Invoice(
                invoice_number=f"INV-2026-{idx+1:04d}",
                patient_id=p.id,
                issue_date=date.today() - timedelta(days=idx*3),
                due_date=date.today() + timedelta(days=30),
                subtotal_amount=200.00,
                tax_amount=10.00,
                total_amount=210.00,
                paid_amount=210.00 if idx % 2 == 0 else 0.00,
                balance_due=0.00 if idx % 2 == 0 else 210.00
            )
            db.add(inv)
            db.commit()
            
            item = InvoiceItem(
                invoice_id=inv.id,
                item_description="Cardiology Consultation & Diagnostic ECG",
                quantity=1,
                unit_price=200.00,
                total_price=200.00
            )
            db.add(item)
        db.commit()

        print("[*] Seeding HIPAA Security Audit Logs...")
        for idx in range(25):
            log = AuditLog(
                timestamp=datetime.now(timezone.utc) - timedelta(minutes=idx * 15),
                user_id=users[1].id,
                username="dr.smith",
                user_role="DOCTOR",
                action=AuditAction.PATIENT_VIEW,
                resource_type="PATIENT",
                resource_id=str((idx % 10) + 1),
                ip_address="192.168.1.45",
                details="Physician accessed patient electronic health record"
            )
            db.add(log)
        db.commit()

        print("[+] Clinical Database Seed Finished Successfully!")

    except Exception as e:
        db.rollback()
        print(f"[!] Error seeding database: {e}")
    finally:
        db.close()
