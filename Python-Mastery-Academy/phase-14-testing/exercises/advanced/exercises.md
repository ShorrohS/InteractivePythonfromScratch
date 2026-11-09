# Phase 14 — Advanced Exercises

> These are harder. Plan your test strategy before writing code.
> Think about what each test is actually verifying — and what it is NOT verifying.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. TDD: Build a ShoppingCart from Scratch**

Using the **red-green-refactor** cycle, build a `ShoppingCart` class entirely test-first. You are given a specification below — **do not write any implementation code until you have a failing test for that feature**.

Specification:
- `add_item(name, price, quantity=1)` — adds an item; adding the same name again increments quantity
- `remove_item(name)` — removes the item completely; raises `KeyError` if not found
- `get_total()` — returns sum of `price × quantity` for all items
- `item_count()` — returns total number of individual items (sum of all quantities)
- `clear()` — empties the cart

Steps:
1. Write ALL tests first — run pytest and confirm they all fail (**red**)
2. Write the minimum `ShoppingCart` code to make each test pass (**green**)
3. Refactor the implementation — cleaner names, extracted helpers — and confirm tests still pass (**refactor**)

Mark each block with a comment: `# RED — failing tests`, `# GREEN — minimal implementation`, `# REFACTOR — cleaned up`.

---

**Q2. Mock a Database Layer**

The `UserService` class below depends on a `UserRepository` object. Write tests that **replace the repository with a `MagicMock`** so no real database is needed. Cover three scenarios: user found (returns a dict), user not found (mock returns `None`, service raises `ValueError`), and a database error (set `side_effect` to `Exception("DB timeout")`).

```python
# Code under test
class UserService:
    def __init__(self, repository):
        self.repo = repository

    def get_user_by_email(self, email):
        user = self.repo.find_by_email(email)
        if user is None:
            raise ValueError(f"User not found: {email}")
        return user

    def create_user(self, email, name):
        if self.repo.find_by_email(email) is not None:
            raise ValueError(f"Email already registered: {email}")
        return self.repo.save({"email": email, "name": name})
```

Use `unittest.mock.MagicMock`. After each call, verify the mock was called with the correct arguments using `assert_called_once_with`.

---

**Q3. Full Test Suite for a REST API Client**

The `WeatherClient` class below wraps an HTTP API. Write a **complete test suite** that mocks `requests.get` and covers four scenarios: successful response, API error (non-200 status code), network timeout (`requests.exceptions.Timeout`), and a response whose `.json()` raises `ValueError`. For each case, assert both the return value (or raised exception) and that `requests.get` was called with the correct URL.

```python
# Code under test
import requests

class WeatherClient:
    BASE_URL = "https://api.weather.example.com"

    def get_temperature(self, city):
        try:
            response = requests.get(f"{self.BASE_URL}/current?city={city}")
            response.raise_for_status()
            data = response.json()
            return data["temperature"]
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request timed out for city: {city}")
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(f"API error: {e}")
```

---

**Q4. Share Fixtures with conftest.py**

You have two test files — `test_account.py` and `test_transaction.py` — that both need a `bank_account` fixture and a `sample_transactions` fixture. Instead of repeating them:

1. Create a `conftest.py` file containing both fixtures
2. Show how each test file uses them without importing anything from `conftest.py`
3. Set `bank_account` to **function scope** (default) and `sample_transactions` to **module scope** — explain in comments what this means: when each fixture is created and torn down, and why you'd choose one over the other

```python
# BankAccount class — include this in conftest.py or a shared module
class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance

    def deposit(self, amount):
        self._balance += amount

    def get_balance(self):
        return self._balance
```

---

**Q5. Unit Tests vs Integration Tests**

For the `OrderProcessor` class below, write **two separate test files**:

- `test_order_unit.py` — unit tests that mock every external dependency (`inventory`, `payment_gateway`, `notifier`)
- `test_order_integration.py` — integration tests that use simple real in-memory implementations (no mocks)

Then add a comment block (10–15 lines) at the top of each file explaining:
- What this test type verifies vs what it does NOT verify
- When you would run it in a development workflow
- Why it runs faster or slower than the other type

```python
# Code under test
class OrderProcessor:
    def __init__(self, inventory, payment_gateway, notifier):
        self.inventory = inventory
        self.payment   = payment_gateway
        self.notifier  = notifier

    def place_order(self, item, quantity, amount):
        if not self.inventory.check_stock(item, quantity):
            raise ValueError("Insufficient stock")
        self.payment.charge(amount)
        self.inventory.deduct(item, quantity)
        self.notifier.send_confirmation(item, quantity)
        return {"status": "confirmed", "item": item, "qty": quantity}
```

---

**Q6. Test Async Code with pytest-asyncio**

The async function below fetches weather data using `aiohttp`. Write **async test functions** using `pytest-asyncio` that test: a successful fetch returning a temperature, a failed fetch (status != 200, expects `ConnectionError`), and two concurrent fetches using `asyncio.gather`.

```python
# Code under test
import asyncio
import aiohttp

async def fetch_temperature(session, city):
    url = f"https://api.weather.example.com/current?city={city}"
    async with session.get(url) as response:
        if response.status != 200:
            raise ConnectionError(f"Failed to fetch data for {city}")
        data = await response.json()
        return data["temperature"]
```

Show how to mock `aiohttp.ClientSession` so no real HTTP calls are made, and how to decorate each test with `@pytest.mark.asyncio`.

---

**Q7. Improve Coverage from 60% to 95%**

The `calculator.py` module below has multiple branches. First, write a minimal test suite that covers only ~60% of lines (deliberately omit some branches). Run `pytest --cov=calculator --cov-report=term-missing` and record the output. Then write additional tests to reach 95% coverage, tagging each new test with `# COVERAGE: covers <branch description>`.

```python
# calculator.py — Code under test

def safe_divide(a, b):
    if b == 0:
        return None
    return a / b

def grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def bmi(weight_kg, height_m):
    if height_m <= 0:
        raise ValueError("Height must be positive")
    bmi_val = weight_kg / (height_m ** 2)
    if bmi_val < 18.5:
        return "Underweight"
    elif bmi_val < 25:
        return "Normal"
    elif bmi_val < 30:
        return "Overweight"
    else:
        return "Obese"
```

---

> **Solutions:** `../../solutions/advanced/solutions.md`
