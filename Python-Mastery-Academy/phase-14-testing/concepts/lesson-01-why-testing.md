# Lesson 01 — Why Testing Matters

**Phase:** 14 — Testing | **Time:** ~30 min

---

## Part 1: The Cost of Not Testing

Software without automated tests creates three painful problems.

**Silent regressions** — you change function A, and function B quietly breaks.
You ship it. Your customers find it three days later.

**Fear of refactoring** — nobody touches the old code because nobody knows what
it does. The codebase accumulates technical debt that compounds every sprint.

**"It works on my machine"** — manual testing on a developer laptop misses
environment differences. Tests run the same way on every machine.

Finding bugs has a well-known cost multiplier:

| When bug is found | Relative cost |
|-------------------|---------------|
| During development | 1× |
| In QA / testing phase | 10× |
| In production | 100× |

Automated tests push discovery to the cheapest possible moment.

---

## Part 2: The Testing Pyramid

The testing pyramid describes three levels. Write more tests at the base, fewer at the top.

```
            ┌──────────┐
            │   E2E    │   ← few, slowest, most brittle
          ┌─┴──────────┴─┐
          │ Integration  │   ← moderate count, moderate speed
        ┌─┴──────────────┴─┐
        │   Unit Tests     │   ← many, milliseconds each
        └──────────────────┘
```

**Unit tests** — test one function or class in isolation. No database, no
network, no filesystem. Thousands can run per second.

**Integration tests** — test multiple components working together. Example:
a function that queries a real (in-memory) database. Slower, but verify that
components connect correctly.

**End-to-end tests** — simulate a full user workflow through the whole system.
Example: a browser test that logs in, adds a product, and checks out. Slowest
and most expensive to maintain.

Practical target: many unit tests, a moderate number of integration tests, a
small suite of E2E tests for critical user journeys.

---

## Part 3: The FIRST Properties of Good Tests

Good tests share five properties (acronym: **FIRST**).

| Property | Meaning |
|----------|---------|
| **F**ast | Run in milliseconds — the full suite runs in seconds |
| **I**solated | Each test sets up its own state; order never matters |
| **R**epeatable | Same result on every machine, every run |
| **S**elf-validating | Pass or fail automatically — no human judgment required |
| **T**imely | Written alongside (or before) the code they test |

A test that needs a live network connection, takes 30 seconds, and prints
"looks OK" for a human to verify violates all five properties.

---

## Part 4: Naming Conventions

Testing frameworks discover tests by name. Follow these rules exactly:

```python
# File names — prefix or suffix with test
test_calculator.py       # ✅ discovered by pytest and unittest
calculator_test.py       # ✅ discovered by pytest
calculator.py            # ❌ not discovered

# Function names — must start with test_
def test_add_returns_sum():           # ✅
def test_divide_by_zero_raises():     # ✅
def add_test():                       # ❌ not discovered

# Test class names — must start with Test (no suffix needed)
class TestCalculator:                 # ✅
class TestBankAccount:                # ✅
class CalculatorTests:                # ❌ not discovered by default
```

The best test names describe function, scenario, and expected result:

```python
# Pattern: test_<function>_<scenario>_<expected_result>

test_divide_by_zero_raises_value_error
test_login_with_valid_credentials_returns_token
test_cart_total_after_discount_applied
test_withdraw_when_balance_insufficient_returns_false
```

---

## Part 5: What to Test

**Happy path** — normal input, expected output:

```python
def test_add_two_positive_numbers():
    assert add(3, 7) == 10

def test_full_name_joins_first_and_last():
    assert full_name("Alice", "Smith") == "Alice Smith"
```

**Edge cases** — boundaries, empty input, zero, None:

```python
def test_add_with_zero():
    assert add(0, 5) == 5

def test_add_negative_numbers():
    assert add(-3, -4) == -7

def test_process_empty_list_returns_empty():
    assert process([]) == []

def test_percentage_when_total_is_zero_raises():
    with pytest.raises(ZeroDivisionError):
        percentage(5, 0)
```

**Error cases** — invalid input must raise an exception, not silently produce
wrong output:

```python
def test_product_with_negative_price_raises_value_error():
    with pytest.raises(ValueError):
        Product("Widget", price=-5.00)

def test_withdraw_more_than_balance_raises():
    account = BankAccount(balance=100)
    with pytest.raises(ValueError):
        account.withdraw(200)
```

**What NOT to test:**
- Trivial attribute assignment (`self.name = name`)
- Third-party libraries — pytest, Django, SQLAlchemy test themselves
- Language built-ins (`len([1, 2]) == 2`)
- Pure configuration constants with no logic

---

## Part 6: Unit vs Integration — Concrete Example

```python
# ── Unit test ──────────────────────────────────────────────
# Tests pure logic in isolation — no database involved

def calculate_total(items: list[dict]) -> float:
    """Sum price × qty for each item."""
    return sum(item["price"] * item["qty"] for item in items)


def test_calculate_total_two_items():
    items = [
        {"price": 10.00, "qty": 2},   # 20.00
        {"price": 5.00,  "qty": 3},   # 15.00
    ]
    assert calculate_total(items) == 35.00


def test_calculate_total_empty_list():
    assert calculate_total([]) == 0.0


def test_calculate_total_single_item():
    assert calculate_total([{"price": 9.99, "qty": 1}]) == 9.99


# ── Integration test ────────────────────────────────────────
# Tests the same logic wired to a real (in-memory) SQLite database

import sqlite3

def get_order_total(conn: sqlite3.Connection, order_id: int) -> float:
    rows = conn.execute(
        "SELECT price, qty FROM order_items WHERE order_id = ?",
        (order_id,)
    ).fetchall()
    return sum(price * qty for price, qty in rows)


def test_get_order_total_integration():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE order_items (order_id INT, price REAL, qty INT)"
    )
    conn.executemany(
        "INSERT INTO order_items VALUES (?, ?, ?)",
        [(1, 10.00, 2), (1, 5.00, 3)]
    )
    conn.commit()

    assert get_order_total(conn, 1) == 35.00
    conn.close()
```

The unit test runs in microseconds; it catches logic bugs.
The integration test catches wiring bugs — wrong column names, bad SQL, schema mismatches.

---

## Practice Exercises

1. For a function `def withdraw(balance, amount) -> float`, write out (in plain
   English, not code) one happy-path test, one edge-case test, and one error-case test.

2. Classify each scenario as the test level that catches it best (unit,
   integration, or E2E): (a) wrong formula in a discount calculation; (b) a
   SQL query returning rows in the wrong order; (c) the login page redirecting
   to the wrong URL after a successful login.

3. Look at this function and list the missing test cases:
   ```python
   def percentage(part, total):
       return (part / total) * 100
   ```

4. Identify which FIRST property each of the following tests violates: (a) a
   test that queries a live production database; (b) a test that prints
   "output looks good" for a human to review; (c) a test written six months
   after the feature shipped.

---

## Next Lesson

**[Lesson 02 → unittest Framework](lesson-02-unittest.md)**
