# Lesson 05 — Working with CSVs and Excel Files for Automation

**Phase:** 12 — Automation | **Time:** ~55 min

---

## Part 1: The csv Module — Reading and Writing

Python's built-in `csv` module handles comma-separated values without any
extra install. The `newline=""` parameter is required on Windows to prevent
the module from writing double blank lines between rows.

```python
import csv

# ── Writing ─────────────────────────────────────────────────────────────────
rows = [
    ["Product",   "Q1",  "Q2",  "Q3",  "Q4"],
    ["Laptop",   15000, 18200, 17100, 22300],
    ["Monitor",   8400,  9100,  8800, 10200],
    ["Keyboard",  3200,  3600,  3100,  4100],
]

with open("sales.csv", "w", newline="", encoding="utf-8-sig") as f:
    # utf-8-sig adds a BOM so Excel opens the file with the correct encoding
    writer = csv.writer(f)
    writer.writerows(rows)      # write all rows at once

# ── Reading ─────────────────────────────────────────────────────────────────
with open("sales.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    header = next(reader)       # consume the header row
    print("Columns:", header)
    for row in reader:
        # Every value is a string — convert numerics explicitly
        product = row[0]
        q1      = int(row[1])
        print(f"{product:12} Q1={q1:>6,}")
```

---

## Part 2: DictReader and DictWriter

`DictReader` maps each row to a dictionary keyed by the header names.
This is much safer than relying on column indices.

```python
import csv

# ── DictReader — each row is a dict ─────────────────────────────────────────
with open("sales.csv", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total = sum(int(row[q]) for q in ["Q1", "Q2", "Q3", "Q4"])
        print(f"{row['Product']:<12} annual total: {total:>8,}")

# ── DictWriter — write dicts to CSV ─────────────────────────────────────────
fieldnames = ["Product", "Q1", "Q2", "Q3", "Q4", "Annual"]
records = [
    {"Product": "Laptop",   "Q1": 15000, "Q2": 18200, "Q3": 17100, "Q4": 22300, "Annual": 72600},
    {"Product": "Monitor",  "Q1":  8400, "Q2":  9100, "Q3":  8800, "Q4": 10200, "Annual": 36500},
    {"Product": "Keyboard", "Q1":  3200, "Q2":  3600, "Q3":  3100, "Q4":  4100, "Annual": 14000},
]

with open("sales_totals.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()        # writes the column names as the first row
    writer.writerows(records)
```

---

## Part 3: CSV Options — Delimiters and Quoting

```python
import csv

# Tab-separated (TSV) — common export from databases
with open("data.tsv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows([["name", "score"], ["Alice", 95], ["Bob", 87]])

# Semicolon-separated — common in European locales where , is a decimal separator
with open("data_eu.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerows([["name", "score"], ["Alice", "9,5"], ["Bob", "8,7"]])

# Force quotes around every field to handle values that contain commas
with open("quoted.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["Product", "Description", "Price"])
    writer.writerow(["Laptop", "14-inch, i7, 16 GB RAM", 1299.99])
```

---

## Part 4: openpyxl — Creating and Reading Excel Files

```bash
pip install openpyxl
```

```python
from openpyxl import Workbook, load_workbook

# ── Create a new workbook ────────────────────────────────────────────────────
wb = Workbook()
ws = wb.active
ws.title = "Sales Report"

# Write individual cells — either by address or by row/column numbers
ws["A1"] = "Product"
ws["B1"] = "Q1 Sales"
ws.cell(row=2, column=1).value = "Laptop"
ws.cell(row=2, column=2).value = 15000

# Append whole rows (fast for bulk data)
data = [
    ("Product", "Q1",  "Q2",  "Q3",  "Q4"),
    ("Laptop",  15000, 18200, 17100, 22300),
    ("Monitor",  8400,  9100,  8800, 10200),
]
for row in data:
    ws.append(row)

wb.save("report.xlsx")

# ── Open an existing workbook ────────────────────────────────────────────────
wb2 = load_workbook("report.xlsx")
ws2 = wb2.active                        # first sheet
ws3 = wb2["Sales Report"]              # sheet by name

# Read a cell
print(ws2["A1"].value)
print(ws2.cell(row=2, column=3).value)

# Iterate rows (values_only=True returns plain values, not Cell objects)
for row in ws2.iter_rows(min_row=2, values_only=True):
    print(row)    # tuple: ('Laptop', 15000, 18200, ...)
```

---

## Part 5: Formatting with openpyxl

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active

# ── Style objects ─────────────────────────────────────────────────────────────
header_font = Font(bold=True, color="FFFFFF", size=12)
header_fill = PatternFill(fill_type="solid", fgColor="003366")
center      = Alignment(horizontal="center")

headers = ["Product", "Q1", "Q2", "Q3", "Q4", "Total"]
for col_idx, heading in enumerate(headers, start=1):
    cell            = ws.cell(row=1, column=col_idx, value=heading)
    cell.font       = header_font
    cell.fill       = header_fill
    cell.alignment  = center

# ── Number formatting ─────────────────────────────────────────────────────────
# Apply to all data cells (rows 2 onwards, numeric columns)
for row_idx in range(2, 6):
    for col_idx in range(2, len(headers) + 1):
        ws.cell(row=row_idx, column=col_idx).number_format = "#,##0"

# ── Auto-fit column width (approximation) ─────────────────────────────────────
for col in ws.columns:
    max_len = max((len(str(cell.value or "")) for cell in col), default=10)
    col_letter = get_column_letter(col[0].column)
    ws.column_dimensions[col_letter].width = max_len + 4

wb.save("formatted.xlsx")
```

---

## Part 6: Complete Example — CSV to Formatted Excel Report

```python
"""
csv_to_excel.py
Reads sales_data.csv, computes quarterly totals and averages,
and writes a formatted Excel report with bold headers, a totals row,
and number formatting.

Expected CSV columns: Product, Q1, Q2, Q3, Q4
"""

import csv
from pathlib import Path
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

CSV_INPUT = Path("data/sales_data.csv")
XLSX_OUT  = Path("reports/sales_report.xlsx")
QUARTERS  = ["Q1", "Q2", "Q3", "Q4"]


def load_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def build_report(rows: list[dict]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = f"Sales {date.today().year}"

    # ── Styles ────────────────────────────────────────────────────────────────
    h_font  = Font(bold=True, color="FFFFFF", size=11)
    h_fill  = PatternFill(fill_type="solid", fgColor="003366")
    t_font  = Font(bold=True)
    center  = Alignment(horizontal="center")
    num_fmt = "#,##0"

    # ── Header row ────────────────────────────────────────────────────────────
    headers = ["Product"] + QUARTERS + ["Total", "Average"]
    for col, heading in enumerate(headers, start=1):
        cell           = ws.cell(row=1, column=col, value=heading)
        cell.font      = h_font
        cell.fill      = h_fill
        cell.alignment = center

    # ── Data rows ─────────────────────────────────────────────────────────────
    for r, row in enumerate(rows, start=2):
        quarterly = [int(row.get(q, 0)) for q in QUARTERS]
        total     = sum(quarterly)
        average   = round(total / len(quarterly), 1)
        values    = [row["Product"]] + quarterly + [total, average]
        for col, val in enumerate(values, start=1):
            cell = ws.cell(row=r, column=col, value=val)
            if col > 1:
                cell.number_format = num_fmt

    # ── Totals row ────────────────────────────────────────────────────────────
    last_data_row = 1 + len(rows)
    totals_row    = last_data_row + 1
    ws.cell(row=totals_row, column=1, value="TOTAL").font = t_font

    for col in range(2, len(headers) + 1):
        col_letter = get_column_letter(col)
        formula_cell = ws.cell(
            row=totals_row,
            column=col,
            value=f"=SUM({col_letter}2:{col_letter}{last_data_row})",
        )
        formula_cell.font          = t_font
        formula_cell.number_format = num_fmt

    # ── Auto column width ─────────────────────────────────────────────────────
    for col in ws.columns:
        width = max(len(str(c.value or "")) for c in col) + 4
        ws.column_dimensions[get_column_letter(col[0].column)].width = width

    XLSX_OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(XLSX_OUT)
    print(f"Report saved → {XLSX_OUT.resolve()}")


if __name__ == "__main__":
    data = load_csv(CSV_INPUT)
    build_report(data)
```

---

## Part 7: pandas for Larger Datasets

For datasets with thousands of rows, or when you need grouping, filtering,
and pivoting, `pandas` is faster and more expressive than `csv` + `openpyxl`.

```python
import pandas as pd

# Read CSV into a DataFrame — one line
df = pd.read_csv("data/sales_data.csv")

# Add a computed column
df["Total"] = df[["Q1", "Q2", "Q3", "Q4"]].sum(axis=1)

# Quick stats
print(df.describe())
print(df.groupby("Region")["Total"].sum())

# Write to Excel — one line
df.to_excel("reports/pandas_report.xlsx", index=False, sheet_name="Sales")

# Read back
df2 = pd.read_excel("reports/pandas_report.xlsx", sheet_name="Sales")
```

Use `csv` + `openpyxl` when you need precise control over cell formatting,
formulas, or multi-sheet workbooks. Use `pandas` when the priority is data
transformation speed and conciseness.

---

## Practice Exercises

1. Write a script that reads a student grades CSV (columns: Name, Math,
   English, Science) using `csv.DictReader`. Compute each student's average
   across the three subjects and write the results to a new CSV file that
   adds an `Average` column, rounded to one decimal place.

2. Create an Excel workbook with `openpyxl` that has two sheets: "Raw Data"
   and "Summary". Write 10 rows of sales data on "Raw Data" and add SUM
   formulas on "Summary" that reference those rows.

3. Extend `csv_to_excel.py` to colour data cells: red fill
   (`fgColor="FF0000"`) when a quarterly value is below 5 000, and green
   fill (`fgColor="00AA00"`) when it is above 20 000. Use
   `openpyxl.styles.PatternFill` on each cell after writing its value.

4. Build a full pipeline combining Lessons 03, 04, and 05: schedule a weekly
   job that reads a CSV, generates an Excel report with `build_report()`,
   and emails it as an attachment using the `add_attachment()` function from
   Lesson 04.

---

## Next Lesson

**[Phase 13 → Data Analysis with pandas](../../phase-13-data-analysis/concepts/lesson-01-pandas-intro.md)**
