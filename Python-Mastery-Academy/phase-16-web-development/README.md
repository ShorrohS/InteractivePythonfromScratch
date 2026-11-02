# 🌍 Phase 16 — Web Development

> **Goal:** Build web applications and REST APIs with Flask and FastAPI.

---

## The Two Frameworks

```
Flask   → Micro-framework, great for learning, full control
FastAPI → Modern, fast, built-in docs, async support
```

---

## Installation

```bash
# Flask
pip install flask flask-sqlalchemy

# FastAPI
pip install fastapi uvicorn[standard] pydantic
```

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-web-concepts.md](concepts/lesson-01-web-concepts.md) | How web apps work |
| 02 | [lesson-02-flask-basics.md](concepts/lesson-02-flask-basics.md) | Flask routes and templates |
| 03 | [lesson-03-flask-database.md](concepts/lesson-03-flask-database.md) | Flask + SQLAlchemy |
| 04 | [lesson-04-fastapi-basics.md](concepts/lesson-04-fastapi-basics.md) | FastAPI fundamentals |
| 05 | [lesson-05-rest-api.md](concepts/lesson-05-rest-api.md) | REST API design |
| 06 | [lesson-06-authentication.md](concepts/lesson-06-authentication.md) | JWT Authentication |

---

## Flask Quick Start

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/users", methods=["GET"])
def get_users():
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    return jsonify(users)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    return jsonify({"message": f"Created user {data['name']}"}), 201

if __name__ == "__main__":
    app.run(debug=True)
```

## FastAPI Quick Start

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/users")
def get_users():
    return [{"id": 1, "name": "Alice"}]

@app.post("/users", status_code=201)
def create_user(user: User):
    return {"message": f"Created {user.name}", "email": user.email}

# Run: uvicorn main:app --reload
# Docs: http://localhost:8000/docs
```

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [Flask Blog](guided-projects/project-01-flask-blog/) | Full blog with templates |
| [FastAPI REST](guided-projects/project-02-fastapi-rest/) | Inventory REST API |

---

## ✅ Completion Checklist

- [ ] Understand HTTP methods (GET, POST, PUT, DELETE)
- [ ] Can create Flask routes and return JSON
- [ ] Can connect Flask to SQLite
- [ ] Can create FastAPI endpoints with Pydantic models
- [ ] Know how JWT authentication works

---

## Previous: [Phase 15](../phase-15-gui/README.md) | Next: [Phase 17](../phase-17-advanced-python/README.md)
