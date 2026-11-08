# Phase 06 — Advanced Exercises: Error Handling

**Difficulty:** ⭐⭐⭐ Advanced

---

**Q1. Retry Decorator**

Write a decorator factory `retry(max_attempts=3, delay=0.0, exceptions=(Exception,))` that:
- Retries the decorated function when it raises one of the listed exception types
- Waits `delay` seconds between attempts
- Re-raises the last exception (with the attempt count embedded in the message) after `max_attempts` are exhausted
- Does **not** retry on exception types not listed in `exceptions`

Use `functools.wraps` to preserve the wrapped function's name and docstring.

Test with a function that uses an external counter and fails for the first N calls then succeeds:
```python
call_count = 0

@retry(max_attempts=3, delay=0.0, exceptions=(ValueError,))
def flaky():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ValueError("not ready yet")
    return "success"
```
Show it succeeds on the third attempt, that a function failing all 3 times re-raises with the count, and that an unlisted exception type (`TypeError`) bubbles up immediately without retrying.

---

**Q2. Circuit Breaker**

Implement a `CircuitBreaker` class that wraps a callable and manages three states:

| State       | Behaviour |
|-------------|-----------|
| `CLOSED`    | Normal — calls pass through; failures increment a counter |
| `OPEN`      | Tripped — calls raise `CircuitBreakerOpenError` immediately without calling the wrapped function |
| `HALF_OPEN` | Probe — after `recovery_timeout` seconds, one call is allowed through; success → `CLOSED`, failure → `OPEN` |

Constructor signature: `CircuitBreaker(func, failure_threshold=3, recovery_timeout=5)`

Also define `CircuitBreakerOpenError(Exception)` as a distinct exception class.

Demonstrate the full state machine with a `flaky_service()` that fails 4 times then succeeds:
1. Calls 1–3 fail and trip the circuit to `OPEN`
2. Call 4 is blocked (`CircuitBreakerOpenError`)
3. After the recovery timeout, the circuit moves to `HALF_OPEN`
4. The probe call fails → circuit returns to `OPEN`
5. After another timeout, the probe call succeeds → circuit returns to `CLOSED`

---

**Q3. Exception Chaining**

Demonstrate Python's `raise X from Y` explicit exception chaining:

1. Define `DataAccessError(Exception)` (domain-level error).
2. Write `DataRepository.get_user(user_id)` that catches a low-level `IOError` and
   re-raises it wrapped in a `DataAccessError` using `from` (so `__cause__` is set).
3. Write `print_exception_chain(exc)` that walks `__cause__` and `__context__` to
   print each exception in the chain, indented by depth.
4. Show the difference between:
   - `raise X from Y` — sets `__cause__`, Python prints
     *"The above exception was the direct cause of the following"*
   - `raise X` inside an `except` block without `from` — sets `__context__`, Python
     prints *"During handling of the above exception, another exception occurred"*

---

**Q4. Accumulating Validation**

Build a validation framework that collects **all** errors before reporting, rather than stopping at the first failure:

Define:
- `ValidationError(Exception)` — carries a `field` name and a `message`
- `MultiValidationError(Exception)` — holds a `list[ValidationError]`; its `__str__` lists all of them with field names

Implement a `Validator` class with these methods:
- `require_non_empty(field, value)` — fail if None, empty, or whitespace-only
- `require_email(field, value)` — fail if value does not match a basic email pattern
- `require_int_range(field, value, min_val, max_val)` — fail if not an integer in range
- `require_positive_number(field, value)` — fail if not a positive number
- `raise_if_invalid()` — raises `MultiValidationError` if any errors were collected

Write `validate_user(name, email, age, salary)` that uses `Validator` for all four fields.

Test with three deliberately invalid fields (empty name, bad email, age below minimum) and a valid salary. Confirm the raised `MultiValidationError` contains **all three** errors at once.

---

**Q5. Safe JSON Config Loader**

Write a `ConfigLoader` class that loads application config from a JSON file with four layers of fallback:

1. **Missing file** — log a warning and use all defaults
2. **Malformed JSON** — log a warning and use all defaults
3. **Missing key** — log a warning and fill from that key's default
4. **Wrong type** — attempt coercion; if that fails, log a warning and use the default

Required config keys and their defaults:

| Key               | Type   | Default       |
|-------------------|--------|---------------|
| `host`            | `str`  | `"localhost"` |
| `port`            | `int`  | `8080`        |
| `debug`           | `bool` | `False`       |
| `max_connections` | `int`  | `10`          |

Use `logging` for all warnings (not `print`). Provide a `get(key, fallback=None)` method.

Demonstrate by loading:
1. A missing file → all defaults
2. A valid JSON file where `port` is the string `"9000"` → coerced to `int 9000`
3. A file containing only `{` (malformed JSON) → all defaults

---

**Q6. Robust CSV Processor**

Write `process_csv(csv_string, required_columns, type_map)` that:
- Validates `required_columns` exist in the CSV header
- Processes each data row independently, applying `type_map` conversions
- **Skips** bad rows (empty row, missing required values, type conversion failure)
  instead of crashing
- Records each skipped row in an error report with `row` number and `error` message
- Returns `(successful_rows, error_report)`

`type_map` is a dict mapping column name → callable, e.g. `{"age": int, "salary": float}`.

Test with this CSV (6 data rows):
```
name,age,department,salary
Alice,30,Engineering,85000.0
Bob,25,Marketing,60000.0
Carol,35,Engineering,92000.0
Dave,,Sales,
Alice2,abc,Engineering,85000.0
,,,
```
Row 4 (`Dave`) has missing required values, row 5 (`Alice2`) has a bad `age` type, row 6 is empty.

Expected result: **3 successful rows** and **3 entries** in the error report.

---

> **Solutions:** `../../solutions/advanced/solutions.py`
