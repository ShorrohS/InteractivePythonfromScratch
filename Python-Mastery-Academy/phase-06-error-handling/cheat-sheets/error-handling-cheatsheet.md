# ⚡ Phase 06 Cheat Sheet — Error Handling

---

## Full Syntax

```python
try:
    risky_code()
except SpecificError as e:
    handle_specific(e)
except (TypeError, ValueError) as e:
    handle_multi(e)
except Exception as e:
    handle_any(e)
else:
    # Runs only if NO exception
    success()
finally:
    # ALWAYS runs
    cleanup()
```

---

## Common Exception Types

| Exception | Caused by |
|-----------|-----------|
| `ValueError` | Wrong value: `int("abc")` |
| `TypeError` | Wrong type: `"x" + 1` |
| `KeyError` | Missing dict key: `d["missing"]` |
| `IndexError` | List out of range: `[][0]` |
| `AttributeError` | Missing attribute: `None.upper()` |
| `FileNotFoundError` | File doesn't exist |
| `ZeroDivisionError` | Division by zero |
| `NameError` | Undefined variable |
| `ImportError` | Module not found |
| `RecursionError` | Infinite recursion |

---

## Custom Exceptions

```python
class AppError(Exception):
    """Base application exception."""

class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Validation error on '{field}': {message}")

class InsufficientFundsError(AppError):
    def __init__(self, balance, amount):
        super().__init__(f"Need ${amount:.2f}, have ${balance:.2f}")

# Usage
raise ValidationError("email", "Invalid format")
raise InsufficientFundsError(100, 500)
```

---

## raise

```python
raise ValueError("message")           # new exception
raise TypeError(f"Got {type(x)}")     # with detail

# Re-raise current exception
except Exception as e:
    log(e)
    raise    # re-raises same exception

# Chain exceptions
except IOError as e:
    raise AppError("Failed to load") from e
```

---

## Input Validation Pattern

```python
def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError("Must be positive")
            return value
        except ValueError as e:
            print(f"  Invalid: {e}. Try again.")
```

---

## Defensive Patterns

```python
# Safe dict access
value = d.get("key", default)

# Safe type conversion
def to_int(x, default=0):
    try: return int(x)
    except (ValueError, TypeError): return default

# Guard clauses
def process(data, user):
    if not data: raise ValueError("data required")
    if not user: raise ValueError("user required")
    return do_work(data, user)

# NEVER silently swallow exceptions
except Exception:
    pass    # BAD — hides bugs

# Log the error
except Exception as e:
    logger.error(f"Unexpected: {e}")
    return None    # or raise
```

---

## Exception Hierarchy (Simplified)

```
BaseException
└── Exception
    ├── ArithmeticError (ZeroDivisionError, OverflowError)
    ├── LookupError (KeyError, IndexError)
    ├── TypeError
    ├── ValueError
    ├── OSError (FileNotFoundError, PermissionError)
    └── RuntimeError (RecursionError)
```
