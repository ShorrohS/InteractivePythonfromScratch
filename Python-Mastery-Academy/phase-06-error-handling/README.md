# 🛡️ Phase 06 — Error Handling

> **Goal:** Write programs that handle failures gracefully instead of crashing.

---

## Why Error Handling?

Every program will encounter errors. The question is: does it crash, or does it recover gracefully?

```
Without error handling:
  User enters "abc" for age → CRASH
  File is missing → CRASH
  Network is down → CRASH

With error handling:
  User enters "abc" → "Please enter a valid number."
  File is missing → "File not found. Creating new one."
  Network is down → "Connection failed. Retrying in 5s."
```

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-try-except.md](concepts/lesson-01-try-except.md) | try/except basics |
| 02 | [lesson-02-multiple.md](concepts/lesson-02-multiple.md) | Multiple exception types |
| 03 | [lesson-03-finally.md](concepts/lesson-03-finally.md) | finally and else |
| 04 | [lesson-04-raise.md](concepts/lesson-04-raise.md) | raise and custom exceptions |
| 05 | [lesson-05-defensive.md](concepts/lesson-05-defensive.md) | Defensive programming |

---

## Core Syntax

```python
try:
    # Code that might fail
    result = 10 / 0
except ZeroDivisionError:
    # Handle specific error
    print("Cannot divide by zero")
except ValueError as e:
    # Handle another type; 'e' has the error message
    print(f"Value error: {e}")
except Exception as e:
    # Catch-all
    print(f"Unexpected error: {e}")
else:
    # Runs only if NO exception occurred
    print(f"Result: {result}")
finally:
    # ALWAYS runs, with or without exception
    print("Done.")
```

---

## Common Exception Types

| Exception | When it occurs |
|-----------|---------------|
| `ValueError` | Wrong value type (e.g., int("abc")) |
| `TypeError` | Wrong type operation |
| `ZeroDivisionError` | Division by zero |
| `FileNotFoundError` | File doesn't exist |
| `KeyError` | Dictionary key doesn't exist |
| `IndexError` | List index out of range |
| `AttributeError` | Object doesn't have attribute |
| `ImportError` | Module can't be imported |
| `NameError` | Variable not defined |
| `ConnectionError` | Network failure |

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [ATM Simulator](guided-projects/project-01-atm-simulator/) | Full ATM with error handling |
| [Data Import Tool](guided-projects/project-02-data-import-tool/) | CSV import with validation |
| [Banking Simulator](guided-projects/project-03-banking-simulator/) | Banking with custom exceptions |

---

## ✅ Completion Checklist

- [ ] Understand try/except syntax
- [ ] Can catch specific exception types
- [ ] Use finally for cleanup
- [ ] Can raise exceptions with meaningful messages
- [ ] Can create custom exception classes
- [ ] Never use bare `except:` (always specify type)

---

## Previous: [Phase 05](../phase-05-file-handling/README.md) | Next: [Phase 07](../phase-07-oop/README.md)
