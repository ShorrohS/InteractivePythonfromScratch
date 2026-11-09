# ✅ Phase 18 — Beginner Solutions

> Read each exercise fully and attempt it before looking here.
> Each solution demonstrates production patterns: proper error handling, logging,
> no bare excepts, and type hints throughout.

---

## Solution Q1 — Structured Application Logger

```python
"""
app_logger.py — Reusable logger factory for production applications.

Design notes:
  - The logger's own level is set to DEBUG so nothing is filtered at source.
  - Each handler applies its own level filter independently.
  - RotatingFileHandler prevents runaway log files on long-running services.
"""

import logging
import logging.handlers
from pathlib import Path


LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str, log_file: str = "app.log") -> logging.Logger:
    """Create and return a fully configured logger.

    Args:
        name:     Logger name — use __name__ in production modules.
        log_file: Path to the rotating log file.

    Returns:
        A logger with a console handler (WARNING+) and a
        rotating file handler (DEBUG+, 5 KB max, 3 backups).
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers if get_logger is called twice with the same name
    if logger.handlers:
        return logger

    # Root level must be DEBUG so handlers can see all messages
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # --- Console handler: WARNING and above only ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # --- Rotating file handler: all levels ---
    # maxBytes=5120 → rotate at 5 KB; backupCount=3 → keep app.log.1, .2, .3
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5120,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# --- Demo / test ---
if __name__ == "__main__":
    log = get_logger("sales_app")

    log.debug("Loading config file")                                    # file only
    log.info("Application started — env: production")                  # file only
    log.warning("Config value missing, using default: MAX_RETRIES=3")  # console + file
    log.error("Failed to connect to database at localhost:5432")        # console + file
    log.critical("Data corruption detected — initiating emergency shutdown")  # console + file

    print(f"\nLog written to: {Path('app.log').resolve()}")
```

**Why it works:**
- Setting the logger level to `DEBUG` lets the logger pass every message to its handlers.
- Each handler then applies its own level filter — the console only shows WARNING and above.
- The `if logger.handlers` guard prevents duplicate output if `get_logger` is called twice in
  the same process (common when modules import from each other).

---

## Solution Q2 — Environment Configuration Loader

```python
"""
config.py — Load and validate application config from environment variables.

Design notes:
  - Collect ALL validation errors before raising so operators see every problem at once.
  - In a real app, call python-dotenv's load_dotenv() before load_config() to
    populate os.environ from a .env file.  This module uses only stdlib.
"""

import os
from typing import Any

REQUIRED_VARS = ["DB_HOST", "DB_PORT", "DB_NAME", "APP_ENV", "LOG_LEVEL"]
VALID_APP_ENVS = {"development", "staging", "production"}
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}


def load_config() -> dict[str, Any]:
    """Read config from os.environ, validate, and return a typed dict.

    Returns:
        dict with lowercase keys and coerced types.

    Raises:
        ValueError: if any required variable is missing or has an invalid value.
    """
    errors: list[str] = []

    # Phase 1 — check all required vars are present
    missing = [v for v in REQUIRED_VARS if not os.environ.get(v)]
    if missing:
        raise ValueError(f"Missing required configuration variables: {', '.join(missing)}")

    # Phase 2 — type coercion and value validation
    try:
        db_port = int(os.environ["DB_PORT"])
    except ValueError:
        errors.append(f"DB_PORT must be an integer, got: {os.environ['DB_PORT']!r}")
        db_port = 0  # placeholder so we can continue collecting errors

    app_env = os.environ["APP_ENV"]
    if app_env not in VALID_APP_ENVS:
        errors.append(
            f"APP_ENV must be one of {', '.join(sorted(VALID_APP_ENVS))} — got: {app_env!r}"
        )

    log_level = os.environ["LOG_LEVEL"]
    if log_level not in VALID_LOG_LEVELS:
        errors.append(
            f"LOG_LEVEL must be one of {', '.join(sorted(VALID_LOG_LEVELS))} — got: {log_level!r}"
        )

    if errors:
        raise ValueError("\n".join(errors))

    # Phase 3 — build the config dict with optional defaults
    try:
        max_retries = int(os.environ.get("MAX_RETRIES", "3"))
    except ValueError:
        max_retries = 3  # fall back to default if env var is malformed

    try:
        timeout_sec = int(os.environ.get("TIMEOUT_SEC", "30"))
    except ValueError:
        timeout_sec = 30

    return {
        "db_host":     os.environ["DB_HOST"],
        "db_port":     db_port,
        "db_name":     os.environ["DB_NAME"],
        "app_env":     app_env,
        "log_level":   log_level,
        "max_retries": max_retries,
        "timeout_sec": timeout_sec,
    }


# --- Demo / test ---
if __name__ == "__main__":
    import os

    # Simulate .env values
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_PORT"] = "5432"
    os.environ["DB_NAME"] = "sales_db"
    os.environ["APP_ENV"] = "development"
    os.environ["LOG_LEVEL"] = "INFO"

    config = load_config()
    for key, value in config.items():
        print(f"  {key:<15} = {value!r}  ({type(value).__name__})")
```

**Why it works:**
- The two-phase approach (check presence, then validate values) gives clean, actionable error messages.
- Collecting all errors before raising means operators fix everything in one deploy cycle.
- Defaulting malformed optional vars rather than crashing is a deliberate trade-off — optional means optional.

---

## Solution Q3 — CSV Data Cleaner

```python
"""
csv_cleaner.py — Read a messy employee CSV, apply cleaning rules, write a clean version.

Design notes:
  - DictReader and DictWriter keep column handling readable and order-independent.
  - Each cleaning rule is a separate guard clause — easy to add/remove rules later.
  - The summary is printed to stdout; errors go to stderr to keep them separable.
"""

import csv
import sys
from pathlib import Path

INPUT_FILE = Path("employees_raw.csv")
OUTPUT_FILE = Path("employees_clean.csv")


def clean_row(row: dict) -> dict | None:
    """Apply cleaning rules to a single row.

    Returns the cleaned row dict, or None if the row should be skipped.
    """
    # Strip whitespace from every field first
    row = {k: v.strip() for k, v in row.items()}

    # Rule 1: ID must exist and be a whole number
    if not row.get("id") or not row["id"].isdigit():
        return None

    # Rule 2 + 3: first_name must be present (last_name alone is not enough)
    if not row.get("first_name"):
        return None

    # Rule 4: Title-case name and department fields
    row["first_name"] = row["first_name"].title()
    row["last_name"]  = row["last_name"].title()
    row["department"] = row["department"].title()

    # Rule 5: Default missing salary to 0
    if not row.get("salary"):
        row["salary"] = "0"

    return row


def main() -> None:
    if not INPUT_FILE.exists():
        print(f"Error: input file not found: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)

    rows_read = 0
    rows_skipped = 0
    cleaned_rows: list[dict] = []

    with INPUT_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames  # capture before iteration

        for row in reader:
            rows_read += 1
            cleaned = clean_row(row)
            if cleaned is None:
                rows_skipped += 1
            else:
                cleaned_rows.append(cleaned)

    rows_written = len(cleaned_rows)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print("CSV Cleaner Summary")
    print("-" * 19)
    print(f"Rows read:    {rows_read}")
    print(f"Rows skipped: {rows_skipped}")
    print(f"Rows written: {rows_written}")
    print(f"\nOutput written to: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
```

**Why it works:**
- `DictReader` stores the header in `reader.fieldnames`; passing it to `DictWriter` preserves the
  original column order without hard-coding column names.
- The `clean_row` function returns `None` for skippable rows — this makes the main loop intent
  readable: "if clean is None, skip".
- Reading all rows into `cleaned_rows` first lets us write the output file in a single pass with
  the full count already known.

---

## Solution Q4 — JSON Expense Tracker

```python
"""
expense_tracker.py — Command-line expense tracker backed by a JSON file.

Design notes:
  - All persistence goes through load_expenses() / save_expenses() — never write JSON inline.
  - Input validation is separated from menu logic for testability.
  - IDs are never reused: next_id takes the current maximum and adds 1.
"""

import json
import datetime
import sys
from pathlib import Path

EXPENSE_FILE = Path("expenses.json")


def load_expenses() -> list[dict]:
    """Load expenses from JSON, returning an empty list on first run."""
    try:
        return json.loads(EXPENSE_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Warning: expense file is corrupt ({e}). Starting fresh.", file=sys.stderr)
        return []


def save_expenses(expenses: list[dict]) -> None:
    """Persist the expenses list to disk."""
    EXPENSE_FILE.write_text(json.dumps(expenses, indent=2), encoding="utf-8")


def next_id(expenses: list[dict]) -> int:
    """Return the next available ID (never reuses deleted IDs)."""
    return max((e["id"] for e in expenses), default=0) + 1


def validate_amount(amount_str: str) -> float:
    """Parse and validate a monetary amount string."""
    try:
        amount = float(amount_str)
    except ValueError:
        raise ValueError("Amount must be a number (e.g. 45.99)")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    return amount


def validate_date(date_str: str) -> str:
    """Validate that a string is a YYYY-MM-DD date."""
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format (e.g. 2024-01-15)")
    return date_str


def add_expense(expenses: list[dict]) -> None:
    date = input("  Date (YYYY-MM-DD): ").strip()
    try:
        validate_date(date)
    except ValueError as e:
        print(f"  Error: {e}")
        return

    description = input("  Description: ").strip()
    if not description:
        print("  Error: description cannot be empty")
        return

    amount_str = input("  Amount: ").strip()
    try:
        amount = validate_amount(amount_str)
    except ValueError as e:
        print(f"  Error: {e}")
        return

    category = input("  Category: ").strip().lower()
    if not category:
        print("  Error: category cannot be empty")
        return

    expense = {
        "id": next_id(expenses),
        "date": date,
        "description": description,
        "amount": round(amount, 2),
        "category": category,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"  ✓ Added expense #{expense['id']}")


def list_expenses(expenses: list[dict], category: str | None = None) -> None:
    filtered = expenses if category is None else [
        e for e in expenses if e["category"] == category.lower()
    ]
    if not filtered:
        print("  No expenses found.")
        return

    print(f"\n  {'ID':<5} {'Date':<12} {'Description':<30} {'Category':<15} {'Amount':>10}")
    print(f"  {'-'*5} {'-'*12} {'-'*30} {'-'*15} {'-'*10}")
    for e in filtered:
        print(f"  {e['id']:<5} {e['date']:<12} {e['description']:<30} {e['category']:<15} ${e['amount']:>9.2f}")


def category_totals(expenses: list[dict]) -> None:
    totals: dict[str, float] = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0.0) + e["amount"]

    if not totals:
        print("  No expenses found.")
        return

    print("\n  Category Totals:")
    for cat, total in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"    {cat:<20} ${total:.2f}")


def delete_expense(expenses: list[dict]) -> None:
    id_str = input("  Expense ID to delete: ").strip()
    try:
        expense_id = int(id_str)
    except ValueError:
        print("  Error: ID must be a whole number")
        return

    original_len = len(expenses)
    expenses[:] = [e for e in expenses if e["id"] != expense_id]

    if len(expenses) < original_len:
        save_expenses(expenses)
        print(f"  ✓ Deleted expense #{expense_id}")
    else:
        print(f"  Error: no expense found with ID {expense_id}")


def main() -> None:
    expenses = load_expenses()

    while True:
        print("\n--- Expense Tracker ---")
        print("  1. Add expense")
        print("  2. List all expenses")
        print("  3. List by category")
        print("  4. Category totals")
        print("  5. Delete expense")
        print("  6. Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            cat = input("  Category filter: ").strip()
            list_expenses(expenses, cat)
        elif choice == "4":
            category_totals(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("  Invalid choice — enter 1–6")


if __name__ == "__main__":
    main()
```

**Why it works:**
- `expenses[:] = [...]` mutates the existing list in place — `del expenses[:]` followed by `expenses.extend(...)` would also work, but slice assignment is idiomatic Python.
- The `try/except json.JSONDecodeError` on load means a corrupt file doesn't crash the app on startup — it warns and starts fresh.
- Saving after every add/delete is slightly inefficient but safe — no risk of losing a transaction if the process is killed.

---

## Solution Q5 — Employee Data Validator

```python
"""
validator.py — Validate employee dict records before HR system import.

Design notes:
  - Returns a list of error messages instead of raising on the first error.
  - Check for bool before int: isinstance(True, int) is True in Python,
    so you must check the more specific type first.
  - The validator is a pure function (no side effects) — easy to test and reuse.
"""

import re
import datetime

VALID_DEPARTMENTS = {"Engineering", "Marketing", "Sales", "HR", "Finance"}
EMP_ID_PATTERN = re.compile(r"^EMP-\d{4}$")


def validate_employee(data: dict) -> list[str]:
    """Validate an employee record dict.

    Returns:
        List of error messages. Empty list means the record is valid.
    """
    errors: list[str] = []

    # employee_id
    emp_id = data.get("employee_id")
    if not emp_id:
        errors.append("employee_id: required field is missing")
    elif not EMP_ID_PATTERN.match(str(emp_id)):
        errors.append("employee_id: must match format EMP-DDDD (e.g. EMP-0042)")

    # first_name
    first = data.get("first_name")
    if not first:
        errors.append("first_name: required field is missing")
    elif not (2 <= len(str(first)) <= 50):
        errors.append("first_name: must be 2–50 characters")

    # last_name
    last = data.get("last_name")
    if not last:
        errors.append("last_name: required field is missing")
    elif not (2 <= len(str(last)) <= 50):
        errors.append("last_name: must be 2–50 characters")

    # email — basic structural check (not RFC-5321 full validation)
    email = data.get("email")
    if not email:
        errors.append("email: required field is missing")
    else:
        email_str = str(email)
        if "@" not in email_str or "." not in email_str.split("@")[-1]:
            errors.append("email: must be a valid email address")

    # department
    dept = data.get("department")
    if not dept:
        errors.append("department: required field is missing")
    elif dept not in VALID_DEPARTMENTS:
        errors.append(
            f"department: must be one of {', '.join(sorted(VALID_DEPARTMENTS))}"
        )

    # salary
    salary = data.get("salary")
    if salary is None:
        errors.append("salary: required field is missing")
    else:
        try:
            salary_val = float(salary)
            if not (20000 <= salary_val <= 500000):
                errors.append("salary: must be between 20000 and 500000")
        except (TypeError, ValueError):
            errors.append("salary: must be a number")

    # start_date
    start_date = data.get("start_date")
    if not start_date:
        errors.append("start_date: required field is missing")
    else:
        try:
            datetime.datetime.strptime(str(start_date), "%Y-%m-%d")
        except ValueError:
            errors.append("start_date: must be in YYYY-MM-DD format")

    # is_active — must be actual bool, not a truthy value like "yes" or 1
    is_active = data.get("is_active")
    if is_active is None:
        errors.append("is_active: required field is missing")
    elif not isinstance(is_active, bool):
        # Note: check bool before int — bool is a subclass of int in Python
        errors.append("is_active: must be a boolean (True or False)")

    return errors


# --- Demo / test ---
if __name__ == "__main__":
    valid = {
        "employee_id": "EMP-0042",
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@company.com",
        "department": "Engineering",
        "salary": 85000,
        "start_date": "2023-06-15",
        "is_active": True,
    }
    print("Valid record errors:", validate_employee(valid))  # []

    invalid = {
        "employee_id": "EMP42",
        "first_name": "A",
        "email": "not-an-email",
        "department": "IT",
        "salary": 15000,
        "start_date": "15-06-2023",
        "is_active": "yes",
    }
    print("\nInvalid record errors:")
    for err in validate_employee(invalid):
        print(f"  - {err}")
```

**Why it works:**
- Every field guard uses an early-exit pattern: check for missing first, then check format/value.
  This avoids calling `.match()` or `float()` on `None` which would raise a `TypeError`.
- The `isinstance(is_active, bool)` check catches strings like `"yes"` and integers like `1` that
  would otherwise slip through — a critical distinction for HR system imports.

---

> **Exercises:** → [../../exercises/beginner/exercises.md](../../exercises/beginner/exercises.md)
