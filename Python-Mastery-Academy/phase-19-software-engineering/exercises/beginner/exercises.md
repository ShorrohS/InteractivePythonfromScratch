# 📝 Phase 19 — Beginner Exercises

> Each exercise shows **bad code that actually works** — it runs, but it violates clean code principles.
> Your tasks:
> 1. Read the bad code and identify what is wrong.
> 2. Rewrite it to fix the issue.
>
> Solutions: `../../solutions/beginner/solutions.md`

---

## Q1 — Rename for Clarity ⭐

The function below works correctly, but the names make it impossible to understand without running it.

```python
def f(x, y, z):
    a = x * y
    b = a * z
    c = a + b
    return c


r = f(5, 12.99, 0.08)
print(r)
```

**Context clue:** `5` is a quantity, `12.99` is a unit price, `0.08` is a tax rate.

**What to look for:**
- What does `f` calculate? What should it be called?
- What do `x`, `y`, `z`, `a`, `b`, `c`, `r` each represent?
- After renaming, someone should understand the logic without any comments.

**Expected improvement:** The function and every variable have meaningful names. A reader can understand the calculation in one pass.

---

## Q2 — Add Docstrings and Type Hints ⭐

These three functions have no documentation and no type annotations. Add Google-style docstrings and full type hints to all three.

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

**What to look for:**
- What is the type of each parameter? What does each function return?
- What are the valid ranges or formats for `rate` and `full_name`?
- Which edge cases are worth calling out? (`rate` must be 0–1; a name with only one word.)
- Google docstring format: `Args:`, `Returns:`, `Raises:` sections.

**Expected improvement:** All three functions have type annotations on parameters and return values, plus a Google-style docstring explaining purpose, args, return value, and any exceptions.

---

## Q3 — Split an Overloaded Function ⭐

This single function does four separate things. Break it into smaller functions, each with one responsibility.

```python
def process_order(items, customer_email, discount_code):
    # Calculate total
    total = 0
    for item in items:
        total += item['price'] * item['quantity']

    # Apply discount
    if discount_code == "SAVE10":
        total = total * 0.90
    elif discount_code == "SAVE20":
        total = total * 0.80
    elif discount_code == "SAVE30":
        total = total * 0.70

    # Format invoice lines
    invoice_lines = []
    for item in items:
        line = f"  {item['name']:<20} x{item['quantity']}  ${item['price']:.2f}"
        invoice_lines.append(line)
    invoice_text = "\n".join(invoice_lines)

    # Send confirmation email
    message = (f"Dear Customer,\n\n"
               f"Your order total: ${total:.2f}\n\n"
               f"{invoice_text}\n\n"
               f"Thank you!")
    print(f"Sending email to {customer_email}:")
    print(message)

    return total
```

**What to look for:**
- Count the distinct jobs this function does (hint: four comments = four responsibilities).
- What would you need to change if the discount rules changed?  
- What if the email body format changed?  
- Which parts could be reused by another function elsewhere?

**Expected improvement:** Four short, focused functions. The original `process_order` becomes an orchestrator that calls them in sequence.

---

## Q4 — Remove Magic Numbers ⭐

The function below is littered with bare numeric literals. Replace each one with a named constant defined at module level.

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

**What to look for:**
- What does each number mean? (`0.08` = tax rate, `100` = free-shipping threshold, `9.99` = standard shipping fee, `0.15` = premium discount rate, `2.5` = international shipping multiplier)
- If the tax rate changes to 0.09, how many places need updating?
- Constants should be named in `UPPER_SNAKE_CASE` at the top of the module.

**Expected improvement:** Every number has a descriptive name. The logic inside `calculate_invoice` contains zero bare literals.

---

## Q5 — Replace Nested Conditions with Early Returns ⭐

The deeply nested logic below is hard to follow. Refactor it using early returns (guard clauses) to produce a flat, easy-to-read structure.

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

**What to look for:**
- What is the *first* condition that returns `0.0`? Move that check to the very top and return immediately — that is a guard clause.
- After inverting each outer `if`, you eliminate the entire nesting level.
- After the refactor, every `return` line should be at the same indentation level (no nested `if` blocks).

**Expected improvement:** Zero nesting beyond one level. The happy path reads top to bottom without any `else` branches.

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
