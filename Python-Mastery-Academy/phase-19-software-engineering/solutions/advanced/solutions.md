# ✅ Phase 19 — Advanced Solutions

> Each solution includes the refactored code, an explanation of every pattern applied, and a note on why the new architecture is better than the original.

---

## Q1 — Break Up a God Object

### What was wrong

`OrderManager.place_order` touched five distinct concerns in one method:
validation → pricing (with DB reads inside a loop) → inventory → persistence → email notification. It opened raw SQLite connections in multiple places and was untestable without a real database and SMTP server.

### Refactored architecture

```
OrderService (orchestrator)
├── OrderValidator
├── PricingService ──────► ProductRepository
├── InventoryService ────► ProductRepository
├── OrderRepository
├── CustomerRepository
└── NotificationService
```

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
import sqlite3


# ── Domain objects ──────────────────────────────────────────────────

@dataclass
class OrderItem:
    product_id: int
    quantity: int
    unit_price: float = 0.0


@dataclass
class Order:
    customer_id: int
    items: List[OrderItem]
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    order_id: Optional[int] = None


# ── Abstract interfaces ──────────────────────────────────────────────

class ProductRepository(ABC):
    @abstractmethod
    def get_price(self, product_id: int) -> float: ...
    @abstractmethod
    def get_stock(self, product_id: int) -> int: ...
    @abstractmethod
    def decrement_stock(self, product_id: int, qty: int) -> None: ...


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> int: ...   # returns new order_id


class CustomerRepository(ABC):
    @abstractmethod
    def get_email(self, customer_id: int) -> str: ...


class NotificationService(ABC):
    @abstractmethod
    def order_placed(self, email: str, order_id: int, total: float) -> None: ...


# ── Focused service classes ──────────────────────────────────────────

class OrderValidator:
    """Validates raw order input before any processing."""

    def validate(self, customer_id: int, items: List[dict]) -> None:
        if not items:
            raise ValueError("Order must have at least one item")
        if customer_id <= 0:
            raise ValueError("Invalid customer ID")
        for item in items:
            if item.get('quantity', 0) <= 0:
                raise ValueError(f"Invalid quantity for item {item.get('id')}")


class PricingService:
    """Looks up prices and computes order totals."""

    TAX_RATE = 0.08

    def __init__(self, products: ProductRepository) -> None:
        self.products = products

    def price_order(self, items: List[dict]) -> tuple[List[OrderItem], float, float, float]:
        order_items = []
        subtotal = 0.0
        for raw in items:
            price = self.products.get_price(raw['id'])
            oi = OrderItem(product_id=raw['id'], quantity=raw['quantity'], unit_price=price)
            order_items.append(oi)
            subtotal += price * raw['quantity']
        tax   = subtotal * self.TAX_RATE
        total = subtotal + tax
        return order_items, subtotal, tax, total


class InventoryService:
    """Checks and reserves stock."""

    def __init__(self, products: ProductRepository) -> None:
        self.products = products

    def check_and_reserve(self, items: List[OrderItem]) -> None:
        for item in items:
            stock = self.products.get_stock(item.product_id)
            if stock < item.quantity:
                raise ValueError(f"Insufficient stock for product {item.product_id}")
        for item in items:
            self.products.decrement_stock(item.product_id, item.quantity)


# ── Orchestrator ─────────────────────────────────────────────────────

class OrderService:
    """Wires together all order-related services. Contains no business logic."""

    def __init__(
        self,
        validator:     OrderValidator,
        pricing:       PricingService,
        inventory:     InventoryService,
        order_repo:    OrderRepository,
        customer_repo: CustomerRepository,
        notifier:      NotificationService,
    ) -> None:
        self.validator     = validator
        self.pricing       = pricing
        self.inventory     = inventory
        self.order_repo    = order_repo
        self.customer_repo = customer_repo
        self.notifier      = notifier

    def place_order(self, customer_id: int, items: List[dict]) -> int:
        self.validator.validate(customer_id, items)

        order_items, subtotal, tax, total = self.pricing.price_order(items)
        self.inventory.check_and_reserve(order_items)

        order = Order(
            customer_id=customer_id,
            items=order_items,
            subtotal=subtotal,
            tax=tax,
            total=total,
        )
        order_id = self.order_repo.save(order)

        email = self.customer_repo.get_email(customer_id)
        self.notifier.order_placed(email, order_id, total)
        return order_id
```

### Why this architecture is better

- **Testability.** Every dependency is an ABC. In tests, inject `FakeProductRepository`, `FakeOrderRepository`, etc. No SQLite or SMTP needed.
- **Single reason to change.** Tax rate change? Edit `PricingService` only. Email template change? Edit `NotificationService` only.
- **No DB connections leaking out of repositories.** The concrete SQLite implementations (not shown) live behind the interfaces and are invisible to the orchestrator.
- **The orchestrator reads like a process spec** — validate → price → check stock → save → notify. No SQL or SMTP details obscure the flow.

---

## Q2 — Implement Command Pattern for Undo/Redo

### Refactored

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class Command(ABC):
    """Every editor operation implements execute and undo."""

    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


class InsertCommand(Command):
    def __init__(self, editor: TextEditor, position: int, text: str) -> None:
        self._editor   = editor
        self._position = position
        self._text     = text

    def execute(self) -> None:
        c = self._editor.content
        self._editor.content = c[:self._position] + self._text + c[self._position:]

    def undo(self) -> None:
        c   = self._editor.content
        end = self._position + len(self._text)
        self._editor.content = c[:self._position] + c[end:]


class DeleteCommand(Command):
    def __init__(self, editor: TextEditor, start: int, end: int) -> None:
        self._editor        = editor
        self._start         = start
        self._end           = end
        self._deleted_text  = ""   # filled on execute

    def execute(self) -> None:
        c = self._editor.content
        self._deleted_text   = c[self._start:self._end]
        self._editor.content = c[:self._start] + c[self._end:]

    def undo(self) -> None:
        c = self._editor.content
        self._editor.content = (
            c[:self._start] + self._deleted_text + c[self._start:]
        )


class ReplaceCommand(Command):
    def __init__(self, editor: TextEditor, old: str, new: str) -> None:
        self._editor      = editor
        self._old         = old
        self._new         = new
        self._replaced_at = -1   # filled on execute

    def execute(self) -> None:
        c = self._editor.content
        self._replaced_at    = c.find(self._old)
        if self._replaced_at == -1:
            return
        self._editor.content = c.replace(self._old, self._new, 1)

    def undo(self) -> None:
        if self._replaced_at == -1:
            return
        c   = self._editor.content
        end = self._replaced_at + len(self._new)
        self._editor.content = (
            c[:self._replaced_at] + self._old + c[end:]
        )


class TextEditor:
    def __init__(self) -> None:
        self.content    = ""
        self._history:  list[Command] = []
        self._redo_stack: list[Command] = []

    def do(self, cmd: Command) -> None:
        cmd.execute()
        self._history.append(cmd)
        self._redo_stack.clear()   # new action invalidates redo history

    def undo(self) -> None:
        if not self._history:
            return
        cmd = self._history.pop()
        cmd.undo()
        self._redo_stack.append(cmd)

    def redo(self) -> None:
        if not self._redo_stack:
            return
        cmd = self._redo_stack.pop()
        cmd.execute()
        self._history.append(cmd)

    def get_content(self) -> str:
        return self.content


# --- Demo ---
# editor = TextEditor()
# editor.do(InsertCommand(editor, 0, "Hello, World"))
# editor.do(ReplaceCommand(editor, "World", "Python"))
# print(editor.get_content())   # "Hello, Python"
# editor.undo()
# print(editor.get_content())   # "Hello, World"
# editor.redo()
# print(editor.get_content())   # "Hello, Python"
```

### Why this architecture is better

- **Each command is self-contained.** It stores everything needed to reverse itself. The editor doesn't need to know the internals of any operation.
- **Open/Closed.** Adding a `FormatCommand` (bold, italic) means a new class — zero changes to `TextEditor`.
- **Redo is trivial** once you have history stacks. Clearing the redo stack on new actions is the standard behaviour (matches every text editor you've used).
- **Testable in isolation.** You can create a `TextEditor`, call `execute()` on a single command, and inspect `content` — no UI required.

---

## Q3 — Fix Dependency Inversion

**Principle: Dependency Inversion Principle (DIP)**
*High-level modules should not depend on low-level modules. Both should depend on abstractions.*

### Refactored

```python
from __future__ import annotations
from typing import Protocol, runtime_checkable


# ── Abstractions (the "interfaces" both sides depend on) ─────────────

@runtime_checkable
class Database(Protocol):
    def query(self, sql: str, params: tuple = ()) -> list: ...


@runtime_checkable
class EmailSender(Protocol):
    def send(self, to_addr: str, subject: str, body: str) -> None: ...


# ── Concrete implementations (low-level modules) ─────────────────────

class MySQLDatabase:
    """Implements Database protocol using a real MySQL connection."""

    def __init__(self, host: str, user: str, password: str, db: str) -> None:
        self.connection = None  # real setup omitted

    def query(self, sql: str, params: tuple = ()) -> list:
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()


class SmtpEmailSender:
    """Implements EmailSender protocol using SMTP."""

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def send(self, to_addr: str, subject: str, body: str) -> None:
        import smtplib
        with smtplib.SMTP(self.host, self.port) as server:
            server.sendmail(
                "reports@company.com", to_addr, f"{subject}\n\n{body}"
            )


# ── High-level module depends on abstractions, not concrete classes ──

class ReportService:
    """Generates and delivers reports. Never imports MySQL or SMTP."""

    def __init__(self, db: Database, mailer: EmailSender) -> None:
        self.db     = db
        self.mailer = mailer

    def send_monthly_report(self, recipient: str) -> None:
        rows  = self.db.query("SELECT * FROM sales WHERE month = MONTH(NOW())")
        total = sum(r[2] for r in rows)
        body  = f"Monthly sales total: ${total:,.2f}\nRecords: {len(rows)}"
        self.mailer.send(recipient, "Monthly Report", body)


# ── Production wiring (done by the caller, not by ReportService) ─────
# db      = MySQLDatabase("db.prod.internal", "app", "s3cr3t", "analytics")
# mailer  = SmtpEmailSender("smtp.company.com", 587)
# service = ReportService(db, mailer)

# ── Test wiring (no real DB or SMTP needed) ──────────────────────────
# class FakeDatabase:
#     def query(self, sql, params=()):
#         return [(1, "2024-01", 4500.00), (2, "2024-01", 3200.00)]
#
# class FakeEmailSender:
#     def __init__(self): self.sent = []
#     def send(self, to, subject, body): self.sent.append((to, subject, body))
#
# fake_db     = FakeDatabase()
# fake_mailer = FakeEmailSender()
# service     = ReportService(fake_db, fake_mailer)
# service.send_monthly_report("boss@company.com")
# assert fake_mailer.sent[0][0] == "boss@company.com"
```

### Why this architecture is better

`Protocol` (PEP 544, structural subtyping) means `MySQLDatabase` doesn't have to inherit from `Database` — it just needs to implement the right methods. This is Python's idiomatic way to express DIP without forcing inheritance hierarchies.

`ReportService` now contains pure business logic. The test snippet shows exactly how to verify that logic without a database or network: inject doubles, assert on the fake's `sent` list.

---

## Q4 — Refactor a Data Pipeline

### Refactored

```python
from typing import Iterator, Callable, TypeVar

Record = dict
T = TypeVar('T')

REGION_CODES = {
    'north': 'NA', 'south': 'SA', 'east': 'EA', 'west': 'WA'
}

TIER_THRESHOLDS = [
    (10_000, 'platinum'),
    ( 5_000, 'gold'),
    ( 1_000, 'silver'),
    (     0, 'bronze'),
]


# ── Individual pipeline stages ────────────────────────────────────────

def filter_incomplete(records: Iterator[Record]) -> Iterator[Record]:
    """Drop records missing required fields."""
    required = {'amount', 'region', 'date'}
    for r in records:
        if required.issubset(r):
            yield r


def parse_amounts(records: Iterator[Record]) -> Iterator[Record]:
    """Parse 'amount' to float; drop records with invalid or non-positive values."""
    for r in records:
        try:
            amount = float(r['amount'])
        except (ValueError, TypeError):
            continue
        if amount > 0:
            yield {**r, 'amount': amount}


def enrich_region(records: Iterator[Record]) -> Iterator[Record]:
    """Translate region name to a two-letter code."""
    for r in records:
        code = REGION_CODES.get(r['region'].lower(), 'XX')
        yield {**r, 'region_code': code}


def classify_tier(records: Iterator[Record]) -> Iterator[Record]:
    """Add a sales tier label based on amount."""
    for r in records:
        tier = next(
            label for threshold, label in TIER_THRESHOLDS
            if r['amount'] > threshold
        )
        yield {**r, 'tier': tier}


def assemble_records(records: Iterator[Record]) -> Iterator[Record]:
    """Keep only the output fields."""
    for r in records:
        yield {
            'date':        r['date'],
            'amount':      r['amount'],
            'region_code': r['region_code'],
            'tier':        r['tier'],
        }


# ── Pipeline class ────────────────────────────────────────────────────

class Pipeline:
    """Chains generator-based transformation stages."""

    def __init__(self, source) -> None:
        self._source = iter(source)

    def through(self, stage: Callable[[Iterator], Iterator]) -> 'Pipeline':
        self._source = stage(self._source)
        return self

    def to_list(self) -> list:
        return list(self._source)


# ── Usage ─────────────────────────────────────────────────────────────

def process_sales_data(raw_records: list) -> list:
    return (
        Pipeline(raw_records)
        .through(filter_incomplete)
        .through(parse_amounts)
        .through(enrich_region)
        .through(classify_tier)
        .through(assemble_records)
        .to_list()
    )
```

### Why this architecture is better

- **Each stage is independently testable.** `test_parse_amounts` passes in a small list and verifies the output without running any other stage.
- **Generators are lazy.** The pipeline processes one record at a time through all stages without building intermediate lists. For large files this is memory-efficient.
- **Adding a stage** (e.g., `normalise_dates`) means one new function and one `.through(normalise_dates)` call — zero changes to existing stages.
- **The `Pipeline` class** captures the composability pattern and gives calling code a clean, readable API.

---

## Q5 — Design a Plugin Architecture

### Refactored

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type


# ── Core infrastructure ───────────────────────────────────────────────

class BaseExporter(ABC):
    name: str   # subclasses set this as a class attribute

    @abstractmethod
    def export(self, data: list) -> str: ...


class ExporterRegistry:
    """Maintains a name → class mapping and provides a registration decorator."""

    def __init__(self) -> None:
        self._registry: dict[str, Type[BaseExporter]] = {}

    def register(self, cls: Type[BaseExporter]) -> Type[BaseExporter]:
        """Decorator that adds cls to the registry under cls.name."""
        self._registry[cls.name] = cls
        return cls

    def get(self, name: str) -> BaseExporter:
        cls = self._registry.get(name)
        if cls is None:
            raise KeyError(f"No exporter registered for '{name}'")
        return cls()

    @property
    def available(self) -> list[str]:
        return list(self._registry.keys())


registry = ExporterRegistry()


class ExportEngine:
    """Looks up and runs exporters by name. Has no knowledge of any specific exporter."""

    def __init__(self, reg: ExporterRegistry) -> None:
        self._registry = reg

    def run(self, name: str, data: list) -> str:
        exporter = self._registry.get(name)
        return exporter.export(data)


# ── Built-in plugins ──────────────────────────────────────────────────

@registry.register
class JsonExporter(BaseExporter):
    name = 'json'

    def export(self, data: list) -> str:
        import json
        return json.dumps(data, indent=2)


@registry.register
class MarkdownExporter(BaseExporter):
    name = 'markdown'

    def export(self, data: list) -> str:
        if not data:
            return ""
        headers = ' | '.join(data[0].keys())
        sep     = ' | '.join('---' for _ in data[0])
        rows    = '\n'.join(' | '.join(str(v) for v in r.values()) for r in data)
        return f"| {headers} |\n| {sep} |\n" + '\n'.join(f"| {r} |" for r in rows.split('\n'))


# ── Third-party plugin — zero edits to the engine ─────────────────────

@registry.register
class YamlExporter(BaseExporter):
    name = 'yaml'

    def export(self, data: list) -> str:
        import yaml   # pip install pyyaml
        return yaml.dump(data, default_flow_style=False)


# ── Demo ──────────────────────────────────────────────────────────────

# engine = ExportEngine(registry)
# sample = [{'name': 'Alice', 'score': 95}, {'name': 'Bob', 'score': 87}]
# print(engine.run('json',     sample))
# print(engine.run('markdown', sample))
# print(engine.run('yaml',     sample))
# print(registry.available)   # ['json', 'markdown', 'yaml']
```

### Why this architecture is better

- **`ExportEngine` never imports any exporter.** It asks the registry for one by name. You can deploy a new format as a separate package that registers itself on import.
- **The `@registry.register` decorator** is the only coupling a plugin needs — it doesn't inherit from anything in the engine.
- **Discovery is trivial** (`registry.available`), which enables building dynamic menus or CLI help text.

---

## Q6 — Complete `pyproject.toml`

```toml
[build-system]
requires      = ["hatchling"]
build-backend = "hatchling.build"

[project]
name        = "reportcraft"
version     = "0.4.2"
description = "A library for generating PDF and HTML reports"
readme      = "README.md"
license     = { text = "MIT" }
requires-python = ">=3.10"

dependencies = [
    "jinja2>=3.1",
    "weasyprint>=60.0",
    "click>=8.1",
]

classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "ruff>=0.1",
    "mypy>=1.5",
]

[project.scripts]
reportcraft = "reportcraft.cli:main"

[project.urls]
Homepage  = "https://reportcraft.dev"
Repository = "https://github.com/example/reportcraft"
Changelog  = "https://github.com/example/reportcraft/blob/main/CHANGELOG.md"
```

**Key points:**
- `[build-system]` is mandatory — it tells pip which tool builds the wheel.
- `requires-python` uses PEP 440 version specifiers.
- Optional dependencies group (`[dev]`) installs with `pip install reportcraft[dev]`.
- `[project.scripts]` generates a `reportcraft` executable that calls `reportcraft.cli:main`.
- Classifiers are from the PyPI classifier taxonomy — they affect search and filtering on PyPI.

---

## Q7 — GitHub Actions CI Workflow

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    name: "Python ${{ matrix.python-version }}"
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache pip packages
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('pyproject.toml') }}
          restore-keys: |
            ${{ runner.os }}-pip-${{ matrix.python-version }}-
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Lint with ruff
        run: ruff check .

      - name: Type check with mypy
        run: mypy src/

      - name: Run tests with coverage
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: false
```

**Key points:**
- `fail-fast: false` lets all matrix jobs complete even if one fails — useful for seeing which Python versions break.
- The cache key includes a hash of `pyproject.toml` so the cache is invalidated when dependencies change.
- `pip install -e ".[dev]"` installs the package in editable mode with dev extras (pytest, ruff, mypy).
- `fail_ci_if_error: false` on Codecov means a Codecov outage won't break your CI build.

---

> **Exercises:** → [../../exercises/advanced/exercises.md](../../exercises/advanced/exercises.md)
