# Architecture — TaskFlow Pro

---

## System Overview

TaskFlow Pro is a REST API for task management, built with FastAPI and SQLite. It serves as the capstone project demonstrating every major concept from the Python Mastery Academy.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│   Browser  |  Mobile App  |  curl  |  Python requests           │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     API LAYER (FastAPI)                          │
│                                                                 │
│   ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│   │  /auth/*        │  │  /tasks/*        │  │ /reports/*   │  │
│   │  Registration   │  │  CRUD operations │  │ Analytics    │  │
│   │  Login/Token    │  │  Filtering       │  │ Summary      │  │
│   └────────┬────────┘  └────────┬─────────┘  └──────┬───────┘  │
│            │                    │                     │          │
│            ▼                    ▼                     ▼          │
│   ┌────────────────────────────────────────────────────────┐    │
│   │              MIDDLEWARE LAYER                          │    │
│   │   JWT Authentication  |  CORS  |  Error Handling      │    │
│   └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                  │
│                                                                 │
│   SQLite Database (taskflow.db)                                 │
│   ┌──────────────┐  ┌──────────────┐                           │
│   │   users      │  │   tasks      │                           │
│   │  - id        │  │  - id        │                           │
│   │  - username  │  │  - title     │                           │
│   │  - email     │  │  - status    │                           │
│   │  - password  │  │  - priority  │                           │
│   │  - created   │  │  - owner_id  │                           │
│   └──────────────┘  └──────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Framework | FastAPI 0.104 | REST endpoints, docs |
| Validation | Pydantic v2 | Input/output models |
| Auth | python-jose + passlib | JWT tokens + bcrypt hashing |
| Database | SQLite + sqlite3 | Persistent storage |
| Testing | pytest + httpx | Unit + integration tests |
| Config | python-dotenv | Environment variables |
| Docs | FastAPI built-in | Swagger UI auto-generated |

---

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /auth/register | No | Create new account |
| POST | /auth/login | No | Get JWT token |
| GET | /tasks | Yes | List user's tasks |
| POST | /tasks | Yes | Create task |
| GET | /tasks/{id} | Yes | Get single task |
| PATCH | /tasks/{id} | Yes | Update task |
| DELETE | /tasks/{id} | Yes | Delete task |
| GET | /reports/summary | Yes | Analytics |
| GET | /health | No | Health check |

---

## Authentication Flow

```
1. POST /auth/register → User created, returns user data
2. POST /auth/login    → Returns JWT access_token
3. Include in requests:
   Authorization: Bearer <access_token>
4. Token expires in 60 minutes (configurable)
```

---

## Data Models

### User
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

### Task
```json
{
  "id": 42,
  "title": "Complete capstone project",
  "description": "Build and deploy the TaskFlow Pro API",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2024-02-01",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:00:00",
  "owner_username": "alice"
}
```

---

## Project Structure

```
phase-20-capstone/
├── .env.example          ← Environment template
├── requirements.txt      ← Production dependencies
├── README.md
│
├── src/
│   └── main.py           ← FastAPI application
│
├── tests/
│   └── test_main.py      ← Full test suite
│
└── docs/
    ├── architecture.md   ← This file
    └── deployment-guide.md
```

---

## Security Decisions

1. **Passwords:** Hashed with bcrypt (never stored in plaintext)
2. **JWT:** Signed with HS256 algorithm, configurable expiry
3. **Task isolation:** Users can only access their own tasks
4. **Input validation:** Pydantic validates all inputs before reaching business logic
5. **SQL injection:** Parameterized queries throughout
6. **Secrets:** All sensitive values in .env (never hardcoded)
