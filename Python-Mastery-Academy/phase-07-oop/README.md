# 🏛️ Phase 07 — Object-Oriented Programming (OOP)

> **Goal:** Model real-world entities using classes and objects.

---

## Why OOP?

Functions organize code into reusable blocks.
OOP organizes code into objects that combine **data** (attributes) + **behavior** (methods) together.

**Without OOP:**
```python
# 10 variables for one employee
emp1_name = "Alice"
emp1_salary = 75000
emp1_dept = "Engineering"
# ...50 more variables for 5 employees
```

**With OOP:**
```python
class Employee:
    def __init__(self, name, salary, dept):
        self.name = name
        self.salary = salary
        self.dept = dept

alice = Employee("Alice", 75000, "Engineering")
bob = Employee("Bob", 65000, "Sales")
```

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-classes.md](concepts/lesson-01-classes.md) | Classes and objects |
| 02 | [lesson-02-methods.md](concepts/lesson-02-methods.md) | Instance and class methods |
| 03 | [lesson-03-inheritance.md](concepts/lesson-03-inheritance.md) | Inheritance and super() |
| 04 | [lesson-04-polymorphism.md](concepts/lesson-04-polymorphism.md) | Polymorphism |
| 05 | [lesson-05-encapsulation.md](concepts/lesson-05-encapsulation.md) | Encapsulation and @property |
| 06 | [lesson-06-abstraction.md](concepts/lesson-06-abstraction.md) | Abstract classes |
| 07 | [lesson-07-dunder.md](concepts/lesson-07-dunder.md) | Dunder/magic methods |

---

## The 4 Pillars of OOP

```
ENCAPSULATION  → Bundle data + methods; control access
INHERITANCE    → Child classes inherit from parent classes
POLYMORPHISM   → Same interface, different behaviors
ABSTRACTION    → Hide complexity, expose interface
```

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [Library Management](guided-projects/project-01-library-management/) | Book, Member, Library classes |
| [Employee System](guided-projects/project-02-employee-system/) | Full employee hierarchy |
| [Banking System](guided-projects/project-03-banking-system/) | Account, Transaction classes |

---

## ✅ Completion Checklist

- [ ] Can define a class with `__init__`
- [ ] Understand instance vs class attributes
- [ ] Can write instance and class methods
- [ ] Can implement inheritance with `super()`
- [ ] Understand polymorphism through method overriding
- [ ] Can use `@property` for encapsulation
- [ ] Built Library, Employee, and Banking systems

---

## Previous: [Phase 06](../phase-06-error-handling/README.md) | Next: [Phase 08](../phase-08-intermediate-projects/)
