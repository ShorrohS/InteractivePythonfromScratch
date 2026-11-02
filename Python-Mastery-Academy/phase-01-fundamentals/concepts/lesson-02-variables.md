# Lesson 02 — Variables

**Phase:** 01 — Fundamentals | **Time:** ~30 min | **Prerequisite:** Lesson 01

---

## Part 1: Concept

### What is a Variable?

A variable is a **named container** that stores a value in memory.

**Analogy:** A labeled box. The label is the variable name. Whatever you put inside is the value.

```
name = "Alice"

┌───────────┐
│  "Alice"  │  ← The value
└───────────┘
      ▲
   name  ← The label (variable name)
```

**Why they exist:** Programs need to remember information while running. Variables store that information so you can use it later.

---

## Part 2: Creating Variables

In Python, creating a variable is called **assignment**:

```python
variable_name = value
```

Examples:

```python
name = "Alice"
age = 30
salary = 75000.50
is_employed = True
```

Python figures out the type automatically — you don't declare types like in some other languages.

---

## Part 3: Naming Rules

### Rules (must follow — or error):

```python
# ✅ VALID names
name = "Alice"
age = 30
first_name = "Bob"
_private = "secret"
salary2024 = 75000

# ❌ INVALID names (will cause errors)
2name = "Alice"        # Cannot start with a number
my-name = "Alice"      # Hyphens not allowed (it's subtraction)
my name = "Alice"      # Spaces not allowed
class = "Math"         # 'class' is a reserved keyword
```

### Conventions (should follow — best practice):

```python
# Python style: snake_case (lowercase + underscores)
first_name = "Alice"     ✅ Professional
employee_id = 1001       ✅ Professional

# NOT recommended (but valid):
firstName = "Alice"      ← camelCase (used in JavaScript, not Python)
FIRST_NAME = "Alice"     ← UPPER_CASE (reserved for constants in Python)
FirstName = "Alice"      ← PascalCase (reserved for class names)
```

### Python Reserved Keywords (cannot use as variable names):

```
False    None     True     and      as       assert   async
await    break    class    continue def      del      elif
else     except   finally  for      from     global   if
import   in       is       lambda   nonlocal not      or
pass     raise    return   try      while    with     yield
```

---

## Part 4: Assigning and Reassigning

```python
# Initial assignment
score = 0
print(score)   # 0

# Reassignment — the variable changes
score = 100
print(score)   # 100

# Reassign using current value
score = score + 10
print(score)   # 110

# Shorthand
score += 10    # same as: score = score + 10
score -= 5     # same as: score = score - 5
score *= 2     # same as: score = score * 2
score /= 4     # same as: score = score / 4
```

---

## Part 5: Multiple Assignment

```python
# Assign multiple variables on one line
x, y, z = 1, 2, 3
print(x, y, z)   # 1 2 3

# Assign same value to multiple variables
a = b = c = 0
print(a, b, c)   # 0 0 0

# Swap values (Python does this elegantly)
x = 10
y = 20
x, y = y, x      # swap!
print(x, y)       # 20 10
```

---

## Part 6: Type Checking

```python
name = "Alice"
age = 30
height = 5.8
is_active = True

print(type(name))      # <class 'str'>
print(type(age))       # <class 'int'>
print(type(height))    # <class 'float'>
print(type(is_active)) # <class 'bool'>
```

---

## Part 7: Real-World Example

```python
# Employee Record
employee_name = "Sarah Johnson"
employee_id = 10042
department = "Sales"
annual_salary = 68000.00
is_full_time = True
years_employed = 3

# Display the record
print("=" * 35)
print("EMPLOYEE PROFILE")
print("=" * 35)
print(f"Name:       {employee_name}")
print(f"ID:         {employee_id}")
print(f"Department: {department}")
print(f"Salary:     ${annual_salary:,.2f}")
print(f"Full-time:  {is_full_time}")
print(f"Years:      {years_employed}")
print("=" * 35)
```

Output:
```
===================================
EMPLOYEE PROFILE
===================================
Name:       Sarah Johnson
ID:         10042
Department: Sales
Salary:     $68,000.00
Full-time:  True
Years:      3
===================================
```

---

## Part 8: Common Mistakes

### Mistake 1: Using undefined variable

```python
# WRONG
print(username)     # username was never defined

# Error: NameError: name 'username' is not defined

# CORRECT
username = "alice123"
print(username)
```

### Mistake 2: Typo in variable name

```python
# WRONG
user_name = "Alice"
print(username)     # Typo: user_name vs username

# Error: NameError: name 'username' is not defined

# CORRECT
user_name = "Alice"
print(user_name)
```

### Mistake 3: Wrong case

```python
# WRONG
Name = "Alice"
print(name)     # 'name' and 'Name' are different variables!

# Error: NameError: name 'name' is not defined

# Python is case-sensitive!
# Name, name, NAME are three different variables
```

### Mistake 4: Using reserved keyword

```python
# WRONG
list = [1, 2, 3]     # 'list' is a built-in type
print = "hello"      # 'print' is a built-in function

# This works but BREAKS the built-in
# You can no longer use print() after this!
# Avoid using built-in names as variables
```

---

## Part 9: Practice Exercises

1. Create variables to store your name, age, city, and favorite programming language. Print all four values.

2. Create a variable `price = 50`. Then increase it by 15 using the `+=` operator. Print the result.

3. Create two variables `x = 100` and `y = 200`. Swap their values without using a third variable. Print both.

4. What is the output of this code?
   ```python
   a = 10
   b = a
   a = 20
   print(a, b)
   ```

5. Which of these variable names are valid in Python?
   ```
   first_name, 2nd_name, my-age, _score, class, total$, employee_id
   ```

---

## Summary

| Concept | Example |
|---------|---------|
| Create variable | `name = "Alice"` |
| Reassign | `name = "Bob"` |
| Augmented assign | `score += 10` |
| Multiple assign | `x, y = 1, 2` |
| Swap | `x, y = y, x` |
| Check type | `type(name)` |
| Snake case convention | `first_name` |

---

## Next Lesson

**[Lesson 03 → Data Types](lesson-03-data-types.md)**
