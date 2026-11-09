# ⚡ Phase 14 Quick Reference — Testing

---

## 1. unittest Assertions

| Method | Passes when… |
|--------|-------------|
| `assertEqual(a, b)` | `a == b` |
| `assertNotEqual(a, b)` | `a != b` |
| `assertTrue(expr)` | `bool(expr)` is `True` |
| `assertFalse(expr)` | `bool(expr)` is `False` |
| `assertIsNone(x)` | `x is None` |
| `assertIsNotNone(x)` | `x is not None` |
| `assertIn(a, b)` | `a in b` |
| `assertNotIn(a, b)` | `a not in b` |
| `assertRaises(Exc, fn, *args)` | calling `fn(*args)` raises `Exc` |
| `assertRaises(Exc)` as `with` | the `with` block raises `Exc` |
| `assertAlmostEqual(a, b)` | `round(a - b, 7) == 0` |
| `assertIsInstance(obj, cls)` | `isinstance(obj, cls)` |

```python
import unittest

class TestExample(unittest.TestCase):
    def setUp(self):          # runs before EVERY test method
        self.value = 42

    def tearDown(self):       # runs after EVERY test method
        pass

    def test_value(self):
        self.assertEqual(self.value, 42)
        self.assertIsInstance(self.value, int)

    def test_raises(self):
        with self.assertRaises(ZeroDivisionError):
            _ = 1 / 0

if __name__ == "__main__":
    unittest.main()
```

---

## 2. pytest Syntax

### Test naming rules
```
Files:     test_*.py  or  *_test.py
Functions: test_*
Classes:   Test*  (methods also test_*)
```

### Common patterns
```python
import pytest

# Plain assertion
def test_add():
    assert 1 + 1 == 2

# Exception testing
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0

# Exception message check
def test_error_message():
    with pytest.raises(ValueError, match="must be positive"):
        raise ValueError("Value must be positive")

# Warning check
def test_deprecation():
    with pytest.warns(DeprecationWarning):
        import warnings
        warnings.warn("old API", DeprecationWarning)

# Float comparison
def test_float():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

### Parametrize
```python
@pytest.mark.parametrize("x, expected", [
    (2, 4),
    (3, 9),
    (0, 0),
])
def test_square(x, expected):
    assert x ** 2 == expected
# Generates 3 independent tests
```

### Marks
```python
@pytest.mark.skip(reason="not implemented yet")
def test_future(): ...

@pytest.mark.skipif(sys.platform == "win32", reason="Linux only")
def test_linux(): ...

@pytest.mark.xfail(reason="known bug #42")
def test_known_failure(): ...
```

---

## 3. Fixtures

```python
import pytest

@pytest.fixture                        # function scope (default) — fresh per test
def db_connection():
    conn = create_connection()
    yield conn                         # value passed to test
    conn.close()                       # teardown runs after test

@pytest.fixture(scope="module")        # one instance per test file
def config():
    return load_config("test.cfg")

@pytest.fixture(scope="session")       # one instance for the entire run
def auth_token():
    return generate_token()

# Usage — inject by parameter name:
def test_query(db_connection, config):
    result = db_connection.query("SELECT 1")
    assert result is not None
```

### Fixture scopes at a glance

| Scope | Created | Destroyed | Best for |
|-------|---------|-----------|----------|
| `function` | before each test | after each test | mutable objects, stateful setup |
| `class` | before first test in class | after last test in class | shared class-level state |
| `module` | before first test in file | after last test in file | read-only data, file parsing |
| `session` | before first test in run | after all tests finish | auth tokens, DB schemas |

### Built-in fixtures
```python
def test_file(tmp_path):          # pathlib.Path to a temp dir; auto-cleaned
    f = tmp_path / "data.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"

def test_capsys(capsys):          # capture stdout/stderr
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
```

---

## 4. Mocking (unittest.mock)

### Mock vs MagicMock
| | `Mock` | `MagicMock` |
|-|--------|-------------|
| Any attribute access | returns `Mock` | returns `MagicMock` |
| Magic methods (`__len__`, `__iter__`, `__str__`) | raises `AttributeError` | pre-configured automatically |
| Use when | simple attribute/method mocking | need `len()`, `in`, iteration, context managers |

### Core patterns
```python
from unittest.mock import Mock, MagicMock, patch

# Basic mock
m = Mock()
m.some_method.return_value = 42
assert m.some_method() == 42

# Side effect — raise an exception
m.risky.side_effect = ValueError("boom")

# Side effect — return different values on successive calls
m.fetch.side_effect = [1, 2, 3]    # returns 1, then 2, then 3

# Verify calls
m.save({"id": 1})
m.save.assert_called_once_with({"id": 1})
m.save.assert_called_with({"id": 1})     # most recent call
assert m.save.call_count == 1
m.save.assert_any_call({"id": 1})        # any call matched
m.reset_mock()                           # clear call history
```

### patch as decorator
```python
from unittest.mock import patch

@patch("mymodule.requests.get")    # patch where it is USED, not defined
def test_api(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"key": "value"}
    result = mymodule.fetch_data()
    assert result == {"key": "value"}
    mock_get.assert_called_once()
```

### patch as context manager
```python
with patch("mymodule.open", mock_open(read_data="file contents")):
    data = mymodule.read_file("path.txt")
    assert data == "file contents"
```

### patch.object — patch one method on a real object
```python
from unittest.mock import patch

service = MyService()
with patch.object(service, "save", return_value=True) as mock_save:
    result = service.process()
    mock_save.assert_called_once()
```

### Mocking a context manager
```python
mock_smtp = MagicMock()
mock_server = MagicMock()
mock_smtp.return_value.__enter__.return_value = mock_server
mock_smtp.return_value.__exit__.return_value  = False

with patch("smtplib.SMTP", mock_smtp):
    send_email("to@example.com", "Subject", "Body")
    mock_server.sendmail.assert_called_once()
```

---

## 5. Coverage Commands

```bash
# Install
pip install pytest-cov

# Run tests + show coverage in terminal
pytest --cov=mymodule

# Show which lines were NOT covered
pytest --cov=mymodule --cov-report=term-missing

# Generate HTML report (open htmlcov/index.html)
pytest --cov=mymodule --cov-report=html

# Set a minimum threshold (fails if below 80%)
pytest --cov=mymodule --cov-fail-under=80

# Cover multiple modules
pytest --cov=src --cov-report=term-missing
```

Coverage report columns:
```
Name        Stmts   Miss  Cover   Missing
mymodule       25      3    88%   14, 22-23
```
- **Stmts** — total executable statements
- **Miss** — statements never reached by any test
- **Cover** — percentage of statements covered
- **Missing** — exact line numbers not covered

---

## 6. TDD Cycle

```
RED    → Write a failing test for the next feature
          Run pytest → see it FAIL (NameError or AssertionError is fine)
          A failing test is progress — it proves the feature is missing

GREEN  → Write the MINIMUM code to make that test pass
          Do not add features not tested yet
          Run pytest → see it PASS

REFACTOR → Clean up the code and the test
            Better names, extracted helpers, removed duplication
            Run pytest again → must still be all green
```

```python
# Pattern — TDD for a new function

# RED: test first (will fail — function doesn't exist yet)
def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello")   is False

# GREEN: minimal implementation
def is_palindrome(s):
    return s == s[::-1]

# REFACTOR: handle edge cases, add type hint
def is_palindrome(s: str) -> bool:
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

# Re-run: still green ✓
```

---

## 5 Most Common Patterns

### Pattern 1 — pytest fixture + parametrize together
```python
@pytest.fixture
def calculator():
    return Calculator()

@pytest.mark.parametrize("a, b, expected", [(1,2,3),(0,0,0),(-1,1,0)])
def test_add(calculator, a, b, expected):
    assert calculator.add(a, b) == expected
```

### Pattern 2 — mock an HTTP call
```python
@patch("myapp.requests.get")
def test_fetch(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": 42}
    assert myapp.fetch() == 42
```

### Pattern 3 — test file I/O with tmp_path
```python
def test_writes_file(tmp_path):
    out = tmp_path / "out.txt"
    write_data(out, "hello")
    assert out.read_text() == "hello"
```

### Pattern 4 — mock a dependency injected into a class
```python
def test_service():
    mock_repo = MagicMock()
    mock_repo.find.return_value = {"id": 1}
    svc = UserService(repo=mock_repo)
    result = svc.get(1)
    assert result["id"] == 1
    mock_repo.find.assert_called_once_with(1)
```

### Pattern 5 — conftest.py shared fixture
```python
# conftest.py (no imports needed in test files)
@pytest.fixture(scope="session")
def app_config():
    return {"env": "test", "debug": True}

# test_something.py
def test_env(app_config):
    assert app_config["env"] == "test"
```
