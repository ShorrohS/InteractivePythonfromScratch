# Lesson 02 — pytest Fundamentals

**Phase:** 14 — Testing | **Time:** ~35 min

---

## Part 1: Why pytest over unittest?

pytest is the industry-standard Python testing framework.

- Less boilerplate — no class required
- Better failure messages
- Powerful fixtures
- Rich plugin ecosystem
- Works with unittest tests too

```bash
pip install pytest pytest-cov
```

---

## Part 2: First Tests

```python
# test_calculator.py

def add(a, b): return a + b
def divide(a, b): return a / b if b != 0 else None

def test_add_positive():
    assert add(3, 5) == 8

def test_add_negative():
    assert add(-3, 5) == 2

def test_add_zero():
    assert add(0, 0) == 0

def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_by_zero_returns_none():
    assert divide(10, 0) is None

# Naming rules:
# File:     test_*.py or *_test.py
# Function: test_*
```

---

## Part 3: Running Tests

```bash
pytest                            # run all
pytest test_calculator.py         # specific file
pytest test_calculator.py::test_add_positive  # one test
pytest -v                         # verbose
pytest -v -k "divide"             # filter by name
pytest --tb=short                 # compact traceback
pytest --co                       # collect (list) only
```

---

## Part 4: Assertions

```python
# Equality
assert result == expected
assert result != wrong

# Comparisons
assert score > 90
assert 0 <= pct <= 100

# Types
assert isinstance(result, float)
assert isinstance(result, (int, float))

# Containers
assert "Alice" in names
assert key in my_dict

# Exceptions
import pytest

def test_raises_on_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_raises_with_message():
    with pytest.raises(ValueError, match="positive"):
        validate_amount(-50)

# Approximate equality (floats)
assert result == pytest.approx(0.3, rel=1e-6)
assert result == pytest.approx(expected, abs=0.01)
```

---

## Part 5: Fixtures

Fixtures provide reusable setup:

```python
import pytest

@pytest.fixture
def sample_employee():
    return {"name": "Alice", "salary": 85000, "dept": "Eng"}

@pytest.fixture
def empty_cart():
    return []

@pytest.fixture
def populated_cart():
    return [{"name": "Laptop", "price": 999.99}]

# Use fixture as parameter
def test_employee_has_name(sample_employee):
    assert sample_employee["name"] == "Alice"

def test_cart_is_empty(empty_cart):
    assert len(empty_cart) == 0

# Fixture with setup and teardown
@pytest.fixture
def temp_db():
    import sqlite3
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    yield conn          # ← test runs here
    conn.close()        # ← teardown after test

def test_insert(temp_db):
    temp_db.execute("INSERT INTO items (name) VALUES (?)", ("Widget",))
    temp_db.commit()
    row = temp_db.execute("SELECT name FROM items").fetchone()
    assert row[0] == "Widget"
```

---

## Part 6: Parametrize

Run same test with multiple inputs:

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (2,  3,  5),
    (0,  0,  0),
    (-1, 1,  0),
    (100, -50, 50),
])
def test_add(a, b, expected):
    assert add(a, b) == expected

@pytest.mark.parametrize("score, expected_grade", [
    (95, "A"),
    (85, "B"),
    (75, "C"),
    (65, "D"),
    (50, "F"),
])
def test_grade_assignment(score, expected_grade):
    assert calculate_grade(score) == expected_grade
```

---

## Part 7: Test Coverage

```bash
# Install
pip install pytest-cov

# Run with coverage
pytest --cov=src --cov-report=term-missing

# HTML report
pytest --cov=src --cov-report=html
# → open htmlcov/index.html

# Coverage shows which lines are not tested
# Aim for 80%+ coverage on business logic
```

---

## Part 8: Best Practices

```python
# 1. Test ONE thing per test function
# 2. Name tests clearly: test_<function>_<scenario>
# 3. Test happy path AND error cases
# 4. Don't test external services in unit tests (mock them)
# 5. Tests should be fast and independent
# 6. Setup in fixtures, not in test bodies
# 7. Use pytest.approx for float comparisons
```

---

## Practice Exercises

1. Write tests for a `is_palindrome(text)` function.

2. Write tests for a `calculate_discount(price, pct)` function — test normal, zero discount, and 100% discount.

3. Write a fixture that provides 3 different employee dicts, and write a parametrized test.

---

## Next Lesson

**[Lesson 03 → Fixtures & Mocking](lesson-03-fixtures.md)**
