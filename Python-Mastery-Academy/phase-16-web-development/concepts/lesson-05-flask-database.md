# Lesson 05 — Working with a Database in Flask

**Phase:** 16 — Web Development | **Time:** ~50 min

---

## Part 1: Why Databases in Web Apps

An in-memory list resets every time the server restarts. A database persists data across requests, server restarts, and deployments.

```
Without a database            With SQLite
────────────────              ─────────────────────────────
employees = []                employees.db  ← file on disk
# lost on restart             # survives restarts and deploys
```

Python ships with `sqlite3` — no extra install needed. It stores everything in a single `.db` file, making it ideal for learning and small apps.

---

## Part 2: Initialising the Database

Define the schema once using `CREATE TABLE IF NOT EXISTS` so the table is only created when it does not exist yet.

```python
import sqlite3
from flask import Flask

app = Flask(__name__)
DATABASE = "tasks.db"

def init_db():
    """Create tables if they do not exist yet."""
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            done        INTEGER NOT NULL DEFAULT 0,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()

# Call once when the app starts
with app.app_context():
    init_db()
```

---

## Part 3: Flask App Context and get_db

Opening a new connection for every query is wasteful. Flask's `g` object stores per-request resources — the connection opens once per request and closes automatically when the request ends.

```python
from flask import g

def get_db():
    """Return the current request's database connection (opens if needed)."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row   # rows behave like dicts
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Close the database connection at the end of every request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()
```

`sqlite3.Row` lets you access columns by name (`row["title"]`) instead of index, which keeps route code and templates readable.

---

## Part 4: CRUD Routes with Parameterised Queries

Always use `?` placeholders — **never** format user input directly into a SQL string. Parameterised queries are the primary defence against SQL injection.

```python
from flask import request, redirect, url_for, render_template, abort

# LIST — GET /
@app.route("/")
def list_tasks():
    tasks = get_db().execute(
        "SELECT * FROM tasks ORDER BY created_at DESC"
    ).fetchall()
    return render_template("tasks.html", tasks=tasks)

# CREATE — POST /tasks
@app.route("/tasks", methods=["POST"])
def create_task():
    title = request.form.get("title", "").strip()
    if title:
        db = get_db()
        db.execute(
            "INSERT INTO tasks (title) VALUES (?)",   # ← parameterised
            (title,)
        )
        db.commit()
    return redirect(url_for("list_tasks"))

# UPDATE — POST /tasks/<id>/toggle
@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    db = get_db()
    row = db.execute(
        "SELECT id FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    if row is None:
        abort(404)
    db.execute(
        "UPDATE tasks SET done = NOT done WHERE id = ?",   # ← parameterised
        (task_id,)
    )
    db.commit()
    return redirect(url_for("list_tasks"))

# DELETE — POST /tasks/<id>/delete
@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    db = get_db()
    db.execute(
        "DELETE FROM tasks WHERE id = ?",   # ← parameterised
        (task_id,)
    )
    db.commit()
    return redirect(url_for("list_tasks"))
```

---

## Part 5: Complete Task Manager Example

**app.py:**

```python
import sqlite3
from flask import Flask, g, request, redirect, url_for, render_template, abort

app = Flask(__name__)
DATABASE = "tasks.db"

# ── Database helpers ──────────────────────────────────────────

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT    NOT NULL,
                done  INTEGER NOT NULL DEFAULT 0
            )
        """)
        db.commit()

# ── Routes ────────────────────────────────────────────────────

@app.route("/")
def list_tasks():
    tasks = get_db().execute("SELECT * FROM tasks").fetchall()
    return render_template("tasks.html", tasks=tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    title = request.form.get("title", "").strip()
    if title:
        db = get_db()
        db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        db.commit()
    return redirect(url_for("list_tasks"))

@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    return redirect(url_for("list_tasks"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
```

**templates/tasks.html:**

```html
{% extends 'base.html' %}
{% block title %}Task Manager{% endblock %}

{% block content %}
<h1>Tasks</h1>

<!-- Add task form -->
<form action="/tasks" method="POST">
    <input type="text" name="title" placeholder="New task..." required>
    <button type="submit">Add</button>
</form>

<!-- Task list -->
<ul>
{% for task in tasks %}
    <li>
        {{ task['title'] }}
        {% if task['done'] %}<em>(done)</em>{% endif %}

        <!-- Delete button uses POST to avoid accidental deletions via GET -->
        <form action="/tasks/{{ task['id'] }}/delete" method="POST"
              style="display:inline">
            <button type="submit">Delete</button>
        </form>
    </li>
{% else %}
    <li>No tasks yet. Add one above.</li>
{% endfor %}
</ul>
{% endblock %}
```

---

## Part 6: Brief Intro to Flask-SQLAlchemy

For larger apps, an ORM (Object-Relational Mapper) replaces raw SQL with Python classes. Each class maps to a table; each instance maps to a row.

```python
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
db = SQLAlchemy(app)

class Task(db.Model):                       # class = table
    id    = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done  = db.Column(db.Boolean, default=False)

# Create tables
with app.app_context():
    db.create_all()

# Query — replaces SELECT *
tasks = Task.query.all()

# Filter — replaces WHERE
pending = Task.query.filter_by(done=False).all()

# Insert
new_task = Task(title="Write tests")
db.session.add(new_task)
db.session.commit()

# Delete
task = Task.query.get(1)
db.session.delete(task)
db.session.commit()
```

Install: `pip install flask-sqlalchemy`

---

## Practice Exercises

1. Add a `priority` column (`TEXT`, values: `low`, `medium`, `high`) to the tasks table. Update the INSERT route to accept it from the form and the SELECT route to display it.

2. Create a `GET /tasks/<id>` route that fetches a single task by ID and returns it as JSON using `jsonify`. Return 404 if the task does not exist.

3. Add an update route: `POST /tasks/<id>/edit` that reads a new `title` from the form and runs an `UPDATE` query with a parameterised placeholder.

4. Filter tasks by status in the list route: `GET /?done=1` shows only completed tasks, `GET /?done=0` shows only pending tasks. Use `request.args.get`.

5. Rewrite the Task Manager using Flask-SQLAlchemy. Replace every raw SQL call with the equivalent ORM call and verify the app behaves identically.

---

## Next Lesson

**[Lesson 06 → Deploying a Flask App](lesson-06-deploying-flask.md)**
