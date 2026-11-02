# Lesson 05 — Operators

**Phase:** 01 — Fundamentals | **Time:** ~45 min | **Prerequisite:** Lesson 04

---

## Part 1: Arithmetic Operators

```python
a = 17
b = 5

print(a + b)    # 22  — Addition
print(a - b)    # 12  — Subtraction
print(a * b)    # 85  — Multiplication
print(a / b)    # 3.4 — Division (always float)
print(a // b)   # 3   — Floor Division (no decimal)
print(a % b)    # 2   — Modulo (remainder)
print(a ** b)   # 1419857 — Exponentiation (a to the power b)
```

### When to use each:

| Operator | Use Case |
|----------|---------|
| `+` | Adding prices, scores, quantities |
| `-` | Subtracting costs, finding differences |
| `*` | Calculating total (price × quantity) |
| `/` | Dividing amounts (split bill) |
| `//` | How many full groups fit |
| `%` | Check if even/odd, cyclic operations |
| `**` | Compound interest, geometric calculations |

### Modulo practical uses:

```python
# Is a number even or odd?
n = 17
if n % 2 == 0:
    print("Even")
else:
    print("Odd")

# Every 5th item gets a discount
item_number = 15
if item_number % 5 == 0:
    print("Apply discount!")

# Hours from total minutes
total_minutes = 137
hours = total_minutes // 60    # 2
minutes = total_minutes % 60   # 17
print(f"{hours}h {minutes}m")  # 2h 17m
```

---

## Part 2: Assignment Operators

Shortcut operators that modify a variable in-place:

```python
score = 100

score += 10     # score = score + 10  → 110
score -= 5      # score = score - 5   → 105
score *= 2      # score = score * 2   → 210
score /= 3      # score = score / 3   → 70.0
score //= 2     # score = score // 2  → 35.0
score %= 8      # score = score % 8   → 3.0
score **= 2     # score = score ** 2  → 9.0
```

---

## Part 3: Comparison Operators

Return `True` or `False`:

```python
a = 10
b = 20

print(a == b)    # False  — Equal to
print(a != b)    # True   — Not equal to
print(a > b)     # False  — Greater than
print(a < b)     # True   — Less than
print(a >= 10)   # True   — Greater than or equal
print(a <= 10)   # True   — Less than or equal
```

**Important: `=` vs `==`**
```python
x = 5      # ASSIGNMENT — sets x to 5
x == 5     # COMPARISON — asks "is x equal to 5?"
```

---

## Part 4: Logical Operators

Combine multiple conditions:

```python
age = 25
income = 50000
credit_score = 720

# AND — both conditions must be True
is_eligible = (age >= 18) and (income >= 30000)
print(is_eligible)   # True

# OR — at least one must be True
has_access = (age < 12) or (age > 65)
print(has_access)    # False (25 is neither)

# NOT — reverses True/False
is_minor = not (age >= 18)
print(is_minor)      # False

# Combined
approved = (age >= 21) and (income >= 40000) and (credit_score >= 700)
print(f"Loan approved: {approved}")   # True
```

### Truth Table

| A | B | A and B | A or B | not A |
|---|---|---------|--------|-------|
| T | T | T | T | F |
| T | F | F | T | F |
| F | T | F | T | T |
| F | F | F | F | T |

---

## Part 5: Membership Operators

Check if a value exists in a collection:

```python
fruits = ["apple", "banana", "cherry"]

print("apple" in fruits)        # True
print("mango" in fruits)        # False
print("mango" not in fruits)    # True

name = "Alice"
print("A" in name)              # True
print("z" in name)              # False
```

---

## Part 6: Identity Operators

Check if two variables point to the SAME object:

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)    # True  — same values
print(a is b)    # False — different objects
print(a is c)    # True  — same object (c points to a)

# None checks — always use 'is', not ==
value = None
if value is None:
    print("No value assigned")
```

---

## Part 7: Operator Precedence

Python follows mathematical order of operations (PEMDAS):

```
P — Parentheses       ()
E — Exponentiation    **
M — Multiplication    *
D — Division          /
A — Addition          +
S — Subtraction       -
```

```python
# Without parentheses:
result = 2 + 3 * 4    # 14 (not 20!) — multiplication first

# With parentheses:
result = (2 + 3) * 4  # 20

# Complex example:
x = 10 + 2 ** 3 * 4 - 6 / 2
#   = 10 + 8   * 4 - 3.0
#   = 10 + 32      - 3.0
#   = 39.0
print(x)   # 39.0

# When in doubt, use parentheses!
x = 10 + ((2 ** 3) * 4) - (6 / 2)
print(x)   # Same result, but much clearer
```

---

## Part 8: Business Example — EMI Calculator

```python
"""
EMI Calculator
EMI = Equated Monthly Installment (loan payment)

Formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
P = Principal, r = monthly rate, n = months
"""

print("=" * 40)
print("    EMI CALCULATOR")
print("=" * 40)

principal = float(input("Loan amount ($): "))
annual_rate = float(input("Annual interest rate (%): "))
years = int(input("Loan duration (years): "))

# Convert annual rate to monthly decimal
monthly_rate = (annual_rate / 100) / 12
n = years * 12  # total months

# EMI formula
emi = principal * monthly_rate * (1 + monthly_rate) ** n / ((1 + monthly_rate) ** n - 1)
total_payment = emi * n
total_interest = total_payment - principal

print()
print(f"Monthly EMI:    ${emi:,.2f}")
print(f"Total Payment:  ${total_payment:,.2f}")
print(f"Total Interest: ${total_interest:,.2f}")
```

---

## Practice Exercises

1. Write expressions for these (do NOT use if/else):
   - Check if a number is divisible by 3
   - Check if a year is even
   - Check if a score is between 50 and 100 (inclusive)

2. What is the result of:
   ```python
   print(3 + 4 * 2)
   print((3 + 4) * 2)
   print(2 ** 3 ** 2)   # Right-to-left! 3**2 first
   print(15 % 4)
   print(-15 % 4)
   ```

3. Write a profit calculator: ask for revenue and expenses, calculate and print gross profit and profit margin percentage.

4. Fix the bug:
   ```python
   temperature = 36.6
   if temperature = 37.0:
       print("Fever")
   ```

5. What is wrong here and how do you fix it?
   ```python
   x = 10
   y = 3
   ratio = x / y
   print(f"Ratio: {ratio:%.1f}")
   ```

---

## Summary

| Category | Operators |
|----------|-----------|
| Arithmetic | `+ - * / // % **` |
| Assignment | `= += -= *= /= //= %= **=` |
| Comparison | `== != > < >= <=` |
| Logical | `and or not` |
| Membership | `in not in` |
| Identity | `is is not` |

---

## Next Lesson

**[Lesson 06 → Strings](lesson-06-strings.md)**
