# Phase 16 — Advanced Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises: `../../exercises/advanced/exercises.md`

---

## Q1. Full CRUD REST API — Notes Resource

```python
# app.py
import sqlite3
from flask import Flask, jsonify, request, g

app = Flask(__name__)
DATABASE = "notes.db"

# --- Database helpers ---

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db:
        db.close()

def init_db():
    get_db().executescript("""
        CREATE TABLE IF NOT EXISTS notes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT    NOT NULL,
            body       TEXT    NOT NULL DEFAULT '',
            created_at TEXT    NOT NULL DEFAULT (datetime('now'))
        );
    """)
    get_db().commit()

with app.app_context():
    init_db()

# --- Routes ---

@app.route("/notes", methods=["GET"])
def list_notes():
    db = get_db()
    q  = request.args.get("q", "").strip()
    if q:
        # Use LIKE for a simple case-insensitive substring search
        pattern = f"%{q}%"
        rows = db.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR body LIKE ?",
            (pattern, pattern)
        ).fetchall()
    else:
        rows = db.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows]), 200

@app.route("/notes", methods=["POST"])
def create_note():
    data  = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    body  = data.get("body",  "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    db  = get_db()
    cur = db.execute("INSERT INTO notes (title, body) VALUES (?, ?)", (title, body))
    db.commit()
    row = db.execute("SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201

@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    row = get_db().execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(dict(row)), 200

@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    db  = get_db()
    row = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Note not found"}), 404

    data    = request.get_json(silent=True) or {}
    # Only update fields that were actually supplied in the body
    title   = data.get("title", row["title"]).strip()
    body    = data.get("body",  row["body"]).strip()

    db.execute(
        "UPDATE notes SET title = ?, body = ? WHERE id = ?",
        (title, body, note_id)
    )
    db.commit()
    updated = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    return jsonify(dict(updated)), 200

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    db  = get_db()
    row = db.execute("SELECT id FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Note not found"}), 404
    db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    return jsonify({"deleted": note_id}), 200

if __name__ == "__main__":
    app.run(debug=True)

# =============================================================================
# CURL TEST COMMANDS
# =============================================================================
# Create a note
#   curl -X POST http://127.0.0.1:5000/notes \
#        -H "Content-Type: application/json" \
#        -d '{"title": "First Note", "body": "Hello world"}'
#
# List all notes
#   curl http://127.0.0.1:5000/notes
#
# Search notes
#   curl "http://127.0.0.1:5000/notes?q=hello"
#
# Get one note
#   curl http://127.0.0.1:5000/notes/1
#
# Update a note
#   curl -X PUT http://127.0.0.1:5000/notes/1 \
#        -H "Content-Type: application/json" \
#        -d '{"title": "Updated Title"}'
#
# Delete a note
#   curl -X DELETE http://127.0.0.1:5000/notes/1
# =============================================================================
```

---

## Q2. JWT Token Authentication

```python
# app.py — adds auth on top of the Notes API from Q1
import sqlite3, time, base64, hashlib, hmac, json
from flask import Flask, jsonify, request, g
from functools import wraps

app = Flask(__name__)
DATABASE  = "notes.db"
SECRET    = "super-secret-signing-key"   # move to env var in production

# Hard-coded user for demo purposes only
USERS = {"admin": "secret"}

# --- JWT helpers (HS256 implemented with hmac + base64) ---

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def _b64url_decode(s: str) -> bytes:
    padding = 4 - len(s) % 4
    return base64.urlsafe_b64decode(s + "=" * padding)

def create_token(username: str, ttl: int = 3600) -> str:
    header  = _b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    payload = _b64url_encode(json.dumps({
        "sub": username,
        "exp": int(time.time()) + ttl
    }).encode())
    signature = _b64url_encode(
        hmac.new(SECRET.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
    )
    return f"{header}.{payload}.{signature}"

def verify_token(token: str):
    """Return the payload dict if valid, or raise ValueError."""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("malformed token")
    header, payload, sig = parts
    expected = _b64url_encode(
        hmac.new(SECRET.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
    )
    if not hmac.compare_digest(expected, sig):
        raise ValueError("invalid signature")
    data = json.loads(_b64url_decode(payload))
    if data.get("exp", 0) < time.time():
        raise ValueError("token expired")
    return data

# --- Auth decorator ---

def require_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401
        token = auth[7:]
        try:
            g.current_user = verify_token(token)["sub"]
        except ValueError as e:
            return jsonify({"error": f"Unauthorized: {e}"}), 401
        return f(*args, **kwargs)
    return wrapper

# --- Auth route ---

@app.route("/auth/login", methods=["POST"])
def auth_login():
    data     = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    if USERS.get(username) != password:
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"token": create_token(username)}), 200

# --- Protected notes routes (same logic as Q1, with @require_token added) ---

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db:
        db.close()

with app.app_context():
    get_db().executescript("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, body TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
    """)
    get_db().commit()

@app.route("/notes", methods=["GET"])
@require_token
def list_notes():
    rows = get_db().execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows]), 200

@app.route("/notes", methods=["POST"])
@require_token
def create_note():
    data  = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    db  = get_db()
    cur = db.execute("INSERT INTO notes (title, body) VALUES (?, ?)",
                     (title, data.get("body", "")))
    db.commit()
    row = db.execute("SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201

if __name__ == "__main__":
    app.run(debug=True)

# TEST:
#   TOKEN=$(curl -s -X POST http://127.0.0.1:5000/auth/login \
#     -H "Content-Type: application/json" \
#     -d '{"username":"admin","password":"secret"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")
#   curl http://127.0.0.1:5000/notes -H "Authorization: Bearer $TOKEN"
```

---

## Q3. Application Factory Pattern

**`notes_app/config.py`:**
```python
import os

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

config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "testing":     TestingConfig,
}
```

**`notes_app/db.py`:**
```python
import sqlite3
from flask import g, current_app

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exc=None):
    db = g.pop("db", None)
    if db:
        db.close()

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body  TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
    """)
    db.commit()
```

**`notes_app/routes.py`:**
```python
import sqlite3
from flask import Blueprint, jsonify, request
from .db import get_db

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/", methods=["GET"])
def list_notes():
    rows = get_db().execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows]), 200

@notes_bp.route("/", methods=["POST"])
def create_note():
    data  = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    db  = get_db()
    cur = db.execute("INSERT INTO notes (title, body) VALUES (?, ?)",
                     (title, data.get("body", "")))
    db.commit()
    row = db.execute("SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201
```

**`notes_app/__init__.py`:**
```python
from flask import Flask
from .config import config_map
from .db import close_db, init_db
from .routes import notes_bp

def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)

    # Load config from config_map
    cfg = config_map.get(config_name, config_map["development"])
    app.config.from_object(cfg)

    # Initialise the database
    with app.app_context():
        init_db()

    # Register teardown
    app.teardown_appcontext(close_db)

    # Register Blueprint
    app.register_blueprint(notes_bp, url_prefix="/notes")

    return app
```

**`run.py`:**
```python
from notes_app import create_app

app = create_app("development")

if __name__ == "__main__":
    app.run()
```

---

## Q4. File Upload

```python
# app.py
import os
from flask import Flask, jsonify, render_template_string, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER   = os.path.join(app.root_path, "uploads")
ALLOWED_EXTENSIONS = {".txt", ".csv"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)   # create uploads/ if it doesn't exist
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

UPLOAD_FORM = """
<!DOCTYPE html>
<html><head><title>Upload</title></head><body>
<h1>Upload a File</h1>
<form method="POST" enctype="multipart/form-data" action="/upload">
    <input type="file" name="file">
    <button type="submit">Upload</button>
</form>
</body></html>
"""

def allowed_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["GET"])
def upload_form():
    return render_template_string(UPLOAD_FORM)

@app.route("/upload", methods=["POST"])
def upload_file():
    # 1. Check a file was included in the request
    if "file" not in request.files:
        return jsonify({"error": "no file provided"}), 400

    file = request.files["file"]

    # 2. Check the user actually chose a file
    if file.filename == "":
        return jsonify({"error": "no file selected"}), 400

    # 3. Validate file type
    if not allowed_file(file.filename):
        return jsonify({"error": "only .txt and .csv files are allowed"}), 415

    # 4. Sanitise and save
    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    return jsonify({"message": "uploaded", "filename": filename}), 201

@app.route("/uploads/<filename>", methods=["GET"])
def serve_file(filename):
    # send_from_directory prevents path traversal attacks
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Q5. Flask CLI Seed Command

```python
# app.py  — add this to the notes app from Q1

import click

@app.cli.command("seed-db")
@click.option("--clear/--no-clear", default=True,
              help="Clear existing rows before seeding.")
def seed_db(clear):
    """Populate the database with 10 sample notes."""
    db = get_db()
    if clear:
        db.execute("DELETE FROM notes")
        click.echo("Cleared existing notes.")

    sample_notes = [
        ("Buy groceries",         "Milk, eggs, bread, coffee"),
        ("Team meeting notes",    "Q3 roadmap discussion — follow up with PM"),
        ("Book recommendations",  "The Pragmatic Programmer, Clean Code"),
        ("Workout routine",       "Mon: chest, Wed: back, Fri: legs"),
        ("Recipe: pasta",         "Boil 200g penne, add basil pesto, serve"),
        ("Python tips",           "Use list comprehensions for cleaner loops"),
        ("Travel bucket list",    "Japan, Iceland, Patagonia"),
        ("Project ideas",         "Flask tutorial, CLI tool, web scraper"),
        ("Read later",            "https://docs.python.org/3/"),
        ("Daily goals",           "Deep work block 9–12, review PRs 14:00"),
    ]

    db.executemany(
        "INSERT INTO notes (title, body) VALUES (?, ?)",
        sample_notes
    )
    db.commit()
    click.echo("Seeded 10 notes.")

# Run with:  flask seed-db
#            flask seed-db --no-clear   (keep existing rows)
```

---

## Q6. Deployment Readiness

**`requirements.txt`** (pin exact versions from your environment):
```
flask==3.0.3
Werkzeug==3.0.3
click==8.1.7
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==2.1.5
```
Generate with: `pip freeze | grep -E "^(flask|Werkzeug|click|itsdangerous|Jinja2|MarkupSafe)" > requirements.txt`

**`.env.example`:**
```
# Copy to .env and fill in real values. Never commit .env to git.
SECRET_KEY=your-very-long-random-secret-key-here
DATABASE_URL=notes.db
FLASK_ENV=production
PORT=5000
```

**Production checklist (add to top of `app.py`):**
```python
# PRODUCTION CHECKLIST
# [ ] SECRET_KEY is loaded from environment variable, not hard-coded
# [ ] DEBUG = False  (debug=True exposes a code console — never in production)
# [ ] Database path configurable via DATABASE_URL environment variable
# [ ] HTTPS enforced — handled by reverse proxy (nginx / Caddy)
# [ ] Error logging configured (logging.basicConfig or Sentry SDK)
# [ ] Rate limiting in place (see Q7 or use flask-limiter)
# [ ] CORS headers set if the API is consumed by a browser app (flask-cors)
# [ ] SQL uses parameterised queries only — never f-string into SQL
# [ ] Uploaded files validated by type AND size; stored outside web root if sensitive
# [ ] app.secret_key set and rotated periodically
```

---

## Q7. In-Memory Rate Limiter Decorator

```python
# rate_limiter.py  — or paste directly into app.py
import time
from functools import wraps
from flask import request, jsonify

# Module-level storage: {ip: [timestamp, timestamp, ...]}
_call_log: dict = {}

def rate_limit(max_calls: int = 10, window: int = 60):
    """
    Decorator factory.
    max_calls — max requests allowed within the time window
    window    — time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ip  = request.remote_addr
            now = time.time()

            # Get existing call timestamps for this IP, default to empty list
            timestamps = _call_log.get(ip, [])

            # Evict calls older than the window
            timestamps = [t for t in timestamps if now - t < window]

            if len(timestamps) >= max_calls:
                # Tell the client how long to wait (Retry-After header)
                oldest   = min(timestamps)
                retry_in = int(window - (now - oldest)) + 1
                response = jsonify({"error": "rate limit exceeded"})
                response.headers["Retry-After"] = str(retry_in)
                return response, 429

            # Record this call and update the log
            timestamps.append(now)
            _call_log[ip] = timestamps

            return f(*args, **kwargs)
        return wrapper
    return decorator


# --- Usage in app.py ---

from flask import Flask
app = Flask(__name__)

@app.route("/notes", methods=["POST"])
@rate_limit(max_calls=10, window=60)   # max 10 POSTs per minute per IP
def create_note():
    return jsonify({"message": "note created"}), 201

if __name__ == "__main__":
    app.run(debug=True)
```

**How it works:**
1. On each request, fetch the list of past timestamps for this IP.
2. Remove timestamps older than `window` seconds (sliding window).
3. If the count is at or above `max_calls`, return 429.
4. Otherwise, append the current timestamp and proceed.

**Limitations of in-memory approach:**
- Resets when the server restarts.
- Does not work across multiple server processes/workers.
- For production, use `flask-limiter` with a Redis backend.

---

> **Exercises:** → [../../exercises/advanced/exercises.md](../../exercises/advanced/exercises.md)
