# 🗂️ Guided Project 02 — Data Import Tool

**Phase:** 06 — Error Handling
**Difficulty:** ⭐⭐ Intermediate
**Time:** ~60–90 minutes

---

## Project Goal

Build a robust CSV and JSON data importer that handles real-world file problems gracefully. Instead of crashing on bad data, it records every error, processes as many rows as possible, and prints a clear summary report at the end.

---

## Learning Objectives

By completing this project you will be able to:

1. Catch `FileNotFoundError` and `PermissionError` when reading files from disk
2. Handle `csv.Error` for structurally malformed CSV data
3. Catch `json.JSONDecodeError` for invalid JSON strings
4. Recover from `KeyError` when expected columns or fields are missing
5. Convert data types safely, catching `ValueError` and `TypeError` per row
6. Generate a structured summary report of successes and failures

---

## Prerequisites

- Completed Phase 06 Lessons 01–05
- Familiar with `try/except`, custom exceptions, and `finally`
- Know what a CSV and JSON file looks like

---

## How to Run

```bash
python data_import_tool.py
```

No external files needed — all sample data is defined as string constants inside the script. It runs anywhere, immediately.

---

## What You Will Build

Follow the comments inside `data_import_tool.py`. Each section is labelled **STEP N** and tells you exactly what to build next.

### Step 1 — ImportResult class

A data container that tracks the outcome of one import operation:
- `rows_processed` — total rows seen (good + bad)
- `successful` — rows that passed all checks
- `failed` — rows that failed for any reason
- `errors` — list of human-readable error messages
- `records` — list of valid, fully converted row dicts

### Step 2 — DataImporter.import_csv()

Reads a CSV string using `csv.DictReader` on an `io.StringIO` object (no temp files needed). For each row:
- Checks that `name`, `age`, and `salary` columns exist (`KeyError`)
- Converts `age` to `int` and `salary` to `float` (`ValueError`)
- Validates business rules: age must be non-negative, salary must be non-negative

### Step 3 — DataImporter.import_json()

Parses a JSON string. For each record in the array:
- Catches `json.JSONDecodeError` for completely invalid JSON syntax
- Checks that top-level value is a list and each element is a dict (`TypeError`)
- Checks for required fields (`KeyError`)
- Validates types and values (`TypeError`, `ValueError`)

### Step 4 — DataImporter.import_from_file()

Reads a real file from disk:
- Catches `FileNotFoundError` and `PermissionError`
- Routes `.csv` files to `import_csv()` and `.json` files to `import_json()`
- Raises `ValueError` for unsupported file extensions

### Step 5 — print_report()

Formats and prints the import summary: source name, rows processed, success count, failure count, and all error messages with a preview of valid records.

### Step 6 — main()

Runs all four demo scenarios automatically:
1. `SAMPLE_CSV` — five rows, three of which have deliberate errors
2. `SAMPLE_JSON` — three records, two with type/field errors
3. `BAD_JSON` — a completely unparseable JSON string
4. `import_from_file('nonexistent.csv')` — demonstrates `FileNotFoundError`

---

## Sample Expected Output

```
============================================================
DATA IMPORT TOOL — Phase 06 Error Handling Project
============================================================

────────────────────────────────────────────────────────────
Scenario 1: SAMPLE_CSV (mix of valid and invalid rows)
────────────────────────────────────────────────────────────

Import Report — SAMPLE_CSV
  Rows processed    : 5
  Successful        : 2
  Failed            : 3
  Errors:
    • Row 2: age conversion failed — 'invalid_age' is not a valid integer
    • Row 3: salary conversion failed — salary is missing (empty string)
    • Row 5: age must be non-negative, got -5
  Preview of valid records (2 shown):
    Alice      age=30    salary=$75,000.00
    Dave       age=35    salary=$90,000.00

────────────────────────────────────────────────────────────
Scenario 2: SAMPLE_JSON (mix of valid and invalid records)
────────────────────────────────────────────────────────────

Import Report — SAMPLE_JSON
  Rows processed    : 3
  Successful        : 1
  Failed            : 2
  Errors:
    • Row 2: salary must be numeric, got 'str' (value: 'not_a_number')
    • Row 3: missing field 'salary'
  Preview of valid records (1 shown):
    Frank      age=28    salary=$82,000.00

────────────────────────────────────────────────────────────
Scenario 3: BAD_JSON (unparseable JSON string)
────────────────────────────────────────────────────────────

Import Report — BAD_JSON
  Rows processed    : 0
  Successful        : 0
  Failed            : 0
  Errors:
    • JSON parse error: Expecting property name enclosed in double quotes ...

────────────────────────────────────────────────────────────
Scenario 4: import_from_file('nonexistent.csv')
────────────────────────────────────────────────────────────

Import Report — nonexistent.csv
  Rows processed    : 0
  Successful        : 0
  Failed            : 0
  Errors:
    • File not found: nonexistent.csv
```

---

## Extension Challenges

Once the base project works, try these:

1. Add a `min_salary` parameter that skips rows below the threshold (counted as skipped, not failed)
2. Write the successfully imported records to a new CSV file using `csv.DictWriter`
3. Add support for `.tsv` (tab-separated values) files — hint: `csv.DictReader` accepts a `delimiter` argument
4. Track *skipped* rows separately from *failed* rows in `ImportResult`

---

## Key Concepts Practiced

| Concept | Where Used |
|---------|-----------|
| `FileNotFoundError` | `import_from_file()` |
| `PermissionError` | `import_from_file()` |
| `csv.Error` | `import_csv()` |
| `json.JSONDecodeError` | `import_json()` |
| `KeyError` | Both import methods (missing columns) |
| `ValueError` | Both import methods (type conversion + range) |
| `TypeError` | `import_json()` (wrong JSON structure) |
| Summary reporting | `print_report()` |
| `io.StringIO` | Treating a string as a file |

---

## Next

**→ [Project 03 — Banking Simulator](../project-03-banking-simulator/README.md)**
