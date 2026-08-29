# AegisCare Enterprise Patient Management Platform
=====================================================

[![Architecture: Layered Clean Enterprise](https://img.shields.io/badge/Architecture-Clean%20Enterprise-blue.svg)](#architecture)
[![License: Proprietary Commercial](https://img.shields.io/badge/License-Proprietary%20AegisCare-red.svg)](#license)
[![HIPAA Compliance](https://img.shields.io/badge/Compliance-HIPAA%20Audit%20Ready-green.svg)](#compliance)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#requirements)

**AegisCare** is an enterprise-grade Clinical and Patient Management Platform architected for acute hospitals, multi-specialty healthcare systems, outpatient polyclinics, and diagnostic medical centers.

---

## 1. System Architecture

AegisCare strictly enforces a four-tier enterprise architecture:

```
+-------------------------------------------------------------------------+
|                  Modern Responsive Web Client (HTML5 / CSS3 / ES6+)     |
|   Physician Workbench | Nurse Triage Station | Patient Portal | Admin   |
+-------------------------------------------------------------------------+
                                    |  (REST API & HTTP JSON)
                                    v
+-------------------------------------------------------------------------+
|                 FastAPI Application Controllers & Routers               |
|      RBAC Middleware | HIPAA Audit Interceptor | Security Headers       |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                        Domain Business Services Layer                   |
|  - ESI 5-Level Triage Decision Engine                                    |
|  - Drug-Drug Interaction Cross-Reference Engine                         |
|  - Inpatient Bed Allocation & Ward Matrix Manager                       |
|  - Itemized Billing & Tax Calculator                                    |
|  - HL7 FHIR R4 Interoperability Converters                              |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                       Repository & Data Access Layer                    |
|       Generic Repository Pattern | Eager Loading | Dynamic Filters      |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                     Relational Storage (SQLAlchemy 2.0 ORM)             |
|   Embedded SQLite (Zero-config) / Enterprise PostgreSQL Supported       |
+-------------------------------------------------------------------------+
```

---

## 2. Core Functional Modules

1. **Role-Based Access Control (RBAC)**:
   - 13 distinct healthcare roles (`ADMIN`, `CHIEF_MEDICAL_OFFICER`, `DOCTOR`, `SPECIALIST`, `HEAD_NURSE`, `TRIAGE_NURSE`, `STAFF_NURSE`, `PHARMACIST`, `LAB_TECHNICIAN`, `BILLING_OFFICER`, `RECEPTIONIST`, `PATIENT`, `AUDITOR`).
   - Granular permission matrix safeguarding Protected Health Information (PHI).

2. **Emergency Severity Index (ESI) Triage Engine**:
   - Implements authentic ESI Version 4 algorithm (Levels 1 to 5).
   - Automated danger vital signs threshold triggers with immediate acuity upgrade.

3. **Clinical Electronic Health Records (EHR)**:
   - Longitudinal vital signs timeseries graphing (BP, Heart Rate, SpO2, Temp).
   - ICD-10-CM international classification catalogue integration with search.
   - Doctor consultation notes and diagnostic plans.

4. **Pharmacy & Medication Safety Engine**:
   - Formulary drug catalogue with dosage guidelines and monographs.
   - Real-time contraindication detection for critical drug-drug combinations.

5. **Diagnostic Laboratory Management**:
   - Standardized test catalogue (Hematology, Biochemistry, Immunology).
   - Critical value alerts and automated normal reference range evaluation.

6. **Inpatient Ward & Bed Management**:
   - Ward capacity monitoring (ICU, CCU, General Wards, Isolation).
   - Real-time bed occupancy, cleaning turnover, and patient transfers.

7. **Financial Ledger & Billing**:
   - Itemized invoicing with healthcare taxes and discounts.
   - Payment settlement tracking and insurance claim submissions.

8. **HL7 / FHIR R4 Interoperability**:
   - Export internal patient and observation models as FHIR R4 resources.

---

## 3. Quick Start & Installation

### Prerequisites
- Python 3.10 or higher
- Git

### Installation Steps

1. **Clone or Navigate to Repository**:
   ```bash
   cd "C:\Users\shaik\OneDrive\Desktop\project-4-Health Care"
   ```

2. **Install Locked Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Application**:
   - On Windows: Double click `start.bat` or run `powershell ./start.ps1`
   - Or directly via Python:
     ```bash
     python run.py
     ```

4. **Open in Web Browser**:
   - **Clinical Portal**: [http://localhost:8000](http://localhost:8000)
   - **Interactive API Documentation (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 4. Default Demo Role Credentials

The system includes pre-seeded realistic clinical demo data with instant 1-click login buttons on the `/login` page:

| Role | Username | Password | Direct Portal |
| :--- | :--- | :--- | :--- |
| **Doctor** | `dr.smith` | `Doctor@123` | `/doctor-dashboard` |
| **Nurse** | `nurse.clara` | `Nurse@123` | `/nurse-station` |
| **Patient** | `patient.john` | `Patient@123` | `/patient-portal` |
| **Admin** | `admin` | `Admin@123` | `/admin-console` |
| **Pharmacist** | `pharma.elena` | `Pharma@123` | `/pharmacy-console` |
| **Lab Tech** | `lab.david` | `Lab@123` | `/lab-console` |
| **Billing** | `billing.sarah` | `Billing@123` | `/billing-console` |

---

## 5. Verification & Metric Audit (`measure.py`)

Run the automated TrainPlex compliance and LOC verification suite:

```bash
python measure.py
```

This analyzes:
- Production lines of code (LOC) across Python, JavaScript, CSS, HTML, and SQL.
- Validates 14/14 TrainPlex enterprise criteria.

---

## 6. Automated Testing

Execute the test suite with Pytest:

```bash
pytest tests/ -v
```

---

## 7. License

**AegisCare Proprietary Commercial Healthcare License**
Copyright (c) 2026 AegisCare Health Technologies, Inc. All Rights Reserved.
This product is NOT licensed under open source terms (No GPL, Apache, or MIT).
