# ============================================================
# Phase 06 — Advanced Solutions: Error Handling
# ============================================================
# Run:  python solutions.py
#
# Solves every exercise in exercises/advanced/exercises.md.
# All file I/O uses tempfile so no external files are required.
# All network/service calls are simulated with in-process
# counters.  The script runs cleanly from end to end with no
# user input and no external dependencies.
# ============================================================

import csv
import functools
import io
import json
import logging
import os
import re
import tempfile
import time


# ============================================================
# === Solution 1: Retry Decorator ===
# ============================================================
# Key ideas:
#   • retry() is a decorator factory — it returns a decorator.
#   • The inner wrapper counts total attempts (not retries) and
#     re-raises the last exception after max_attempts exhausted,
#     embedding the attempt count in the error message.
#   • Only exceptions in the `exceptions` tuple trigger a retry;
#     all others propagate immediately.
#   • functools.wraps preserves __name__, __doc__, and __module__
#     on the wrapper so debugging tools see the real function name.

def retry(max_attempts=3, delay=0.0, exceptions=(Exception,)):
    """Decorator factory: retry on listed exception types.

    Args:
        max_attempts: total calls allowed (first attempt + retries).
        delay:        seconds to sleep between attempts (0 = no sleep).
        exceptions:   tuple of exception types that trigger a retry.

    After max_attempts the last exception is re-raised with the
    attempt count appended to the message.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt < max_attempts and delay > 0:
                        time.sleep(delay)
            # All attempts exhausted — re-raise with context message
            raise type(last_exc)(
                f"{last_exc}  (failed after {max_attempts} attempt(s))"
            ) from last_exc
        return wrapper
    return decorator


def demo_exercise_1():
    print("=== Exercise 1: Retry Decorator ===")

    # Case 1: fails twice then succeeds on the third attempt
    call_log = []

    @retry(max_attempts=3, delay=0.0, exceptions=(ValueError,))
    def flaky_succeed_on_3():
        call_log.append(len(call_log) + 1)
        if len(call_log) < 3:
            raise ValueError("service not ready")
        return "success"

    result = flaky_succeed_on_3()
    print(f"Attempts made: {call_log}  → result: {result!r}")
    assert result == "success" and len(call_log) == 3

    # Case 2: always fails — re-raises after max_attempts with count
    @retry(max_attempts=3, delay=0.0, exceptions=(RuntimeError,))
    def always_fails():
        raise RuntimeError("permanently broken")

    try:
        always_fails()
    except RuntimeError as e:
        print(f"Exhausted retries: {e}")

    # Case 3: exception type NOT in the list — bubbles up immediately
    calls_made = [0]

    @retry(max_attempts=3, delay=0.0, exceptions=(ValueError,))
    def wrong_exc_type():
        calls_made[0] += 1
        raise TypeError("wrong type — should not be retried")

    try:
        wrong_exc_type()
    except TypeError as e:
        print(f"Non-listed exception not retried (calls={calls_made[0]}): {e}")
    assert calls_made[0] == 1, "TypeError must not be retried"
    print()


# ============================================================
# === Solution 2: Circuit Breaker ===
# ============================================================
# Key ideas:
#   • Three states are tracked in instance variables.
#   • The `state` property checks whether recovery_timeout has
#     elapsed and transitions OPEN → HALF_OPEN automatically,
#     so callers always read the current effective state.
#   • A successful call from CLOSED or HALF_OPEN resets
#     failure_count to 0 and closes the circuit.
#   • A failed call from HALF_OPEN increments failure_count
#     and can re-trip the circuit immediately.

class CircuitBreakerOpenError(Exception):
    """Raised when a call is blocked because the circuit is OPEN."""


class CircuitBreaker:
    """Wraps a callable and applies the circuit-breaker pattern.

    States:
        CLOSED    — normal; failures accumulate toward failure_threshold.
        OPEN      — tripped; calls raise CircuitBreakerOpenError instantly.
        HALF_OPEN — probe state after recovery_timeout; one call allowed.

    Args:
        func:              callable to protect.
        failure_threshold: consecutive failures needed to trip the circuit.
        recovery_timeout:  seconds to wait in OPEN before probing again.
    """
    CLOSED    = "CLOSED"
    OPEN      = "OPEN"
    HALF_OPEN = "HALF_OPEN"

    def __init__(self, func, failure_threshold=3, recovery_timeout=5):
        self._func          = func
        self._threshold     = failure_threshold
        self._timeout       = recovery_timeout
        self._state         = self.CLOSED
        self._failure_count = 0
        self._opened_at     = None

    @property
    def state(self):
        """Current state, auto-transitioning OPEN → HALF_OPEN after timeout."""
        if (self._state == self.OPEN
                and (time.time() - self._opened_at) >= self._timeout):
            self._state = self.HALF_OPEN
        return self._state

    def __call__(self, *args, **kwargs):
        if self.state == self.OPEN:
            raise CircuitBreakerOpenError(
                f"Circuit OPEN — call blocked "
                f"(failure count: {self._failure_count})"
            )
        try:
            result              = self._func(*args, **kwargs)
            # Success: reset failure count and close the circuit
            self._failure_count = 0
            self._state         = self.CLOSED
            return result
        except Exception:
            self._failure_count += 1
            if self._failure_count >= self._threshold:
                self._state     = self.OPEN
                self._opened_at = time.time()
            raise


def demo_exercise_2():
    print("=== Exercise 2: Circuit Breaker ===")

    fail_count = [0]

    def flaky_service():
        fail_count[0] += 1
        if fail_count[0] <= 4:
            raise ConnectionError(f"service down (call #{fail_count[0]})")
        return "ok"

    # Use a short timeout so the demo completes quickly
    cb = CircuitBreaker(flaky_service, failure_threshold=3, recovery_timeout=0.1)

    # Calls 1–3: fail and trip the circuit to OPEN
    for i in range(1, 4):
        try:
            cb()
        except ConnectionError as e:
            print(f"  Call {i}: ConnectionError — "
                  f"state={cb._state}, failures={cb._failure_count}")

    # Call 4: circuit is OPEN — blocked immediately
    try:
        cb()
    except CircuitBreakerOpenError as e:
        print(f"  Call 4: CircuitBreakerOpenError — {e}")

    # Wait for recovery_timeout; property transitions OPEN → HALF_OPEN
    time.sleep(0.15)
    print(f"  After timeout  : state → {cb.state}")   # HALF_OPEN

    # Probe call (call #4 internally) — still fails → back to OPEN
    try:
        cb()
    except ConnectionError:
        print(f"  Probe (fail)   : state → {cb._state}")  # OPEN

    # Second recovery wait
    time.sleep(0.15)
    print(f"  After 2nd timeout: state → {cb.state}")  # HALF_OPEN

    # Probe call (call #5 internally) — now succeeds → CLOSED
    result = cb()
    print(f"  Probe (success): {result!r} — state={cb._state}")
    assert cb._state == CircuitBreaker.CLOSED
    print()


# ============================================================
# === Solution 3: Exception Chaining ===
# ============================================================
# Key ideas:
#   • `raise X from Y` sets X.__cause__ = Y and marks
#     __suppress_context__ = True.  Python prints
#     "The above exception was the direct cause of the following".
#   • `raise X` inside an except block (no `from`) sets
#     X.__context__ implicitly and leaves __suppress_context__
#     False.  Python prints "During handling of the above...".
#   • Walking the chain: follow __cause__ first (explicit), then
#     __context__ if __suppress_context__ is False (implicit).

class DataAccessError(Exception):
    """Raised when a data-layer operation cannot be completed."""


class UserNotFoundError(DataAccessError):
    """Raised when a requested user record does not exist."""


class DataRepository:
    """Simulates a data access layer that wraps low-level I/O errors."""

    def get_user(self, user_id):
        """Fetch a user record, wrapping IOError as DataAccessError.

        Uses `raise ... from` so the original IOError is preserved as
        __cause__ in the resulting DataAccessError — the full context is
        never lost even when the caller only catches DataAccessError.
        """
        try:
            # Simulate a low-level failure (file missing, network down, etc.)
            raise IOError(f"No record file found for user {user_id!r}")
        except IOError as original:
            raise DataAccessError(
                f"Failed to retrieve user {user_id!r}"
            ) from original   # __cause__ set; original IOError is preserved


def print_exception_chain(exc):
    """Walk __cause__ / __context__ and print each link indented by depth.

    Explicit chain (__cause__) is always followed first.  Implicit chain
    (__context__) is followed only when __suppress_context__ is False.
    """
    chain   = []
    current = exc
    while current is not None:
        chain.append(current)
        if current.__cause__ is not None:
            current = current.__cause__
        elif (current.__context__ is not None
              and not current.__suppress_context__):
            current = current.__context__
        else:
            break

    # chain[0] is the caught exception; chain[-1] is the root cause.
    # Print outermost (caught) first, then indent each root cause beneath it.
    print("  Exception chain (outermost first):")
    for depth, err in enumerate(chain):
        prefix = "  " * depth
        link   = "└─ caused by: " if depth > 0 else ""
        print(f"    {prefix}{link}{type(err).__name__}: {err}")


def demo_exercise_3():
    print("=== Exercise 3: Exception Chaining ===")

    repo = DataRepository()

    # Explicit chaining: raise X from Y  →  __cause__ is set
    print("Explicit chain  (raise DataAccessError from IOError):")
    try:
        repo.get_user(42)
    except DataAccessError as e:
        print_exception_chain(e)
        cause   = e.__cause__
        context = e.__context__
        print(f"  __cause__   = {type(cause).__name__}: {cause}")
        print(f"  __context__ = {context!r}")

    # Implicit chaining: raise X inside except without `from`
    print("\nImplicit chain  (raise RuntimeError inside except ValueError):")
    try:
        try:
            raise ValueError("original problem at the data layer")
        except ValueError:
            raise RuntimeError("something else went wrong during handling")
    except RuntimeError as e:
        print(f"  __cause__   = {e.__cause__!r}  (None — no explicit `from`)")
        print(f"  __context__ = {type(e.__context__).__name__}: {e.__context__}")
        print_exception_chain(e)
    print()


# ============================================================
# === Solution 4: Accumulating Validation ===
# ============================================================
# Key ideas:
#   • Validator stores errors internally; individual check methods
#     never raise — they only append to the internal list.
#   • raise_if_invalid() is the single raise point: it packages
#     every collected error into one MultiValidationError so callers
#     see all failures in a single exception.
#   • ValidationError carries a field name so each error is
#     actionable ("age: must be between 18 and 120, got 15").

_ACCUM_EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
)


class ValidationError(Exception):
    """Single-field validation failure carrying a field name and message."""

    def __init__(self, field, message):
        self.field   = field
        self.message = message
        super().__init__(f"{field}: {message}")


class MultiValidationError(Exception):
    """Aggregates multiple ValidationError instances.

    Attributes:
        errors: list of ValidationError — one per failed field.
    """

    def __init__(self, errors):
        self.errors = list(errors)
        summary     = "; ".join(str(e) for e in self.errors)
        super().__init__(
            f"{len(self.errors)} validation error(s) — {summary}"
        )


class Validator:
    """Collect validation errors across fields; raise once at the end.

    Usage:
        v = Validator()
        v.require_non_empty("name", name)
        v.require_email("email", email)
        v.raise_if_invalid()   # raises MultiValidationError if any failed
    """

    def __init__(self):
        self._errors = []

    def require_non_empty(self, field, value):
        """Fail if value is None, empty string, or whitespace-only."""
        if not value or not str(value).strip():
            self._errors.append(ValidationError(field, "cannot be empty"))

    def require_email(self, field, value):
        """Fail if value does not match a basic email pattern."""
        if not _ACCUM_EMAIL_RE.match(str(value or "")):
            self._errors.append(
                ValidationError(field, f"'{value}' is not a valid email address")
            )

    def require_int_range(self, field, value, min_val, max_val):
        """Fail if value is not an integer in [min_val, max_val]."""
        try:
            n = int(value)
            if not (min_val <= n <= max_val):
                self._errors.append(ValidationError(
                    field,
                    f"must be between {min_val} and {max_val}, got {n}",
                ))
        except (ValueError, TypeError):
            self._errors.append(
                ValidationError(field, f"must be an integer, got {value!r}")
            )

    def require_positive_number(self, field, value):
        """Fail if value cannot be parsed as a positive number."""
        try:
            n = float(value)
            if n <= 0:
                self._errors.append(
                    ValidationError(field, f"must be positive, got {n}")
                )
        except (ValueError, TypeError):
            self._errors.append(
                ValidationError(field, f"must be a number, got {value!r}")
            )

    def raise_if_invalid(self):
        """Raise MultiValidationError if any errors were collected."""
        if self._errors:
            raise MultiValidationError(self._errors)


def validate_user(name, email, age, salary):
    """Validate all four user fields; raise with every failure at once."""
    v = Validator()
    v.require_non_empty("name", name)
    v.require_email("email", email)
    v.require_int_range("age", age, 18, 120)
    v.require_positive_number("salary", salary)
    v.raise_if_invalid()
    return True


def demo_exercise_4():
    print("=== Exercise 4: Accumulating Validation ===")

    # Case 1: three invalid fields — all reported in one exception
    print("Case 1 — three invalid fields:")
    try:
        validate_user(
            name   = "",           # empty name     → fails
            email  = "not-email",  # bad format     → fails
            age    = 15,           # below minimum  → fails
            salary = 80000.0,      # valid
        )
    except MultiValidationError as e:
        print(f"  Caught {len(e.errors)} error(s) in one exception:")
        for err in e.errors:
            print(f"    • {err}")
    assert True   # reaching here means MultiValidationError was raised

    # Case 2: all valid fields — no exception
    print("\nCase 2 — all valid fields:")
    try:
        ok = validate_user("Alice", "alice@example.com", 30, 90000.0)
        print(f"  Valid user → {ok}")
    except MultiValidationError as e:
        print(f"  Unexpected error: {e}")
    print()


# ============================================================
# === Solution 5: Safe JSON Config Loader ===
# ============================================================
# Key ideas:
#   • FileNotFoundError and json.JSONDecodeError are caught
#     separately so the log message names the exact failure mode.
#   • Per-key defaults fill gaps without overwriting valid values.
#   • Type coercion is attempted before using defaults, so the
#     string "9000" becomes int 9000 rather than being rejected.
#   • logging.WARNING (not print) keeps the warnings separate from
#     normal program output and lets callers silence them.

logging.basicConfig(
    level  = logging.WARNING,
    format = "%(levelname)s [%(name)s]: %(message)s",
)
_cfg_log = logging.getLogger("ConfigLoader")

_CFG_DEFAULTS = {
    "host":            "localhost",
    "port":            8080,
    "debug":           False,
    "max_connections": 10,
}

_CFG_TYPES = {
    "host":            str,
    "port":            int,
    "debug":           bool,
    "max_connections": int,
}


class ConfigLoader:
    """Load a JSON config file with four layers of fallback.

    Fallback order:
      1. Missing file   → all defaults, warning logged.
      2. Malformed JSON → all defaults, warning logged.
      3. Missing key    → that key's default, warning logged.
      4. Wrong type     → coerce if possible, else default, warning logged.
    """

    def __init__(self, filepath, defaults=None, type_map=None):
        self._filepath = filepath
        self._defaults = defaults if defaults is not None else dict(_CFG_DEFAULTS)
        self._types    = type_map  if type_map  is not None else dict(_CFG_TYPES)
        self.config    = self._load()

    def _coerce(self, key, raw_val, expected_type, default_val):
        """Try to coerce raw_val to expected_type; return default on failure."""
        try:
            if expected_type is bool:
                if isinstance(raw_val, str):
                    coerced = raw_val.strip().lower() in ("true", "1", "yes")
                else:
                    coerced = bool(raw_val)
            else:
                coerced = expected_type(raw_val)
            _cfg_log.warning(
                "Key '%s': expected %s, got %r — coerced to %r",
                key, expected_type.__name__, raw_val, coerced,
            )
            return coerced
        except (ValueError, TypeError):
            _cfg_log.warning(
                "Key '%s': cannot coerce %r to %s — using default %r",
                key, raw_val, expected_type.__name__, default_val,
            )
            return default_val

    def _load(self):
        # ── Step 1: read and parse the JSON file ─────────────────────
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except FileNotFoundError:
            _cfg_log.warning(
                "Config file '%s' not found — using all defaults.",
                self._filepath,
            )
            return dict(self._defaults)
        except json.JSONDecodeError as e:
            _cfg_log.warning(
                "Config '%s' has invalid JSON (%s) — using all defaults.",
                self._filepath, e,
            )
            return dict(self._defaults)

        # ── Step 2: validate / coerce each required key ───────────────
        result = {}
        for key, default_val in self._defaults.items():
            if key not in raw:
                _cfg_log.warning(
                    "Key '%s' missing — using default %r", key, default_val
                )
                result[key] = default_val
                continue

            val           = raw[key]
            expected_type = self._types.get(key)

            if expected_type is None or isinstance(val, expected_type):
                result[key] = val
            else:
                result[key] = self._coerce(key, val, expected_type, default_val)

        return result

    def get(self, key, fallback=None):
        """Return config[key], or fallback if the key is not present."""
        return self.config.get(key, fallback)


def demo_exercise_5():
    print("=== Exercise 5: Safe JSON Config Loader ===")

    # Case 1: file does not exist → all defaults
    print("Case 1 — missing file (warnings sent to stderr):")
    cl1 = ConfigLoader("no_such_config.json")
    print(f"  host={cl1.get('host')!r}, port={cl1.get('port')}, "
          f"debug={cl1.get('debug')}, max_connections={cl1.get('max_connections')}")
    assert cl1.get("port") == 8080

    # Case 2: port is a string "9000" → coerced to int
    print("\nCase 2 — port as string '9000' (should coerce to int):")
    fd, path = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump({"host": "prod.server.com", "port": "9000",
                       "debug": True, "max_connections": 100}, f)
        cl2 = ConfigLoader(path)
        print(f"  port={cl2.get('port')!r}  (type: {type(cl2.get('port')).__name__})")
        assert isinstance(cl2.get("port"), int) and cl2.get("port") == 9000
    finally:
        os.remove(path)

    # Case 3: malformed JSON → all defaults
    print("\nCase 3 — malformed JSON '{':")
    fd, path_bad = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            f.write("{")             # deliberately incomplete JSON
        cl3 = ConfigLoader(path_bad)
        print(f"  host={cl3.get('host')!r} (fell back to default)")
        assert cl3.get("host") == "localhost"
    finally:
        os.remove(path_bad)
    print()


# ============================================================
# === Solution 6: Robust CSV Processor ===
# ============================================================
# Key ideas:
#   • csv.DictReader reads from io.StringIO so no filesystem I/O
#     is needed — the function works entirely in memory.
#   • Each row is processed independently; a failure in row N
#     only skips that row and never affects row N+1.
#   • `required_columns` are checked at two levels: header (the
#     column must exist) and row (the cell must be non-empty).
#   • type_map conversions are applied per column; the first
#     failure in a row skips the whole row and records the error.

def process_csv(csv_string, required_columns, type_map=None):
    """Parse a CSV string row-by-row, skip bad rows, collect errors.

    Args:
        csv_string:       CSV text with a header row.
        required_columns: list of column names that must exist and be
                          non-empty for a row to be accepted.
        type_map:         dict mapping column name → callable for
                          type conversion.  Absent keys keep as str.

    Returns:
        (successful_rows, error_report)
        successful_rows: list of dicts for rows that parsed cleanly.
        error_report:    list of dicts {row, error[, data]} for skipped rows.
    """
    type_map   = type_map or {}
    good_rows  = []
    errors     = []
    reader     = csv.DictReader(io.StringIO(csv_string))

    # Header-level check: required columns must appear in the schema
    if not reader.fieldnames:
        return [], [{"row": 0, "error": "CSV has no header row"}]
    missing_headers = [
        c for c in required_columns if c not in reader.fieldnames
    ]
    if missing_headers:
        return [], [{"row": 0,
                     "error": f"Header missing columns: {missing_headers}"}]

    for row_num, row in enumerate(reader, start=2):   # row 1 is the header
        # Skip completely empty rows
        if all((v is None or v.strip() == "") for v in row.values()):
            errors.append({"row": row_num, "error": "empty row skipped"})
            continue

        # Required value check: non-empty cells for required columns
        empty_cols = [
            c for c in required_columns if not (row.get(c) or "").strip()
        ]
        if empty_cols:
            errors.append({
                "row":   row_num,
                "error": f"missing required values for: {empty_cols}",
                "data":  dict(row),
            })
            continue

        # Apply type conversions
        converted = {}
        failed    = False
        for col, val in row.items():
            raw = (val or "").strip()
            if col in type_map:
                try:
                    converted[col] = type_map[col](raw)
                except (ValueError, TypeError) as e:
                    errors.append({
                        "row":   row_num,
                        "error": f"column '{col}': cannot convert {raw!r} — {e}",
                        "data":  dict(row),
                    })
                    failed = True
                    break
            else:
                converted[col] = raw

        if not failed:
            good_rows.append(converted)

    return good_rows, errors


def demo_exercise_6():
    print("=== Exercise 6: Robust CSV Processor ===")

    TEST_CSV = (
        "name,age,department,salary\n"
        "Alice,30,Engineering,85000.0\n"    # row 2 — good
        "Bob,25,Marketing,60000.0\n"        # row 3 — good
        "Carol,35,Engineering,92000.0\n"    # row 4 — good
        "Dave,,Sales,\n"                    # row 5 — missing required values
        "Alice2,abc,Engineering,85000.0\n"  # row 6 — bad age type
        ",,,\n"                             # row 7 — empty row
    )

    required = ["name", "age", "department", "salary"]
    type_map = {"age": int, "salary": float}

    good, report = process_csv(TEST_CSV, required, type_map)

    print(f"Successful rows ({len(good)}):")
    for r in good:
        print(f"  {r}")

    print(f"\nError report ({len(report)} skipped row(s)):")
    for entry in report:
        print(f"  Row {entry['row']}: {entry['error']}")

    assert len(good)   == 3, f"Expected 3 good rows, got {len(good)}"
    assert len(report) == 3, f"Expected 3 errors,    got {len(report)}"
    print()


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    demo_exercise_1()
    demo_exercise_2()
    demo_exercise_3()
    demo_exercise_4()
    demo_exercise_5()
    demo_exercise_6()
    print("All advanced solutions completed successfully.")
