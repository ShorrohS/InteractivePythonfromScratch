# 🔧 Phase 04 — Functions

> **Goal:** Write reusable, organized code using functions.

---

## Why Functions?

Without functions: Copy the same code 20 times across your program.
With functions: Write it once, call it anywhere.

**Functions are the foundation of good code.** Every professional program is organized into functions.

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-basics.md](concepts/lesson-01-basics.md) | Defining and calling functions |
| 02 | [lesson-02-parameters.md](concepts/lesson-02-parameters.md) | Parameters and return values |
| 03 | [lesson-03-defaults.md](concepts/lesson-03-defaults.md) | Default and keyword arguments |
| 04 | [lesson-04-args-kwargs.md](concepts/lesson-04-args-kwargs.md) | *args and **kwargs |
| 05 | [lesson-05-scope.md](concepts/lesson-05-scope.md) | Local and global scope |
| 06 | [lesson-06-recursion.md](concepts/lesson-06-recursion.md) | Recursive functions |
| 07 | [lesson-07-lambda.md](concepts/lesson-07-lambda.md) | Lambda functions |

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [Calculator Engine](guided-projects/project-01-calculator-engine/) | All operations as functions |
| [Payroll Module](guided-projects/project-02-payroll-module/) | Complete payroll with functions |
| [Report Generator](guided-projects/project-03-report-generator/) | Data + formatting functions |

---

## Key Concepts to Master

```python
# Basic function
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Default argument
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# *args — variable positional arguments
def add(*numbers):
    return sum(numbers)

# **kwargs — variable keyword arguments
def create_profile(**info):
    return info

# Lambda
square = lambda x: x ** 2

# Recursion
def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)
```

---

## ✅ Completion Checklist

- [ ] Can define functions with parameters and return values
- [ ] Understand default arguments
- [ ] Can use *args and **kwargs
- [ ] Understand local vs global scope
- [ ] Can write simple recursive functions
- [ ] Can write lambda functions
- [ ] Type hints on all functions

---

## Previous: [Phase 03](../phase-03-collections/README.md) | Next: [Phase 05](../phase-05-file-handling/README.md)
