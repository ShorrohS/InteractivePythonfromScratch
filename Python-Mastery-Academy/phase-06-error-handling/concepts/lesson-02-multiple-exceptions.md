# Lesson 02 — Multiple Exception Types

**Phase:** 06 — Error Handling | **Time:** ~25 min

---

## Part 1: Catching Specific Exception Types

Always catch the most specific exception you expect:

```python
# BAD — too broad, hides bugs
try:
    result = risky_code()
except Exception:
    print("Something failed")

# GOOD — specific, meaningful handling
try:
    result = risky_code()
except ValueError as e:
    print(f"Bad value: {e}")
except TypeError as e:
    print(f"Wrong type: {e}")
except ZeroDivisionError:
    print("Cannot divide by zero")
```

---

## Part 2: Multiple except Blocks

```python
def safe_convert_and_divide(text: str, divisor: str) -> float | None:
    try:
        number = int(text)       # might raise ValueError
        result = number / float(divisor)  # might raise ZeroDivisionError
        return result
    except ValueError:
        print(f"  Cannot convert '{text}' or '{divisor}' to number")
        return None
    except ZeroDivisionError:
        print("  Cannot divide by zero")
        return None

print(safe_convert_and_divide("10", "2"))      # 5.0
print(safe_convert_and_divide("abc", "2"))     # ValueError
print(safe_convert_and_divide("10", "0"))      # ZeroDivisionError
```

---

## Part 3: Catching Multiple Exceptions Together

```python
# Same handling for multiple exception types
try:
    data = process(raw_input)
except (ValueError, TypeError):
    print("Invalid data type or value")

# Catching with the exception object
try:
    result = complex_operation()
except (ValueError, KeyError, IndexError) as e:
    print(f"Data error ({type(e).__name__}): {e}")
```

---

## Part 4: Exception Hierarchy

Python exceptions form a hierarchy — catching a parent catches all children:

```
BaseException
└── Exception
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── TypeError
    ├── ValueError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── TimeoutError
    └── RuntimeError
        └── RecursionError
```

```python
# Catching LookupError catches both IndexError and KeyError
try:
    value = data[key]
except LookupError as e:
    print(f"Key/index not found: {e}")
```

---

## Part 5: Real-World Example — Data Import

```python
def import_employee_record(raw: dict) -> dict | None:
    """Parse a raw dict into a validated employee record."""
    try:
        return {
            "id":     int(raw["employee_id"]),
            "name":   str(raw["name"]).strip().title(),
            "salary": float(raw["salary"]),
            "dept":   str(raw["department"]).strip()
        }
    except KeyError as e:
        print(f"  Missing field: {e}")
        return None
    except ValueError as e:
        print(f"  Invalid value: {e}")
        return None
    except TypeError as e:
        print(f"  Wrong type: {e}")
        return None

# Process multiple records
raw_data = [
    {"employee_id": "101", "name": "Alice", "salary": "85000", "department": "Eng"},
    {"employee_id": "102", "name": "Bob",   "salary": "abc",   "department": "Sales"},
    {"name": "Carol", "salary": "75000", "department": "Marketing"},   # missing id
]

for raw in raw_data:
    record = import_employee_record(raw)
    if record:
        print(f"  Imported: {record['name']}")
```

---

## Practice Exercises

1. Write `safe_dict_access(d, key, default=None)` using try/except.

2. Write a function that reads a file and handles: FileNotFoundError, PermissionError, UnicodeDecodeError.

3. What exception does `[][0]` raise? What about `{}["key"]`?

---

## Next Lesson

**[Lesson 03 → finally and else](lesson-03-finally.md)**
