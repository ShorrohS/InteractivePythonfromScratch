# Lesson 02 — Flask Basics

**Phase:** 16 — Web Development | **Time:** ~40 min

---

## Part 1: Setup

```bash
pip install flask
```

```python
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
```

Run: `python app.py` → visit `http://localhost:5000`

---

## Part 2: Routes

```python
# Basic route
@app.route("/")
def index():
    return "Home page"

# Dynamic route
@app.route("/users/<int:user_id>")
def get_user(user_id):
    return f"User #{user_id}"

@app.route("/search/<string:query>")
def search(query):
    return f"Searching: {query}"

# Multiple methods
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return jsonify({"users": []})
    elif request.method == "POST":
        data = request.json
        return jsonify(data), 201

# URL parameters (query string)
# GET /items?page=2&limit=10
@app.route("/items")
def items():
    page  = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    return jsonify({"page": page, "limit": limit})
```

---

## Part 3: Request Object

```python
from flask import request

# JSON body
data = request.json           # dict from JSON body

# Form data
name = request.form.get("name")

# URL query params
q = request.args.get("q", "")

# Headers
token = request.headers.get("Authorization")

# Method
request.method               # "GET", "POST", etc.
```

---

## Part 4: Response Formats

```python
# Return JSON
from flask import jsonify

@app.route("/api/data")
def get_data():
    return jsonify({"status": "ok", "data": [1, 2, 3]})

# Return with status code
@app.route("/api/create", methods=["POST"])
def create():
    return jsonify({"id": 1}), 201

# Return HTML
@app.route("/page")
def page():
    return render_template("index.html", name="Alice")

# Return error
from flask import abort

@app.route("/admin")
def admin():
    abort(403)    # Forbidden
```

---

## Part 5: Complete REST API Example

```python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory "database"
employees = [
    {"id": 1, "name": "Alice",  "salary": 85000},
    {"id": 2, "name": "Bob",    "salary": 65000},
]
next_id = 3

def find_employee(eid: int):
    return next((e for e in employees if e["id"] == eid), None)

@app.route("/api/employees", methods=["GET"])
def get_all():
    return jsonify({"employees": employees, "count": len(employees)})

@app.route("/api/employees/<int:eid>", methods=["GET"])
def get_one(eid):
    emp = find_employee(eid)
    if not emp:
        abort(404)
    return jsonify(emp)

@app.route("/api/employees", methods=["POST"])
def create():
    global next_id
    data = request.json
    if not data or not data.get("name"):
        return jsonify({"error": "Name is required"}), 400
    emp = {"id": next_id, "name": data["name"],
           "salary": data.get("salary", 50000)}
    employees.append(emp)
    next_id += 1
    return jsonify(emp), 201

@app.route("/api/employees/<int:eid>", methods=["PATCH"])
def update(eid):
    emp = find_employee(eid)
    if not emp:
        abort(404)
    data = request.json or {}
    emp.update({k: v for k, v in data.items() if k in ("name", "salary")})
    return jsonify(emp)

@app.route("/api/employees/<int:eid>", methods=["DELETE"])
def delete(eid):
    emp = find_employee(eid)
    if not emp:
        abort(404)
    employees.remove(emp)
    return "", 204

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request"}), 400

if __name__ == "__main__":
    app.run(debug=True)
```

Test with curl:
```bash
curl http://localhost:5000/api/employees
curl http://localhost:5000/api/employees/1
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"Carol","salary":90000}' \
     http://localhost:5000/api/employees
```

---

## Next Lesson

**[Lesson 04 → FastAPI Basics](lesson-04-fastapi-basics.md)**
