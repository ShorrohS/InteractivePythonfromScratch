# Lesson 01 — Clean Code Principles

**Phase:** 19 — Software Engineering | **Time:** ~50 min | **Prerequisite:** Phase 18 — Business Projects

---

## Learning Objectives

- Apply PEP 8 naming conventions consistently across variables, functions, classes, and constants
- Write single-responsibility functions and identify when a function does too much
- Know when to write a comment versus letting the code speak for itself
- Use type hints to communicate intent without adding noise
- Spot and fix common readability problems in real Python code

---

## Part 1: PEP 8 Naming Conventions

Naming is the first thing a reviewer reads. Consistent conventions signal that you take the codebase seriously.

```python
# ── Variables and function parameters ──────────────────────────────────────
# snake_case: lowercase words separated by underscores

user_age = 28
total_price = 149.99
is_active = True
items_per_page = 25

# ── Functions and methods ───────────────────────────────────────────────────
# snake_case verbs that describe what the function does

def calculate_discount(price: float, rate: float) -> float:
    return price * (1 - rate)

def fetch_user_by_email(email: str) -> dict | None:
    ...

def is_valid_email(email: str) -> bool:
    ...

# ── Classes ─────────────────────────────────────────────────────────────────
# PascalCase (CapWords): each word capitalised, no underscores

class OrderProcessor:
    ...

class DatabaseConnectionPool:
    ...

class InvalidEmailError(ValueError):
    ...

# ── Constants ───────────────────────────────────────────────────────────────
# SCREAMING_SNAKE_CASE at module level

MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT_SECONDS = 30
API_BASE_URL = "https://api.example.com/v2"
TAX_RATE = 0.10

# ── Private members ─────────────────────────────────────────────────────────
# Single leading underscore: "internal use" convention
# Double leading underscore: name mangling (use sparingly)

class BankAccount:
    def __init__(self, balance: float) -> None:
        self._balance = balance          # internal, but accessible
        self.__pin = "1234"              # name-mangled, strongly private

    def _validate_amount(self, amount: float) -> bool:
        return amount > 0

# ── Type aliases ────────────────────────────────────────────────────────────
# PascalCase to match type convention

UserId = int
EmailAddress = str
PriceMap = dict[str, float]
```

**Common naming mistakes to avoid:**

```python
# BAD: single-letter names outside of tiny loops
def calc(x, y, z):
    return x * y - z

# GOOD: names reveal intent
def calculate_net_price(unit_price: float, quantity: int, discount: float) -> float:
    return unit_price * quantity - discount

# BAD: abbreviations that save two keystrokes but cost five seconds of confusion
def proc_ord(o, u):
    ...

# GOOD: spell it out
def process_order(order: dict, user: dict) -> None:
    ...

# BAD: misleading boolean name
def check_user(user: dict) -> bool:
    return user.get("active", False)   # does "check" mean validate? find? enable?

# GOOD: boolean names start with is_, has_, can_, should_
def is_user_active(user: dict) -> bool:
    return user.get("active", False)
```

---

## Part 2: Single-Responsibility Functions

A function should do **one thing** and do it well. When you struggle to name a function without using "and", it is doing too much.

```python
# ── BEFORE: one function doing three jobs ──────────────────────────────────

def process_order(order_data: dict) -> str:
    # Job 1: validation
    if not order_data.get("items"):
        raise ValueError("Order has no items")
    if not order_data.get("customer_email"):
        raise ValueError("Customer email required")

    # Job 2: price calculation
    subtotal = sum(
        item["price"] * item["quantity"]
        for item in order_data["items"]
    )
    tax = round(subtotal * 0.10, 2)
    total = subtotal + tax

    # Job 3: receipt formatting
    lines = [f"Order for {order_data['customer_email']}"]
    for item in order_data["items"]:
        lines.append(f"  {item['name']}: ${item['price'] * item['quantity']:.2f}")
    lines.append(f"Tax: ${tax:.2f}")
    lines.append(f"Total: ${total:.2f}")
    return "\n".join(lines)


# ── AFTER: each function has one clear job ──────────────────────────────────

def validate_order(order_data: dict) -> None:
    """Raise ValueError if required fields are missing."""
    if not order_data.get("items"):
        raise ValueError("Order has no items")
    if not order_data.get("customer_email"):
        raise ValueError("Customer email required")


def calculate_order_totals(items: list[dict]) -> tuple[float, float, float]:
    """Return (subtotal, tax, total) for a list of line items."""
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax = round(subtotal * 0.10, 2)
    total = subtotal + tax
    return subtotal, tax, total


def format_receipt(order_data: dict, tax: float, total: float) -> str:
    """Format a human-readable receipt string."""
    lines = [f"Order for {order_data['customer_email']}"]
    for item in order_data["items"]:
        lines.append(f"  {item['name']}: ${item['price'] * item['quantity']:.2f}")
    lines.append(f"Tax: ${tax:.2f}")
    lines.append(f"Total: ${total:.2f}")
    return "\n".join(lines)


def process_order(order_data: dict) -> str:
    """Coordinate validation, pricing, and formatting."""
    validate_order(order_data)
    subtotal, tax, total = calculate_order_totals(order_data["items"])
    return format_receipt(order_data, tax, total)
```

The refactored version is easier to test (each piece in isolation), easier to read, and easier to change — if the tax rate changes, you touch `calculate_order_totals` only.

---

## Part 3: Comments vs Self-Documenting Code

The best comment is code that does not need one. When a comment explains **what** the code does, that is usually a sign the code should be clearer. Comments shine when explaining **why** — the reasoning, trade-off, or constraint that is not obvious from reading the code.

```python
# ── BEFORE: comments patch bad names ───────────────────────────────────────

# multiply price by discount percentage and subtract
def calc(p, d):
    # convert percentage to decimal
    r = d / 100
    # apply discount
    return p - (p * r)

# check if c is premium
def chk(c):
    # premium if spent more than 1000
    return c["spent"] > 1000


# ── AFTER: names remove the need for most comments ─────────────────────────

PREMIUM_SPEND_THRESHOLD = 1000.00

def apply_percentage_discount(price: float, discount_percent: float) -> float:
    discount_rate = discount_percent / 100
    return price - (price * discount_rate)

def is_premium_customer(customer: dict) -> bool:
    return customer["total_spend"] > PREMIUM_SPEND_THRESHOLD


# ── When comments ARE valuable ──────────────────────────────────────────────

def fetch_exchange_rate(currency: str) -> float:
    # The free-tier API caps at 100 requests/day.
    # We cache for 6 hours to stay well under that limit.
    cache_key = f"exchange_rate:{currency}"
    cached = _cache.get(cache_key)
    if cached:
        return cached
    rate = _api_client.get(f"/rates/{currency}")
    _cache.set(cache_key, rate, ttl=21600)
    return rate


def calculate_shipping(weight_kg: float, distance_km: float) -> float:
    # Formula agreed with logistics team on 2024-03-10.
    # Base fee covers first 500 km; weight surcharge applies beyond that.
    base_fee = 5.00
    if distance_km > 500:
        base_fee += (distance_km - 500) * 0.002
    weight_surcharge = weight_kg * 0.50
    return round(base_fee + weight_surcharge, 2)
```

---

## Part 4: Type Hints Clarify Intent

Type hints turn function signatures into mini-documentation. Readers understand what to pass and what to expect without reading the body.

```python
from typing import Optional
from datetime import date

# ── Without type hints: the caller has to read the body to understand usage ─

def get_report(user, start, end, fmt):
    ...

# ── With type hints: the signature is self-explanatory ──────────────────────

def get_report(
    user_id: int,
    start_date: date,
    end_date: date,
    format: str = "pdf",
) -> bytes:
    """Generate a sales report for the given user and date range."""
    ...

# ── Use Optional (or X | None) for values that may be absent ────────────────

def find_customer(email: str) -> Optional[dict]:
    """Return customer dict, or None if not found."""
    ...

# Python 3.10+ union syntax
def find_customer(email: str) -> dict | None:
    ...

# ── TypedDict for structured dictionaries ───────────────────────────────────

from typing import TypedDict

class OrderItem(TypedDict):
    name: str
    price: float
    quantity: int

class Order(TypedDict):
    customer_email: str
    items: list[OrderItem]
    created_at: date

def validate_order(order: Order) -> None:
    if not order["items"]:
        raise ValueError("Order must have at least one item")

# ── Callable type hints for function arguments ──────────────────────────────

from typing import Callable

def retry(
    func: Callable[[], bool],
    max_attempts: int = MAX_RETRY_ATTEMPTS,
    on_failure: Callable[[int], None] | None = None,
) -> bool:
    for attempt in range(1, max_attempts + 1):
        if func():
            return True
        if on_failure:
            on_failure(attempt)
    return False
```

Type hints do not enforce anything at runtime by default, but tools like `mypy` and your IDE use them to catch bugs before you run the code.

---

## Key Takeaways

- Follow PEP 8 naming conventions — `snake_case` for variables and functions, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants
- A function that is hard to name without using "and" is doing too many things; split it
- Comments should explain **why**, not **what** — clear names do the "what" for free
- Type hints are documentation that tools can check; use them from day one on any public function
- Clean code is not about being clever — it is about being considerate to the next reader, who is often yourself

---

## What's Next

**[Lesson 02 → Design Patterns](lesson-02-design-patterns.md)**

We cover Singleton, Factory, Observer, and Strategy patterns — proven templates for solving recurring design problems in Python.
