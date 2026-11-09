# Phase 19 — Advanced Exercises

> These exercises require architecture-level thinking.
> Plan your new design on paper before writing any code.
> Solutions: `../../solutions/advanced/solutions.md`

---

## Q1 — Break Up a God Object ⭐⭐⭐

`OrderManager` does everything: validates input, prices items, checks inventory, persists to the database, and sends email notifications. Any change to any of those five concerns touches this one class. Decompose it.

```python
import sqlite3
import smtplib
from typing import List, Dict

class OrderManager:
    DB_PATH   = "orders.db"
    SMTP_HOST = "smtp.company.com"
    TAX_RATE  = 0.08

    def place_order(self, customer_id: int, items: List[Dict]) -> int:
        # --- Validation ---
        if not items:
            raise ValueError("Order must have at least one item")
        if customer_id <= 0:
            raise ValueError("Invalid customer ID")
        for item in items:
            if item.get('quantity', 0) <= 0:
                raise ValueError(f"Invalid quantity for item {item.get('id')}")

        # --- Pricing (reads from DB inside the loop) ---
        subtotal = 0
        for item in items:
            conn = sqlite3.connect(self.DB_PATH)
            row  = conn.execute(
                "SELECT price FROM products WHERE id=?", (item['id'],)
            ).fetchone()
            conn.close()
            if not row:
                raise ValueError(f"Product {item['id']} not found")
            item['unit_price'] = row[0]
            subtotal += row[0] * item['quantity']
        tax   = subtotal * self.TAX_RATE
        total = subtotal + tax

        # --- Inventory check ---
        conn = sqlite3.connect(self.DB_PATH)
        for item in items:
            stock = conn.execute(
                "SELECT stock FROM products WHERE id=?", (item['id'],)
            ).fetchone()[0]
            if stock < item['quantity']:
                conn.close()
                raise ValueError(f"Insufficient stock for product {item['id']}")
        conn.close()

        # --- Persist ---
        conn   = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (customer_id, total, status) VALUES (?,?,?)",
            (customer_id, total, 'pending')
        )
        order_id = cursor.lastrowid
        for item in items:
            conn.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (item['quantity'], item['id'])
            )
        conn.commit()
        conn.close()

        # --- Notify ---
        conn = sqlite3.connect(self.DB_PATH)
        row  = conn.execute(
            "SELECT email FROM customers WHERE id=?", (customer_id,)
        ).fetchone()
        conn.close()
        customer_email = row[0]
        body = f"Your order #{order_id} has been placed. Total: ${total:.2f}"
        with smtplib.SMTP(self.SMTP_HOST) as server:
            server.sendmail("orders@company.com", customer_email, body)

        return order_id
```

**Refactoring goals:**
1. Extract `OrderValidator`, `PricingService`, `InventoryService`, `OrderRepository`, `CustomerRepository`, `NotificationService`.
2. Add an `OrderService` orchestrator that receives all six via `__init__` (constructor injection).
3. No class should reach into SQLite directly except the repository classes.
4. The refactored `OrderService.place_order` should be testable with mock objects for every dependency.

---

## Q2 — Implement Command Pattern for Undo/Redo ⭐⭐⭐

This text editor mutates its buffer directly. There is no history, so undo is impossible. Refactor to the Command pattern so every operation can be reversed.

```python
class TextEditor:
    def __init__(self):
        self.content = ""

    def insert(self, position: int, text: str) -> None:
        self.content = (
            self.content[:position] + text + self.content[position:]
        )

    def delete(self, start: int, end: int) -> None:
        self.content = self.content[:start] + self.content[end:]

    def replace(self, old: str, new: str) -> None:
        self.content = self.content.replace(old, new, 1)

    def get_content(self) -> str:
        return self.content
```

**What to build:**
1. An abstract `Command` base class with `execute() -> None` and `undo() -> None`.
2. `InsertCommand(editor, position, text)` — stores the position and inserted text so it can remove them on undo.
3. `DeleteCommand(editor, start, end)` — stores the deleted text so it can re-insert on undo.
4. `ReplaceCommand(editor, old, new)` — stores the original text so it can restore it on undo.
5. `TextEditor` gains a `history: list[Command]` stack. `do(cmd)` calls `execute()` and pushes. `undo()` pops and calls `undo()`. Add a `redo_stack` for bonus marks.

---

## Q3 — Fix Dependency Inversion ⭐⭐⭐

`ReportService` directly instantiates `MySQLDatabase` and `SmtpEmailSender`. It is welded to infrastructure. Introduce abstractions and inject the dependencies.

```python
import smtplib

class MySQLDatabase:
    def __init__(self, host, user, password, db):
        self.connection = None  # real connection setup omitted

    def query(self, sql, params=()):
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()


class SmtpEmailSender:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, to_addr, subject, body):
        with smtplib.SMTP(self.host, self.port) as server:
            server.sendmail(
                "reports@company.com", to_addr, f"{subject}\n\n{body}"
            )


class ReportService:
    def __init__(self):
        # High-level module directly creates low-level modules — DIP violation
        self.db     = MySQLDatabase("db.prod.internal", "app", "s3cr3t", "analytics")
        self.mailer = SmtpEmailSender("smtp.company.com", 587)

    def send_monthly_report(self, recipient: str):
        rows  = self.db.query("SELECT * FROM sales WHERE month = MONTH(NOW())")
        total = sum(r[2] for r in rows)
        body  = f"Monthly sales total: ${total:,.2f}\nRecords: {len(rows)}"
        self.mailer.send(recipient, "Monthly Report", body)
```

**What to fix:**
1. Define `Database` and `EmailSender` as `Protocol` (or ABC).
2. `ReportService.__init__` accepts a `Database` and an `EmailSender` as parameters.
3. `MySQLDatabase` and `SmtpEmailSender` implement the protocols without inheriting from them.
4. Show how a unit test would inject a `FakeDatabase` and a `FakeEmailSender` to test `send_monthly_report` without any network or database.

---

## Q4 — Refactor a Data Pipeline ⭐⭐⭐

This function processes sales records in one tangled block. Refactor it into composable, independently testable stages using generators.

```python
def process_sales_data(raw_records):
    results = []
    for record in raw_records:
        # Step 1: Skip incomplete records
        if ('amount' not in record
                or 'region' not in record
                or 'date' not in record):
            continue
        # Step 2: Parse and validate amount
        try:
            amount = float(record['amount'])
            if amount <= 0:
                continue
        except (ValueError, TypeError):
            continue
        # Step 3: Enrich with region code
        region_codes = {
            'north': 'NA', 'south': 'SA', 'east': 'EA', 'west': 'WA'
        }
        region_code = region_codes.get(record['region'].lower(), 'XX')
        # Step 4: Classify sales tier
        if amount > 10000:
            tier = 'platinum'
        elif amount > 5000:
            tier = 'gold'
        elif amount > 1000:
            tier = 'silver'
        else:
            tier = 'bronze'
        # Step 5: Assemble output record
        results.append({
            'date':        record['date'],
            'amount':      amount,
            'region_code': region_code,
            'tier':        tier,
        })
    return results
```

**What to build:**
1. Named generator functions: `filter_incomplete(records)`, `parse_amounts(records)`, `enrich_region(records)`, `classify_tier(records)`, `assemble_records(records)` — each takes an iterable and yields transformed items.
2. A `Pipeline` class that chains them fluently:
   ```python
   result = (Pipeline(raw_records)
             .through(filter_incomplete)
             .through(parse_amounts)
             .through(enrich_region)
             .through(classify_tier)
             .through(assemble_records)
             .to_list())
   ```
3. Each stage is testable in isolation with a small list of inputs.

---

## Q5 — Design a Plugin Architecture ⭐⭐⭐

Build a plugin system where new exporters can be added by dropping in a new class and registering it — no edits to the core engine required.

**Requirements:**
1. A `BaseExporter` ABC with:
   - A `name` class attribute (string identifier used for lookup)
   - An `export(data: list) -> str` abstract method
2. An `ExporterRegistry` class:
   - Stores a `dict` mapping name → exporter class
   - Provides a `register` decorator: `@registry.register`
   - Provides `get(name) -> BaseExporter` that raises `KeyError` for unknown names
3. Built-in plugins: `JsonExporter` and `MarkdownExporter`
4. An `ExportEngine(registry)` with `run(name, data) -> str`
5. A "third-party" plugin `YamlExporter` — registered with just `@registry.register`, zero changes to the engine

Show the complete implementation, then demonstrate all three exporters working.

---

## Q6 — Write a Complete `pyproject.toml` ⭐⭐⭐

You are packaging `reportcraft`, a library that generates PDF and HTML reports.

Project details:
- Package name: `reportcraft`, version `0.4.2`
- Python requires `>=3.10`
- Runtime dependencies: `jinja2>=3.1`, `weasyprint>=60.0`, `click>=8.1`
- Optional extras `[dev]`: `pytest>=7.4`, `ruff>=0.1`, `mypy>=1.5`
- Build backend: `hatchling`
- CLI entry point: command `reportcraft` → `reportcraft.cli:main`
- Classifiers: Development Status 4 - Beta, MIT license, Python 3.10 / 3.11 / 3.12
- Project URLs: homepage, repository, changelog

Write the complete, valid `pyproject.toml`. Include every mandatory section: `[build-system]`, `[project]`, `[project.optional-dependencies]`, `[project.scripts]`, `[project.urls]`.

---

## Q7 — Write a GitHub Actions CI Workflow ⭐⭐⭐

Write a complete `.github/workflows/ci.yml` for a Python project.

Requirements:
- **Triggers:** push to `main` or `develop`; pull requests targeting `main`
- **Job name:** `test`
- **Matrix:** Python 3.10, 3.11, 3.12 on `ubuntu-latest`
- **Steps (in order):**
  1. Checkout code — `actions/checkout@v4`
  2. Setup Python — `actions/setup-python@v5`
  3. Cache pip packages — `actions/cache@v4` (key includes OS + Python version + hash of `pyproject.toml`)
  4. Install dependencies — `pip install -e ".[dev]"`
  5. Lint — `ruff check .`
  6. Type check — `mypy src/`
  7. Test with coverage — `pytest --cov=src --cov-report=xml`
  8. Upload coverage to Codecov — `codecov/codecov-action@v4`

Write the complete YAML file.

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
