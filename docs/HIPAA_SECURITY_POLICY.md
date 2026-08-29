# AegisCare HIPAA Security & Access Control Policy

## Overview
This document defines the zero-trust security architecture, AES-256 encrypted storage standards, and JWT role-based access control (RBAC) protocols implemented within the AegisCare Enterprise Healthcare Platform.

### Security Controls:
1. **Password Hashing**: Bcrypt with salt rounds >= 12.
2. **Session Security**: Ephemeral JWT access tokens signed with HMAC-SHA256.
3. **Audit Trails**: Immutable event logs for all Protected Health Information (PHI) access events.
4. **Role Isolation**: Granular separation of duties between System Admins, Attending Physicians, Triage Nurses, and Patients.
