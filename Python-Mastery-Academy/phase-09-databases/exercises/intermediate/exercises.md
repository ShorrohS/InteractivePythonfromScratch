# Phase 09 — Intermediate Exercises

> These exercises move beyond single-table CRUD and introduce multi-table design, JOINs, aggregation, transactions, and the `sqlite3.Row` factory.
> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. Multi-Table Schema**

Create an in-memory SQLite database with two related tables:

- `customers(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL)`
- `orders(id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL, product TEXT NOT NULL, amount REAL NOT NULL, FOREIGN KEY(customer_id) REFERENCES customers(id))`

Insert 4 customers and 6 orders. Ensure at least 2 customers have more than one order, and at least 1 customer has no orders at all. Print a confirmation showing how many rows were inserted into each table.

**Example:**
```
Inserted 4 customers and 6 orders.
```

> **Hints:**
> - `conn.executemany()` accepts a list of tuples and inserts all rows in one call.
> - Call `conn.commit()` once after all inserts to persist everything in a single transaction.
> - The `FOREIGN KEY(customer_id) REFERENCES customers(id)` clause goes at the end of the `CREATE TABLE` body.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q2. INNER JOIN**

Using the two-table schema from Q1, write a query that returns every order together with the ordering customer's name and email address. Print each row on a formatted line.

**Example:**
```
Order 1: Laptop          $ 999.99  —  Alice (alice@example.com)
Order 3: Keyboard        $  49.99  —  Bob   (bob@example.com)
```

> **Hints:**
> - `FROM orders o INNER JOIN customers c ON o.customer_id = c.id`
> - Customers who placed no orders do **not** appear — that is the expected behaviour for INNER JOIN.
> - Use table aliases (`o` and `c`) to keep column references short and readable.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q3. LEFT JOIN — Customers With No Orders**

Write a query that finds every customer who has **not** placed any order. A LEFT JOIN keeps all rows from the left table even when no matching row exists on the right side; those missing rows appear as `NULL`.

**Example:**
```
No orders: Dave (dave@example.com)
```

> **Hints:**
> - `FROM customers c LEFT JOIN orders o ON c.id = o.customer_id`
> - After the JOIN, filter with `WHERE o.id IS NULL` to keep only the unmatched customer rows.
> - An INNER JOIN would silently drop these customers — LEFT JOIN is the correct choice when you need to include non-matches.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q4. GROUP BY + HAVING**

Write a query that counts how many orders each customer has placed and returns only those customers with **2 or more orders**. Display the customer name and their order count, sorted by order count descending.

**Example:**
```
Alice     : 2 orders
Bob       : 2 orders
Carol     : 2 orders
```

> **Hints:**
> - Use `COUNT(o.id)` to count orders and `GROUP BY c.id, c.name` to group per customer.
> - `HAVING COUNT(o.id) >= 2` filters groups **after** aggregation; `WHERE` filters rows **before** grouping.
> - Use INNER JOIN here since you only want customers who actually have orders.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q5. Atomic Transaction**

Create an `accounts(id, name, balance)` table and insert two rows. Write a `transfer(conn, from_id, to_id, amount)` function that:

1. Deducts the amount from the sender's balance
2. Checks whether the balance has gone negative; if it has, raises an exception
3. Credits the amount to the receiver's balance
4. Calls `conn.commit()` on success and `conn.rollback()` in the `except` block

Call `transfer` twice: once with a valid amount (succeeds) and once with an amount that exceeds the sender's balance (triggers the rollback). Print the final balances after both calls.

**Example:**
```
Transferred $300.00 from account 1 to account 2.
Transfer failed (Insufficient funds) — changes rolled back.
Alice     : $700.00
Bob       : $800.00
```

> **Hints:**
> - With the default `isolation_level`, Python's sqlite3 wraps DML statements in an implicit transaction; `conn.commit()` saves it, `conn.rollback()` undoes it.
> - SELECT the sender's balance **within the same transaction** (after the deduct UPDATE) to verify it hasn't gone negative.
> - Wrap the two UPDATE statements and the balance check in a `try` block with `except Exception as e`.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q6. sqlite3.Row — Rows as Dicts**

Create a small `products(id, name, price, stock)` table and insert three rows. Set `conn.row_factory = sqlite3.Row`, execute a SELECT, convert the result to a list of plain Python dicts, and print them. Then demonstrate both column-name access (`row["name"]`) and explain in a comment why it is safer than index access (`row[2]`).

**Example:**
```python
[{'id': 1, 'name': 'Widget', 'price': 9.99, 'stock': 100}, ...]
Widget      :  $ 9.99  (stock: 100)
```

> **Hints:**
> - Set `conn.row_factory = sqlite3.Row` **before** executing any queries on that connection.
> - `dict(row)` converts a `sqlite3.Row` object into an ordinary Python dict.
> - Column-name access (`row["price"]`) stays correct even if the SELECT column order changes; index access (`row[2]`) silently reads the wrong value if columns are reordered.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q7. Parameterized UPDATE + DELETE**

Create a `products(id, name, price)` table and an `orders(id, product_name, order_date TEXT)` table. Insert sample rows with varied dates. Then:

1. Update a specific product's price by its id using a `?` placeholder; print `cursor.rowcount`
2. Delete all orders older than a given cutoff date using a `?` placeholder; print `cursor.rowcount`

**Example:**
```
UPDATE rowcount: 1
DELETE rowcount: 2
```

> **Hints:**
> - `cursor = conn.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, product_id))`
> - `cursor.rowcount` reports how many rows were changed — useful for confirming the operation matched something.
> - Dates stored as ISO-8601 strings (`"2024-01-15"`) compare correctly with `<` and `>` in SQLite.

> **Difficulty:** ⭐⭐ Intermediate

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
