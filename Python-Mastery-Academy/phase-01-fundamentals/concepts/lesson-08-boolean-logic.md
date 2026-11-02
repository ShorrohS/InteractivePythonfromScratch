# Lesson 08 — Boolean Logic

**Phase:** 01 — Fundamentals | **Time:** ~30 min | **Prerequisite:** Lesson 07

---

## Part 1: Concept

Booleans represent **True** or **False**. Almost every decision in programming is based on boolean logic.

**Analogy:** A light switch — it's either ON (True) or OFF (False). No in-between.

---

## Part 2: Boolean Values

```python
# Direct assignment
is_logged_in = True
is_admin = False
has_subscription = True

print(type(True))    # <class 'bool'>
print(type(False))   # <class 'bool'>
```

---

## Part 3: Comparison Operators Produce Booleans

```python
age = 25
salary = 50000

print(age == 25)         # True
print(age != 30)         # True
print(age > 18)          # True
print(age < 18)          # False
print(salary >= 50000)   # True
print(salary <= 40000)   # False
```

---

## Part 4: Logical Operators

### and — Both must be True

```python
age = 25
has_id = True
has_ticket = True

# Both conditions required
can_enter = (age >= 18) and has_id and has_ticket
print(can_enter)    # True

age = 15
can_enter = (age >= 18) and has_id
print(can_enter)    # False (age condition fails)
```

### or — At least one must be True

```python
is_member = False
has_coupon = True

# Either one is enough for discount
gets_discount = is_member or has_coupon
print(gets_discount)    # True

is_member = False
has_coupon = False
gets_discount = is_member or has_coupon
print(gets_discount)    # False
```

### not — Reverses the value

```python
is_banned = False
can_access = not is_banned
print(can_access)    # True

is_active = True
print(not is_active)    # False
```

---

## Part 5: Truthy and Falsy Values

In Python, non-boolean values can be evaluated as True or False:

```python
# FALSY values (evaluate to False):
print(bool(0))       # False
print(bool(0.0))     # False
print(bool(""))      # False (empty string)
print(bool([]))      # False (empty list)
print(bool({}))      # False (empty dict)
print(bool(None))    # False

# TRUTHY values (evaluate to True):
print(bool(1))           # True
print(bool(-1))          # True (any non-zero number)
print(bool("hello"))     # True (non-empty string)
print(bool([1, 2]))      # True (non-empty list)
print(bool({"a": 1}))   # True
```

**Practical use:**
```python
name = input("Enter your name: ")

# Instead of: if name != "":
if name:
    print(f"Hello, {name}!")
else:
    print("Please enter a name.")
```

---

## Part 6: Short-Circuit Evaluation

Python stops evaluating as soon as the result is determined:

```python
# AND: stops at first False
result = False and some_function()   # some_function() NEVER called
                                      # because False and anything = False

# OR: stops at first True
result = True or some_function()     # some_function() NEVER called
                                      # because True or anything = True

# Practical use: safe attribute access
user = None
# Instead of: if user is not None and user.is_active:
if user and user.is_active:   # If user is None, stops at user
    print("Active user")
```

---

## Part 7: Chaining Comparisons

Python allows readable chaining:

```python
age = 25

# Python way (very readable)
if 18 <= age <= 65:
    print("Working age")

# Equivalent but verbose
if age >= 18 and age <= 65:
    print("Working age")

# More examples
score = 75
print(0 <= score <= 100)        # True — valid percentage
print(60 <= score < 70)         # False — not in 60s
```

---

## Part 8: Business Example — Login Validator

```python
"""
Login Validator
Checks if login credentials meet requirements.
"""

# System has these stored (in reality, from a database)
VALID_USER = "admin"
VALID_PASS = "secret123"
MAX_ATTEMPTS = 3

print("=" * 40)
print("   LOGIN SYSTEM")
print("=" * 40)

username = input("Username: ")
password = input("Password: ")

# Validations
is_correct_user = username == VALID_USER
is_correct_pass = password == VALID_PASS
username_not_empty = len(username) > 0
password_not_empty = len(password) > 0

# Combined check
inputs_provided = username_not_empty and password_not_empty
credentials_valid = is_correct_user and is_correct_pass

if not inputs_provided:
    print("Error: Username and password required.")
elif credentials_valid:
    print(f"\n✅ Login successful! Welcome, {username}.")
else:
    print("\n❌ Invalid credentials. Please try again.")
```

---

## Part 9: Common Mistakes

### Mistake 1: Using = instead of ==

```python
# WRONG
if age = 18:        # SyntaxError!
    print("Adult")

# CORRECT
if age == 18:
    print("Adult")
```

### Mistake 2: Not understanding None

```python
value = None

# WRONG
if value == None:    # Works but not idiomatic

# CORRECT
if value is None:    # Preferred
    print("No value")
```

### Mistake 3: Confusing and/or with &&/||

```python
# WRONG (JavaScript style)
if (age > 18) && (income > 50000):    # SyntaxError

# CORRECT (Python)
if age > 18 and income > 50000:
    print("Eligible")
```

---

## Practice Exercises

1. Write boolean expressions for:
   - A user can vote (age >= 18 AND is_citizen)
   - A product is on sale (is_clearance OR discount_percentage > 0)
   - A user is NOT banned

2. Predict the output:
   ```python
   print(True and False)
   print(True or False)
   print(not True)
   print(True and True or False)
   print(not (True and False))
   ```

3. Write a program that checks if a number is:
   - Positive
   - Even
   - Between 10 and 100 (inclusive)
   Print all three results.

4. What is the truthy/falsy value of each?
   ```python
   bool(0)
   bool(-1)
   bool("0")
   bool([])
   bool([0])
   bool(None)
   ```

5. Create a "loan eligibility" checker. Ask for age, income, and credit score. Print whether the person is eligible based on: age >= 21, income >= 25000, credit_score >= 650.

---

## Summary

| Concept | Description | Example |
|---------|-------------|---------|
| `True` / `False` | Boolean values | `is_active = True` |
| `and` | Both must be True | `a and b` |
| `or` | One must be True | `a or b` |
| `not` | Inverts the value | `not a` |
| Truthy | Non-zero, non-empty | `bool("hi")` → True |
| Falsy | Zero, empty, None | `bool("")` → False |
| Chaining | `18 <= x <= 65` | Pythonic range check |
| `is None` | None check | `if x is None:` |

---

## Phase 01 Complete!

You now know:
- ✅ print() and output formatting
- ✅ Variables and assignment
- ✅ All 4 core data types
- ✅ Input and output
- ✅ All operator types
- ✅ String operations
- ✅ Number functions
- ✅ Boolean logic

**→ Now build the 5 guided projects before moving to Phase 02!**

Projects: [Guided Projects Folder](../guided-projects/)
