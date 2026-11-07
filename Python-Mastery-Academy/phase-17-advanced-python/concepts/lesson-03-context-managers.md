# Lesson 03 — Context Managers

**Phase:** 17 — Advanced Python | **Time:** ~25 min

---

## Part 1: What is a Context Manager?

A context manager handles setup and teardown automatically. The `with` statement uses them.

```python
# You already use context managers:
with open("file.txt") as f:
    data = f.read()
# File is automatically closed here — no need to call f.close()
```

Behind the scenes: `__enter__` runs on entry, `__exit__` runs on exit (even if an error occurs).

---

## Part 2: Class-Based Context Manager

```python
class DatabaseConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn    = None

    def __enter__(self):
        import sqlite3
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        print(f"  Connected to {self.db_path}")
        return self.conn    # this is what `as conn` receives

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
            print(f"  Error — rolled back: {exc_val}")
        else:
            self.conn.commit()
        self.conn.close()
        print("  Connection closed.")
        return False    # False = don't suppress exceptions

# Usage
with DatabaseConnection("mydb.db") as conn:
    conn.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
# Automatically committed and closed
```

---

## Part 3: @contextmanager Decorator (Simpler)

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(label: str):
    """Measure execution time of a code block."""
    start = time.perf_counter()
    try:
        yield    # code inside 'with' block runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"  {label}: {elapsed:.4f}s")

with timer("data processing"):
    total = sum(range(1_000_000))

# Output: data processing: 0.0234s


@contextmanager
def temporary_directory():
    """Create and clean up a temp directory."""
    import tempfile, shutil
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir    # caller uses the path
    finally:
        shutil.rmtree(tmpdir)   # always cleaned up

with temporary_directory() as tmp:
    with open(f"{tmp}/data.txt", "w") as f:
        f.write("temporary data")
# Directory deleted automatically


@contextmanager
def suppress_errors(*exceptions):
    """Silently ignore specific exceptions."""
    try:
        yield
    except exceptions:
        pass

with suppress_errors(FileNotFoundError):
    os.remove("nonexistent.txt")   # no error raised
```

---

## Part 4: Practical Examples

```python
# Logging context
@contextmanager
def log_operation(name: str):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Starting: {name}")
    try:
        yield
        logger.info(f"Completed: {name}")
    except Exception as e:
        logger.error(f"Failed: {name} — {e}")
        raise

with log_operation("data import"):
    process_data()

# Transaction context
@contextmanager
def database_transaction(conn):
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pass   # conn stays open
```

---

## Practice Exercises

1. Write a `redirect_stdout(filename)` context manager that redirects `print()` output to a file.

2. Write a `retry(times)` context manager.

3. What is the difference between `__exit__` returning `True` vs `False`?

---

## Next Lesson

**[Lesson 04 → Dataclasses](lesson-04-dataclasses.md)**
