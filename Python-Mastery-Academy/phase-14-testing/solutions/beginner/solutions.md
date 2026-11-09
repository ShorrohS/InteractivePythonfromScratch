# Phase 14 — Beginner Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/beginner/exercises.md`

---

## A1. unittest TestCase for add()

```python
import unittest

# --- Code under test ---
def add(a, b):
    return a + b

# --- Test class ---
class TestAdd(unittest.TestCase):

    def test_positive_numbers(self):
        # Two positive integers should sum correctly
        self.assertEqual(add(3, 4), 7)
        self.assertEqual(add(100, 200), 300)

    def test_negative_numbers(self):
        # Negative values should also work
        self.assertEqual(add(-1, -1), -2)
        self.assertNotEqual(add(-1, -1), 0)   # -2 is not 0

    def test_zeros(self):
        # Adding zero should not change the other operand
        self.assertEqual(add(0, 0), 0)
        self.assertTrue(add(5, 0) == 5)        # assertTrue: checks any boolean expression

if __name__ == "__main__":
    unittest.main()
```

Key points:
- `assertEqual(a, b)` — passes when `a == b`
- `assertNotEqual(a, b)` — passes when `a != b`
- `assertTrue(expr)` — passes when `bool(expr)` is `True`
- Every test method name must start with `test_`

---

## A2. pytest test functions for multiply()

```python
# --- Code under test (include at top of test file or import from a module) ---
def multiply(a, b):
    return a * b

# --- Test functions ---

def test_positive_numbers():
    # Standard multiplication of two positive integers
    assert multiply(3, 4) == 12

def test_negative_and_positive():
    # Negative × positive should give a negative result
    assert multiply(-3, 4) == -12

def test_zero_operand():
    # Anything × zero is zero
    assert multiply(7, 0) == 0
    assert multiply(0, 99) == 0

def test_float_and_integer():
    # Float × int should return a float
    result = multiply(2.5, 4)
    assert result == 10.0
    assert isinstance(result, float)
```

Key points:
- pytest discovers functions named `test_*` automatically
- Plain `assert` is used — pytest rewrites assertions to show helpful diffs on failure
- No imports needed for basic pytest usage

---

## B3. pytest.raises for divide()

```python
import pytest

# --- Code under test ---
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

# --- Tests ---

def test_divide_by_zero_raises():
    # pytest.raises as a context manager catches the expected exception
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_by_zero_message():
    # You can also check the exception message
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(5, 0)

def test_normal_division():
    # Verify the return value when no exception is expected
    result = divide(10, 2)
    assert result == 5.0

def test_division_returns_float():
    # Integer inputs still return a float (Python 3 true division)
    assert divide(7, 2) == 3.5
```

Key points:
- `with pytest.raises(ExceptionType):` — the block inside must raise that exact exception
- `match=` accepts a regex pattern to verify the exception message
- If the exception is NOT raised, the test fails

---

## B4. List equality test for get_even_numbers()

```python
# --- Code under test ---
def get_even_numbers(n):
    return [i for i in range(n) if i % 2 == 0]

# --- Tests ---

def test_empty_range():
    # n=0 means range(0) is empty → no even numbers
    assert get_even_numbers(0) == []

def test_single_element_range():
    # range(1) = [0], and 0 is even → returns [0]
    assert get_even_numbers(1) == [0]

def test_standard_range():
    # range(10) → evens are 0,2,4,6,8
    assert get_even_numbers(10) == [0, 2, 4, 6, 8]

def test_odd_upper_bound():
    # range(7) → evens are 0,2,4,6  (7 itself is excluded by range)
    assert get_even_numbers(7) == [0, 2, 4, 6]

def test_returns_list():
    # Verify the return type, not just the values
    result = get_even_numbers(5)
    assert isinstance(result, list)
```

Key points:
- `assert result == [...]` compares list contents in order — both must match exactly
- `isinstance(result, list)` is a useful secondary check on the return type
- Testing edge cases (`n=0`, `n=1`) catches off-by-one errors early

---

## C5. Predicting pytest -v output

```python
# --- Code under test ---
def is_even(n):
    return n % 2 == 0

# --- test_example.py with predictions ---

def test_four_is_even():
    assert is_even(4) == True      # PASS — 4 % 2 == 0 is True

def test_three_is_even():
    assert is_even(3) == True      # FAIL — 3 % 2 == 1, is_even(3) returns False

def test_zero_is_even():
    assert is_even(0) == True      # PASS — 0 % 2 == 0 is True

def test_negative_even():
    assert is_even(-2) == True     # PASS — -2 % 2 == 0 in Python is True

"""
Expected `pytest -v test_example.py` output:
===========================================

test_example.py::test_four_is_even   PASSED   [ 25%]
test_example.py::test_three_is_even  FAILED   [ 50%]
test_example.py::test_zero_is_even   PASSED   [ 75%]
test_example.py::test_negative_even  PASSED   [100%]

FAILURES
--------
FAILED test_example.py::test_three_is_even
AssertionError: assert False == True
 +  where False = is_even(3)

========================= 3 passed, 1 failed in 0.05s =========================
"""
```

Key points:
- `pytest -v` (verbose) shows the full test node ID (`filename::test_name`) and PASSED/FAILED per line
- The percentage in brackets shows progress through the collection
- When a test fails, pytest shows the `AssertionError` with the actual vs expected values
- In Python, `-2 % 2` evaluates to `0` (Python uses floored division for modulo), so `-2` is correctly identified as even
