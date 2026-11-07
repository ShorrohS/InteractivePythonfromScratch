# Lesson 04 — FastAPI Basics

**Phase:** 16 — Web Development | **Time:** ~40 min

---

## Part 1: Setup

```bash
pip install fastapi uvicorn[standard] pydantic
```

```bash
# Run the app
uvicorn main:app --reload --port 8000

# View interactive docs at:
# http://localhost:8000/docs      (Swagger UI)
# http://localhost:8000/redoc     (ReDoc)
```

---

## Part 2: First FastAPI App

```python
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/health")
def health():
    return {"status": "healthy"}
```

---

## Part 3: Pydantic Models

Pydantic handles validation automatically:

```python
from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional

class EmployeeCreate(BaseModel):
    name:    str
    email:   str
    salary:  float
    dept:    Optional[str] = "General"

    @field_validator("salary")
    @classmethod
    def salary_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Salary must be positive")
        return v

class EmployeeResponse(BaseModel):
    id:     int
    name:   str
    email:  str
    salary: float
    dept:   str
```

---

## Part 4: Path & Query Parameters

```python
from fastapi import FastAPI, HTTPException, Query, Path

app = FastAPI()

employees_db = {}

# Path parameter
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int = Path(ge=1)):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees_db[employee_id]

# Query parameters
@app.get("/employees")
def list_employees(
    skip:  int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    dept:  str = Query(None)
):
    items = list(employees_db.values())
    if dept:
        items = [e for e in items if e.get("dept") == dept]
    return items[skip : skip + limit]
```

---

## Part 5: Complete CRUD API

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Employee API")

class EmployeeIn(BaseModel):
    name:    str
    salary:  float
    dept:    Optional[str] = "General"

class EmployeeOut(EmployeeIn):
    id: int

# In-memory store
db: dict[int, dict] = {}
counter = 0

@app.get("/employees", response_model=list[EmployeeOut])
def get_all(dept: Optional[str] = None):
    employees = list(db.values())
    if dept:
        employees = [e for e in employees if e["dept"] == dept]
    return employees

@app.get("/employees/{eid}", response_model=EmployeeOut)
def get_one(eid: int):
    if eid not in db:
        raise HTTPException(404, f"Employee {eid} not found")
    return db[eid]

@app.post("/employees", response_model=EmployeeOut, status_code=201)
def create(employee: EmployeeIn):
    global counter
    counter += 1
    emp = {"id": counter, **employee.model_dump()}
    db[counter] = emp
    return emp

@app.patch("/employees/{eid}", response_model=EmployeeOut)
def update(eid: int, updates: dict):
    if eid not in db:
        raise HTTPException(404, "Not found")
    db[eid].update({k: v for k, v in updates.items()
                    if k in ("name", "salary", "dept")})
    return db[eid]

@app.delete("/employees/{eid}", status_code=204)
def delete(eid: int):
    if eid not in db:
        raise HTTPException(404, "Not found")
    del db[eid]
```

---

## Part 6: FastAPI vs Flask Summary

```python
# Flask                          # FastAPI
# ──────────────────────         # ─────────────────────────────
@app.route("/users")             @app.get("/users")
def get_users():                 def get_users():
    return jsonify([...])            return [...]

# No validation                  # Auto validation with Pydantic
data = request.json              def create(user: UserModel):
name = data.get("name")              # name is validated automatically
```

---

## Practice Exercises

1. Build a Flask API with CRUD routes for a "products" resource.

2. Build the same API in FastAPI — compare the code and notice what's automatic.

3. Add a `/stats` endpoint that returns count, avg_salary, max_salary.

---

## Next Lesson

**[Lesson 05 → REST API Design](lesson-05-rest-api.md)**
