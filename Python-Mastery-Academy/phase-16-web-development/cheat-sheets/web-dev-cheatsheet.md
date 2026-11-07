# ⚡ Phase 16 Cheat Sheet — Web Development

---

## Flask

```bash
pip install flask
python app.py   # runs on localhost:5000
```

```python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello"

@app.route("/api/items", methods=["GET", "POST"])
def items():
    if request.method == "GET":
        return jsonify({"items": []})
    data = request.json   # body as dict
    return jsonify(data), 201

@app.route("/api/items/<int:id>")
def get_item(id):
    return jsonify({"id": id})

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Flask Request

```python
request.method          # "GET", "POST"...
request.json            # JSON body → dict
request.args.get("q")   # query string ?q=...
request.form.get("name")# form data
request.headers.get("Authorization")
```

---

## Flask Response

```python
return jsonify(data)              # 200 OK
return jsonify(data), 201         # 201 Created
return "", 204                    # 204 No Content
abort(404)                        # raise 404

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404
```

---

## FastAPI

```bash
pip install fastapi uvicorn[standard] pydantic
uvicorn main:app --reload    # localhost:8000
# Docs: localhost:8000/docs
```

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name:  str
    price: float
    desc:  Optional[str] = None

@app.get("/items")
def get_all():
    return []

@app.get("/items/{id}")
def get_one(id: int):
    if id not in db:
        raise HTTPException(404, "Not found")
    return db[id]

@app.post("/items", status_code=201)
def create(item: Item):
    return {"id": 1, **item.model_dump()}

@app.patch("/items/{id}")
def update(id: int, item: Item):
    return item

@app.delete("/items/{id}", status_code=204)
def delete(id: int):
    pass
```

---

## HTTP Status Codes

```
200 OK                  — success (GET/PATCH)
201 Created             — resource created (POST)
204 No Content          — success, no body (DELETE)
400 Bad Request         — invalid input
401 Unauthorized        — not authenticated
403 Forbidden           — no permission
404 Not Found           — resource doesn't exist
422 Unprocessable       — validation error (FastAPI)
429 Too Many Requests   — rate limited
500 Internal Error      — server crash
```

---

## REST URL Patterns

```
GET    /products          → list all
GET    /products/5        → get one
POST   /products          → create
PUT    /products/5        → replace
PATCH  /products/5        → update fields
DELETE /products/5        → delete

# Nested resources
GET    /users/3/orders    → user 3's orders
POST   /users/3/orders    → create order for user 3

# Query strings
GET    /products?category=electronics&limit=10&page=2
```

---

## Pydantic (FastAPI validation)

```python
from pydantic import BaseModel, field_validator

class Product(BaseModel):
    name:   str
    price:  float
    qty:    int = 0

    @field_validator("price")
    @classmethod
    def positive_price(cls, v):
        if v < 0: raise ValueError("Must be positive")
        return v

# Auto-validates on POST, returns 422 if invalid
@app.post("/products")
def create(product: Product):
    return product.model_dump()
```
