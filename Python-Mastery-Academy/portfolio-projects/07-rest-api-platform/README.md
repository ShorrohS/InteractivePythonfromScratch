# REST API Platform — Portfolio Project

> A production-grade REST API demonstrating professional Python backend development.

---

## Project Overview

This is a full REST API platform built with FastAPI, SQLite, and JWT authentication. It represents the most employer-relevant portfolio project in the academy.

---

## Features

- ✅ Full CRUD API endpoints
- ✅ JWT authentication (register, login, protected routes)
- ✅ Pydantic input validation
- ✅ SQLite database with proper relationships
- ✅ Auto-generated OpenAPI documentation
- ✅ Error handling and proper HTTP status codes
- ✅ Structured logging
- ✅ pytest test suite
- ✅ Environment-based configuration

---

## Technologies

| Technology | Purpose |
|-----------|---------|
| FastAPI | API framework |
| SQLite | Database |
| python-jose | JWT authentication |
| Pydantic | Data validation |
| pytest | Testing |
| uvicorn | ASGI server |
| python-dotenv | Configuration |

---

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/rest-api-platform.git
cd rest-api-platform

# Virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\Activate.ps1   # Windows

# Install dependencies
pip install -r requirements.txt

# Run
uvicorn main:app --reload

# View API docs
# http://localhost:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /auth/register | Create account | No |
| POST | /auth/login | Get JWT token | No |
| GET | /tasks | List your tasks | Yes |
| POST | /tasks | Create task | Yes |
| GET | /tasks/{id} | Get task | Yes |
| PATCH | /tasks/{id} | Update task | Yes |
| DELETE | /tasks/{id} | Delete task | Yes |
| GET | /reports/summary | Analytics | Yes |
| GET | /health | Health check | No |

---

## Example Requests

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "secure123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secure123"}'
# Returns: {"access_token": "..."}

# Create task (with token)
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "priority": "high"}'
```

---

## Project Structure

```
rest-api-platform/
├── main.py              ← FastAPI app + routes
├── requirements.txt
├── .env.example
├── tests/
│   └── test_api.py     ← pytest tests
└── README.md
```

---

## Running Tests

```bash
pip install pytest httpx
pytest tests/ -v
```

---

## What This Demonstrates

This project shows a hiring manager that you can:
- Build and structure a REST API professionally
- Implement authentication securely
- Validate input data properly
- Write tests for API endpoints
- Use modern Python (FastAPI, Pydantic, type hints)
- Follow REST principles (proper HTTP methods and status codes)
- Document your API

---

*Built as part of the Python Mastery Academy portfolio track.*
