# AegisCare Enterprise Patient Management Platform

AegisCare is a comprehensive Clinical and Patient Management Platform architected for multi-specialty hospitals, emergency triage centers, diagnostic clinics, and inpatient healthcare facilities.

---

## 1. System Architecture

The platform follows a clean four-tier enterprise architecture:

- **Presentation Layer**: Responsive HTML5, CSS3 Custom Properties, and modular JavaScript (ES6+) clinical portals.
- **Application Controller Layer**: FastAPI REST API endpoints, RBAC permission enforcement, and HIPAA audit interceptors.
- **Domain Services Layer**: Clinical Decision Support, Emergency Severity Index (ESI) triage scoring, drug-drug safety cross-reference, inpatient bed allocation matrix, and HL7 FHIR R4 serializers.
- **Data Access & Storage Layer**: Generic repository pattern backed by SQLAlchemy 2.0 ORM and SQLite/PostgreSQL.

---

## 2. Installation

### Prerequisites
- Python 3.10 or higher
- Git

### Steps
1. Navigate to the project root directory:
   ```bash
   cd "C:\Users\shaik\OneDrive\Desktop\project-4-Health Care"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Build

Validate the project build and run the test suite:

```bash
# Using Makefile
make build

# Or using Pytest
pytest tests/ -v
```

---

## 4. Run

Start the AegisCare application server:

```bash
# Direct Python launcher
python main.py

# Or using launcher scripts
start.bat        # Windows Batch
powershell ./start.ps1  # PowerShell
make run         # Linux / macOS Makefile
```

### Access URLs
- **Web Interface**: [http://localhost:8888](http://localhost:8888)
- **Clinical Dashboard**: [http://localhost:8888/doctor-dashboard](http://localhost:8888/doctor-dashboard)
- **Patient Portal**: [http://localhost:8888/patient-portal](http://localhost:8888/patient-portal)

---

## 5. Testing

Execute the automated test suite covering authentication, triage calculations, drug safety, billing calculations, and FHIR resource conversion:

```bash
pytest tests/ -v
```

---

## 6. Default Demo Credentials

One-click quick login buttons are available on the `/login` page:

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Doctor** | `dr.smith` | `Doctor@123` | Physician workbench, patient queue, vitals charting |
| **Nurse** | `nurse.clara` | `Nurse@123` | Emergency triage intake, ESI calculator, bed matrix |
| **Patient** | `patient.john` | `Patient@123` | Appointment booking, prescriptions, billing |
| **Admin** | `admin` | `Admin@123` | Executive revenue KPIs, user RBAC, HIPAA audit logs |
| **Pharmacist** | `pharma.elena` | `Pharma@123` | Formulary inventory, drug-drug safety checker |
| **Lab Tech** | `lab.david` | `Lab@123` | Diagnostic lab queue, result entry |
| **Billing** | `billing.sarah` | `Billing@123` | Invoicing, ledger, payment receipts |

---

## 7. TrainPlex Code Metrics

Run the integrated verification tool:

```bash
python measure.py
```

---

## 8. License

PROPRIETARY COMMERCIAL LICENSE  
Copyright (c) 2026 AegisCare Health Technologies, Inc. All Rights Reserved.  
Commercial deployment requires an authorized enterprise license agreement.
