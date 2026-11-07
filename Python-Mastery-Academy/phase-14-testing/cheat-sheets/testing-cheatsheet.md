# ⚡ Phase 14 Cheat Sheet — Testing

---

## pytest Quick Start

```bash
pip install pytest pytest-cov

pytest                          # run all tests
pytest test_file.py             # specific file
pytest -v                       # verbose
pytest -v -k "keyword"          # filter
pytest --tb=short               # short traceback
pytest --co                     # collect only (list)
```

---

## Test Structure

```python
# Naming: test_*.py or *_test.py
# Functions: test_*

def test_something():
    assert 2 + 2 == 4

class TestMyClass:
    def test_method(self):
        assert True
```

---

## Assertions

```python
assert result == expected
assert result != wrong
assert result > 0
assert result is None
assert isinstance(x, int)
assert "key" in dict_obj
assert item in list_obj
assert result == pytest.approx(0.3)   # floats

# Exceptions
import pytest
with pytest.raises(ValueError):
    risky_function()

with pytest.raises(ValueError, match="positive"):
    validate(-1)
```

---

## Fixtures

```python
@pytest.fixture
def sample_data():
    return {"name": "Alice", "score": 95}

def test_name(sample_data):
    assert sample_data["name"] == "Alice"

# With setup + teardown
@pytest.fixture
def db():
    connection = setup_db()
    yield connection         # test runs here
    connection.close()       # teardown

# Scope: function (default), class, module, session
@pytest.fixture(scope="session")
def shared_resource():
    return create_once()
```

---

## Parametrize

```python
@pytest.mark.parametrize("input, expected", [
    (0, 0),
    (5, 25),
    (-3, 9),
])
def test_square(input, expected):
    assert square(input) == expected
```

---

## Mocking

```python
from unittest.mock import Mock, patch, MagicMock

# Mock an object
mock = Mock()
mock.method.return_value = 42
mock.method()   # returns 42

# Patch in context
with patch("module.function") as mock_fn:
    mock_fn.return_value = "fake"
    result = function_under_test()

# Patch as decorator
@patch("requests.get")
def test_api(mock_get):
    mock_get.return_value.json.return_value = {"data": "test"}
    result = my_api_function()
    assert result == "test"
```

---

## Coverage

```bash
pytest --cov=src --cov-report=term-missing
pytest --cov=src --cov-report=html
# HTML report in htmlcov/
```

---

## What to Test

```
✅ Normal/happy path inputs
✅ Edge cases (zero, empty, max, min)
✅ Invalid inputs (wrong type, negative, None)
✅ Error cases (exceptions that should be raised)
✅ Boundary values (just above/below thresholds)

❌ External services (mock them)
❌ Third-party code (they test it)
❌ Simple property assignments
```

---

## TDD Cycle

```
1. RED   — write a failing test for new behaviour
2. GREEN — write minimal code to make it pass
3. REFACTOR — improve code, keep tests green
Repeat
```
