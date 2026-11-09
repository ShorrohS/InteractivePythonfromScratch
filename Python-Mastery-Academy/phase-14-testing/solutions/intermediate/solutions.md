# Phase 14 — Intermediate Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/intermediate/exercises.md`

---

## Q1. pytest Fixture for BankAccount

```python
import pytest

# --- Code under test ---
class BankAccount:
    def __init__(self, initial_balance=0):
        self._balance = initial_balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def get_balance(self):
        return self._balance

# --- Fixture ---
@pytest.fixture
def account():
    # Returns a fresh BankAccount with $500 before each test
    return BankAccount(initial_balance=500)

# --- Tests ---

def test_initial_balance(account):
    # Fixture provides the starting balance
    assert account.get_balance() == 500

def test_deposit_increases_balance(account):
    account.deposit(200)
    assert account.get_balance() == 700   # 500 + 200

def test_withdraw_decreases_balance(account):
    account.withdraw(100)
    assert account.get_balance() == 400   # 500 - 100

def test_withdraw_insufficient_funds_raises(account):
    # Withdrawing more than the balance must raise ValueError
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(1000)

def test_deposit_negative_raises(account):
    # Depositing a non-positive amount must raise ValueError
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(-50)
```

Key points:
- A fixture is a function decorated with `@pytest.fixture`; pytest injects it by matching the parameter name
- Each test receives a **fresh** fixture instance — changes in one test do not affect others
- Function-scope fixtures (the default) are called before every single test function

---

## Q2. Parametrize Temperature Converter

```python
import pytest

# --- Code under test ---
def celsius_to_fahrenheit(c):
    return (c * 9 / 5) + 32

# --- Parametrized test ---
@pytest.mark.parametrize("celsius, expected_f", [
    (0,    32.0),     # freezing point of water
    (100,  212.0),    # boiling point of water
    (-40,  -40.0),    # the point where C and F scales are equal
    (37,   98.6),     # normal human body temperature
    (20,   68.0),     # comfortable room temperature
])
def test_celsius_to_fahrenheit(celsius, expected_f):
    # pytest.approx handles floating-point rounding differences
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected_f, rel=1e-3)
```

Key points:
- `@pytest.mark.parametrize("arg1, arg2", [...])` — the string names the parameters, the list provides tuples of values
- pytest generates one individual test case per tuple, each with its own pass/fail result
- `pytest.approx` compares floats within a small relative tolerance — avoids `0.1 + 0.2 != 0.3` failures

---

## Q3. unittest with setUp and tearDown

```python
import unittest

# --- Code under test ---
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

# --- Test class ---
class TestStack(unittest.TestCase):

    def setUp(self):
        # Called before EVERY test method — creates a clean stack each time
        self.stack = Stack()

    def tearDown(self):
        # Called after EVERY test method — cleanup or confirmation
        print("--- test complete ---")

    def test_push_adds_item(self):
        self.stack.push(10)
        self.assertFalse(self.stack.is_empty())

    def test_pop_returns_last_item(self):
        self.stack.push(1)
        self.stack.push(2)
        result = self.stack.pop()
        self.assertEqual(result, 2)          # LIFO: last in, first out

    def test_peek_does_not_remove(self):
        self.stack.push(42)
        top = self.stack.peek()
        self.assertEqual(top, 42)
        self.assertFalse(self.stack.is_empty())  # item still there

    def test_is_empty_on_new_stack(self):
        self.assertTrue(self.stack.is_empty())

    def test_pop_empty_stack_raises(self):
        # assertRaises as a context manager catches the expected exception
        with self.assertRaises(IndexError):
            self.stack.pop()

if __name__ == "__main__":
    unittest.main()
```

Key points:
- `setUp` runs before every single test method — guarantees a clean state
- `tearDown` runs after every test method, even if the test failed
- `self.assertRaises(ExceptionType)` is the unittest equivalent of `pytest.raises`

---

## Q4. Mock an External API Call

```python
from unittest.mock import patch, MagicMock
import requests

# --- Code under test ---
def get_user(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    if response.status_code == 200:
        return response.json()
    return None

# --- Tests ---

@patch("requests.get")   # replaces requests.get for the duration of this test
def test_get_user_success(mock_get):
    # Configure the mock to simulate a 200 response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Alice"}
    mock_get.return_value = mock_response

    result = get_user(1)

    # Verify the return value
    assert result == {"id": 1, "name": "Alice"}
    # Verify requests.get was called with the correct URL
    mock_get.assert_called_once_with("https://api.example.com/users/1")

@patch("requests.get")
def test_get_user_not_found(mock_get):
    # Configure the mock to simulate a 404 response
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = get_user(99)

    assert result is None
    mock_get.assert_called_once_with("https://api.example.com/users/99")
```

Key points:
- `@patch("requests.get")` temporarily replaces `requests.get` with a `MagicMock` for the duration of the test
- The mock object is passed as the first argument after `self` (or the only argument for plain functions)
- `mock_get.return_value` sets what the mock returns when called
- `assert_called_once_with(...)` verifies the mock was called exactly once with those exact arguments

---

## Q5. Test File-Writing with tmp_path

```python
# --- Code under test ---
def write_report(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)

# --- Tests ---
# tmp_path is a built-in pytest fixture that provides a fresh temporary directory per test

def test_file_is_created(tmp_path):
    report_file = tmp_path / "report.txt"   # pathlib.Path object
    write_report(report_file, "Hello")
    assert report_file.exists()             # file must exist after the call

def test_file_content_is_correct(tmp_path):
    report_file = tmp_path / "report.txt"
    write_report(report_file, "Test content")
    assert report_file.read_text() == "Test content"

def test_second_write_overwrites(tmp_path):
    report_file = tmp_path / "report.txt"
    write_report(report_file, "First write")
    write_report(report_file, "Second write")
    # Only the second content should remain
    assert report_file.read_text() == "Second write"
```

Key points:
- `tmp_path` is injected by pytest — each test gets its own isolated temp directory
- The directory is automatically cleaned up after the test session
- `tmp_path / "filename"` uses `pathlib.Path` — clean cross-platform path construction
- `path.read_text()` reads the file content as a string — no need to open manually

---

## Q6. Return Values and Exceptions for an Inventory System

```python
import pytest

# --- Code under test ---
class Inventory:
    def __init__(self):
        self._stock = {}

    def add_item(self, name, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self._stock[name] = self._stock.get(name, 0) + quantity
        return self._stock[name]

    def remove_item(self, name, quantity):
        if name not in self._stock:
            raise KeyError(f"{name} not in inventory")
        if quantity > self._stock[name]:
            raise ValueError("Not enough stock")
        self._stock[name] -= quantity
        return self._stock[name]

    def get_quantity(self, name):
        return self._stock.get(name, 0)

# --- Fixture ---
@pytest.fixture
def inv():
    return Inventory()

# --- Tests: return values ---

def test_add_item_returns_total_quantity(inv):
    result = inv.add_item("apple", 10)
    assert result == 10       # return value is the new total

def test_add_same_item_twice_accumulates(inv):
    inv.add_item("apple", 10)
    result = inv.add_item("apple", 5)
    assert result == 15       # 10 + 5 = 15

def test_remove_item_returns_remaining(inv):
    inv.add_item("banana", 8)
    result = inv.remove_item("banana", 3)
    assert result == 5        # 8 - 3 = 5

def test_get_quantity_unknown_item_returns_zero(inv):
    assert inv.get_quantity("mango") == 0

# --- Tests: exceptions ---

def test_add_zero_quantity_raises(inv):
    with pytest.raises(ValueError, match="Quantity must be positive"):
        inv.add_item("apple", 0)

def test_remove_unknown_item_raises(inv):
    with pytest.raises(KeyError):
        inv.remove_item("ghost_item", 1)

def test_remove_more_than_stock_raises(inv):
    inv.add_item("cherry", 3)
    with pytest.raises(ValueError, match="Not enough stock"):
        inv.remove_item("cherry", 10)
```

---

## Q7. Measure Coverage

```python
# test_inventory_coverage.py
#
# Coverage commands:
#   Run tests + show coverage summary in terminal:
#       pytest --cov=inventory --cov-report=term-missing
#
#   Run tests + generate an HTML report in htmlcov/ folder:
#       pytest --cov=inventory --cov-report=html
#   Then open: htmlcov/index.html in your browser
#
# What does "90% coverage" mean?
#   It means 90% of the executable lines in inventory.py were reached
#   (i.e., "covered") by at least one test. 10% were never executed.
#
# Why not always aim for 100%?
#   Some branches are defensive guards (e.g. "should never happen" checks)
#   that are difficult or unnatural to trigger. Chasing the last 5-10%
#   often produces tests with little real value. 90%+ is typically
#   considered excellent for production code.

import pytest
from inventory import Inventory  # assume Inventory is in inventory.py

@pytest.fixture
def inv():
    return Inventory()

def test_add_item(inv):
    assert inv.add_item("apple", 5) == 5

def test_add_item_accumulates(inv):
    inv.add_item("apple", 5)
    assert inv.add_item("apple", 3) == 8

def test_add_invalid_quantity(inv):
    with pytest.raises(ValueError):
        inv.add_item("apple", 0)

def test_remove_item(inv):
    inv.add_item("banana", 10)
    assert inv.remove_item("banana", 4) == 6

def test_remove_unknown_raises(inv):
    with pytest.raises(KeyError):
        inv.remove_item("ghost", 1)

def test_remove_excess_raises(inv):
    inv.add_item("cherry", 2)
    with pytest.raises(ValueError):
        inv.remove_item("cherry", 5)

def test_get_quantity_existing(inv):
    inv.add_item("date", 7)
    assert inv.get_quantity("date") == 7

def test_get_quantity_missing(inv):
    assert inv.get_quantity("fig") == 0
# All branches of add_item, remove_item, and get_quantity are now covered → ~100%
```
