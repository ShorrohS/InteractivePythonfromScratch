# Lesson 01 — Web Fundamentals

**Phase:** 16 — Web Development | **Time:** ~30 min

---

## Part 1: How the Web Works

```
CLIENT (Browser)                    SERVER (Python)
──────────────────                  ────────────────
User visits URL  ──── HTTP Request ──►  Flask/FastAPI
                                        processes request
                 ◄─── HTTP Response ──  sends back HTML/JSON
Browser renders
```

Every web interaction is a **request-response cycle**.

---

## Part 2: HTTP Methods

| Method | Use | Example |
|--------|-----|---------|
| `GET` | Retrieve data | Get all users |
| `POST` | Create new data | Create a user |
| `PUT` | Replace data | Replace a user |
| `PATCH` | Update part of data | Update email only |
| `DELETE` | Remove data | Delete a user |

---

## Part 3: URLs and Routes

```
https://api.example.com/users/42/orders?status=pending

  Protocol: https
  Domain:   api.example.com
  Path:     /users/42/orders
  Query:    status=pending
```

Routes in Flask:
```python
@app.route("/users")          # GET /users
@app.route("/users/<int:id>") # GET /users/42 (dynamic)
@app.route("/users", methods=["POST"])  # POST /users
```

---

## Part 4: Request and Response

```
HTTP REQUEST:
  POST /users HTTP/1.1
  Host: api.example.com
  Content-Type: application/json
  Authorization: Bearer abc123

  {"name": "Alice", "email": "alice@example.com"}

HTTP RESPONSE:
  HTTP/1.1 201 Created
  Content-Type: application/json

  {"id": 42, "name": "Alice", "email": "alice@example.com"}
```

---

## Part 5: REST API Design Principles

```
REST = Representational State Transfer

1. Resources identified by URLs
   GET /products           → list all products
   GET /products/5         → get product #5
   POST /products          → create product
   PUT /products/5         → replace product #5
   PATCH /products/5       → update product #5
   DELETE /products/5      → delete product #5

2. Stateless
   Each request contains all info needed
   No session state on server

3. Consistent response format (JSON)
   {"id": 1, "name": "Widget", "price": 9.99}

4. Proper HTTP status codes
   200 OK, 201 Created, 400 Bad Request, 404 Not Found
```

---

## Part 6: JSON — The Web's Language

```python
import json

# Python dict → JSON string
data = {"name": "Alice", "age": 30, "active": True}
json_str = json.dumps(data)          # '{"name": "Alice", ...}'

# JSON string → Python dict
data = json.loads('{"name": "Bob"}') # {'name': 'Bob'}

# In Flask/FastAPI, this happens automatically
# Flask: jsonify(data) or return data (in newer versions)
# FastAPI: return data directly (Pydantic handles it)
```

---

## Part 7: Flask vs FastAPI

| Feature | Flask | FastAPI |
|---------|-------|---------|
| Speed | Medium | Very fast |
| Learning curve | Easy | Easy (needs Pydantic) |
| Type hints | Optional | Required |
| Auto docs | No | Yes (Swagger + ReDoc) |
| Async | Optional | Built-in |
| Validation | Manual | Pydantic auto |
| Best for | Full web apps | REST APIs |

---

## Next Lesson

**[Lesson 02 → Flask Basics](lesson-02-flask-basics.md)**
