# 📝 Phase 18 — Advanced Exercises

> **Full Mini-Application Format:** Each exercise is a complete, runnable command-line application.
> Read the business requirements carefully before writing any code — design your data structures
> and module layout first. These are representative of real entry-level business Python work.
>
> Solutions: `../../solutions/advanced/solutions.md`

---

## Q1. ⭐⭐⭐ Invoice Management CLI

**Business context:** A small consulting firm needs a CLI tool to create and track client invoices,
mark them as paid, and report on outstanding (overdue) balances at month-end.

### Business Requirements

1. **Create** an invoice: client name, description, amount, due date
2. **List** all invoices with status (unpaid / paid / overdue)
3. **Mark paid**: update a specific invoice by ID
4. **Monthly summary**: total invoiced, total paid, total overdue for a given month
5. **Overdue alert**: any unpaid invoice past its due date shows `[OVERDUE]` in the list
6. Data persists in `invoices.json`

### Data Structure

```python
{
  "id": 1,
  "client": "Acme Corp",
  "description": "Website redesign — Phase 1",
  "amount": 4500.00,
  "due_date": "2024-01-31",
  "issued_date": "2024-01-10",
  "paid": false,
  "paid_date": null
}
```

### CLI Interface

```
Invoice Manager
===============
1. Create invoice
2. List invoices
3. Mark invoice paid
4. Monthly summary
5. Exit
```

### Expected `List invoices` output

```
ID  Client              Description                  Amount     Due Date    Status
--  ------------------  ---------------------------  ---------  ----------  --------
1   Acme Corp           Website redesign — Phase 1   $4,500.00  2024-01-31  OVERDUE
2   Bright Ltd          SEO audit                    $1,200.00  2024-03-15  Unpaid
3   Sunrise LLC         Branding package             $3,800.00  2024-02-28  Paid
```

### Expected `Monthly summary` output (for month `2024-01`)

```
Monthly Summary — January 2024
Invoiced:   $5,700.00  (2 invoices)
Paid:       $3,800.00  (1 invoice)
Overdue:    $4,500.00  (1 invoice)
Outstanding: $1,900.00
```

### Sample data to seed your app

```python
SEED_INVOICES = [
    {"client": "Acme Corp",    "description": "Website redesign",  "amount": 4500.00, "due_date": "2024-01-31"},
    {"client": "Bright Ltd",   "description": "SEO audit",          "amount": 1200.00, "due_date": "2024-03-15"},
    {"client": "Sunrise LLC",  "description": "Branding package",   "amount": 3800.00, "due_date": "2024-02-28"},
]
```

### Hints

- Use `datetime.date.today()` to determine if an invoice is overdue
- Store `issued_date` as today's date when creating
- `datetime.date.fromisoformat("2024-01-31")` parses date strings cleanly
- The monthly summary filters by `issued_date[:7] == "YYYY-MM"` (or `due_date` — pick one and document it)

---

## Q2. ⭐⭐⭐ Employee Attendance System

**Business context:** A small company tracks daily clock-in and clock-out times for employees.
HR needs daily summaries, weekly totals per employee, and automatic overtime flagging
(anything over 8 hours/day or 40 hours/week).

### Business Requirements

1. **Clock in**: record employee ID + current timestamp
2. **Clock out**: record employee ID + current timestamp (must have clocked in first)
3. **Daily summary**: show each employee's hours for a given date
4. **Weekly report**: show total hours per employee for a given week, flag overtime
5. **Export to CSV**: write the full attendance log to `attendance_export.csv`
6. Data persists in `attendance.json`

### Data Structure

```python
# One record per clock-in/clock-out pair:
{
  "id": 1,
  "employee_id": "EMP-0001",
  "date": "2024-01-15",
  "clock_in":  "08:45",
  "clock_out": "17:30",
  "hours": 8.75
}
```

### Expected CLI outputs

**Clock in:**
```
Employee EMP-0001 clocked IN at 09:00 on 2024-01-15
```

**Daily summary (2024-01-15):**
```
Daily Summary — 2024-01-15
Employee     Clock In   Clock Out   Hours   Overtime
-----------  ---------  ----------  ------  --------
EMP-0001     08:45      17:30       8.75    0.75 hrs
EMP-0002     09:00      17:00       8.00    —
EMP-0003     07:30      18:00      10.50    2.50 hrs
```

**Weekly report (week of 2024-01-15):**
```
Weekly Report — Week of 2024-01-15
Employee     Total Hrs   Overtime Hrs
-----------  ----------  ------------
EMP-0001     42.25       2.25
EMP-0002     38.00       —
EMP-0003     45.50       5.50
```

### Sample seed data

```python
SEED_ATTENDANCE = [
    {"employee_id": "EMP-0001", "date": "2024-01-15", "clock_in": "08:45", "clock_out": "17:30"},
    {"employee_id": "EMP-0002", "date": "2024-01-15", "clock_in": "09:00", "clock_out": "17:00"},
    {"employee_id": "EMP-0003", "date": "2024-01-15", "clock_in": "07:30", "clock_out": "18:00"},
    {"employee_id": "EMP-0001", "date": "2024-01-16", "clock_in": "08:30", "clock_out": "17:00"},
]
```

### Hints

- Parse `clock_in` and `clock_out` strings with `datetime.datetime.strptime(t, "%H:%M")`
- Hours = `(clock_out - clock_in).seconds / 3600`
- Daily overtime = `max(0, hours - 8)`, weekly overtime = `max(0, total_hours - 40)`
- Use `csv.DictWriter` with `fieldnames=["id", "employee_id", "date", "clock_in", "clock_out", "hours"]` for export

---

## Q3. ⭐⭐⭐ Departmental Budget Tracker with Alerts

**Business context:** Finance needs to track spending against monthly budgets for each department.
When a department exceeds 80% of its budget, an alert must be triggered. At month-end, a variance
report shows how much each department was over or under budget.

### Business Requirements

1. **Set up departments** with monthly budget allocations
2. **Record spending**: amount + description + department
3. **Check alerts**: after every transaction, print a warning if any department exceeds 80% of budget
4. **Variance report**: show each department's budget, actual spend, variance (+ = under, − = over)
5. **List transactions** for a department, filtered by month
6. Data persists in `budget_data.json`

### Data Structures

```python
# Departments
{"name": "Engineering",  "monthly_budget": 15000.00}
{"name": "Marketing",    "monthly_budget": 8000.00}
{"name": "Sales",        "monthly_budget": 12000.00}

# Transactions
{"id": 1, "date": "2024-01-10", "department": "Engineering",
 "amount": 3500.00, "description": "Cloud hosting — Q1"}
```

### Expected alert message

```
⚠️  BUDGET ALERT: Engineering has used $13,200.00 of $15,000.00 (88.0%) this month
```

### Expected variance report output

```
Budget Variance Report — January 2024
Department     Budget       Actual       Variance   % Used
-----------    ----------   ----------   ---------  ------
Engineering    $15,000.00   $13,200.00   +$1,800.00  88.0%  ⚠️ OVER 80%
Marketing       $8,000.00    $5,400.00   +$2,600.00  67.5%
Sales          $12,000.00   $14,100.00   -$2,100.00 117.5%  🔴 OVER BUDGET
```

### Sample seed data

```python
SEED_DEPARTMENTS = [
    {"name": "Engineering", "monthly_budget": 15000.00},
    {"name": "Marketing",   "monthly_budget": 8000.00},
    {"name": "Sales",       "monthly_budget": 12000.00},
]

SEED_TRANSACTIONS = [
    {"date": "2024-01-10", "department": "Engineering", "amount": 3500.00, "description": "Cloud hosting"},
    {"date": "2024-01-12", "department": "Marketing",   "amount": 2200.00, "description": "Ad campaign"},
    {"date": "2024-01-18", "department": "Engineering", "amount": 5800.00, "description": "Developer licences"},
    {"date": "2024-01-20", "department": "Sales",       "amount": 7500.00, "description": "Conference travel"},
    {"date": "2024-01-22", "department": "Engineering", "amount": 3900.00, "description": "Hardware refresh"},
    {"date": "2024-01-25", "department": "Marketing",   "amount": 3200.00, "description": "Design agency"},
    {"date": "2024-01-28", "department": "Sales",       "amount": 6600.00, "description": "Client entertainment"},
]
```

### Hints

- Store both departments and transactions in a single JSON file under separate keys
- `sum(t["amount"] for t in transactions if t["department"] == name and t["date"][:7] == month)`
- Variance is positive when under budget: `budget - actual`
- Check the 80% threshold immediately after adding any transaction

---

## Q4. ⭐⭐⭐ Sales Performance Reporter (CSV → HTML)

**Business context:** The sales director wants a one-click HTML report generated from a raw
sales CSV export. It must compute key metrics and produce a self-contained HTML file that can
be emailed or opened in any browser.

### Business Requirements

1. Read a sales CSV file and compute:
   - Total revenue and transaction count
   - Average deal size
   - Top performer (rep with highest total)
   - Best month (month with highest total)
   - Revenue by category (sorted highest to lowest)
   - Revenue by sales rep (sorted highest to lowest)
2. Output a self-contained `sales_report.html` file
3. If a prior-year CSV is provided, include a Year-on-Year (YoY) change percentage

### Input CSV format (`sales_2024.csv`)

```csv
date,rep,category,amount,region
2024-01-08,Alice,Software,3200,North
2024-01-15,Bob,Hardware,5800,South
2024-02-03,Alice,Services,2100,North
2024-02-19,Carol,Software,4400,East
2024-03-05,Bob,Hardware,6200,South
2024-03-12,Alice,Software,3800,North
2024-03-28,Carol,Services,1900,East
```

### Expected HTML report sections

The HTML must include:
- Header with report title and generation timestamp
- Key Metrics table (total revenue, count, average, top rep, best month)
- Revenue by Category table
- Revenue by Rep table
- A simple footer

### Expected console output when generating

```
Reading sales data from sales_2024.csv...
  7 transactions loaded
  Total revenue: $27,400.00
  Top performer: Bob ($12,000.00)
  Best month: 2024-03 ($11,900.00)
Report written to: sales_report.html
```

### Hints

- Use `csv.DictReader` to read the file; amounts are strings — convert with `float(row["amount"])`
- Build the HTML with regular string formatting — no template library needed
- For the HTML, a simple `<table>` with inline styles is self-contained and email-safe
- YoY: `(current - prior) / prior * 100` — only include if a prior-year file is provided as a second argument

---

## Q5. ⭐⭐⭐ Inventory Reorder System

**Business context:** A warehouse needs automatic purchase order generation. When any product's
stock level falls below its reorder point, the system must generate a purchase order with the
supplier details and send an email-ready text summary to the console.

### Business Requirements

1. **Load inventory** from `inventory.json` (products with stock levels and reorder points)
2. **Update stock**: record received shipments (+) or sales (−)
3. **Auto-check reorders**: after every stock update, check if any product needs reordering
4. **Generate purchase order**: for each under-stocked product, create a PO with a PO number,
   supplier, ordered quantity (reorder point × 2), and estimated delivery date (7 days from today)
5. **Save POs** to `purchase_orders.json`
6. **Print email-ready text** for each PO generated

### Data Structures

```python
# Product
{"sku": "LAPTOP-001", "name": "Business Laptop",  "supplier": "TechSupply Co",
 "supplier_email": "orders@techsupply.com",
 "stock": 8, "reorder_point": 10, "unit_cost": 899.00}

# Purchase Order
{"po_number": "PO-20240115-001",
 "generated_date": "2024-01-15",
 "estimated_delivery": "2024-01-22",
 "supplier": "TechSupply Co",
 "supplier_email": "orders@techsupply.com",
 "items": [
   {"sku": "LAPTOP-001", "name": "Business Laptop",
    "quantity": 20, "unit_cost": 899.00, "total": 17980.00}
 ],
 "total_value": 17980.00,
 "status": "pending"}
```

### Expected email-ready text output

```
======================================================
PURCHASE ORDER: PO-20240115-001
Generated:  2024-01-15
======================================================
To: orders@techsupply.com (TechSupply Co)

Please supply the following items:

  SKU          Description           Qty    Unit Cost    Total
  -----------  --------------------  -----  ----------   ----------
  LAPTOP-001   Business Laptop         20    $899.00     $17,980.00

  ORDER TOTAL:                                           $17,980.00

Estimated Delivery: 2024-01-22
======================================================
```

### Sample inventory seed data

```python
SEED_INVENTORY = [
    {"sku": "LAPTOP-001",  "name": "Business Laptop",  "supplier": "TechSupply Co",
     "supplier_email": "orders@techsupply.com",   "stock": 8,  "reorder_point": 10, "unit_cost": 899.00},
    {"sku": "MOUSE-002",   "name": "Wireless Mouse",   "supplier": "TechSupply Co",
     "supplier_email": "orders@techsupply.com",   "stock": 45, "reorder_point": 20, "unit_cost":  24.99},
    {"sku": "DESK-003",    "name": "Standing Desk",    "supplier": "OfficeFurn Ltd",
     "supplier_email": "orders@officefurn.com",   "stock": 3,  "reorder_point": 5,  "unit_cost": 450.00},
    {"sku": "CHAIR-004",   "name": "Ergonomic Chair",  "supplier": "OfficeFurn Ltd",
     "supplier_email": "orders@officefurn.com",   "stock": 12, "reorder_point": 8,  "unit_cost": 320.00},
]
```

### Hints

- Group items by supplier so each supplier gets a single PO (not one per product)
- PO number format: `f"PO-{datetime.date.today().strftime('%Y%m%d')}-{sequence:03d}"`
- Reorder quantity = `reorder_point * 2` — double the threshold to avoid frequent reorders
- A product needs reordering when `stock < reorder_point` (strictly less than, not equal)

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
