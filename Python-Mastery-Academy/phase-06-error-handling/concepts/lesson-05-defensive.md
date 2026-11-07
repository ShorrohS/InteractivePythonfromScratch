# Lesson 05 — Defensive Programming

**Phase:** 06 — Error Handling | **Time:** ~25 min

---

## Part 1: What is Defensive Programming?

Defensive programming means writing code that anticipates failures and handles them gracefully — rather than assuming everything will work perfectly.

**Principle:** *Hope for the best, plan for the worst.*

---

## Part 2: Input Validation

Validate at the boundaries of your system:

```python
def set_age(age: int) -> None:
    # Validate BEFORE doing anything
    if not isinstance(age, int):
        raise TypeError(f"Age must be int, got {type(age).__name__}")
    if age < 0 or age > 150:
        raise ValueError(f"Age must be 0–150, got {age}")
    # Safe to proceed
    self._age = age


def process_order(items: list, quantity: int) -> float:
    if not items:
        raise ValueError("Order must contain at least one item")
    if quantity < 1:
        raise ValueError(f"Quantity must be positive, got {quantity}")
    if quantity > 1000:
        raise ValueError(f"Quantity exceeds maximum (1000), got {quantity}")
    # ...
```

---

## Part 3: Guard Clauses (Fail Fast)

Return early on invalid conditions instead of nesting:

```python
# BAD — deep nesting
def process(data, user):
    if data:
        if user:
            if user.is_active:
                if len(data) > 0:
                    return do_processing(data, user)

# GOOD — guard clauses (fail fast)
def process(data, user):
    if not data:
        raise ValueError("Data cannot be empty")
    if not user:
        raise ValueError("User cannot be None")
    if not user.is_active:
        raise PermissionError("User account is inactive")

    return do_processing(data, user)
```

---

## Part 4: Safe Defaults and Fallbacks

```python
# Instead of crashing, use defaults
def get_config_value(config: dict, key: str, default=None):
    return config.get(key, default)

# Safe type conversion
def to_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# Safe dict access
def safe_get(d: dict, *keys, default=None):
    """Safely get a nested value."""
    current = d
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current

data = {"user": {"address": {"city": "London"}}}
print(safe_get(data, "user", "address", "city"))    # London
print(safe_get(data, "user", "phone", "number"))    # None (no error)
```

---

## Part 5: Assertions for Developer Contracts

```python
# Assertions check DEVELOPER assumptions (not user input)
def calculate_discount(price: float, rate: float) -> float:
    assert 0 <= rate <= 1, f"Rate must be 0-1, got {rate}"
    assert price >= 0, f"Price cannot be negative: {price}"
    return price * (1 - rate)

# Note: assertions can be disabled with python -O
# Use raise ValueError for user-facing validation
# Use assert for internal developer contracts
```

---

## Part 6: Logging Errors (Don't Swallow Silently)

```python
import logging

logger = logging.getLogger(__name__)

def process_record(record: dict) -> bool:
    try:
        validated = validate(record)
        result = transform(validated)
        save(result)
        return True
    except ValidationError as e:
        logger.warning(f"Invalid record skipped: {e} | record={record}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error processing record: {e}", exc_info=True)
        return False   # Don't let one record break the entire batch
```

---

## Part 7: Practical — Robust CSV Importer

```python
import csv
import logging

def import_csv(filepath: str) -> tuple[list, list]:
    """Import CSV and return (valid_records, error_records)."""
    valid, errors = [], []

    try:
        file_handle = open(filepath, "r", newline="")
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    except PermissionError:
        raise PermissionError(f"Cannot read file: {filepath}")

    with file_handle as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            try:
                # Validate and convert each field
                if not row.get("name", "").strip():
                    raise ValueError("Name is required")
                salary = float(row["salary"])
                if salary < 0:
                    raise ValueError(f"Salary cannot be negative: {salary}")

                valid.append({
                    "name":   row["name"].strip().title(),
                    "salary": salary,
                    "dept":   row.get("department", "Unknown").strip()
                })
            except (KeyError, ValueError) as e:
                errors.append({"row": i, "data": dict(row), "error": str(e)})

    return valid, errors
```

---

## Practice Exercises

1. Rewrite this function using guard clauses:
   ```python
   def approve_loan(age, income, credit):
       if age >= 21:
           if income >= 25000:
               if credit >= 650:
                   return True
   ```

2. Write a `safe_divide(a, b, default=0)` function that never raises an exception.

3. Write a `validate_email(email)` function that raises `ValueError` with a specific message for each failure case.

---

## Phase 06 Complete — Build the Projects!

**→ [Project 01 — ATM Simulator](../guided-projects/project-01-atm-simulator/)**
**→ [Project 02 — Data Import Tool](../guided-projects/project-02-data-import-tool/)**
**→ [Project 03 — Banking Simulator](../guided-projects/project-03-banking-simulator/)**
