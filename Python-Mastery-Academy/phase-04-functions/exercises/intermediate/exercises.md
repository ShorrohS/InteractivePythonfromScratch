# Phase 04 — Intermediate Exercises: Functions

> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. Payroll Calculator**

Write these functions:
- `hourly_to_annual(hourly_rate, hours_per_week=40, weeks=52)` → annual salary
- `annual_to_monthly(annual)` → monthly gross
- `calculate_net(gross, tax_rate=0.20, ni_rate=0.12)` → net pay

Print a payslip for an employee earning $32/hour.

---

**Q2. String Utilities Module**

Write these pure string functions:
- `title_case_name(name)` — handles leading/trailing whitespace
- `generate_username(first, last, year)` — `first[0]+last+year[-2:]` all lowercase
- `generate_email(first, last, domain="company.com")`
- `mask_password(pwd)` — shows first char + `*` × (len-2) + last char
- `count_words(text)` — returns word count

---

**Q3. Statistics Functions**

Write without using statistics module:
- `mean(numbers)` → average
- `median(numbers)` → middle value
- `mode(numbers)` → most frequent value
- `std_dev(numbers)` → standard deviation (hint: sqrt(mean of squared deviations))
- `summary(numbers)` → returns dict with all four

---

**Q4. Shopping Cart Functions**

Build these cart functions:
- `create_cart()` → returns empty cart dict
- `add_item(cart, name, price, qty=1)` → modifies cart
- `remove_item(cart, name)` → modifies cart
- `get_total(cart)` → returns total price
- `apply_discount(cart, pct)` → returns new total after discount
- `print_receipt(cart, tax_rate=0.08)` → prints formatted receipt

---

**Q5. Validator Functions**

Write validation functions that return `(bool, str)` tuples — True/False and a message:
- `validate_age(age)` — must be int, 0–120
- `validate_email(email)` — must contain `@` and `.`
- `validate_salary(salary)` — must be positive float
- `validate_password(pwd)` — min 8 chars, 1 digit, 1 uppercase
- `validate_all(**fields)` — runs all validators, returns combined result

---

**Q6. Higher-Order Functions**

Write:
- `apply_to_all(func, items)` — applies a function to each item
- `make_adder(n)` — returns a function that adds n to its argument
- `make_validator(min_val, max_val)` — returns a function that validates a number is in range
- `compose(f, g)` — returns a function that applies g then f

---

**Q7. Recursive Functions**

Write recursive versions of:
- `sum_list(numbers)` — sum without sum()
- `max_list(numbers)` — max without max()
- `count_occurrences(lst, target)` — count without .count()
- `palindrome_check(s)` — check if string reads same forwards/backwards

---

**Q8. Data Pipeline with Lambda**

Given a list of sales records:
```python
sales = [
    {"rep": "Alice", "region": "North", "amount": 5200, "month": "Jan"},
    {"rep": "Bob",   "region": "South", "amount": 3100, "month": "Jan"},
    ...
]
```
Using `sorted`, `filter`, `map`:
- Get all sales over $4000
- Sort by amount descending
- Extract just `rep: amount` pairs
- Calculate total

---

**Q9. Memoisation**

Write a `memoize(func)` decorator-style function that:
- Caches results in a dict
- Returns cached result if called with same args
- Count how many times the original function was actually called

Test with a slow fibonacci function.

---

**Q10. Currying**

Write a `curry(func)` function that transforms:
```python
add(1, 2, 3)  →  curry(add)(1)(2)(3)
```

---

> **Solutions:** `../../solutions/intermediate/solutions.md`
