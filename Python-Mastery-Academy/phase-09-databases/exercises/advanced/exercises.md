# Phase 09 — Advanced Exercises

> These exercises introduce SQLAlchemy ORM, three-table JOINs, database views, CSV round-trips, and schema migrations.
> Plan your model and schema design carefully before writing code.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. SQLAlchemy ORM Models**

Define two ORM models using `declarative_base` from SQLAlchemy:

- `Author(id, name, nationality)` — one author has many books
- `Book(id, title, year, author_id)` — each book belongs to one author

Use `Column`, `ForeignKey`, and `relationship` to wire them together. Create both tables in an in-memory SQLite engine with `Base.metadata.create_all(engine)` and print the table names to confirm they were created.

**Example:**
```python
# pip install sqlalchemy
Tables created: dict_keys(['authors', 'books'])
```

> **Hints:**
> - `from sqlalchemy.orm import declarative_base, relationship`
> - `from sqlalchemy import create_engine, Column, Integer, String, ForeignKey`
> - `relationship("Book", back_populates="author")` on `Author` and `relationship("Author", back_populates="books")` on `Book` create the two-way link.
> - `create_engine("sqlite:///:memory:")` creates an in-memory SQLite database.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q2. SQLAlchemy Session CRUD**

Using the `Author` and `Book` models from Q1, perform a complete CRUD cycle with a `Session`:

1. Add 3 authors and 5 books via `session.add_all()`
2. Query all books and print their titles
3. Use `filter_by` to get all books by one specific author
4. Retrieve a single book by primary key with `session.get(Book, pk)`
5. Update one book's `year` field and commit
6. Delete one book and confirm the count dropped

**Example:**
```
All books: 5
Rowling's books: 2
Book id=3: Nineteen Eighty-Four
Updated year: 1948
Books after delete: 4
```

> **Hints:**
> - `session.flush()` assigns database IDs before you reference them (e.g., `authors[0].id`) without committing the transaction.
> - `session.query(Book).filter_by(author_id=author.id).all()` returns a list.
> - `session.get(Book, 3)` fetches by primary key; returns `None` if not found.
> - Call `session.commit()` after every mutation you want to persist.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q3. Three-Table JOIN**

Create three tables using plain `sqlite3`:

- `students(id INTEGER PRIMARY KEY, name TEXT)`
- `courses(id INTEGER PRIMARY KEY, name TEXT)`
- `enrollments(student_id INTEGER, course_id INTEGER, grade REAL)`

Insert 3 students, 3 courses, and 6 enrolment rows. Write a single query using two INNER JOINs that returns each student's name, course name, and grade for every enrolment. Print the results in an aligned table.

**Example:**
```
Student    Course           Grade
--------------------------------
Alice      Databases         3.8
Alice      Python            3.5
Bob        Python            2.9
```

> **Hints:**
> - `FROM enrollments e INNER JOIN students s ON e.student_id = s.id INNER JOIN courses c ON e.course_id = c.id`
> - Chain the two JOINs on separate lines for readability.
> - Use f-string width specifiers (`f"{val:<10}"`) to align the output columns.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q4. Database View**

Create a `students(id, name, gpa)` table and insert 5 students with varying GPAs. Then:

1. Create a `CREATE VIEW top_students AS SELECT ...` that returns students with `gpa >= 3.5`, ordered by GPA descending
2. Query the view with `SELECT * FROM top_students` as if it were a table
3. Print the results

**Example:**
```sql
CREATE VIEW top_students AS
SELECT id, name, gpa FROM students WHERE gpa >= 3.5 ORDER BY gpa DESC;
```

```
Top students (GPA >= 3.5):
  Alice     : 3.90
  Carol     : 3.70
  Eve       : 3.60
```

> **Hints:**
> - `conn.execute("CREATE VIEW top_students AS SELECT ...")` — views are created like tables but store a query, not data.
> - After creation, `SELECT * FROM top_students` runs the underlying query each time.
> - Views are stored in the database and can be queried by any connection to that DB.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q5. CSV Round-Trip**

Create an `employees(id, name, department, salary)` table and insert 4 rows. Then:

1. Export the entire table to a CSV string (use `io.StringIO` as an in-memory file)
2. Clear the table with `DELETE FROM employees` and commit
3. Re-import every row from the CSV back into the table
4. Verify the final row count matches the original; assert and print confirmation

**Example:**
```
Table cleared. Rows now: 0
Original rows: 4 | Re-imported rows: 4
✓ Row count matches.
```

> **Hints:**
> - `csv.DictWriter` writes dicts to CSV; `csv.DictReader` reads them back.
> - `buffer.seek(0)` rewinds the in-memory buffer before reading.
> - Cast types when re-importing: `int(record["id"])`, `float(record["salary"])`.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q6. Schema Migration**

Create a `students(id, name, gpa)` table and insert 3 rows. Simulate a schema migration that:

1. Adds a new `email TEXT` column with `ALTER TABLE students ADD COLUMN email TEXT`
2. Updates all existing rows to set `email = 'unknown@example.com'`
3. Selects all rows and prints the new column to confirm it exists
4. Uses `PRAGMA table_info(students)` to programmatically verify the column is present

**Example:**
```
After migration:
  Alice     : unknown@example.com
  Bob       : unknown@example.com
  Carol     : unknown@example.com

Columns: ['id', 'name', 'gpa', 'email']
✓ Migration successful.
```

> **Hints:**
> - `ALTER TABLE ... ADD COLUMN` is the only `ALTER TABLE` operation SQLite supports — it cannot rename or drop columns without recreating the table.
> - `PRAGMA table_info(table_name)` returns one row per column; column `[1]` is the column name.
> - `conn.commit()` after the UPDATE ensures the default values are persisted.

> **Difficulty:** ⭐⭐⭐ Advanced

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
