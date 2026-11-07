"""
Demo 01 - SQL Basics with SQLite
Phase 09: Databases

Run: python demo-01-sql-basics.py
"""

import sqlite3
import os

DB = ":memory:"   # in-memory database — no file created

print("=" * 55)
print("DEMO 01 - SQL Fundamentals with SQLite")
print("=" * 55)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row   # access columns by name

# --- CREATE TABLE ---
print("\n1. CREATE TABLE:")
conn.execute("""
    CREATE TABLE employees (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        department  TEXT    NOT NULL,
        salary      REAL    NOT NULL,
        active      INTEGER DEFAULT 1
    )
""")
print("  Table 'employees' created.")

# --- INSERT ---
print("\n2. INSERT data:")
employees = [
    ("Alice Johnson",  "Engineering", 85000),
    ("Bob Smith",      "Sales",       65000),
    ("Carol Davis",    "Engineering", 92000),
    ("Dave Wilson",    "Marketing",   71000),
    ("Eve Martinez",   "Sales",       68000),
    ("Frank Lee",      "Engineering", 78000),
    ("Grace Kim",      "Marketing",   82000),
]

conn.executemany(
    "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
    employees
)
conn.commit()
print(f"  Inserted {len(employees)} employees.")

# --- SELECT ALL ---
print("\n3. SELECT all:")
rows = conn.execute("SELECT * FROM employees").fetchall()
for r in rows:
    print(f"  [{r['id']}] {r['name']:<22} {r['department']:<14} ${r['salary']:,}")

# --- WHERE ---
print("\n4. WHERE clause:")
eng = conn.execute(
    "SELECT name, salary FROM employees WHERE department = ?", ("Engineering",)
).fetchall()
print("  Engineering dept:")
for r in eng:
    print(f"    {r['name']}: ${r['salary']:,}")

# --- ORDER BY ---
print("\n5. ORDER BY salary DESC:")
top = conn.execute(
    "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3"
).fetchall()
for i, r in enumerate(top, 1):
    print(f"  #{i} {r['name']}: ${r['salary']:,}")

# --- AGGREGATE ---
print("\n6. Aggregate functions:")
stats = conn.execute("""
    SELECT
        COUNT(*)            AS total,
        ROUND(AVG(salary))  AS avg_sal,
        MAX(salary)         AS max_sal,
        MIN(salary)         AS min_sal,
        SUM(salary)         AS payroll
    FROM employees
""").fetchone()
print(f"  Total:   {stats['total']}")
print(f"  Average: ${stats['avg_sal']:,.0f}")
print(f"  Highest: ${stats['max_sal']:,}")
print(f"  Lowest:  ${stats['min_sal']:,}")
print(f"  Payroll: ${stats['payroll']:,}")

# --- GROUP BY ---
print("\n7. GROUP BY department:")
depts = conn.execute("""
    SELECT department, COUNT(*) AS count, ROUND(AVG(salary)) AS avg
    FROM employees
    GROUP BY department
    ORDER BY avg DESC
""").fetchall()
print(f"  {'Dept':<15} {'Count':>6} {'Avg Salary':>12}")
for d in depts:
    print(f"  {d['department']:<15} {d['count']:>6} ${d['avg']:>11,.0f}")

# --- UPDATE ---
print("\n8. UPDATE:")
conn.execute("UPDATE employees SET salary = 90000 WHERE name = 'Alice Johnson'")
conn.commit()
alice = conn.execute("SELECT salary FROM employees WHERE name='Alice Johnson'").fetchone()
print(f"  Alice's new salary: ${alice['salary']:,}")

# --- DELETE ---
print("\n9. DELETE (soft delete — flag inactive):")
conn.execute("UPDATE employees SET active = 0 WHERE department = 'Marketing'")
conn.commit()
active_count = conn.execute("SELECT COUNT(*) FROM employees WHERE active=1").fetchone()[0]
print(f"  Active employees after soft-delete Marketing: {active_count}")

conn.close()
print("\n  Demo complete. Database was in-memory (no file created).")
print("=" * 55)
