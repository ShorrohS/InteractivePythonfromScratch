# Lesson 04 — Advanced Queries: JOINs, Filtering, Aggregation

**Phase:** 09 — Databases | **Time:** ~55 min

---

## Part 1: Setting Up the Practice Database

All examples in this lesson use a three-table HR database. Run this setup block once.

```python
import sqlite3

DB = "hr.db"

def setup_database() -> None:
    """Create and populate the HR practice database."""
    with sqlite3.connect(DB) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS departments (
                id      INTEGER PRIMARY KEY,
                name    TEXT    NOT NULL UNIQUE,
                budget  REAL    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS employees (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                email       TEXT    UNIQUE,
                department  TEXT    NOT NULL,
                salary      REAL    NOT NULL,
                hire_date   TEXT    NOT NULL,
                active      INTEGER DEFAULT 1,
                FOREIGN KEY (department) REFERENCES departments(name)
            );

            CREATE TABLE IF NOT EXISTS projects (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                dept_name   TEXT    NOT NULL,
                budget      REAL    NOT NULL,
                FOREIGN KEY (dept_name) REFERENCES departments(name)
            );

            INSERT OR IGNORE INTO departments VALUES
                (1, 'Engineering', 1200000),
                (2, 'Sales',        800000),
                (3, 'Marketing',    400000),
                (4, 'HR',           200000);

            INSERT OR IGNORE INTO employees
                (name, email, department, salary, hire_date) VALUES
                ('Alice Chen',   'alice@co.com',  'Engineering', 95000, '2021-03-15'),
                ('Bob Ross',     'bob@co.com',    'Sales',       68000, '2022-01-10'),
                ('Carol Davis',  'carol@co.com',  'Engineering', 88000, '2020-06-01'),
                ('Dave Kim',     'dave@co.com',   'Marketing',   72000, '2023-02-28'),
                ('Eve Martinez', 'eve@co.com',    'Sales',       74000, '2021-11-05'),
                ('Frank Liu',    'frank@co.com',  'Engineering', 102000,'2019-08-20'),
                ('Grace Park',   'grace@co.com',  'HR',          61000, '2022-09-14'),
                ('Hank Moore',   NULL,            'Sales',       59000, '2023-05-01');

            INSERT OR IGNORE INTO projects (title, dept_name, budget) VALUES
                ('Cloud Migration', 'Engineering', 350000),
                ('CRM Rollout',     'Sales',       120000),
                ('Brand Refresh',   'Marketing',    85000),
                ('AI Analytics',    'Engineering', 480000);
        """)

setup_database()

def run_query(sql: str, params: tuple = ()) -> list[dict]:
    """Execute a SELECT query and return rows as a list of dicts."""
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row   # Access columns by name
        cur = conn.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]
```

---

## Part 2: INNER JOIN and LEFT JOIN

```python
# INNER JOIN — only employees whose department has a matching departments row
results = run_query("""
    SELECT e.name, e.salary, d.budget AS dept_budget
    FROM employees e
    INNER JOIN departments d ON e.department = d.name
    WHERE e.active = 1
    ORDER BY e.salary DESC
""")
for row in results:
    print(f"{row['name']:15} ${row['salary']:>9,.0f}   dept budget ${row['dept_budget']:>12,.0f}")

# LEFT JOIN — all employees, NULL dept_budget if no matching department row
results = run_query("""
    SELECT e.name, e.department, d.budget AS dept_budget
    FROM employees e
    LEFT JOIN departments d ON e.department = d.name
""")
```

**INNER JOIN** returns only rows where both tables have a match — employees with no matching department row are excluded.
**LEFT JOIN** keeps every row from the left table (`employees`) and fills NULLs for missing right-table data. Use it whenever you want "all from the left, optionally matched on the right."

RIGHT JOIN works the opposite way — all rows from the right table, optional match on the left. SQLite does not natively support RIGHT JOIN; flip the table order and use LEFT JOIN instead.

---

## Part 3: Joining Three Tables

```python
# Employees with their department budget and assigned projects
results = run_query("""
    SELECT
        e.name          AS employee,
        e.salary,
        d.name          AS department,
        d.budget        AS dept_budget,
        p.title         AS project,
        p.budget        AS project_budget
    FROM employees e
    INNER JOIN departments d ON e.department  = d.name
    LEFT JOIN  projects    p ON p.dept_name   = d.name
    WHERE e.active = 1
    ORDER BY d.name, e.name
""")
for row in results:
    project = row["project"] or "— no project —"
    print(f"{row['department']:12} | {row['employee']:15} | {project}")
```

Chain as many JOINs as needed — each one adds columns from the joined table. Use aliases (`e`, `d`, `p`) to keep column references readable.

---

## Part 4: WHERE Clause Operators

```python
# Exact match and inequality
run_query("SELECT * FROM employees WHERE department = ?",    ("Engineering",))
run_query("SELECT * FROM employees WHERE salary != ?",       (65000,))

# BETWEEN — inclusive on both ends
run_query("SELECT * FROM employees WHERE salary BETWEEN ? AND ?", (70000, 95000))

# IN and NOT IN — list membership
run_query("SELECT * FROM employees WHERE department IN (?, ?)",     ("Engineering", "Sales"))
run_query("SELECT * FROM employees WHERE department NOT IN (?)",    ("HR",))

# LIKE — pattern matching (% = any characters, _ = exactly one character)
run_query("SELECT * FROM employees WHERE name LIKE ?",  ("A%",))     # starts with A
run_query("SELECT * FROM employees WHERE email LIKE ?", ("%@co%",))  # contains @co

# NULL checks — always use IS NULL / IS NOT NULL, never = NULL
run_query("SELECT * FROM employees WHERE email IS NULL")
run_query("SELECT * FROM employees WHERE email IS NOT NULL")

# Combining conditions with AND / OR
run_query("""
    SELECT * FROM employees
    WHERE (department = ? OR department = ?)
      AND salary > ?
      AND active = 1
""", ("Engineering", "Marketing", 80000))
```

---

## Part 5: ORDER BY, LIMIT, and OFFSET (Pagination)

```python
# Single column — highest salary first
run_query("SELECT name, salary FROM employees ORDER BY salary DESC")

# Multiple columns — department alphabetically, then salary high-to-low within each dept
run_query("""
    SELECT name, department, salary
    FROM employees
    ORDER BY department ASC, salary DESC
""")

# Top 3 earners
run_query("SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3")

# Pagination — page 2, 3 rows per page
PAGE_SIZE = 3
page      = 2
offset    = (page - 1) * PAGE_SIZE   # page 2 → skip first 3 rows

results = run_query(
    "SELECT name, salary FROM employees ORDER BY name LIMIT ? OFFSET ?",
    (PAGE_SIZE, offset)
)
```

`LIMIT` controls how many rows to return. `OFFSET` skips the first N rows. The formula `(page - 1) * page_size` is the standard pagination pattern — page 1 → offset 0, page 2 → offset 3, and so on.

---

## Part 6: GROUP BY and Aggregate Functions

```python
# Headcount, payroll and salary range per department
results = run_query("""
    SELECT
        department,
        COUNT(*)               AS headcount,
        ROUND(AVG(salary), 0)  AS avg_salary,
        SUM(salary)            AS total_payroll,
        MIN(salary)            AS min_salary,
        MAX(salary)            AS max_salary
    FROM employees
    WHERE active = 1
    GROUP BY department
    ORDER BY total_payroll DESC
""")
for row in results:
    print(
        f"{row['department']:12} | {row['headcount']} staff | "
        f"avg ${row['avg_salary']:>7,.0f} | payroll ${row['total_payroll']:>9,.0f}"
    )
```

`GROUP BY` collapses all rows with the same department value into one summary row. Every column in SELECT must either appear in GROUP BY or be wrapped in an aggregate function (`COUNT`, `AVG`, `SUM`, `MIN`, `MAX`).

---

## Part 7: HAVING — Filtering Aggregated Groups

```python
# Departments with average salary above $75,000
run_query("""
    SELECT department, ROUND(AVG(salary), 0) AS avg_salary
    FROM employees
    WHERE active = 1
    GROUP BY department
    HAVING avg_salary > 75000
    ORDER BY avg_salary DESC
""")

# Departments with more than two active employees
run_query("""
    SELECT department, COUNT(*) AS headcount
    FROM employees
    WHERE active = 1
    GROUP BY department
    HAVING headcount > 2
""")
```

**WHERE** filters individual rows before aggregation.
**HAVING** filters groups after aggregation — it can reference aggregate results like `avg_salary` or `COUNT(*)`. You cannot use aggregate results in a WHERE clause.

---

## Part 8: Subqueries

```python
# Employees earning above the company-wide average
above_avg = run_query("""
    SELECT name, salary
    FROM employees
    WHERE salary > (SELECT AVG(salary) FROM employees WHERE active = 1)
      AND active = 1
    ORDER BY salary DESC
""")

# Departments that have at least one assigned project
active_depts = run_query("""
    SELECT name
    FROM departments
    WHERE name IN (SELECT DISTINCT dept_name FROM projects)
""")

# Employees in departments with no current project (subquery + NOT IN)
no_project_employees = run_query("""
    SELECT name, department
    FROM employees
    WHERE department NOT IN (SELECT DISTINCT dept_name FROM projects)
      AND active = 1
""")
```

A subquery inside parentheses runs first and its result feeds the outer query. Keep subqueries simple — complex multi-step logic is usually clearer as a JOIN.

---

## Part 9: Practical Business Queries

```python
# Top 5 earners with their department's budget
top_earners = run_query("""
    SELECT e.name, e.salary, e.department, d.budget AS dept_budget
    FROM employees e
    INNER JOIN departments d ON e.department = d.name
    WHERE e.active = 1
    ORDER BY e.salary DESC
    LIMIT 5
""")

# Employees hired in a specific date range
hired_in_2022 = run_query("""
    SELECT name, hire_date, department
    FROM employees
    WHERE hire_date BETWEEN ? AND ?
    ORDER BY hire_date
""", ("2022-01-01", "2022-12-31"))

# Departments above the $75k average salary threshold
high_pay_depts = run_query("""
    SELECT
        department,
        COUNT(*)               AS headcount,
        ROUND(AVG(salary), 0)  AS avg_salary
    FROM employees
    WHERE active = 1
    GROUP BY department
    HAVING avg_salary > 75000
    ORDER BY avg_salary DESC
""")

# Departments with no active employees (LEFT JOIN + NULL check)
empty_depts = run_query("""
    SELECT d.name
    FROM departments d
    LEFT JOIN employees e ON e.department = d.name AND e.active = 1
    WHERE e.id IS NULL
""")

# Products (or employees) below a reorder threshold — using a parameter
REORDER_LEVEL = 70000
low_salary = run_query("""
    SELECT name, salary, department
    FROM employees
    WHERE salary < ? AND active = 1
    ORDER BY salary ASC
""", (REORDER_LEVEL,))

print("High-paying departments:")
for dept in high_pay_depts:
    print(f"  {dept['department']:12} — {dept['headcount']} staff, avg ${dept['avg_salary']:,.0f}")

print("\nTop 5 earners:")
for emp in top_earners:
    print(f"  {emp['name']:15} ${emp['salary']:>8,.0f}")
```

---

## Practice Exercises

1. Write a `get_top_earners_by_dept(department: str, n: int) -> list[dict]` function that returns the top `n` earners within a specific department.

2. Write a query that returns employees hired in the last 365 days using `date('now', '-365 days')` as the cutoff date (no Python datetime needed — SQLite handles it).

3. Write a `get_employees_paginated(page: int, page_size: int) -> list[dict]` function that returns the correct page of active employees sorted by name.

4. Write a query that finds departments where the total project budget exceeds the department's own budget. Join the `departments` and `projects` tables, group by department, and use HAVING.

---

## Next Lesson

**[Lesson 05 → ORM Basics with SQLAlchemy](lesson-05-orm-basics.md)**
