# Lesson 04 — Refactoring Techniques

**Phase:** 19 — Software Engineering | **Time:** ~50 min | **Prerequisite:** Lesson 03 — SOLID Principles

---

## Learning Objectives

- Apply extract-function and rename-variable refactoring to messy code
- Replace magic numbers with named constants
- Eliminate duplication using the DRY principle
- Replace long if/elif chains with polymorphism
- Recognise when refactoring is the right move versus when to leave code alone

---

## Part 1: What Is Refactoring?

Refactoring is changing the internal structure of code **without changing its external behaviour**. The goal is to make the code easier to read, test, and extend — not to add features.

Two rules:
1. Run the tests before you start. If there are no tests, write them first.
2. Make small, incremental changes and verify after each one. Big rewrites break things.

---

## Part 2: Extract Function

When a block of code does a distinct sub-task, extract it into its own named function. The name communicates intent; the body shows how.

```python
# ── BEFORE: one big block with inline comments propping up readability ──────

def generate_invoice_email(order: dict) -> str:
    # Build greeting
    greeting = f"Dear {order['customer_name']},"

    # Calculate totals
    subtotal = 0.0
    for item in order["items"]:
        subtotal += item["price"] * item["qty"]
    tax = round(subtotal * 0.10, 2)
    total = round(subtotal + tax, 2)

    # Build item table
    rows = ""
    for item in order["items"]:
        line_total = item["price"] * item["qty"]
        rows += f"  {item['name']:<30} ${line_total:>8.2f}\n"

    # Assemble email
    body = (
        f"{greeting}\n\n"
        f"Thank you for your order #{order['order_id']}.\n\n"
        f"Items:\n{rows}\n"
        f"  Subtotal: ${subtotal:.2f}\n"
        f"  Tax:      ${tax:.2f}\n"
        f"  Total:    ${total:.2f}\n\n"
        f"Your order will be dispatched within 2 business days."
    )
    return body


# ── AFTER: each function does one job ───────────────────────────────────────

TAX_RATE = 0.10


def _calculate_order_totals(items: list[dict]) -> tuple[float, float, float]:
    subtotal = sum(item["price"] * item["qty"] for item in items)
    tax = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + tax, 2)
    return subtotal, tax, total


def _format_item_table(items: list[dict]) -> str:
    lines = []
    for item in items:
        line_total = item["price"] * item["qty"]
        lines.append(f"  {item['name']:<30} ${line_total:>8.2f}")
    return "\n".join(lines)


def generate_invoice_email(order: dict) -> str:
    subtotal, tax, total = _calculate_order_totals(order["items"])
    item_table = _format_item_table(order["items"])
    return (
        f"Dear {order['customer_name']},\n\n"
        f"Thank you for your order #{order['order_id']}.\n\n"
        f"Items:\n{item_table}\n\n"
        f"  Subtotal: ${subtotal:.2f}\n"
        f"  Tax:      ${tax:.2f}\n"
        f"  Total:    ${total:.2f}\n\n"
        f"Your order will be dispatched within 2 business days."
    )
```

The "after" version is testable in pieces: you can unit-test `_calculate_order_totals` without touching any email logic.

---

## Part 3: Replace Magic Numbers with Constants

A magic number is a bare numeric literal whose meaning is not obvious from context. Naming it once makes every use self-documenting.

```python
# ── BEFORE: readers must guess what each number means ───────────────────────

def calculate_loan_payment(principal: float, annual_rate: float, years: int) -> float:
    monthly_rate = annual_rate / 12 / 100        # why /12? why /100?
    months = years * 12                           # why *12?
    if monthly_rate == 0:
        return principal / months
    factor = (1 + monthly_rate) ** months
    return principal * monthly_rate * factor / (factor - 1)

def categorise_bmi(weight_kg: float, height_m: float) -> str:
    bmi = weight_kg / (height_m ** 2)
    if bmi < 18.5:      # magic
        return "Underweight"
    if bmi < 25.0:      # magic
        return "Normal"
    if bmi < 30.0:      # magic
        return "Overweight"
    return "Obese"


# ── AFTER: named constants make the domain visible ──────────────────────────

MONTHS_PER_YEAR = 12
PERCENT_TO_DECIMAL = 100

BMI_UNDERWEIGHT_THRESHOLD = 18.5
BMI_NORMAL_THRESHOLD      = 25.0
BMI_OVERWEIGHT_THRESHOLD  = 30.0


def calculate_loan_payment(principal: float, annual_rate: float, years: int) -> float:
    monthly_rate = annual_rate / MONTHS_PER_YEAR / PERCENT_TO_DECIMAL
    months = years * MONTHS_PER_YEAR
    if monthly_rate == 0:
        return principal / months
    factor = (1 + monthly_rate) ** months
    return principal * monthly_rate * factor / (factor - 1)


def categorise_bmi(weight_kg: float, height_m: float) -> str:
    bmi = weight_kg / (height_m ** 2)
    if bmi < BMI_UNDERWEIGHT_THRESHOLD:
        return "Underweight"
    if bmi < BMI_NORMAL_THRESHOLD:
        return "Normal"
    if bmi < BMI_OVERWEIGHT_THRESHOLD:
        return "Overweight"
    return "Obese"
```

---

## Part 4: DRY — Don't Repeat Yourself

Every piece of knowledge should have a **single, authoritative representation** in the codebase. Duplication means two places to update when something changes, and two chances to introduce a bug.

```python
# ── BEFORE: same validation logic copy-pasted in three places ───────────────

def create_employee(name: str, email: str, salary: float) -> dict:
    if not name or not name.strip():
        raise ValueError("Name cannot be blank")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Invalid email address")
    if salary < 0:
        raise ValueError("Salary cannot be negative")
    return {"name": name.strip(), "email": email.lower(), "salary": salary}


def update_employee(emp_id: int, name: str, email: str, salary: float) -> dict:
    if not name or not name.strip():          # DUPLICATED
        raise ValueError("Name cannot be blank")
    if "@" not in email or "." not in email.split("@")[-1]:  # DUPLICATED
        raise ValueError("Invalid email address")
    if salary < 0:                            # DUPLICATED
        raise ValueError("Salary cannot be negative")
    return {"id": emp_id, "name": name.strip(), "email": email.lower(), "salary": salary}


# ── AFTER: validation extracted once, reused everywhere ─────────────────────

def _validate_employee_fields(name: str, email: str, salary: float) -> None:
    """Raise ValueError if any employee field is invalid."""
    if not name or not name.strip():
        raise ValueError("Name cannot be blank")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Invalid email address")
    if salary < 0:
        raise ValueError("Salary cannot be negative")


def create_employee(name: str, email: str, salary: float) -> dict:
    _validate_employee_fields(name, email, salary)
    return {"name": name.strip(), "email": email.lower(), "salary": salary}


def update_employee(emp_id: int, name: str, email: str, salary: float) -> dict:
    _validate_employee_fields(name, email, salary)
    return {"id": emp_id, "name": name.strip(), "email": email.lower(), "salary": salary}
```

Now the validation logic lives in one place. Fix a bug there, fix it everywhere.

---

## Part 5: Replace Conditional with Polymorphism

Long if/elif chains that switch on a type or category are a sign that polymorphism would be cleaner. Each branch becomes a separate class.

```python
# ── BEFORE: growing if/elif chain ───────────────────────────────────────────

def calculate_shipping(method: str, weight_kg: float, distance_km: float) -> float:
    if method == "standard":
        base = 3.00
        rate = 0.005
    elif method == "express":
        base = 8.00
        rate = 0.012
    elif method == "overnight":
        base = 15.00
        rate = 0.025
    elif method == "freight":
        base = 2.00
        rate = 0.003
    else:
        raise ValueError(f"Unknown shipping method: {method}")
    return round(base + rate * weight_kg * distance_km, 2)


# ── AFTER: one class per method, no conditionals in the caller ───────────────

from abc import ABC, abstractmethod


class ShippingMethod(ABC):
    @abstractmethod
    def calculate(self, weight_kg: float, distance_km: float) -> float:
        ...


class StandardShipping(ShippingMethod):
    BASE_FEE = 3.00
    RATE = 0.005

    def calculate(self, weight_kg: float, distance_km: float) -> float:
        return round(self.BASE_FEE + self.RATE * weight_kg * distance_km, 2)


class ExpressShipping(ShippingMethod):
    BASE_FEE = 8.00
    RATE = 0.012

    def calculate(self, weight_kg: float, distance_km: float) -> float:
        return round(self.BASE_FEE + self.RATE * weight_kg * distance_km, 2)


class OvernightShipping(ShippingMethod):
    BASE_FEE = 15.00
    RATE = 0.025

    def calculate(self, weight_kg: float, distance_km: float) -> float:
        return round(self.BASE_FEE + self.RATE * weight_kg * distance_km, 2)


class FreightShipping(ShippingMethod):
    BASE_FEE = 2.00
    RATE = 0.003

    def calculate(self, weight_kg: float, distance_km: float) -> float:
        return round(self.BASE_FEE + self.RATE * weight_kg * distance_km, 2)


SHIPPING_REGISTRY: dict[str, ShippingMethod] = {
    "standard":  StandardShipping(),
    "express":   ExpressShipping(),
    "overnight": OvernightShipping(),
    "freight":   FreightShipping(),
}


def calculate_shipping(method: str, weight_kg: float, distance_km: float) -> float:
    if method not in SHIPPING_REGISTRY:
        raise ValueError(f"Unknown shipping method: {method}")
    return SHIPPING_REGISTRY[method].calculate(weight_kg, distance_km)


# Adding a new method: create a class, add one entry to the registry.
# Zero changes to existing code.
class DroneShipping(ShippingMethod):
    BASE_FEE = 20.00
    RATE = 0.008

    def calculate(self, weight_kg: float, distance_km: float) -> float:
        return round(self.BASE_FEE + self.RATE * weight_kg * distance_km, 2)

SHIPPING_REGISTRY["drone"] = DroneShipping()
```

---

## Key Takeaways

- **Extract function** when a block of code has a distinct purpose; name it after what it does, not how it does it
- **Named constants** replace magic numbers and make the business domain visible in the code
- **DRY** is not about removing all repetition — it is about removing duplicated **knowledge**; similar-looking code that represents different things should stay separate
- **Replace conditional with polymorphism** when an if/elif grows because you keep adding new types or categories
- Refactor in small steps with tests running after each change; never refactor without a safety net

---

## What's Next

**[Lesson 05 → Documentation](lesson-05-documentation.md)**

We cover Google-style and NumPy-style docstrings, type annotations, the Sphinx workflow, and README best practices for open-source and team projects.
