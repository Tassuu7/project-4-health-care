#!/usr/bin/env python3
"""
AegisCare Enterprise Patient Management System
Primary Application Entry Point and Web Server Launcher
"""

import os
import sys
import uvicorn

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.config import get_settings
from app.db.session import init_db
from app.db.seed import seed_database

def start_server():
    """Initialize clinical schema, seed demo records, and start ASGI web server."""
    settings = get_settings()
    print("=" * 76)
    print(f"  {settings.APP_NAME}")
    print(f"  Version: {settings.APP_VERSION} | Environment: {settings.APP_ENV}")
    print("=" * 76)
    
    print("[*] Initializing Database...")
    init_db()
    seed_database()
    
    print(f"[*] Application Server listening on http://{settings.APP_HOST}:{settings.APP_PORT}")
    print(f"[*] Web Interface:        http://localhost:{settings.APP_PORT}")
    print("=" * 76)

    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    start_server()
