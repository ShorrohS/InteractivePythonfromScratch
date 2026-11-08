# Lesson 02 — Working with Business Data

**Phase:** 18 — Business Projects | **Time:** ~60 min | **Prerequisite:** Lesson 01

---

## Learning Objectives

- Read and write CSV files using `DictReader` and `DictWriter`
- Work with nested JSON structures using the `json` module
- Understand when to reach for `openpyxl` vs the stdlib CSV approach
- Apply validation patterns — type checks, range checks, required-field checks
- Clean raw data — strip whitespace, normalise dates, handle missing values
- Transform and aggregate data using `defaultdict` and comprehensions

---

## Part 1: The Sales Data Pipeline

A typical business data task follows four stages:

```
Raw file  →  Read  →  Validate & Clean  →  Transform  →  Output / Report
```

We'll use a **sales records** scenario throughout this lesson. Imagine a CSV exported from a CRM:

```
order_id,customer,region,product,quantity,unit_price,order_date
1001,Acme Corp,North,Widget A,10,25.99,2024-01-15
1002,Beta Ltd,South,Widget B,5,49.00,2024/01/16
1003,,East,Widget A,abc,25.99,2024-01-17
1004,Delta Inc,North,Widget C,-2,99.99,2024-01-18
1005,Echo SA,West,Widget B,3,49.00,
```

Notice the real-world messiness: wrong date format on row 2, missing customer on row 3, non-numeric quantity on row 3, negative quantity on row 4, missing date on row 5.

---

## Part 2: Reading CSV with DictReader

`csv.DictReader` maps each row to a dictionary keyed by the header row.

```python
import csv
from pathlib import Path

def read_sales_csv(filepath: str) -> list[dict]:
    """Read raw rows from a CSV file, returning a list of dicts."""
    records = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))   # dict() makes a plain mutable copy
    return records

raw = read_sales_csv("sales.csv")
print(raw[0])
# {'order_id': '1001', 'customer': 'Acme Corp', 'region': 'North',
#  'product': 'Widget A', 'quantity': '10', 'unit_price': '25.99',
#  'order_date': '2024-01-15'}
```

All values arrive as **strings** — validation and conversion are your responsibility.

---

## Part 3: Writing CSV with DictWriter

```python
import csv

def write_sales_csv(filepath: str, records: list[dict], fieldnames: list[str]) -> None:
    """Write cleaned records back to a CSV file."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

# Usage
clean_records = [...]   # validated and cleaned records
write_sales_csv(
    "sales_clean.csv",
    clean_records,
    fieldnames=["order_id", "customer", "region", "product",
                "quantity", "unit_price", "order_date"]
)
```

`extrasaction="ignore"` on `DictWriter` silently drops keys not in `fieldnames` — useful when your dict has extra computed fields you don't want in the output.

---

## Part 4: JSON with Nested Structures

JSON suits hierarchical data (e.g. an order with multiple line items).

```python
import json
from pathlib import Path

# Write — Python dict → JSON file
order = {
    "order_id": "1001",
    "customer": {
        "name": "Acme Corp",
        "region": "North",
        "contact": "alice@acme.com"
    },
    "items": [
        {"product": "Widget A", "quantity": 10, "unit_price": 25.99},
        {"product": "Widget B", "quantity": 2, "unit_price": 49.00},
    ],
    "order_date": "2024-01-15"
}

with open("order_1001.json", "w", encoding="utf-8") as f:
    json.dump(order, f, indent=2)

# Read — JSON file → Python dict
with open("order_1001.json", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded["customer"]["name"])   # Acme Corp

# Access nested list
for item in loaded["items"]:
    line_total = item["quantity"] * item["unit_price"]
    print(f"{item['product']}: ${line_total:.2f}")
# Widget A: $259.90
# Widget B: $98.00
```

Use `json.dumps()` / `json.loads()` when working with strings rather than files.

---

## Part 5: Excel Files — openpyxl Awareness

When stakeholders send `.xlsx` files, `openpyxl` is the standard tool:

```python
# pip install openpyxl
import openpyxl

wb = openpyxl.load_workbook("sales.xlsx")
ws = wb.active

headers = [cell.value for cell in ws[1]]   # first row = headers
for row in ws.iter_rows(min_row=2, values_only=True):
    record = dict(zip(headers, row))
    print(record)
```

For stdlib-only workflows, ask stakeholders to export to CSV — it is simpler, faster, and has no external dependency.

---

## Part 6: Data Validation

Validate before processing. Return errors rather than raising immediately so you can report all problems at once.

```python
from datetime import datetime

REQUIRED_FIELDS = {"order_id", "customer", "region", "product",
                   "quantity", "unit_price", "order_date"}

def validate_record(row: dict, line_number: int) -> list[str]:
    """Return a list of error messages, empty if valid."""
    errors = []

    # Required field check
    for field in REQUIRED_FIELDS:
        if not row.get(field, "").strip():
            errors.append(f"Line {line_number}: missing required field '{field}'")

    # Type check — quantity must be a positive integer
    qty_raw = row.get("quantity", "")
    try:
        qty = int(qty_raw)
        if qty <= 0:
            errors.append(f"Line {line_number}: quantity must be > 0 (got {qty})")
    except ValueError:
        errors.append(f"Line {line_number}: quantity is not an integer (got {qty_raw!r})")

    # Type check — unit_price must be a positive float
    price_raw = row.get("unit_price", "")
    try:
        price = float(price_raw)
        if price < 0:
            errors.append(f"Line {line_number}: unit_price must be >= 0 (got {price})")
    except ValueError:
        errors.append(f"Line {line_number}: unit_price is not a number (got {price_raw!r})")

    return errors


# Run validation over all rows
def validate_all(records: list[dict]) -> tuple[list[dict], list[str]]:
    valid, all_errors = [], []
    for i, record in enumerate(records, start=2):   # start=2: row 1 is headers
        errs = validate_record(record, i)
        if errs:
            all_errors.extend(errs)
        else:
            valid.append(record)
    return valid, all_errors
```

---

## Part 7: Cleaning Patterns

```python
from datetime import datetime

DATE_FORMATS = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]

def parse_date(raw: str) -> str | None:
    """Normalise a date string to ISO format YYYY-MM-DD."""
    raw = raw.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    return None   # unrecognised format


def clean_record(row: dict) -> dict:
    """Return a new dict with whitespace stripped, types converted, dates normalised."""
    return {
        "order_id":   row["order_id"].strip(),
        "customer":   row["customer"].strip().title(),   # "acme corp" → "Acme Corp"
        "region":     row["region"].strip().capitalize(),
        "product":    row["product"].strip(),
        "quantity":   int(row["quantity"].strip()),
        "unit_price": float(row["unit_price"].strip()),
        "order_date": parse_date(row["order_date"]),
        "line_total": round(int(row["quantity"]) * float(row["unit_price"]), 2),
    }


def clean_all(valid_records: list[dict]) -> list[dict]:
    return [clean_record(r) for r in valid_records]
```

---

## Part 8: Transformation — Aggregation and Grouping

`collections.defaultdict` makes grouping concise.

```python
from collections import defaultdict

def regional_summary(records: list[dict]) -> dict:
    """Aggregate total revenue and order count per region."""
    totals = defaultdict(lambda: {"orders": 0, "revenue": 0.0})

    for rec in records:
        region = rec["region"]
        totals[region]["orders"] += 1
        totals[region]["revenue"] += rec["line_total"]

    return dict(totals)


def top_products(records: list[dict], n: int = 3) -> list[tuple]:
    """Return the top N products by total quantity sold."""
    qty_by_product = defaultdict(int)
    for rec in records:
        qty_by_product[rec["product"]] += rec["quantity"]

    return sorted(qty_by_product.items(), key=lambda x: x[1], reverse=True)[:n]


# --- Full pipeline ---
raw = read_sales_csv("sales.csv")
valid, errors = validate_all(raw)

if errors:
    print("Validation errors found:")
    for err in errors:
        print(f"  ⚠  {err}")

cleaned = clean_all(valid)
summary = regional_summary(cleaned)
top = top_products(cleaned)

print("\nRegional Revenue Summary:")
for region, data in sorted(summary.items()):
    print(f"  {region:<10} {data['orders']:>3} orders  ${data['revenue']:>9,.2f}")

print("\nTop Products by Quantity:")
for product, qty in top:
    print(f"  {product:<15} {qty:>5} units")

write_sales_csv("sales_clean.csv", cleaned,
                fieldnames=["order_id","customer","region","product",
                            "quantity","unit_price","order_date","line_total"])
print("\nClean file written: sales_clean.csv")
```

---

## Key Takeaways

- `DictReader` / `DictWriter` are the stdlib workhorses for CSV — no extra dependencies needed
- All CSV values arrive as strings; always convert and validate before using them as numbers or dates
- Collect all validation errors before rejecting input — it gives users one actionable error report
- Normalise data (strip, capitalise, parse dates) in a dedicated cleaning step, separate from validation
- `defaultdict` removes boilerplate when building aggregations — no `if key not in dict` guards needed

---

## What's Next

**[Lesson 03 → Production-Quality Python](lesson-03-production-quality-python.md)**

We add the layers that turn working code into production-ready code: structured logging, environment-based configuration, a custom exception hierarchy, and retry logic.
