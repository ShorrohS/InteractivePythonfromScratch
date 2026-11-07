# Phase 09 — Beginner Solutions: Databases

---

## Q1. Create students table

```python
import sqlite3

conn = sqlite3.connect("school.db")
conn.row_factory = sqlite3.Row
conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT    NOT NULL,
        age   INTEGER NOT NULL,
        grade REAL    CHECK(grade >= 0 AND grade <= 4.0)
    )
""")
conn.commit()
```

---

## Q2. add_student (parameterized)

```python
def add_student(name: str, age: int, grade: float) -> int:
    with sqlite3.connect("school.db") as conn:
        cursor = conn.execute(
            "INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
            (name, age, grade)
        )
        conn.commit()
        return cursor.lastrowid
```

---

## Q3. get_all_students

```python
def get_all_students() -> list[dict]:
    conn = sqlite3.connect("school.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM students ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]
```

---

## Q4. get_student_by_id

```python
def get_student_by_id(sid: int) -> dict | None:
    conn = sqlite3.connect("school.db")
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM students WHERE id = ?", (sid,)).fetchone()
    conn.close()
    return dict(row) if row else None
```

---

## Q5. update_grade

```python
def update_grade(sid: int, new_grade: float) -> bool:
    with sqlite3.connect("school.db") as conn:
        cursor = conn.execute(
            "UPDATE students SET grade = ? WHERE id = ?", (new_grade, sid)
        )
        conn.commit()
        return cursor.rowcount > 0
```

---

## Q6. delete_student

```python
def delete_student(sid: int) -> bool:
    with sqlite3.connect("school.db") as conn:
        cursor = conn.execute("DELETE FROM students WHERE id = ?", (sid,))
        conn.commit()
        return cursor.rowcount > 0
```

---

## Q7. honour_roll

```python
def honour_roll() -> list[dict]:
    conn = sqlite3.connect("school.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM students WHERE grade >= 3.5 ORDER BY grade DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
```

---

## Q8. class_stats

```python
def class_stats() -> dict:
    conn = sqlite3.connect("school.db")
    conn.row_factory = sqlite3.Row
    row = conn.execute("""
        SELECT COUNT(*) AS count,
               ROUND(AVG(grade), 2) AS avg,
               MAX(grade) AS max,
               MIN(grade) AS min
        FROM students
    """).fetchone()
    conn.close()
    return dict(row) if row else {}
```

---

## Q9. SQL Injection bug

The code directly injects user input into the SQL string. If name = `"' OR '1'='1"` it could return all rows. If name = `"'; DROP TABLE students; --"` it could destroy the table.

Fix: always use parameterized queries:
```python
conn.execute("SELECT * FROM students WHERE name = ?", (name,))
```

---

## Q10. row_factory = sqlite3.Row

Without it, fetchone/fetchall returns tuples — you access data by index `row[0]`, `row[1]` — brittle if column order changes.

With `conn.row_factory = sqlite3.Row`:
- Access by column name: `row["name"]`, `row["salary"]`
- Much more readable and maintainable
- Can convert to dict with: `dict(row)`
