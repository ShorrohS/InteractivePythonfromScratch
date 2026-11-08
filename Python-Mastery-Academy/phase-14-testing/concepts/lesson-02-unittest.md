# Lesson 02 — unittest Framework

**Phase:** 14 — Testing | **Time:** ~40 min

---

## Part 1: unittest.TestCase

Python ships with `unittest` — no installation needed. Every test class
inherits from `unittest.TestCase`.

```python
import unittest

class TestMyFeature(unittest.TestCase):

    def test_something(self):
        result = 1 + 1
        self.assertEqual(result, 2)

if __name__ == "__main__":
    unittest.main()
```

Rules:
- Class must inherit from `unittest.TestCase`
- Every test method must start with `test_`
- Use `self.assert*` methods — never bare Python `assert`

---

## Part 2: setUp and tearDown

`setUp()` runs **before each** test method. `tearDown()` runs **after each**,
even if the test fails.

```python
import unittest
import sqlite3

class TestOrderRepo(unittest.TestCase):

    def setUp(self):
        """Runs before every test — fresh database each time."""
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute(
            "CREATE TABLE orders (id INTEGER PRIMARY KEY, total REAL)"
        )
        self.conn.commit()

    def tearDown(self):
        """Runs after every test — close connection."""
        self.conn.close()

    def test_insert_order(self):
        self.conn.execute("INSERT INTO orders (total) VALUES (99.99)")
        self.conn.commit()
        row = self.conn.execute("SELECT total FROM orders").fetchone()
        self.assertEqual(row[0], 99.99)

    def test_empty_table_has_no_rows(self):
        count = self.conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        self.assertEqual(count, 0)
```

Each test gets a fresh database — tests are isolated from each other.

---

## Part 3: Class-Level Setup

`setUpClass()` and `tearDownClass()` run once for the whole class, not per test.
Use them for expensive setup (e.g. starting a server, connecting to a shared resource).

```python
import unittest

class TestWithSharedResource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before any test in this class."""
        cls.shared_data = [1, 2, 3, 4, 5]   # expensive to build once

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests in this class."""
        del cls.shared_data

    def test_list_length(self):
        self.assertEqual(len(self.shared_data), 5)

    def test_list_sum(self):
        self.assertEqual(sum(self.shared_data), 15)
```

---

## Part 4: Assertion Methods

Always pass `expected` before `actual` — this matches the error message wording.

```python
# Equality
self.assertEqual(add(3, 4), 7)             # a == b
self.assertNotEqual(status, "error")       # a != b

# Truth
self.assertTrue(user.is_active)            # bool(x) is True
self.assertFalse(cart.is_empty())          # bool(x) is False

# None checks
self.assertIsNone(result)                  # result is None
self.assertIsNotNone(user)                 # result is not None

# Membership
self.assertIn("Alice", names)              # "Alice" in names
self.assertNotIn("Bob", banned_users)      # "Bob" not in banned_users

# Floats — never use assertEqual for floats
self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)

# Comparisons
self.assertGreater(score, 90)              # score > 90
self.assertGreaterEqual(age, 18)           # age >= 18
self.assertLess(response_time, 0.5)        # response_time < 0.5

# Exceptions
with self.assertRaises(ValueError):
    Product("Widget", price=-1)

with self.assertRaises(ZeroDivisionError):
    divide(10, 0)
```

---

## Part 5: Running Tests

```bash
# Run a single test file
python -m unittest test_calculator.py

# Run a specific class
python -m unittest test_calculator.TestCalculator

# Run a specific method
python -m unittest test_calculator.TestCalculator.test_add

# Verbose output (shows each test name)
python -m unittest -v test_calculator.py

# Auto-discover all test_*.py files under a directory
python -m unittest discover -s tests -p "test_*.py"
```

Test discovery rules: looks for files matching `test*.py` (default), classes
inheriting `TestCase`, and methods starting with `test_`.

---

## Part 6: Complete Example — Calculator

```python
# calculator.py

class Calculator:
    """A simple calculator with four operations."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```

```python
# test_calculator.py

import unittest
from calculator import Calculator


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    # ── add ──────────────────────────────────────────────────
    def test_add_two_positive_numbers(self):
        self.assertEqual(self.calc.add(3, 7), 10)

    def test_add_negative_numbers(self):
        self.assertEqual(self.calc.add(-3, -4), -7)

    def test_add_positive_and_negative(self):
        self.assertEqual(self.calc.add(-5, 10), 5)

    def test_add_with_zero(self):
        self.assertEqual(self.calc.add(0, 99), 99)

    # ── subtract ─────────────────────────────────────────────
    def test_subtract_positive_numbers(self):
        self.assertEqual(self.calc.subtract(10, 3), 7)

    def test_subtract_gives_negative_result(self):
        self.assertEqual(self.calc.subtract(3, 10), -7)

    # ── multiply ─────────────────────────────────────────────
    def test_multiply_two_numbers(self):
        self.assertEqual(self.calc.multiply(4, 5), 20)

    def test_multiply_by_zero_gives_zero(self):
        self.assertEqual(self.calc.multiply(99, 0), 0)

    def test_multiply_negative_by_positive(self):
        self.assertEqual(self.calc.multiply(-3, 4), -12)

    # ── divide ───────────────────────────────────────────────
    def test_divide_even_numbers(self):
        self.assertEqual(self.calc.divide(10, 2), 5.0)

    def test_divide_returns_float(self):
        result = self.calc.divide(7, 2)
        self.assertAlmostEqual(result, 3.5, places=5)

    def test_divide_by_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_divide_by_zero_error_message(self):
        with self.assertRaises(ValueError) as ctx:
            self.calc.divide(10, 0)
        self.assertIn("zero", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

Running this produces:

```
test_add_negative_numbers ... ok
test_add_positive_and_negative ... ok
test_add_two_positive_numbers ... ok
test_add_with_zero ... ok
test_divide_by_zero_error_message ... ok
test_divide_by_zero_raises_value_error ... ok
test_divide_even_numbers ... ok
test_divide_returns_float ... ok
test_multiply_by_zero_gives_zero ... ok
test_multiply_negative_by_positive ... ok
test_multiply_two_numbers ... ok
test_subtract_gives_negative_result ... ok
test_subtract_positive_numbers ... ok

Ran 13 tests in 0.001s — OK
```

---

## Practice Exercises

1. Add a `power(base, exponent)` method to the Calculator and write at least
   four test methods covering it (positive exponent, zero exponent, negative
   exponent, and fractional base).

2. Create a `StringProcessor` class with `reverse(s)`, `is_palindrome(s)`, and
   `word_count(s)`. Write a `TestStringProcessor` class with `setUp` that
   creates the instance, and at least 8 test methods.

3. Write tests for a `Stack` class (`push`, `pop`, `peek`, `is_empty`). Include
   a test that verifies `pop()` on an empty stack raises `IndexError`.

4. What is the difference between `setUp` and `setUpClass`? Write a brief
   example that shows a case where `setUpClass` is more appropriate than `setUp`.

---

## Next Lesson

**[Lesson 03 → pytest Fundamentals](lesson-03-pytest-fundamentals.md)**
