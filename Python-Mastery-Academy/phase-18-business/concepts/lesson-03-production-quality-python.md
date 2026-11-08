# Lesson 03 — Production-Quality Python

**Phase:** 18 — Business Projects | **Time:** ~60 min | **Prerequisite:** Lesson 02

---

## Learning Objectives

- Configure the `logging` module with multiple handlers and custom formatters
- Write to both a file and the console with a single logger
- Load environment-specific settings via `os.environ` and `.env` files
- Build a custom exception hierarchy for expressive, structured error handling
- Use context managers to guarantee resource cleanup even when errors occur
- Implement a simple retry pattern for unreliable operations (network, I/O)

---

## Part 1: Why `print()` Is Not Enough

`print()` statements disappear silently in production. You can't filter them by severity, direct them to a file, or add timestamps. The `logging` module solves all of that and is already in the standard library.

```
Severity levels (low → high):
  DEBUG    → detailed diagnostic info (dev only)
  INFO     → normal operational events
  WARNING  → something unexpected but recoverable
  ERROR    → a task failed, the app can continue
  CRITICAL → a serious failure, the app may not continue
```

Setting the level to `INFO` means `DEBUG` messages are silently dropped — no code changes needed when you move from dev to production.

---

## Part 2: Basic Logger Setup

```python
import logging

# Get (or create) a logger named after the module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)   # capture everything at this logger

# --- Console handler ---
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)   # only INFO+ to console

# --- File handler ---
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)     # everything to the file

# --- Formatter ---
formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Attach handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# --- Usage ---
logger.debug("Loading configuration...")          # → file only
logger.info("Application started.")               # → console + file
logger.warning("Config file not found, using defaults.")
logger.error("Database connection failed.")
logger.critical("Out of disk space — shutting down.")
```

Sample output in `app.log`:
```
2024-01-15 09:00:01 | DEBUG    | __main__ | Loading configuration...
2024-01-15 09:00:01 | INFO     | __main__ | Application started.
2024-01-15 09:00:02 | WARNING  | __main__ | Config file not found, using defaults.
```

---

## Part 3: Application-Wide Logging Setup

Centralise logger setup so every module in the application inherits the same configuration.

```python
# src/invoicing/logging_config.py
import logging
import logging.handlers
from pathlib import Path

def setup_logging(log_dir: str = "logs", level: str = "INFO") -> None:
    """Configure root logger once at application startup."""
    Path(log_dir).mkdir(exist_ok=True)
    log_level = getattr(logging, level.upper(), logging.INFO)

    root = logging.getLogger()   # root logger — all child loggers inherit
    root.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Rotating file: max 5 MB, keep last 3 files
    fh = logging.handlers.RotatingFileHandler(
        f"{log_dir}/app.log", maxBytes=5 * 1024 * 1024, backupCount=3,
        encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)    # controlled by environment
    ch.setFormatter(fmt)

    root.addHandler(fh)
    root.addHandler(ch)

# In main.py — call once, first thing
# from invoicing.logging_config import setup_logging
# setup_logging(level=config.log_level)
```

Any module then just does:

```python
import logging
logger = logging.getLogger(__name__)
# No handler setup needed — inherits from root
```

---

## Part 4: Environment Variables and `.env` Files

Credentials and environment-specific values must never be hard-coded in source files.

```python
# src/invoicing/config.py
import os

class Settings:
    """Reads from environment variables with sensible defaults."""

    # Database
    DB_HOST:  str  = os.environ.get("DB_HOST",  "localhost")
    DB_PORT:  int  = int(os.environ.get("DB_PORT",  "5432"))
    DB_NAME:  str  = os.environ.get("DB_NAME",  "invoicing")
    DB_USER:  str  = os.environ.get("DB_USER",  "app_user")
    DB_PASS:  str  = os.environ.get("DB_PASS",  "")   # no default for secrets

    # Application
    DEBUG:    bool = os.environ.get("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")

    @classmethod
    def validate(cls) -> None:
        """Fail fast at startup if critical config is missing."""
        missing = []
        if not cls.DB_PASS:
            missing.append("DB_PASS")
        if not cls.SECRET_KEY:
            missing.append("SECRET_KEY")
        if missing:
            raise EnvironmentError(
                f"Required environment variables not set: {', '.join(missing)}"
            )
```

A `.env` file for local development (never committed to git):

```ini
# .env — local development only
DB_HOST=localhost
DB_PORT=5432
DB_NAME=invoicing_dev
DB_USER=dev_user
DB_PASS=dev_password_123
LOG_LEVEL=DEBUG
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production
```

Load it with a small helper (no external library needed):

```python
def load_dotenv(path: str = ".env") -> None:
    """Load KEY=VALUE pairs from a .env file into os.environ."""
    from pathlib import Path
    env_file = Path(path)
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())
```

---

## Part 5: Custom Exception Hierarchy

A flat `raise Exception("something went wrong")` tells callers nothing useful. A hierarchy lets you catch at the right level of specificity.

```python
# src/invoicing/exceptions.py

class InvoicingError(Exception):
    """Base exception for the entire application."""

class DataError(InvoicingError):
    """Raised when input data is invalid or unreadable."""

class ValidationError(DataError):
    """Raised when a record fails business-rule validation."""
    def __init__(self, field: str, value, message: str):
        self.field = field
        self.value = value
        super().__init__(f"Validation failed on '{field}' = {value!r}: {message}")

class DatabaseError(InvoicingError):
    """Raised when a database operation fails."""

class ConnectionError(DatabaseError):
    """Raised when a database connection cannot be established."""

class NotFoundError(DatabaseError):
    """Raised when a requested record does not exist."""
    def __init__(self, entity: str, identifier):
        super().__init__(f"{entity} with id={identifier!r} not found.")
        self.entity = entity
        self.identifier = identifier
```

Usage:

```python
from invoicing.exceptions import ValidationError, NotFoundError
import logging

logger = logging.getLogger(__name__)

def get_invoice(invoice_id: str, store: dict):
    if invoice_id not in store:
        raise NotFoundError("Invoice", invoice_id)   # specific
    return store[invoice_id]

try:
    inv = get_invoice("INV-9999", {})
except NotFoundError as e:
    logger.warning(str(e))                         # log at WARNING, not ERROR
except DatabaseError as e:
    logger.error("Database problem: %s", e)        # catches all DB errors
except InvoicingError as e:
    logger.critical("Unhandled application error: %s", e)
```

---

## Part 6: Context Managers for Guaranteed Cleanup

Context managers (the `with` statement) ensure cleanup code always runs — even when exceptions occur.

```python
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

@contextmanager
def managed_db_connection(dsn: str):
    """Open a DB connection; always close it, even on error."""
    conn = None
    try:
        logger.info("Opening database connection to %s", dsn)
        conn = _connect(dsn)   # hypothetical connection call
        yield conn
        conn.commit()
        logger.info("Transaction committed.")
    except Exception as e:
        if conn:
            conn.rollback()
            logger.error("Transaction rolled back due to: %s", e)
        raise   # re-raise so the caller knows something went wrong
    finally:
        if conn:
            conn.close()
            logger.debug("Database connection closed.")


# Usage — cleanup is guaranteed regardless of what happens inside
with managed_db_connection("postgresql://localhost/invoicing") as conn:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO invoices VALUES (%s, %s)", ("INV-0001", "Acme"))
```

---

## Part 7: Retry Logic

Network calls and file I/O occasionally fail transiently. A simple retry wrapper avoids cascading failures.

```python
import time
import logging
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)
T = TypeVar("T")

def retry(
    func: Callable[..., T],
    *args,
    attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    **kwargs
) -> T:
    """
    Call func(*args, **kwargs), retrying on specified exceptions.
    Uses exponential backoff: delay, delay*backoff, delay*backoff^2, ...
    """
    wait = delay
    last_exception: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            return func(*args, **kwargs)
        except exceptions as e:
            last_exception = e
            if attempt < attempts:
                logger.warning(
                    "Attempt %d/%d failed (%s). Retrying in %.1fs...",
                    attempt, attempts, e, wait
                )
                time.sleep(wait)
                wait *= backoff
            else:
                logger.error("All %d attempts failed: %s", attempts, e)

    raise last_exception   # type: ignore[misc]


# Usage
def fetch_exchange_rate(currency: str) -> float:
    # ... calls an external API ...
    pass

rate = retry(
    fetch_exchange_rate,
    "USD",
    attempts=3,
    delay=0.5,
    backoff=2.0,
    exceptions=(ConnectionError, TimeoutError)
)
```

---

## Key Takeaways

- Replace `print()` with `logging` from day one — set level, attach handlers, and every module gets structured output for free
- `RotatingFileHandler` prevents log files from growing without bound in production
- Environment variables + `.env` files keep secrets out of source control and make the same codebase deployable to any environment
- A custom exception hierarchy lets callers catch at the right granularity — `ValidationError` vs `DatabaseError` vs the catch-all `InvoicingError`
- Context managers guarantee cleanup (close connections, rollback transactions) even when exceptions occur
- Exponential-backoff retry logic absorbs transient failures without hammering a struggling service

---

## What's Next

**Phase 18 — Business Projects**

You now have the architectural, data, and production patterns to build real business applications. The projects in this phase — employee management, expense tracking, sales analytics, inventory management, and ticket management — each apply these three lessons end-to-end. Start with the project READMEs and implement them one layer at a time: models → data pipeline → config + logging → controller → reports.
