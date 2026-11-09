# 📝 Phase 18 — Intermediate Exercises

> **Mini-Project Format:** Each exercise is a module or class to design and build from scratch.
> Focus on reusability, testability, and production patterns — these components slot into larger systems.
>
> Solutions: `../../solutions/intermediate/solutions.md`

---

## Q1. ⭐⭐ Reusable DataValidator Class

**Business context:** Copying ad-hoc validation logic into every function that needs it leads to
inconsistency and bugs. A centralized validator lets you define rules once and apply them
everywhere in a declarative, readable way.

**Your task:** Build a `DataValidator` class in `data_validator.py` that provides a chainable
validation pipeline.

**Required API:**
```python
validator = DataValidator(data)

errors = (
    validator
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
    .validate()   # returns list[str] of all error messages
)
```

**Required methods on `FieldValidator` (returned by `.field()`):**
| Method | Description |
|--------|-------------|
| `.required()` | Error if field is missing or empty string |
| `.min_length(n)` | Error if string length < n |
| `.max_length(n)` | Error if string length > n |
| `.regex(pattern, message)` | Error if string does not match regex |
| `.range(min_val, max_val)` | Error if numeric value outside range |
| `.one_of(choices)` | Error if value not in choices list |

**Calling `.field()` again must return a new `FieldValidator` linked to the same `DataValidator`.**
After all chains, calling `.validate()` on the `DataValidator` returns all accumulated errors.

**Also add a `validate_or_raise()` method** that raises `ValidationError(errors)` instead of returning.

**Sample test:**
```python
result = DataValidator({"username": "AL", "age": 17, "role": "owner"}).validate()
# [
#   "username: must be at least 3 characters",
#   "username: only lowercase letters, digits, and underscores",
#   "age: must be between 18 and 120",
#   "role: must be one of ['admin', 'editor', 'viewer']"
# ]
```

**Hints:**
- Each `FieldValidator` accumulates its own `errors` list; the `DataValidator` collects them all at `.validate()`
- `.field()` on `DataValidator` creates a `FieldValidator`, appends it, and returns it
- The `FieldValidator` methods must return `self` so they can be chained — but `.validate()` is on `DataValidator`
- Return a new `DataValidator` from `FieldValidator.field()` — or give `FieldValidator` a back-reference to `DataValidator`

---

## Q2. ⭐⭐ Retry Decorator with Exponential Backoff

**Business context:** Network calls, file locks, and external API requests can fail transiently.
Rather than crashing the application on the first failure, retrying with exponential backoff
gives transient problems time to resolve while limiting how long the system waits.

**Your task:** Create a decorator `retry` in `retry_decorator.py`.

**Required decorator signature:**
```python
@retry(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(ConnectionError, TimeoutError))
def fetch_report(url: str) -> str:
    ...
```

**Behavior:**
1. Attempt the function call
2. If it raises one of `exceptions`: log a WARNING with attempt number and wait time, then sleep
3. Double the sleep time after each failure (`delay * backoff ** (attempt - 1)`)
4. After all attempts are exhausted, log an ERROR and re-raise the last exception
5. If the function raises an exception NOT in `exceptions`, let it propagate immediately

**Expected log output (max_attempts=3, delay=1.0, backoff=2.0):**
```
WARNING  | Attempt 1/3 failed for fetch_report: Connection refused. Retrying in 1.0s...
WARNING  | Attempt 2/3 failed for fetch_report: Connection refused. Retrying in 2.0s...
ERROR    | All 3 attempts failed for fetch_report: Connection refused
```

**Test harness to verify:**
```python
call_count = 0

@retry(max_attempts=3, delay=0.01, backoff=2.0, exceptions=(ValueError,))
def flaky_operation():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ValueError("transient failure")
    return "success"

result = flaky_operation()
assert result == "success"
assert call_count == 3
print("Test passed!")
```

**Hints:**
- Use `functools.wraps(func)` on the inner wrapper to preserve the original function's name and docstring
- `time.sleep(current_delay)` between retries
- `isinstance(e, tuple_of_types)` — or just `except exceptions as e:` works directly since `exceptions` is a tuple

---

## Q3. ⭐⭐ Repository Pattern — Abstract Base + In-Memory Implementation

**Business context:** The Repository pattern separates business logic from the data store. By
programming to an abstract `Repository` interface, you can swap in-memory storage (for tests)
for a database (for production) without changing any business code.

**Your task:** Create `repository.py` with two classes.

**`Repository` (abstract base class) — define these abstract methods:**
```python
class Repository(ABC):
    def add(self, entity: dict) -> dict:    ...  # returns entity with 'id' set
    def get(self, entity_id: int) -> dict | None: ...
    def get_all(self) -> list[dict]:        ...
    def update(self, entity: dict) -> dict: ...  # entity must have 'id' key
    def delete(self, entity_id: int) -> bool: ... # True if deleted, False if not found
    def count(self) -> int:                 ...
```

**`InMemoryRepository(Repository)` — concrete implementation using a dict:**
- Auto-assign incrementing integer IDs starting at 1
- `update()` must raise `KeyError` if the entity's ID does not exist
- All methods must work correctly with plain dicts (e.g. `{"name": "Alice", "salary": 50000}`)

**Test your implementation:**
```python
repo = InMemoryRepository()

alice = repo.add({"name": "Alice", "role": "engineer"})
print(alice)          # {"id": 1, "name": "Alice", "role": "engineer"}

bob = repo.add({"name": "Bob", "role": "manager"})
print(repo.count())   # 2

found = repo.get(1)
print(found["name"])  # Alice

repo.update({"id": 1, "name": "Alice", "role": "senior engineer"})
print(repo.get(1)["role"])  # senior engineer

deleted = repo.delete(99)
print(deleted)        # False

deleted = repo.delete(1)
print(deleted)        # True
print(repo.count())   # 1
```

**Hints:**
- `from abc import ABC, abstractmethod`
- `self._store: dict[int, dict] = {}` and `self._next_id: int = 1` as instance variables
- In `add()`, do `entity = dict(entity)` before mutating — don't modify the caller's dict
- Abstract methods decorated with `@abstractmethod` will raise `TypeError` if a subclass doesn't implement them

---

## Q4. ⭐⭐ Audit Log System

**Business context:** Compliance regulations (GDPR, SOX, HIPAA) require systems to record every
write operation — who changed what, and when. An audit trail must be immutable (append-only)
and queryable.

**Your task:** Create `audit_log.py` with an `AuditLog` class.

**Requirements:**
1. Every write is recorded with: `timestamp` (ISO-8601 UTC), `user`, `action`, `resource`, `details`
2. Entries are written to an append-only file (`audit.log`) as one JSON line per entry (JSONL format)
3. All entries are also kept in memory for fast querying during the session
4. Provide query methods: `get_history()`, `get_by_user(user)`, `get_by_resource(resource)`
5. Also provide an `@audited(audit_log, resource, action)` decorator that automatically records
   an entry when the decorated function is called

**Class interface:**
```python
log = AuditLog(log_file=Path("audit.log"))
log.record(user="alice", action="CREATE", resource="invoice", details={"invoice_id": 42})
log.record(user="bob",   action="DELETE", resource="employee", details={"id": 7})

print(log.get_by_user("alice"))   # [{"timestamp": ..., "user": "alice", ...}]
print(len(log.get_history()))     # 2
```

**Decorator usage:**
```python
@audited(log, resource="invoice", action="UPDATE")
def update_invoice(invoice_id: int, data: dict) -> None:
    ...   # audit entry recorded automatically
```

**Hints:**
- `datetime.datetime.utcnow().isoformat()` gives an ISO-8601 timestamp
- Open the log file with `"a"` (append) mode and write `json.dumps(entry) + "\n"` per record
- The decorator needs to determine the `user` — accept it as a keyword argument or use a sensible default like `"system"`

---

## Q5. ⭐⭐ Sales Report Generator

**Business context:** Management needs regular summaries of sales data. The report must be
available in CSV (for Excel) and JSON (for downstream systems) simultaneously.

**Your task:** Create `report_generator.py` with functions that transform a list of sales records
into grouped summary reports.

**Input data structure:**
```python
SAMPLE_SALES = [
    {"date": "2024-01-10", "rep": "Alice", "category": "Software", "amount": 1500.00},
    {"date": "2024-01-20", "rep": "Bob",   "category": "Hardware", "amount": 3200.00},
    {"date": "2024-02-05", "rep": "Alice", "category": "Hardware", "amount": 2800.00},
    {"date": "2024-02-14", "rep": "Carol", "category": "Software", "amount":  950.00},
    {"date": "2024-03-01", "rep": "Bob",   "category": "Services", "amount": 4100.00},
    {"date": "2024-03-18", "rep": "Carol", "category": "Software", "amount": 1750.00},
]
```

**Requirements:**
1. `group_by_month_category(sales)` → `dict[str, dict[str, float]]`
   Groups totals as `{"2024-01": {"Software": 1500.0, "Hardware": 3200.0}, ...}`
2. `group_by_rep(sales)` → `dict[str, float]`
   Total per sales rep, sorted highest to lowest
3. `generate_csv_report(sales, output_path)` → writes a CSV with columns: `month, category, total`
4. `generate_json_report(sales, output_path)` → writes the month/category dict as pretty JSON
5. A `print_console_summary(sales)` that prints a formatted table with a grand total row

**Expected console summary:**
```
Month      Category        Total
--------------------------------------
2024-01    Hardware    $3,200.00
2024-01    Software    $1,500.00
2024-02    Hardware    $2,800.00
2024-02    Software      $950.00
2024-03    Services    $4,100.00
2024-03    Software    $1,750.00
--------------------------------------
Grand Total            $14,300.00
```

**Hints:**
- `sale["date"][:7]` extracts the `YYYY-MM` prefix for month grouping
- `sorted(totals.items(), key=lambda x: -x[1])` sorts by value descending
- `csv.DictWriter(f, fieldnames=["month", "category", "total"])` for clean CSV output

---

## Q6. ⭐⭐ Config Manager with File + Environment Override

**Business context:** Applications need configuration from multiple sources: a versioned config
file for defaults and structure, environment variables for deployment-specific overrides
(database passwords, feature flags). Environment always wins.

**Your task:** Create `config_manager.py` with a `ConfigManager` class.

**Constructor:**
```python
manager = ConfigManager(
    config_file=Path("config.json"),
    schema={
        "db_host":    {"type": "str",  "required": True},
        "db_port":    {"type": "int",  "required": True},
        "db_name":    {"type": "str",  "required": True},
        "debug":      {"type": "bool", "required": False, "default": False},
        "max_retries":{"type": "int",  "required": False, "default": 3},
    }
)
config = manager.load()
```

**Rules:**
1. Load defaults from `config.json` if it exists (ignore file silently if it does not)
2. Override any key with its `UPPER_CASE` environment variable counterpart (e.g. `db_port` → `DB_PORT`)
3. Apply type coercion per schema: `"int"` → `int()`, `"bool"` → `"true"` (case-insensitive) maps to `True`
4. Raise `ValueError` listing ALL missing required keys if any are absent after merging
5. Provide `manager.get(key, default=None)` for individual value access after loading

**Test scenario:**
```python
# config.json: {"db_host": "localhost", "db_port": 5432, "db_name": "mydb"}
# os.environ["DB_PORT"] = "9999"   ← env overrides file
config = manager.load()
print(config["db_port"])   # 9999 (int, from env)
print(config["debug"])     # False (default)
```

**Hints:**
- Start with file values → apply env overrides → apply defaults for missing optional keys
- For bool coercion from string: `raw.lower() == "true"` if `isinstance(raw, str)` else `bool(raw)`
- Log each value and its source (file / env / default) at DEBUG level to aid debugging

---

## Q7. ⭐⭐ Error Handler Decorator

**Business context:** Letting exceptions propagate as raw tracebacks to API callers or end users
is poor UX. A consistent error handler catches known exceptions, logs them with full context,
and returns a structured response that callers can handle predictably.

**Your task:** Create `error_handler.py` with a `handle_errors` decorator.

**Required behavior:**
- On **success**: return `{"success": True, "data": <return_value>}`
- On **caught exception**: log it and return `{"success": False, "error": "<message>", "error_type": "<ClassName>"}`
- Only catch the exception types specified — others propagate normally

**Decorator signature:**
```python
@handle_errors(ValueError, KeyError, log_level="warning")
def get_employee(employee_id: int) -> dict:
    ...
```

**Sample usage:**
```python
@handle_errors(ValueError, FileNotFoundError)
def load_config(path: str) -> dict:
    if not Path(path).exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    return json.loads(Path(path).read_text())

result = load_config("missing.json")
print(result)
# {"success": False, "error": "Config file not found: missing.json", "error_type": "FileNotFoundError"}

result = load_config("valid_config.json")
print(result)
# {"success": True, "data": {"db_host": "localhost", ...}}
```

**Requirements:**
1. The decorator must accept multiple exception types as positional args
2. A `log_level` keyword argument controls whether caught errors are logged at `warning` or `error` level
3. Preserve the original function's name and docstring (`functools.wraps`)
4. The logged message should include the function name, exception type, and exception message

**Hints:**
- `*exception_types` collects positional arguments as a tuple, which works directly in `except exception_types as e:`
- `getattr(logger, log_level.lower(), logger.error)` gets the log method by name
- Default `exception_types` to `(Exception,)` if none are provided

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
