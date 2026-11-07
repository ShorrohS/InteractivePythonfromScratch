# Phase 01 — Intermediate Exercise Solutions

---

## Q1. Salary Calculator

```python
name       = input("Name: ").strip().title()
annual     = float(input("Annual salary ($): "))
tax_rate   = float(input("Tax rate (%): ")) / 100
bonus      = float(input("Bonus amount ($): "))

monthly_gross = annual / 12
annual_tax    = annual * tax_rate
take_home     = annual - annual_tax
monthly_net   = take_home / 12
total         = annual + bonus

print(f"\n{'=' * 40}")
print(f"  SALARY REPORT — {name}")
print(f"{'=' * 40}")
print(f"  {'Annual Gross:':<25} ${annual:>10,.2f}")
print(f"  {'Monthly Gross:':<25} ${monthly_gross:>10,.2f}")
print(f"  {'Annual Tax ({:.0f}%):'.format(tax_rate*100):<25} ${annual_tax:>10,.2f}")
print(f"  {'Annual Take-Home:':<25} ${take_home:>10,.2f}")
print(f"  {'Monthly Take-Home:':<25} ${monthly_net:>10,.2f}")
print(f"  {'Bonus:':<25} ${bonus:>10,.2f}")
print(f"  {'Total Earnings:':<25} ${total:>10,.2f}")
```

---

## Q2. Temperature Converter

```python
value = float(input("Enter temperature: "))
unit  = input("Unit (C/F/K): ").strip().upper()

if unit == "C":
    c = value
    f = (c * 9/5) + 32
    k = c + 273.15
elif unit == "F":
    f = value
    c = (f - 32) * 5/9
    k = c + 273.15
elif unit == "K":
    k = value
    c = k - 273.15
    f = (c * 9/5) + 32
else:
    print("Invalid unit. Use C, F, or K.")
    exit()

print(f"\n  Celsius:    {c:.2f} C")
print(f"  Fahrenheit: {f:.2f} F")
print(f"  Kelvin:     {k:.2f} K")
```

---

## Q3. String Statistics

```python
sentence = input("Enter a sentence: ").strip()
words    = sentence.split()
vowels   = sum(1 for ch in sentence.lower() if ch in "aeiou")

# Word frequency
freq = {}
for w in words:
    w = w.lower().strip(".,!?")
    freq[w] = freq.get(w, 0) + 1

most_common = max(freq, key=freq.get)

print(f"\n  Original:   {sentence}")
print(f"  UPPER:      {sentence.upper()}")
print(f"  lower:      {sentence.lower()}")
print(f"  Title:      {sentence.title()}")
print(f"  Words:      {len(words)}")
print(f"  Chars (w/ spaces): {len(sentence)}")
print(f"  Chars (no spaces): {len(sentence.replace(' ', ''))}")
print(f"  Vowels:     {vowels}")
print(f"  Most used:  '{most_common}' ({freq[most_common]} times)")
```

---

## Q4. Product Price Tag Generator

```python
name      = input("Product name: ").strip()
original  = float(input("Original price ($): "))
discount  = float(input("Discount (%): ")) / 100
tax_rate  = float(input("Tax rate (%): ")) / 100

disc_amt   = original * discount
discounted = original - disc_amt
tax_amt    = discounted * tax_rate
final      = discounted + tax_amt
savings    = original - final

border = "=" * 42
print(f"\n{border}")
print(f"|{name:^40}|")
print(f"|{'-'*40}|")
print(f"|  {'Original Price:':<22} ${original:>12.2f}  |")
print(f"|  {'Discount ({:.0f}%):'.format(discount*100):<22} -${disc_amt:>11.2f}  |")
print(f"|  {'Discounted Price:':<22} ${discounted:>12.2f}  |")
print(f"|  {'Tax ({:.1f}%):'.format(tax_rate*100):<22} +${tax_amt:>11.2f}  |")
print(f"|{'-'*40}|")
print(f"|  {'FINAL PRICE:':<22} ${final:>12.2f}  |")
print(f"|  {'YOU SAVE:':<22} ${savings:>12.2f}  |")
print(f"{border}")
```

---

## Q5. Personal Finance Summary

```python
categories = ["Rent", "Food", "Transport", "Utilities", "Entertainment"]
expenses = {}

for cat in categories:
    amt = float(input(f"  {cat}: $"))
    expenses[cat] = amt

total   = sum(expenses.values())
average = total / len(expenses)
highest = max(expenses, key=expenses.get)
lowest  = min(expenses, key=expenses.get)
income  = 5000
pct     = (total / income) * 100

print(f"\n  Monthly Expenses Summary")
print(f"  {'Category':<15} {'Amount':>10}")
print(f"  {'-'*26}")
for cat, amt in expenses.items():
    print(f"  {cat:<15} ${amt:>9.2f}")
print(f"  {'-'*26}")
print(f"  {'TOTAL':<15} ${total:>9.2f}")
print(f"\n  Average expense:  ${average:.2f}")
print(f"  Highest: {highest} (${expenses[highest]:.2f})")
print(f"  Lowest:  {lowest} (${expenses[lowest]:.2f})")
print(f"  % of $5,000 income: {pct:.1f}%")
```

---

## Q6. Data Type Detective

```python
raw = input("Enter any value: ").strip()

# Detect type
if raw.lower() in ("true", "false"):
    detected = bool
    converted = raw.lower() == "true"
else:
    try:
        converted = int(raw)
        detected = int
    except ValueError:
        try:
            converted = float(raw)
            detected = float
        except ValueError:
            converted = raw
            detected = str

print(f"\n  Input:     '{raw}'")
print(f"  Type:      {detected.__name__}")
print(f"  Converted: {converted}")
print(f"  bool():    {bool(converted)}")
```

---

## Q7. Receipt Generator

```python
n = int(input("How many items (1-5)? "))
items = []

for i in range(n):
    name  = input(f"  Item {i+1} name: ").strip().title()
    qty   = int(input(f"  Quantity: "))
    price = float(input(f"  Unit price ($): "))
    items.append((name, qty, price))

subtotal = sum(q * p for _, q, p in items)
tax      = subtotal * 0.085
total    = subtotal + tax
border   = "=" * 45

print(f"\n{border}")
print(f"|{'RECEIPT':^43}|")
print(f"{border}")
for name, qty, price in items:
    line_total = qty * price
    print(f"  {name:<20} {qty} x ${price:.2f} = ${line_total:.2f}")
print(f"  {'-'*41}")
print(f"  {'Subtotal:':<30} ${subtotal:.2f}")
print(f"  {'Tax (8.5%):':<30} ${tax:.2f}")
print(f"  {'TOTAL:':<30} ${total:.2f}")
print(f"{border}")
print(f"|{'THANK YOU!':^43}|")
print(f"{border}")
```

---

## Q8. Number Analyser

```python
import math

raw = input("Enter a number: ").strip()
try:
    num = float(raw)
except ValueError:
    print("Not a valid number.")
    exit()

print(f"\n  Number:    {num}")
print(f"  Positive:  {num > 0}")
print(f"  Negative:  {num < 0}")
print(f"  Zero:      {num == 0}")

if num == int(num):
    print(f"  Even:      {int(num) % 2 == 0}")
    print(f"  Odd:       {int(num) % 2 != 0}")

print(f"  Div by 7:  {num % 7 == 0}")
if num >= 0:
    print(f"  Sqrt:      {math.sqrt(num):.4f}")
print(f"  Squared:   {num ** 2:,.0f}")
print(f"  Cubed:     {num ** 3:,.0f}")
```

---

## Q9. Username & Password Validator

```python
username = input("Username: ").strip()
password = input("Password: ").strip()

u_len  = len(username) >= 4
u_chars = all(c.isalnum() or c == "_" for c in username)
u_space = " " not in username

p_len   = len(password) >= 8
p_digit = any(c.isdigit() for c in password)
p_upper = any(c.isupper() for c in password)

print("\n  USERNAME CHECKS:")
print(f"    Min 4 chars:        {'PASS' if u_len else 'FAIL'}")
print(f"    Valid chars only:   {'PASS' if u_chars else 'FAIL'}")
print(f"    No spaces:          {'PASS' if u_space else 'FAIL'}")

print("\n  PASSWORD CHECKS:")
print(f"    Min 8 chars:        {'PASS' if p_len else 'FAIL'}")
print(f"    Contains digit:     {'PASS' if p_digit else 'FAIL'}")
print(f"    Contains uppercase: {'PASS' if p_upper else 'FAIL'}")

all_pass = u_len and u_chars and u_space and p_len and p_digit and p_upper
print(f"\n  Overall: {'VALID' if all_pass else 'INVALID'}")
```

---

## Q10. Age in Different Units

```python
name       = input("Name: ").strip().title()
birth_year = int(input("Birth year: "))
current    = 2024

age_years  = current - birth_year
age_months = age_years * 12
age_weeks  = age_years * 52
age_days   = age_years * 365
age_hours  = age_days * 24
turn_100   = birth_year + 100

print(f"\n  Hello, {name}!")
print(f"  You are approximately:")
print(f"    {age_years:,}      years old")
print(f"    {age_months:,}    months old")
print(f"    {age_weeks:,}     weeks old")
print(f"    {age_days:,}   days old")
print(f"    {age_hours:,} hours old")
print(f"\n  You will turn 100 in {turn_100}.")
```
