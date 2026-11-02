# Lesson 02 — SQLite with Python

**Phase:** 09 — Databases | **Time:** ~45 min

---

## Part 1: Why SQLite?

SQLite is a file-based database — no server needed. Perfect for:
- Learning SQL
- Desktop applications
- Small to medium web apps
- Local data storage

```python
import sqlite3

# Creates database file (or connects if it exists)
conn = sqlite3.connect("myapp.db")

# In-memory database (perfect for testing)
conn = sqlite3.connect(":memory:")
```

---

## Part 2: Connection and Cursor

```python
import sqlite3

# Connect
conn = sqlite3.connect("students.db")

# Best practice: use row_factory for named column access
conn.row_factory = sqlite3.Row

# Create cursor (executes SQL)
cursor = conn.cursor()

# Execute SQL
cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT)")

# Commit changes (REQUIRED for INSERT/UPDATE/DELETE)
conn.commit()

# Always close when done
conn.close()

# OR use context manager (auto-commits and closes)
with sqlite3.connect("students.db") as conn:
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY)")
```

---

## Part 3: CRUD Operations

```python
import sqlite3

def get_conn():
    conn = sqlite3.connect("employees.db")
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TABLE
def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                department  TEXT    NOT NULL,
                salary      REAL    NOT NULL,
                active      INTEGER DEFAULT 1
            )
        """)
        conn.commit()

# CREATE (Insert)
def add_employee(name: str, department: str, salary: float) -> int:
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
            (name, department, salary)
        )
        conn.commit()
        return cursor.lastrowid   # Returns new row's ID

# READ
def get_all_employees() -> list:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM employees WHERE active = 1").fetchall()
        return [dict(row) for row in rows]

def get_employee_by_id(emp_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM employees WHERE id = ?", (emp_id,)
        ).fetchone()
        return dict(row) if row else None

def search_by_department(dept: str) -> list:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM employees WHERE department LIKE ? AND active = 1",
            (f"%{dept}%",)
        ).fetchall()
        return [dict(r) for r in rows]

# UPDATE
def update_salary(emp_id: int, new_salary: float) -> bool:
    with get_conn() as conn:
        cursor = conn.execute(
            "UPDATE employees SET salary = ? WHERE id = ?",
            (new_salary, emp_id)
        )
        conn.commit()
        return cursor.rowcount > 0

# DELETE (soft delete — better for business data)
def deactivate_employee(emp_id: int) -> bool:
    with get_conn() as conn:
        cursor = conn.execute(
            "UPDATE employees SET active = 0 WHERE id = ?", (emp_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
```

---

## Part 4: Aggregate Queries

```python
def get_department_stats() -> list:
    """Average salary and headcount per department."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT 
                department,
                COUNT(*)            AS headcount,
                ROUND(AVG(salary), 2)  AS avg_salary,
                MAX(salary)         AS max_salary,
                MIN(salary)         AS min_salary,
                SUM(salary)         AS total_payroll
            FROM employees
            WHERE active = 1
            GROUP BY department
            ORDER BY avg_salary DESC
        """).fetchall()
        return [dict(r) for r in rows]
```

---

## Part 5: ⚠️ SQL Injection — NEVER DO THIS

```python
# DANGEROUS — SQL injection vulnerability!
name = input("Employee name: ")
rows = conn.execute(f"SELECT * FROM employees WHERE name = '{name}'").fetchall()
# If name = "'; DROP TABLE employees; --" → DATABASE DESTROYED

# SAFE — always use parameterized queries with ?
rows = conn.execute(
    "SELECT * FROM employees WHERE name = ?", (name,)
).fetchall()
```

---

## Practice Exercises

1. Create a `products` table with: id, name, category, price, quantity. Write CRUD functions.

2. Write a query to find all products with quantity < 10 (reorder needed).

3. Write a query to get the average price per category.

4. Implement a soft-delete pattern for products.

---

## Next Lesson

**→ Build the [Student Database App](../guided-projects/project-01-student-app/)**
