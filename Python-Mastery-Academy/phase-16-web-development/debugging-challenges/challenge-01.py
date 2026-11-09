"""
Debugging Challenge 01 — Phase 16: Web Development with Flask
=============================================================

INSTRUCTIONS:
  This file contains a small Flask task-list application with 7 bugs.
  Find and fix every bug.
  When all bugs are fixed, you should be able to:
    - Visit http://127.0.0.1:5000/tasks  and see the task list rendered
    - POST a new task and be redirected back to the list
    - GET /api/tasks and receive a valid JSON array
    - Session counter increments on every page visit

HINTS:
  - Read error messages carefully — Flask shows line numbers
  - Try to fix one bug at a time, restart the server, then fix the next
  - Bug types present: wrong redirect URL, missing HTTP method, unsafe
    form access, wrong Jinja2 syntax, missing secret_key, unclosed DB
    connection, wrong return type for JSON

DO NOT LOOK AT THE ANSWERS BELOW UNTIL YOU'VE TRIED!

Setup:
  pip install flask
  python challenge_01.py
"""

import sqlite3
from flask import Flask, request, redirect, url_for, session, jsonify

app = Flask(__name__)

# NOTE: In-memory database resets every restart — fine for this challenge
DATABASE = ":memory:"

# --------------------------------------------------------------------------
# Database helper
# --------------------------------------------------------------------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done  INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    return conn


# --------------------------------------------------------------------------
# Inline Jinja2 template (stored as a string to keep everything in one file)
# --------------------------------------------------------------------------

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Tasks</title></head>
<body>
  <h1>Task List</h1>
  <p>Visits this session: %visits%</p>  <!-- BUG 4: wrong Jinja2 syntax -->

  <ul>
  {% for task in tasks %}
    <li>{{ task['title'] }} — {{ 'done' if task['done'] else 'pending' }}</li>
  {% endfor %}
  </ul>

  <h2>Add Task</h2>
  <form method="POST" action="/tasks/new">
    <input type="text" name="title" placeholder="Task title">
    <button type="submit">Add</button>
  </form>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@app.route("/tasks")
def task_list():
    # BUG 5: Missing app.secret_key — session access will raise RuntimeError
    session["visits"] = session.get("visits", 0) + 1

    conn = get_db()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    tasks = [dict(row) for row in rows]
    # BUG 6: Database connection never closed — should call conn.close()

    from flask import render_template_string
    return render_template_string(TEMPLATE, tasks=tasks, visits=session["visits"])


@app.route("/tasks/new")    # BUG 1: method list missing — POST will get 405
def add_task():
    # BUG 2: Using [] instead of .get() — KeyError if 'title' is absent
    title = request.form["title"].strip()
    if not title:
        return redirect(url_for("task_list"))

    conn = get_db()
    conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()

    return redirect("/task")    # BUG 3: wrong URL — should redirect to /tasks


@app.route("/api/tasks")
def api_tasks():
    conn = get_db()
    rows  = conn.execute("SELECT * FROM tasks").fetchall()
    tasks = [dict(row) for row in rows]
    conn.close()

    return tasks    # BUG 7: returning a plain dict/list — must use jsonify()


# --------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)


# ============================================================================
# ANSWERS (don't scroll until you've tried!)
# ============================================================================
#
# BUG 1 (line ~68): Missing methods parameter
#   WRONG:  @app.route("/tasks/new")
#   RIGHT:  @app.route("/tasks/new", methods=["POST"])
#   WHY:    Without methods=["POST"], Flask defaults to GET only.
#           A form POST to this URL returns 405 Method Not Allowed.
#
# BUG 2 (line ~71): Unsafe form field access
#   WRONG:  title = request.form["title"]
#   RIGHT:  title = request.form.get("title", "")
#   WHY:    If the 'title' key is absent, dict-style access raises KeyError.
#           .get() returns a default value instead.
#
# BUG 3 (line ~79): Wrong redirect URL
#   WRONG:  return redirect("/task")
#   RIGHT:  return redirect(url_for("task_list"))
#             OR: return redirect("/tasks")
#   WHY:    "/task" (no 's') does not match any route — results in a 404.
#
# BUG 4 (line ~43): Wrong Jinja2 template syntax
#   WRONG:  %visits%
#   RIGHT:  {{ visits }}
#   WHY:    Jinja2 uses {{ }} for variable output, not %var%.
#
# BUG 5 (line ~57): Missing secret_key before using session
#   WRONG:  (no secret_key anywhere)
#   RIGHT:  Add  app.secret_key = "dev-secret"  after app = Flask(__name__)
#   WHY:    Flask's session uses a signed cookie; without secret_key it
#           raises RuntimeError: "The session is unavailable because no
#           secret key was set."
#
# BUG 6 (line ~63): Database connection never closed
#   WRONG:  conn = get_db() ... (no conn.close())
#   RIGHT:  Add  conn.close()  after the fetchall(), or use a with block /
#           Flask's g + teardown_appcontext pattern.
#   WHY:    Leaving connections open leaks resources; with ":memory:" it
#           also means the rows are in a different in-memory DB instance.
#
# BUG 7 (line ~84): Returning a plain list instead of a JSON response
#   WRONG:  return tasks
#   RIGHT:  return jsonify(tasks)
#   WHY:    Flask cannot serialise a plain Python list as an HTTP response.
#           jsonify() creates a Response object with Content-Type: application/json.
#
# ============================================================================
