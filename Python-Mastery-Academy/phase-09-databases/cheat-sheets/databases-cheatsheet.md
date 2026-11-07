# ⚡ Phase 09 Cheat Sheet — Databases

---

## SQLite Connection

```python
import sqlite3

# Connect to file
conn = sqlite3.connect("mydb.db")

# In-memory (testing)
conn = sqlite3.connect(":memory:")

# Named column access
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Context manager (auto-commit)
with sqlite3.connect("mydb.db") as conn:
    conn.execute(...)

# Close
conn.close()
```

---

## Execute SQL

```python
# Single query
conn.execute("SQL", params)

# Many rows at once
conn.executemany("SQL", list_of_tuples)

# Fetch results
cursor = conn.execute("SELECT ...")
row    = cursor.fetchone()    # one row
rows   = cursor.fetchall()    # all rows

# Access by column name (with row_factory)
row["name"]
row["salary"]

# Commit DML changes
conn.commit()
```

---

## Parameterized Queries (ALWAYS use this)

```python
# SAFE — use ? placeholders
conn.execute(
    "SELECT * FROM users WHERE name = ?", (name,)
)
conn.execute(
    "INSERT INTO users (name, age) VALUES (?, ?)",
    (name, age)
)

# NEVER do this (SQL injection):
conn.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

---

## CRUD

```sql
-- Create
INSERT INTO table (col1, col2) VALUES (?, ?)

-- Read
SELECT * FROM table
SELECT col1, col2 FROM table WHERE condition
SELECT * FROM table ORDER BY col DESC LIMIT 10

-- Update
UPDATE table SET col = ? WHERE id = ?

-- Delete
DELETE FROM table WHERE id = ?

-- Soft delete (preferred)
UPDATE table SET active = 0 WHERE id = ?
```

---

## Aggregates

```sql
COUNT(*)         -- row count
AVG(salary)      -- average
SUM(salary)      -- total
MAX(salary)      -- highest
MIN(salary)      -- lowest
ROUND(val, 2)    -- round to 2 decimals

-- Group by category
SELECT dept, AVG(salary) FROM employees GROUP BY dept
```

---

## Table Creation

```sql
CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT    NOT NULL,
    email    TEXT    UNIQUE,
    age      INTEGER CHECK(age > 0),
    created  TEXT    DEFAULT (datetime('now'))
);
```

---

## Repository Pattern

```python
def get_all():
    with connect() as conn:
        return conn.execute("SELECT * FROM items").fetchall()

def get_by_id(item_id: int):
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM items WHERE id = ?", (item_id,)
        ).fetchone()

def create(name: str, price: float) -> int:
    with connect() as conn:
        cursor = conn.execute(
            "INSERT INTO items (name, price) VALUES (?, ?)", (name, price)
        )
        conn.commit()
        return cursor.lastrowid

def update(item_id: int, **fields) -> bool:
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [item_id]
    with connect() as conn:
        cursor = conn.execute(
            f"UPDATE items SET {set_clause} WHERE id = ?", values
        )
        conn.commit()
        return cursor.rowcount > 0
```
