# Phase 16 — Flask Web Development Cheat Sheet

> Quick reference — not a replacement for the lessons.
> Use `Ctrl+F` to jump to a section.

---

## 1. App Setup and Running

```python
from flask import Flask
app = Flask(__name__)           # __name__ = current module

if __name__ == "__main__":
    app.run(debug=True)         # dev server on http://127.0.0.1:5000
```

```bash
# Alternative: use the Flask CLI
export FLASK_APP=app.py         # Mac/Linux
set FLASK_APP=app.py            # Windows cmd
$env:FLASK_APP="app.py"        # Windows PowerShell
flask run                       # starts the dev server
flask run --port 8000           # custom port
```

---

## 2. Route Decorators

```python
@app.route("/")                             # GET only (default)
@app.route("/submit", methods=["GET","POST"])  # multiple methods
@app.route("/items/<int:item_id>")          # integer URL variable
@app.route("/users/<string:username>")      # string URL variable (default)
@app.route("/path/<path:subpath>")          # matches slashes too
```

---

## 3. URL Parameters and Query Strings

```python
# URL variables are passed as function arguments
@app.route("/users/<int:user_id>")
def get_user(user_id):          # user_id is already an int
    ...

# Query string: /search?q=flask&page=2
q    = request.args.get("q",    "")          # default ""
page = request.args.get("page", 1, type=int) # cast to int, default 1
```

---

## 4. The `request` Object

```python
from flask import request

request.method          # "GET", "POST", "PUT", "DELETE", ...
request.args            # query string params (ImmutableMultiDict)
request.form            # form POST data
request.form.get("name", "")    # safe — returns default if missing
request.json            # parsed JSON body (or None if not JSON)
request.get_json(silent=True)   # same, won't raise on bad JSON
request.files           # uploaded files
request.remote_addr     # client IP address
request.headers.get("Authorization")  # read a specific header
```

---

## 5. Response Helpers

```python
from flask import jsonify, redirect, render_template, abort, make_response

return "Hello"                          # plain text, 200
return "Created", 201                   # plain text, custom status
return jsonify({"key": "value"})        # JSON, 200
return jsonify(data), 201               # JSON, custom status
return render_template("page.html")     # render Jinja2 template
return render_template("page.html", name=name, items=items)  # with context
return redirect("/other")               # 302 redirect
return redirect(url_for("view_name"))   # redirect by view function name
abort(404)                              # raise HTTP error immediately
```

---

## 6. Jinja2 Template Syntax

```jinja2
{# This is a comment — not rendered #}

{{ variable }}              {# output a variable #}
{{ user.name }}             {# attribute access #}
{{ items[0] }}              {# index access #}

{% if condition %}          {# conditional #}
  ...
{% elif other %}
  ...
{% else %}
  ...
{% endif %}

{% for item in items %}     {# loop #}
  {{ loop.index }}          {# 1-based loop counter #}
  {{ loop.index0 }}         {# 0-based loop counter #}
  {{ loop.first }}          {# True on first iteration #}
  {{ loop.last }}           {# True on last iteration #}
{% endfor %}
```

### Built-in Filters

```jinja2
{{ name | upper }}          {# ALICE #}
{{ name | lower }}          {# alice #}
{{ name | title }}          {# Alice Smith #}
{{ price | round(2) }}      {# 9.99 #}
{{ text | truncate(50) }}   {# truncate to 50 chars #}
{{ html | safe }}           {# mark as safe — skip auto-escaping #}
{{ items | length }}        {# list length #}
{{ items | join(", ") }}    {# join list to string #}
{{ value | default("N/A") }}{# fallback if value is falsy #}
```

### Template Inheritance

```html
{# base.html #}
<!DOCTYPE html>
<html>
<head><title>{% block title %}Site{% endblock %}</title></head>
<body>
  <nav>...</nav>
  {% block content %}{% endblock %}
</body>
</html>
```

```html
{# child.html #}
{% extends "base.html" %}

{% block title %}My Page{% endblock %}

{% block content %}
  <h1>Hello</h1>
{% endblock %}
```

### Macros

```jinja2
{# macros.html #}
{% macro input_field(label, name, type="text", error=None) %}
  <div>
    <label>{{ label }}</label>
    <input type="{{ type }}" name="{{ name }}">
    {% if error %}<span class="error">{{ error }}</span>{% endif %}
  </div>
{% endmacro %}

{# using_macros.html #}
{% from "macros.html" import input_field %}
{{ input_field("Email", "email", type="email", error=errors.get("email")) }}
```

---

## 7. SQLite with Flask

```python
import sqlite3
from flask import g

DATABASE = "app.db"

def get_db():
    """Return a per-request db connection (stored on g)."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row   # enables row["col"] access
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db:
        db.close()

# Usage inside a route
db  = get_db()
db.execute("INSERT INTO items (name) VALUES (?)", (name,))   # ? = parameterised
db.commit()
rows = db.execute("SELECT * FROM items").fetchall()
row  = db.execute("SELECT * FROM items WHERE id = ?", (id,)).fetchone()
# Convert sqlite3.Row to dict
data = dict(row)
data_list = [dict(r) for r in rows]
```

---

## 8. Session

```python
from flask import session

app.secret_key = "your-secret-key"   # REQUIRED — must be set before using session

session["user"] = "alice"            # store a value
user = session.get("user")           # read (None if not set)
session.pop("user", None)            # remove one key
session.clear()                      # remove all keys
```

---

## 9. Error Handlers

```python
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found", "status": 404}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error", "status": 500}), 500

# Trigger errors manually
from flask import abort
abort(404)    # raises 404 immediately
abort(400)    # bad request
```

---

## 10. Blueprints

```python
# users/routes.py
from flask import Blueprint
users_bp = Blueprint("users", __name__)

@users_bp.route("/")
def list_users(): ...

# app.py
from users.routes import users_bp
app.register_blueprint(users_bp, url_prefix="/users")
# All users routes are now at /users/...
```

---

## 11. Application Factory

```python
# app.py
def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    app.register_blueprint(some_bp, url_prefix="/prefix")
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
    return app

# run.py
from app import create_app
app = create_app("development")
if __name__ == "__main__":
    app.run()
```

---

## 12. Environment Variables and Config Classes

```python
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key")
    DEBUG      = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Load from .env file (requires python-dotenv)
# pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()          # reads .env into os.environ
```

**.env file (never commit to git):**
```
SECRET_KEY=my-real-secret
DATABASE_URL=prod.db
FLASK_ENV=production
```

---

## 13. Deployment Checklist

```
[ ] SECRET_KEY from environment variable (not hard-coded)
[ ] DEBUG = False
[ ] Database path from env var
[ ] HTTPS via reverse proxy (nginx, Caddy)
[ ] Error logging configured (logging or Sentry)
[ ] Rate limiting in place
[ ] Only required packages in requirements.txt
[ ] .env not committed to git (.gitignore)
[ ] SQL uses parameterised queries only (never f-strings in SQL)
```

**`requirements.txt`** — pin exact versions:
```
flask==3.0.3
Werkzeug==3.0.3
```
Generate: `pip freeze > requirements.txt`

---

## ⚠️ Gotchas

| Gotcha | Why it matters |
|--------|---------------|
| `debug=True` in production | The Werkzeug debugger lets anyone run Python code in your server — a critical security hole |
| `request.form["key"]` | Raises `KeyError` if the field is missing — use `.get("key", "")` |
| Returning `dict` directly | Flask >= 2.2 accepts dicts, but older versions don't — always use `jsonify()` to be explicit and set the correct Content-Type header |
| SQL f-strings: `f"WHERE id = {id}"` | **SQL injection** — always use `?` placeholders: `"WHERE id = ?"`, `(id,)` |
| Using `session` without `secret_key` | Raises `RuntimeError` at runtime — set `app.secret_key` before the first request |
| Forgetting `app.app_context()` | Database helpers that use `g` require an application context — use `with app.app_context():` in scripts and tests |
| CSRF on forms | Flask does not protect forms against CSRF by default — use `flask-wtf` in production |
| Open file handles | Always close SQLite connections (`conn.close()`) or use the `g` + `teardown_appcontext` pattern |
