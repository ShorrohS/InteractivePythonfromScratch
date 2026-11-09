# Phase 18 — Business Python Cheat Sheet

> Quick reference for production Python patterns. Keep this open while working through Phase 18 projects.

---

## 1. Logging Setup

### Basic configuration (simple scripts)
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
```

### FileHandler — write to file
```python
import logging

handler = logging.FileHandler("app.log", encoding="utf-8")
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
))

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)   # logger level must be <= handler level
logger.addHandler(handler)
```

### RotatingFileHandler — rotate at size limit
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=10 * 1024,   # 10 KB per file
    backupCount=3,        # keep app.log.1, .2, .3
    encoding="utf-8",
)
```

### Multiple handlers (console WARNING+, file DEBUG+)
```python
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")

console = logging.StreamHandler()
console.setLevel(logging.WARNING)
console.setFormatter(fmt)

file_h = RotatingFileHandler("app.log", maxBytes=5120, backupCount=3)
file_h.setLevel(logging.DEBUG)
file_h.setFormatter(fmt)

logger.addHandler(console)
logger.addHandler(file_h)
```

### Log level reference
| Level | When to use |
|-------|-------------|
| `DEBUG` | Detailed diagnostic info (config values, step-by-step flow) |
| `INFO` | Routine events (started, loaded N records, completed) |
| `WARNING` | Unexpected situation but recoverable (using default value) |
| `ERROR` | Operation failed but app continues (file not found, DB error) |
| `CRITICAL` | Severe failure — app cannot continue |

---

## 2. Configuration with Environment Variables

### Read env vars with defaults
```python
import os

db_host = os.environ.get("DB_HOST", "localhost")   # default if absent
db_port = int(os.environ.get("DB_PORT", "5432"))   # coerce to int
debug   = os.environ.get("DEBUG", "false").lower() == "true"
```

### Validate required variables
```python
REQUIRED = ["DB_HOST", "DB_PORT", "DB_NAME"]

missing = [k for k in REQUIRED if not os.environ.get(k)]
if missing:
    raise ValueError(f"Missing required config: {', '.join(missing)}")
```

### Use python-dotenv to load a .env file
```python
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()   # reads .env into os.environ — must be called BEFORE os.environ.get()

db_host = os.environ.get("DB_HOST")
```

### .env file format
```
# .env — never commit this file to git
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
APP_ENV=development
```

---

## 3. CSV Patterns

### Read CSV as list of dicts
```python
import csv

with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)   # materialise now so file can close

# rows = [{"name": "Alice", "salary": "75000"}, ...]
```

### Write CSV from list of dicts
```python
import csv

fieldnames = ["name", "department", "salary"]
rows = [{"name": "Alice", "department": "Engineering", "salary": 75000}]

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
```

### Common gotchas
```python
# ❌ Iterating DictReader twice — second pass is empty
reader = csv.DictReader(f)
count = sum(1 for _ in reader)    # exhausts reader
data  = list(reader)              # empty!

# ✅ Materialise to list first
rows  = list(csv.DictReader(f))
count = len(rows)
data  = rows
```

---

## 4. JSON Config Patterns

### Load JSON config file
```python
import json
from pathlib import Path

def load_config(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}        # return empty config if file absent
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file {path}: {e}") from e
```

### Save config dict (human-readable)
```python
def save_config(path: str, config: dict) -> None:
    Path(path).write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
```

### JSONL — one JSON object per line (for audit logs / event streams)
```python
# Write
with open("events.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(event) + "\n")

# Read all
with open("events.jsonl", encoding="utf-8") as f:
    events = [json.loads(line) for line in f if line.strip()]
```

---

## 5. Custom Business Exception Hierarchy

```python
class AppError(Exception):
    """Base class for all application errors."""

class ConfigError(AppError):
    """Raised for missing or invalid configuration."""

class ValidationError(AppError):
    """Raised when business data fails validation."""
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__(f"{len(errors)} validation error(s): {errors}")

class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

class PermissionError(AppError):
    """Raised when an operation is not allowed for the current user."""
```

**Usage:**
```python
try:
    record = repo.get(record_id)
    if record is None:
        raise NotFoundError(f"Record {record_id} not found")
except NotFoundError as e:
    logger.warning("%s", e)
    return {"success": False, "error": str(e)}
```

---

## 6. Validation Pattern — Collect All Errors

```python
def validate_employee(data: dict) -> list[str]:
    """Return a list of error messages. Empty list means valid."""
    errors = []

    if not data.get("name"):
        errors.append("name: required")
    elif len(data["name"]) < 2:
        errors.append("name: must be at least 2 characters")

    salary = data.get("salary")
    if salary is None:
        errors.append("salary: required")
    else:
        try:
            if float(salary) <= 0:
                errors.append("salary: must be positive")
        except (TypeError, ValueError):
            errors.append("salary: must be a number")

    return errors


# Caller pattern
errors = validate_employee(record)
if errors:
    raise ValidationError(errors)
```

---

## 7. Retry Decorator Template

```python
import time
import functools
import logging
from typing import Callable, Type

logger = logging.getLogger(__name__)

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt < max_attempts:
                        logger.warning("Attempt %d/%d for %s failed: %s. Retry in %.1fs",
                                       attempt, max_attempts, func.__name__, e, wait)
                        time.sleep(wait)
                        wait *= backoff
                    else:
                        logger.error("All %d attempts failed for %s: %s",
                                     max_attempts, func.__name__, e)
                        raise
        return wrapper
    return decorator

# Usage:
@retry(max_attempts=4, delay=0.5, exceptions=(ConnectionError, TimeoutError))
def call_api(url: str) -> dict: ...
```

---

## 8. Repository Pattern Base Class Template

```python
from abc import ABC, abstractmethod
from typing import Optional

class Repository(ABC):
    @abstractmethod
    def add(self, entity: dict) -> dict:
        """Add entity; return it with 'id' assigned."""

    @abstractmethod
    def get(self, entity_id: int) -> Optional[dict]:
        """Return entity or None."""

    @abstractmethod
    def get_all(self) -> list[dict]:
        """Return all entities."""

    @abstractmethod
    def update(self, entity: dict) -> dict:
        """Update entity (must have 'id'). Raise KeyError if not found."""

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete by id. Return True if deleted, False if not found."""

    @abstractmethod
    def count(self) -> int: ...


class InMemoryRepository(Repository):
    def __init__(self):
        self._store: dict[int, dict] = {}
        self._next_id = 1

    def add(self, entity):
        e = dict(entity); e["id"] = self._next_id
        self._store[self._next_id] = e; self._next_id += 1
        return e

    def get(self, entity_id):
        r = self._store.get(entity_id); return dict(r) if r else None

    def get_all(self):        return [dict(e) for e in self._store.values()]
    def update(self, entity):
        e = dict(entity)
        if e["id"] not in self._store: raise KeyError(e["id"])
        self._store[e["id"]] = e; return e

    def delete(self, entity_id):
        if entity_id in self._store: del self._store[entity_id]; return True
        return False

    def count(self):           return len(self._store)
```

---

## 9. Structured Error Response Pattern

```python
from typing import Any

def ok(data: Any) -> dict:
    return {"success": True, "data": data}

def err(message: str, error_type: str = "Error") -> dict:
    return {"success": False, "error": message, "error_type": error_type}

# Usage in a service function:
def get_invoice(invoice_id: int) -> dict:
    invoice = repo.get(invoice_id)
    if invoice is None:
        return err(f"Invoice {invoice_id} not found", "NotFoundError")
    return ok(invoice)

# Caller:
result = get_invoice(42)
if result["success"]:
    print(result["data"])
else:
    print(f"Error: {result['error']}")
```

---

## 10. pathlib Patterns

```python
from pathlib import Path

# Build paths safely (handles / vs \ automatically)
base = Path("data")
file = base / "reports" / "monthly.csv"

# Check existence
if file.exists():        print("found")
if file.parent.exists(): print("parent dir exists")

# Create directory (and parents)
Path("reports/2024").mkdir(parents=True, exist_ok=True)

# Read / write text
text = Path("config.json").read_text(encoding="utf-8")
Path("output.txt").write_text("hello", encoding="utf-8")

# Iterate files in a directory
for csv_file in Path("data").glob("*.csv"):
    print(csv_file.name)         # "sales_jan.csv"
    print(csv_file.stem)         # "sales_jan"
    print(csv_file.suffix)       # ".csv"
    print(csv_file.resolve())    # full absolute path

# Safe temp file pattern (write-then-rename avoids partial writes)
tmp = file.with_suffix(".tmp")
tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
tmp.rename(file)   # atomic on most filesystems
```

---

## Quick-Reference: Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| `except: pass` — silent errors | `except SpecificError as e: logger.error(...)` |
| `open(f)` without `with` | Always use `with open(f) as handle:` |
| Mutable default arg `def f(x=[])` | `def f(x=None)` → `if x is None: x = []` |
| CSV reader iterated twice | `rows = list(csv.DictReader(f))` then iterate `rows` |
| `env.get("KEY")` before `load_dotenv()` | Call `load_dotenv()` first |
| Division by zero on empty list | `return total / count if count else 0.0` |
| `isinstance(True, int)` is `True` | Check `isinstance(x, bool)` before `isinstance(x, int)` |
| Logger with no handler = silent | Call `basicConfig()` or add a handler explicitly |
