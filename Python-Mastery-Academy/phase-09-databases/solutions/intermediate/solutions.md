# Phase 09 — Intermediate Solutions: Databases

---

## Q1. Multi-Table Schema

```python
import sqlite3

conn = sqlite3.connect(":memory:")

# Create customers table
conn.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT    NOT NULL,
        email TEXT    NOT NULL
    )
""")

# Create orders table with a FOREIGN KEY reference to customers
conn.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        product     TEXT    NOT NULL,
        amount      REAL    NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
""")

customers = [
    ("Alice", "alice@example.com"),
    ("Bob",   "bob@example.com"),
    ("Carol", "carol@example.com"),
    ("Dave",  "dave@example.com"),   # Dave will have no orders
]
conn.executemany(
    "INSERT INTO customers (name, email) VALUES (?, ?)", customers
)

orders = [
    (1, "Laptop",    999.99),   # Alice
    (1, "Mouse",      25.00),   # Alice — second order
    (2, "Keyboard",   49.99),   # Bob
    (2, "Headset",    89.99),   # Bob — second order
    (3, "Monitor",   299.00),   # Carol
    (3, "Webcam",     79.99),   # Carol — second order
]
conn.executemany(
    "INSERT INTO orders (customer_id, product, amount) VALUES (?, ?, ?)", orders
)
conn.commit()   # persist all inserts in one transaction

c_count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
o_count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
print(f"Inserted {c_count} customers and {o_count} orders.")
conn.close()
```

**Explanation:** Both tables are created first (so the FOREIGN KEY reference is valid), then data is inserted with `executemany` for efficiency. A single `conn.commit()` writes everything atomically — if any insert fails, the whole batch is rolled back.

---

## Q2. INNER JOIN

```python
import sqlite3

def setup(conn):
    """Create and populate the customers + orders tables."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product TEXT NOT NULL, amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    conn.executemany(
        "INSERT INTO customers (name, email) VALUES (?, ?)",
        [("Alice","alice@example.com"),("Bob","bob@example.com"),
         ("Carol","carol@example.com"),("Dave","dave@example.com")]
    )
    conn.executemany(
        "INSERT INTO orders (customer_id, product, amount) VALUES (?, ?, ?)",
        [(1,"Laptop",999.99),(1,"Mouse",25.00),(2,"Keyboard",49.99),
         (3,"Monitor",299.00),(3,"Webcam",79.99),(2,"Headset",89.99)]
    )
    conn.commit()

conn = sqlite3.connect(":memory:")
setup(conn)

# INNER JOIN: only orders that have a matching customer row are returned
rows = conn.execute("""
    SELECT o.id, o.product, o.amount, c.name, c.email
    FROM   orders o
    INNER JOIN customers c ON o.customer_id = c.id
    ORDER  BY c.name, o.id
""").fetchall()

for row in rows:
    print(f"Order {row[0]}: {row[1]:<15} ${row[2]:7.2f}  —  {row[3]} ({row[4]})")

conn.close()
```

**Explanation:** `INNER JOIN` returns only rows where the join condition matches on both sides. Dave (who has no orders) does not appear — that is the expected behaviour. The `ON` clause explicitly links `orders.customer_id` to `customers.id`.

---

## Q3. LEFT JOIN — Customers With No Orders

```python
import sqlite3

def setup(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product TEXT NOT NULL, amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    conn.executemany(
        "INSERT INTO customers (name, email) VALUES (?, ?)",
        [("Alice","alice@example.com"),("Bob","bob@example.com"),
         ("Carol","carol@example.com"),("Dave","dave@example.com")]
    )
    conn.executemany(
        "INSERT INTO orders (customer_id, product, amount) VALUES (?, ?, ?)",
        [(1,"Laptop",999.99),(1,"Mouse",25.00),(2,"Keyboard",49.99),
         (3,"Monitor",299.00),(3,"Webcam",79.99),(2,"Headset",89.99)]
    )
    conn.commit()

conn = sqlite3.connect(":memory:")
setup(conn)

# LEFT JOIN keeps every customer row; unmatched order columns are NULL
rows = conn.execute("""
    SELECT c.id, c.name, c.email
    FROM   customers c
    LEFT JOIN orders o ON c.id = o.customer_id
    WHERE  o.id IS NULL          -- keep only customers with NO matching order
    ORDER  BY c.name
""").fetchall()

if rows:
    for row in rows:
        print(f"No orders: {row[1]} ({row[2]})")
else:
    print("Every customer has placed at least one order.")

conn.close()
```

**Explanation:** `LEFT JOIN` preserves every row from the left table (`customers`) regardless of whether the right side matches. Filtering `WHERE o.id IS NULL` isolates the customers that had no match on the right — exactly the customers with no orders.

---

## Q4. GROUP BY + HAVING

```python
import sqlite3

def setup(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product TEXT NOT NULL, amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    conn.executemany(
        "INSERT INTO customers (name, email) VALUES (?, ?)",
        [("Alice","alice@example.com"),("Bob","bob@example.com"),
         ("Carol","carol@example.com"),("Dave","dave@example.com")]
    )
    conn.executemany(
        "INSERT INTO orders (customer_id, product, amount) VALUES (?, ?, ?)",
        [(1,"Laptop",999.99),(1,"Mouse",25.00),(2,"Keyboard",49.99),
         (3,"Monitor",299.00),(3,"Webcam",79.99),(2,"Headset",89.99)]
    )
    conn.commit()

conn = sqlite3.connect(":memory:")
setup(conn)

rows = conn.execute("""
    SELECT   c.name, COUNT(o.id) AS order_count
    FROM     customers c
    INNER JOIN orders o ON c.id = o.customer_id
    GROUP BY c.id, c.name
    HAVING   COUNT(o.id) >= 2       -- filter AFTER grouping (not WHERE)
    ORDER BY order_count DESC, c.name
""").fetchall()

print("Customers with 2+ orders:")
for row in rows:
    print(f"  {row[0]:<10}: {row[1]} order(s)")

conn.close()
```

**Explanation:** `GROUP BY` collapses all order rows belonging to the same customer into a single summary row. `COUNT(o.id)` counts orders per group. `HAVING` then filters those summary rows — it is the post-aggregation equivalent of `WHERE`. Dave is excluded because he has zero orders (the INNER JOIN drops him before grouping).

---

## Q5. Atomic Transaction

```python
import sqlite3

conn = sqlite3.connect(":memory:")

conn.execute("""
    CREATE TABLE accounts (
        id      INTEGER PRIMARY KEY,
        name    TEXT    NOT NULL,
        balance REAL    NOT NULL
    )
""")
conn.executemany("INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)", [
    (1, "Alice", 1000.00),
    (2, "Bob",    500.00),
])
conn.commit()   # persist initial balances


def transfer(conn, from_id, to_id, amount):
    """
    Transfer amount from one account to another atomically.
    Commits on success, rolls back on any error.
    """
    try:
        # Deduct from sender — Python sqlite3 starts an implicit transaction here
        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, from_id)
        )
        # Check within the same transaction that balance hasn't gone negative
        row = conn.execute(
            "SELECT balance FROM accounts WHERE id = ?", (from_id,)
        ).fetchone()
        if row[0] < 0:
            raise ValueError("Insufficient funds")   # triggers rollback

        # Credit the receiver
        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, to_id)
        )
        conn.commit()   # both UPDATEs saved together
        print(f"Transferred ${amount:.2f} from account {from_id} to account {to_id}.")

    except Exception as e:
        conn.rollback()  # undo the deduct UPDATE and any other pending changes
        print(f"Transfer failed ({e}) — changes rolled back.")


transfer(conn, 1, 2, 300.00)   # succeeds: Alice 700, Bob 800
transfer(conn, 2, 1, 5000.00)  # fails: would leave Bob at -4200

print("\nFinal balances:")
for row in conn.execute("SELECT name, balance FROM accounts ORDER BY id"):
    print(f"  {row[0]:<10}: ${row[1]:.2f}")

conn.close()
```

**Explanation:** With Python's default `isolation_level`, any DML statement starts an implicit transaction. `conn.commit()` makes both UPDATEs permanent; `conn.rollback()` undoes everything since the last commit. The balance check happens inside the transaction, so it sees the tentatively deducted value and can detect the overdraft before the transaction is finalized.

---

## Q6. sqlite3.Row — Rows as Dicts

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row   # must be set BEFORE any queries

conn.execute("""
    CREATE TABLE products (
        id    INTEGER PRIMARY KEY,
        name  TEXT    NOT NULL,
        price REAL    NOT NULL,
        stock INTEGER NOT NULL
    )
""")
conn.executemany(
    "INSERT INTO products (id, name, price, stock) VALUES (?, ?, ?, ?)",
    [
        (1, "Widget",     9.99, 100),
        (2, "Gadget",    24.99,  50),
        (3, "Doohickey",  4.99, 200),
    ]
)
conn.commit()

rows = conn.execute("SELECT * FROM products ORDER BY price DESC").fetchall()

# Convert each sqlite3.Row to a plain Python dict
products = [dict(row) for row in rows]
print(products)
print()

# Column-name access: readable, resilient to column reordering
for row in rows:
    print(f"{row['name']:<12}: ${row['price']:6.2f}  (stock: {row['stock']})")

# Index access also works but is fragile — avoid it
# print(row[1], row[2])  ← breaks silently if SELECT column order changes

conn.close()
```

**Explanation:** Without `row_factory`, `fetchall()` returns plain tuples and columns are accessed by position — brittle if the query changes. Setting `conn.row_factory = sqlite3.Row` upgrades each row to a dict-like object that supports both name (`row["price"]`) and index (`row[2]`) access. `dict(row)` converts it to a standard dict, which works with `json.dumps`, `csv.DictWriter`, and other dict-aware tools.

---

## Q7. Parameterized UPDATE + DELETE

```python
import sqlite3

conn = sqlite3.connect(":memory:")

conn.execute("""
    CREATE TABLE products (
        id    INTEGER PRIMARY KEY,
        name  TEXT    NOT NULL,
        price REAL    NOT NULL
    )
""")
conn.execute("""
    CREATE TABLE orders (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        order_date   TEXT NOT NULL   -- stored as ISO-8601 string: YYYY-MM-DD
    )
""")

conn.executemany(
    "INSERT INTO products (id, name, price) VALUES (?, ?, ?)",
    [(1, "Widget", 9.99), (2, "Gadget", 24.99), (3, "Doohickey", 4.99)]
)
conn.executemany(
    "INSERT INTO orders (product_name, order_date) VALUES (?, ?)",
    [
        ("Widget",    "2023-11-20"),   # old — will be deleted
        ("Gadget",    "2024-02-14"),   # old — will be deleted
        ("Doohickey", "2024-08-01"),   # recent — kept
        ("Widget",    "2025-01-10"),   # recent — kept
    ]
)
conn.commit()

# Parameterized UPDATE — only the targeted row changes
product_id = 2
new_price   = 29.99
cur = conn.execute(
    "UPDATE products SET price = ? WHERE id = ?",
    (new_price, product_id)
)
conn.commit()
print(f"UPDATE rowcount: {cur.rowcount}")   # 1

# Parameterized DELETE — ISO dates compare lexicographically in SQLite
cutoff_date = "2024-06-01"
cur = conn.execute(
    "DELETE FROM orders WHERE order_date < ?",
    (cutoff_date,)
)
conn.commit()
print(f"DELETE rowcount: {cur.rowcount}")   # 2

conn.close()
```

**Explanation:** `cursor.rowcount` is set by SQLite after every DML statement and reports how many rows were actually affected. A `rowcount` of 0 after an UPDATE means the `WHERE` clause matched nothing — useful for detecting typos in the filter value. ISO-8601 date strings (`YYYY-MM-DD`) sort and compare correctly as plain text, so `<` and `>` work without any date-conversion functions.
