# ✅ Phase 19 — Intermediate Solutions

> Each solution explains which SOLID principle the original code violated and how the refactoring fixes it.

---

## Q1 — Fix a Single Responsibility Violation

**Principle: Single Responsibility Principle (SRP)**
*A class should have only one reason to change.*

### Refactored

```python
import csv
import smtplib
from dataclasses import dataclass
from typing import List


@dataclass
class Employee:
    name: str
    email: str
    hours: float
    hourly_rate: float


@dataclass
class PayResult:
    gross: float
    tax: float
    net: float


# Responsibility 1: Load employee records from storage
class EmployeeLoader:
    """Reads employee data from a CSV file."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def load(self) -> List[Employee]:
        with open(self.filepath) as f:
            reader = csv.DictReader(f)
            return [
                Employee(
                    name=row['name'],
                    email=row['email'],
                    hours=float(row['hours']),
                    hourly_rate=float(row['hourly_rate']),
                )
                for row in reader
            ]


# Responsibility 2: Calculate payroll figures
class PayrollCalculator:
    """Computes gross pay, tax, and net pay for an employee."""

    TAX_RATE = 0.22

    def calculate(self, employee: Employee) -> PayResult:
        gross = employee.hours * employee.hourly_rate
        tax   = gross * self.TAX_RATE
        net   = gross - tax
        return PayResult(gross=gross, tax=tax, net=net)


# Responsibility 3: Deliver payslips via email
class PayslipSender:
    """Sends payslip emails via SMTP."""

    SENDER = "payroll@company.com"

    def __init__(self, smtp_host: str, smtp_port: int) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def send(self, employee: Employee, pay: PayResult) -> None:
        body = (
            f"Dear {employee.name},\n"
            f"Gross: ${pay.gross:.2f}\n"
            f"Tax:   ${pay.tax:.2f}\n"
            f"Net:   ${pay.net:.2f}"
        )
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.sendmail(self.SENDER, employee.email, body)


# Thin orchestrator — its only job is wiring and sequencing
class PayrollService:
    def __init__(
        self,
        loader: EmployeeLoader,
        calculator: PayrollCalculator,
        sender: PayslipSender,
    ) -> None:
        self.loader     = loader
        self.calculator = calculator
        self.sender     = sender

    def run(self) -> None:
        for employee in self.loader.load():
            pay = self.calculator.calculate(employee)
            self.sender.send(employee, pay)
```

### Why this is better

The original `PayrollProcessor` had three unrelated reasons to change:
1. The CSV format changes → touches loading logic.
2. The tax rate changes → touches calculation logic.
3. The email server changes → touches sending logic.

After the refactor each class has exactly one reason to change. You can swap SMTP for SendGrid by writing a new `PayslipSender` without touching `PayrollCalculator` at all. You can test `PayrollCalculator` with a hard-coded `Employee` object, no file system required.

---

## Q2 — Fix an Open/Closed Violation

**Principle: Open/Closed Principle (OCP)**
*Software entities should be open for extension but closed for modification.*

### Refactored

```python
from abc import ABC, abstractmethod
from typing import List, Dict


class ReportExporter(ABC):
    """Base class for all report format exporters."""

    @abstractmethod
    def export(self, data: List[Dict]) -> str: ...


class CsvExporter(ReportExporter):
    def export(self, data: List[Dict]) -> str:
        lines = ['name,score']
        for row in data:
            lines.append(f"{row['name']},{row['score']}")
        return '\n'.join(lines)


class HtmlExporter(ReportExporter):
    def export(self, data: List[Dict]) -> str:
        rows = ''.join(
            f"<tr><td>{r['name']}</td><td>{r['score']}</td></tr>"
            for r in data
        )
        return f"<table><tr><th>Name</th><th>Score</th></tr>{rows}</table>"


class TxtExporter(ReportExporter):
    def export(self, data: List[Dict]) -> str:
        lines = [f"{r['name']:<20} {r['score']}" for r in data]
        return '\n'.join(lines)


# Registry maps a string key to a class
_EXPORTERS: dict[str, type[ReportExporter]] = {
    'csv':  CsvExporter,
    'html': HtmlExporter,
    'txt':  TxtExporter,
}


def export_report(data: List[Dict], format_type: str) -> str:
    cls = _EXPORTERS.get(format_type)
    if cls is None:
        raise ValueError(f"Unknown format: {format_type}")
    return cls().export(data)


# --- Adding a new format: zero edits above this line ---
class JsonExporter(ReportExporter):
    def export(self, data: List[Dict]) -> str:
        import json
        return json.dumps(data, indent=2)

_EXPORTERS['json'] = JsonExporter
```

### Why this is better

The original function grew an `elif` branch every time a new format was needed. Each addition risked breaking existing branches and required a test run of the entire function.

With the registry approach, adding `JsonExporter` is a two-step process (write the class, register it) that touches zero existing code. The `export_report` function itself never changes. This is what OCP means in practice: new behaviour is added by extension, not by modification.

---

## Q3 — Fix a Liskov Substitution Violation

**Principle: Liskov Substitution Principle (LSP)**
*A subclass must be substitutable for its superclass without breaking the program.*

### Refactored

```python
from abc import ABC, abstractmethod


class ReadableFile(ABC):
    """Guarantees only read operations."""

    @abstractmethod
    def read(self) -> str: ...

    @abstractmethod
    def size(self) -> int: ...


class WritableFile(ReadableFile):
    """Extends ReadableFile with write capability."""

    @abstractmethod
    def write(self, text: str) -> None: ...


class ReadOnlyFile(ReadableFile):
    """A file whose content is set at construction time and cannot change."""

    def __init__(self, path: str, content: str = "") -> None:
        self.path     = path
        self._content = content

    def read(self) -> str:
        return self._content

    def size(self) -> int:
        return len(self._content)


class RegularFile(WritableFile):
    """A mutable file that supports both read and write."""

    def __init__(self, path: str) -> None:
        self.path     = path
        self._content = ""

    def read(self) -> str:
        return self._content

    def write(self, text: str) -> None:
        self._content += text

    def size(self) -> int:
        return len(self._content)
```

### Why this is better

The original code broke LSP: any function that accepted a `File` and called `.write()` would crash if handed a `ReadOnlyFile`. That is the exact scenario LSP forbids.

The fix splits the hierarchy at the capability boundary. Code that only needs to read accepts `ReadableFile` — it can safely receive either subclass. Code that needs to write accepts `WritableFile` — the type system prevents passing a `ReadOnlyFile` there. No surprises at runtime, and no need for defensive `isinstance` checks in calling code.

---

## Q4 — Apply the Factory Pattern

**Pattern: Factory**
*Centralise object creation so callers depend on an interface, not a concrete class.*

### Refactored

```python
from abc import ABC, abstractmethod
from typing import Any, Dict


class PaymentProcessor(ABC):
    """Common interface for all payment providers."""

    @abstractmethod
    def charge(self, amount: float, card_details: Dict[str, Any]) -> bool: ...


class StripeProcessor(PaymentProcessor):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def charge(self, amount: float, card_details: Dict[str, Any]) -> bool:
        print(f"[Stripe] Charging ${amount:.2f} with key ...{self.api_key[-4:]}")
        return True  # real implementation would call the Stripe SDK


class PayPalProcessor(PaymentProcessor):
    def __init__(self, client_id: str) -> None:
        self.client_id = client_id

    def charge(self, amount: float, card_details: Dict[str, Any]) -> bool:
        print(f"[PayPal] Charging ${amount:.2f} via client {self.client_id[:6]}...")
        return True


class SquareProcessor(PaymentProcessor):
    def __init__(self, location_id: str) -> None:
        self.location_id = location_id

    def charge(self, amount: float, card_details: Dict[str, Any]) -> bool:
        print(f"[Square] Charging ${amount:.2f} at location {self.location_id}")
        return True


class PaymentProcessorFactory:
    """Creates the correct PaymentProcessor for a given payment type."""

    _CONFIG = {
        'stripe': lambda: StripeProcessor(api_key="sk_live_abc123"),
        'paypal': lambda: PayPalProcessor(client_id="pp_client_xyz"),
        'square': lambda: SquareProcessor(location_id="sq_loc_789"),
    }

    @classmethod
    def create(cls, payment_type: str) -> PaymentProcessor:
        builder = cls._CONFIG.get(payment_type)
        if builder is None:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return builder()


class CheckoutService:
    """Processes payments using an injected processor."""

    def __init__(self, processor: PaymentProcessor) -> None:
        self.processor = processor

    def charge(self, amount: float, card_details: Dict[str, Any]) -> bool:
        return self.processor.charge(amount, card_details)


# --- Usage ---
# processor = PaymentProcessorFactory.create('stripe')
# service   = CheckoutService(processor)
# service.charge(99.99, {...})
```

### Why this is better

The original `CheckoutService.charge` contained the entire selection logic. Adding PayPal required opening the service class and editing it.

Now, `CheckoutService` depends only on the `PaymentProcessor` interface — it has no idea whether the underlying implementation is Stripe, PayPal, or something that doesn't exist yet. The factory centralises the construction decision. Adding a fourth provider means adding one entry to `_CONFIG` and one new class; `CheckoutService` never changes.

Injecting the processor into `CheckoutService.__init__` also enables testing: pass a `FakePaymentProcessor` that always returns `True`, and you can test checkout logic without real credentials.

---

## Q5 — Apply the Observer Pattern

**Pattern: Observer**
*Define a subscription mechanism to notify multiple objects about events in another object.*

### Refactored

```python
from abc import ABC, abstractmethod
from typing import List


class OrderObserver(ABC):
    """Receives notifications when an order event occurs."""

    @abstractmethod
    def update(self, event: str, order: 'Order') -> None: ...


class EmailObserver(OrderObserver):
    def update(self, event: str, order: 'Order') -> None:
        if event == 'shipped':
            print(f"[Email] → {order.customer.email}: "
                  f"Order {order.order_id} has shipped!")


class SmsObserver(OrderObserver):
    def update(self, event: str, order: 'Order') -> None:
        if event == 'shipped':
            print(f"[SMS] → {order.customer.phone}: "
                  f"Order {order.order_id} shipped.")


class PushObserver(OrderObserver):
    def update(self, event: str, order: 'Order') -> None:
        if event == 'shipped':
            print(f"[Push] → {order.customer.device_id}: "
                  f"Your order is on its way!")


class Order:
    def __init__(self, order_id: str, customer) -> None:
        self.order_id  = order_id
        self.customer  = customer
        self.status    = 'pending'
        self._observers: List[OrderObserver] = []

    def subscribe(self, observer: OrderObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: OrderObserver) -> None:
        self._observers.remove(observer)

    def _notify_all(self, event: str) -> None:
        for observer in self._observers:
            observer.update(event, self)

    def mark_shipped(self) -> None:
        self.status = 'shipped'
        self._notify_all('shipped')
```

### Why this is better

The original `Order.mark_shipped` imported and called three specific notifiers. It would need editing every time a new notification channel was added.

With Observer, `Order` knows nothing about what happens when it ships — only that *something* should happen. Observers register themselves from outside. Adding a Slack notification means writing `SlackObserver` and calling `order.subscribe(SlackObserver())` from the setup code. The `Order` class never changes.

This also enables per-customer configuration: a customer who has opted out of SMS simply doesn't have an `SmsObserver` subscribed to their order.

---

## Q6 — Apply the Repository Pattern

**Pattern: Repository**
*Separate data access logic from business logic behind an abstract interface.*

### Refactored

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import sqlite3


@dataclass
class User:
    id: int
    name: str
    email: str


class UserRepository(ABC):
    """Abstract interface for user data storage."""

    @abstractmethod
    def find_active(self) -> List[User]: ...

    @abstractmethod
    def deactivate(self, user_id: int) -> None: ...

    @abstractmethod
    def set_role(self, user_id: int, role: str) -> None: ...


class SqliteUserRepository(UserRepository):
    """Concrete repository backed by SQLite."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def find_active(self) -> List[User]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, name, email FROM users WHERE is_active = 1"
            ).fetchall()
        return [User(id=r[0], name=r[1], email=r[2]) for r in rows]

    def deactivate(self, user_id: int) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE users SET is_active = 0 WHERE id = ?", (user_id,)
            )

    def set_role(self, user_id: int, role: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE users SET role = ? WHERE id = ?", (role, user_id)
            )


class UserService:
    """Business logic for user management. Has no SQL knowledge."""

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def get_active_users(self) -> List[User]:
        return self.repo.find_active()

    def deactivate_user(self, user_id: int) -> None:
        self.repo.deactivate(user_id)

    def promote_to_admin(self, user_id: int) -> None:
        self.repo.set_role(user_id, 'admin')


# --- In tests: ---
# class FakeUserRepository(UserRepository):
#     def __init__(self):
#         self._users = [User(1, "Alice", "alice@example.com")]
#     def find_active(self): return self._users
#     def deactivate(self, user_id): ...
#     def set_role(self, user_id, role): ...
```

### Why this is better

The original `UserService` opened a new SQLite connection in every method and contained raw SQL strings. Switching to PostgreSQL would require rewriting the entire service.

With the Repository pattern, `UserService` talks to an abstract `UserRepository`. All the SQL lives in `SqliteUserRepository`. Switching to PostgreSQL means writing `PostgresUserRepository` without touching `UserService`. Unit tests inject a `FakeUserRepository` — no database file required, tests run in milliseconds.

---

## Q7 — Remove Duplication via Helper Extraction

**Principle: DRY — Don't Repeat Yourself**
*Every piece of knowledge should have a single, unambiguous representation in the codebase.*

### Refactored

```python
import logging
from typing import Callable, TypeVar

T = TypeVar('T')


class ReportRunner:
    def _run_report(self, name: str, work: Callable[[], T]) -> T:
        """Wrap a report function with standard logging and error handling."""
        logging.info(f"Starting {name}")
        try:
            result = work()
            logging.info(f"{name} completed successfully")
            return result
        except Exception as e:
            logging.error(f"{name} failed: {e}")
            raise

    def run_sales_report(self, start_date: str, end_date: str):
        return self._run_report(
            f"sales report: {start_date} to {end_date}",
            lambda: self._format_sales(self._fetch_sales(start_date, end_date)),
        )

    def run_inventory_report(self, warehouse_id: str):
        return self._run_report(
            f"inventory report for warehouse {warehouse_id}",
            lambda: self._format_inventory(self._fetch_inventory(warehouse_id)),
        )

    def run_employee_report(self, department: str):
        return self._run_report(
            f"employee report for {department}",
            lambda: self._format_employees(self._fetch_employees(department)),
        )
```

### Why this is better

The three original methods shared identical structure: log start, try block, log success, except block with log and re-raise. That is duplicated logic — a change to the error-handling behaviour (e.g., adding a metrics counter on failure) would require editing three places instead of one.

`_run_report` captures the scaffolding once. Each public method describes *what* it does (`name`) and *how* it does it (the `work` lambda). If the logging format changes, you edit one line. The `TypeVar` preserves the return type so callers still get type-checked results.

---

> **Exercises:** → [../../exercises/intermediate/exercises.md](../../exercises/intermediate/exercises.md)
