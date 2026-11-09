# ✅ Phase 19 — Beginner Solutions

> Read the explanation beneath each solution — understanding *why* matters more than the fix itself.

---

## Q1 — Rename for Clarity

### Bad code
```python
def f(x, y, z):
    a = x * y
    b = a * z
    c = a + b
    return c

r = f(5, 12.99, 0.08)
print(r)
```

### Refactored
```python
def calculate_order_total(quantity: int, unit_price: float, tax_rate: float) -> float:
    subtotal = quantity * unit_price
    tax      = subtotal * tax_rate
    total    = subtotal + tax
    return total


order_total = calculate_order_total(quantity=5, unit_price=12.99, tax_rate=0.08)
print(order_total)
```

### Why this is better

**Principle: Meaningful Names (Clean Code, Chapter 2)**

- `f` tells you nothing — `calculate_order_total` tells you exactly what it computes and returns.
- Single-letter names (`x`, `y`, `z`, `a`, `b`, `c`, `r`) force the reader to mentally track what each one holds. Descriptive names (`quantity`, `unit_price`, `subtotal`) make the code self-documenting.
- Using keyword arguments at the call site (`quantity=5, unit_price=12.99`) prevents silent mistakes if the parameter order ever changes.
- The intermediate variable `subtotal` is now visible and named, which also helps when debugging.

---

## Q2 — Add Docstrings and Type Hints

### Bad code
```python
def greet_user(name, title=""):
    if title:
        return f"Hello, {title} {name}!"
    return f"Hello, {name}!"


def calculate_discount(price, rate):
    if rate < 0 or rate > 1:
        raise ValueError("Rate must be between 0 and 1")
    return price * (1 - rate)


def split_full_name(full_name):
    parts = full_name.strip().split()
    if len(parts) < 2:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])
```

### Refactored
```python
def greet_user(name: str, title: str = "") -> str:
    """Build a personalised greeting for a user.

    Args:
        name:  The user's full name or given name.
        title: Optional honorific (e.g. "Dr.", "Ms."). When omitted,
               the greeting uses the name alone.

    Returns:
        A greeting string ending with an exclamation mark.
    """
    if title:
        return f"Hello, {title} {name}!"
    return f"Hello, {name}!"


def calculate_discount(price: float, rate: float) -> float:
    """Apply a fractional discount rate to a price.

    Args:
        price: The original price. Must be non-negative.
        rate:  The discount fraction, between 0.0 (no discount) and
               1.0 (free). A rate of 0.2 means 20% off.

    Returns:
        The discounted price as a float.

    Raises:
        ValueError: If rate is outside the range [0, 1].
    """
    if rate < 0 or rate > 1:
        raise ValueError("Rate must be between 0 and 1")
    return price * (1 - rate)


def split_full_name(full_name: str) -> tuple[str, str]:
    """Split a full name string into given name and family name.

    Leading and trailing whitespace is stripped before splitting. If
    the string contains only one word, the second element of the tuple
    is an empty string.

    Args:
        full_name: A space-separated name string, e.g. "Alice Johnson"
                   or "Madonna".

    Returns:
        A two-element tuple (first_name, last_name). last_name includes
        all parts after the first word, joined by spaces.
    """
    parts = full_name.strip().split()
    if len(parts) < 2:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])
```

### Why this is better

**Principles: Intentional Documentation, Type Safety**

- **Type hints** turn your function signature into a machine-readable contract. IDEs can warn you when you pass a wrong type, and tools like `mypy` can catch bugs before runtime.
- **Google-style docstrings** (`Args:`, `Returns:`, `Raises:`) follow a consistent structure that tools like Sphinx and pydoc can parse into HTML documentation automatically.
- Documenting the *valid range* of `rate` (0–1) and the *edge case* for `split_full_name` (single-word names) saves every future caller from reading the function body to discover those constraints.
- The `tuple[str, str]` return type is more informative than just `tuple` — it tells callers exactly how many items to expect and what type each is.

---

## Q3 — Split an Overloaded Function

### Bad code
```python
def process_order(items, customer_email, discount_code):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']

    if discount_code == "SAVE10":
        total = total * 0.90
    elif discount_code == "SAVE20":
        total = total * 0.80
    elif discount_code == "SAVE30":
        total = total * 0.70

    invoice_lines = []
    for item in items:
        line = f"  {item['name']:<20} x{item['quantity']}  ${item['price']:.2f}"
        invoice_lines.append(line)
    invoice_text = "\n".join(invoice_lines)

    message = (f"Dear Customer,\n\n"
               f"Your order total: ${total:.2f}\n\n"
               f"{invoice_text}\n\n"
               f"Thank you!")
    print(f"Sending email to {customer_email}:")
    print(message)

    return total
```

### Refactored
```python
from typing import List, Dict


def calculate_subtotal(items: List[Dict]) -> float:
    """Sum price × quantity for every item in the order."""
    return sum(item['price'] * item['quantity'] for item in items)


def apply_discount(total: float, discount_code: str) -> float:
    """Return the discounted total given a promotional code.

    Unknown codes are ignored (no discount applied).
    """
    discount_rates = {
        "SAVE10": 0.90,
        "SAVE20": 0.80,
        "SAVE30": 0.70,
    }
    multiplier = discount_rates.get(discount_code, 1.0)
    return total * multiplier


def format_invoice(items: List[Dict]) -> str:
    """Build a human-readable invoice body from the order items."""
    lines = [
        f"  {item['name']:<20} x{item['quantity']}  ${item['price']:.2f}"
        for item in items
    ]
    return "\n".join(lines)


def send_order_confirmation(
    customer_email: str, total: float, invoice_text: str
) -> None:
    """Print (or send) the order confirmation email."""
    message = (
        f"Dear Customer,\n\n"
        f"Your order total: ${total:.2f}\n\n"
        f"{invoice_text}\n\n"
        f"Thank you!"
    )
    print(f"Sending email to {customer_email}:")
    print(message)


def process_order(
    items: List[Dict], customer_email: str, discount_code: str
) -> float:
    """Orchestrate the full order processing flow."""
    subtotal      = calculate_subtotal(items)
    final_total   = apply_discount(subtotal, discount_code)
    invoice_text  = format_invoice(items)
    send_order_confirmation(customer_email, final_total, invoice_text)
    return final_total
```

### Why this is better

**Principle: Single Responsibility Principle (SRP)**

- The original function had four distinct jobs. Changing the discount scheme, the email format, the invoice layout, or the price calculation all required editing the same function.
- Each new function has exactly one reason to change. The discount logic lives in `apply_discount` alone — if the business adds a `SAVE40` code, you touch one dictionary in one place.
- The smaller functions are independently testable. You can unit-test `apply_discount` with just a total and a code, without needing any items or email address.
- `process_order` becomes an orchestrator: it reads like a list of steps, which is the clearest possible documentation of the process flow.

---

## Q4 — Remove Magic Numbers

### Bad code
```python
def calculate_invoice(subtotal, is_premium_member, is_international):
    tax = subtotal * 0.08
    if subtotal > 100:
        shipping = 0
    else:
        shipping = 9.99
    if is_premium_member:
        discount = subtotal * 0.15
    else:
        discount = 0
    if is_international:
        shipping = shipping * 2.5
    total = subtotal + tax + shipping - discount
    return round(total, 2)
```

### Refactored
```python
TAX_RATE                   = 0.08   # 8% sales tax
FREE_SHIPPING_THRESHOLD    = 100.00  # orders above this qualify for free shipping
STANDARD_SHIPPING_FEE      = 9.99
PREMIUM_DISCOUNT_RATE      = 0.15   # 15% discount for premium members
INTERNATIONAL_SHIPPING_MULT = 2.5   # international shipping costs 2.5× domestic


def calculate_invoice(
    subtotal: float,
    is_premium_member: bool,
    is_international: bool,
) -> float:
    """Calculate the final invoice total including tax, shipping, and discounts."""
    tax = subtotal * TAX_RATE

    if subtotal > FREE_SHIPPING_THRESHOLD:
        shipping = 0.0
    else:
        shipping = STANDARD_SHIPPING_FEE

    discount = subtotal * PREMIUM_DISCOUNT_RATE if is_premium_member else 0.0

    if is_international:
        shipping *= INTERNATIONAL_SHIPPING_MULT

    total = subtotal + tax + shipping - discount
    return round(total, 2)
```

### Why this is better

**Principle: Avoid Magic Numbers (Clean Code, Chapter 17)**

- Every numeric literal now has a name that explains its meaning. `0.08` becomes `TAX_RATE` — intent is explicit.
- When the tax rate changes, you update one constant at the top of the file. Without constants, you would need to search the entire codebase for `0.08` and guess which occurrences are tax rates vs. something else.
- `UPPER_SNAKE_CASE` for module-level constants is the Python convention (PEP 8). It visually distinguishes constants from variables and parameters.
- The function body now reads like a business rule spec: "charge `TAX_RATE`; give free shipping above `FREE_SHIPPING_THRESHOLD`; etc." — no translation required.

---

## Q5 — Replace Nested Conditions with Early Returns

### Bad code
```python
def get_user_discount(user):
    if user is not None:
        if user.get('is_active'):
            if user.get('subscription') == 'premium':
                if user.get('years_as_customer', 0) >= 5:
                    return 0.30
                else:
                    return 0.20
            else:
                if user.get('years_as_customer', 0) >= 5:
                    return 0.10
                else:
                    return 0.05
        else:
            return 0.0
    else:
        return 0.0
```

### Refactored
```python
def get_user_discount(user: dict | None) -> float:
    """Return the discount rate for a user based on subscription and loyalty.

    Returns:
        0.30 for premium members with 5+ years.
        0.20 for premium members with fewer years.
        0.10 for standard members with 5+ years.
        0.05 for standard members with fewer years.
        0.00 for inactive or missing users.
    """
    if user is None or not user.get('is_active'):
        return 0.0

    is_premium   = user.get('subscription') == 'premium'
    is_loyal     = user.get('years_as_customer', 0) >= 5

    if is_premium and is_loyal:
        return 0.30
    if is_premium:
        return 0.20
    if is_loyal:
        return 0.10
    return 0.05
```

### Why this is better

**Principle: Guard Clauses / Avoid Deep Nesting (Clean Code, Chapter 17)**

- The first thing the original function does is check for `None` and inactivity, but it wraps everything inside those checks instead of returning early. A guard clause inverts the condition and returns immediately, eliminating the nesting.
- After the guard clause, the function knows `user` is valid and active. Everything after that point is the "happy path" — no defensive wrapping needed.
- Introducing named booleans (`is_premium`, `is_loyal`) extracts the condition logic so the `if` statements read like English: "if premium and loyal, give 30%."
- Indentation depth is a complexity signal. Flat code is easier to read, test, and modify than code with 4+ levels of nesting.
- The docstring captures the exact discount table, so callers never have to trace through the logic to know what to expect.

---

> **Exercises:** → [../../exercises/beginner/exercises.md](../../exercises/beginner/exercises.md)
