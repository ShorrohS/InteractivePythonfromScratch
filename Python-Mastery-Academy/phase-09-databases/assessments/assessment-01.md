# Phase 09 — Completion Assessment

**Pass mark: 80% | Time: 30 minutes**

---

## PART A: Write the Code

**Task 1.** Create a `library.db` file-based SQLite database with two tables:

```sql
authors(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, nationality TEXT)
books(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, year INTEGER,
      author_id INTEGER, FOREIGN KEY(author_id) REFERENCES authors(id))
```

Implement the following four functions. Each must use parameterized queries (`?` placeholders) and call `conn.commit()` after any write.

- `add_author(name, nationality)` — inserts an author row and returns the new author's id
- `add_book(title, year, author_id)` — inserts a book row and returns the new book's id
- `get_all_books_with_authors()` — returns a list of dicts, each containing `title`, `year`, `author_name`, and `author_nationality` (use an INNER JOIN)
- `delete_book(book_id)` — deletes the book with that id and returns `True` if a row was deleted, `False` otherwise

---

**Task 2.** Using the same database, write a single SQL query (executed with `conn.execute()`) that returns the name of every author who has written **2 or more books**, along with their book count. Return only authors with 2+ books, sorted by book count descending.

**Expected output shape:**
```
George Orwell   : 2 books
J.K. Rowling    : 2 books
```

---

## PART B: Predict the Output

**Q3.** What does this code print?

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.execute("CREATE TABLE scores (player TEXT, pts INTEGER)")
conn.executemany("INSERT INTO scores VALUES (?, ?)",
                 [("Alice", 90), ("Bob", 75), ("Carol", 85)])
conn.commit()

row = conn.execute(
    "SELECT player, pts FROM scores ORDER BY pts DESC LIMIT 1"
).fetchone()
print(row["player"], row["pts"])
```

---

**Q4.** What does this code print?

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE items (name TEXT, qty INTEGER)")
conn.executemany("INSERT INTO items VALUES (?, ?)",
                 [("apple", 5), ("banana", 3), ("cherry", 8)])
conn.commit()

result = conn.execute("""
    SELECT COUNT(*) AS total, SUM(qty) AS units, MAX(qty) AS biggest
    FROM items
""").fetchone()
print(result[0], result[1], result[2])
```

---

## PART C: Find the Bugs

**Q5.** This function has two bugs. Identify both and write the corrected version.

```python
def search_books(conn, author_name):
    rows = conn.execute(
        f"SELECT title, year FROM books WHERE author_name = '{author_name}'"
    ).fetchall()
    return [{"title": row[0], "year": row[1]} for row in rows]
```

---

**Q6.** This function has two bugs. Identify both and write the corrected version.

```python
def save_score(conn, player, score):
    conn.execute(
        "INSERT INTO scores (player, score) VALUES (?, ?)",
        (player, score)
    )
    # no commit

def report(conn):
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM scores").fetchall()
    for row in rows:
        print(row[0], row[1])   # accessing by index when row_factory is set
```

---

## PART D: Short Answer

**Q7.** Explain the difference between `INNER JOIN` and `LEFT JOIN`. Give one example of when you would choose each.

---

**Q8.** Why are parameterized queries (`?` placeholders) required instead of formatting user input directly into SQL strings? Name one specific attack that parameterized queries prevent.

---

## Answers

### Task 1 — Model Solution

```python
import sqlite3

DB_PATH = "library.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            nationality TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT    NOT NULL,
            year      INTEGER,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id)
        )
    """)
    conn.commit()
    conn.close()


def add_author(name: str, nationality: str) -> int:
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO authors (name, nationality) VALUES (?, ?)",
        (name, nationality)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid


def add_book(title: str, year: int, author_id: int) -> int:
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO books (title, year, author_id) VALUES (?, ?, ?)",
        (title, year, author_id)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid


def get_all_books_with_authors() -> list[dict]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT b.title, b.year, a.name AS author_name, a.nationality AS author_nationality
        FROM   books b
        INNER JOIN authors a ON b.author_id = a.id
        ORDER  BY a.name, b.year
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_book(book_id: int) -> bool:
    conn = get_connection()
    cursor = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0
```

### Task 2 — Model Solution

```python
rows = conn.execute("""
    SELECT   a.name, COUNT(b.id) AS book_count
    FROM     authors a
    INNER JOIN books b ON b.author_id = a.id
    GROUP BY a.id, a.name
    HAVING   COUNT(b.id) >= 2
    ORDER BY book_count DESC
""").fetchall()

for row in rows:
    print(f"{row[0]:<20}: {row[1]} books")
```

### Q3 Answer

```
Alice 90
```

`ORDER BY pts DESC LIMIT 1` returns the single row with the highest score. `row["player"]` and `row["pts"]` access by column name (valid because `row_factory = sqlite3.Row`).

### Q4 Answer

```
3 16 8
```

`COUNT(*)` = 3 rows, `SUM(qty)` = 5+3+8 = 16, `MAX(qty)` = 8. These are accessed by index since `row_factory` was not set.

### Q5 — Bug Fixes

**Bug 1:** SQL injection — user-supplied `author_name` is inserted directly via f-string. Fix: use a `?` placeholder.

**Bug 2:** The JOIN schema has `author_id` (a foreign key), not `author_name` as a column on `books`. The query needs a JOIN or the column name must match the actual schema.

```python
def search_books(conn, author_name):
    rows = conn.execute(
        """SELECT b.title, b.year
           FROM books b
           INNER JOIN authors a ON b.author_id = a.id
           WHERE a.name = ?""",
        (author_name,)
    ).fetchall()
    return [{"title": row[0], "year": row[1]} for row in rows]
```

### Q6 — Bug Fixes

**Bug 1:** `save_score` is missing `conn.commit()` — the INSERT is never persisted.

**Bug 2:** In `report`, `row[0]` and `row[1]` access by index when `conn.row_factory = sqlite3.Row` is set. This works but is fragile; use `row["player"]` and `row["score"]` for clarity. More critically, `conn.row_factory` is set in `report` but the connection is shared — `save_score` must use the same connection or both functions should receive a connection that already has `row_factory` configured.

```python
def save_score(conn, player, score):
    conn.execute(
        "INSERT INTO scores (player, score) VALUES (?, ?)",
        (player, score)
    )
    conn.commit()   # ← add commit

def report(conn):
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM scores").fetchall()
    for row in rows:
        print(row["player"], row["score"])   # ← use column names
```

### Q7 Answer

`INNER JOIN` returns only rows where the join condition matches on **both** sides. Use it when you only want records that have a corresponding entry in the related table (e.g., show orders with their customer names — orders without a customer are excluded).

`LEFT JOIN` returns all rows from the left table regardless of whether a match exists on the right; unmatched right-side columns appear as `NULL`. Use it when you need to include records even if they have no related data (e.g., list all customers and their order count, including customers who have placed zero orders).

### Q8 Answer

Parameterized queries (`?` placeholders) hand the SQL string and the data values to the database engine separately. The engine treats the parameter values as literal data, not as SQL syntax, so special characters like `'`, `;`, or `--` in user input cannot alter the query's structure.

The specific attack prevented is **SQL injection** — an attacker supplying a value like `'; DROP TABLE books; --` as a search term would, without parameterization, execute an arbitrary SQL command that destroys data. With `?` placeholders, the entire string is treated as a data value and the malicious SQL is never executed.
