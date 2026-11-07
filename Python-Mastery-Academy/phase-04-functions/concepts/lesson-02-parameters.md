# Lesson 02 — Parameters and Return Values

**Phase:** 04 — Functions | **Time:** ~30 min

---

## Part 1: Parameters vs Arguments

```
PARAMETER — the variable name in the function definition
ARGUMENT  — the actual value you pass when calling

def greet(name):       ← 'name' is the PARAMETER
    print(name)

greet("Alice")         ← "Alice" is the ARGUMENT
```

---

## Part 2: Positional Parameters

Arguments matched by position:

```python
def describe_product(name: str, price: float, qty: int) -> str:
    return f"{qty}x {name} @ ${price:.2f} = ${price * qty:.2f}"

# Must be in correct order
print(describe_product("Laptop", 999.99, 3))
# 3x Laptop @ $999.99 = $2999.97

# Wrong order = wrong result (no error raised!)
print(describe_product(3, 999.99, "Laptop"))   # TypeError
```

---

## Part 3: Keyword Arguments

Pass by name — order doesn't matter:

```python
def create_user(first: str, last: str, age: int, role: str) -> dict:
    return {"name": f"{first} {last}", "age": age, "role": role}

# Keyword — order is flexible
user = create_user(last="Johnson", first="Alice", role="admin", age=30)
print(user)

# Mix positional + keyword (positional must come first)
user = create_user("Bob", "Smith", role="editor", age=25)
```

---

## Part 4: Return Values

```python
# Single return value
def square(n: float) -> float:
    return n ** 2

result = square(7)    # 49

# Multiple return values (returns a tuple)
def min_max(numbers: list[float]) -> tuple[float, float]:
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 8, 5, 2])
print(low, high)     # 1 8

# Return with early exit
def divide_safe(a: float, b: float) -> float | None:
    if b == 0:
        return None          # early return on error
    return a / b

result = divide_safe(10, 0)
if result is None:
    print("Cannot divide by zero")
```

---

## Part 5: Type Hints — Professional Standard

```python
# Without hints — ambiguous
def process(x, y):
    return x * y

# With hints — clear contract
def calculate_area(length: float, width: float) -> float:
    """Calculate rectangle area."""
    return length * width

# Complex types
from typing import Optional

def find_user(user_id: int) -> Optional[dict]:
    """Returns user dict or None if not found."""
    users = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    return users.get(user_id)

# List and dict hints
def average(scores: list[float]) -> float:
    return sum(scores) / len(scores)

def get_config(defaults: dict[str, str]) -> dict[str, str]:
    return {"host": "localhost", **defaults}
```

---

## Part 6: Business Example

```python
def calculate_invoice(
    items: list[dict],
    tax_rate: float = 0.08,
    discount_pct: float = 0.0
) -> dict:
    """
    Calculate invoice totals.
    
    Args:
        items: List of {'name', 'qty', 'unit_price'} dicts
        tax_rate: Tax rate as decimal (default 8%)
        discount_pct: Discount as decimal (default 0%)
    
    Returns:
        Dict with subtotal, discount, tax, and total
    """
    subtotal = sum(i["qty"] * i["unit_price"] for i in items)
    discount = subtotal * discount_pct
    taxable  = subtotal - discount
    tax      = taxable * tax_rate
    total    = taxable + tax

    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "tax":      round(tax, 2),
        "total":    round(total, 2)
    }

# Usage
order = [
    {"name": "Laptop",   "qty": 1, "unit_price": 999.99},
    {"name": "Mouse",    "qty": 2, "unit_price": 29.99},
    {"name": "Keyboard", "qty": 1, "unit_price": 79.99},
]

invoice = calculate_invoice(order, tax_rate=0.10, discount_pct=0.05)
for k, v in invoice.items():
    print(f"  {k.title():<12} ${v:,.2f}")
```

---

## Part 7: Common Mistakes

```python
# Mistake 1: Mutable default argument — classic Python trap
def add_item(item, lst=[]):      # DANGEROUS: lst shared across calls!
    lst.append(item)
    return lst

add_item("a")   # ['a']
add_item("b")   # ['a', 'b']  ← unexpected!

# Fix: use None as default
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

# Mistake 2: Ignoring return value
def get_total(prices):
    return sum(prices)

get_total([10, 20, 30])   # return value ignored — lost!
total = get_total([10, 20, 30])   # correct: assign it
```

---

## Practice Exercises

1. Write a function `calculate_bmi(weight_kg, height_m)` that returns BMI and category.

2. Write a function `split_bill(total, people, tip_pct=15)` that returns per-person amount.

3. Write a function `password_info(pwd)` that returns a tuple: (length, has_digit, has_upper, is_strong).

4. What is the bug?
   ```python
   def process(data=[]):
       data.append(1)
       return data
   print(process())
   print(process())
   ```

---

## Next Lesson

**[Lesson 03 → Default Arguments](lesson-03-defaults.md)**
