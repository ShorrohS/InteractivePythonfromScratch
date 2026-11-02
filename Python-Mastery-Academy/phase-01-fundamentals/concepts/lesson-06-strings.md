# Lesson 06 — Strings

**Phase:** 01 — Fundamentals | **Time:** ~60 min | **Prerequisite:** Lesson 05

---

## Part 1: String Basics

Strings are sequences of characters. They're the most common data type in real programs.

```python
# Creating strings
single = 'Hello'
double = "Hello"
triple = """This is a
multi-line string"""

# Both quotes are identical — use double by convention
name = "Alice Johnson"
```

---

## Part 2: String Indexing & Slicing

```python
text = "Python"
#       012345  ← Positive indices
#      -654321  ← Negative indices

# Indexing — get one character
print(text[0])      # P  (first character)
print(text[5])      # n  (last character)
print(text[-1])     # n  (last, using negative index)
print(text[-2])     # o  (second from last)

# Slicing — get a portion
print(text[0:3])    # Pyt  (index 0, 1, 2)
print(text[2:5])    # tho  (index 2, 3, 4)
print(text[:3])     # Pyt  (from start to 3)
print(text[3:])     # hon  (from 3 to end)
print(text[:])      # Python  (whole string)
print(text[::2])    # Pto  (every 2nd character)
print(text[::-1])   # nohtyP  (reversed!)
```

---

## Part 3: Essential String Methods

```python
text = "  Hello, World!  "

# Case methods
print(text.upper())           # "  HELLO, WORLD!  "
print(text.lower())           # "  hello, world!  "
print(text.title())           # "  Hello, World!  "
print(text.capitalize())      # "  hello, world!  " (first char capitalized)
print(text.swapcase())        # "  hELLO, wORLD!  "

# Whitespace methods
print(text.strip())           # "Hello, World!"  (removes both sides)
print(text.lstrip())          # "Hello, World!  " (removes left)
print(text.rstrip())          # "  Hello, World!" (removes right)

# Search methods
print(text.find("World"))     # 9  (index of first match, -1 if not found)
print(text.index("World"))    # 9  (like find but raises error if not found)
print(text.count("l"))        # 3  (how many times 'l' appears)
print(text.startswith(" "))   # True
print(text.endswith("! "))    # False (has trailing spaces)
print("World" in text)        # True

# Replace
clean = text.strip()
print(clean.replace("World", "Python"))   # "Hello, Python!"

# Split and Join
sentence = "apple,banana,cherry"
fruits = sentence.split(",")       # ['apple', 'banana', 'cherry']
print(fruits)
joined = " - ".join(fruits)        # "apple - banana - cherry"
print(joined)
```

---

## Part 4: Checking String Content

```python
text1 = "Hello123"
text2 = "   "
text3 = "12345"

print(text1.isalpha())     # False (has digits)
print(text1.isdigit())     # False (has letters)
print(text1.isalnum())     # True  (letters and digits, no spaces)
print(text2.isspace())     # True  (only whitespace)
print(text3.isdigit())     # True  (all digits)
print("HELLO".isupper())   # True
print("hello".islower())   # True
print("Hello World".istitle())  # True
```

---

## Part 5: String Formatting — f-strings (Detailed)

```python
name = "Alice"
age = 30
salary = 75000.50
score = 0.925

# Basic insertion
print(f"Name: {name}, Age: {age}")

# Number formatting
print(f"Salary: ${salary:,.2f}")     # $75,000.50
print(f"Score: {score:.1%}")         # 92.5%
print(f"Pi: {3.14159:.3f}")          # 3.142

# Alignment
item = "Widget"
price = 29.99
print(f"{item:<20} ${price:>8.2f}")  # left & right align

# Expressions
print(f"Next year: {age + 1}")
print(f"Name in caps: {name.upper()}")
print(f"3 x 7 = {3 * 7}")

# Padding
for i in range(1, 6):
    print(f"Item {i:02d}: ${i * 10:.2f}")   # Item 01: $10.00
```

---

## Part 6: Common String Operations

```python
# Repeat
print("=" * 40)
print("-" * 20)

# Length
name = "Alice Johnson"
print(len(name))     # 13

# Check empty
user_input = ""
if not user_input:
    print("Input cannot be empty")

# Reverse a string
word = "Python"
reversed_word = word[::-1]
print(reversed_word)    # nohtyP

# Check palindrome
def is_palindrome(s):
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

print(is_palindrome("racecar"))     # True
print(is_palindrome("hello"))       # False

# Count words
sentence = "Python is a great language"
words = sentence.split()
print(f"Word count: {len(words)}")  # 5
```

---

## Part 7: Real-World Example — Username Generator

```python
"""
Username Generator
Creates a standardized username from user data.
"""

print("=" * 40)
print("   USERNAME GENERATOR")
print("=" * 40)

first = input("First name: ").strip()
last = input("Last name: ").strip()
year = input("Birth year: ").strip()

# Generate username variations
username_basic = (first[0] + last).lower()
username_with_year = (first[0] + last + year[-2:]).lower()
username_dots = (first + "." + last).lower()
username_underscore = (first + "_" + last[0:3]).lower()

print()
print("Generated Usernames:")
print(f"  Option 1: {username_basic}")
print(f"  Option 2: {username_with_year}")
print(f"  Option 3: {username_dots}")
print(f"  Option 4: {username_underscore}")
```

---

## Part 8: Common Mistakes

### Mistake 1: Strings are immutable

```python
name = "Alice"
name[0] = "B"   # TypeError: 'str' object does not support item assignment

# CORRECT: create a new string
name = "B" + name[1:]   # "Blice"
```

### Mistake 2: find() vs index()

```python
text = "Hello World"

# find() returns -1 if not found
print(text.find("xyz"))    # -1

# index() raises ValueError if not found
print(text.index("xyz"))   # ValueError: substring not found

# Use find() when "not found" is a valid case
pos = text.find("World")
if pos != -1:
    print(f"Found at index {pos}")
```

### Mistake 3: Forgetting .strip() on input

```python
# User might accidentally type spaces
name = input("Name: ")   # User types "  Alice  "
print(f"Hello {name}!")  # Hello   Alice  !  ← ugly

# CORRECT
name = input("Name: ").strip()
print(f"Hello {name}!")  # Hello Alice!
```

---

## Practice Exercises

1. Write a program that takes a full name as input and prints:
   - Name in ALL CAPS
   - Name in all lowercase
   - First name only
   - Last name only
   - Number of characters in the full name

2. Write a program that reverses a word entered by the user and checks if it's a palindrome.

3. Create an email formatter that takes first name, last name, and company, then produces: `firstname.lastname@company.com`

4. Fix this code:
   ```python
   message = "Hello, World!"
   message[0] = "h"
   print(message)
   ```

5. What is the output?
   ```python
   s = "Python Programming"
   print(s[7:])
   print(s[:6])
   print(s[::2])
   print(s.count("m"))
   ```

---

## String Methods Quick Reference

| Method | Description | Example |
|--------|-------------|---------|
| `.upper()` | All uppercase | `"hi".upper()` → `"HI"` |
| `.lower()` | All lowercase | `"HI".lower()` → `"hi"` |
| `.strip()` | Remove whitespace | `" hi ".strip()` → `"hi"` |
| `.replace(a,b)` | Replace text | `"cat".replace("c","b")` → `"bat"` |
| `.split(sep)` | Split to list | `"a,b".split(",")` → `["a","b"]` |
| `.join(list)` | Join list | `",".join(["a","b"])` → `"a,b"` |
| `.find(s)` | Find position | `"hello".find("e")` → `1` |
| `.count(s)` | Count occurrences | `"hello".count("l")` → `2` |
| `.startswith(s)` | Check start | `"hello".startswith("he")` → `True` |
| `.endswith(s)` | Check end | `"hello".endswith("lo")` → `True` |
| `.isdigit()` | All digits? | `"123".isdigit()` → `True` |
| `len(s)` | Length | `len("hello")` → `5` |

---

## Next Lesson

**[Lesson 07 → Numbers](lesson-07-numbers.md)**
