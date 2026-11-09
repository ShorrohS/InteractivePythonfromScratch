# 📝 Phase 16 — Beginner Exercises: Web Development with Flask

> These are **code-writing tasks**, not stdin/stdout programs.
> Each question asks you to implement a Flask feature.
> Write your solution, then run it locally with `flask run` or `python app.py`.
> Solutions: `../../solutions/beginner/solutions.md`

**Setup (do this once before starting):**
```bash
pip install flask
```

---

## Q1. ⭐ Three-Route Flask App

Write a complete Flask application (`app.py`) with exactly three routes:

| Route | What it returns |
|-------|----------------|
| `/` | An HTML string: `<h1>Welcome to My Site</h1><p>Home page.</p>` |
| `/about` | The plain string `About page` |
| `/hello/<name>` | The string `Hello, <name>!` where `<name>` is whatever the user puts in the URL |

Requirements:
- Use `from flask import Flask`
- Create the app with `app = Flask(__name__)`
- The `<name>` segment is a URL variable (use `<name>` in the route decorator)
- Run with `if __name__ == "__main__": app.run(debug=True)`

Test by visiting:
- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/about`
- `http://127.0.0.1:5000/hello/Jordan`

---

## Q2. ⭐ Template Inheritance

Create a two-file template system and a Flask route that uses it.

**File structure you need to create:**
```
app.py
templates/
    base.html
    index.html
```

**`templates/base.html`** must have:
- A `<nav>` bar with three links: Home (`/`), About (`/about`), Contact (`/contact`)
- A `{% block content %}{% endblock %}` placeholder in the `<body>`
- A `<title>` tag that also uses a block so child templates can override it

**`templates/index.html`** must:
- Use `{% extends "base.html" %}`
- Fill the `content` block with an `<h1>` heading and a `<p>` paragraph of your choice

**`app.py`** must have:
- `from flask import Flask, render_template`
- A route at `/` that calls `render_template("index.html")`

Test by visiting `http://127.0.0.1:5000/` — you should see the navbar and your content.

---

## Q3. ⭐ JSON Product List

Write a Flask route that returns data as JSON.

Create `app.py` with a route `/products` (GET) that:
- Builds a Python list of **3** product dictionaries, each with keys `id`, `name`, and `price`
- Returns the list as a JSON response using `jsonify`
- Sets the HTTP status code to `200`

Example of what a browser/client should receive:
```json
[
  {"id": 1, "name": "Laptop", "price": 999.99},
  {"id": 2, "name": "Mouse",  "price": 25.00},
  {"id": 3, "name": "Keyboard", "price": 49.99}
]
```

Requirements:
- `from flask import Flask, jsonify`
- Use your own product names and prices
- The route must explicitly pass the status code to `jsonify` **or** return a tuple `(jsonify(...), 200)`

---

## Q4. ⭐ Contact Form (GET + POST)

Build an HTML form and the Flask route that handles it.

**File structure:**
```
app.py
templates/
    contact.html
    thankyou.html
```

**`templates/contact.html`**: An HTML page with a `<form>` that:
- Has `method="POST"` and `action="/contact"`
- Contains a text input named `name`
- Contains a textarea named `message`
- Has a submit button labelled "Send"

**`templates/thankyou.html`**: Displays "Thanks, `{{ name }}`! We got your message."

**`app.py`** must have a single route `/contact` that:
- On **GET**: renders `contact.html`
- On **POST**: reads `name` and `message` from `request.form` using `.get()`, prints them to the console, then redirects to `/` (or renders `thankyou.html` passing `name`)

Requirements:
- `from flask import Flask, render_template, request, redirect, url_for`
- Route decorator must include `methods=["GET", "POST"]`
- Use `request.form.get("name")` (not `request.form["name"]`) to safely read form data

---

## Q5. ⭐ To-Do List with Jinja2 Loop and Conditional

Write a Flask app that passes a list of task dictionaries to a Jinja2 template, which renders them with a loop and marks completed tasks differently.

**`app.py`**: Define a list called `TASKS` in your Python file:
```python
TASKS = [
    {"id": 1, "title": "Buy groceries",    "done": True},
    {"id": 2, "title": "Write report",     "done": False},
    {"id": 3, "title": "Call the dentist", "done": False},
    {"id": 4, "title": "Clean the house",  "done": True},
]
```
Pass it to `render_template("tasks.html", tasks=TASKS)` from a `/tasks` route.

**`templates/tasks.html`**: Must use:
- `{% for task in tasks %}` to loop over the list
- `{% if task.done %}` inside the loop to apply a CSS class (e.g., `class="done"`) or a ✅ symbol to completed tasks
- `{{ task.title }}` to display the title

Add a small `<style>` block so that `.done` items appear with `text-decoration: line-through` and `color: grey`.

Test by visiting `http://127.0.0.1:5000/tasks`.

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
