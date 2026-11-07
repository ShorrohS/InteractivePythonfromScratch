# Phase 04 — Beginner Solutions: Functions

---

## Q1. greet function

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Alice"))
print(greet("Bob"))
print(greet("World"))
```

---

## Q2. Basic arithmetic functions

```python
def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float | None:
    if b == 0:
        return None
    return a / b

print(add(10, 5))        # 15
print(subtract(10, 5))   # 5
print(multiply(10, 5))   # 50
print(divide(10, 5))     # 2.0
print(divide(10, 0))     # None
```

---

## Q3. is_even and is_odd

```python
def is_even(n: int) -> bool:
    return n % 2 == 0

def is_odd(n: int) -> bool:
    return not is_even(n)   # uses is_even!

print(is_even(4))    # True
print(is_odd(7))     # True
```

---

## Q4. Temperature converters

```python
def celsius_to_fahrenheit(c: float) -> float:
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5/9

print(celsius_to_fahrenheit(100))       # 212.0
print(fahrenheit_to_celsius(212))       # 100.0
```

---

## Q5. Rectangle functions

```python
def area_of_rectangle(length: float, width: float) -> float:
    return length * width

def perimeter_of_rectangle(length: float, width: float) -> float:
    return 2 * (length + width)

print(area_of_rectangle(5, 3))         # 15
print(perimeter_of_rectangle(5, 3))    # 16
```

---

## Q6. find_max (no max())

```python
def find_max(a: float, b: float, c: float) -> float:
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c

print(find_max(3, 7, 5))   # 7
```

---

## Q7. count_vowels

```python
def count_vowels(text: str) -> int:
    return sum(1 for ch in text.lower() if ch in "aeiou")

print(count_vowels("Hello World"))    # 3
print(count_vowels("Python"))         # 1
```

---

## Q8. repeat_string

```python
def repeat_string(text: str, n: int = 2) -> str:
    return text * n

print(repeat_string("abc"))       # abcabc
print(repeat_string("hi", 4))    # hihihihi
```

---

## Q9. Predict output

```python
def mystery(x, y=5):
    return x * y

print(mystery(3))         # 15  (3 * 5, using default)
print(mystery(3, 10))     # 30  (3 * 10)
print(mystery(y=2, x=4))  # 8   (4 * 2, keyword args)
```

---

## Q10. Fix the code

```python
# Bug: 'Name' is undefined — Python is case-sensitive, should be 'name'

def greet(name: str, punctuation: str = "!") -> str:
    return "Hello, " + name + punctuation   # FIX: name (lowercase)

print(greet("Alice"))    # Hello, Alice!
```
