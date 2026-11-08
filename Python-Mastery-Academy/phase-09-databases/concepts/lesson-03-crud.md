# Lesson 03 — CRUD Operations with Python

**Phase:** 09 — Databases | **Time:** ~50 min

---

## Part 1: What is CRUD?

CRUD stands for the four fundamental database operations every application needs:

| Operation | SQL Command | Description |
|-----------|-------------|-------------|
| **C**reate | INSERT | Add new records |
| **R**ead | SELECT | Retrieve records |
| **U**pdate | UPDATE | Modify existing records |
| **D**elete | DELETE | Remove records |

Every business system — from payroll to inventory — is built on these four operations. Master CRUD and you can build the data layer of almost any application.

---

## Part 2: Parameterized Queries — The Safe Way

**Never** build SQL strings with f-strings or concatenation — that opens the door to SQL injection. Always use `?` placeholders.

```python
import sqlite3

# ❌ DANGEROUS — SQL Injection risk
name = "Alice'; DROP TABLE employees; --"
# cursor.execute(f"SELECT * FROM employees WHERE name = '{name}'")

# ✅ SAFE — Parameterized query
# cursor.execute("SELECT * FROM employees WHERE name = ?", (name,))

# Multiple parameters — one ? per value, values passed as a tuple
# cursor.execute(
#     "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
#     ("Bob", "Sales", 65000)
# )
```

The `?` placeholder works for SQLite. Other databases use `%s` (MySQL/PostgreSQL with psycopg2) or `:name` for named placeholders. The principle is the same: never put user data directly into the SQL string.

---

## Part 3: The Context Manager Pattern

Use `with sqlite3.connect() as conn:` to handle commits and rollbacks automatically.

```python
import sqlite3

DB_PATH = "company.db"

def get_connection():
    """Return a database connection with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # Access columns by name: row["name"]
    return conn

# Context manager — commits on success, rolls back on exception
with get_connection() as conn:
    conn.execute(
        "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
        ("Alice", "Engineering", 85000)
    )
# conn.commit() is called automatically when the block exits cleanly
# conn.rollback() is called automatically if an exception is raised
```

---

## Part 4: INSERT — Create Records

```python
import sqlite3
from typing import Optional

DB_PATH = "company.db"

def create_table() -> None:
    """Create the employees table if it does not already exist."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                department TEXT    NOT NULL,
                salary     REAL    NOT NULL CHECK (salary >= 0),
                active     INTEGER DEFAULT 1
            )
        """)

def add_employee(name: str, department: str, salary: float) -> int:
    """
    Insert a new employee record.

    Returns:
        The auto-generated id of the new row (cursor.lastrowid).
    """
    sql = "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)"
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(sql, (name, department, salary))
        return cursor.lastrowid   # ID of the row just inserted
```

`cursor.lastrowid` gives you the auto-generated primary key immediately after the INSERT — useful when you need to create related records right away.

---

## Part 5: SELECT — Read Records

```python
def get_employee(employee_id: int) -> Optional[dict]:
    """
    Fetch a single active employee by primary key.

    Returns:
        A dict with employee data, or None if not found.
    """
    sql = "SELECT * FROM employees WHERE id = ? AND active = 1"
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(sql, (employee_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_employees() -> list[dict]:
    """
    Fetch all active employees ordered by name.

    Returns:
        A list of employee dicts (empty list if none found).
    """
    sql = "SELECT * FROM employees WHERE active = 1 ORDER BY name"
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(sql)
        return [dict(row) for row in cursor.fetchall()]
```

---

## Part 6: UPDATE — Modify Records

```python
def update_salary(employee_id: int, new_salary: float) -> bool:
    """
    Update an employee's salary.

    Returns:
        True if a row was updated, False if the employee was not found.
    """
    sql = "UPDATE employees SET salary = ? WHERE id = ? AND active = 1"
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(sql, (new_salary, employee_id))
        return cursor.rowcount > 0   # rowcount = number of rows affected
```

`cursor.rowcount` tells you how many rows the UPDATE actually changed. A value of `0` means the WHERE clause matched nothing — either the ID doesn't exist or the employee is already inactive.

---

## Part 7: Soft Delete vs Hard Delete

```python
def deactivate_employee(employee_id: int) -> bool:
    """
    Soft-delete: set active = 0 instead of removing the row.

    Preserves history, supports undo, and is safe for foreign keys.

    Returns:
        True if the employee was deactivated, False if not found.
    """
    sql = "UPDATE employees SET active = 0 WHERE id = ?"
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(sql, (employee_id,))
        return cursor.rowcount > 0

def hard_delete_employee(employee_id: int) -> bool:
    """
    Hard-delete: permanently removes the row.
    Use only when required by law (e.g., GDPR right to erasure).

    Returns:
        True if a row was deleted, False if not found.
    """
    sql = "DELETE FROM employees WHERE id = ?"
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(sql, (employee_id,))
        return cursor.rowcount > 0
```

**When to use each:**
- **Soft delete** (`active = 0`) — the default for business data; preserves audit history, supports undo, keeps foreign key references intact
- **Hard delete** (`DELETE`) — only when legally required or when purging truly temporary data

---

## Part 8: Class-Based Database Manager

Wrapping CRUD in a class keeps the database path and connection logic in one place.

```python
import sqlite3
from typing import Optional

class EmployeeDB:
    """Manages all database operations for the employees table."""

    def __init__(self, db_path: str = "company.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Create the employees table on first run."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    name       TEXT    NOT NULL,
                    department TEXT    NOT NULL,
                    salary     REAL    NOT NULL,
                    active     INTEGER DEFAULT 1
                )
            """)

    def _connect(self):
        """Return a connection with row_factory enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add_employee(self, name: str, department: str, salary: float) -> int:
        """Insert employee, return new id."""
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
                (name, department, salary)
            )
            return cur.lastrowid

    def get_employee(self, employee_id: int) -> Optional[dict]:
        """Fetch one active employee by id."""
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT * FROM employees WHERE id = ? AND active = 1",
                (employee_id,)
            )
            row = cur.fetchone()
            return dict(row) if row else None

    def get_all_employees(self) -> list[dict]:
        """Return all active employees sorted by name."""
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT * FROM employees WHERE active = 1 ORDER BY name"
            )
            return [dict(r) for r in cur.fetchall()]

    def update_salary(self, employee_id: int, salary: float) -> bool:
        """Update salary; return True if the row was found and updated."""
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE employees SET salary = ? WHERE id = ? AND active = 1",
                (salary, employee_id)
            )
            return cur.rowcount > 0

    def deactivate_employee(self, employee_id: int) -> bool:
        """Soft-delete an employee by setting active = 0."""
        with self._connect() as conn:
            cur = conn.execute(
                "UPDATE employees SET active = 0 WHERE id = ?",
                (employee_id,)
            )
            return cur.rowcount > 0
```

---

## Part 9: Error Handling

```python
import sqlite3
from typing import Optional

def safe_add_employee(
    db: EmployeeDB, name: str, dept: str, salary: float
) -> Optional[int]:
    """Add an employee with error handling for common database exceptions."""
    try:
        return db.add_employee(name, dept, salary)
    except sqlite3.IntegrityError as e:
        # Triggered by UNIQUE constraint violations, NOT NULL violations, etc.
        print(f"Data integrity error: {e}")
        return None
    except sqlite3.OperationalError as e:
        # Triggered by missing tables, wrong column names, locked database, etc.
        print(f"Database operation error: {e}")
        return None

# ── Full workflow example ───────────────────────────────────────────────
db = EmployeeDB("company.db")

emp_id = db.add_employee("Alice Johnson", "Engineering", 85000)
print(f"Added employee #{emp_id}")

emp = db.get_employee(emp_id)
print(f"Retrieved: {emp['name']} — ${emp['salary']:,.0f}")

updated = db.update_salary(emp_id, 92000)
print(f"Salary updated: {updated}")

all_staff = db.get_all_employees()
print(f"Active employees: {len(all_staff)}")

removed = db.deactivate_employee(emp_id)
print(f"Deactivated: {removed}")

# Employee no longer appears in active results
print(db.get_employee(emp_id))   # None
```

---

## Practice Exercises

1. Add a `search_by_department(department: str) -> list[dict]` method to `EmployeeDB` that returns all active employees in a given department, ordered by salary descending.

2. Add a `give_raise(employee_id: int, percent: float) -> bool` method that increases salary by the given percentage without reading the current salary into Python first. Hint: use SQL arithmetic: `SET salary = salary * ?`.

3. Add a `get_payroll_summary() -> dict` method that returns `{"total_employees": int, "total_payroll": float, "avg_salary": float}` using a single SQL query with aggregate functions.

4. Create a `DepartmentDB` class for a `departments` table with columns `id`, `name`, and `manager`. Implement `add()`, `get()`, `all()`, and `update_manager()` following the same pattern as `EmployeeDB`.

---

## Next Lesson

**[Lesson 04 → Advanced Queries: JOINs, Filtering, Aggregation](lesson-04-queries.md)**
