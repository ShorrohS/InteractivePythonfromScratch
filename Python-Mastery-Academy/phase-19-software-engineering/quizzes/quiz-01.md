# Phase 19 — Quiz 01: Software Engineering

**Questions:** 20 | **Pass:** 16/20 | **Time:** 25 min (closed notes)

> Most questions show code and ask *what principle does this violate?* or *which fix is correct?*. Pure memorisation won't be enough.

---

## Section 1: Clean Code (Q1–Q4)

**Q1.** Which of these function names best follows clean code conventions?

```
A) process()
B) do_stuff(d)
C) calculate_monthly_interest(principal, annual_rate)
D) calc(p, r)
```

---

**Q2.** What is wrong with this code?

```python
def check(u):
    if u != None:
        if u['a'] == True:
            if u['r'] == 'admin':
                return True
            else:
                return False
        else:
            return False
    else:
        return False
```

```
A) It has a syntax error
B) It is too deeply nested and uses cryptic names — should use guard clauses and meaningful names
C) It returns bool incorrectly
D) It is missing type hints only
```

---

**Q3.** You have a function called `save_user_and_send_welcome_email_and_log_to_database`. Which principle does this name warn you it probably violates?

```
A) Open/Closed Principle
B) Single Responsibility Principle
C) Liskov Substitution Principle
D) Interface Segregation Principle
```

---

**Q4.** A developer changes `TAX = 0.08` to `TAX = 0.09` in one place and the entire codebase updates correctly. What clean code practice makes this possible?

```
A) Using constants instead of magic numbers
B) Adding type hints
C) Using f-strings
D) Writing docstrings
```

---

## Section 2: SOLID Principles (Q5–Q11)

**Q5.** A class `OrderManager` handles validation, pricing, persistence, and email sending. Which SOLID principle does it violate?

```
A) Open/Closed
B) Single Responsibility
C) Dependency Inversion
D) Interface Segregation
```

---

**Q6.** Look at this code:

```python
def export(data, fmt):
    if fmt == 'csv':
        ...
    elif fmt == 'pdf':
        ...
    elif fmt == 'html':
        ...
    # Every new format requires editing this function
```

Which SOLID principle does this design violate?

```
A) Single Responsibility
B) Liskov Substitution
C) Open/Closed
D) Dependency Inversion
```

---

**Q7.** What does the Liskov Substitution Principle state in plain terms?

```
A) Classes should be small
B) A subclass must be usable wherever its parent is expected, without breaking the program
C) High-level modules should not import low-level modules
D) Interfaces should be split into smaller ones
```

---

**Q8.** `Square` extends `Rectangle` and overrides `set_width` to also change the height (to keep it a square). Code that sets `width=4, height=6` on a `Rectangle` gets different results when it receives a `Square`. Which principle is violated?

```
A) Single Responsibility
B) Open/Closed
C) Liskov Substitution
D) Interface Segregation
```

---

**Q9.** Which code example demonstrates Dependency Inversion correctly?

```
A) class Service:
       def __init__(self):
           self.db = MySQLDatabase()   # direct instantiation

B) class Service:
       def __init__(self, db: Database):   # abstract type injected
           self.db = db

C) class Service:
       db = MySQLDatabase()   # class-level attribute

D) class Service:
       def connect(self):
           import sqlite3   # import inside method
```

---

**Q10.** A `Worker` interface has `work()`, `eat()`, and `sleep()`. A `RobotWorker` must implement `eat()` and `sleep()` even though robots don't eat or sleep. Which SOLID principle is violated?

```
A) Single Responsibility
B) Open/Closed
C) Liskov Substitution
D) Interface Segregation
```

---

**Q11.** You have a `NotificationService` that directly instantiates `SmtpEmailSender`. To test `NotificationService` without sending real emails, you would need to:

```
A) Mock the SMTP server in production
B) Inject an EmailSender abstraction so a fake can be swapped in during tests
C) Set an environment variable to disable email
D) Use a try/except to catch the SMTP error in tests
```

---

## Section 3: Design Patterns (Q12–Q16)

**Q12.** Which pattern is being implemented here?

```python
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str: ...

class AnimalFactory:
    @staticmethod
    def create(kind: str) -> Animal:
        if kind == 'dog':   return Dog()
        if kind == 'cat':   return Cat()
        raise ValueError(kind)
```

```
A) Observer
B) Strategy
C) Factory
D) Singleton
```

---

**Q13.** An `Order` object maintains a list of `OrderObserver` objects and calls `observer.update('shipped', self)` for each one when its status changes. Which pattern is this?

```
A) Command
B) Observer
C) Repository
D) Strategy
```

---

**Q14.** You have a `SortContext` class that accepts a `sort_strategy` object in its constructor. You can swap `BubbleSort`, `QuickSort`, or `MergeSort` at runtime without changing `SortContext`. Which pattern is this?

```
A) Factory
B) Observer
C) Singleton
D) Strategy
```

---

**Q15.** A `TextEditor` stores a list of `Command` objects. Each command has `execute()` and `undo()`. Calling `editor.undo()` pops the last command and calls its `undo()`. Which pattern is this?

```
A) Strategy
B) Observer
C) Command
D) Repository
```

---

**Q16.** Which pattern does this describe?

> "Move all SQL queries out of the service class into a separate class. The service depends only on an abstract interface, not on the database driver."

```
A) Factory
B) Observer
C) Repository
D) Singleton
```

---

## Section 4: Documentation and Tools (Q17–Q20)

**Q17.** What is wrong with this function signature?

```python
def process(data, mode=1, flag=False):
    ...
```

```
A) It uses keyword arguments, which is wrong
B) It has no type hints, making parameter types ambiguous
C) Default values are not allowed in Python
D) The function name is too short
```

---

**Q18.** In a Google-style docstring, which section documents a value the function returns?

```
A) Yields:
B) Notes:
C) Returns:
D) Output:
```

---

**Q19.** A `pyproject.toml` contains:

```toml
[project.optional-dependencies]
dev = ["pytest>=7.4", "ruff>=0.1"]
```

Which `pip` command installs these dev dependencies?

```
A) pip install mypackage --dev
B) pip install mypackage[dev]
C) pip install mypackage -r dev
D) pip install -e mypackage
```

---

**Q20.** In a GitHub Actions workflow, the `matrix` key is used to:

```
A) Store secrets for deployment
B) Run the same job across multiple Python versions simultaneously
C) Cache pip dependencies between runs
D) Define which branch to push to
```

---

## Answers

.
.
.
.
.
.
.

| Q  | Answer | Explanation |
|----|--------|-------------|
|  1 | C | Descriptive verb + noun + parameters. `process()` and `do_stuff()` say nothing. |
|  2 | B | Four levels of nesting with one-letter names. Guard clauses + `is None` check + `is True` (not `== True`) would fix it. |
|  3 | B | A name listing three verbs is a code smell for SRP. One function should do one thing. |
|  4 | A | Named constants mean the value lives in one place — change it once and it propagates. |
|  5 | B | Four unrelated responsibilities = four reasons to change = SRP violation. |
|  6 | C | Adding a new format requires editing the function — it's not closed for modification. |
|  7 | B | LSP: every subclass must be a valid substitute for its parent without surprising callers. |
|  8 | C | `Square` breaks the `Rectangle` contract (`width` and `height` are independent) — LSP violation. |
|  9 | B | The service depends on an abstract `Database`, not on a concrete class — the definition of DIP. |
| 10 | D | ISP: clients shouldn't be forced to implement methods they don't use. |
| 11 | B | Inject an abstraction so tests can pass a fake without real network calls — this is DIP in practice. |
| 12 | C | A class with a `create` method that picks a concrete class based on a string key — Factory. |
| 13 | B | Subject maintains a list of observers and notifies them on events — Observer. |
| 14 | D | An interchangeable algorithm injected at runtime — Strategy. |
| 15 | C | Operations as objects with execute/undo — Command pattern. |
| 16 | C | Separating data access logic behind an abstract interface — Repository. |
| 17 | B | Without type hints, callers must read the body to know what `data`, `mode`, and `flag` should be. |
| 18 | C | Google-style sections are `Args:`, `Returns:`, `Raises:`, `Yields:`. |
| 19 | B | Square-bracket extras syntax: `pip install mypackage[dev]`. |
| 20 | B | `matrix` defines axes of variation; GitHub runs one job per combination in parallel. |
