# Phase 06 — Intermediate Exercises: Error Handling

**Difficulty:** ⭐⭐ Intermediate

---

**Q1. Graceful File Reader**

Write a function `read_file_safe(filepath)` that:
- Returns the full file contents as a string if the file exists and is readable
- Returns `None` (without raising or crashing) if anything goes wrong

Test it with:
1. A real temporary file created with `tempfile.NamedTemporaryFile` or `tempfile.mkstemp`
2. A path that does not exist (e.g. `"ghost_file.txt"`)
3. Confirm that `None` is returned gracefully for the missing path

Hint: `OSError` is the parent class of `FileNotFoundError` and `PermissionError` — one handler covers all I/O failures.

---

**Q2. Validated Age Input Loop**

Write two functions that separate validation logic from I/O:

`validate_age(value_str)` — pure validation, no `input()`:
- Parses `value_str` as an integer (handle `ValueError`)
- Checks that the result is in range 1–120 (inclusive)
- Returns `(age_int, None)` on success
- Returns `(None, error_message)` on failure

`get_valid_age()` — interactive loop:
- Calls `input()` in a loop, passing the result to `validate_age`
- Prints the error message and re-prompts on failure
- Returns the valid integer once the user enters one

Test `validate_age` directly with: `"25"`, `"abc"`, `"0"`, `"200"`, `"  42  "`.

---

**Q3. Safe Type Converter**

Write `safe_convert(value, target_type, default=None)` that:
- Attempts `target_type(value)` and returns the result on success
- Returns `default` if conversion raises `ValueError` or `TypeError`
- Handles `bool` as a special case — `bool("False")` is `True` in Python because
  any non-empty string is truthy. Instead, map strings by comparison:
  `"true"/"1"/"yes"` → `True` and `"false"/"0"/"no"` → `False`

Test with:
```python
safe_convert("42",    int)             # → 42
safe_convert("3.14",  float)           # → 3.14
safe_convert("hello", int, default=0)  # → 0
safe_convert("true",  bool)            # → True
safe_convert("False", bool)            # → False
safe_convert(None,    float, -1.0)     # → -1.0
```

---

**Q4. try / except / else / finally — All Four Clauses**

Write `process_data_file(filepath)` that opens a file, reads lines, converts each to `float`, and sums them. Each clause must play a meaningful role:

- `try` — open the file and convert the data (the risky part)
- `except FileNotFoundError` — handle a missing file
- `except ValueError` — handle a line that is not numeric
- `else` — runs **only** when try completed without exception; print results here
- `finally` — runs **always**; log a one-line "finished processing" message here

Returns the sum on success or `None` on error.

Demonstrate by calling it with:
1. A valid temp file containing three numeric lines
2. A non-existent filepath
3. A temp file that includes a non-numeric line (e.g. `"ten"`)

---

**Q5. Custom Exception Hierarchy**

Define a three-level exception hierarchy:

```
Exception
  └─ ValidationError        ← base class for all validation errors
       ├─ EmptyFieldError    ← field is blank or None
       └─ InvalidFormatError ← field value has an unacceptable format
```

Write `validate_email(email)` that:
- Raises `EmptyFieldError` if `email` is `None` or empty/whitespace
- Raises `InvalidFormatError` if `email` does not match a basic `user@domain.tld` pattern
- Returns `True` for a well-formed address

Demonstrate three different catching strategies using the same bad inputs:
1. Catch `InvalidFormatError` specifically (most specific)
2. Catch the base `ValidationError` (catches all subclasses)
3. Catch `Exception` (catches everything)

---

**Q6. Context Manager for Timing**

Implement a `Timer` class usable as a context manager:

```python
with Timer() as t:
    # ... work to time ...
print(f"Elapsed: {t.elapsed:.4f}s")
```

Requirements:
- Implement `__enter__` and `__exit__`
- `__enter__` records the start time and returns `self` (so `as t` works)
- `__exit__` records the elapsed time in `t.elapsed`; does **not** suppress exceptions

Then implement the same behaviour as a generator-based context manager using `@contextlib.contextmanager`.

Finally, benchmark a loop that sums 100 000 squared values using both versions and confirm both report approximately the same elapsed time.

---

> **Solutions:** `../../solutions/intermediate/solutions.py`
