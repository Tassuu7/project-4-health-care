#!/usr/bin/env python3
"""
AegisCare Enterprise Patient Management System
Application Launcher and Server Runner
"""

import os
import sys
import uvicorn

# Add workspace directory to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app.config import get_settings
from app.db.session import init_db
from app.db.seed import seed_database

def main():
    """Initialize database, seed sample healthcare records, and run ASGI server."""
    settings = get_settings()
    print("=" * 72)
    print(f"  {settings.APP_NAME}")
    print(f"  Version: {settings.APP_VERSION} | Environment: {settings.APP_ENV}")
    print(f"  Healthcare Compliance: HIPAA Audit Enabled | RBAC: Active")
    print("=" * 72)
    
    print("[*] Initializing Database Schema...")
    init_db()
    print("[*] Seeding Clinical Demo Data (Doctors, Patients, Appointments, Vitals, Invoices)...")
    seed_database()
    
    print(f"[*] Starting Application Server on http://{settings.APP_HOST}:{settings.APP_PORT}")
    print(f"[*] Access Clinical Portal: http://localhost:{settings.APP_PORT}")
    print(f"[*] Default Physician:    dr.smith / Doctor@123")
    print(f"[*] Default Nurse:        nurse.clara / Nurse@123")
    print(f"[*] Default Admin:        admin / Admin@123")
    print(f"[*] Default Patient:      patient.john / Patient@123")
    print("=" * 72)

    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
        log_level="info"
    )

if __name__ == "__main__":
    main()
