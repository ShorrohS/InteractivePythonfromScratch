# Phase 09 — Quiz 01: Databases

**Questions: 20 | Pass: 16/20 | Time: 20 min**

---

## Section 1: SQL Fundamentals (Q1–Q5)

**Q1.** Which SQLite data type would you use to store a decimal number like `3.14` or `99.95`?

`A) INTEGER  B) REAL  C) BLOB  D) NUMERIC_FLOAT`

---

**Q2.** What does `INTEGER PRIMARY KEY AUTOINCREMENT` do in a `CREATE TABLE` statement?

`A) Creates a column that must be filled manually  B) Creates a unique auto-incrementing integer ID  C) Prevents NULL values only  D) Creates a floating-point primary key`

---

**Q3.** What is the difference between `TEXT NOT NULL` and `TEXT` when defining a column?

`A) No difference — both accept NULL  B) NOT NULL means the column cannot be omitted on INSERT  C) NOT NULL stores text more efficiently  D) TEXT alone raises an error if left empty`

---

**Q4.** Which `CREATE TABLE` clause ensures a grade column only accepts values between 0.0 and 4.0?

```sql
A) VALIDATE(grade >= 0 AND grade <= 4.0)
B) RANGE grade 0 TO 4.0
C) CHECK(grade >= 0 AND grade <= 4.0)
D) CONSTRAINT grade BETWEEN 0 AND 4.0
```

---

**Q5.** What happens if you run `CREATE TABLE students (...)` a second time on the same database?

`A) It silently succeeds and resets the table  B) It raises an OperationalError: table already exists  C) It adds a second copy of the table  D) It merges the two schemas`

---

## Section 2: CRUD (Q6–Q10)

**Q6.** Which is the correct parameterized INSERT using `sqlite3`?

```python
A) conn.execute("INSERT INTO t VALUES {name}, {age}", name="Alice", age=30)
B) conn.execute("INSERT INTO t (name, age) VALUES (?, ?)", ("Alice", 30))
C) conn.execute("INSERT INTO t (name, age) VALUES (%s, %s)", ("Alice", 30))
D) conn.execute(f"INSERT INTO t VALUES ('Alice', 30)")
```

---

**Q7.** What does `ORDER BY amount DESC LIMIT 5` do in a SELECT query?

`A) Returns the 5 cheapest rows  B) Returns the 5 most expensive rows  C) Returns all rows, sorted with the 5 cheapest last  D) Raises an error if there are fewer than 5 rows`

---

**Q8.** Which UPDATE statement correctly changes Alice's grade to 3.9 by her id?

```python
A) conn.execute("UPDATE students SET grade = 3.9")
B) conn.execute("UPDATE students SET grade = ? WHERE id = ?", (3.9,))
C) conn.execute("UPDATE students SET grade = ? WHERE id = ?", (3.9, 1))
D) conn.execute("MODIFY students grade = 3.9 WHERE id = 1")
```

---

**Q9.** After running `conn.execute("DELETE FROM orders WHERE id = ?", (7,))`, how do you confirm a row was actually deleted?

`A) Check conn.lastrowid  B) Check cursor.rowcount == 1  C) Run SELECT COUNT(*) before and after  D) B or C both work`

---

**Q10.** You call `conn.execute("INSERT INTO products ...")` but forget `conn.commit()`. What is the risk?

`A) The INSERT raises an exception  B) The row exists in memory but is lost if the connection closes unexpectedly  C) The row is automatically committed after 30 seconds  D) Nothing — sqlite3 always auto-commits`

---

## Section 3: JOINs and Aggregation (Q11–Q15)

**Q11.** A `customers` table has 4 rows; an `orders` table has 6 rows. One customer has no orders. How many rows does `INNER JOIN orders ON customers.id = orders.customer_id` return?

`A) 10  B) 6  C) 4  D) 24`

---

**Q12.** You want to list ALL customers, including those with no orders, with a NULL for the order columns when there is no match. Which JOIN should you use?

`A) INNER JOIN  B) RIGHT JOIN  C) LEFT JOIN customers ON ...  D) LEFT JOIN orders ON ...`

---

**Q13.** What does `SELECT COUNT(*), AVG(amount), MAX(amount) FROM orders` return?

`A) Three separate result sets  B) One row with three aggregate values  C) A list of all amounts  D) An error — you cannot mix aggregate functions`

---

**Q14.** What is wrong with this query?

```sql
SELECT customer_id, COUNT(*) AS total
FROM orders
WHERE COUNT(*) > 2
GROUP BY customer_id
```

`A) COUNT(*) is not allowed in SELECT  B) WHERE cannot use aggregate functions — use HAVING instead  C) GROUP BY must come before WHERE  D) Nothing is wrong`

---

**Q15.** What does `GROUP BY department HAVING AVG(salary) > 80000` do?

`A) Filters individual employee rows where salary > 80000  B) Groups employees by department and keeps only groups whose average salary exceeds 80000  C) Sorts departments by salary  D) Returns one row per employee in high-salary departments`

---

## Section 4: Python + ORM (Q16–Q20)

**Q16.** What is the correct way to open a connection to an in-memory SQLite database in Python?

```python
A) sqlite3.connect("memory")
B) sqlite3.connect(":memory:")
C) sqlite3.open(":memory:")
D) sqlite3.Database(":memory:")
```

---

**Q17.** Why should you always use `?` placeholders instead of f-strings in SQL queries?

`A) f-strings are slower  B) ? placeholders prevent SQL injection attacks  C) sqlite3 does not support f-strings  D) f-strings cannot contain numbers`

---

**Q18.** What does setting `conn.row_factory = sqlite3.Row` change about query results?

`A) Results are returned as DataFrames  B) Each row can be accessed by column name as well as by index  C) Rows are automatically converted to JSON  D) Queries run faster`

---

**Q19.** Which pattern correctly uses a context manager to ensure a SQLite connection is closed even if an exception occurs?

```python
A) conn = sqlite3.connect("db.sqlite")
   try: conn.execute(...)
   finally: conn.close()

B) with sqlite3.connect("db.sqlite") as conn:
       conn.execute(...)

C) using sqlite3.connect("db.sqlite") as conn:
       conn.execute(...)

D) A and B are both valid
```

---

**Q20.** In SQLAlchemy, what is the difference between `session.add(obj)` and `session.execute(stmt)`?

`A) add() is for SELECT; execute() is for INSERT  B) add() registers an ORM object for INSERT/UPDATE; execute() runs raw or Core SQL directly  C) They are identical  D) execute() only works with DELETE statements`

---

## Answers

| Q  | Answer | Key Point |
|----|--------|-----------|
| 1  | B      | `REAL` stores floating-point numbers in SQLite |
| 2  | B      | `INTEGER PRIMARY KEY AUTOINCREMENT` creates a unique, auto-generated ID |
| 3  | B      | `NOT NULL` rejects rows that omit the column or pass `None` |
| 4  | C      | `CHECK(expr)` enforces a column-level constraint on every INSERT/UPDATE |
| 5  | B      | Without `IF NOT EXISTS`, a duplicate `CREATE TABLE` raises `OperationalError` |
| 6  | B      | `?` placeholder with a tuple is the correct sqlite3 parameterized syntax |
| 7  | B      | `DESC` sorts largest first; `LIMIT 5` keeps only the top 5 rows |
| 8  | C      | Two `?` placeholders need a tuple with two values: `(3.9, 1)` |
| 9  | D      | Both `cursor.rowcount == 1` and a COUNT comparison confirm deletion |
| 10 | B      | Uncommitted changes are pending and will be rolled back if the connection drops |
| 11 | B      | INNER JOIN returns 6 rows — one per order (the customer with no orders is excluded) |
| 12 | D      | `LEFT JOIN orders ON customers.id = orders.customer_id` keeps all customers |
| 13 | B      | Multiple aggregate functions in one SELECT return a single summary row |
| 14 | B      | Aggregate functions are not allowed in `WHERE`; use `HAVING` after `GROUP BY` |
| 15 | B      | `HAVING` filters aggregated groups, not individual rows |
| 16 | B      | `":memory:"` is the special SQLite path for a transient in-memory database |
| 17 | B      | `?` placeholders sanitize user input and prevent SQL injection |
| 18 | B      | `sqlite3.Row` enables column-name access: `row["salary"]` instead of `row[3]` |
| 19 | D      | Both `try/finally` with `conn.close()` and `with` context manager are valid |
| 20 | B      | `session.add()` works with mapped ORM objects; `session.execute()` runs SQL directly |
