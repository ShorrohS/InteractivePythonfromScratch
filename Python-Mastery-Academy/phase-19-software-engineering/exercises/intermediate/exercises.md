# 📝 Phase 19 — Intermediate Exercises

> Each exercise shows code that **runs correctly but violates engineering principles**.
> Your tasks:
> 1. Name the specific principle that is violated.
> 2. Sketch the refactored design (class diagram or description).
> 3. Implement the refactored version.
>
> Solutions: `../../solutions/intermediate/solutions.md`

---

## Q1 — Fix a Single Responsibility Violation ⭐⭐

This class loads employee records from a CSV, calculates their net pay, and sends payslip emails — three unrelated responsibilities packed into one class.

```python
import csv
import smtplib

class PayrollProcessor:
    def __init__(self, filepath, smtp_host, smtp_port):
        self.filepath  = filepath
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.employees = []

    def load_employees(self):
        with open(self.filepath) as f:
            reader = csv.DictReader(f)
            self.employees = list(reader)

    def calculate_pay(self, employee):
        hours = float(employee['hours'])
        rate  = float(employee['hourly_rate'])
        gross = hours * rate
        tax   = gross * 0.22
        net   = gross - tax
        return {'gross': gross, 'tax': tax, 'net': net}

    def send_payslip(self, employee, pay):
        body = (f"Dear {employee['name']},\n"
                f"Gross: ${pay['gross']:.2f}\n"
                f"Tax:   ${pay['tax']:.2f}\n"
                f"Net:   ${pay['net']:.2f}")
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.sendmail("payroll@company.com", employee['email'], body)

    def run(self):
        self.load_employees()
        for emp in self.employees:
            pay = self.calculate_pay(emp)
            self.send_payslip(emp, pay)
```

**Principle violated:** Single Responsibility Principle (SRP)

**What to fix:** Create three focused classes — `EmployeeLoader`, `PayrollCalculator`, `PayslipSender`. Add a thin `PayrollService` that wires them together. Each class has exactly one reason to change.

---

## Q2 — Fix an Open/Closed Violation ⭐⭐

Adding a new export format requires editing `export_report`. A well-designed function is *open for extension* (new formats) but *closed for modification* (existing code untouched).

```python
def export_report(data, format_type):
    if format_type == 'csv':
        lines = ['name,score']
        for row in data:
            lines.append(f"{row['name']},{row['score']}")
        return '\n'.join(lines)

    elif format_type == 'html':
        rows = ''.join(
            f"<tr><td>{r['name']}</td><td>{r['score']}</td></tr>"
            for r in data
        )
        return f"<table><tr><th>Name</th><th>Score</th></tr>{rows}</table>"

    elif format_type == 'txt':
        lines = [f"{r['name']:<20} {r['score']}" for r in data]
        return '\n'.join(lines)

    else:
        raise ValueError(f"Unknown format: {format_type}")
```

**Principle violated:** Open/Closed Principle (OCP)

**What to fix:** Define a `ReportExporter` ABC with a single `export(data) -> str` method. Implement `CsvExporter`, `HtmlExporter`, `TxtExporter`. Store them in a registry dict (`{'csv': CsvExporter, ...}`). Adding a fourth format = one new class, zero edits to existing code.

---

## Q3 — Fix a Liskov Substitution Violation ⭐⭐

`ReadOnlyFile` extends `File`, but any code that calls `.write()` on a `File` will crash when handed a `ReadOnlyFile`. A subclass must honour its parent's contract.

```python
class File:
    def __init__(self, path):
        self.path     = path
        self._content = ""

    def read(self):
        return self._content

    def write(self, text):
        self._content += text

    def size(self):
        return len(self._content)


class ReadOnlyFile(File):
    def write(self, text):
        raise PermissionError("This file is read-only")
```

**Principle violated:** Liskov Substitution Principle (LSP)

**What to fix:** Split the hierarchy at the capability boundary. A `ReadableFile` ABC declares only `read()` and `size()`. A `WritableFile` ABC adds `write()`. `ReadOnlyFile` implements `ReadableFile`. `RegularFile` implements `WritableFile`. No subclass breaks any parent's contract.

---

## Q4 — Apply the Factory Pattern ⭐⭐

`CheckoutService` instantiates payment processors itself using `if/elif`. Adding a new provider forces you to edit this class. Replace the conditional logic with a Factory.

```python
class CheckoutService:
    def __init__(self, payment_type):
        self.payment_type = payment_type

    def charge(self, amount, card_details):
        if self.payment_type == 'stripe':
            processor = StripeProcessor(api_key="sk_live_abc123")
            return processor.charge(amount, card_details)

        elif self.payment_type == 'paypal':
            processor = PayPalProcessor(client_id="pp_client_xyz")
            return processor.execute(amount, card_details)

        elif self.payment_type == 'square':
            processor = SquareProcessor(location_id="sq_loc_789")
            return processor.process(amount, card_details)

        else:
            raise ValueError(f"Unknown payment type: {self.payment_type}")
```

**Pattern to apply:** Factory

**What to fix:**
1. Define a `PaymentProcessor` ABC with a `charge(amount, details)` method.
2. Implement `StripeProcessor`, `PayPalProcessor`, `SquareProcessor` — each with the same interface.
3. Build `PaymentProcessorFactory.create(payment_type) -> PaymentProcessor`.
4. `CheckoutService` receives a `PaymentProcessor` via its constructor. It never calls the factory itself — the caller is responsible for wiring.

---

## Q5 — Apply the Observer Pattern ⭐⭐

When an order ships, `Order` calls every notifier directly. Adding a new channel (e.g. Slack) requires editing `Order`. Replace tight coupling with the Observer pattern.

```python
class Order:
    def __init__(self, order_id, customer):
        self.order_id      = order_id
        self.customer      = customer
        self.status        = 'pending'
        self.email_notifier = EmailNotifier()
        self.sms_notifier   = SmsNotifier()
        self.push_notifier  = PushNotifier()

    def mark_shipped(self):
        self.status = 'shipped'
        self.email_notifier.send(
            self.customer.email,
            f"Order {self.order_id} has shipped!"
        )
        self.sms_notifier.send(
            self.customer.phone,
            f"Order {self.order_id} shipped."
        )
        self.push_notifier.notify(
            self.customer.device_id,
            "Your order is on its way!"
        )
```

**Pattern to apply:** Observer

**What to fix:**
1. Define an `OrderObserver` ABC with an `update(event: str, order: 'Order') -> None` method.
2. Implement `EmailObserver`, `SmsObserver`, `PushObserver`.
3. `Order` stores a list of observers. `subscribe(observer)` and `unsubscribe(observer)` manage the list. `mark_shipped()` calls a private `_notify_all('shipped')` helper.
4. `Order` no longer imports or knows about any specific notifier.

---

## Q6 — Apply the Repository Pattern ⭐⭐

`UserService` is littered with raw SQL. Swap the database engine and you must rewrite the entire service. Extract all data access into a repository.

```python
import sqlite3

class UserService:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_active_users(self):
        conn   = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users WHERE is_active = 1")
        rows = cursor.fetchall()
        conn.close()
        return [{'id': r[0], 'name': r[1], 'email': r[2]} for r in rows]

    def deactivate_user(self, user_id):
        conn   = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

    def promote_to_admin(self, user_id):
        conn   = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
```

**Pattern to apply:** Repository

**What to fix:**
1. Define a `UserRepository` ABC with `find_active() -> list`, `deactivate(user_id: int) -> None`, `set_role(user_id: int, role: str) -> None`.
2. Implement `SqliteUserRepository(UserRepository)` that contains all the SQL.
3. `UserService` receives a `UserRepository` in its constructor. It never touches `sqlite3`.
4. Show how a `FakeUserRepository` could be swapped in for unit tests.

---

## Q7 — Remove Duplication via Helper Extraction ⭐⭐

Every report method follows the same pattern: log start → try the work → log success or log error and re-raise. Only the middle part differs. Extract the scaffolding.

```python
import logging

class ReportRunner:
    def run_sales_report(self, start_date, end_date):
        logging.info(f"Starting sales report: {start_date} to {end_date}")
        try:
            data   = self._fetch_sales(start_date, end_date)
            result = self._format_sales(data)
            logging.info("Sales report completed successfully")
            return result
        except Exception as e:
            logging.error(f"Sales report failed: {e}")
            raise

    def run_inventory_report(self, warehouse_id):
        logging.info(f"Starting inventory report for warehouse {warehouse_id}")
        try:
            data   = self._fetch_inventory(warehouse_id)
            result = self._format_inventory(data)
            logging.info("Inventory report completed successfully")
            return result
        except Exception as e:
            logging.error(f"Inventory report failed: {e}")
            raise

    def run_employee_report(self, department):
        logging.info(f"Starting employee report for {department}")
        try:
            data   = self._fetch_employees(department)
            result = self._format_employees(data)
            logging.info("Employee report completed successfully")
            return result
        except Exception as e:
            logging.error(f"Employee report failed: {e}")
            raise
```

**Principle applied:** DRY (Don't Repeat Yourself)

**What to fix:** Extract a `_run_report(name: str, work: Callable) -> Any` helper that wraps the logging and error handling. Each public method becomes a one-liner that calls `_run_report`. Alternatively, implement this as a context manager or decorator.

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
