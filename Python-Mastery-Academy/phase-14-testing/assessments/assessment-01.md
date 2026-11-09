# Phase 14 — Completion Assessment

> Complete before moving to Phase 15.
> Pass mark: 80% | Time: 45 minutes

---

## The Code Under Test

Both `Stack` and `EmailNotifier` are provided here. Do **not** modify these classes — only write tests for them.

```python
# stack.py

class Stack:
    """A last-in, first-out (LIFO) data structure."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Push an item onto the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("Cannot peek an empty stack")
        return self._items[-1]

    def is_empty(self):
        """Return True if the stack has no items."""
        return len(self._items) == 0
```

```python
# notifier.py
import smtplib

class EmailNotifier:
    """Sends confirmation emails using SMTP."""

    def __init__(self, smtp_host="smtp.example.com", port=587):
        self.smtp_host = smtp_host
        self.port      = port

    def send(self, to_address, subject, body):
        """Open an SMTP connection and send one email."""
        with smtplib.SMTP(self.smtp_host, self.port) as server:
            server.ehlo()
            server.starttls()
            server.login("user@example.com", "password")
            server.sendmail(
                "user@example.com",
                to_address,
                f"Subject: {subject}\n\n{body}",
            )
        return True
```

---

## PART A: unittest TestCase for Stack

**Task 1.** Write a `unittest.TestCase` subclass called `TestStack`. It must have at least **8 test methods** covering:

1. A new stack is empty
2. A stack is not empty after pushing an item
3. `push` followed by `pop` returns the pushed value
4. Multiple pushes — `pop` returns items in LIFO order
5. `peek` returns the top item without removing it
6. `pop` on an empty stack raises `IndexError`
7. `peek` on an empty stack raises `IndexError`
8. Pushing items of different types (int, str, list) all work correctly

Requirements:
- Use `setUp` to create a fresh `Stack` before every test
- Use at least 4 different assertion methods (`assertEqual`, `assertTrue`, `assertFalse`, `assertRaises`)
- Include `if __name__ == "__main__": unittest.main()` at the bottom

---

## PART B: pytest with Fixtures and Parametrize

**Task 2.** Rewrite the same tests using **pytest** (plain functions, no class).

Additional requirements:
- Define a `stack` fixture that returns a fresh `Stack` instance
- Use `@pytest.mark.parametrize` to test `push()` with at least four values: an integer, a string, a float, and `None`
- Each parametrized case should verify that after pushing the value, `stack.peek()` returns that same value

---

## PART C: Mocking smtplib.SMTP

**Task 3.** Write tests for `EmailNotifier.send()` that **mock `smtplib.SMTP`** so no real email is sent and no network connection is opened.

Your tests must:

1. Verify that `send()` returns `True` on success
2. Verify that `smtplib.SMTP` was called with the correct host and port (`"smtp.example.com"`, `587`)
3. Verify that `server.sendmail` was called with the correct `from_address`, `to_address`, and a message containing the subject

Hint: `smtplib.SMTP` is used as a context manager (`with smtplib.SMTP(...) as server:`). You will need to configure the mock to support context manager protocol.

---

## PART D: TDD — Add size() and clear()

**Task 4.** Using red-green-refactor, add two new methods to `Stack`:
- `size()` — returns the number of items currently on the stack
- `clear()` — removes all items

Steps:
1. Write failing tests for `size()` and `clear()` first (red)
2. Add the methods to `Stack` and make the tests pass (green)
3. Confirm no existing tests broke (refactor check)

Your answer should show the failing tests, the implementation additions, and a comment confirming everything passes.

---

## Scoring

| Task | Points | What is assessed |
|------|--------|-----------------|
| Task 1 (unittest) | 25 | 8 test methods, setUp, 4 assertion types |
| Task 2 (pytest + parametrize) | 25 | fixture, parametrize decorator, correct assertions |
| Task 3 (mocking) | 25 | patch target, context manager mock, assert_called_with |
| Task 4 (TDD) | 25 | failing tests first, correct implementation, no regressions |
| **Total** | **100** | |

Pass: 80/100 | Distinction: 95/100

---

## Answer Key

### Task 1 — unittest

```python
import unittest
from stack import Stack

class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = Stack()

    def test_new_stack_is_empty(self):
        self.assertTrue(self.stack.is_empty())

    def test_stack_not_empty_after_push(self):
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())

    def test_push_then_pop_returns_value(self):
        self.stack.push(42)
        result = self.stack.pop()
        self.assertEqual(result, 42)

    def test_lifo_order(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.assertEqual(self.stack.pop(), 3)  # last in, first out
        self.assertEqual(self.stack.pop(), 2)

    def test_peek_returns_top_without_removing(self):
        self.stack.push(99)
        top = self.stack.peek()
        self.assertEqual(top, 99)
        self.assertFalse(self.stack.is_empty())   # still there

    def test_pop_empty_raises_index_error(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_peek_empty_raises_index_error(self):
        with self.assertRaises(IndexError):
            self.stack.peek()

    def test_push_different_types(self):
        self.stack.push(10)
        self.stack.push("hello")
        self.stack.push([1, 2, 3])
        self.assertEqual(self.stack.peek(), [1, 2, 3])  # last pushed is on top

if __name__ == "__main__":
    unittest.main()
```

---

### Task 2 — pytest + fixtures + parametrize

```python
import pytest
from stack import Stack

@pytest.fixture
def stack():
    # Fresh Stack instance for each test
    return Stack()

def test_new_stack_is_empty(stack):
    assert stack.is_empty()

def test_push_makes_not_empty(stack):
    stack.push(1)
    assert not stack.is_empty()

def test_pop_returns_last_pushed(stack):
    stack.push("a")
    stack.push("b")
    assert stack.pop() == "b"

def test_peek_does_not_remove(stack):
    stack.push(7)
    _ = stack.peek()
    assert not stack.is_empty()

def test_pop_empty_raises(stack):
    with pytest.raises(IndexError):
        stack.pop()

def test_peek_empty_raises(stack):
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize("value", [
    42,           # integer
    "hello",      # string
    3.14,         # float
    None,         # NoneType
])
def test_push_peek_roundtrip(stack, value):
    # After pushing any value, peek should return that exact value
    stack.push(value)
    assert stack.peek() == value
```

---

### Task 3 — Mocking smtplib.SMTP

```python
import pytest
from unittest.mock import patch, MagicMock
from notifier import EmailNotifier

@patch("notifier.smtplib.SMTP")          # patch where it is USED, not where it is defined
def test_send_returns_true(mock_smtp_class):
    # Configure the mock to behave as a context manager
    mock_server = MagicMock()
    mock_smtp_class.return_value.__enter__.return_value = mock_server
    mock_smtp_class.return_value.__exit__.return_value  = False

    notifier = EmailNotifier()
    result = notifier.send("alice@example.com", "Hello", "Test body")

    assert result is True

@patch("notifier.smtplib.SMTP")
def test_smtp_called_with_correct_host_and_port(mock_smtp_class):
    mock_server = MagicMock()
    mock_smtp_class.return_value.__enter__.return_value = mock_server
    mock_smtp_class.return_value.__exit__.return_value  = False

    notifier = EmailNotifier()
    notifier.send("bob@example.com", "Subject", "Body")

    # Verify SMTP was constructed with the right host and port
    mock_smtp_class.assert_called_once_with("smtp.example.com", 587)

@patch("notifier.smtplib.SMTP")
def test_sendmail_called_with_correct_arguments(mock_smtp_class):
    mock_server = MagicMock()
    mock_smtp_class.return_value.__enter__.return_value = mock_server
    mock_smtp_class.return_value.__exit__.return_value  = False

    notifier = EmailNotifier()
    notifier.send("carol@example.com", "Welcome", "Hello Carol")

    # Verify sendmail was called; extract the actual call arguments
    args = mock_server.sendmail.call_args[0]
    assert args[0] == "user@example.com"       # from address
    assert args[1] == "carol@example.com"      # to address
    assert "Welcome" in args[2]                # subject in message body
```

---

### Task 4 — TDD: size() and clear()

```python
# STEP 1 — RED: Write failing tests first
# Run pytest → both tests fail with AttributeError: 'Stack' has no attribute 'size'

import pytest
from stack import Stack

def test_size_of_empty_stack():
    s = Stack()
    assert s.size() == 0          # fails: AttributeError

def test_size_after_pushes():
    s = Stack()
    s.push("a")
    s.push("b")
    s.push("c")
    assert s.size() == 3          # fails: AttributeError

def test_clear_empties_stack():
    s = Stack()
    s.push(1)
    s.push(2)
    s.clear()
    assert s.is_empty()           # fails: AttributeError
    assert s.size() == 0          # fails: AttributeError

def test_clear_then_push_works():
    s = Stack()
    s.push(10)
    s.clear()
    s.push(20)
    assert s.peek() == 20         # fails: AttributeError on clear()

# STEP 2 — GREEN: Add the two methods to Stack (in stack.py)
#
#     def size(self):
#         """Return the number of items on the stack."""
#         return len(self._items)
#
#     def clear(self):
#         """Remove all items from the stack."""
#         self._items.clear()
#
# Run pytest → all 4 new tests pass; all 8 original tests still pass.

# STEP 3 — REFACTOR: No changes needed here — implementation is already clean.
# Confirm: pytest -v → 12 tests collected, 12 passed.
```
