"""
TaskFlow Pro — Capstone Application
Phase 20: Production-Ready Python Application

ARCHITECTURE:
  FastAPI backend with SQLite database.
  JWT authentication, repository pattern, logging.

SETUP:
  pip install fastapi uvicorn sqlalchemy python-jose passlib python-dotenv
  uvicorn src.main:app --reload
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime, timedelta
from enum import Enum
import sqlite3
import hashlib
import secrets
import logging
import os

# ============================================================
# LOGGING SETUP
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("taskflow")

# ============================================================
# CONFIGURATION
# ============================================================

SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
DATABASE_URL = os.getenv("DATABASE_URL", "taskflow.db")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE", "60"))

# ============================================================
# ENUMS
# ============================================================

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# ============================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
    @field_validator("username")
    @classmethod
    def username_must_be_valid(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v.lower()

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[str] = None
    
    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[str]
    created_at: str
    updated_at: str
    owner_username: str

# ============================================================
# DATABASE LAYER
# ============================================================

def get_db():
    """Get database connection (use as dependency)."""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """Create all tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_URL)
    conn.execute("PRAGMA foreign_keys = ON")
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT    NOT NULL UNIQUE,
            email      TEXT    NOT NULL UNIQUE,
            password   TEXT    NOT NULL,
            created_at TEXT    DEFAULT (datetime('now'))
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            description TEXT,
            status      TEXT    NOT NULL DEFAULT 'todo',
            priority    TEXT    NOT NULL DEFAULT 'medium',
            due_date    TEXT,
            owner_id    INTEGER NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now')),
            updated_at  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (owner_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()
    logger.info("Database initialized.")

# ============================================================
# AUTH UTILITIES
# ============================================================

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(username: str) -> str:
    """Simple token (in production, use JWT with python-jose)."""
    import base64
    import json
    payload = {
        "sub": username,
        "exp": (datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).isoformat()
    }
    token_data = json.dumps(payload)
    token = base64.b64encode(token_data.encode()).decode()
    return f"{token}.{hash_password(token + SECRET_KEY)[:16]}"

def verify_token(token: str) -> Optional[str]:
    """Verify token and return username."""
    try:
        import base64, json
        parts = token.split(".")
        if len(parts) != 2:
            return None
        decoded = json.loads(base64.b64decode(parts[0]).decode())
        if datetime.fromisoformat(decoded["exp"]) < datetime.utcnow():
            return None
        return decoded["sub"]
    except Exception:
        return None

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: sqlite3.Connection = Depends(get_db)
):
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return dict(user)

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="TaskFlow Pro",
    description="A task management API — Python Mastery Academy Capstone",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_database()
    logger.info("TaskFlow Pro API started.")

# ============================================================
# AUTH ROUTES
# ============================================================

@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: sqlite3.Connection = Depends(get_db)):
    """Register a new user."""
    existing = db.execute("SELECT id FROM users WHERE username = ?", (user.username,)).fetchone()
    if existing:
        raise HTTPException(400, "Username already taken")
    
    hashed = hash_password(user.password)
    cursor = db.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (user.username, user.email, hashed)
    )
    db.commit()
    
    new_user = db.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)).fetchone()
    logger.info(f"New user registered: {user.username}")
    return dict(new_user)

@app.post("/auth/login", response_model=TokenResponse)
def login(creds: LoginRequest, db: sqlite3.Connection = Depends(get_db)):
    """Authenticate user and return access token."""
    user = db.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (creds.username, hash_password(creds.password))
    ).fetchone()
    
    if not user:
        logger.warning(f"Failed login attempt: {creds.username}")
        raise HTTPException(401, "Invalid credentials")
    
    token = create_access_token(creds.username)
    logger.info(f"User logged in: {creds.username}")
    return {"access_token": token, "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60}

# ============================================================
# TASK ROUTES
# ============================================================

@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """List all tasks for the current user."""
    query = """
        SELECT t.*, u.username as owner_username 
        FROM tasks t JOIN users u ON t.owner_id = u.id
        WHERE t.owner_id = ?
    """
    params = [current_user["id"]]
    
    if status:
        query += " AND t.status = ?"
        params.append(status.value)
    if priority:
        query += " AND t.priority = ?"
        params.append(priority.value)
    
    query += " ORDER BY t.created_at DESC"
    tasks = db.execute(query, params).fetchall()
    return [dict(t) for t in tasks]

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Create a new task."""
    cursor = db.execute(
        """INSERT INTO tasks (title, description, priority, due_date, owner_id)
           VALUES (?, ?, ?, ?, ?)""",
        (task.title, task.description, task.priority.value, task.due_date, current_user["id"])
    )
    db.commit()
    
    new_task = db.execute(
        "SELECT t.*, u.username as owner_username FROM tasks t JOIN users u ON t.owner_id = u.id WHERE t.id = ?",
        (cursor.lastrowid,)
    ).fetchone()
    
    logger.info(f"Task created: '{task.title}' by {current_user['username']}")
    return dict(new_task)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Get a specific task."""
    task = db.execute(
        "SELECT t.*, u.username as owner_username FROM tasks t JOIN users u ON t.owner_id = u.id WHERE t.id = ? AND t.owner_id = ?",
        (task_id, current_user["id"])
    ).fetchone()
    
    if not task:
        raise HTTPException(404, "Task not found")
    return dict(task)

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    updates: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Update a task's fields."""
    existing = db.execute(
        "SELECT id FROM tasks WHERE id = ? AND owner_id = ?",
        (task_id, current_user["id"])
    ).fetchone()
    
    if not existing:
        raise HTTPException(404, "Task not found")
    
    update_data = {k: v for k, v in updates.model_dump(exclude_none=True).items()}
    if not update_data:
        raise HTTPException(400, "No fields to update")
    
    update_data["updated_at"] = datetime.now().isoformat()
    
    set_clause = ", ".join(f"{k} = ?" for k in update_data.keys())
    values = list(update_data.values()) + [task_id]
    
    db.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
    db.commit()
    
    updated = db.execute(
        "SELECT t.*, u.username as owner_username FROM tasks t JOIN users u ON t.owner_id = u.id WHERE t.id = ?",
        (task_id,)
    ).fetchone()
    return dict(updated)

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Delete a task."""
    cursor = db.execute(
        "DELETE FROM tasks WHERE id = ? AND owner_id = ?",
        (task_id, current_user["id"])
    )
    db.commit()
    
    if cursor.rowcount == 0:
        raise HTTPException(404, "Task not found")
    
    logger.info(f"Task {task_id} deleted by {current_user['username']}")

# ============================================================
# ANALYTICS ROUTES
# ============================================================

@app.get("/reports/summary")
def get_summary(
    current_user: dict = Depends(get_current_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Get task summary statistics for current user."""
    user_id = current_user["id"]
    
    total = db.execute("SELECT COUNT(*) FROM tasks WHERE owner_id = ?", (user_id,)).fetchone()[0]
    by_status = db.execute(
        "SELECT status, COUNT(*) as count FROM tasks WHERE owner_id = ? GROUP BY status",
        (user_id,)
    ).fetchall()
    by_priority = db.execute(
        "SELECT priority, COUNT(*) as count FROM tasks WHERE owner_id = ? GROUP BY priority",
        (user_id,)
    ).fetchall()
    
    return {
        "total_tasks": total,
        "by_status": {row["status"]: row["count"] for row in by_status},
        "by_priority": {row["priority"]: row["count"] for row in by_priority},
        "completion_rate": f"{(dict(zip([r['status'] for r in by_status], [r['count'] for r in by_status])).get('done', 0) / total * 100):.1f}%" if total > 0 else "0%"
    }

# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0", "timestamp": datetime.now().isoformat()}

@app.get("/")
def root():
    return {
        "app": "TaskFlow Pro",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }
