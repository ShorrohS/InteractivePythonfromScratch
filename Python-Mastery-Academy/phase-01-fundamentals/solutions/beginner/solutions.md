# Phase 01 — Beginner Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/beginner/exercises.md`

---

## A1. Profile variables

```python
name     = "Jordan Smith"
age      = 28
height   = 1.75
employed = True

print(f"Name:     {name}")
print(f"Age:      {age}")
print(f"Height:   {height}m")
print(f"Employed: {employed}")
```

---

## A2. What is the output?

```python
x = 10
y = x       # y gets the current value of x (10)
x = 20      # x changes — y is unaffected
print(x)    # 20
print(y)    # 10
```

`y` stored the value 10 at the time of assignment. Changing `x` later does not affect `y` because integers are immutable — `y` is not a reference to `x`, it holds its own copy of the value.

---

## A3. Valid and invalid variable names

| Name | Valid? | Reason if invalid |
|------|--------|-------------------|
| `score` | Yes | — |
| `valid_user` | Yes | — |
| `2fast` | **No** | Cannot start with a digit |
| `my-name` | **No** | Hyphens not allowed (subtraction operator) |
| `_private` | Yes | — |
| `first name` | **No** | Spaces not allowed |
| `total$` | **No** | `$` not allowed in identifiers |
| `class` | **No** | Reserved keyword |
| `salary2024` | Yes | — |
| `TRUE` | Yes | (not the keyword `True` — valid but confusing, avoid) |

---

## A4. Data types

```python
a = "42"    # str  — text inside quotes
b = 42      # int  — whole number
c = 42.0    # float — has decimal point
d = True    # bool
e = None    # NoneType
```

---

## A5. Augmented assignment

```python
price = 100
price += 25    # 125
price *= 2     # 250
print(price)   # 250
```

---

## B6. Two numbers program

```python
name = input("Enter your name: ").strip()
num  = int(input("Enter your favourite number: "))
print(f"Hello {name}, your favourite number doubled is {num * 2}.")
```

---

## B7. Fix the code — type conversion

```python
# PROBLEM: input() returns a string, can't add int to string
age = input("Enter your age: ")
next_year = age + 1        # TypeError

# FIX:
age = int(input("Enter your age: "))
next_year = age + 1
print(f"Next year you will be {next_year}")
```

---

## B8. f-string output

```python
price = 1234.5678
print(f"{price:.2f}")    # 1234.57
print(f"{price:,.2f}")   # 1,234.57
print(f"{price:.0f}")    # 1235
```

---

## B9. Shopping item program

```python
item     = input("Item name: ").strip().title()
price    = float(input("Item price: $"))
quantity = int(input("Quantity: "))
subtotal = price * quantity

print(f"Item:      {item}")
print(f"Price:     ${price:.2f}")
print(f"Quantity:  {quantity}")
print(f"Subtotal:  ${subtotal:.2f}")
```

---

## B10. String method output

```python
name = "python"
print(name.upper())          # PYTHON
print(name.title())          # Python
print(len(name))             # 6
print(name.replace("p","P")) # Python
```

---

## C11. Operator results

```python
a = 25
b = 7
print(a + b)    # 32
print(a - b)    # 18
print(a * b)    # 175
print(a / b)    # 3.5714285714285716
print(a // b)   # 3
print(a % b)    # 4
print(a ** b)   # 6103515625
```

---

## C12. Operator precedence

```python
print(2 + 3 * 4)     # 14  — multiplication first
print((2 + 3) * 4)   # 20  — parentheses override
print(10 - 2 ** 3)   # 2   — exponentiation before subtraction (10 - 8)
print(10 / 2 + 3 * 2)  # 11.0 — (5.0) + (6) = 11.0
```

---

## C13. Minutes to hours

```python
total = int(input("Enter minutes: "))
hours   = total // 60
minutes = total % 60
print(f"{total} minutes = {hours} hours and {minutes} minutes")
```

---

## C14. Comparison output

```python
x = 15
print(x > 10)              # True
print(x == 15)             # True
print(x != 20)             # True
print(x >= 15)             # True
print(x < 20 and x > 10)  # True
print(x < 5 or x > 10)    # True
```

---

## C15. Divisible by 3 and 5

```python
def check(n):
    return n % 3 == 0 and n % 5 == 0

print(check(15))   # True  (15 / 3 = 5, 15 / 5 = 3)
print(check(9))    # False (divisible by 3 but not 5)
print(check(10))   # False (divisible by 5 but not 3)
```

---

## D16. String operations

```python
text = "  Hello, World!  "
print(text.strip())                    # "Hello, World!"
print(text.strip().upper())            # "HELLO, WORLD!"
print(text.count("l"))                 # 3
print(text.strip().replace("World","Python"))  # "Hello, Python!"
```

---

## D17. Name extraction

```python
name = "Alice Johnson"
parts     = name.split()
first     = parts[0]        # "Alice"
last      = parts[1]        # "Johnson"
initials  = f"{first[0]}.{last[0]}."  # "A.J."
username  = (first[0] + last).lower() # "ajohnson"

print(first, last, initials, username)
```

---

## D18. Indexing output

```python
s = "Python"
print(s[0])     # P
print(s[-1])    # n
print(s[2:5])   # tho
print(s[::-1])  # nohtyP
print(s * 3)    # PythonPythonPython
```

---

## D19. Sentence analysis

```python
sentence = input("Enter a sentence: ").strip()
reversed_s = sentence[::-1]
word_count = len(sentence.split())
is_palindrome = sentence.lower().replace(" ","") == sentence.lower().replace(" ","")[::-1]

print(f"Reversed: {reversed_s}")
print(f"Word count: {word_count}")
print(f"Palindrome: {is_palindrome}")
```

---

## D20. Fix the code

```python
full_name = "Alice Johnson"
parts = full_name.split()
first = parts[0]
last  = parts[1]
print(f"First: {first}, Last: {last}")
email = first + "." + last + "@company.com"
print(f"Email: {email}")   # FIX: was missing closing quote on f-string
```

Bug was: `print(f"Email: {email})` — missing closing `"` before `)`.
