# 🏆 Phase 20 — Capstone Project

> **The Final Exam. Build a complete, production-ready application from scratch.**

---

## What You Will Build

A **Task Management & Analytics Platform** — a real-world application demonstrating every major skill from the academy.

---

## Project: TaskFlow Pro

A complete task and project management system with:

```
✅ Python Backend (OOP + Clean Architecture)
✅ SQLite Database (CRUD + Analytics queries)
✅ REST API (FastAPI)
✅ Authentication (JWT tokens)
✅ Logging (structured, rotating)
✅ Testing (pytest, 80%+ coverage)
✅ HTML Dashboard (interactive reports)
✅ Configuration (environment variables)
✅ Documentation (README + API docs)
✅ Deployment Guide
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TASKFLOW PRO                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  HTML DASHBOARD                                             │
│  ─────────────                                              │
│  Charts & Reports  →  API calls                             │
│                           │                                 │
│  FASTAPI LAYER            │                                 │
│  ───────────              ▼                                 │
│  REST Endpoints  ←  Business Logic                         │
│  JWT Auth              (Services)                           │
│                           │                                 │
│  DATA LAYER               │                                 │
│  ──────────               ▼                                 │
│  Repository Pattern  →  SQLite DB                          │
│  SQLAlchemy ORM                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
phase-20-capstone/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── src/
│   ├── main.py              ← FastAPI app entry point
│   ├── config.py            ← Settings & environment
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          ← Authentication routes
│   │   ├── tasks.py         ← Task CRUD routes
│   │   ├── projects.py      ← Project routes
│   │   └── reports.py       ← Analytics routes
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   └── jwt_handler.py   ← JWT token logic
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py    ← DB connection management
│   │   └── models.py        ← SQLAlchemy models
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── task_repo.py     ← Task data access
│   │   ├── project_repo.py
│   │   └── user_repo.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py  ← Business logic
│   │   ├── project_service.py
│   │   └── report_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py        ← Logging setup
│       └── validators.py    ← Input validation
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_task_service.py
│   │   └── test_validators.py
│   └── integration/
│       ├── test_task_api.py
│       └── test_auth.py
│
├── dashboard/
│   ├── index.html           ← Main dashboard
│   └── assets/
│
└── docs/
    ├── architecture.md
    ├── api-reference.md
    └── deployment.md
```

---

## Build Milestones

### Milestone 1 — Foundation (Days 1-3)
- [ ] Project structure created
- [ ] Virtual environment + requirements
- [ ] Database models designed
- [ ] Basic FastAPI app running

### Milestone 2 — Data Layer (Days 4-6)
- [ ] SQLAlchemy models created
- [ ] Repository classes implemented
- [ ] Basic CRUD working in Python

### Milestone 3 — API Layer (Days 7-10)
- [ ] Task CRUD API endpoints
- [ ] Project CRUD API endpoints
- [ ] Input validation with Pydantic
- [ ] Auto-generated API docs (Swagger)

### Milestone 4 — Authentication (Days 11-13)
- [ ] User registration endpoint
- [ ] Login endpoint with JWT
- [ ] Protected routes
- [ ] Token refresh

### Milestone 5 — Business Logic (Days 14-16)
- [ ] Task assignment
- [ ] Project analytics
- [ ] Reporting service

### Milestone 6 — Dashboard (Days 17-19)
- [ ] HTML dashboard
- [ ] Charts for analytics
- [ ] Real-time updates

### Milestone 7 — Testing & Hardening (Days 20-22)
- [ ] Unit tests (80%+ coverage)
- [ ] Integration tests
- [ ] Error handling everywhere
- [ ] Logging throughout

### Milestone 8 — Deployment Prep (Days 23-25)
- [ ] .env configuration
- [ ] README complete
- [ ] Deployment guide
- [ ] Final review

---

## Installation & Setup

```bash
# 1. Clone/create project
mkdir taskflow-pro && cd taskflow-pro

# 2. Virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\Activate.ps1   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Initialize database
python src/database/init_db.py

# 6. Run the API
uvicorn src.main:app --reload

# 7. View API docs
# Open: http://localhost:8000/docs

# 8. Run tests
pytest tests/ -v --cov=src
```

---

## requirements.txt

```
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Validation
pydantic==2.4.2
pydantic-settings==2.0.3

# Utilities
python-dotenv==1.0.0
httpx==0.25.1

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Development
black==23.10.1
ruff==0.1.3
```

---

## This Capstone Demonstrates

| Skill | Demonstrated In |
|-------|----------------|
| Python OOP | Models, Services, Repositories |
| Databases | SQLAlchemy + SQLite |
| REST APIs | FastAPI endpoints |
| Authentication | JWT tokens |
| Error Handling | Global exception handlers |
| Testing | pytest with coverage |
| Logging | Structured application logs |
| Config Management | Pydantic Settings + .env |
| Clean Architecture | Layered design |
| Documentation | README + API docs |

---

## Previous: [Phase 19](../phase-19-software-engineering/README.md)
## → Go build it!
