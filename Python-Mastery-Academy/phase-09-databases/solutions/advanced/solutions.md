# Phase 09 — Advanced Solutions: Databases

---

## Q1. SQLAlchemy ORM Models

```python
# pip install sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id          = Column(Integer, primary_key=True)
    name        = Column(String, nullable=False)
    nationality = Column(String)
    # One author → many books (back_populates wires the reverse side)
    books       = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(name={self.name!r}, nationality={self.nationality!r})>"


class Book(Base):
    __tablename__ = "books"

    id        = Column(Integer, primary_key=True)
    title     = Column(String, nullable=False)
    year      = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))   # FK to authors.id
    # Many books → one author
    author    = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book(title={self.title!r}, year={self.year})>"


# create_engine with echo=False keeps output clean
engine = create_engine("sqlite:///:memory:")

# Create all tables defined on Base in the correct dependency order
Base.metadata.create_all(engine)

print("Tables created:", Base.metadata.tables.keys())
# dict_keys(['authors', 'books'])
```

**Explanation:** `declarative_base()` returns a base class that tracks all subclasses as ORM models. Each model class maps to one table; `Column` defines a column's type and constraints. `ForeignKey("authors.id")` creates the relational link at the SQL level, while `relationship()` exposes it as a Python attribute. `create_all` issues `CREATE TABLE IF NOT EXISTS` statements in the correct order, so `books` (which depends on `authors`) is created second.

---

## Q2. SQLAlchemy Session CRUD

```python
# pip install sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
    id          = Column(Integer, primary_key=True)
    name        = Column(String, nullable=False)
    nationality = Column(String)
    books       = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"
    id        = Column(Integer, primary_key=True)
    title     = Column(String, nullable=False)
    year      = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author    = relationship("Author", back_populates="books")


engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    # ── INSERT ──────────────────────────────────────────────
    authors = [
        Author(name="J.K. Rowling",   nationality="British"),
        Author(name="George Orwell",   nationality="British"),
        Author(name="Haruki Murakami", nationality="Japanese"),
    ]
    session.add_all(authors)
    session.flush()   # write to DB and assign primary key IDs without committing

    books = [
        Book(title="Harry Potter and the Philosopher's Stone",
             year=1997, author_id=authors[0].id),
        Book(title="Harry Potter and the Chamber of Secrets",
             year=1998, author_id=authors[0].id),
        Book(title="Nineteen Eighty-Four", year=1949, author_id=authors[1].id),
        Book(title="Animal Farm",          year=1945, author_id=authors[1].id),
        Book(title="Norwegian Wood",       year=1987, author_id=authors[2].id),
    ]
    session.add_all(books)
    session.commit()

    # ── SELECT ALL ──────────────────────────────────────────
    all_books = session.query(Book).all()
    print(f"All books: {len(all_books)}")                        # 5

    # ── FILTER BY ───────────────────────────────────────────
    rowling_books = session.query(Book).filter_by(
        author_id=authors[0].id
    ).all()
    print(f"Rowling's books: {len(rowling_books)}")             # 2

    # ── GET BY PRIMARY KEY ──────────────────────────────────
    book = session.get(Book, 3)
    print(f"Book id=3: {book.title}")                           # Nineteen Eighty-Four

    # ── UPDATE ──────────────────────────────────────────────
    book.year = 1948                # mutate the attribute directly
    session.commit()
    updated = session.get(Book, 3)
    print(f"Updated year: {updated.year}")                      # 1948

    # ── DELETE ──────────────────────────────────────────────
    to_delete = session.get(Book, 5)   # Norwegian Wood
    session.delete(to_delete)
    session.commit()
    print(f"Books after delete: {session.query(Book).count()}")  # 4
```

**Explanation:** `Session` is the unit-of-work object — it tracks all changes and flushes them to the database on `commit()`. `flush()` sends pending SQL to the database within the current transaction (so IDs are assigned) without permanently committing. `session.get(Model, pk)` is the recommended primary-key lookup in SQLAlchemy 2.x; `session.delete(obj)` marks the object for deletion on the next commit.

---

## Q3. Three-Table JOIN

```python
import sqlite3

conn = sqlite3.connect(":memory:")

# Three related tables
conn.execute("""
    CREATE TABLE students (
        id   INTEGER PRIMARY KEY,
        name TEXT    NOT NULL
    )
""")
conn.execute("""
    CREATE TABLE courses (
        id   INTEGER PRIMARY KEY,
        name TEXT    NOT NULL
    )
""")
conn.execute("""
    CREATE TABLE enrollments (
        student_id INTEGER NOT NULL,
        course_id  INTEGER NOT NULL,
        grade      REAL    NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id)  REFERENCES courses(id)
    )
""")

conn.executemany("INSERT INTO students (id, name) VALUES (?, ?)", [
    (1, "Alice"), (2, "Bob"), (3, "Carol"),
])
conn.executemany("INSERT INTO courses (id, name) VALUES (?, ?)", [
    (1, "Databases"), (2, "Python"), (3, "Algorithms"),
])
conn.executemany(
    "INSERT INTO enrollments (student_id, course_id, grade) VALUES (?, ?, ?)",
    [
        (1, 1, 3.8), (1, 2, 3.5),   # Alice in two courses
        (2, 2, 2.9), (2, 3, 3.2),   # Bob in two courses
        (3, 1, 4.0), (3, 3, 3.7),   # Carol in two courses
    ]
)
conn.commit()

# Two INNER JOINs resolve the many-to-many relationship through enrollments
rows = conn.execute("""
    SELECT   s.name  AS student,
             c.name  AS course,
             e.grade
    FROM     enrollments e
    INNER JOIN students s ON e.student_id = s.id
    INNER JOIN courses  c ON e.course_id  = c.id
    ORDER BY s.name, c.name
""").fetchall()

print(f"{'Student':<10} {'Course':<15} Grade")
print("-" * 34)
for row in rows:
    print(f"{row[0]:<10} {row[1]:<15} {row[2]:.1f}")

conn.close()
```

**Explanation:** `enrollments` is a junction (bridge) table that resolves the many-to-many relationship between students and courses. Two INNER JOINs chain through it: first joining to `students` to get the name, then joining to `courses` to get the course name. The result is one row per enrolment, enriched with human-readable names from both sides.

---

## Q4. Database View

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

conn.execute("""
    CREATE TABLE students (
        id   INTEGER PRIMARY KEY,
        name TEXT    NOT NULL,
        gpa  REAL    NOT NULL
    )
""")
conn.executemany("INSERT INTO students (id, name, gpa) VALUES (?, ?, ?)", [
    (1, "Alice", 3.9),
    (2, "Bob",   3.2),
    (3, "Carol", 3.7),
    (4, "Dave",  2.8),
    (5, "Eve",   3.6),
])
conn.commit()

# CREATE VIEW stores the query — not the data — in the database
conn.execute("""
    CREATE VIEW top_students AS
    SELECT id, name, gpa
    FROM   students
    WHERE  gpa >= 3.5
    ORDER  BY gpa DESC
""")

# Query the view exactly like a table — the underlying SELECT runs each time
rows = conn.execute("SELECT * FROM top_students").fetchall()

print("Top students (GPA >= 3.5):")
for row in rows:
    print(f"  {row['name']:<10}: {row['gpa']:.2f}")

conn.close()
```

**Explanation:** A view is a named, saved SQL query stored in the database catalog. `CREATE VIEW name AS SELECT ...` defines it; subsequent `SELECT * FROM name` executes the underlying query and returns fresh results. Views are useful for encapsulating complex JOINs or filter logic so callers don't need to repeat the SQL. In SQLite, views are read-only by default.

---

## Q5. CSV Round-Trip

```python
import sqlite3
import csv
import io

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

conn.execute("""
    CREATE TABLE employees (
        id         INTEGER PRIMARY KEY,
        name       TEXT    NOT NULL,
        department TEXT    NOT NULL,
        salary     REAL    NOT NULL
    )
""")
conn.executemany(
    "INSERT INTO employees (id, name, department, salary) VALUES (?, ?, ?, ?)",
    [
        (1, "Alice", "Engineering", 95000),
        (2, "Bob",   "Marketing",   72000),
        (3, "Carol", "Engineering", 88000),
        (4, "Dave",  "HR",          65000),
    ]
)
conn.commit()

original_count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]

# ── EXPORT ───────────────────────────────────────────────────
rows = conn.execute("SELECT * FROM employees").fetchall()
buffer = io.StringIO()                     # in-memory file object
writer = csv.DictWriter(buffer, fieldnames=rows[0].keys())
writer.writeheader()
for row in rows:
    writer.writerow(dict(row))             # convert sqlite3.Row → dict

# ── CLEAR ────────────────────────────────────────────────────
conn.execute("DELETE FROM employees")
conn.commit()
cleared = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
print(f"Table cleared. Rows now: {cleared}")    # 0

# ── RE-IMPORT ────────────────────────────────────────────────
buffer.seek(0)                             # rewind to start of the CSV data
reader = csv.DictReader(buffer)
for record in reader:
    conn.execute(
        "INSERT INTO employees (id, name, department, salary) VALUES (?, ?, ?, ?)",
        (int(record["id"]), record["name"],
         record["department"], float(record["salary"]))
    )
conn.commit()

final_count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
print(f"Original rows: {original_count} | Re-imported rows: {final_count}")
assert original_count == final_count, "Row count mismatch!"
print("✓ Row count matches.")

conn.close()
```

**Explanation:** `io.StringIO` acts as an in-memory text file, avoiding disk I/O while keeping the `csv` module's standard interface. `DictWriter` produces a CSV with a header row; `DictReader` consumes it as an iterable of dicts. Type casting on re-import (`int()`, `float()`) is essential because CSV stores everything as strings — SQLite's type affinity would accept string values, but explicit casting keeps the Python types correct.

---

## Q6. Schema Migration

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row

# Original schema — no email column
conn.execute("""
    CREATE TABLE students (
        id   INTEGER PRIMARY KEY,
        name TEXT    NOT NULL,
        gpa  REAL
    )
""")
conn.executemany("INSERT INTO students (id, name, gpa) VALUES (?, ?, ?)", [
    (1, "Alice", 3.8),
    (2, "Bob",   3.2),
    (3, "Carol", 3.9),
])
conn.commit()

# ── MIGRATION STEP 1: add the new column ─────────────────────
# ALTER TABLE ... ADD COLUMN is the only structural change SQLite supports directly
conn.execute("ALTER TABLE students ADD COLUMN email TEXT")

# ── MIGRATION STEP 2: back-fill existing rows ─────────────────
conn.execute("UPDATE students SET email = 'unknown@example.com'")
conn.commit()

# ── VERIFY ────────────────────────────────────────────────────
rows = conn.execute("SELECT id, name, gpa, email FROM students").fetchall()
print("After migration:")
for row in rows:
    print(f"  {row['name']:<10}: {row['email']}")

# PRAGMA table_info returns one row per column: (cid, name, type, notnull, dflt, pk)
col_names = [
    info[1]
    for info in conn.execute("PRAGMA table_info(students)").fetchall()
]
print(f"\nColumns: {col_names}")
assert "email" in col_names, "Migration failed: email column not found"
print("✓ Migration successful.")

conn.close()
```

**Explanation:** `ALTER TABLE ... ADD COLUMN` is SQLite's only supported table alteration — renaming or dropping columns requires recreating the table. New columns added this way default to `NULL` for all existing rows, so an `UPDATE` is needed to back-fill a meaningful default. `PRAGMA table_info` is a SQLite meta-command that returns the schema of any table, making it useful for migration verification scripts.
