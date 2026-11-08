# Lesson 03 — pytest Fundamentals

**Phase:** 14 — Testing | **Time:** ~45 min

---

## Part 1: pytest vs unittest

pytest is the industry-standard Python testing framework.

| Feature | unittest | pytest |
|---------|----------|--------|
| Boilerplate | Class required | Plain functions |
| Assertions | `self.assertEqual(a, b)` | `assert a == b` |
| Failure messages | Basic | Rich diff output |
| Fixtures | `setUp` / `tearDown` | `@pytest.fixture` |
| Parameterization | Manual | `@pytest.mark.parametrize` |
| Plugin ecosystem | Limited | 1000+ plugins |

pytest runs existing unittest tests too — migration is gradual.

```bash
pip install pytest
```

---

## Part 2: Writing Test Functions

No class required. Any function starting with `test_` is discovered.

```python
# test_math.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def test_add_two_positives():
    assert add(3, 5) == 8

def test_add_negative():
    assert add(-3, 5) == 2

def test_divide_normal():
    assert divide(10, 2) == 5.0

# Exceptions
def test_divide_by_zero_raises():
    import pytest
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_by_zero_message():
    import pytest
    with pytest.raises(ValueError, match="zero"):
        divide(10, 0)

# Float comparisons — never use == for floats
def test_float_approx():
    import pytest
    assert divide(1, 3) == pytest.approx(0.333, abs=1e-3)

# Other assert patterns
def test_assorted_assertions():
    assert "Alice" in ["Alice", "Bob"]    # membership
    assert result is None                  # identity
    assert isinstance(3.14, float)         # type check
```

---

## Part 3: Running pytest

```bash
pytest                              # run all tests in project
pytest test_math.py                 # single file
pytest test_math.py::test_add_two_positives  # single test
pytest -v                           # verbose output
pytest -v -k "divide"               # filter by name substring
pytest -x                           # stop on first failure
pytest --tb=short                   # compact traceback
pytest -q                           # quiet (counts only)
```

---

## Part 4: Fixtures

Fixtures provide reusable setup. Request them by matching the parameter name.

```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Alice", "email": "alice@example.com", "balance": 500.0}

def test_user_has_name(sample_user):
    assert sample_user["name"] == "Alice"

def test_user_balance_is_positive(sample_user):
    assert sample_user["balance"] > 0
```

**Fixture scope** controls how often the object is created:
`function` (default, once per test) → `class` → `module` → `session` (once per run).

**Yield fixtures** for setup and teardown:

```python
@pytest.fixture(scope="module")
def db_connection():
    import sqlite3
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()
    yield conn          # ← test runs here
    conn.close()        # ← teardown after all tests in this module

def test_insert(db_connection):
    db_connection.execute("INSERT INTO items (name) VALUES (?)", ("Widget",))
    db_connection.commit()
    row = db_connection.execute("SELECT name FROM items").fetchone()
    assert row[0] == "Widget"
```

**conftest.py** — place shared fixtures here; pytest loads it automatically.
Any test file in the same directory (or below) can use them without importing.

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_product():
    return {"name": "Widget", "price": 9.99}
```

---

## Part 5: Parametrize

Run the same test logic with multiple inputs — one function, many cases.

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (2,   3,   5),
    (0,   0,   0),
    (-1,  1,   0),
    (100, -50, 50),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

pytest generates one test ID per row; failures show exactly which inputs failed.

---

## Part 6: Built-in Marks

```python
import pytest, sys

# Skip unconditionally
@pytest.mark.skip(reason="not implemented yet")
def test_export_to_pdf():
    pass

# Skip conditionally
@pytest.mark.skipif(sys.platform == "win32", reason="Linux only")
def test_unix_permissions():
    pass

# Expected to fail — runs but failure is not an error
@pytest.mark.xfail(reason="bug #123 open")
def test_known_bug():
    assert buggy_function() == "correct"
```

---

## Part 7: Complete Example — BankAccount

```python
# bank_account.py
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
```

```python
# test_bank_account.py
import pytest
from bank_account import BankAccount

# Three fixtures
@pytest.fixture
def empty_account():
    return BankAccount("Alice")

@pytest.fixture
def funded_account():
    return BankAccount("Bob", balance=1000.0)

@pytest.fixture
def small_account():
    return BankAccount("Carol", balance=50.0)


# Functional tests
def test_new_account_has_zero_balance(empty_account):
    assert empty_account.balance == 0.0

def test_deposit_increases_balance(empty_account):
    empty_account.deposit(200.0)
    assert empty_account.balance == 200.0

def test_withdraw_decreases_balance(funded_account):
    funded_account.withdraw(300.0)
    assert funded_account.balance == 700.0

def test_withdraw_more_than_balance_raises(small_account):
    with pytest.raises(ValueError, match="Insufficient"):
        small_account.withdraw(100.0)

def test_negative_initial_balance_raises():
    with pytest.raises(ValueError, match="negative"):
        BankAccount("Dave", balance=-100)


# Two parametrized tests
@pytest.mark.parametrize("amount", [100, 250, 999.99])
def test_valid_deposits(empty_account, amount):
    empty_account.deposit(amount)
    assert empty_account.balance == pytest.approx(amount)

@pytest.mark.parametrize("amount", [0, -10, -0.01])
def test_invalid_deposit_amounts_raise(empty_account, amount):
    with pytest.raises(ValueError):
        empty_account.deposit(amount)
```

---

## Practice Exercises

1. Write a `test_string_utils.py` with 5 test functions for a
   `reverse_words(sentence)` function. Include edge cases for empty string,
   single word, and extra spaces.

2. Create a `@pytest.fixture` that returns a list of 3 product dicts. Write
   three test functions that use it.

3. Write a parametrized test for a `clamp(value, min_val, max_val)` function
   covering: within range, below minimum, above maximum, and equal to each boundary.

4. Add `scope="module"` to a fixture and add a comment explaining when the
   fixture object is created and destroyed.

---

## Next Lesson

**[Lesson 04 → Test-Driven Development](lesson-04-tdd.md)**
