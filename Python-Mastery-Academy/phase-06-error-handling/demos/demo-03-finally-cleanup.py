"""
Demo 03 - finally and Context Managers
Phase 06: Error Handling

Run: python demo-03-finally-cleanup.py
"""

print("=" * 55)
print("DEMO 03 - finally and Context Managers")
print("=" * 55)

# --- 1. FINALLY ALWAYS RUNS ---
print("\n1. finally always runs:")

def risky_divide(a, b):
    try:
        result = a / b
        print(f"  {a} / {b} = {result}")
        return result
    except ZeroDivisionError as e:
        print(f"  Caught: {e}")
        return None
    finally:
        # This block ALWAYS executes — even if we return early
        # or an exception is raised and caught.
        print("  [finally] cleanup ran")

print("  Case 1 — normal execution:")
risky_divide(10, 2)

print("  Case 2 — exception raised:")
risky_divide(10, 0)

print("  Case 3 — finally fires BEFORE the return value is delivered:")

def with_return():
    try:
        print("  Inside try, about to return")
        return "from try"
    finally:
        # The return statement in try is held; finally runs first,
        # THEN the caller receives the return value.
        print("  [finally] fires before the return is delivered")

result = with_return()
print(f"  Caller received: {result!r}")


# --- 2. CONTEXT MANAGERS WITH FILES ---
print("\n2. Context managers — safe file I/O:")
import tempfile
import os

# tempfile.NamedTemporaryFile gives us a real auto-named temp file.
# We close it right away (delete=False) so we can open it again
# with a normal 'with open()' below — purely to show the pattern.
tmp = tempfile.NamedTemporaryFile(
    mode="w", suffix=".txt", delete=False
)
tmp_path = tmp.name
tmp.write("Hello from the temp file!\nLine two.\n")
tmp.close()

print(f"  Created temp file: {os.path.basename(tmp_path)}")

# 'with open(...)' guarantees the file handle is closed even if
# an exception occurs inside the block — no explicit finally needed.
try:
    with open(tmp_path, "r") as f:
        contents = f.read()
    print(f"  Read {len(contents.splitlines())} lines via 'with open()'")
finally:
    # We still use finally here to clean up the temp file itself,
    # so it is always removed regardless of what happens above.
    os.unlink(tmp_path)
    print(f"  Temp file removed: {not os.path.exists(tmp_path)}")


# --- 3. CUSTOM CONTEXT MANAGER CLASS ---
print("\n3. Custom context manager class (simulated DB connection):")

class DatabaseConnection:
    """
    Simulates a database connection with explicit open/close.
    __enter__ is called when we enter the 'with' block.
    __exit__  is called when we leave — even due to an exception.
    """

    def __init__(self, db_name: str):
        self.db_name   = db_name
        self.connected = False

    def __enter__(self):
        # Runs at the start of the 'with' block.
        # Whatever we return here becomes the 'as' target.
        print(f"  [DB] Opening connection to '{self.db_name}'")
        self.connected = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type/exc_val/exc_tb are None if no exception occurred.
        # Return False (or None) to NOT suppress any exception —
        # it will continue propagating after __exit__ returns.
        self.connected = False
        exc_name = exc_type.__name__ if exc_type else None
        print(f"  [DB] Connection to '{self.db_name}' closed "
              f"(exc_type={exc_name})")
        return False

    def query(self, sql: str):
        if not self.connected:
            raise RuntimeError("Cannot query: not connected")
        print(f"  [DB] Executing: {sql}")
        return [{"id": 1, "name": "Alice"}]

print("  Normal use:")
with DatabaseConnection("main.db") as db:
    rows = db.query("SELECT * FROM users LIMIT 1")
    print(f"  Got {len(rows)} row(s)")

print("  Use with exception (connection still closes cleanly):")
try:
    with DatabaseConnection("audit.db") as db:
        db.query("INSERT INTO logs VALUES (?)")
        raise RuntimeError("Simulated mid-query failure")
except RuntimeError as e:
    print(f"  Caught outside 'with': {e}")


# --- 4. contextlib.contextmanager GENERATOR ---
print("\n4. contextlib.contextmanager generator:")
from contextlib import contextmanager

@contextmanager
def db_connection(db_name: str):
    """
    Generator-based context manager — same behaviour as the class above,
    but written as a single function.

    Code BEFORE yield  →  runs when 'with' block is entered (__enter__)
    The yield value    →  becomes the 'as' target
    Code AFTER yield   →  runs when 'with' block exits (__exit__)
    We wrap the yield in try/finally so cleanup always happens.
    """
    print(f"  [gen-db] Opening '{db_name}'")
    connection = {"name": db_name, "open": True}
    try:
        yield connection
    finally:
        connection["open"] = False
        print(f"  [gen-db] Closed '{db_name}'")

print("  Generator-based context manager:")
with db_connection("reports.db") as conn:
    print(f"  Connected: {conn['open']}, db: {conn['name']}")

print("  Generator manager handles exceptions cleanly:")
try:
    with db_connection("temp.db") as conn:
        raise ValueError("Intentional error inside with-block")
except ValueError as e:
    print(f"  Caught: {e}")


# --- 5. NESTED TRY/FINALLY (CLEANUP ORDER) ---
print("\n5. Nested try/finally — cleanup order:")

def outer():
    print("  outer: entering try block")
    try:
        inner()
    finally:
        # This runs AFTER inner()'s finally has already fired.
        print("  outer: finally (runs LAST)")

def inner():
    print("  inner: entering try block")
    try:
        raise ValueError("error raised in inner")
    except ValueError as e:
        print(f"  inner: caught '{e}'")
    finally:
        # inner's finally fires FIRST, before control returns to outer.
        print("  inner: finally (runs FIRST)")

outer()


# --- 6. COMMENTARY ---
print("\n6. When to use finally vs context managers:")
print("""
  FINALLY                           CONTEXT MANAGER
  ──────────────────────────────    ─────────────────────────────────
  One-off cleanup inside a func     Reusable pattern across many files
  When you need exception details   Clean, readable 'with' syntax
  Simple ad-hoc resource release    Pairs acquire/release explicitly
  No imports needed                 Needs a class or @contextmanager

  Rule of thumb:
  • Use 'with' for anything with a clear acquire/release lifecycle:
    files, locks, DB connections, network sockets, temp directories.
  • Use 'finally' for ad-hoc cleanup inside a single function when
    writing a full context manager would be overkill.
  • Use contextlib.contextmanager when you want the 'with' syntax
    without writing a full class.
""")
