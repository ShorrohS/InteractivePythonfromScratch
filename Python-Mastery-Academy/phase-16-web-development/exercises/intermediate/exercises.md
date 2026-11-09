# 📝 Phase 16 — Intermediate Exercises: Web Development with Flask

> These are **code-writing tasks**.
> Each question asks you to implement a Flask feature; write the complete Python
> (and any HTML templates) needed to make it work.
> Solutions: `../../solutions/intermediate/solutions.md`

**Setup:**
```bash
pip install flask
```

---

## Q1. ⭐⭐ SQLite Task API (Full CRUD)

Build a Flask app backed by a SQLite database with four routes for a **tasks** resource.

**Database schema** (create automatically on startup):
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT    NOT NULL,
    done  INTEGER NOT NULL DEFAULT 0
);
```

**Routes to implement:**

| Method | URL | Behaviour |
|--------|-----|-----------|
| GET | `/tasks` | Return all rows as a JSON array |
| POST | `/tasks` | Insert a new task; body is JSON `{"title": "..."}` |
| GET | `/tasks/<int:id>` | Return one task or 404 JSON if not found |
| DELETE | `/tasks/<int:id>` | Delete the task; return `{"deleted": id}` |

Requirements:
- Use `sqlite3` from the standard library (no ORM)
- Open/close the connection per request using `g` and `teardown_appcontext`, or a `with` block
- All responses are JSON (`jsonify`)
- POST returns HTTP 201; DELETE returns 200

---

## Q2. ⭐⭐ Input Validation on POST /tasks

Extend the `POST /tasks` route from Q1 with request body validation:

1. **Title required**: if `title` is missing or an empty string, return:
   ```json
   {"error": "title is required"}
   ```
   with HTTP status **400**.

2. **Max length**: if `title` is longer than 100 characters, return:
   ```json
   {"error": "title must be 100 characters or fewer"}
   ```
   with HTTP status **400**.

3. **Content-Type check**: if the request body is not JSON (i.e., `request.json` returns `None`), return:
   ```json
   {"error": "request body must be JSON"}
   ```
   with HTTP status **415**.

4. On success, return the newly created task object with HTTP **201**.

---

## Q3. ⭐⭐ Flask Blueprint

Refactor your app so the "users" feature lives in its own Blueprint module.

**File structure:**
```
app.py
users/
    __init__.py
    routes.py
```

**`users/routes.py`** must:
- Create a Blueprint: `users_bp = Blueprint("users", __name__)`
- Define three routes: `GET /` (list users), `GET /<int:id>` (get one), `POST /` (create user)
- Each route can return simple placeholder JSON (no real database needed for this exercise)

**`app.py`** must:
- Create the Flask app with `create_app()` (an application factory function)
- Import and register `users_bp` with `url_prefix="/users"`
- Return the app from `create_app()`

Test that visiting `http://127.0.0.1:5000/users/` returns a JSON list.

---

## Q4. ⭐⭐ Custom Error Handlers (JSON)

Add a custom 404 and 500 error handler to a Flask API so that errors return JSON instead of HTML pages.

**Implement:**
```python
@app.errorhandler(404)
def not_found(e): ...

@app.errorhandler(500)
def server_error(e): ...
```

Each handler must return a JSON body like:
```json
{"error": "Not found", "status": 404}
```
with the correct HTTP status code.

Also add a route `/boom` that deliberately raises an unhandled `Exception` so you can test the 500 handler.

Test with:
- `GET /nonexistent` → 404 JSON
- `GET /boom` → 500 JSON

---

## Q5. ⭐⭐ Pagination on GET /tasks

Extend `GET /tasks` from Q1 to support pagination via query parameters.

**Query parameters:**
- `page` (integer, default `1`)
- `per_page` (integer, default `5`, max `20`)

**Response shape:**
```json
{
  "items": [...],
  "pagination": {
    "total": 23,
    "page": 2,
    "per_page": 5,
    "pages": 5
  }
}
```

Requirements:
- Use `LIMIT` and `OFFSET` in the SQL query
- Use `request.args.get("page", 1, type=int)` to read query params
- If `per_page` exceeds 20, cap it at 20 and return the result (don't error)
- A separate `SELECT COUNT(*)` query provides the total

---

## Q6. ⭐⭐ Session-Based Login

Implement a minimal session-based login system.

**Routes:**

| Method | URL | Behaviour |
|--------|-----|-----------|
| POST | `/login` | Reads JSON `{"username": "..."}`, stores it in `session["user"]`, returns `{"message": "logged in"}` |
| GET | `/dashboard` | If `session["user"]` is set, returns `{"user": "..."}`. If not set, returns a redirect to `/` |
| POST | `/logout` | Clears `session["user"]` (or calls `session.clear()`), returns `{"message": "logged out"}` |

Requirements:
- Set `app.secret_key = "dev-secret-key"` (any string; in production use an env var)
- Import `session` from Flask
- The dashboard route must use `session.get("user")` — if it returns `None`, call `redirect(url_for("index"))` (add a simple `/` route that returns `"Home"`)

---

## Q7. ⭐⭐ Jinja2 Macro for Form Fields

Write a Jinja2 macro that renders a labelled form field with an optional error message, then use it in two different templates.

**`templates/macros.html`** — define this macro:
```jinja
{% macro field(label, name, value="", error=None, type="text") %}
  <div class="field">
    <label for="{{ name }}">{{ label }}</label>
    <input type="{{ type }}" id="{{ name }}" name="{{ name }}" value="{{ value }}">
    {% if error %}
      <span class="error">{{ error }}</span>
    {% endif %}
  </div>
{% endmacro %}
```

**`templates/register.html`**: imports the macro and uses it for `username` and `email` fields.

**`templates/login.html`**: imports the macro and uses it for `username` and `password` (type="password") fields.

Write Flask routes `GET /register` and `GET /login` that render each template. Pass an `errors` dict (can be empty `{}`) to each template so the macro's `error` parameter can be wired up.

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
