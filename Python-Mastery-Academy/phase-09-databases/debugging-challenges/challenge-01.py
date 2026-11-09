"""
Debugging Challenge 01 — Phase 09: Databases
=============================================

INSTRUCTIONS:
  This file contains 7 bugs related to SQLite3 and Python database operations.
  Find and fix each one.
  When all bugs are corrected, the program creates an in-memory database,
  inserts sample data, runs several queries, and prints correct output.

HINTS:
  Bug 1 — Look for a SQL injection risk in a WHERE clause.
  Bug 2 — A write operation is missing its commit; data will be lost on rollback.
  Bug 3 — A row is accessed by index when row_factory = sqlite3.Row is set;
           one of the indexes points to the wrong column.
  Bug 4 — A CREATE TABLE statement is called twice without IF NOT EXISTS.
  Bug 5 — A JOIN type returns incomplete results; one customer is missing.
  Bug 6 — A database connection is opened but never closed.
  Bug 7 — A Python comparison uses = (assignment) instead of == (equality).

Run: python challenge-01.py
"""

import sqlite3

print("=" * 55)
print("DEBUGGING CHALLENGE 01 — Phase 09: Databases")
print("=" * 55)

# ============================================================
# SETUP — shared in-memory database (no bugs here)
# ============================================================
conn = sqlite3.connect(":memory:")

conn.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT    NOT NULL,
        email TEXT    NOT NULL
    )
""")
conn.executemany("INSERT INTO customers (name, email) VALUES (?, ?)", [
    ("Alice", "alice@example.com"),
    ("Bob",   "bob@example.com"),
    ("Carol", "carol@example.com"),
    ("Dave",  "dave@example.com"),   # Dave will have no orders
])
conn.commit()


# ============================================================
# === BUG 1 ===
# GOAL: Search for a customer by name safely.
# ============================================================
print("\nBug 1 — Search by name:")
search_name = "Alice"
# BUG: the f-string injects search_name directly into the SQL string.
#      A malicious value like "' OR '1'='1" would return all rows.
#      Replace the f-string with a ? placeholder and a parameter tuple.
rows = conn.execute(
    f"SELECT id, name, email FROM customers WHERE name = '{search_name}'"
).fetchall()
for row in rows:
    print(f"  Found: {row}")


# ============================================================
# === BUG 2 ===
# GOAL: Insert a new customer and ensure the row is persisted.
# ============================================================
print("\nBug 2 — Insert and verify:")
conn.execute(
    "INSERT INTO customers (name, email) VALUES (?, ?)",
    ("Eve", "eve@example.com")
)
# BUG: conn.commit() is missing here.
#      Uncommitted changes are visible within this connection but will be lost
#      if the connection closes unexpectedly or conn.rollback() is called.
#      Add conn.commit() immediately after the INSERT.

# Simulate a rollback (e.g. an unexpected error elsewhere in the program)
conn.rollback()
count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
print(f"  Customers in DB: {count}")   # should be 5, not 4


# ============================================================
# === BUG 3 ===
# GOAL: Print the customer's name using row_factory column-name access.
# ============================================================
print("\nBug 3 — Row factory access:")
conn.row_factory = sqlite3.Row
row = conn.execute(
    "SELECT id, name, email FROM customers WHERE id = 1"
).fetchone()
# BUG: row[2] is the email column (index 0=id, 1=name, 2=email).
#      The intent is to print the name, so this should be row["name"].
#      With row_factory = sqlite3.Row, prefer column-name access for clarity.
print(f"  Customer name: {row[2]}")    # prints email, not name — wrong!


# ============================================================
# === BUG 4 ===
# GOAL: Create the orders table so the script can be called more than once
#       without crashing.
# ============================================================
print("\nBug 4 — CREATE TABLE safety:")


def setup_orders(conn):
    """Create the orders table and insert sample rows."""
    # BUG: missing IF NOT EXISTS — raises OperationalError on the second call
    conn.execute("""
        CREATE TABLE orders (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product     TEXT    NOT NULL,
            amount      REAL    NOT NULL
        )
    """)
    conn.executemany(
        "INSERT INTO orders (customer_id, product, amount) VALUES (?, ?, ?)",
        [
            (1, "Laptop",    999.99),   # Alice
            (2, "Keyboard",   49.99),   # Bob
            (3, "Monitor",   299.00),   # Carol
            (3, "Webcam",     79.99),   # Carol — second order
        ]
    )
    conn.commit()


setup_orders(conn)      # first call — works
setup_orders(conn)      # second call — crashes without IF NOT EXISTS
print("  Orders table ready.")


# ============================================================
# === BUG 5 ===
# GOAL: List ALL customers with their order count, including those with 0 orders.
# ============================================================
print("\nBug 5 — All customers with order count:")
# BUG: INNER JOIN silently drops customers who have no matching orders.
#      Dave has no orders and will be missing from the results.
#      Change INNER JOIN to LEFT JOIN to keep all customers.
rows = conn.execute("""
    SELECT c.name, COUNT(o.id) AS order_count
    FROM   customers c
    INNER JOIN orders o ON c.id = o.customer_id
    GROUP  BY c.id, c.name
    ORDER  BY c.name
""").fetchall()
for row in rows:
    print(f"  {row[0]:<10}: {row[1]} order(s)")
# Dave is missing from output — fix: change INNER JOIN to LEFT JOIN


# ============================================================
# === BUG 6 ===
# GOAL: Open a secondary connection for a quick lookup, then release it.
# ============================================================
print("\nBug 6 — Connection lifecycle:")
conn2 = sqlite3.connect(":memory:")
conn2.execute("CREATE TABLE temp_log (msg TEXT)")
conn2.execute("INSERT INTO temp_log VALUES (?)", ("session started",))
conn2.commit()
msg = conn2.execute("SELECT msg FROM temp_log").fetchone()[0]
print(f"  Log entry: {msg}")
# BUG: conn2 is never closed — this is a resource leak.
#      Add conn2.close() here, or use: with sqlite3.connect(":memory:") as conn2:


# ============================================================
# === BUG 7 ===
# GOAL: Check whether a DELETE affected any rows using cursor.rowcount.
# ============================================================
print("\nBug 7 — rowcount check:")
cursor = conn.execute(
    "DELETE FROM orders WHERE product = ?", ("Nonexistent Product",)
)
conn.commit()
# BUG: = is the assignment operator; == is the equality comparison.
#      This line is a SyntaxError — Python will not even run the file until fixed.
if cursor.rowcount = 0:
    print("  No matching rows to delete.")
else:
    print(f"  Deleted {cursor.rowcount} row(s).")


print("\n" + "=" * 55)
print("Fixed all 7 bugs? The output should be logical and correct.")
print("=" * 55)


# ============================================================
# ANSWER KEY
# ============================================================
#
# BUG 1 — SQL injection: replace f-string with parameterized query
#   rows = conn.execute(
#       "SELECT id, name, email FROM customers WHERE name = ?",
#       (search_name,)
#   ).fetchall()
#
# BUG 2 — Missing commit: add conn.commit() BEFORE conn.rollback()
#   conn.execute("INSERT INTO customers (name, email) VALUES (?, ?)",
#                ("Eve", "eve@example.com"))
#   conn.commit()    ← add this line
#   # (remove the conn.rollback() line once the commit is in place)
#
# BUG 3 — Wrong column index: use column name instead of index
#   print(f"  Customer name: {row['name']}")
#   (row[2] is the email column, not the name)
#
# BUG 4 — Missing IF NOT EXISTS: add it to the CREATE TABLE statement
#   CREATE TABLE IF NOT EXISTS orders (
#       ...
#   )
#
# BUG 5 — Wrong JOIN type: change INNER JOIN to LEFT JOIN
#   FROM   customers c
#   LEFT JOIN orders o ON c.id = o.customer_id
#   (COUNT(o.id) returns 0 for customers with no orders when LEFT JOIN is used)
#
# BUG 6 — Unclosed connection: add conn2.close() after the lookup
#   conn2.close()    ← add this line
#   (Or restructure as: with sqlite3.connect(":memory:") as conn2: ...)
#
# BUG 7 — Assignment instead of comparison: use == not =
#   if cursor.rowcount == 0:
