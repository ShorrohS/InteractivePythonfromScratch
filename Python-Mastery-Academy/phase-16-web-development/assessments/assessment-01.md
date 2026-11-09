# Phase 16 — Completion Assessment: Web Development with Flask

> Complete all tasks before checking the answer key.
> **Pass mark: 80%** | **Time: 60 minutes**

**Setup:**
```bash
pip install flask
```

---

## Task 1 — Routes and Templates (25 points)

Build a Flask app with three pages that all share a common layout via template inheritance.

**Required files:**
```
app.py
templates/
    base.html
    home.html
    about.html
    contact.html
```

**Specifications:**

1. `base.html` must contain:
   - A `<nav>` with links to `/`, `/about`, and `/contact`
   - A `{% block title %}` and a `{% block content %}` block

2. `home.html` must:
   - Extend `base.html`
   - Render a list of blog post dicts passed from Python using a `{% for %}` loop
   - Display each post's `title` and `author` in an `<article>` tag

3. Flask routes:
   - `GET /` — renders `home.html` and passes this list:
     ```python
     POSTS = [
         {"title": "Getting Started with Flask", "author": "Alice"},
         {"title": "Jinja2 Templates Explained",  "author": "Bob"},
         {"title": "Building REST APIs",           "author": "Alice"},
     ]
     ```
   - `GET /about` — renders `about.html` (any content)
   - `GET /contact` — renders `contact.html` with a simple form (name + message fields)

**Scoring:** 5 pts per requirement correctly implemented (routes work, templates extend base, loop renders posts).

---

## Task 2 — Database (25 points)

Add SQLite persistence to your app using the `sqlite3` module.

**Schema** (create automatically when the app starts):
```sql
CREATE TABLE IF NOT EXISTS posts (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title   TEXT NOT NULL,
    content TEXT NOT NULL DEFAULT '',
    author  TEXT NOT NULL DEFAULT 'Anonymous'
);
```

**Routes to add:**

| Method | URL | Behaviour |
|--------|-----|-----------|
| GET | `/posts` | Render an HTML page listing all posts from the DB (title + author) |
| POST | `/posts` | Insert a new post (JSON body: `title`, `content`, `author`); return the new row as JSON with 201 |
| GET | `/posts/<int:id>` | Render an HTML detail page showing title, author, and content; return 404 JSON if not found |
| DELETE | `/posts/<int:id>` | Delete the post and return `{"deleted": id}` as JSON with 200 |

**Requirements:**
- Use Flask's `g` object and `teardown_appcontext` to manage the connection lifecycle
- `row_factory = sqlite3.Row` so rows can be accessed by column name

**Scoring:** 5 pts per route correctly implemented (correct method, correct response type, correct status code).

---

## Task 3 — Forms and Validation (25 points)

Add a "new post" form at `/posts/new`.

**GET `/posts/new`**: Render a form template with fields for `title`, `content`, and `author`.

**POST `/posts/new`**: Validate and insert the post:

| Rule | Failure response |
|------|-----------------|
| `title` must not be empty | Re-render the form with error: `"Title is required"` |
| `content` must be at least 20 characters | Re-render the form with error: `"Content must be at least 20 characters"` |
| Both pass | Insert into DB and redirect to `/posts/<new_id>` |

**Requirements:**
- Use `request.form.get()` (not `request.form[]`) for safe field access
- Pass an `errors` dict to the template so error messages appear next to each field
- After a successful insert, use `redirect(url_for("post_detail", id=new_id))` (or equivalent)

**Scoring:** 5 pts each: form renders, title validation works, content validation works, successful redirect, errors display in template.

---

## Task 4 — JSON API (25 points)

Add a parallel JSON API for the posts resource.

**Endpoints:**

| Method | URL | Behaviour |
|--------|-----|-----------|
| GET | `/api/posts` | Return all posts as a JSON array with HTTP 200 |
| POST | `/api/posts` | Accept JSON body `{"title":"...","content":"...","author":"..."}`; validate title required; return new post with HTTP 201, or `{"error":"..."}` with 400 |
| GET | `/api/posts/<int:id>` | Return one post as JSON with 200, or `{"error":"Not found"}` with 404 |

**Requirements:**
- All three endpoints use `jsonify()` for responses
- POST validates `title` (required) and returns a descriptive 400 error if missing
- The routes should reuse the same `get_db()` helper from Task 2

**Scoring:** 5 pts each: GET all returns correct JSON, POST creates and returns 201, POST validates and returns 400, GET one returns 200, GET one returns 404 for missing id.

---

## Scoring Table

| Task | Points available | Your score |
|------|-----------------|------------|
| Task 1 — Routes + Templates | 25 | /25 |
| Task 2 — Database | 25 | /25 |
| Task 3 — Forms + Validation | 25 | /25 |
| Task 4 — API | 25 | /25 |
| **Total** | **100** | **/100** |

| Score | Action |
|-------|--------|
| 80–100 | Move to Phase 17 |
| 65–79 | Review weak areas (see topics below), then proceed |
| < 65 | Redo the exercises and guided projects before continuing |

**Review topics by score:**
- Low Task 1 → revisit Jinja2 template inheritance
- Low Task 2 → revisit Flask + SQLite lesson
- Low Task 3 → revisit POST handling and redirects
- Low Task 4 → revisit jsonify and status codes

---

## Answer Key

### Task 1 — Routes and Templates

**`app.py`:**
```python
from flask import Flask, render_template

app = Flask(__name__)

POSTS = [
    {"title": "Getting Started with Flask", "author": "Alice"},
    {"title": "Jinja2 Templates Explained",  "author": "Bob"},
    {"title": "Building REST APIs",           "author": "Alice"},
]

@app.route("/")
def home():
    return render_template("home.html", posts=POSTS)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
```

**`templates/base.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}My Blog{% endblock %}</title>
  <style>
    nav a { margin-right: 1rem; }
    body  { font-family: sans-serif; max-width: 800px; margin: 2rem auto; }
  </style>
</head>
<body>
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
  </nav>
  <hr>
  {% block content %}{% endblock %}
</body>
</html>
```

**`templates/home.html`:**
```html
{% extends "base.html" %}
{% block title %}Home — My Blog{% endblock %}
{% block content %}
  <h1>Latest Posts</h1>
  {% for post in posts %}
    <article>
      <h2>{{ post.title }}</h2>
      <p>By {{ post.author }}</p>
    </article>
  {% endfor %}
{% endblock %}
```

### Task 2 — Database (add to app.py)

```python
import sqlite3
from flask import Flask, render_template, jsonify, request, g

DATABASE = "blog.db"

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
        CREATE TABLE IF NOT EXISTS posts (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT NOT NULL,
            content TEXT NOT NULL DEFAULT '',
            author  TEXT NOT NULL DEFAULT 'Anonymous'
        );
    """)
    get_db().commit()

with app.app_context():
    init_db()

@app.route("/posts", methods=["GET"])
def post_list():
    rows  = get_db().execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    posts = [dict(r) for r in rows]
    return render_template("post_list.html", posts=posts)

@app.route("/posts", methods=["POST"])
def create_post_api():
    data    = request.get_json(silent=True) or {}
    title   = data.get("title",   "").strip()
    content = data.get("content", "").strip()
    author  = data.get("author",  "Anonymous").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    db  = get_db()
    cur = db.execute("INSERT INTO posts (title, content, author) VALUES (?,?,?)",
                     (title, content, author))
    db.commit()
    row = db.execute("SELECT * FROM posts WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201

@app.route("/posts/<int:post_id>", methods=["GET"])
def post_detail(post_id):
    row = get_db().execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Not found"}), 404
    return render_template("post_detail.html", post=dict(row))

@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    db  = get_db()
    row = db.execute("SELECT id FROM posts WHERE id = ?", (post_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Not found"}), 404
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    return jsonify({"deleted": post_id}), 200
```

### Task 3 — Forms and Validation (add to app.py)

```python
from flask import redirect, url_for

@app.route("/posts/new", methods=["GET", "POST"])
def new_post():
    errors = {}
    if request.method == "POST":
        title   = request.form.get("title",   "").strip()
        content = request.form.get("content", "").strip()
        author  = request.form.get("author",  "Anonymous").strip()

        if not title:
            errors["title"] = "Title is required"
        if len(content) < 20:
            errors["content"] = "Content must be at least 20 characters"

        if not errors:
            db  = get_db()
            cur = db.execute(
                "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
                (title, content, author)
            )
            db.commit()
            return redirect(url_for("post_detail", post_id=cur.lastrowid))

    return render_template("new_post.html", errors=errors)
```

### Task 4 — JSON API (add to app.py)

```python
@app.route("/api/posts", methods=["GET"])
def api_list_posts():
    rows = get_db().execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows]), 200

@app.route("/api/posts", methods=["POST"])
def api_create_post():
    data    = request.get_json(silent=True) or {}
    title   = data.get("title",   "").strip()
    content = data.get("content", "").strip()
    author  = data.get("author",  "Anonymous").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    db  = get_db()
    cur = db.execute(
        "INSERT INTO posts (title, content, author) VALUES (?,?,?)",
        (title, content, author)
    )
    db.commit()
    row = db.execute("SELECT * FROM posts WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201

@app.route("/api/posts/<int:post_id>", methods=["GET"])
def api_get_post(post_id):
    row = get_db().execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row)), 200
```
