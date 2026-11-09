# ⚡ Phase 09 Cheat Sheet — Databases

---

## sqlite3 Connection Setup

```python
import sqlite3

# File-based database (persists between runs)
conn = sqlite3.connect("mydb.db")

# In-memory database (destroyed when connection closes)
conn = sqlite3.connect(":memory:")

# Enable column-name row access (set BEFORE any queries)
conn.row_factory = sqlite3.Row

# Context manager — auto-commits on success, rolls back on exception
with sqlite3.connect("mydb.db") as conn:
    conn.execute("...")

# Always close when done (if not using 'with')
conn.close()
```

---

## CREATE TABLE

```sql
CREATE TABLE IF NOT EXISTS students (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT    NOT NULL,
    email TEXT    UNIQUE,
    grade REAL    CHECK(grade >= 0.0 AND grade <= 4.0),
    age   INTEGER DEFAULT 18
);

-- Table with a FOREIGN KEY
CREATE TABLE IF NOT EXISTS orders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product     TEXT    NOT NULL,
    amount      REAL    NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

---

## CRUD (INSERT / SELECT / UPDATE / DELETE with ?)

```python
# INSERT — always use ? placeholders, never f-strings
conn.execute(
    "INSERT INTO students (name, grade) VALUES (?, ?)",
    ("Alice", 3.8)
)
conn.commit()                           # persist the write

# Batch INSERT
conn.executemany(
    "INSERT INTO students (name, grade) VALUES (?, ?)",
    [("Bob", 3.2), ("Carol", 3.9)]
)
conn.commit()

# SELECT — all rows
rows = conn.execute("SELECT * FROM students ORDER BY name").fetchall()

# SELECT — one row
row = conn.execute(
    "SELECT * FROM students WHERE id = ?", (1,)
).fetchone()                            # returns None if not found

# SELECT — with ORDER BY and LIMIT
rows = conn.execute(
    "SELECT name, grade FROM students ORDER BY grade DESC LIMIT 5"
).fetchall()

# UPDATE — check rowcount to confirm a row was matched
cursor = conn.execute(
    "UPDATE students SET grade = ? WHERE id = ?", (3.9, 1)
)
conn.commit()
print(cursor.rowcount)                  # 1 if updated, 0 if not found

# DELETE
cursor = conn.execute(
    "DELETE FROM students WHERE id = ?", (1,)
)
conn.commit()
print(cursor.rowcount)                  # 1 if deleted, 0 if not found

# Get the ID of the last inserted row
cursor = conn.execute(
    "INSERT INTO students (name, grade) VALUES (?, ?)", ("Dave", 3.5)
)
new_id = cursor.lastrowid
```

---

## JOINs

```sql
-- INNER JOIN: only rows matching on BOTH sides
SELECT o.id, o.product, c.name, c.email
FROM   orders o
INNER JOIN customers c ON o.customer_id = c.id;

-- LEFT JOIN: all rows from left table; NULL for unmatched right-side columns
SELECT c.name, COUNT(o.id) AS order_count
FROM   customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name;

-- Find rows with NO match on the right side
SELECT c.name
FROM   customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE  o.id IS NULL;

-- Three-table JOIN through a junction table
SELECT s.name, c.name AS course, e.grade
FROM   enrollments e
INNER JOIN students s ON e.student_id = s.id
INNER JOIN courses  c ON e.course_id  = c.id;
```

---

## Aggregation

```sql
-- Basic aggregates
SELECT COUNT(*), AVG(grade), MAX(grade), MIN(grade)
FROM students;

-- GROUP BY: one summary row per group
SELECT department, COUNT(*) AS headcount, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;

-- HAVING: filter groups AFTER aggregation (WHERE filters rows BEFORE)
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 80000;

-- WHERE vs HAVING
-- WHERE salary > 50000       ← filters individual rows first
-- HAVING AVG(salary) > 80000 ← filters aggregated groups
```

---

## Transactions

```python
# Default isolation level — Python auto-wraps DML in an implicit transaction
conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (500, 1))
conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (500, 2))
conn.commit()    # both UPDATEs saved atomically

# Rollback on error
try:
    conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
    row = conn.execute("SELECT balance FROM accounts WHERE id = ?", (from_id,)).fetchone()
    if row[0] < 0:
        raise ValueError("Insufficient funds")
    conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
    conn.commit()
except Exception as e:
    conn.rollback()   # undo all pending changes
    print(f"Transaction failed: {e}")
```

---

## sqlite3.Row

```python
conn.row_factory = sqlite3.Row          # enable once per connection

row = conn.execute(
    "SELECT id, name, grade FROM students WHERE id = ?", (1,)
).fetchone()

# Access by column name (preferred — resilient to column reordering)
print(row["name"], row["grade"])

# Access by index (works, but fragile)
print(row[1], row[2])

# Convert to a plain dict (works with json.dumps, csv.DictWriter, etc.)
d = dict(row)                           # {'id': 1, 'name': 'Alice', 'grade': 3.8}

# Convert all rows to a list of dicts
rows = conn.execute("SELECT * FROM students").fetchall()
students = [dict(r) for r in rows]
```

---

## SQLAlchemy Quick Start

```python
# pip install sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()

# Define ORM models
class Author(Base):
    __tablename__ = "authors"
    id    = Column(Integer, primary_key=True)
    name  = Column(String, nullable=False)
    books = relationship("Book", back_populates="author")  # one-to-many

class Book(Base):
    __tablename__ = "books"
    id        = Column(Integer, primary_key=True)
    title     = Column(String, nullable=False)
    year      = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author    = relationship("Author", back_populates="books")  # many-to-one

# Create engine and tables
engine = create_engine("sqlite:///:memory:")   # file: "sqlite:///mydb.db"
Base.metadata.create_all(engine)

# Session CRUD
with Session(engine) as session:
    # INSERT
    author = Author(name="George Orwell", nationality="British")
    session.add(author)
    session.flush()                        # assigns ID without committing

    book = Book(title="Animal Farm", year=1945, author_id=author.id)
    session.add(book)
    session.commit()

    # SELECT all
    all_books = session.query(Book).all()

    # FILTER
    books = session.query(Book).filter_by(author_id=author.id).all()

    # GET by primary key
    b = session.get(Book, 1)

    # UPDATE
    b.year = 1946
    session.commit()

    # DELETE
    session.delete(b)
    session.commit()
```
