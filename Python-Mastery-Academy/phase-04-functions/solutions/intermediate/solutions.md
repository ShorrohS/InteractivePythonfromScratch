# Phase 04 — Intermediate Solutions: Functions

---

## Q1. Payroll Calculator

```python
def hourly_to_annual(hourly_rate: float, hours_per_week: float = 40, weeks: int = 52) -> float:
    return hourly_rate * hours_per_week * weeks

def annual_to_monthly(annual: float) -> float:
    return annual / 12

def calculate_net(gross: float, tax_rate: float = 0.20, ni_rate: float = 0.12) -> dict:
    tax = gross * tax_rate
    ni  = gross * ni_rate
    net = gross - tax - ni
    return {"gross": gross, "tax": round(tax,2), "ni": round(ni,2), "net": round(net,2)}

rate    = 32.00
annual  = hourly_to_annual(rate)
monthly = annual_to_monthly(annual)
payslip = calculate_net(monthly)
print(f"Hourly: ${rate:.2f} | Annual: ${annual:,.0f} | Monthly: ${monthly:,.2f}")
print(f"Tax: ${payslip['tax']:,.2f} | NI: ${payslip['ni']:,.2f} | Net: ${payslip['net']:,.2f}")
```

---

## Q2. String Utilities

```python
def title_case_name(name: str) -> str:
    return name.strip().title()

def generate_username(first: str, last: str, year: int) -> str:
    return (first[0] + last + str(year)[-2:]).lower()

def generate_email(first: str, last: str, domain: str = "company.com") -> str:
    return f"{first.lower()}.{last.lower()}@{domain}"

def mask_password(pwd: str) -> str:
    if len(pwd) <= 2:
        return "*" * len(pwd)
    return pwd[0] + "*" * (len(pwd) - 2) + pwd[-1]

def count_words(text: str) -> int:
    return len(text.split())

print(title_case_name("  alice johnson  "))
print(generate_username("Alice", "Johnson", 1994))
print(generate_email("Alice", "Johnson"))
print(mask_password("MySecret123"))
print(count_words("Python is awesome"))
```

---

## Q3. Statistics Functions

```python
import math

def mean(numbers: list) -> float:
    return sum(numbers) / len(numbers)

def median(numbers: list) -> float:
    s = sorted(numbers)
    n = len(s)
    return s[n//2] if n % 2 else (s[n//2-1] + s[n//2]) / 2

def mode(numbers: list) -> float:
    freq = {}
    for n in numbers:
        freq[n] = freq.get(n, 0) + 1
    return max(freq, key=freq.get)

def std_dev(numbers: list) -> float:
    avg = mean(numbers)
    variance = mean([(x - avg)**2 for x in numbers])
    return round(math.sqrt(variance), 4)

def summary(numbers: list) -> dict:
    return {
        "mean":    round(mean(numbers), 2),
        "median":  median(numbers),
        "mode":    mode(numbers),
        "std_dev": std_dev(numbers)
    }

data = [4, 7, 2, 9, 4, 5, 8, 4, 3, 6]
print(summary(data))
```

---

## Q4. Shopping Cart

```python
def create_cart() -> dict:
    return {"items": {}, "discount": 0.0}

def add_item(cart: dict, name: str, price: float, qty: int = 1) -> None:
    if name in cart["items"]:
        cart["items"][name]["qty"] += qty
    else:
        cart["items"][name] = {"price": price, "qty": qty}

def remove_item(cart: dict, name: str) -> bool:
    return cart["items"].pop(name, None) is not None

def get_total(cart: dict) -> float:
    return sum(i["price"] * i["qty"] for i in cart["items"].values())

def apply_discount(cart: dict, pct: float) -> float:
    total = get_total(cart)
    return total * (1 - pct / 100)

def print_receipt(cart: dict, tax_rate: float = 0.08) -> None:
    print("=" * 40)
    subtotal = get_total(cart)
    tax = subtotal * tax_rate
    for name, info in cart["items"].items():
        line = info["price"] * info["qty"]
        print(f"  {name:<18} {info['qty']}x ${line:.2f}")
    print("-" * 40)
    print(f"  {'Subtotal':<20} ${subtotal:.2f}")
    print(f"  {'Tax':<20} ${tax:.2f}")
    print(f"  {'TOTAL':<20} ${subtotal+tax:.2f}")
    print("=" * 40)

cart = create_cart()
add_item(cart, "Laptop", 999.99)
add_item(cart, "Mouse", 29.99, 2)
print_receipt(cart)
```

---

## Q5. Validators

```python
def validate_age(age) -> tuple:
    if not isinstance(age, int):
        return False, "Age must be an integer"
    if not 0 <= age <= 120:
        return False, f"Age {age} out of range (0-120)"
    return True, "Valid"

def validate_email(email: str) -> tuple:
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Invalid email format"
    return True, "Valid"

def validate_password(pwd: str) -> tuple:
    if len(pwd) < 8:
        return False, "Min 8 characters"
    if not any(c.isdigit() for c in pwd):
        return False, "Must contain a digit"
    if not any(c.isupper() for c in pwd):
        return False, "Must contain uppercase"
    return True, "Valid"

print(validate_age(25))
print(validate_email("alice@example.com"))
print(validate_password("Secure1"))
```

---

## Q6. Higher-Order Functions

```python
def apply_to_all(func, items):
    return [func(item) for item in items]

def make_adder(n: float):
    return lambda x: x + n

def make_validator(min_val, max_val):
    return lambda x: min_val <= x <= max_val

def compose(f, g):
    return lambda x: f(g(x))

add5 = make_adder(5)
print(apply_to_all(add5, [1, 2, 3]))     # [6, 7, 8]

is_teen = make_validator(13, 19)
print(is_teen(15))    # True
print(is_teen(25))    # False

double_then_add5 = compose(add5, lambda x: x * 2)
print(double_then_add5(3))   # 11
```

---

## Q7. Recursive Functions

```python
def sum_list(numbers: list) -> float:
    if not numbers:
        return 0
    return numbers[0] + sum_list(numbers[1:])

def max_list(numbers: list) -> float:
    if len(numbers) == 1:
        return numbers[0]
    rest_max = max_list(numbers[1:])
    return numbers[0] if numbers[0] > rest_max else rest_max

def count_occurrences(lst: list, target) -> int:
    if not lst:
        return 0
    return (1 if lst[0] == target else 0) + count_occurrences(lst[1:], target)

def palindrome_check(s: str) -> bool:
    s = s.lower().replace(" ", "")
    if len(s) <= 1:
        return True
    return s[0] == s[-1] and palindrome_check(s[1:-1])

print(sum_list([1, 2, 3, 4, 5]))          # 15
print(max_list([3, 7, 2, 9, 1]))           # 9
print(count_occurrences([1,2,3,2,1], 2))   # 2
print(palindrome_check("racecar"))         # True
print(palindrome_check("hello"))           # False
```
