# ============================================================
# Phase 06 — Intermediate Solutions: Error Handling
# ============================================================
# Run:  python solutions.py
#
# Solves every exercise in exercises/intermediate/exercises.md.
# Each section defines the required functions, then a
# demo_exercise_N() function shows them in action.
# Input-dependent functions are tested with simulated values
# via unittest.mock so the script runs non-interactively.
# Temporary files are created in-process and removed on exit.
# ============================================================

import contextlib
import os
import re
import tempfile
import time
from unittest.mock import patch


# ============================================================
# === Solution 1: Graceful File Reader ===
# ============================================================
# Key idea: wrap open() in a broad OSError handler.  OSError is
# the parent of FileNotFoundError, PermissionError, and all
# other I/O-related exceptions, so one except clause covers
# every realistic read failure.

def read_file_safe(filepath):
    """Return file contents as a string, or None on any read error.

    Catches OSError (parent of FileNotFoundError, PermissionError,
    etc.) so the caller never has to handle file-not-found itself.
    Encoding is explicitly set to utf-8 for portability.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def demo_exercise_1():
    print("=== Exercise 1: Graceful File Reader ===")

    # Create a real temp file, write to it, then read it back
    fd, path = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w") as f:
            f.write("Hello from temp file!\nSecond line here.")
        content = read_file_safe(path)
        print(f"Existing file → {repr(content[:30])}...")
        assert content is not None
    finally:
        os.remove(path)

    # Non-existent path — must return None, not raise
    result = read_file_safe("ghost_file_xyz_99999.txt")
    print(f"Missing file  → {result!r}")
    assert result is None, "Expected None for missing file"
    print()


# ============================================================
# === Solution 2: Validated Age Input Loop ===
# ============================================================
# Key idea: separate I/O from logic.  validate_age is a pure
# function with no side effects — it can be unit-tested without
# any mocking.  get_valid_age is a thin shell that delegates
# all validation to validate_age and only handles the loop/prompt.

def validate_age(value_str):
    """Parse and validate an age string.

    Returns (int, None) on success or (None, error_message) on failure.
    Handles ValueError from int() and a range check for 1–120.
    The input string is stripped of surrounding whitespace before parsing.
    """
    try:
        age = int(str(value_str).strip())
    except (ValueError, AttributeError):
        return None, f"'{value_str}' is not a valid integer."
    if not (1 <= age <= 120):
        return None, f"Age must be between 1 and 120, got {age}."
    return age, None


def get_valid_age():
    """Prompt repeatedly until the user enters a valid age (1–120).

    Prints each error message so the user understands what went wrong.
    Returns the validated integer age.
    """
    while True:
        raw = input("Enter your age (1-120): ").strip()
        age, error = validate_age(raw)
        if error:
            print(f"Invalid: {error}  Please try again.")
        else:
            return age


def demo_exercise_2():
    print("=== Exercise 2: Validated Age Input Loop ===")

    # Unit-test validate_age with no I/O
    cases = [
        ("25",    25,   "valid integer in range"),
        ("abc",   None, "non-integer string"),
        ("0",     None, "below minimum (0 < 1)"),
        ("200",   None, "above maximum (200 > 120)"),
        ("  42 ", 42,   "valid with surrounding whitespace"),
    ]
    for raw, expected_age, desc in cases:
        age, err = validate_age(raw)
        status   = "✓" if age == expected_age else "✗"
        print(f"  {status} validate_age({raw!r:<9}) → age={age!r:<4}  [{desc}]")

    # Simulate get_valid_age with mock inputs: two bad, then one good
    with patch("builtins.input", side_effect=["abc", "0", "28"]):
        age = get_valid_age()
    print(f"\nget_valid_age() mocked with ['abc', '0', '28'] → {age}")
    assert age == 28
    print()


# ============================================================
# === Solution 3: Safe Type Converter ===
# ============================================================
# Key idea: bool("False") is True in Python because any non-empty
# string is truthy.  We must intercept bool conversions and use
# string comparison to determine the intended boolean value before
# falling through to the generic try/except path.

def safe_convert(value, target_type, default=None):
    """Convert value to target_type, returning default on failure.

    Handles bool as a special case:
      - "true"/"1"/"yes"    → True
      - "false"/"0"/"no"   → False
      - other strings       → default  (avoids bool("abc") == True)

    All other types use a plain try/except around target_type(value).
    """
    if target_type is bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalised = value.strip().lower()
            if normalised in ("true",  "1", "yes"):
                return True
            if normalised in ("false", "0", "no"):
                return False
            return default          # unrecognised string — fall back
        try:
            return bool(value)      # int 0 → False, others → True
        except (ValueError, TypeError):
            return default

    try:
        return target_type(value)
    except (ValueError, TypeError):
        return default


def demo_exercise_3():
    print("=== Exercise 3: Safe Type Converter ===")

    cases = [
        ("42",    int,   None,  42,    "string integer"),
        ("3.14",  float, None,  3.14,  "string float"),
        ("hello", int,   0,     0,     "invalid int → default"),
        ("true",  bool,  None,  True,  "truthy string"),
        ("false", bool,  None,  False, "falsy string"),
        ("False", bool,  None,  False, "capital-F False string"),
        (None,    float, -1.0, -1.0,   "None → float default"),
        ("yes",   bool,  None,  True,  "'yes' → True"),
    ]
    for val, typ, dflt, expected, desc in cases:
        result = safe_convert(val, typ, dflt)
        status = "✓" if result == expected else "✗"
        print(f"  {status} safe_convert({val!r:<8}, {typ.__name__:<5}, {dflt!r:<5})"
              f" → {result!r:<6}  [{desc}]")
    print()


# ============================================================
# === Solution 4: try / except / else / finally — All Four ===
# ============================================================
# Key idea: else is the "happy-path continuation" — it only runs
# when try completes without any exception.  Using else (rather
# than putting success logic at the end of try) makes the intent
# explicit: this code only runs if nothing went wrong.
# finally is perfect for audit logging or cleanup — it always
# runs whether the call succeeded, failed, or was interrupted.

def process_data_file(filepath):
    """Open filepath, convert each non-empty line to float, return the sum.

    Clause roles
    ────────────
    try     open the file and run the float conversions (the risky part)
    except  handle missing file or non-numeric data
    else    print results — only reached when try had no exception
    finally always print a "finished" audit line (cleanup / logging)

    Returns the sum as a float on success, or None on any error.
    """
    result = None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        total = sum(float(ln) for ln in lines)   # ValueError on bad data
    except FileNotFoundError:
        print(f"  [ERROR] File not found: {filepath}")
    except ValueError as e:
        print(f"  [ERROR] Non-numeric data in file: {e}")
    else:
        # Runs only when try completed without raising
        result = total
        print(f"  [OK]    {len(lines)} line(s) summed to {result}")
    finally:
        # Runs every time — good for audit logs and resource cleanup
        print(f"  [DONE]  Finished attempt for: {os.path.basename(filepath)}")
    return result


def demo_exercise_4():
    print("=== Exercise 4: try/except/else/finally ===")

    # Case 1: valid file — else clause runs
    fd, path_good = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w") as f:
        f.write("10.5\n20.0\n30.5\n")
    print("Case 1 — valid numeric file:")
    r = process_data_file(path_good)
    assert r == 61.0, f"Expected 61.0, got {r}"
    os.remove(path_good)
    print()

    # Case 2: file does not exist — FileNotFoundError branch
    print("Case 2 — missing file:")
    r = process_data_file("nonexistent_abc.txt")
    assert r is None
    print()

    # Case 3: file contains a non-numeric line — ValueError branch
    fd, path_bad = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w") as f:
        f.write("10\nten\n30\n")
    print("Case 3 — non-numeric data:")
    r = process_data_file(path_bad)
    assert r is None
    os.remove(path_bad)
    print()


# ============================================================
# === Solution 5: Custom Exception Hierarchy ===
# ============================================================
# Key ideas:
#   • Subclassing makes the hierarchy catchable at multiple levels.
#   • A caller who cares about the specific failure catches
#     EmptyFieldError or InvalidFormatError directly.
#   • A caller who only needs "something validation-related went
#     wrong" catches the base ValidationError.
#   • A compiled regex is defined once at module level to avoid
#     recompiling on every call.

_EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
)


class ValidationError(Exception):
    """Base class for all field-validation errors in this application."""


class EmptyFieldError(ValidationError):
    """Raised when a required field is None, empty, or whitespace-only."""


class InvalidFormatError(ValidationError):
    """Raised when a field value does not match the expected format."""


def validate_email(email):
    """Validate an email address, raising the appropriate subclass on failure.

    Raises:
        EmptyFieldError:    email is None or blank.
        InvalidFormatError: email does not match a basic user@domain.tld pattern.

    Returns True for a well-formed address.
    """
    if not email or not str(email).strip():
        raise EmptyFieldError("Email address cannot be empty.")
    if not _EMAIL_PATTERN.match(str(email).strip()):
        raise InvalidFormatError(
            f"'{email}' does not look like a valid email address."
        )
    return True


def demo_exercise_5():
    print("=== Exercise 5: Custom Exception Hierarchy ===")

    test_inputs = [
        ("alice@example.com", "valid"),
        ("",                  "empty string → EmptyFieldError"),
        (None,                "None        → EmptyFieldError"),
        ("not-an-email",      "no @-sign   → InvalidFormatError"),
        ("user@nodot",        "no TLD      → InvalidFormatError"),
    ]
    for email, desc in test_inputs:
        try:
            result = validate_email(email)
            print(f"  ✓ {desc:<35} → {result}")
        except EmptyFieldError as e:
            print(f"  EmptyFieldError    [{desc}]: {e}")
        except InvalidFormatError as e:
            print(f"  InvalidFormatError [{desc}]: {e}")

    # Catching at base ValidationError level catches all subclasses
    print("\nCatching at ValidationError (catches both subclasses):")
    for email in ("", "bad-format"):
        try:
            validate_email(email)
        except ValidationError as e:
            print(f"  ValidationError caught for {email!r}: "
                  f"{type(e).__name__} — {e}")

    # Catching at Exception level catches everything
    print("\nCatching at Exception (catches all exceptions):")
    try:
        validate_email(None)
    except Exception as e:
        print(f"  Exception caught: {type(e).__name__} — {e}")
    print()


# ============================================================
# === Solution 6: Context Manager for Timing ===
# ============================================================
# Key ideas:
#   Class-based: __enter__ records the start time and returns
#   self so `as t` gives access to the elapsed attribute.
#   __exit__ calculates elapsed time; returning False lets any
#   exception propagate normally (we do not suppress errors).
#
#   Generator-based: the yield point is the body of the with
#   block.  A mutable dict is yielded so the caller can read
#   elapsed after the block finishes.  time values are captured
#   in the finally clause so they always run.

class Timer:
    """Class-based context manager that measures elapsed wall-clock time.

    Usage:
        with Timer() as t:
            do_work()
        print(f"Elapsed: {t.elapsed:.4f}s")

    Uses time.perf_counter for the highest-resolution timer available.
    """

    def __enter__(self):
        self._start  = time.perf_counter()
        self.elapsed = 0.0
        return self                  # 'as t' binds to this instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self._start
        return False                 # do not suppress exceptions


@contextlib.contextmanager
def timer():
    """Generator-based context manager equivalent to Timer.

    Yields a mutable dict {'elapsed': 0.0}; the elapsed key is updated
    with the wall-clock time after the with block finishes.

    Usage:
        with timer() as t:
            do_work()
        print(f"Elapsed: {t['elapsed']:.4f}s")
    """
    info  = {"elapsed": 0.0}
    start = time.perf_counter()
    try:
        yield info
    finally:
        info["elapsed"] = time.perf_counter() - start


def demo_exercise_6():
    print("=== Exercise 6: Context Manager for Timing ===")
    N = 100_000

    # Class-based Timer
    with Timer() as t_class:
        total1 = sum(i * i for i in range(N))
    print(f"Timer class          : {t_class.elapsed:.6f}s  (sum={total1})")

    # @contextlib.contextmanager version
    with timer() as t_gen:
        total2 = sum(i * i for i in range(N))
    print(f"@contextmanager timer: {t_gen['elapsed']:.6f}s  (sum={total2})")

    assert total1 == total2, "Both loops should produce the same sum"

    # Compare timings — both should be within the same order of magnitude
    class_ms = t_class.elapsed * 1000
    gen_ms   = t_gen["elapsed"] * 1000
    print(f"Class-based: {class_ms:.2f}ms  |  generator: {gen_ms:.2f}ms  "
          f"(results identical: {total1 == total2})")
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
    print("All intermediate solutions completed successfully.")
