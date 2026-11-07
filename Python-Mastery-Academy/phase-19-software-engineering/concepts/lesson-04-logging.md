# Lesson 04 — Logging

**Phase:** 19 — Software Engineering | **Time:** ~25 min

---

## Part 1: Why Logging over print()?

```
print()          Logging
──────────────   ──────────────────────────────────
Hard to disable  Can set levels (DEBUG/INFO/WARNING)
No context       Includes timestamp, module, level
No levels        Easy to filter by severity
Not for prod     Industry standard for production
```

---

## Part 2: Basic Setup

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

logger.debug("Detailed debug info — development only")
logger.info("Normal operation message")
logger.warning("Something unexpected but recoverable")
logger.error("A serious problem — functionality affected")
logger.critical("Critical failure — system may stop")
```

Output:
```
2024-01-15 10:30:45 | main | INFO | Normal operation message
2024-01-15 10:30:45 | main | WARNING | Something unexpected
```

---

## Part 3: Professional Setup

```python
import logging
import logging.handlers
from pathlib import Path

def setup_logging(
    name: str,
    log_file: str = "app.log",
    console_level=logging.INFO,
    file_level=logging.DEBUG
) -> logging.Logger:
    """Configure application logging with console + file handlers."""

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # capture everything
    logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler (INFO and above)
    console = logging.StreamHandler()
    console.setLevel(console_level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Rotating file handler (DEBUG and above)
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10_000_000,   # 10 MB per file
        backupCount=5          # keep 5 old files
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# In your app's main module:
logger = setup_logging(__name__, "logs/app.log")
logger.info("Application started")
```

---

## Part 4: Logging Best Practices

```python
# 1. Use module-level logger
logger = logging.getLogger(__name__)   # named after module

# 2. Use f-strings only if log will be emitted
# BAD: expensive string formatting always happens
logger.debug("Processing %s items" % len(large_list))

# GOOD: string built only when DEBUG is enabled
logger.debug("Processing %d items", len(large_list))
# OR: use lazy evaluation
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(f"Processing {len(large_list)} items")

# 3. Include context in messages
# BAD:
logger.error("Not found")

# GOOD:
logger.error("Employee not found: id=%d", employee_id)

# 4. Log exceptions with traceback
try:
    risky_operation()
except Exception as e:
    logger.error("Failed to process payment", exc_info=True)
    # exc_info=True includes the full traceback

# 5. Use structured logging for production
logger.info("Payment processed", extra={
    "user_id": 42,
    "amount": 99.99,
    "currency": "USD"
})
```

---

## Part 5: Logging Levels Decision Guide

```
DEBUG    → Detailed diagnostics. Used only during development.
INFO     → Confirmation things work. "User logged in", "Order created".
WARNING  → Something unexpected, but recoverable. "Retry attempt 2/3".
ERROR    → Serious problem. Function failed. Alert needed.
CRITICAL → System-level failure. Immediate action required.
```

---

## Part 6: Context in Flask/FastAPI

```python
# Add request context to all logs
import logging

app_logger = logging.getLogger("myapp")

@app.before_request
def log_request():
    app_logger.info(
        "Request: %s %s from %s",
        request.method, request.path, request.remote_addr
    )

@app.after_request
def log_response(response):
    app_logger.info(
        "Response: %d for %s %s",
        response.status_code, request.method, request.path
    )
    return response
```
