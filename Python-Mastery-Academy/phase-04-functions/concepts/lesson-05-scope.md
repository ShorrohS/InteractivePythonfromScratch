# Lesson 05 — Scope (LEGB Rule)

**Phase:** 04 — Functions | **Time:** ~25 min

---

## Part 1: What is Scope?

Scope determines where a variable can be seen and used.

**Analogy:** A hotel building. Guests in room 205 can use items in their room (local), items in the hotel lobby (global), but not items in other rooms.

---

## Part 2: The LEGB Rule

Python looks up names in this order:

```
L — Local       Variables inside the current function
E — Enclosing   Variables in outer function (for closures)
G — Global      Module-level variables
B — Built-in    Python's built-ins: print, len, range...
```

```python
x = "global"   # Global scope

def outer():
    x = "enclosing"   # Enclosing scope

    def inner():
        x = "local"    # Local scope
        print(x)       # finds Local first → "local"

    inner()
    print(x)   # finds Enclosing → "enclosing"

outer()
print(x)   # finds Global → "global"
```

---

## Part 3: Local vs Global

```python
total = 0    # global

def add_to_total(amount: float) -> None:
    total = total + amount    # UnboundLocalError!
    # Python sees 'total = ...' and treats it as LOCAL
    # But then tries to read it before assignment

# FIX 1: Return value (recommended)
def add_to_total(current: float, amount: float) -> float:
    return current + amount

total = add_to_total(total, 50)

# FIX 2: global keyword (use sparingly)
def add_to_total_global(amount: float) -> None:
    global total
    total += amount    # explicitly modifies the global

# RULE: Avoid global variables. Use return values instead.
```

---

## Part 4: Closures

A function that "remembers" variables from its enclosing scope:

```python
def make_multiplier(factor: int):
    """Returns a function that multiplies by factor."""
    def multiply(x: float) -> float:
        return x * factor    # 'factor' captured from enclosing scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(10))   # 20
print(triple(10))   # 30
print(double(7))    # 14

# Practical: configurable tax calculator
def make_tax_calculator(rate: float):
    def calculate(amount: float) -> float:
        return amount * rate
    return calculate

uk_vat   = make_tax_calculator(0.20)
us_tax   = make_tax_calculator(0.085)

print(uk_vat(100))    # 20.0
print(us_tax(100))    # 8.5
```

---

## Part 5: nonlocal

Modify a variable in the enclosing (not global) scope:

```python
def make_counter():
    count = 0

    def increment():
        nonlocal count    # refers to enclosing 'count'
        count += 1
        return count

    return increment

counter = make_counter()
print(counter())   # 1
print(counter())   # 2
print(counter())   # 3
```

---

## Part 6: Best Practices

```python
# BAD: using globals
score = 0

def add_score(points):
    global score
    score += points    # side effect — hard to test

# GOOD: pure functions (input → output, no side effects)
def add_score(current_score: int, points: int) -> int:
    return current_score + points

score = add_score(score, 10)
```

---

## Practice Exercises

1. What prints?
   ```python
   x = 5
   def f():
       x = 10
       print(x)
   f()
   print(x)
   ```

2. Write a `make_greeting(prefix)` function that returns a function accepting a name.

3. What is the bug?
   ```python
   count = 0
   def increment():
       count += 1
   increment()
   ```

---

## Next Lesson

**[Lesson 06 → Recursion](lesson-06-recursion.md)**
