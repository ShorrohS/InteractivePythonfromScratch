# Phase 16 — Intermediate Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises: `../../exercises/intermediate/exercises.md`

---

## Q1. SQLite Task API (Full CRUD)

```python
# app.py
import sqlite3
from flask import Flask, jsonify, request, g

app = Flask(__name__)
DATABASE = "tasks.db"

# --- Database helpers ---

def get_db():
    """Return a per-request database connection, stored on Flask's g object."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row   # rows behave like dicts
    return g.db

@app.teardown_appcontext
def close_db(exc):
    """Close the connection at the end of every request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    """Create the tasks table if it doesn't already exist."""
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT    NOT NULL,
            done  INTEGER NOT NULL DEFAULT 0
        )
    """)
    db.commit()

# Create the table when the app starts
with app.app_context():
    init_db()

# --- Routes ---

@app.route("/tasks", methods=["GET"])
def list_tasks():
    db    = get_db()
    rows  = db.execute("SELECT * FROM tasks").fetchall()
    tasks = [dict(row) for row in rows]
    return jsonify(tasks), 200

@app.route("/tasks", methods=["POST"])
def create_task():
    data  = request.json or {}
    title = data.get("title", "").strip()
    db    = get_db()
    cur   = db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()
    task  = dict(db.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone())
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    db   = get_db()
    row  = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(dict(row)), 200

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    db  = get_db()
    row = db.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Task not found"}), 404
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return jsonify({"deleted": task_id}), 200

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Q2. Input Validation on POST /tasks

Replace the `create_task` function from Q1 with this validated version:

```python
@app.route("/tasks", methods=["POST"])
def create_task():
    # 1. Check Content-Type — request.json is None if body isn't valid JSON
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "request body must be JSON"}), 415

    title = data.get("title", "").strip()

    # 2. Title required
    if not title:
        return jsonify({"error": "title is required"}), 400

    # 3. Max length
    if len(title) > 100:
        return jsonify({"error": "title must be 100 characters or fewer"}), 400

    # 4. Insert and return the new task
    db  = get_db()
    cur = db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    db.commit()
    row = db.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201
```

---

## Q3. Flask Blueprint

**`users/__init__.py`** — empty file to make this a package:
```python
# users/__init__.py
```

**`users/routes.py`:**
```python
# users/routes.py
from flask import Blueprint, jsonify, request

users_bp = Blueprint("users", __name__)

# Placeholder in-memory store — replace with a real DB in production
_USERS = [
    {"id": 1, "username": "alice"},
    {"id": 2, "username": "bob"},
]

@users_bp.route("/", methods=["GET"])
def list_users():
    return jsonify(_USERS), 200

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in _USERS if u["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@users_bp.route("/", methods=["POST"])
def create_user():
    data     = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    if not username:
        return jsonify({"error": "username is required"}), 400
    new_user = {"id": len(_USERS) + 1, "username": username}
    _USERS.append(new_user)
    return jsonify(new_user), 201
```

**`app.py`:**
```python
# app.py
from flask import Flask
from users.routes import users_bp

def create_app():
    """Application factory — creates and configures the Flask app."""
    app = Flask(__name__)
    app.secret_key = "dev-secret"

    # Register the Blueprint; all its routes are prefixed with /users
    app.register_blueprint(users_bp, url_prefix="/users")

    @app.route("/")
    def index():
        return {"message": "API is running"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
```

---

## Q4. Custom Error Handlers (JSON)

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

# --- Error handlers ---

@app.errorhandler(404)
def not_found(e):
    """Return JSON instead of Flask's default HTML 404 page."""
    return jsonify({"error": "Not found", "status": 404}), 404

@app.errorhandler(500)
def server_error(e):
    """Return JSON instead of Flask's default HTML 500 page."""
    return jsonify({"error": "Internal server error", "status": 500}), 500

# --- Routes ---

@app.route("/")
def index():
    return jsonify({"message": "API is running"})

@app.route("/boom")
def boom():
    # Deliberately raise an exception to test the 500 handler
    raise RuntimeError("Something went very wrong!")

if __name__ == "__main__":
    # propagate_exceptions must be False (default) for errorhandler to fire
    app.run(debug=False)   # NOTE: with debug=True Flask shows its own debugger
```

---

## Q5. Pagination on GET /tasks

Replace the `list_tasks` route from Q1 with this paginated version:

```python
import math

@app.route("/tasks", methods=["GET"])
def list_tasks():
    db = get_db()

    # Read and validate query params
    page     = request.args.get("page",     1,  type=int)
    per_page = request.args.get("per_page", 5,  type=int)

    # Guard against bad values
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 5
    if per_page > 20:           # cap at 20
        per_page = 20

    offset = (page - 1) * per_page

    # Total count for pagination metadata
    total = db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    pages = math.ceil(total / per_page) if total > 0 else 1

    # Paginated rows
    rows  = db.execute(
        "SELECT * FROM tasks LIMIT ? OFFSET ?", (per_page, offset)
    ).fetchall()
    items = [dict(row) for row in rows]

    return jsonify({
        "items": items,
        "pagination": {
            "total":    total,
            "page":     page,
            "per_page": per_page,
            "pages":    pages,
        }
    }), 200
```

---

## Q6. Session-Based Login

```python
# app.py
from flask import Flask, jsonify, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "dev-secret-key"   # REQUIRED before using session

@app.route("/")
def index():
    return jsonify({"message": "Home"})

@app.route("/login", methods=["POST"])
def login():
    data     = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    if not username:
        return jsonify({"error": "username required"}), 400

    session["user"] = username          # store in signed cookie
    return jsonify({"message": "logged in", "user": username}), 200

@app.route("/dashboard", methods=["GET"])
def dashboard():
    user = session.get("user")          # None if not logged in
    if user is None:
        # Redirect unauthenticated visitors to home
        return redirect(url_for("index"))
    return jsonify({"user": user, "message": "Welcome to the dashboard"}), 200

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()                     # remove all session keys
    return jsonify({"message": "logged out"}), 200

if __name__ == "__main__":
    app.run(debug=True)
```

**Test flow with curl:**
```bash
# Login
curl -X POST http://127.0.0.1:5000/login \
     -H "Content-Type: application/json" \
     -d '{"username": "alice"}' \
     -c cookies.txt

# Access dashboard (include the session cookie)
curl http://127.0.0.1:5000/dashboard -b cookies.txt

# Logout
curl -X POST http://127.0.0.1:5000/logout -b cookies.txt -c cookies.txt
```

---

## Q7. Jinja2 Macro for Form Fields

**`templates/macros.html`** — macro definition (not rendered directly):
```html
{# macros.html — import this file in other templates #}

{% macro field(label, name, value="", error=None, type="text") %}
<div class="field" style="margin-bottom: 1rem;">
    <label for="{{ name }}" style="display:block; font-weight:bold;">
        {{ label }}
    </label>
    <input
        type="{{ type }}"
        id="{{ name }}"
        name="{{ name }}"
        value="{{ value }}"
        style="padding: 0.3rem; width: 100%; box-sizing: border-box;"
    >
    {% if error %}
        <span class="error" style="color: red; font-size: 0.85rem;">
            {{ error }}
        </span>
    {% endif %}
</div>
{% endmacro %}
```

**`templates/register.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Register</title></head>
<body>
    <h1>Register</h1>

    {# Import the macro from macros.html #}
    {% from "macros.html" import field %}

    <form method="POST" action="/register">
        {{ field("Username", "username", error=errors.get("username")) }}
        {{ field("Email",    "email",    error=errors.get("email"),    type="email") }}
        <button type="submit">Create account</button>
    </form>
</body>
</html>
```

**`templates/login.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Login</title></head>
<body>
    <h1>Login</h1>

    {% from "macros.html" import field %}

    <form method="POST" action="/login">
        {{ field("Username", "username", error=errors.get("username")) }}
        {{ field("Password", "password", error=errors.get("password"), type="password") }}
        <button type="submit">Log in</button>
    </form>
</body>
</html>
```

**`app.py`:**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/register")
def register():
    # Pass an empty errors dict; populate it after failed validation
    return render_template("register.html", errors={})

@app.route("/login")
def login_page():
    return render_template("login.html", errors={})

if __name__ == "__main__":
    app.run(debug=True)
```

---

> **Exercises:** → [../../exercises/intermediate/exercises.md](../../exercises/intermediate/exercises.md)
