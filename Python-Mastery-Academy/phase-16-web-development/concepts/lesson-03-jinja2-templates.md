# Lesson 03 — HTML Templates with Jinja2

**Phase:** 16 — Web Development | **Time:** ~40 min

---

## Part 1: Why Templates?

Hardcoding HTML inside Python functions does not scale. Jinja2 solves this by letting you write HTML files with placeholders that Flask fills in at runtime.

```
Flask (app.py)                      templates/index.html
──────────────                      ────────────────────
render_template(                    <h1>Hello, {{ name }}!</h1>
  "index.html",         ─────►
  name="Alice"
)
```

Flask looks for templates in a `templates/` folder next to `app.py`.

```
my_project/
├── app.py
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    └── style.css
```

---

## Part 2: Variable Output

Double curly braces insert a Python value into the HTML at render time.

```html
<!-- templates/profile.html -->

<!-- Simple variable -->
<h1>Hello, {{ name }}!</h1>

<!-- Attribute on an object -->
<p>Email: {{ user.email }}</p>

<!-- Dictionary key access -->
<p>Price: ${{ item['price'] }}</p>

<!-- Expression -->
<p>Total: ${{ quantity * price }}</p>

<!-- Jinja2 comment — never rendered in the browser -->
{# TODO: add edit button here #}
```

Python route that passes values to the template:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/profile")
def profile():
    user = {"name": "Alice", "email": "alice@example.com"}
    return render_template("profile.html",
                           name=user["name"],
                           user=user)
```

---

## Part 3: Filters

Filters transform a value with the `|` pipe operator.

```html
<!-- String filters -->
<p>{{ name | upper }}</p>                       <!-- ALICE SMITH -->
<p>{{ name | lower }}</p>                       <!-- alice smith -->
<p>{{ name | title }}</p>                       <!-- Alice Smith -->
<p>{{ description | truncate(80) }}</p>         <!-- cuts at 80 chars... -->

<!-- Number filter -->
<p>${{ price | round(2) }}</p>                  <!-- $19.99 -->

<!-- List filter -->
<p>Items in cart: {{ cart | length }}</p>

<!-- Default value when variable is None or empty -->
<p>{{ nickname | default('Anonymous') }}</p>

<!-- Chaining filters -->
<p>{{ name | default('Guest') | upper }}</p>
```

---

## Part 4: Control Flow

### If / Elif / Else

```html
{% if user.role == 'admin' %}
    <a href="/admin">Admin Panel</a>
{% elif user.role == 'manager' %}
    <a href="/reports">Reports</a>
{% else %}
    <p>Welcome, {{ user.name }}!</p>
{% endif %}
```

### For Loops

```html
<ul>
{% for employee in employees %}
    <li>
        {{ loop.index }}. {{ employee.name }} — {{ employee.dept }}
        {% if loop.first %}<span class="badge">Top</span>{% endif %}
    </li>
{% else %}
    <!-- Rendered only when the list is empty -->
    <li>No employees found.</li>
{% endfor %}
</ul>
```

Useful `loop` variables inside any `{% for %}` block:

| Variable | Description |
|----------|-------------|
| `loop.index` | Current iteration (1-based) |
| `loop.index0` | Current iteration (0-based) |
| `loop.first` | `True` on the first iteration |
| `loop.last` | `True` on the last iteration |
| `loop.length` | Total number of items |

---

## Part 5: Template Inheritance

Inheritance lets every page share a common layout defined once. The base template defines `{% block %}` slots; child templates fill them in.

**templates/base.html** — the shared skeleton:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My App{% endblock %}</title>
    <link rel="stylesheet"
          href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('index') }}">Home</a>
        <a href="{{ url_for('employee_list') }}">Employees</a>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer><p>Python Mastery Academy</p></footer>
</body>
</html>
```

**templates/employee_list.html** — a child template that fills the blocks:

```html
{% extends 'base.html' %}

{% block title %}Employee List{% endblock %}

{% block content %}
<h1>Employees</h1>

<table>
    <thead>
        <tr>
            <th>#</th>
            <th>Name</th>
            <th>Department</th>
            <th>Salary</th>
        </tr>
    </thead>
    <tbody>
    {% for emp in employees %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>{{ emp.name }}</td>
            <td>{{ emp.dept | default('Unassigned') }}</td>
            <td>${{ emp.salary | round(2) }}</td>
        </tr>
    {% else %}
        <tr><td colspan="4">No employees on record.</td></tr>
    {% endfor %}
    </tbody>
</table>

<p>Total: {{ employees | length }} employee(s)</p>
{% endblock %}
```

Flask route:

```python
@app.route("/employees")
def employee_list():
    employees = [
        {"name": "Alice", "dept": "Engineering", "salary": 85000},
        {"name": "Bob",   "dept": "Marketing",   "salary": 65000},
    ]
    return render_template("employee_list.html", employees=employees)
```

---

## Part 6: URL Generation with url_for

Use `url_for()` to build links from view function names instead of hardcoding paths. If you rename a route, the links update automatically.

```html
<!-- Link to a view function by its Python name -->
<a href="{{ url_for('index') }}">Home</a>
<a href="{{ url_for('employee_list') }}">Employees</a>

<!-- Link with a URL parameter -->
<a href="{{ url_for('get_employee', emp_id=emp.id) }}">View Profile</a>

<!-- Static file (CSS, images, JS) -->
<link rel="stylesheet"
      href="{{ url_for('static', filename='style.css') }}">
<img src="{{ url_for('static', filename='images/logo.png') }}">
```

Python route for reference:

```python
@app.route("/employees/<int:emp_id>")
def get_employee(emp_id):
    # url_for('get_employee', emp_id=5) generates '/employees/5'
    ...
```

---

## Practice Exercises

1. Create a `base.html` with a navigation bar and footer. Build a `home.html` that extends it and displays a welcome heading.

2. Display a list of products in a table using `{% for %}`. Show "Sold Out" next to each item where `stock == 0`, otherwise show the stock count.

3. Write a template that shows a user's name with `| title` case and truncates their bio to 100 characters with `| truncate`.

4. Use `{% if %}` to show "Edit" and "Delete" buttons only when a variable `is_admin` is `True`.

5. Create an `employee_detail.html` that extends `base.html` and displays a single employee's full details. Use `url_for` to generate the back-to-list navigation link.

---

## Next Lesson

**[Lesson 04 → FastAPI Basics](lesson-04-fastapi-basics.md)**
