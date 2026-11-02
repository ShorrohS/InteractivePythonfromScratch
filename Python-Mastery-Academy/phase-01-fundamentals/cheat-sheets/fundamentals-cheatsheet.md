# ⚡ Phase 01 Cheat Sheet — Python Fundamentals

---

## Variables

```python
name = "Alice"          # String
age = 30                # Integer
salary = 75000.50       # Float
active = True           # Boolean
nothing = None          # NoneType

x, y, z = 1, 2, 3      # Multiple assignment
a = b = c = 0           # Same value
x, y = y, x             # Swap
```

---

## Data Types

```python
type("hello")           # str
type(42)                # int
type(3.14)              # float
type(True)              # bool

int("42")               # 42      string → int
float("3.14")           # 3.14    string → float
str(42)                 # "42"    int → string
bool(0)                 # False
bool(1)                 # True
bool("")                # False
bool("hi")              # True
```

---

## Input & Output

```python
name = input("Your name: ")         # always returns str
age  = int(input("Your age: "))     # convert to int
price = float(input("Price: "))     # convert to float

print("Hello", name)                # Hello Alice
print(f"Hello {name}!")             # Hello Alice!
print(f"{price:.2f}")               # 19.99
print(f"{price:,.2f}")              # 1,999.99
print(f"{0.95:.1%}")                # 95.0%
print(f"{'hi':<10}|")              # hi        |
print(f"{'hi':>10}|")              # "        hi|"
print(f"{'hi':^10}|")              # "    hi    |"
```

---

## Arithmetic Operators

```python
10 + 3      # 13   addition
10 - 3      # 7    subtraction
10 * 3      # 30   multiplication
10 / 3      # 3.33 division (always float)
10 // 3     # 3    floor division
10 % 3      # 1    modulo (remainder)
10 ** 3     # 1000 exponentiation

# Augmented
x += 5      # x = x + 5
x -= 5
x *= 5
x /= 5
x //= 5
x %= 5
x **= 5
```

---

## Comparison & Logic

```python
a == b      # Equal
a != b      # Not equal
a > b       # Greater than
a < b       # Less than
a >= b      # Greater or equal
a <= b      # Less or equal

x and y     # Both true
x or y      # At least one true
not x       # Inverts

18 <= age <= 65   # Chained comparison
```

---

## Strings

```python
s = "Hello, World!"

# Indexing
s[0]        # 'H'
s[-1]       # '!'
s[0:5]      # 'Hello'
s[::-1]     # Reversed

# Methods
s.upper()           # "HELLO, WORLD!"
s.lower()           # "hello, world!"
s.title()           # "Hello, World!"
s.strip()           # Remove whitespace
s.lstrip()          # Remove left whitespace
s.rstrip()          # Remove right whitespace
s.replace("o","0")  # "Hell0, W0rld!"
s.split(",")        # ['Hello', ' World!']
",".join(["a","b"]) # "a,b"
s.find("World")     # 7
s.count("l")        # 3
s.startswith("Hello") # True
s.endswith("!")     # True
len(s)              # 13
"World" in s        # True
```

---

## Number Functions

```python
abs(-5)             # 5
round(3.14159, 2)   # 3.14
max(1, 5, 3)        # 5
min(1, 5, 3)        # 1
sum([1, 2, 3])      # 6

import math
math.sqrt(16)       # 4.0
math.floor(3.9)     # 3
math.ceil(3.1)      # 4
math.pi             # 3.14159...

import random
random.randint(1, 10)    # random 1-10
random.random()           # random 0.0-1.0
random.choice(["a","b"]) # random element
```

---

## Truthy / Falsy

```
Falsy:  0, 0.0, "", [], {}, None, False
Truthy: Everything else
```

---

## Common Patterns

```python
# Check if string is empty
if user_input:                  # truthy check
    print("Has content")

# Safe number parsing
value = float(input("Amount: $"))

# Format currency
print(f"Total: ${amount:,.2f}")

# String contains check
if "error" in log_message.lower():
    print("Error found")

# Title case name
name = input("Name: ").strip().title()
```
