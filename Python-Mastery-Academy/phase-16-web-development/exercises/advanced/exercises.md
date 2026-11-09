# 📝 Phase 16 — Advanced Exercises: Web Development with Flask

> These are challenging, multi-part implementations.
> Plan your file structure before writing code.
> Solutions: `../../solutions/advanced/solutions.md`

**Setup:**
```bash
pip install flask
```

---

## Q1. ⭐⭐⭐ Full CRUD REST API — Notes Resource

Build a complete REST API for a **Notes** resource using Flask and SQLite.

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS notes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT    NOT NULL,
    body       TEXT    NOT NULL DEFAULT '',
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

**Endpoints:**

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/notes` | List all notes; support `?q=<term>` search on title and body |
| POST | `/notes` | Create a note; body: `{"title": "...", "body": "..."}` |
| GET | `/notes/<int:id>` | Get one note (404 if not found) |
| PUT | `/notes/<int:id>` | Update a note (partial update — only fields present in body change) |
| DELETE | `/notes/<int:id>` | Delete a note; return `{"deleted": id}` |

**Curl commands** to test every endpoint (write these as comments at the bottom of `app.py`):
```bash
# Create
curl -X POST http://127.0.0.1:5000/notes \
     -H "Content-Type: application/json" \
     -d '{"title": "First Note", "body": "Hello world"}'

# List all
curl http://127.0.0.1:5000/notes

# Search
curl "http://127.0.0.1:5000/notes?q=hello"

# Get one
curl http://127.0.0.1:5000/notes/1

# Update
curl -X PUT http://127.0.0.1:5000/notes/1 \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Title"}'

# Delete
curl -X DELETE http://127.0.0.1:5000/notes/1
```

---

## Q2. ⭐⭐⭐ JWT Token Authentication

Add token-based authentication to the Notes API from Q1.

**How it works:**
1. `POST /auth/login` accepts `{"username": "...", "password": "..."}` and returns a signed JWT token.
2. All `/notes` routes now require an `Authorization: Bearer <token>` header.
3. If the token is missing or invalid, return `{"error": "Unauthorized"}` with HTTP 401.

**Implementation rules:**
- Do **not** use `flask-jwt-extended`; implement signing manually using the `hmac` and `base64` modules from the standard library (create a simple header.payload.signature token), **or** use `PyJWT` (`pip install PyJWT`).
- Hard-code one valid user for testing: `{"username": "admin", "password": "secret"}`.
- Token payload must include `sub` (username) and `exp` (expiry timestamp — 1 hour from issue).
- Write a `require_token` decorator using `functools.wraps` that reads and validates the token, then attach it to every notes route.

---

## Q3. ⭐⭐⭐ Application Factory Pattern

Refactor the Notes app to use the **Application Factory** pattern with multiple config classes.

**File structure:**
```
notes_app/
    __init__.py       ← contains create_app(config_name)
    config.py         ← DevelopmentConfig, ProductionConfig, TestingConfig
    routes.py         ← Blueprint with all /notes routes
    db.py             ← get_db(), close_db(), init_db()
run.py                ← calls create_app("development") and runs it
```

**`config.py`** must define:
```python
class Config:
    SECRET_KEY = "change-me"
    DATABASE   = "notes.db"
    DEBUG      = False

class DevelopmentConfig(Config):
    DEBUG    = True
    DATABASE = "notes_dev.db"

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-prod")
    DATABASE   = os.environ.get("DATABASE_URL", "notes.db")

class TestingConfig(Config):
    TESTING  = True
    DATABASE = ":memory:"
```

**`create_app(config_name)`** must:
- Accept `"development"`, `"production"`, or `"testing"` (map to config classes)
- Register the notes Blueprint
- Register the `init_db` teardown
- Return the app

---

## Q4. ⭐⭐⭐ File Upload

Add file upload functionality to the Flask app.

**Routes:**

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/upload` | Renders an upload form (HTML template) |
| POST | `/upload` | Accepts `multipart/form-data`; field name is `file` |
| GET | `/uploads/<filename>` | Serves the uploaded file back to the client |

**Validation rules for POST `/upload`:**
- If no file is included, return `{"error": "no file provided"}` with 400.
- If the filename is empty (user submitted without choosing a file), return 400.
- If the file extension is not `.txt` or `.csv`, return `{"error": "only .txt and .csv files are allowed"}` with 415.

**Implementation:**
- Use `from werkzeug.utils import secure_filename` to sanitise the filename before saving.
- Save files to an `uploads/` folder inside the app directory; create it if it doesn't exist (`os.makedirs`).
- `GET /uploads/<filename>` uses `send_from_directory(app.config["UPLOAD_FOLDER"], filename)`.

---

## Q5. ⭐⭐⭐ Flask CLI Seed Command

Write a Flask CLI command `flask seed-db` that populates the `notes` table with 10 sample records.

**Requirements:**
- Register the command using `@app.cli.command("seed-db")`
- The command must:
  1. Open a database connection
  2. Optionally clear existing rows (`DELETE FROM notes`)
  3. Insert 10 rows with varied titles and bodies
  4. Print `"Seeded 10 notes."` on success
- Running `flask seed-db` from the terminal must work without extra arguments

**Bonus**: add a `--clear/--no-clear` option using `click.option` so the user can choose whether to wipe existing data first.

---

## Q6. ⭐⭐⭐ Deployment Readiness

Create three deployment-related files for the Notes app.

**`requirements.txt`**: Pin exact versions of every package the app needs:
```
flask==3.0.3
Werkzeug==3.0.3
click==8.1.7
# add any other packages you used
```
Generate the real list with `pip freeze > requirements.txt` and trim to only the direct dependencies.

**`.env.example`**: A template showing all required environment variables (no real values):
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=notes.db
FLASK_ENV=production
PORT=5000
```

**`app.py` production comments**: Add a section at the top of `app.py` (or in a `PRODUCTION_CHECKLIST` docstring) with these checks as comments:
```python
# PRODUCTION CHECKLIST
# [ ] SECRET_KEY loaded from environment, not hard-coded
# [ ] DEBUG = False
# [ ] Database file path configurable via env var
# [ ] HTTPS enforced (handled by reverse proxy, e.g. nginx)
# [ ] Error logging configured (e.g. logging.basicConfig or Sentry)
# [ ] Rate limiting in place (see Q7)
# [ ] CORS headers set if the API is consumed by a browser app
```

---

## Q7. ⭐⭐⭐ In-Memory Rate Limiter Decorator

Write a `rate_limit` decorator that limits how many times a specific route can be called **per IP address per minute**, using only the standard library plus Flask.

**Specification:**
- `@rate_limit(max_calls=10, window=60)` — configurable max calls and time window (seconds)
- Uses a module-level dict to store `{ip: [(timestamp1, ...), ...]}` call records
- On each request: evict records older than `window` seconds, count remaining, reject if over limit
- If the limit is exceeded, return `{"error": "rate limit exceeded"}` with HTTP **429**
- Use `functools.wraps` to preserve the wrapped function's metadata
- Apply the decorator to `POST /notes` to limit to 10 requests per minute per IP

**Skeleton to complete:**
```python
import time
from functools import wraps
from flask import request, jsonify

_call_log: dict = {}   # {ip: [timestamp, ...]}

def rate_limit(max_calls: int = 10, window: int = 60):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ip  = request.remote_addr
            now = time.time()
            # --- your implementation here ---
        return wrapper
    return decorator
```

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
