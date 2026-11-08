# Lesson 05 — Mocking and Patching

**Phase:** 14 — Testing | **Time:** ~45 min

---

## Part 1: Why Mock?

A unit test must be isolated from external systems. Real dependencies — databases,
HTTP endpoints, email servers, the clock, the filesystem — make tests slow,
brittle, and impossible to run offline.

**Mocking** replaces a real dependency with a controlled fake that:
- Returns whatever value you specify
- Records every call made to it
- Can raise exceptions on demand

```
Without mocking:                  With mocking:
  test → real email server  →       test → fake SMTP  → assertion
        (may fail, slow, cost)             (instant, deterministic)
```

`unittest.mock` ships with Python 3 — no installation needed.

```python
from unittest.mock import Mock, MagicMock, patch
```

---

## Part 2: The Mock Class

```python
from unittest.mock import Mock

# Create a mock object
m = Mock()

# Set what it returns when called
m.return_value = 42
print(m())          # 42

# Set return values for attribute access
m.name = "Alice"

# Set return value for a method
m.connect.return_value = True
print(m.connect("localhost"))   # True

# Raise an exception on call
m.side_effect = ConnectionError("timeout")
try:
    m()
except ConnectionError as e:
    print(e)   # timeout

# Return different values on successive calls
m.side_effect = [10, 20, 30]
print(m())   # 10
print(m())   # 20
print(m())   # 30
```

---

## Part 3: Mock Assertions

After a test runs, verify how the mock was used:

```python
from unittest.mock import Mock

m = Mock(return_value="ok")
m("hello")
m("hello")

print(m.call_count)              # 2
print(m.called)                  # True

m.assert_called_with("hello")    # most recent call arguments
m.assert_called_once()           # fails — called twice

m2 = Mock()
m2.send(to="alice@example.com", subject="Hello")
m2.send.assert_called_once_with(to="alice@example.com", subject="Hello")

m3 = Mock()
m3.assert_not_called()           # passes — never invoked
```

---

## Part 4: MagicMock for Magic Methods

`MagicMock` is a subclass of `Mock` that supports Python magic methods
(`__len__`, `__str__`, `__iter__`, etc.):

```python
from unittest.mock import MagicMock

m = MagicMock()
m.__len__.return_value = 5
print(len(m))            # 5

m.__str__.return_value = "FakeObject"
print(str(m))            # FakeObject

# Iteration
m.__iter__.return_value = iter([1, 2, 3])
print(list(m))           # [1, 2, 3]
```

Use `MagicMock` when the code under test calls magic methods on your dependency.

---

## Part 5: patch() as a Decorator

`patch()` replaces a named object in a module for the duration of a test, then
restores it automatically.

```python
from unittest.mock import patch

# The target is always "where it is USED, not where it is defined"
# If mymodule.py does: import os
# then patch: "mymodule.os.path.exists"

# As a decorator — mock is passed as the last parameter
@patch("os.path.exists")
def test_file_check(mock_exists):
    mock_exists.return_value = True
    from mymodule import check_file
    result = check_file("/some/path")
    mock_exists.assert_called_once_with("/some/path")
    assert result is True
```

Multiple patches stack (innermost decorator = first parameter):

```python
@patch("mymodule.send_email")
@patch("mymodule.get_user")
def test_notify(mock_get_user, mock_send_email):
    mock_get_user.return_value = {"email": "alice@example.com"}
    # ...
```

---

## Part 6: patch() as a Context Manager

```python
from unittest.mock import patch

def test_datetime_patched():
    with patch("datetime.datetime") as mock_dt:
        mock_dt.now.return_value = "2025-01-01 12:00:00"
        from mymodule import get_timestamp
        result = get_timestamp()
        assert result == "2025-01-01 12:00:00"
```

The context manager form is handy when you only need the mock for part of a test.

---

## Part 7: Complete Example — EmailNotifier

```python
# notifier.py
import smtplib

class EmailNotifier:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send(self, to: str, subject: str, body: str) -> bool:
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.sendmail(
                    "no-reply@app.com",
                    to,
                    f"Subject: {subject}\n\n{body}"
                )
            return True
        except smtplib.SMTPException:
            return False
```

```python
# test_notifier.py
from unittest.mock import patch, MagicMock
from notifier import EmailNotifier


@patch("notifier.smtplib.SMTP")
def test_send_calls_sendmail(mock_smtp_class):
    # Arrange: mock_smtp_class() returns a mock context manager
    mock_server = MagicMock()
    mock_smtp_class.return_value.__enter__.return_value = mock_server

    notifier = EmailNotifier("smtp.example.com", 587)

    # Act
    result = notifier.send("alice@example.com", "Hello", "Test body")

    # Assert
    assert result is True
    mock_smtp_class.assert_called_once_with("smtp.example.com", 587)
    mock_server.sendmail.assert_called_once()


@patch("notifier.smtplib.SMTP")
def test_send_returns_false_on_smtp_error(mock_smtp_class):
    import smtplib
    mock_smtp_class.return_value.__enter__.side_effect = smtplib.SMTPException

    notifier = EmailNotifier("smtp.example.com", 587)
    result = notifier.send("alice@example.com", "Hello", "Test body")

    assert result is False
```

---

## Part 8: Patching HTTP Requests

```python
# weather.py
import requests

def get_temperature(city: str) -> float:
    response = requests.get(f"https://api.weather.example.com/{city}")
    response.raise_for_status()
    return response.json()["temp_celsius"]
```

```python
# test_weather.py
from unittest.mock import patch, Mock
from weather import get_temperature


@patch("weather.requests.get")
def test_get_temperature_returns_parsed_value(mock_get):
    # Arrange — build a fake response
    mock_response = Mock()
    mock_response.json.return_value = {"temp_celsius": 22.5}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Act
    temp = get_temperature("London")

    # Assert
    assert temp == 22.5
    mock_get.assert_called_once_with(
        "https://api.weather.example.com/London"
    )


```

The `spec` parameter limits a Mock to only the attributes present on the real class —
useful to catch typos early: `Mock(spec=requests.Response)`.

---

## Practice Exercises

1. Write a function `read_config(path)` that calls `open(path)` and returns a
   dict parsed from JSON. Mock `builtins.open` to test it without a real file.

2. Write a `DatabaseRepo.save(record)` method that calls `conn.execute()`.
   Use a `MagicMock` for `conn` and assert that `execute` was called with the
   correct SQL and parameters.

3. Patch `datetime.datetime.now` to return a fixed timestamp. Write a function
   `stamped_message(text)` that prepends the current time, and test that it
   produces the expected output regardless of when the test runs.

4. Explain the rule "patch where the name is *used*, not where it is *defined*".
   Give a concrete example of a test that would silently fail if you patched
   the wrong location.

---

## Next Lesson

**[Lesson 06 → Code Coverage and Best Practices](lesson-06-coverage.md)**
