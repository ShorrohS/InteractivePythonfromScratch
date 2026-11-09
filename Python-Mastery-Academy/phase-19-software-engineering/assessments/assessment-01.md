# Phase 19 — Completion Assessment: Refactor Legacy Order System

> **Pass mark:** 80% (64 / 80 points) | **Time:** 50 minutes

---

## Introduction

You have inherited the following legacy module. It works, but it was written quickly and violates multiple software engineering principles. Your job is to identify the problems, design a better architecture, and implement targeted improvements.

Read the entire code block before starting any part.

```python
import sqlite3, smtplib, logging

DB = "shop.db"
SMTP_HOST = "mail.company.com"
total_orders_placed = 0   # global counter

class OrderService:

    def place_order(self, cust_id, name, email, items, ptype):
        # validate
        if cust_id == None or cust_id <= 0:
            return None
        if not items or len(items) == 0:
            return None

        # price
        subtotal = 0
        conn = sqlite3.connect(DB)
        for i in items:
            row = conn.execute("SELECT price FROM products WHERE id=?", (i['id'],)).fetchone()
            if row == None:
                conn.close()
                return None
            subtotal += row[0] * i['qty']
        conn.close()

        if subtotal > 1000:
            subtotal = subtotal * 0.85
        elif subtotal > 500:
            subtotal = subtotal * 0.90
        tax = subtotal * 0.08
        total = subtotal + tax

        # payment
        if ptype == 'stripe':
            import stripe
            stripe.api_key = "sk_live_HARDCODED_SECRET"
            stripe.Charge.create(amount=int(total*100), currency="usd")
        elif ptype == 'paypal':
            import paypalrestsdk
            paypalrestsdk.configure({"client_id": "HARDCODED_ID", "client_secret": "HARDCODED_SECRET"})
            payment = paypalrestsdk.Payment({"intent": "sale", "transactions": [{"amount": {"total": str(total), "currency": "USD"}}]})
            payment.create()
        elif ptype == 'cash':
            pass  # nothing to process

        # save
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO orders (customer_id, total, status) VALUES (?,?,?)", (cust_id, total, 'placed'))
        oid = c.lastrowid
        conn.commit()
        conn.close()

        # notify
        if email.endswith('@gmail.com') or email.endswith('@yahoo.com'):
            with smtplib.SMTP(SMTP_HOST) as s:
                s.sendmail("orders@company.com", email,
                           f"Order {oid} placed! Total: ${total:.2f}")
        elif email.endswith('@company.com'):
            with smtplib.SMTP(SMTP_HOST) as s:
                s.sendmail("orders@company.com", email,
                           f"[INTERNAL] Order {oid} placed for customer {cust_id}. Total: ${total:.2f}")

        global total_orders_placed
        total_orders_placed += 1
        return oid

    def get_orders(self, cust_id, status=None, include_cancelled=[]):
        conn = sqlite3.connect(DB)
        if status != None:
            rows = conn.execute("SELECT * FROM orders WHERE customer_id=? AND status=?", (cust_id, status)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM orders WHERE customer_id=?", (cust_id,)).fetchall()
        conn.close()
        for r in include_cancelled:
            rows.append(r)
        return rows

    def cancel_order(self, order_id):
        try:
            conn = sqlite3.connect(DB)
            conn.execute("UPDATE orders SET status='cancelled' WHERE id=?", (order_id,))
            conn.commit()
            conn.close()
        except:
            pass
```

---

## PART A — Identify Violations (30 points)

List every SOLID violation and code quality problem you can find. For each issue:
- State what the problem is (one sentence)
- Name the principle it violates (SOLID letter or clean code rule)
- Point to the line or method where it occurs

**Scoring:** 5 points each (maximum 6 issues accepted, additional ones are bonus)

**Minimum expected findings:**
1. God Object / SRP violation in `OrderService`
2. Magic numbers for discount thresholds and tax rate
3. Mutable default argument in `get_orders`
4. Bare `except: pass` in `cancel_order`
5. Global state mutation (`total_orders_placed`)
6. Hardcoded secrets (API keys inline in source code)

---

## PART B — Design the Refactoring (15 points)

In ASCII or plain text, describe the new class structure you would create.

For each class/service you propose:
- Give it a name
- List its public methods
- State what it depends on (if anything)

**Example structure to expand on:**
```
OrderService (orchestrator)
  place_order(request: OrderRequest) -> int
  └── depends on: OrderValidator, PricingService, PaymentProcessor,
                  OrderRepository, NotificationService

PaymentProcessor (ABC)
  charge(amount: float, details: dict) -> bool
  └── implementations: StripeProcessor, PayPalProcessor, CashProcessor
```

You must name at least 5 distinct classes and identify which pattern(s) you are applying and why.

**Scoring:** 3 points per well-described class (up to 5 classes = 15 points)

---

## PART C — Implement (30 points)

### Task 1 — Extract a PaymentProcessor abstraction (10 points)

Replace the `if ptype == 'stripe' ... elif ptype == 'paypal'` block with:
1. A `PaymentProcessor` ABC with a `charge(amount: float, details: dict) -> bool` method.
2. `StripeProcessor` and `PayPalProcessor` concrete classes.
3. A `PaymentProcessorFactory.create(ptype: str) -> PaymentProcessor` class method.
4. The `OrderService` receiving a `PaymentProcessor` via its constructor (not creating one itself).

Write the complete code for all four components.

---

### Task 2 — Replace the notification if/elif with Observer pattern (10 points)

Replace the email-dispatch block (`if email.endswith('@gmail.com')...`) with:
1. An `OrderObserver` ABC with `on_order_placed(order_id: int, email: str, total: float) -> None`.
2. `ExternalCustomerObserver` (sends the standard confirmation email).
3. `InternalCustomerObserver` (sends the internal copy).
4. `OrderService` maintains a list of observers and calls each one after saving the order.

Write the complete code for all four components.

---

### Task 3 — Add type hints and Google-style docstrings (10 points)

Rewrite the `place_order` method signature (you do not need to rewrite the body) with:
1. Full type annotations on every parameter and the return value.
2. A Google-style docstring with `Args:`, `Returns:`, and `Raises:` sections.
3. Replace the `ptype: str` parameter with a `payment_processor: PaymentProcessor` parameter (from Task 1).
4. Replace the flat `cust_id, name, email` params with an `OrderRequest` dataclass.

Define the `OrderRequest` dataclass and the annotated method signature.

---

## PART D — Written Questions (5 points each)

**Q1.** The Factory pattern and the Strategy pattern both involve polymorphism and interchangeable implementations. Explain the key difference between them. Give one sentence for each pattern describing when you would choose it.

---

**Q2.** A colleague says: "I don't need docstrings — good variable names are enough documentation." Give two concrete scenarios where a docstring provides information that no variable name can.

---

**Q3.** Explain what "dependency injection" means and why it makes code easier to test. Use a one-paragraph explanation and a short code snippet showing the *before* (bad) and *after* (good).

---

## Scoring Rubric

| Part | Max Points | Pass threshold |
|------|-----------|----------------|
| A — Identify violations | 30 | 20 |
| B — Design | 15 | 10 |
| C — Implement (3 tasks) | 30 | 20 |
| D — Written (3 questions) | 15 | 10 |
| **Total** | **80** | **64** |

---

## Answer Key

### Part A — Expected findings

| # | Issue | Principle |
|---|-------|-----------|
| 1 | `OrderService` does validation, pricing, payment, persistence, and notification | SRP |
| 2 | `0.85`, `0.90`, `1000`, `500`, `0.08` are bare literals | Avoid Magic Numbers |
| 3 | `include_cancelled=[]` mutable default argument | Python gotcha |
| 4 | `except: pass` in `cancel_order` silently swallows all exceptions | Fail loudly |
| 5 | `global total_orders_placed` mutated inside a method | Avoid Global State |
| 6 | `"sk_live_HARDCODED_SECRET"` and PayPal secrets in source code | Security: never hardcode credentials |
| Bonus | `if ptype == 'stripe' ... elif ptype == 'paypal'` — adding cash/crypto requires editing the class | OCP |
| Bonus | `OrderService` directly instantiates `stripe` and `paypalrestsdk` — no way to test without real credentials | DIP |

---

### Part C — Task 1 model solution

```python
from abc import ABC, abstractmethod
from typing import Any, Dict


class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, amount: float, details: Dict[str, Any]) -> bool: ...


class StripeProcessor(PaymentProcessor):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def charge(self, amount: float, details: Dict[str, Any]) -> bool:
        # real implementation would call the Stripe SDK
        print(f"[Stripe] Charging ${amount:.2f}")
        return True


class PayPalProcessor(PaymentProcessor):
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id     = client_id
        self.client_secret = client_secret

    def charge(self, amount: float, details: Dict[str, Any]) -> bool:
        print(f"[PayPal] Charging ${amount:.2f}")
        return True


class CashProcessor(PaymentProcessor):
    def charge(self, amount: float, details: Dict[str, Any]) -> bool:
        print(f"[Cash] No electronic charge needed for ${amount:.2f}")
        return True


class PaymentProcessorFactory:
    _BUILDERS = {
        'stripe': lambda: StripeProcessor(api_key="from_env_or_config"),
        'paypal': lambda: PayPalProcessor("from_config", "from_config"),
        'cash':   lambda: CashProcessor(),
    }

    @classmethod
    def create(cls, ptype: str) -> PaymentProcessor:
        builder = cls._BUILDERS.get(ptype)
        if builder is None:
            raise ValueError(f"Unknown payment type: {ptype}")
        return builder()
```

---

### Part C — Task 2 model solution

```python
from abc import ABC, abstractmethod
import smtplib

SMTP_HOST = "mail.company.com"


class OrderObserver(ABC):
    @abstractmethod
    def on_order_placed(self, order_id: int, email: str, total: float) -> None: ...


class ExternalCustomerObserver(OrderObserver):
    def on_order_placed(self, order_id: int, email: str, total: float) -> None:
        with smtplib.SMTP(SMTP_HOST) as s:
            s.sendmail(
                "orders@company.com", email,
                f"Order {order_id} placed! Total: ${total:.2f}"
            )


class InternalCustomerObserver(OrderObserver):
    def on_order_placed(self, order_id: int, email: str, total: float) -> None:
        with smtplib.SMTP(SMTP_HOST) as s:
            s.sendmail(
                "orders@company.com", email,
                f"[INTERNAL] Order {order_id} placed. Total: ${total:.2f}"
            )


# In OrderService:
# self._observers: list[OrderObserver] = []
# def subscribe(self, obs: OrderObserver) -> None: self._observers.append(obs)
# After saving the order:
# for obs in self._observers: obs.on_order_placed(oid, email, total)
```

---

### Part C — Task 3 model solution

```python
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class OrderItem:
    product_id: int
    quantity: int


@dataclass
class OrderRequest:
    customer_id: int
    customer_name: str
    customer_email: str
    items: List[OrderItem]


class OrderService:
    def place_order(
        self,
        request: OrderRequest,
        processor: PaymentProcessor,
    ) -> Optional[int]:
        """Place an order and charge the customer.

        Validates the request, prices each item, processes payment,
        persists the order, and notifies all registered observers.

        Args:
            request:   Validated order request containing customer info
                       and the list of items to purchase.
            processor: A PaymentProcessor implementation responsible for
                       executing the charge.

        Returns:
            The integer order ID assigned by the database, or None if
            validation fails at any step.

        Raises:
            ValueError: If a product ID in the request does not exist in
                        the product catalogue.
            RuntimeError: If the payment processor raises an error.
        """
        ...  # implementation
```

---

### Part D — Model answers

**Q1.** Factory decides *which* object to create based on a parameter, then hands it to the caller. Use Factory when object construction is complex or needs to vary by type. Strategy defines an interchangeable algorithm that is injected at construction time and called repeatedly. Use Strategy when you want to swap behaviour at runtime without changing the host class.

**Q2.** (1) The valid range or format of a parameter — `rate: float` tells you the type but not that it must be between 0 and 1. (2) What exceptions the function raises and under what conditions — no variable name conveys "raises `ValueError` if the product does not exist."

**Q3.** Dependency injection means passing dependencies into a class from the outside rather than letting the class create them. This makes testing trivial because you can pass a fake implementation instead of the real one. Before: `class Service: def __init__(self): self.db = MySQLDatabase()` — tests require a real database. After: `class Service: def __init__(self, db: Database): self.db = db` — tests pass `FakeDatabase()`, no database required.
