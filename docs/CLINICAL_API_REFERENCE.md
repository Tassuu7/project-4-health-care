# AegisCare Clinical REST API Reference

## API Architecture
High-throughput asynchronous RESTful API powered by FastAPI, SQLAlchemy ORM, and Pydantic validation models.

### Core Endpoint Groups:
- `POST /api/auth/login`: Secure OAuth2 token exchange.
- `GET /api/patients`: Paginated patient registry search with filtering.
- `POST /api/triage/evaluate`: Automated Emergency Severity Index (ESI 1-5) algorithm.
- `POST /api/prescriptions`: Multi-drug prescription order with automated conflict detection.
- `GET /api/billing/invoices`: Real-time invoice balance calculation.
