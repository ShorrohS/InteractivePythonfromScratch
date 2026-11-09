# Phase 14 — Intermediate Exercises

> These require writing complete test suites, not just single test functions.
> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. pytest Fixture for BankAccount**

A `BankAccount` class is provided below. Write a **pytest fixture** named `account` that creates and returns a `BankAccount` pre-loaded with a balance of `$500`. Then write at least **four test functions** that use this fixture to test `deposit`, `withdraw`, `get_balance`, and the case where `withdraw` is called with more than the available balance.

```python
# Code under test
class BankAccount:
    def __init__(self, initial_balance=0):
        self._balance = initial_balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def get_balance(self):
        return self._balance
```

---

**Q2. Parametrize a Temperature Converter**

The `celsius_to_fahrenheit` function is defined below. Use **`@pytest.mark.parametrize`** to test it with exactly **five data points**: `(0, 32)`, `(100, 212)`, `(-40, -40)`, `(37, 98.6)`, and `(20, 68)`. Each tuple is `(celsius_input, expected_fahrenheit)`.

```python
# Code under test
def celsius_to_fahrenheit(c):
    return (c * 9 / 5) + 32
```

Write a single test function decorated with `@pytest.mark.parametrize` that covers all five cases. Use `pytest.approx` for floating-point comparisons.

---

**Q3. unittest with setUp and tearDown**

The `Stack` class below uses a Python list internally. Write a `unittest.TestCase` subclass that:
- Uses `setUp` to create a fresh `Stack` instance before every test method
- Uses `tearDown` to print `"--- test complete ---"` after every test method
- Has test methods for: push, pop, peek, is_empty, and popping from an empty stack (expects `IndexError`)

```python
# Code under test
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0
```

---

**Q4. Mock an External API Call**

The `get_user` function below makes a real HTTP request using `requests`. Write tests that **mock `requests.get`** so no network call is ever made. Test two scenarios: (a) the API returns `{"id": 1, "name": "Alice"}` with status 200, and (b) the API returns status 404 (function should return `None`).

```python
# Code under test
import requests

def get_user(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    if response.status_code == 200:
        return response.json()
    return None
```

Use `unittest.mock.patch` as a **decorator** on each test function. Verify that `requests.get` was called with the correct URL.

---

**Q5. Test File-Writing with tmp_path**

The `write_report` function writes text to a file. Use pytest's built-in **`tmp_path` fixture** to test it — no hardcoded paths allowed. Write tests that verify: (a) the file is created, (b) the content matches what was written, and (c) calling the function twice on the same path overwrites the previous content.

```python
# Code under test
def write_report(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)
```

---

**Q6. Return Values and Exceptions for an Inventory System**

The `Inventory` class below manages stock levels. Write a test suite that checks **both return values and raised exceptions** for the `add_item`, `remove_item`, and `get_quantity` methods. You must include at least one `pytest.raises` block and at least one assertion on a return value.

```python
# Code under test
class Inventory:
    def __init__(self):
        self._stock = {}

    def add_item(self, name, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self._stock[name] = self._stock.get(name, 0) + quantity
        return self._stock[name]

    def remove_item(self, name, quantity):
        if name not in self._stock:
            raise KeyError(f"{name} not in inventory")
        if quantity > self._stock[name]:
            raise ValueError("Not enough stock")
        self._stock[name] -= quantity
        return self._stock[name]

    def get_quantity(self, name):
        return self._stock.get(name, 0)
```

---

**Q7. Measure Coverage**

Using the `Inventory` class from Q6, write a test file that achieves **at least 90% line coverage**. Include a comment at the top of the file showing:

1. The exact command to run coverage and generate an HTML report
2. The command to view a terminal summary with missing lines
3. A brief explanation of what "90% coverage" means and why 100% is not always the goal

---

> **Solutions:** `../../solutions/intermediate/solutions.md`
