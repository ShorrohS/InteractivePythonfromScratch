# 📝 Phase 18 — Beginner Exercises

> **Mini-Project Format:** Each exercise is a small but complete application or module to build.
> Unlike snippet exercises, you will write multiple functions, handle real files, and structure
> your code properly. Attempt ALL projects before checking solutions.
>
> Solutions: `../../solutions/beginner/solutions.md`

---

## Q1. ⭐ Structured Application Logger

**Business context:** Every production application needs logging. Console output is not enough —
logs must be written to files, rotated to prevent disk overflow, and formatted consistently so
operators can search them later.

**Your task:** Create a module `app_logger.py` that sets up a logger with two handlers:
- A **console handler** that shows `WARNING` level and above
- A **rotating file handler** that writes ALL levels to `app.log` (max 5 KB per file, keep 3 backups)

**Requirements:**
1. Write a function `get_logger(name: str) -> logging.Logger` that returns a fully configured logger
2. The formatter must produce: `2024-01-15 14:32:07 | INFO     | message`
3. Log one message at each of the five standard levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
4. The console should only show the WARNING, ERROR, and CRITICAL messages
5. The file `app.log` must contain all five messages

**Sample usage:**
```python
logger = get_logger("sales_app")
logger.debug("Loading config file")
logger.info("Application started — env: production")
logger.warning("Config value missing, using default: MAX_RETRIES=3")
logger.error("Failed to connect to database at localhost:5432")
logger.critical("Data corruption detected — initiating emergency shutdown")
```

**Expected console output (WARNING and above only):**
```
2024-01-15 14:32:07 | WARNING  | Config value missing, using default: MAX_RETRIES=3
2024-01-15 14:32:07 | ERROR    | Failed to connect to database at localhost:5432
2024-01-15 14:32:07 | CRITICAL | Data corruption detected — initiating emergency shutdown
```

**Hints:**
- `logging.handlers.RotatingFileHandler` handles automatic log rotation
- Set the logger itself to `DEBUG`, then apply level filters on each individual handler
- `logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")` gives the right format

---

## Q2. ⭐ Environment Configuration Loader

**Business context:** Hard-coding database passwords and API keys in source code is a security
risk. Production applications read secrets from environment variables, often loaded from a `.env`
file that is never committed to source control.

**Your task:** Create a module `config.py` with a function `load_config() -> dict` that reads
application configuration from `os.environ`.

**Required variables (all must be present — fail loudly if any are missing):**
| Variable | Description |
|----------|-------------|
| `DB_HOST` | Database hostname |
| `DB_PORT` | Database port — must coerce to `int` |
| `DB_NAME` | Database name |
| `APP_ENV` | Must be one of: `development`, `staging`, `production` |
| `LOG_LEVEL` | Must be one of: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

**Optional variables (use defaults if absent):**
| Variable | Default |
|----------|---------|
| `MAX_RETRIES` | `3` |
| `TIMEOUT_SEC` | `30` |

**Requirements:**
1. Collect ALL missing required variables before raising — show them all at once
2. Raise `ValueError` with a descriptive message for each problem found
3. Return a dict with all values, with `DB_PORT`, `MAX_RETRIES`, and `TIMEOUT_SEC` coerced to `int`
4. Keys in the returned dict should be lowercase (e.g. `"db_host"`, not `"DB_HOST"`)

**Sample `.env` values to test with (set via `os.environ` in a test script):**
```python
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "sales_db"
os.environ["APP_ENV"] = "development"
os.environ["LOG_LEVEL"] = "INFO"
```

**Expected behavior:**
```python
# With all vars set correctly:
config = load_config()
# Returns: {'db_host': 'localhost', 'db_port': 5432, 'db_name': 'sales_db',
#           'app_env': 'development', 'log_level': 'INFO',
#           'max_retries': 3, 'timeout_sec': 30}

# With DB_HOST and DB_NAME missing:
# ValueError: Missing required configuration variables: DB_HOST, DB_NAME

# With DB_PORT="abc":
# ValueError: DB_PORT must be an integer, got: 'abc'

# With APP_ENV="qa":
# ValueError: APP_ENV must be one of development, staging, production — got: 'qa'
```

**Hints:**
- `os.environ.get("KEY")` returns `None` if absent; `os.environ["KEY"]` raises `KeyError`
- Build a list of error messages, then raise all at once to give the user complete feedback
- `if not os.environ.get("DB_HOST"):` catches both missing and empty-string values

---

## Q3. ⭐ CSV Data Cleaner

**Business context:** Data imported from spreadsheets is almost always messy — blank rows,
inconsistent capitalisation, extra whitespace, missing fields. A cleaning step is always the
first stage of any data pipeline.

**Your task:** Create a script `csv_cleaner.py` that reads a messy CSV, applies cleaning rules,
and writes a clean version.

**Create this input file as `employees_raw.csv` to test with:**
```
id,first_name,last_name,department,salary
1,alice,SMITH,engineering,75000
2,BOB,jones,  MARKETING  ,82000
3,,,  ,
4,Carol,WHITE,Engineering,91000
5,dave,Brown,marketing,67000
,frank,MILLER,SALES,58000
7,  ,Davis,ENGINEERING,
```

**Cleaning rules (apply in this order):**
1. Skip any row where `id` is empty or not a whole number
2. Skip any row where both `first_name` and `last_name` are empty
3. Skip any row where `first_name` is empty (even if last name is present)
4. Strip leading/trailing whitespace from every field
5. Title-case `first_name`, `last_name`, and `department`
6. If `salary` is empty, set it to `0`
7. Write clean rows to `employees_clean.csv`

**Print a summary after running:**
```
CSV Cleaner Summary
-------------------
Rows read:    7
Rows skipped: 3
Rows written: 4
```

**Expected output file (`employees_clean.csv`):**
```
id,first_name,last_name,department,salary
1,Alice,Smith,Engineering,75000
2,Bob,Jones,Marketing,82000
4,Carol,White,Engineering,91000
5,Dave,Brown,Marketing,67000
```

**Hints:**
- `csv.DictReader` reads rows as dicts keyed by the header row
- `csv.DictWriter` writes dicts back — pass `fieldnames=reader.fieldnames` to preserve column order
- `value.strip().isdigit()` checks that a string is a valid whole number

---

## Q4. ⭐ JSON Expense Tracker

**Business context:** A small expense tracker stores transactions in a JSON file so data persists
between runs. This is the simplest form of persistent application state — no database required.

**Your task:** Create `expense_tracker.py` with a simple command-line menu.

**JSON data structure (stored in `expenses.json`):**
```json
[
  {"id": 1, "date": "2024-01-15", "description": "Office supplies", "amount": 45.99, "category": "supplies"},
  {"id": 2, "date": "2024-01-16", "description": "Team lunch",      "amount": 87.50, "category": "meals"},
  {"id": 3, "date": "2024-01-17", "description": "Printer paper",   "amount": 23.00, "category": "supplies"}
]
```

**Menu:**
```
1. Add expense
2. List all expenses
3. List by category
4. Show category totals
5. Delete expense by ID
6. Exit
```

**Requirements:**
1. Load `expenses.json` on startup — create an empty list if the file does not exist
2. Save to `expenses.json` after every add or delete
3. Auto-generate incrementing IDs (never reuse a deleted ID)
4. Validate: `amount` must be a positive number, `date` must match `YYYY-MM-DD`
5. Category totals sorted from highest to lowest spending
6. Use `json.dump(..., indent=2)` so the file is human-readable

**Expected output for option 4 (with the sample data above):**
```
Category Totals:
  meals      $87.50
  supplies   $68.99
```

**Hints:**
- `try/except FileNotFoundError` handles first run when no file exists
- `datetime.datetime.strptime(s, "%Y-%m-%d")` raises `ValueError` if the format is wrong — use that to validate
- `max((e["id"] for e in expenses), default=0) + 1` gives the next safe ID

---

## Q5. ⭐ Employee Data Validator

**Business context:** Before importing employee records into an HR system, every record must
pass validation. Rather than crashing on the first bad field, a good validator collects ALL
errors and returns them so the user can fix everything at once.

**Your task:** Create a module `validator.py` with a function:
```python
def validate_employee(data: dict) -> list[str]:
```
Return a list of error messages. An empty list means the record is valid.

**Fields and rules:**
| Field | Type | Rule |
|-------|------|------|
| `employee_id` | str | Required. Must match `EMP-DDDD` (e.g. `EMP-0042`) |
| `first_name` | str | Required. 2–50 characters |
| `last_name` | str | Required. 2–50 characters |
| `email` | str | Required. Must contain `@` and a `.` after the `@` |
| `department` | str | Required. One of: Engineering, Marketing, Sales, HR, Finance |
| `salary` | int/float | Required. Between 20000 and 500000 |
| `start_date` | str | Required. Format `YYYY-MM-DD` |
| `is_active` | bool | Required. Must be `True` or `False` (not the string `"yes"`) |

**Sample test cases:**
```python
valid = {
    "employee_id": "EMP-0042", "first_name": "Alice", "last_name": "Smith",
    "email": "alice@company.com", "department": "Engineering",
    "salary": 85000, "start_date": "2023-06-15", "is_active": True
}
print(validate_employee(valid))  # []

invalid = {
    "employee_id": "EMP42",       # wrong format
    "first_name": "A",            # too short
    # last_name missing
    "email": "not-an-email",      # no @
    "department": "IT",           # not in allowed list
    "salary": 15000,              # below minimum
    "start_date": "15-06-2023",   # wrong date format
    "is_active": "yes"            # string instead of bool
}
print(validate_employee(invalid))
# [
#   "employee_id: must match format EMP-DDDD (e.g. EMP-0042)",
#   "first_name: must be 2–50 characters",
#   "last_name: required field is missing",
#   "email: must be a valid email address",
#   "department: must be one of Engineering, Finance, HR, Marketing, Sales",
#   "salary: must be between 20000 and 500000",
#   "start_date: must be in YYYY-MM-DD format",
#   "is_active: must be a boolean (True or False)"
# ]
```

**Hints:**
- `re.match(r"^EMP-\d{4}$", value)` validates the ID pattern
- `isinstance(value, bool)` — note that `bool` is a subclass of `int`; always check `bool` first before `int`
- Wrap `datetime.datetime.strptime(value, "%Y-%m-%d")` in `try/except ValueError` to validate date format

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
