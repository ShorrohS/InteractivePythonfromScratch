# Phase 01 — Completion Assessment

> Complete before moving to Phase 02.
> Pass mark: 80% | Time: 30 minutes

---

## PART A: Practical Coding Tasks

**Task 1.** Without looking at notes, write a program from scratch that:
- Asks for a person's first name, last name, and age
- Prints a formatted ID card:

```
==============================
   IDENTITY CARD
==============================
  Name:     Alice Johnson
  Username: ajohnson
  Age:      28
  Status:   Adult
==============================
```

Requirements:
- Generate username as: first initial + last name (all lowercase)
- Status is "Adult" if age >= 18, otherwise "Minor"

---

**Task 2.** Write a program that:
- Asks for a product name, price, and quantity
- Calculates: subtotal, 8% tax, total
- Prints a formatted receipt with all values as `$X,XXX.XX`

---

**Task 3.** Fix all bugs in this code (there are 4):

```python
name = input(Enter your name: )
age = input("Enter your age: ")

greeting = "Hello " + name + "! You are " + age + " years old."

if age > 17:
    print(greeting)
    print(Adult)
else
    print(greeting)
    print("Minor")
```

---

## PART B: Written Questions

**Q4.** Explain the difference between `=` and `==` with an example of each.

---

**Q5.** What are the 4 basic data types in Python? For each one, give an example value.

---

**Q6.** Why does `input()` always return a string? Give a code example showing what happens if you forget to convert it.

---

**Q7.** What is the output of this code and why?

```python
x = "5"
y = 3
print(x * y)
```

---

**Q8.** Write three different ways to create the string: `Hello, Alice! You are 30 years old.`
- Using `+` concatenation
- Using an f-string
- Using `.format()`

---

**Q9.** What is wrong with this code? Write the corrected version.

```python
print(f"Total: ${salary:2.f}")
```

---

**Q10.** Explain what "truthy" and "falsy" mean. Give 2 truthy and 2 falsy examples.

---

## PART C: Predict the Output

For each block, write what will be printed **before running it**:

**Q11.**
```python
a = 10
b = 3
print(a // b)
print(a % b)
print(a / b)
```

**Q12.**
```python
text = "python programming"
print(text[0])
print(text[-1])
print(text[7:14])
print(text.title())
print(len(text))
```

**Q13.**
```python
x = 5
x += 10
x *= 2
x -= 5
print(x)
```

**Q14.**
```python
print(bool(0))
print(bool(""))
print(bool("0"))
print(bool([]))
```

**Q15.**
```python
name = "  Alice  "
print(len(name))
print(len(name.strip()))
print(name.strip().upper())
```

---

## Scoring

| Score | Action |
|-------|--------|
| 13–15 | Move to Phase 02 |
| 11–12 | Review weak areas, then proceed |
| < 11  | Redo Phase 01 lessons before continuing |

---

## Answer Key

**Task 1 expected output:**
```python
first    = input("First name: ").strip().title()
last     = input("Last name: ").strip().title()
age      = int(input("Age: "))
username = (first[0] + last).lower()
status   = "Adult" if age >= 18 else "Minor"
print("=" * 30)
print("   IDENTITY CARD")
print("=" * 30)
print(f"  Name:     {first} {last}")
print(f"  Username: {username}")
print(f"  Age:      {age}")
print(f"  Status:   {status}")
print("=" * 30)
```

**Task 3 bugs:**
1. `input(Enter...)` — missing quotes around prompt
2. `age = input(...)` should be `age = int(input(...))`
3. `print(Adult)` — missing quotes: `print("Adult")`
4. `else` — missing colon: `else:`

**Q11:** `3`, `1`, `3.3333...`
**Q12:** `p`, `g`, `program`, `Python Programming`, `18`
**Q13:** `25` → (5+10=15, 15*2=30, 30-5=25)
**Q14:** `False`, `False`, `True`, `False`
**Q15:** `9`, `5`, `ALICE`
