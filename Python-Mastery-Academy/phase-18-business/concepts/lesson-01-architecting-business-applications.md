# Lesson 01 — Architecting Business Applications

**Phase:** 18 — Business Projects | **Time:** ~60 min | **Prerequisite:** Phase 17 — Advanced Python

---

## Learning Objectives

- Understand the difference between flat layout and src layout for Python projects
- Organise a multi-module business application into logical packages
- Use `__init__.py` to control what a package exposes
- Apply the MVC (Model-View-Controller) pattern with real Python classes
- Manage environment-specific configuration using `configparser`

---

## Part 1: Flat Layout vs Src Layout

Two conventions exist for structuring a Python project.

**Flat layout** — code sits at the project root:

```
invoicing-system/
├── models.py
├── views.py
├── controllers.py
├── config.py
├── tests/
└── README.md
```

Simple to start with, but packages collide with test runners as projects grow.

**Src layout** — code lives inside a `src/` directory:

```
invoicing-system/
├── src/
│   └── invoicing/
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── invoice.py
│       │   └── customer.py
│       ├── views/
│       │   ├── __init__.py
│       │   └── invoice_view.py
│       ├── controllers/
│       │   ├── __init__.py
│       │   └── invoice_controller.py
│       └── config.py
├── tests/
│   └── test_invoice.py
├── pyproject.toml
└── README.md
```

**Prefer src layout** for anything beyond a small script. It prevents the project root being importable accidentally and makes packaging straightforward.

---

## Part 2: `__init__.py` and Package Imports

`__init__.py` marks a directory as a Python package and controls its public API.

```python
# src/invoicing/__init__.py

# Re-export the things callers actually need
from invoicing.models.invoice import Invoice
from invoicing.models.customer import Customer
from invoicing.controllers.invoice_controller import InvoiceController

__version__ = "1.0.0"
__all__ = ["Invoice", "Customer", "InvoiceController"]
```

With this in place, callers can write clean imports:

```python
# Clean — one import line, no internal paths exposed
from invoicing import Invoice, Customer, InvoiceController

# Without the __init__.py re-exports the caller would need:
from invoicing.models.invoice import Invoice          # leaks internals
from invoicing.controllers.invoice_controller import InvoiceController
```

Use `__all__` to declare the official surface area of your package.

---

## Part 3: MVC Pattern in Python

MVC separates three responsibilities:

| Layer | Responsibility | Python artefact |
|-------|---------------|-----------------|
| **Model** | Data and business rules | dataclass / plain class |
| **View** | Presentation / formatting | class with render methods |
| **Controller** | Wires Model ↔ View, handles user input | class with action methods |

### Model

```python
# src/invoicing/models/invoice.py
from dataclasses import dataclass, field
from datetime import date
from typing import List

@dataclass
class LineItem:
    description: str
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Invoice:
    invoice_id: str
    customer_name: str
    issue_date: date
    line_items: List[LineItem] = field(default_factory=list)

    def add_item(self, description: str, quantity: int, unit_price: float) -> None:
        self.line_items.append(LineItem(description, quantity, unit_price))

    @property
    def subtotal(self) -> float:
        return sum(item.total for item in self.line_items)

    @property
    def tax(self) -> float:
        return round(self.subtotal * 0.10, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax, 2)
```

### View

```python
# src/invoicing/views/invoice_view.py

class InvoiceView:
    """Formats an Invoice for display — knows nothing about storage."""

    def render(self, invoice) -> str:
        lines = [
            f"{'=' * 50}",
            f"  INVOICE #{invoice.invoice_id}",
            f"  Customer: {invoice.customer_name}",
            f"  Date:     {invoice.issue_date}",
            f"{'─' * 50}",
            f"  {'Description':<25} {'Qty':>5} {'Unit':>8} {'Total':>9}",
            f"{'─' * 50}",
        ]
        for item in invoice.line_items:
            lines.append(
                f"  {item.description:<25} {item.quantity:>5} "
                f"{item.unit_price:>8.2f} {item.total:>9.2f}"
            )
        lines += [
            f"{'─' * 50}",
            f"  {'Subtotal':>40} {invoice.subtotal:>9.2f}",
            f"  {'Tax (10%)':>40} {invoice.tax:>9.2f}",
            f"  {'TOTAL':>40} {invoice.total:>9.2f}",
            f"{'=' * 50}",
        ]
        return "\n".join(lines)
```

### Controller

```python
# src/invoicing/controllers/invoice_controller.py
from datetime import date
from invoicing.models.invoice import Invoice
from invoicing.views.invoice_view import InvoiceView

class InvoiceController:
    """Handles invoice creation workflow."""

    def __init__(self):
        self._view = InvoiceView()
        self._invoices: dict[str, Invoice] = {}
        self._counter = 1

    def create_invoice(self, customer_name: str) -> Invoice:
        invoice_id = f"INV-{self._counter:04d}"
        self._counter += 1
        inv = Invoice(invoice_id, customer_name, date.today())
        self._invoices[invoice_id] = inv
        return inv

    def print_invoice(self, invoice_id: str) -> None:
        invoice = self._invoices.get(invoice_id)
        if invoice is None:
            print(f"Invoice {invoice_id} not found.")
            return
        print(self._view.render(invoice))
```

### Putting it together

```python
# main.py
from invoicing import InvoiceController

ctrl = InvoiceController()

inv = ctrl.create_invoice("Acme Corp")
inv.add_item("Python Consulting (hrs)", 8, 150.00)
inv.add_item("Code Review", 2, 200.00)
inv.add_item("Technical Report", 1, 350.00)

ctrl.print_invoice(inv.invoice_id)
```

---

## Part 4: Configuration Management

Hard-coding database URLs or API keys is a security risk and makes deployments fragile. Use `configparser` to externalise configuration.

```python
# config/settings.ini
[DEFAULT]
debug = false
log_level = INFO

[database]
host = localhost
port = 5432
name = invoicing_db

[email]
smtp_host = smtp.example.com
smtp_port = 587
from_address = invoices@example.com
```

```python
# src/invoicing/config.py
import configparser
import os

class AppConfig:
    """Loads settings from a .ini file, overridable by environment variables."""

    def __init__(self, config_path: str = "config/settings.ini"):
        self._cfg = configparser.ConfigParser()
        self._cfg.read(config_path)

    @property
    def db_host(self) -> str:
        # Environment variable takes priority over config file
        return os.environ.get("DB_HOST") or self._cfg["database"]["host"]

    @property
    def db_port(self) -> int:
        return int(os.environ.get("DB_PORT") or self._cfg["database"]["port"])

    @property
    def log_level(self) -> str:
        return os.environ.get("LOG_LEVEL") or self._cfg["DEFAULT"]["log_level"]

    @property
    def debug(self) -> bool:
        raw = os.environ.get("DEBUG") or self._cfg["DEFAULT"]["debug"]
        return raw.lower() in ("true", "1", "yes")


# Usage
config = AppConfig()
print(config.db_host)   # "localhost" (or DB_HOST env var if set)
print(config.debug)      # False
```

---

## Key Takeaways

- **Src layout** keeps your package importable only after installation, preventing subtle bugs in larger projects
- `__init__.py` is your package's public contract — keep it intentional with `__all__`
- **MVC separates concerns**: change the view without touching the model; swap the data store without touching the view
- Config files + environment variable overrides give you one codebase deployable to dev, staging, and production
- Dataclasses with `@property` keep business logic close to the data it describes

---

## What's Next

**[Lesson 02 → Working with Business Data](lesson-02-working-with-business-data.md)**

We'll build a real sales data pipeline — reading, validating, cleaning, and transforming CSV and JSON data using the Python standard library.
