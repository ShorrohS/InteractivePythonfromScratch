# Lesson 03 — finally and else

**Phase:** 06 — Error Handling | **Time:** ~20 min

---

## Part 1: The Full try/except/else/finally

```python
try:
    # Code that might fail
    result = risky_operation()
except SpecificError as e:
    # Runs if SpecificError occurs
    handle_error(e)
else:
    # Runs ONLY if NO exception occurred
    process_result(result)
finally:
    # ALWAYS runs — error or not
    cleanup()
```

---

## Part 2: finally — Always Runs

```python
def read_data(filename: str) -> str:
    conn = None
    try:
        print("  Opening connection...")
        conn = open(filename, "r")
        data = conn.read()
        return data
    except FileNotFoundError:
        print(f"  File not found: {filename}")
        return ""
    finally:
        if conn:
            conn.close()
            print("  Connection closed.")   # ALWAYS prints
        print("  Finally block ran.")

# With error
read_data("nonexistent.txt")
# Output: Opening connection... / File not found: ... / Connection closed. / Finally...

# Without error
read_data("existing.txt")
# Output: Opening connection... / Connection closed. / Finally...
```

**Use `finally` for:** database connections, file handles, network sockets, locks — anything that needs cleanup regardless of success or failure.

---

## Part 3: else — Runs Only on Success

```python
def process_payment(amount: float) -> bool:
    try:
        if amount <= 0:
            raise ValueError(f"Amount must be positive: {amount}")
        charge = apply_charge(amount)
    except ValueError as e:
        print(f"  Payment rejected: {e}")
        return False
    else:
        # Only reached if no exception
        print(f"  Payment of ${amount:.2f} successful.")
        send_receipt(amount)
        return True
    finally:
        print("  Payment attempt logged.")

# The else block signals genuine success — distinct from the error paths
```

---

## Part 4: Context Managers and finally

The `with` statement is effectively a `try/finally`:

```python
# These are equivalent:

# Using with (preferred)
with open("file.txt", "r") as f:
    data = f.read()

# Manual equivalent
f = open("file.txt", "r")
try:
    data = f.read()
finally:
    f.close()    # guaranteed cleanup
```

Always prefer `with` for resources — it's cleaner and harder to forget.

---

## Part 5: Practical Pattern — Database Operation

```python
import sqlite3

def execute_query(db_path: str, query: str, params: tuple = ()) -> list:
    """Execute a SQL query with full lifecycle management."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.commit()
        return results
    except sqlite3.OperationalError as e:
        print(f"  DB error: {e}")
        if conn:
            conn.rollback()    # undo any partial changes
        return []
    except sqlite3.IntegrityError as e:
        print(f"  Integrity error: {e}")
        if conn:
            conn.rollback()
        return []
    finally:
        if conn:
            conn.close()     # ALWAYS close the connection
```

---

## Practice Exercises

1. When does the `else` block in a try statement run?

2. Write a function that connects to a file, reads it, and guarantees the file is closed using `finally`.

3. What is the output?
   ```python
   try:
       print("try")
       raise ValueError("test")
   except ValueError:
       print("except")
   else:
       print("else")
   finally:
       print("finally")
   ```

---

## Next Lesson

**[Lesson 05 → Defensive Programming](lesson-05-defensive.md)**
