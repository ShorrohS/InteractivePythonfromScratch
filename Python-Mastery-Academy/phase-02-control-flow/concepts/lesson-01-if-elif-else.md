# Lesson 01 — If / Elif / Else

**Phase:** 02 — Control Flow | **Time:** ~30 min

---

## Part 1: Concept

The `if` statement lets your program make decisions.

**Analogy:** Think of it as a fork in the road. The program checks a condition and goes down the appropriate path.

---

## Part 2: Basic Syntax

```python
# if
if condition:
    # runs if condition is True
    action

# if / else
if condition:
    action_if_true
else:
    action_if_false

# if / elif / else
if condition1:
    action1
elif condition2:
    action2
elif condition3:
    action3
else:
    default_action
```

**Indentation is CRITICAL in Python.** Use 4 spaces. Never mix tabs and spaces.

---

## Part 3: Examples

### Simple Decision

```python
age = 20

if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")
```

### Multiple Branches

```python
score = 75

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score} → Grade: {grade}")
```

### Salary Band Classification

```python
salary = 85000

if salary >= 150000:
    band = "Senior Executive"
elif salary >= 100000:
    band = "Senior"
elif salary >= 75000:
    band = "Mid-level"
elif salary >= 50000:
    band = "Junior"
else:
    band = "Entry-level"

print(f"Salary: ${salary:,} → Band: {band}")
```

---

## Part 4: Nested If

```python
age = 22
income = 45000

if age >= 18:
    print("Age requirement met.")
    if income >= 30000:
        print("Income requirement met.")
        print("Loan approved!")
    else:
        print("Income too low. Loan denied.")
else:
    print("Must be 18+ for a loan.")
```

---

## Part 5: Inline / Ternary

```python
# One-line if/else for simple assignments
age = 20
status = "adult" if age >= 18 else "minor"
print(status)

# Another example
score = 72
result = "Pass" if score >= 60 else "Fail"
print(result)
```

---

## Part 6: Business Project — Grade System

```python
"""Grade System — calculates letter grade, GPA, and status."""

print("=" * 40)
print("    STUDENT GRADE SYSTEM")
print("=" * 40)

student = input("Student Name: ")
score = float(input("Score (0-100): "))

# Determine grade
if score >= 90:
    letter, gpa = "A", 4.0
elif score >= 80:
    letter, gpa = "B", 3.0
elif score >= 70:
    letter, gpa = "C", 2.0
elif score >= 60:
    letter, gpa = "D", 1.0
else:
    letter, gpa = "F", 0.0

status = "Pass" if score >= 60 else "Fail"

print()
print(f"Student: {student}")
print(f"Score:   {score:.1f}%")
print(f"Grade:   {letter}")
print(f"GPA:     {gpa:.1f}")
print(f"Status:  {status}")
```

---

## Part 7: Common Mistakes

```python
# Mistake 1: = instead of ==
if age = 18:    # SyntaxError
if age == 18:   # Correct

# Mistake 2: Wrong indentation
if age > 18:
print("Adult")       # IndentationError
    print("Adult")   # Correct (4 spaces)

# Mistake 3: Missing colon
if age > 18      # SyntaxError
if age > 18:     # Correct

# Mistake 4: Overlapping conditions (unreachable code)
if score >= 60:
    grade = "D"
elif score >= 90:     # This NEVER runs — 90 is caught by >= 60 first
    grade = "A"       # Bug! Order matters.
```

---

## Practice Exercises

1. Write a program that takes a temperature in Celsius and prints "Hot" (>30), "Warm" (20-30), "Cool" (10-19), "Cold" (<10).

2. Write a BMI calculator that classifies as: Underweight (<18.5), Normal (18.5-24.9), Overweight (25-29.9), Obese (≥30).

3. Ask for a year and determine if it's a leap year. (Divisible by 4, except centuries unless divisible by 400).

4. Loan eligibility: age ≥ 21, income ≥ 25000, credit score ≥ 650. Show which requirements are met.

5. Fix: `if x > 5 and < 10:` — what's wrong?

---

## Next Lesson

**[Lesson 02 → Match/Case](lesson-02-match-case.md)**
