# Lesson 01 — Hello World & print()

**Phase:** 01 — Fundamentals | **Time:** ~20 min | **Prerequisite:** Phase 00 complete

---

## Part 1: Concept

### What is print()?

`print()` is a built-in Python function that displays output on the screen.

**Analogy:** `print()` is like a loudspeaker. Whatever you give it, it announces to the screen.

**When to use:** Any time you want to show information to the user.

---

## Part 2: print() Basics

```python
# The most basic Python program
print("Hello, World!")
```

Output:
```
Hello, World!
```

### What's happening:
- `print` — the function name
- `(` `)` — parentheses contain what to print
- `"Hello, World!"` — a string (text between quotes)

---

## Part 3: Comments

Comments are lines Python ignores. They are notes for humans reading the code.

```python
# This is a single-line comment
# Python completely ignores this line

print("This line runs")  # Inline comment — also ignored by Python

"""
This is a multi-line comment (docstring).
Use triple quotes.
Often used to describe what a file or function does.
"""
```

**When to use comments:**
- Explain WHY you're doing something (not what — the code shows what)
- Mark TODO items
- Temporarily disable code during debugging

---

## Part 4: Variations

### Printing different data types:

```python
print("Hello")          # String
print(42)               # Integer
print(3.14)             # Float
print(True)             # Boolean
```

### Printing expressions:

```python
print(2 + 2)            # 4
print(10 * 5)           # 50
print(100 / 4)          # 25.0
print(2 ** 10)          # 1024 (2 to the power of 10)
```

### Printing multiple items:

```python
print("Name:", "Alice")               # Name: Alice
print("Age:", 30)                     # Age: 30
print("Score:", 95, "out of", 100)    # Score: 95 out of 100
```

### Customizing separator and end:

```python
# sep — what goes between items (default is space)
print("Python", "is", "fun")          # Python is fun
print("Python", "is", "fun", sep="-") # Python-is-fun
print("Python", "is", "fun", sep="")  # Pythonisfun

# end — what goes at the end (default is newline \n)
print("Hello", end=" ")
print("World!")                        # Hello World!  (same line)
print("A", end="")
print("B", end="")
print("C")                             # ABC
```

### Printing blank lines:

```python
print("Line 1")
print()            # empty print = blank line
print("Line 3")
```

---

## Part 5: Escape Characters

Special characters inside strings:

```python
print("Line 1\nLine 2")          # \n = newline
print("Col1\tCol2\tCol3")        # \t = tab
print("She said \"Hello\"")      # \" = literal quote
print("C:\\Users\\Alice")        # \\ = literal backslash
print("100\% correct")           # just % — no escape needed
```

---

## Part 6: Common Mistakes

### Mistake 1: Missing quotes

```python
# WRONG
print(Hello World)

# Why it fails: Python thinks Hello is a variable, not text
# Error: SyntaxError: invalid syntax

# CORRECT
print("Hello World")
```

### Mistake 2: Mismatched quotes

```python
# WRONG
print("Hello World')

# Error: SyntaxError: EOL while scanning string literal

# CORRECT
print("Hello World")   # both double quotes
print('Hello World')   # both single quotes (also valid)
```

### Mistake 3: Missing parentheses

```python
# WRONG (Python 2 style)
print "Hello"

# Error: SyntaxError: Missing parentheses in call to 'print'

# CORRECT
print("Hello")
```

### Mistake 4: Extra spaces before print

```python
# WRONG (unexpected indentation)
    print("Hello")

# Error: IndentationError: unexpected indent

# CORRECT
print("Hello")
```

---

## Part 7: Practice Exercises

Do these without looking at the answers:

1. Write a Python program that prints your full name on one line.

2. Write a program that prints these three lines:
   ```
   Name: Alice
   Age: 25
   City: New York
   ```

3. What is the output of this code?
   ```python
   print("A", "B", "C", sep="-")
   ```

4. What is the output of this code?
   ```python
   print("Hello", end="!")
   print("World")
   ```

5. Fix this code so it runs without errors:
   ```python
   print(Hello, World)
   ```

---

## Summary

| Concept | Syntax | Example |
|---------|--------|---------|
| Print text | `print("text")` | `print("Hello")` |
| Print number | `print(num)` | `print(42)` |
| Print math | `print(expr)` | `print(2+2)` |
| Print multiple | `print(a, b)` | `print("Age:", 30)` |
| Custom separator | `sep="x"` | `sep="-"` |
| Custom ending | `end="x"` | `end=" "` |
| Single comment | `# text` | `# this runs` |
| Multi-line comment | `"""text"""` | docstrings |

---

## Next Lesson

**[Lesson 02 → Variables](lesson-02-variables.md)**
