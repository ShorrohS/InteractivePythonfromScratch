# Phase 18 — Completion Assessment: Budget Tracking CLI

> **Pass mark:** 80% | **Time:** 60 minutes | **Open book:** No
>
> Build a command-line Budget Tracking Application from scratch.
> You may use any Python standard library module. No third-party packages.

---

## Introduction

You are building `budget_cli.py` — a command-line application for tracking departmental budgets.
The application must be self-contained (no imports from your own modules), runnable with
`python budget_cli.py`, and persist data between runs using JSON.

Read all four parts before writing any code. Plan your data structures first.

---

## PART A: Implementation Tasks (60 points)

### Task 1 — Configuration & Logging Setup (10 points)

At the top of `budget_cli.py`, implement:

**Logging:**
- A rotating file logger writing to `budget.log` (max 10 KB, 2 backups)
- Console handler showing `WARNING` and above only
- Format: `YYYY-MM-DD HH:MM:SS | LEVEL    | message`

**Configuration (read from environment variables):**

| Variable | Type | Required | Default |
|----------|------|----------|---------|
| `APP_ENV` | str | No | `"development"` |
| `DATA_FILE` | str | No | `"budget_data.json"` |
| `ALERT_THRESHOLD` | float | No | `0.80` |

- Raise `ValueError` with a descriptive message if `APP_ENV` is not one of:
  `development`, `staging`, `production`
- Log the loaded config values at `DEBUG` level on startup

**Deliverable:** Function `setup()` that returns a `(logger, config)` tuple.

---

### Task 2 — Data Models (15 points)

Implement two dataclass-like structures (you may use `@dataclass` or plain dicts — your choice):

**`BudgetCategory`:**
```python
name:           str       # unique, title-cased
monthly_budget: float     # must be > 0
```

Validation rules (raise `ValueError` with descriptive messages):
- `name` must be 2–50 characters
- `monthly_budget` must be greater than 0

**`Transaction`:**
```python
id:          int           # auto-assigned
date:        str           # YYYY-MM-DD
department:  str           # must match an existing category name
amount:      float         # must be > 0
description: str           # required, max 100 characters
```

Validation rules (raise `ValueError` with descriptive messages):
- `amount` must be > 0
- `date` must be valid `YYYY-MM-DD`
- `description` must not be empty and must be ≤ 100 characters

**Deliverable:** Both validation functions (or class `__post_init__` methods) working correctly.

---

### Task 3 — CRUD Operations (20 points)

Implement these functions with JSON persistence:

```python
def load_data(filepath: str) -> dict:
    """Load {'categories': [...], 'transactions': [...]}.
    Return empty structure if file does not exist."""

def save_data(filepath: str, data: dict) -> None:
    """Save data dict to JSON file with indent=2."""

def add_category(data: dict, name: str, budget: float) -> None:
    """Add a new BudgetCategory. Raise ValueError if name already exists."""

def add_transaction(data: dict, dept: str, amount: float,
                    description: str, date: str | None = None) -> dict:
    """Add a Transaction. date defaults to today. Return the new transaction."""

def list_transactions(data: dict, department: str | None = None,
                      month: str | None = None) -> list[dict]:
    """Return filtered transactions. None = no filter."""

def delete_transaction(data: dict, transaction_id: int) -> bool:
    """Delete by ID. Return True if deleted, False if not found."""
```

Requirements:
- IDs must be auto-incrementing and never reused
- All writes must call `save_data()` immediately
- No bare `except` clauses anywhere

---

### Task 4 — Reporting (15 points)

Implement:

```python
def monthly_report(data: dict, month: str) -> None:
    """Print a formatted monthly variance report to stdout."""
```

The report must show, for each category:
- Monthly budget
- Actual spending in `month` (format: `YYYY-MM`)
- Variance (positive = under budget, shown as `+$X`)
- Percentage used
- An alert flag if spending exceeds `ALERT_THRESHOLD` × budget

**Expected output format:**
```
Budget Report — January 2024
=================================================================
Category         Budget          Actual        Variance  % Used
-----------------------------------------------------------------
Engineering      $15,000.00     $13,200.00    +$1,800.00   88.0%  ⚠️
Marketing         $8,000.00      $5,400.00    +$2,600.00   67.5%
Sales            $12,000.00     $14,100.00    -$2,100.00  117.5%  🔴
=================================================================
TOTAL            $35,000.00     $32,700.00    +$2,300.00   93.4%
```

- `⚠️` flag when `% used >= ALERT_THRESHOLD * 100` but ≤ 100%
- `🔴` flag when over budget (> 100%)

---

## PART B: Design Questions (20 points — 5 points each)

Answer each question in 3–5 sentences.

**Q1.** Your application currently stores data in a JSON file. A colleague suggests switching to
an SQLite database. Describe one concrete benefit and one concrete risk of making that change.
What would you change in the code structure to make the swap easier?

---

**Q2.** The `add_transaction` function currently raises `ValueError` for invalid input. In a
real application, multiple users might submit transactions through a web API at the same time.
What problem would this raise, and how would you handle validation errors in that context?

---

**Q3.** You are asked to add a feature: "email an alert to the finance team whenever a department
exceeds its budget." Describe where in the existing code you would add this, and why. Would you
modify the reporting function or add a separate function? Justify your choice.

---

**Q4.** The current `delete_transaction` function accepts an integer ID. A junior developer
suggests replacing it with `delete_all_transactions(department)` for convenience. Describe the
risk and what safeguard you would add before accepting that change.

---

## PART C: Code Review Task (20 points)

The following module has 4 issues. Identify each one, explain what is wrong, and write the corrected line(s).

```python
# budget_module.py — BUGGY VERSION FOR REVIEW

import json
import logging

logger = logging.getLogger("budget")

def load_budget(filepath):
    try:
        with open(filepath) as f:
            return json.load(f)
    except:                              # Line A
        return {}

def add_spend(record, amount, history=[]):  # Line B
    record["spent"] = record.get("spent", 0) + amount
    history.append({"amount": amount})
    return history

def get_average_spend(records):
    total = sum(r["spent"] for r in records)
    return total / len(records)           # Line C

def update_budget(filepath, data):
    f = open(filepath, "w")               # Line D
    json.dump(data, f, indent=2)
    f.close()
```

Identify all four issues (Lines A–D), explain each, and write the correct replacement code.

---

## Scoring Rubric

### Part A (60 points)

| Task | Points | Criteria |
|------|--------|----------|
| Task 1: Config & logging | 10 | Rotating handler, correct levels, env var loading, validation |
| Task 2: Data models | 15 | Both models, all validation rules, descriptive error messages |
| Task 3: CRUD | 20 | All 6 functions, correct persistence, auto-IDs, no bare excepts |
| Task 4: Reporting | 15 | Correct calculations, formatting, alert flags, totals row |

### Part B (20 points)

| Question | Points | Criteria |
|----------|--------|----------|
| Q1–Q4 | 5 each | Clear reasoning, technically accurate, shows awareness of trade-offs |

### Part C (20 points)

| Finding | Points | Criteria |
|---------|--------|----------|
| Each of Lines A–D | 5 each | Correctly identified, explained, and fixed |

### Grade bands

| Score | Outcome |
|-------|---------|
| 80–100 | Pass — move to Phase 19 |
| 65–79 | Near pass — review weak areas, then proceed |
| < 65 | Restudy Phase 18 lessons before continuing |

---

## Requirements Checklist

Before submitting, verify:
- [ ] Application runs with `python budget_cli.py` without errors
- [ ] Data persists between runs (exit and re-run — data should still be there)
- [ ] `budget.log` is created and contains log entries
- [ ] No bare `except:` or `except Exception: pass` anywhere
- [ ] Every `open()` call uses a `with` statement
- [ ] No hard-coded secrets or file paths (use env vars or constants at the top)
- [ ] All amounts display with 2 decimal places and comma separators

---

## Sample Expected Output

```
Budget Tracking CLI
===================
1. Add category
2. Record transaction
3. List transactions
4. Monthly report
5. Exit
Choice: 1

  Category name: Engineering
  Monthly budget: 15000
  ✓ Added category 'Engineering' ($15,000.00/month)

Choice: 2
  Categories: Engineering, Marketing, Sales
  Department: Engineering
  Amount: 3500
  Description: Cloud hosting — Q1
  ✓ Transaction #1 recorded — $3,500.00 to Engineering on 2024-01-10

Choice: 4
  Month (YYYY-MM): 2024-01
  
  Budget Report — January 2024
  =================================================================
  Category         Budget          Actual        Variance  % Used
  -----------------------------------------------------------------
  Engineering      $15,000.00      $3,500.00   +$11,500.00   23.3%
  =================================================================
  TOTAL            $15,000.00      $3,500.00   +$11,500.00   23.3%
```

---

## Part C — Answer Key

> Do not read until after you have completed the code review task.

---

**Line A** — Bare `except: return {}`

Issue: Catches every exception including `KeyboardInterrupt`, `SystemExit`, and programming
errors like `AttributeError`. File parsing errors are silently swallowed; the caller gets `{}`
with no indication that anything went wrong.

Fix:
```python
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        logger.warning("Could not load budget file %s: %s", filepath, exc)
        return {}
```

---

**Line B** — Mutable default argument `history=[]`

Issue: The list is created once when the module is loaded. Every call that does not pass
`history` explicitly shares the same object — entries accumulate across calls.

Fix:
```python
def add_spend(record, amount, history=None):
    if history is None:
        history = []
    record["spent"] = record.get("spent", 0) + amount
    history.append({"amount": amount})
    return history
```

---

**Line C** — Division by zero on empty list

Issue: `len(records)` is 0 when the list is empty, causing `ZeroDivisionError`.

Fix:
```python
def get_average_spend(records):
    if not records:
        return 0.0
    return sum(r["spent"] for r in records) / len(records)
```

---

**Line D** — File opened without context manager

Issue: If `json.dump` raises an exception (e.g. a value is not JSON-serialisable), `f.close()`
is never called. On Windows, this leaves a file lock; on all platforms, the file may be
truncated or corrupt.

Fix:
```python
def update_budget(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
```
