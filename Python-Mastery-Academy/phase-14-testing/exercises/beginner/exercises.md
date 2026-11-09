# 📝 Phase 14 — Beginner Exercises

> Attempt ALL questions before opening solutions.
> Solutions: `../../solutions/beginner/solutions.md`

---

## Section A: unittest Basics (Q1–Q2)

**Q1.** The `add()` function below has already been written. Your job is to write a `unittest.TestCase` that tests it using at least **three different assertion methods** (`assertEqual`, `assertNotEqual`, and one other of your choice).

```python
# Code under test
def add(a, b):
    return a + b
```

Requirements:
- Import `unittest` at the top of your test file
- Create a class `TestAdd` that inherits from `unittest.TestCase`
- Write three test methods: `test_positive_numbers`, `test_negative_numbers`, and `test_zeros`
- Each method must contain at least one assertion
- End the file with `if __name__ == "__main__": unittest.main()`

---

**Q2.** The `multiply()` function is defined below. Write a pytest test file with exactly **four** test functions covering: two positive numbers, a negative × positive, zero as one operand, and a float × integer.

```python
# Code under test
def multiply(a, b):
    return a * b
```

Requirements:
- Each test function must be named `test_<scenario>` (e.g. `test_positive_numbers`)
- Use plain `assert` statements — not `unittest` assertions
- No class needed; write bare functions at module level

---

## Section B: pytest Essentials (Q3–Q4)

**Q3.** The `divide()` function raises `ZeroDivisionError` when the divisor is 0. Write a pytest test that **verifies this exception is raised** using `pytest.raises` as a context manager. Then write a second test that verifies a normal division returns the correct float result.

```python
# Code under test
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

---

**Q4.** The `get_even_numbers()` function returns a list of even numbers from 0 up to (but not including) `n`. Write pytest tests that check the function returns the **exact expected list** for at least three different inputs, including `n=0` and `n=1`.

```python
# Code under test
def get_even_numbers(n):
    return [i for i in range(n) if i % 2 == 0]
```

---

## Section C: Reading pytest Output (Q5)

**Q5.** Study the four test functions below and predict what `pytest -v` will print. Write your prediction as a comment on each line: `PASS` or `FAIL` and a brief reason.

```python
# Code under test
def is_even(n):
    return n % 2 == 0

# --- test file: test_example.py ---
# Run with: pytest -v test_example.py

def test_four_is_even():
    assert is_even(4) == True      # prediction: ?

def test_three_is_even():
    assert is_even(3) == True      # prediction: ?

def test_zero_is_even():
    assert is_even(0) == True      # prediction: ?

def test_negative_even():
    assert is_even(-2) == True     # prediction: ?
```

After filling in your predictions, write the full expected `pytest -v` output as a multiline comment block below the tests. Include each test name with its PASSED/FAILED marker and the final summary line (e.g. `3 passed, 1 failed in 0.05s`).

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
