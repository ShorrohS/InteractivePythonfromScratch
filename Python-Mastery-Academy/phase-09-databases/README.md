# 🗄️ Phase 09 — Databases

> **Goal:** Store and retrieve data permanently using SQL databases.

---

## Why Databases?

Files are fine for small amounts of data. Databases handle:
- Millions of records efficiently
- Multiple users at the same time
- Complex queries (find all employees in Sales earning > $70k)
- Relationships between data tables
- Transactions (all-or-nothing operations)

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-sql-basics.md](concepts/lesson-01-sql-basics.md) | SQL fundamentals |
| 02 | [lesson-02-sqlite.md](concepts/lesson-02-sqlite.md) | SQLite with Python |
| 03 | [lesson-03-crud.md](concepts/lesson-03-crud.md) | CRUD operations |
| 04 | [lesson-04-queries.md](concepts/lesson-04-queries.md) | Advanced queries |
| 05 | [lesson-05-postgresql.md](concepts/lesson-05-postgresql.md) | PostgreSQL basics |

---

## Core Concepts

```python
import sqlite3

# Connect
conn = sqlite3.connect("students.db")
conn.row_factory = sqlite3.Row    # Access columns by name
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade TEXT,
        score REAL
    )
""")

# Insert (ALWAYS use parameterized queries — prevents SQL injection)
cursor.execute("INSERT INTO students (name, grade, score) VALUES (?, ?, ?)",
               ("Alice", "A", 95.5))
conn.commit()

# Query
cursor.execute("SELECT * FROM students WHERE score > ?", (80,))
rows = cursor.fetchall()
for row in rows:
    print(row["name"], row["score"])

# Update
cursor.execute("UPDATE students SET score = ? WHERE name = ?", (98.0, "Alice"))
conn.commit()

# Delete
cursor.execute("DELETE FROM students WHERE name = ?", ("Alice",))
conn.commit()

# Always close
conn.close()
```

---

## SQL Quick Reference

```sql
-- Create
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT,
    salary REAL,
    hire_date TEXT
);

-- Insert
INSERT INTO employees (name, department, salary) VALUES ('Alice', 'Engineering', 85000);

-- Read
SELECT * FROM employees;
SELECT name, salary FROM employees WHERE salary > 70000;
SELECT * FROM employees ORDER BY salary DESC;
SELECT * FROM employees LIMIT 10;

-- Update
UPDATE employees SET salary = 90000 WHERE name = 'Alice';

-- Delete
DELETE FROM employees WHERE id = 5;

-- Aggregate
SELECT COUNT(*), AVG(salary), MAX(salary), MIN(salary) FROM employees;
SELECT department, AVG(salary) FROM employees GROUP BY department;

-- Join
SELECT e.name, d.manager 
FROM employees e 
JOIN departments d ON e.department = d.name;
```

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [Student App](guided-projects/project-01-student-app/) | Full CRUD student management |
| [Inventory App](guided-projects/project-02-inventory-app/) | Product inventory system |

---

## ⚠️ SQL Injection Prevention

```python
# NEVER do this (vulnerable to SQL injection):
name = input("Name: ")
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
# If name = "'; DROP TABLE users; --" → CATASTROPHIC

# ALWAYS use parameterized queries:
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

---

## ✅ Completion Checklist

- [ ] Understand SQL SELECT, INSERT, UPDATE, DELETE
- [ ] Can create tables with constraints
- [ ] Always use parameterized queries
- [ ] Can use aggregates (COUNT, AVG, SUM, MAX, MIN)
- [ ] Can perform basic JOIN operations
- [ ] Built Student App and Inventory App

---

## Previous: [Phase 08](../phase-08-intermediate-projects/) | Next: [Phase 10](../phase-10-web-scraping/README.md)
