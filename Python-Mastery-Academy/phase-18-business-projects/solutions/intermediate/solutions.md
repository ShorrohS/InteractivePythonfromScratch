# ✅ Phase 18 — Intermediate Solutions

> These solutions use production patterns: chainable APIs, decorators, abstract base classes,
> and structured error responses. Study the design decisions in the comments — the why matters
> as much as the what.

---

## Solution Q1 — Reusable DataValidator Class

```python
"""
data_validator.py — Chainable validation pipeline for business data.

Design notes:
  - FieldValidator accumulates its own errors; DataValidator is the coordinator.
  - FieldValidator holds a back-reference to DataValidator so .field() can be called
    from within a chain, enabling the fluent API: validator.field("x").required().field("y")...
  - Compile regex patterns once at call time, not on every validation.
"""

import re
from typing import Any


class ValidationError(Exception):
    """Raised by validate_or_raise() when validation fails."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__(f"Validation failed with {len(errors)} error(s): {errors}")


class FieldValidator:
    """Accumulates validation errors for a single field. Methods return self for chaining."""

    def __init__(self, field_name: str, value: Any, parent: "DataValidator") -> None:
        self._field = field_name
        self._value = value
        self._errors: list[str] = []
        self._parent = parent  # back-reference enables .field() calls mid-chain

    # --- Rule methods (each returns self for chaining) ---

    def required(self) -> "FieldValidator":
        if self._value is None or (isinstance(self._value, str) and not self._value.strip()):
            self._errors.append(f"{self._field}: is required")
        return self

    def min_length(self, n: int) -> "FieldValidator":
        if self._value is not None and len(str(self._value)) < n:
            self._errors.append(f"{self._field}: must be at least {n} characters")
        return self

    def max_length(self, n: int) -> "FieldValidator":
        if self._value is not None and len(str(self._value)) > n:
            self._errors.append(f"{self._field}: must be at most {n} characters")
        return self

    def regex(self, pattern: str, message: str = "") -> "FieldValidator":
        if self._value is not None and not re.match(pattern, str(self._value)):
            msg = message or f"{self._field}: does not match required pattern"
            self._errors.append(msg)
        return self

    def range(self, min_val: float, max_val: float) -> "FieldValidator":
        if self._value is not None:
            try:
                val = float(self._value)
                if not (min_val <= val <= max_val):
                    self._errors.append(
                        f"{self._field}: must be between {min_val} and {max_val}"
                    )
            except (TypeError, ValueError):
                self._errors.append(f"{self._field}: must be a number")
        return self

    def one_of(self, choices: list) -> "FieldValidator":
        if self._value not in choices:
            self._errors.append(f"{self._field}: must be one of {choices}")
        return self

    # --- Navigate back to the parent to start a new field ---

    def field(self, name: str) -> "FieldValidator":
        """Start validating another field (delegates to parent DataValidator)."""
        return self._parent.field(name)

    def validate(self) -> list[str]:
        """Convenience: finalize all fields and return errors from the parent."""
        return self._parent.validate()

    def validate_or_raise(self) -> None:
        """Convenience: finalize and raise ValidationError if errors exist."""
        return self._parent.validate_or_raise()

    @property
    def errors(self) -> list[str]:
        return self._errors


class DataValidator:
    """Coordinates validation of multiple fields and collects all errors."""

    def __init__(self, data: dict) -> None:
        self._data = data
        self._field_validators: list[FieldValidator] = []

    def field(self, name: str) -> FieldValidator:
        """Start validating a named field. Returns a FieldValidator for rule chaining."""
        fv = FieldValidator(name, self._data.get(name), parent=self)
        self._field_validators.append(fv)
        return fv

    def validate(self) -> list[str]:
        """Collect and return all errors from every field validator."""
        all_errors: list[str] = []
        for fv in self._field_validators:
            all_errors.extend(fv.errors)
        return all_errors

    def validate_or_raise(self) -> None:
        """Raise ValidationError if any field has errors."""
        errors = self.validate()
        if errors:
            raise ValidationError(errors)


# --- Demo ---
if __name__ == "__main__":
    data = {"username": "AL", "age": 17, "role": "owner"}

    errors = (
        DataValidator(data)
        .field("username")
            .required()
            .min_length(3)
            .max_length(20)
            .regex(r"^[a-z0-9_]+$", "username: only lowercase letters, digits, and underscores")
        .field("age")
            .required()
            .range(18, 120)
        .field("role")
            .required()
            .one_of(["admin", "editor", "viewer"])
        .validate()
    )

    for e in errors:
        print(f"  - {e}")
```

---

## Solution Q2 — Retry Decorator with Exponential Backoff

```python
"""
retry_decorator.py — Decorator for retrying unreliable operations with exponential backoff.

Design notes:
  - The delay doubles after each failure: delay, delay*backoff, delay*backoff^2, ...
  - Only exception types listed in `exceptions` are retried; others propagate immediately.
  - functools.wraps preserves the original function's __name__ and __doc__ so introspection
    tools (help(), tracebacks) show the real function name, not 'wrapper'.
"""

import time
import logging
import functools
from typing import Callable, Type

logger = logging.getLogger(__name__)


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    """Retry decorator with exponential backoff.

    Args:
        max_attempts: Total number of tries (including the first attempt).
        delay:        Seconds to wait before the second attempt.
        backoff:      Multiplier applied to delay after each failure.
        exceptions:   Tuple of exception types that trigger a retry.

    Usage:
        @retry(max_attempts=4, delay=0.5, backoff=2.0, exceptions=(ConnectionError,))
        def unreliable_api_call(): ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception: Exception | None = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    if attempt < max_attempts:
                        logger.warning(
                            "Attempt %d/%d failed for %s: %s. Retrying in %.1fs...",
                            attempt,
                            max_attempts,
                            func.__name__,
                            exc,
                            current_delay,
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            "All %d attempts failed for %s: %s",
                            max_attempts,
                            func.__name__,
                            exc,
                        )

            raise last_exception  # type: ignore[misc]

        return wrapper
    return decorator


# --- Demo ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s | %(message)s")

    call_count = 0

    @retry(max_attempts=3, delay=0.01, backoff=2.0, exceptions=(ValueError,))
    def flaky_operation() -> str:
        global call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("transient failure")
        return "success"

    result = flaky_operation()
    assert result == "success"
    assert call_count == 3
    print(f"Passed — succeeded on attempt {call_count}")
```

---

## Solution Q3 — Repository Pattern

```python
"""
repository.py — Abstract Repository base class and an in-memory concrete implementation.

Design notes:
  - Using ABC forces every subclass to implement all abstract methods at class definition time;
    missing a method raises TypeError immediately rather than at runtime.
  - InMemoryRepository uses a plain dict for O(1) get/delete by ID.
  - entity dicts are copied in add() and update() to prevent external mutation of stored data.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class Repository(ABC):
    """Abstract base repository defining the CRUD contract.

    Subclasses must implement every @abstractmethod or they cannot be instantiated.
    """

    @abstractmethod
    def add(self, entity: dict) -> dict:
        """Persist a new entity. Returns the entity with its 'id' field set."""

    @abstractmethod
    def get(self, entity_id: int) -> Optional[dict]:
        """Return entity by ID, or None if not found."""

    @abstractmethod
    def get_all(self) -> list[dict]:
        """Return all stored entities."""

    @abstractmethod
    def update(self, entity: dict) -> dict:
        """Update an existing entity (must have 'id' key). Returns the updated entity."""

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete by ID. Returns True if deleted, False if ID not found."""

    @abstractmethod
    def count(self) -> int:
        """Return the total number of stored entities."""


class InMemoryRepository(Repository):
    """Concrete in-memory implementation. Suitable for testing and prototyping."""

    def __init__(self) -> None:
        self._store: dict[int, dict] = {}
        self._next_id: int = 1

    def add(self, entity: dict) -> dict:
        entity = dict(entity)          # copy — never mutate the caller's dict
        entity["id"] = self._next_id
        self._store[self._next_id] = entity
        self._next_id += 1
        return entity

    def get(self, entity_id: int) -> Optional[dict]:
        stored = self._store.get(entity_id)
        return dict(stored) if stored is not None else None  # return a copy

    def get_all(self) -> list[dict]:
        return [dict(e) for e in self._store.values()]  # return copies

    def update(self, entity: dict) -> dict:
        entity = dict(entity)
        entity_id = entity.get("id")
        if entity_id not in self._store:
            raise KeyError(f"Entity with id={entity_id} does not exist")
        self._store[entity_id] = entity
        return entity

    def delete(self, entity_id: int) -> bool:
        if entity_id in self._store:
            del self._store[entity_id]
            return True
        return False

    def count(self) -> int:
        return len(self._store)


# --- Demo ---
if __name__ == "__main__":
    repo = InMemoryRepository()

    alice = repo.add({"name": "Alice", "role": "engineer"})
    bob   = repo.add({"name": "Bob",   "role": "manager"})
    print(f"Count: {repo.count()}")            # 2
    print(f"Alice: {repo.get(1)}")             # {'id': 1, 'name': 'Alice', ...}

    repo.update({"id": 1, "name": "Alice", "role": "senior engineer"})
    print(f"Updated: {repo.get(1)['role']}")   # senior engineer

    print(f"Delete 99: {repo.delete(99)}")     # False
    print(f"Delete 1:  {repo.delete(1)}")      # True
    print(f"Count: {repo.count()}")            # 1
```

---

## Solution Q4 — Audit Log System

```python
"""
audit_log.py — Append-only audit trail for write operations.

Design notes:
  - JSONL format (one JSON object per line) is easy to process with standard tools
    like jq, grep, and Python's json.loads().
  - The @audited decorator defaults to "system" if no current_user attribute exists.
  - File is opened in append mode per record — this is intentionally simple and safe;
    production systems would use a proper log aggregator.
"""

import json
import logging
import datetime
import functools
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)

DEFAULT_LOG_FILE = Path("audit.log")


class AuditLog:
    """Records every write operation with who, what, and when.

    Data is written to a JSONL file (append-only) and kept in memory for queries.
    """

    def __init__(self, log_file: Path = DEFAULT_LOG_FILE) -> None:
        self._log_file = log_file
        self._history: list[dict] = []

    def record(
        self,
        user: str,
        action: str,
        resource: str,
        details: Any = None,
    ) -> None:
        """Record an audit event immediately to disk and in-memory history."""
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "user":      user,
            "action":    action,
            "resource":  resource,
            "details":   details,
        }
        self._history.append(entry)

        # Append to JSONL file — one JSON object per line
        with self._log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        logger.info("AUDIT | %s | %s | %s", user, action, resource)

    # --- Query methods ---

    def get_history(self) -> list[dict]:
        """Return all audit entries recorded this session."""
        return list(self._history)

    def get_by_user(self, user: str) -> list[dict]:
        return [e for e in self._history if e["user"] == user]

    def get_by_resource(self, resource: str) -> list[dict]:
        return [e for e in self._history if e["resource"] == resource]


def audited(audit_log: AuditLog, resource: str, action: str) -> Callable:
    """Decorator that records an audit entry when the decorated function is called.

    The decorated function may optionally accept a 'current_user' keyword argument;
    if absent, 'system' is used as the user.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("current_user", "system")
            audit_log.record(user=user, action=action, resource=resource)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# --- Demo ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s | %(message)s")

    log = AuditLog(Path("audit_demo.log"))

    log.record("alice", "CREATE", "invoice", {"invoice_id": 42, "amount": 1500})
    log.record("bob",   "DELETE", "employee", {"id": 7})
    log.record("alice", "UPDATE", "invoice", {"invoice_id": 42, "new_amount": 1800})

    print(f"Total entries:  {len(log.get_history())}")
    print(f"Alice's actions: {[e['action'] for e in log.get_by_user('alice')]}")
    print(f"Invoice events: {len(log.get_by_resource('invoice'))}")
```

---

## Solution Q5 — Sales Report Generator

```python
"""
report_generator.py — Transform raw sales records into CSV, JSON, and console reports.

Design notes:
  - Grouping functions are pure (take data, return data) — no file I/O mixed in.
  - The CSV and JSON writers are the only place file handles are opened.
  - Amounts are stored as floats throughout; format with :,.2f only at output time.
"""

import csv
import json
from pathlib import Path

SAMPLE_SALES = [
    {"date": "2024-01-10", "rep": "Alice", "category": "Software", "amount": 1500.00},
    {"date": "2024-01-20", "rep": "Bob",   "category": "Hardware", "amount": 3200.00},
    {"date": "2024-02-05", "rep": "Alice", "category": "Hardware", "amount": 2800.00},
    {"date": "2024-02-14", "rep": "Carol", "category": "Software", "amount":  950.00},
    {"date": "2024-03-01", "rep": "Bob",   "category": "Services", "amount": 4100.00},
    {"date": "2024-03-18", "rep": "Carol", "category": "Software", "amount": 1750.00},
]


def group_by_month_category(sales: list[dict]) -> dict[str, dict[str, float]]:
    """Return {month: {category: total}}."""
    result: dict[str, dict[str, float]] = {}
    for sale in sales:
        month = sale["date"][:7]  # YYYY-MM
        cat   = sale["category"]
        result.setdefault(month, {}).setdefault(cat, 0.0)
        result[month][cat] += sale["amount"]
    return result


def group_by_rep(sales: list[dict]) -> dict[str, float]:
    """Return {rep_name: total} sorted highest to lowest."""
    totals: dict[str, float] = {}
    for sale in sales:
        totals[sale["rep"]] = totals.get(sale["rep"], 0.0) + sale["amount"]
    return dict(sorted(totals.items(), key=lambda x: -x[1]))


def generate_csv_report(sales: list[dict], output_path: Path) -> None:
    """Write a flat month/category/total CSV report."""
    grouped = group_by_month_category(sales)
    rows = [
        {"month": month, "category": cat, "total": total}
        for month in sorted(grouped)
        for cat, total in sorted(grouped[month].items())
    ]
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["month", "category", "total"])
        writer.writeheader()
        writer.writerows(rows)


def generate_json_report(sales: list[dict], output_path: Path) -> None:
    """Write a nested month→category→total JSON report."""
    grouped = group_by_month_category(sales)
    output_path.write_text(json.dumps(grouped, indent=2), encoding="utf-8")


def print_console_summary(sales: list[dict]) -> None:
    grouped = group_by_month_category(sales)
    grand_total = 0.0

    print(f"{'Month':<10} {'Category':<15} {'Total':>12}")
    print("-" * 40)

    for month in sorted(grouped):
        for cat, total in sorted(grouped[month].items()):
            print(f"{month:<10} {cat:<15} ${total:>10,.2f}")
            grand_total += total

    print("-" * 40)
    print(f"{'Grand Total':<26} ${grand_total:>10,.2f}")


# --- Demo ---
if __name__ == "__main__":
    generate_csv_report(SAMPLE_SALES, Path("sales_report.csv"))
    generate_json_report(SAMPLE_SALES, Path("sales_report.json"))
    print_console_summary(SAMPLE_SALES)
    print("\nBy rep:")
    for rep, total in group_by_rep(SAMPLE_SALES).items():
        print(f"  {rep:<10} ${total:,.2f}")
```

---

## Solution Q6 — Config Manager with File + Environment Override

```python
"""
config_manager.py — Load config from a JSON file with environment variable overrides.

Design notes:
  - Precedence: env vars > file values > schema defaults.
  - Type coercion happens after merging — only one place to maintain.
  - Errors are collected before raising so all problems appear in one message.
"""

import os
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_TYPE_COERCERS = {
    "str":   str,
    "int":   int,
    "float": float,
    "bool":  lambda raw: raw.lower() == "true" if isinstance(raw, str) else bool(raw),
}


class ConfigManager:
    """Load and validate config from a JSON file, overridden by environment variables.

    Args:
        config_file: Path to a JSON file containing config key-value pairs.
        schema:      Dict mapping config key names to their spec dicts:
                       {"type": "str"|"int"|"float"|"bool",
                        "required": bool,         # default True
                        "default": <value>}        # only for required=False
    """

    def __init__(self, config_file: Path, schema: dict[str, dict]) -> None:
        self._file = config_file
        self._schema = schema
        self._config: dict[str, Any] = {}

    def load(self) -> dict[str, Any]:
        """Merge file config and env vars, coerce types, validate required fields."""
        # Step 1: load from file (silently skip if file absent)
        file_config: dict = {}
        if self._file.exists():
            try:
                file_config = json.loads(self._file.read_text(encoding="utf-8"))
                logger.debug("Loaded config from %s", self._file)
            except json.JSONDecodeError as exc:
                logger.warning("Cannot parse config file %s: %s", self._file, exc)

        errors: list[str] = []
        result: dict[str, Any] = {}

        for key, spec in self._schema.items():
            env_key = key.upper()

            # Step 2: determine raw value and its source
            if env_key in os.environ:
                raw = os.environ[env_key]
                source = "env"
            elif key in file_config:
                raw = file_config[key]
                source = "file"
            elif "default" in spec:
                raw = spec["default"]
                source = "default"
            elif spec.get("required", True):
                errors.append(f"Missing required config key: '{key}'")
                continue
            else:
                continue

            # Step 3: coerce type
            coerce = _TYPE_COERCERS.get(spec.get("type", "str"), str)
            try:
                result[key] = coerce(raw) if isinstance(raw, str) else raw
                logger.debug("Config '%s'=%r  (from %s)", key, result[key], source)
            except (ValueError, TypeError) as exc:
                errors.append(f"Config '{key}': cannot coerce {raw!r} to {spec.get('type')} — {exc}")

        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(f"  • {e}" for e in errors))

        self._config = result
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Return a single config value after load()."""
        return self._config.get(key, default)


# --- Demo ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s | %(message)s")
    import json, tempfile, os

    # Write a temporary config file
    cfg = {"db_host": "localhost", "db_port": 5432, "db_name": "mydb"}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(cfg, f)
        cfg_path = Path(f.name)

    # Env var overrides the file value
    os.environ["DB_PORT"] = "9999"

    manager = ConfigManager(
        config_file=cfg_path,
        schema={
            "db_host":     {"type": "str",  "required": True},
            "db_port":     {"type": "int",  "required": True},
            "db_name":     {"type": "str",  "required": True},
            "debug":       {"type": "bool", "required": False, "default": False},
            "max_retries": {"type": "int",  "required": False, "default": 3},
        },
    )
    config = manager.load()
    print(config)  # db_port should be 9999 (int), debug=False, max_retries=3
    cfg_path.unlink()  # clean up temp file
```

---

## Solution Q7 — Error Handler Decorator

```python
"""
error_handler.py — Decorator for structured error responses in business functions.

Design notes:
  - Returning {"success": False, ...} instead of propagating exceptions lets callers
    handle errors without try/except everywhere — common in service layer code.
  - The log level is configurable: use 'warning' for expected business errors
    (e.g. record not found), 'error' for unexpected failures.
  - Exception types NOT in the catch list are allowed to propagate — the decorator
    should not swallow programming errors like AttributeError or TypeError.
"""

import logging
import functools
from typing import Any, Callable, Type

logger = logging.getLogger(__name__)


def handle_errors(
    *exception_types: Type[Exception],
    log_level: str = "error",
) -> Callable:
    """Catch specific exceptions, log them, and return a structured dict.

    On success:  {"success": True,  "data": <return_value>}
    On failure:  {"success": False, "error": "<message>", "error_type": "<ClassName>"}

    Args:
        *exception_types: One or more exception types to catch.
        log_level:        "warning", "error", or any valid logging level name.

    Usage:
        @handle_errors(ValueError, FileNotFoundError, log_level="warning")
        def load_config(path: str) -> dict: ...
    """
    # Default to catching all exceptions if none specified
    catch = exception_types if exception_types else (Exception,)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> dict[str, Any]:
            try:
                result = func(*args, **kwargs)
                return {"success": True, "data": result}
            except catch as exc:
                log_fn = getattr(logger, log_level.lower(), logger.error)
                log_fn(
                    "Error in %s(): [%s] %s",
                    func.__name__,
                    type(exc).__name__,
                    exc,
                )
                return {
                    "success":    False,
                    "error":      str(exc),
                    "error_type": type(exc).__name__,
                }
        return wrapper
    return decorator


# --- Demo ---
if __name__ == "__main__":
    import json
    from pathlib import Path

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s | %(message)s")

    @handle_errors(FileNotFoundError, json.JSONDecodeError, log_level="warning")
    def load_config(path: str) -> dict:
        return json.loads(Path(path).read_text())

    # File does not exist:
    print(load_config("missing.json"))
    # {"success": False, "error": "...", "error_type": "FileNotFoundError"}

    # Success — write a temp file first
    Path("tmp_cfg.json").write_text('{"db": "mydb"}')
    print(load_config("tmp_cfg.json"))
    # {"success": True, "data": {"db": "mydb"}}
    Path("tmp_cfg.json").unlink()
```

---

> **Exercises:** → [../../exercises/intermediate/exercises.md](../../exercises/intermediate/exercises.md)
