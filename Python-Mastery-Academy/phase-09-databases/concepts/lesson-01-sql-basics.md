# Lesson 01 — SQL Fundamentals

**Phase:** 09 — Databases | **Time:** ~40 min

---

## Part 1: Why Databases?

Files (JSON/CSV) work for small data. Databases handle:
- Millions of records efficiently
- Multiple users simultaneously
- Complex queries across related tables
- ACID transactions (Atomic, Consistent, Isolated, Durable)

---

## Part 2: SQL — The Language of Databases

SQL (Structured Query Language) is used by all relational databases.

```sql
-- Comments in SQL use --
SELECT name, salary FROM employees WHERE dept = 'Engineering';
```

Every SQL statement is either:
- **DDL** — Data Definition Language: `CREATE`, `DROP`, `ALTER`
- **DML** — Data Manipulation Language: `INSERT`, `UPDATE`, `DELETE`, `SELECT`

---

## Part 3: CREATE TABLE

```sql
CREATE TABLE employees (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name  TEXT    NOT NULL,
    last_name   TEXT    NOT NULL,
    email       TEXT    UNIQUE,
    department  TEXT    NOT NULL,
    salary      REAL    NOT NULL CHECK (salary >= 0),
    hire_date   TEXT    DEFAULT (date('now')),
    active      INTEGER DEFAULT 1
);
```

**Constraints:**
| Constraint | Meaning |
|-----------|---------|
| `PRIMARY KEY` | Unique identifier, never NULL |
| `NOT NULL` | Cannot be empty |
| `UNIQUE` | No duplicate values |
| `DEFAULT` | Value if not provided |
| `CHECK` | Must satisfy condition |

---

## Part 4: INSERT — Add Data

```sql
-- Insert one row
INSERT INTO employees (first_name, last_name, email, department, salary)
VALUES ('Alice', 'Johnson', 'alice@co.com', 'Engineering', 85000);

-- Insert multiple rows
INSERT INTO employees (first_name, last_name, department, salary) VALUES
    ('Bob',   'Smith',  'Sales',       65000),
    ('Carol', 'Davis',  'Engineering', 92000),
    ('Dave',  'Wilson', 'Marketing',   71000);
```

---

## Part 5: SELECT — Read Data

```sql
-- All columns, all rows
SELECT * FROM employees;

-- Specific columns
SELECT first_name, last_name, salary FROM employees;

-- With condition
SELECT * FROM employees WHERE department = 'Engineering';

-- Multiple conditions
SELECT * FROM employees
WHERE department = 'Engineering' AND salary > 80000;

-- Comparison operators
WHERE salary > 70000
WHERE salary BETWEEN 60000 AND 90000
WHERE department IN ('Engineering', 'Sales')
WHERE last_name LIKE 'J%'    -- starts with J
WHERE email IS NOT NULL

-- ORDER BY
SELECT * FROM employees ORDER BY salary DESC;
SELECT * FROM employees ORDER BY last_name ASC, first_name ASC;

-- LIMIT
SELECT * FROM employees ORDER BY salary DESC LIMIT 5;

-- DISTINCT — remove duplicates
SELECT DISTINCT department FROM employees;
```

---

## Part 6: UPDATE — Modify Data

```sql
-- Update one field
UPDATE employees SET salary = 90000 WHERE id = 1;

-- Update multiple fields
UPDATE employees
SET salary = 95000, department = 'Senior Engineering'
WHERE email = 'alice@co.com';

-- Update all rows (careful!)
UPDATE employees SET active = 0 WHERE department = 'Temp';
```

---

## Part 7: DELETE — Remove Data

```sql
-- Delete specific row
DELETE FROM employees WHERE id = 5;

-- Delete with condition
DELETE FROM employees WHERE active = 0;

-- Soft delete (preferred in business apps)
UPDATE employees SET active = 0 WHERE id = 5;
-- Never truly deletes — audit trail preserved
```

---

## Part 8: Aggregate Functions

```sql
SELECT COUNT(*)         AS total_employees  FROM employees;
SELECT COUNT(DISTINCT department) AS dept_count FROM employees;
SELECT AVG(salary)      AS avg_salary       FROM employees;
SELECT MAX(salary)      AS top_salary       FROM employees;
SELECT MIN(salary)      AS min_salary       FROM employees;
SELECT SUM(salary)      AS total_payroll    FROM employees;

-- GROUP BY — aggregate per group
SELECT department,
       COUNT(*)         AS headcount,
       ROUND(AVG(salary), 2) AS avg_salary,
       SUM(salary)      AS total_payroll
FROM employees
WHERE active = 1
GROUP BY department
ORDER BY total_payroll DESC;

-- HAVING — filter on aggregated results
SELECT department, AVG(salary) AS avg
FROM employees
GROUP BY department
HAVING avg > 75000;
```

---

## Part 9: JOINs

```sql
-- Create a related table
CREATE TABLE departments (
    id      INTEGER PRIMARY KEY,
    name    TEXT UNIQUE,
    manager TEXT
);

-- INNER JOIN — only matching rows
SELECT e.first_name, e.last_name, e.salary, d.manager
FROM employees e
JOIN departments d ON e.department = d.name;

-- LEFT JOIN — all from left + matching from right
SELECT e.first_name, d.manager
FROM employees e
LEFT JOIN departments d ON e.department = d.name;
```

---

## Practice Exercises (in SQL)

1. Write SQL to get all employees in the Engineering department sorted by salary descending.

2. Write SQL to find the average salary per department.

3. Write SQL to update the salary of employee with id=3 to 95000.

4. Write SQL to find all employees earning more than the average salary.

---

## Next Lesson

**[Lesson 02 → SQLite with Python](lesson-02-sqlite.md)**
