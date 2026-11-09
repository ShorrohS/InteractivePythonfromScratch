# Phase 18 — Quiz 01: Business Python

**Questions:** 20 | **Pass:** 16/20 | **Time:** 25 min (no notes)

---

## Section 1: Logging (Q1–Q4)

**Q1.** You run this code but see nothing printed to the console. What is wrong?

```python
import logging
logger = logging.getLogger("myapp")
logger.warning("Something went wrong")
```

```
A) getLogger() does not exist — use logging.Logger() instead
B) No handler has been added and basicConfig() was never called
C) warning() requires a second argument for the message
D) getLogger() returns None by default
```

---

**Q2.** You want your logger to write `DEBUG` and above to a file, but only `ERROR` and above to the console. Which approach is correct?

```
A) Create two loggers: one set to DEBUG, one set to ERROR
B) Set the root logger to ERROR and add a file handler set to DEBUG
C) Set the logger level to DEBUG; add a FileHandler(level=DEBUG) and StreamHandler(level=ERROR)
D) Call logging.basicConfig(level=DEBUG) twice with different arguments
```

---

**Q3.** What does this log formatter produce?

```python
fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                         datefmt="%Y-%m-%d")
```

```
A) 2024-01-15 14:32:07 | WARNING  | msg
B) 2024-01-15 | WARNING  | msg
C) WARNING | 2024-01-15 | msg
D) asctime | levelname | message
```

---

**Q4.** What is the purpose of `RotatingFileHandler(maxBytes=5120, backupCount=3)`?

```
A) Writes to 3 separate files simultaneously, max 5 KB each
B) Rotates the log file when it reaches 5 KB; keeps the 3 most recent backups
C) Deletes log entries older than 3 days when the file exceeds 5 KB
D) Compresses log files after 3 rotations
```

---

## Section 2: Configuration Management (Q5–Q7)

**Q5.** What is wrong with this approach to loading a database password?

```python
DB_PASSWORD = "s3cr3tP@ssw0rd"   # used throughout the module
```

```
A) Variable names for secrets must start with SECRET_
B) The password is hard-coded — it will be committed to version control and visible to anyone with repo access
C) This is fine for development but must be wrapped in os.environ for production
D) Passwords must be stored as bytes, not strings
```

---

**Q6.** You call `os.environ.get("DB_PORT")` when `DB_PORT` is not set. What do you get?

```
A) KeyError
B) ""  (empty string)
C) None
D) "0"
```

---

**Q7.** A `ConfigManager` must load values from a JSON file but allow environment variables to override them. Which precedence order is correct?

```
A) JSON file > environment variables > code defaults
B) Code defaults > JSON file > environment variables
C) Environment variables > JSON file > code defaults
D) Code defaults > environment variables > JSON file
```

---

## Section 3: Error Handling Patterns (Q8–Q11)

**Q8.** What is wrong with this error handling?

```python
def load_config(path):
    try:
        return json.load(open(path))
    except:
        pass
```

```
A) json.load() is deprecated — use json.loads() with open().read()
B) The bare except swallows all exceptions silently, including KeyboardInterrupt and SystemExit
C) open() must use a context manager or the code won't run
D) pass is not a valid statement inside except
```

---

**Q9.** You are building a retry decorator. After `max_attempts=3` with `delay=1.0` and `backoff=2.0`, what are the three sleep durations (in seconds)?

```
A) 1.0, 1.0, 1.0    (constant delay)
B) 1.0, 2.0         (only sleep before 2nd and 3rd attempt — no sleep after the final failure)
C) 1.0, 2.0, 4.0    (sleep after every attempt including the last)
D) 0.5, 1.0, 2.0    (half the delay first)
```

---

**Q10.** Your `handle_errors` decorator catches `FileNotFoundError`. A caller passes a path containing a `PermissionError`. What should happen?

```
A) PermissionError is caught and returned as {"success": False, ...}
B) PermissionError propagates — the decorator only catches the listed types
C) The function retries automatically
D) PermissionError is wrapped in FileNotFoundError and re-raised
```

---

**Q11.** Which of these is NOT a good reason to use structured error dicts (`{"success": False, "error": "..."}`) instead of raising exceptions?

```
A) When building a service layer where callers don't use try/except
B) When you want consistent error shapes across many functions
C) To make all errors silently ignorable by the caller
D) When returning error details across an API boundary (e.g. JSON response)
```

---

## Section 4: Data Pipeline Design (Q12–Q15)

**Q12.** You iterate over a `csv.DictReader` object twice in the same function:

```python
reader = csv.DictReader(f)
count = sum(1 for row in reader)   # first iteration
data  = [row for row in reader]    # second iteration
```

What is in `data` after this code runs?

```
A) All rows from the CSV
B) An empty list — the reader is exhausted after the first iteration
C) The same rows as the first iteration — DictReader resets automatically
D) A TypeError — DictReader cannot be iterated twice
```

---

**Q13.** You need to transform a list of sales dicts into a report grouped by month. Which is the most Pythonic approach?

```
A) Use a for-loop with if/else inside to build a nested dict
B) Sort by month then use a for-loop with setdefault()
C) Use collections.defaultdict(dict) or dict.setdefault() with a simple for-loop
D) Convert to a CSV string first, then parse it back
```

---

**Q14.** Which `csv.DictWriter` call correctly writes a header row before the data?

```
A) writer.write_header()
B) writer.writeheader()
C) writer.writerow(fieldnames)
D) writer.header = True
```

---

**Q15.** You read a CSV file and notice amounts are stored as strings like `"1,234.56"`. Which conversion handles the comma correctly?

```
A) int("1,234.56")
B) float("1,234.56")
C) float("1,234.56".replace(",", ""))
D) decimal.Decimal("1,234.56")
```

---

## Section 5: Validation & Business Logic (Q16–Q18)

**Q16.** You need to validate that a field is a `bool`, not just truthy/falsy. Which check is correct?

```python
value = 1   # should FAIL the bool check
```

```
A) if value:                      → passes (truthy)
B) if isinstance(value, int):     → passes (bool is subclass of int)
C) if isinstance(value, bool):    → fails correctly (1 is int, not bool)
D) if type(value) == (bool, int): → TypeError
```

---

**Q17.** Your validator must return ALL errors, not just the first. Which pattern achieves this?

```
A) Raise ValueError at the first error found
B) Use assert statements — they collect all failures
C) Build an errors list; append each error; return the list after all checks
D) Use a try/except block around every field check
```

---

**Q18.** Which regex correctly validates the employee ID format `EMP-0042` (3 uppercase letters, hyphen, exactly 4 digits)?

```
A) r"EMP-\d+"
B) r"^EMP-\d{4}$"
C) r"EMP\d{4}"
D) r"^[A-Z]{3}-[0-9]*$"
```

---

## Section 6: Architecture Patterns (Q19–Q20)

**Q19.** What is the main benefit of the Repository pattern?

```
A) It makes data access faster by caching results in memory
B) It abstracts the storage layer so business logic works against an interface, not a specific database
C) It automatically generates SQL queries from Python class definitions
D) It prevents duplicate records by checking before every insert
```

---

**Q20.** You have an `InMemoryRepository` for tests and a `PostgresRepository` for production, both implementing the same `Repository` ABC. A colleague asks why you don't just use the concrete class directly. What is the best answer?

```
A) Using the ABC is slower at runtime
B) The ABC enforces the interface contract — if PostgresRepository is missing a method,
   Python raises TypeError immediately when the class is defined, not at runtime
C) ABCs are required by PEP 8 for all data-access classes
D) InMemoryRepository and PostgresRepository cannot share any code without an ABC
```

---

## Answers

.
.
.
.
.
.

| Q  | Answer | Explanation |
|----|--------|-------------|
| 1  | B | Without a handler or `basicConfig()`, the logger has nowhere to send messages |
| 2  | C | Set the logger to DEBUG; each handler filters independently with its own level |
| 3  | B | `datefmt="%Y-%m-%d"` omits the time component — only the date appears |
| 4  | B | Rotates at 5 KB and keeps 3 backups: `app.log`, `app.log.1`, `app.log.2`, `app.log.3` |
| 5  | B | Hard-coded secrets end up in git history and are visible to everyone with repo access |
| 6  | C | `.get()` returns `None` when the key is absent (use `["KEY"]` if you want `KeyError`) |
| 7  | C | Env vars win over file config; file config wins over code defaults |
| 8  | B | `except: pass` catches everything silently — `KeyboardInterrupt` and bugs are hidden |
| 9  | B | Sleep only before retries: after attempt 1 sleep 1.0s, after attempt 2 sleep 2.0s; no sleep after final failure |
| 10 | B | Only the explicitly listed exception types are caught; all others propagate |
| 11 | C | Making errors silently ignorable is dangerous and defeats the purpose of error handling |
| 12 | B | `DictReader` is a generator-based iterator; once exhausted it yields nothing |
| 13 | C | `dict.setdefault()` or `defaultdict` handles nested grouping cleanly in one pass |
| 14 | B | `writer.writeheader()` is the correct method name |
| 15 | C | `float()` cannot parse commas — strip them first with `.replace(",", "")` |
| 16 | C | `isinstance(1, bool)` returns `False`; `isinstance(True, bool)` returns `True` |
| 17 | C | Append-and-return is the standard pattern for collecting multiple validation errors |
| 18 | B | `^` anchors start, `$` anchors end, `\d{4}` requires exactly 4 digits |
| 19 | B | Business logic depends on an interface, not an implementation — storage can be swapped |
| 20 | B | ABC enforces the contract at class-definition time, catching missing methods early |
