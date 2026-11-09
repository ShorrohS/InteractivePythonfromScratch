# Phase 16 — Beginner Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises: `../../exercises/beginner/exercises.md`

**Setup for every solution below:**
```bash
pip install flask        # install Flask
export FLASK_APP=app.py  # (Mac/Linux) tell Flask which file to run
set FLASK_APP=app.py     # (Windows cmd)
$env:FLASK_APP="app.py"  # (Windows PowerShell)
flask run                # start the dev server on http://127.0.0.1:5000
# OR simply: python app.py
```

---

## A1. Three-Route Flask App

```python
# app.py
from flask import Flask

app = Flask(__name__)   # __name__ tells Flask where to find templates/static files

# Route 1 — home page returns an HTML string
@app.route("/")
def home():
    return "<h1>Welcome to My Site</h1><p>Home page.</p>"

# Route 2 — about page returns plain text
@app.route("/about")
def about():
    return "About page"

# Route 3 — URL variable <name> is passed as a function argument
@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"   # e.g. /hello/Jordan → "Hello, Jordan!"

if __name__ == "__main__":
    app.run(debug=True)        # debug=True enables auto-reload and better error pages
```

**Test it:**
```
http://127.0.0.1:5000/            → <h1>Welcome to My Site</h1>...
http://127.0.0.1:5000/about       → About page
http://127.0.0.1:5000/hello/Alice → Hello, Alice!
```

---

## A2. Template Inheritance

**File structure:**
```
app.py
templates/
    base.html
    index.html
```

**`templates/base.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- Child templates can override the title block -->
    <title>{% block title %}My Site{% endblock %}</title>
    <style>
        nav a { margin-right: 1rem; text-decoration: none; color: #333; }
        nav   { background: #eee; padding: 0.5rem 1rem; }
        body  { font-family: sans-serif; padding: 1rem; }
    </style>
</head>
<body>
    <!-- Navbar present on every page -->
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/contact">Contact</a>
    </nav>

    <!-- Child templates inject their content here -->
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

**`templates/index.html`:**
```html
{% extends "base.html" %}

{% block title %}Home — My Site{% endblock %}

{% block content %}
    <h1>Welcome!</h1>
    <p>This is the home page. The navbar above comes from <code>base.html</code>.</p>
{% endblock %}
```

**`app.py`:**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # render_template() looks for files in the templates/ folder
    return render_template("index.html")

# Stub routes so the navbar links don't 404
@app.route("/about")
def about():
    return "<p>About page (no template yet)</p>"

@app.route("/contact")
def contact():
    return "<p>Contact page (no template yet)</p>"

if __name__ == "__main__":
    app.run(debug=True)
```

---

## A3. JSON Product List

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)

# Hard-coded data — in a real app this comes from a database
PRODUCTS = [
    {"id": 1, "name": "Laptop",   "price": 999.99},
    {"id": 2, "name": "Mouse",    "price":  25.00},
    {"id": 3, "name": "Keyboard", "price":  49.99},
]

@app.route("/products")
def get_products():
    # jsonify() converts a Python list/dict to a JSON Response object
    # The second element of the tuple sets the HTTP status code
    return jsonify(PRODUCTS), 200

if __name__ == "__main__":
    app.run(debug=True)
```

**Test it:**
```bash
curl http://127.0.0.1:5000/products
# or open the URL in a browser
```

---

## A4. Contact Form (GET + POST)

**File structure:**
```
app.py
templates/
    contact.html
    thankyou.html
```

**`templates/contact.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Contact Us</title></head>
<body>
    <h1>Contact Us</h1>
    <!-- action="/contact" sends the POST to this same route -->
    <form method="POST" action="/contact">
        <p>
            <label>Name:<br>
            <input type="text" name="name" required></label>
        </p>
        <p>
            <label>Message:<br>
            <textarea name="message" rows="5" cols="40" required></textarea>
            </label>
        </p>
        <button type="submit">Send</button>
    </form>
</body>
</html>
```

**`templates/thankyou.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Thank You</title></head>
<body>
    <h1>Thanks, {{ name }}!</h1>
    <p>We received your message.</p>
    <a href="/contact">Send another</a>
</body>
</html>
```

**`app.py`:**
```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# methods=["GET", "POST"] allows both HTTP verbs on this route
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Use .get() instead of [] to avoid KeyError if field is missing
        name    = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()

        # Log to console (in production you'd save to a DB or send an email)
        print(f"Contact form — Name: {name!r}, Message: {message!r}")

        # Render the thank-you page, passing the submitted name
        return render_template("thankyou.html", name=name)

    # GET request — just show the empty form
    return render_template("contact.html")

@app.route("/")
def home():
    return "<h1>Home</h1><a href='/contact'>Contact us</a>"

if __name__ == "__main__":
    app.run(debug=True)
```

---

## A5. To-Do List with Jinja2 Loop and Conditional

**File structure:**
```
app.py
templates/
    tasks.html
```

**`app.py`:**
```python
from flask import Flask, render_template

app = Flask(__name__)

# Python list of task dicts — passed to the template
TASKS = [
    {"id": 1, "title": "Buy groceries",    "done": True},
    {"id": 2, "title": "Write report",     "done": False},
    {"id": 3, "title": "Call the dentist", "done": False},
    {"id": 4, "title": "Clean the house",  "done": True},
]

@app.route("/tasks")
def task_list():
    # Pass the list to the template as 'tasks'
    return render_template("tasks.html", tasks=TASKS)

if __name__ == "__main__":
    app.run(debug=True)
```

**`templates/tasks.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Task List</title>
    <style>
        /* Applied when a task has done=True */
        .done {
            text-decoration: line-through;
            color: grey;
        }
        li { margin: 0.4rem 0; font-size: 1.1rem; }
    </style>
</head>
<body>
    <h1>My Tasks</h1>
    <ul>
        {% for task in tasks %}
            {# If done is True, add the CSS class 'done' to the <li> #}
            <li class="{% if task.done %}done{% endif %}">
                {% if task.done %}✅{% else %}⬜{% endif %}
                {{ task.title }}
            </li>
        {% endfor %}
    </ul>
</body>
</html>
```

**Key Jinja2 concepts used:**
- `{% for task in tasks %}` — loops over the list passed from Flask
- `{% if task.done %}` — checks the boolean field
- `{{ task.title }}` — outputs the value (double braces = output, percent braces = logic)

---

> **Exercises:** → [../../exercises/beginner/exercises.md](../../exercises/beginner/exercises.md)
