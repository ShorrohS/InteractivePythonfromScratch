# Phase 14 — Advanced Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/advanced/exercises.md`

---

## Q1. TDD — ShoppingCart from Scratch

```python
# ============================================================
# RED — All tests written first. Run: pytest → all FAIL.
# ============================================================
import pytest

def test_new_cart_has_zero_total():
    cart = ShoppingCart()
    assert cart.get_total() == 0.0

def test_new_cart_item_count_is_zero():
    cart = ShoppingCart()
    assert cart.item_count() == 0

def test_add_single_item():
    cart = ShoppingCart()
    cart.add_item("apple", price=1.50, quantity=3)
    assert cart.get_total() == pytest.approx(4.50)
    assert cart.item_count() == 3

def test_add_two_different_items():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.add_item("banana", 0.50, 4)
    assert cart.get_total() == pytest.approx(4.00)   # 2.00 + 2.00
    assert cart.item_count() == 6

def test_adding_same_item_twice_updates_quantity():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.add_item("apple", 1.00, 3)   # same name → add to quantity
    assert cart.item_count() == 5
    assert cart.get_total() == pytest.approx(5.00)

def test_remove_item():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 2)
    cart.remove_item("apple")
    assert cart.item_count() == 0
    assert cart.get_total() == 0.0

def test_remove_unknown_item_raises():
    cart = ShoppingCart()
    with pytest.raises(KeyError):
        cart.remove_item("ghost")

def test_clear_empties_cart():
    cart = ShoppingCart()
    cart.add_item("apple", 1.00, 5)
    cart.clear()
    assert cart.item_count() == 0
    assert cart.get_total() == 0.0


# ============================================================
# GREEN — Minimal implementation to make all tests pass.
# ============================================================
class ShoppingCart:
    def __init__(self):
        self._items = {}   # name → {"price": float, "quantity": int}

    def add_item(self, name, price, quantity=1):
        if name in self._items:
            self._items[name]["quantity"] += quantity
        else:
            self._items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name):
        if name not in self._items:
            raise KeyError(f"Item not found: {name}")
        del self._items[name]

    def get_total(self):
        return sum(v["price"] * v["quantity"] for v in self._items.values())

    def item_count(self):
        return sum(v["quantity"] for v in self._items.values())

    def clear(self):
        self._items.clear()


# ============================================================
# REFACTOR — Extracted a helper; all tests still pass.
# ============================================================
class ShoppingCart:  # noqa: F811 — intentional redefinition for the refactor step
    def __init__(self):
        self._items = {}

    def add_item(self, name, price, quantity=1):
        if name in self._items:
            self._items[name]["quantity"] += quantity
        else:
            self._items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name):
        if name not in self._items:
            raise KeyError(f"Item not found: {name}")
        del self._items[name]

    def get_total(self):
        return sum(self._line_total(v) for v in self._items.values())

    def item_count(self):
        return sum(v["quantity"] for v in self._items.values())

    def clear(self):
        self._items.clear()

    # --- private helper extracted during refactor ---
    def _line_total(self, entry):
        return entry["price"] * entry["quantity"]
```

Key points:
- Write tests before the class exists — they all fail with `NameError` until the class is defined
- "Minimum green" means the simplest code that makes tests pass; no cleverness yet
- Refactor without adding features — tests must still be green after every change

---

## Q2. Mock a Database Layer

```python
from unittest.mock import MagicMock

# --- Code under test ---
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

# --- Tests ---
import pytest

def test_get_user_found():
    mock_repo = MagicMock()
    # Configure: find_by_email returns a user dict
    mock_repo.find_by_email.return_value = {"email": "alice@example.com", "name": "Alice"}

    service = UserService(mock_repo)
    result = service.get_user_by_email("alice@example.com")

    assert result == {"email": "alice@example.com", "name": "Alice"}
    mock_repo.find_by_email.assert_called_once_with("alice@example.com")

def test_get_user_not_found_raises():
    mock_repo = MagicMock()
    mock_repo.find_by_email.return_value = None   # user does not exist

    service = UserService(mock_repo)
    with pytest.raises(ValueError, match="User not found"):
        service.get_user_by_email("ghost@example.com")

def test_get_user_database_error():
    mock_repo = MagicMock()
    # side_effect makes the mock raise an exception when called
    mock_repo.find_by_email.side_effect = Exception("DB timeout")

    service = UserService(mock_repo)
    with pytest.raises(Exception, match="DB timeout"):
        service.get_user_by_email("anyone@example.com")

def test_create_user_success():
    mock_repo = MagicMock()
    mock_repo.find_by_email.return_value = None   # email not yet registered
    mock_repo.save.return_value = {"email": "bob@example.com", "name": "Bob"}

    service = UserService(mock_repo)
    result = service.create_user("bob@example.com", "Bob")

    assert result["name"] == "Bob"
    mock_repo.save.assert_called_once_with({"email": "bob@example.com", "name": "Bob"})

def test_create_user_duplicate_email_raises():
    mock_repo = MagicMock()
    # Email already exists
    mock_repo.find_by_email.return_value = {"email": "alice@example.com", "name": "Alice"}

    service = UserService(mock_repo)
    with pytest.raises(ValueError, match="Email already registered"):
        service.create_user("alice@example.com", "Alice2")
```

Key points:
- `MagicMock()` creates an object where any attribute access and any call returns another `MagicMock`
- `return_value` sets what the mock returns when called as a function
- `side_effect` overrides `return_value`; when set to an exception class or instance, calling the mock raises it
- `assert_called_once_with(...)` fails if the mock was called zero times, more than once, or with different arguments

---

## Q3. Full Test Suite for a REST API Client

```python
import pytest
from unittest.mock import patch, MagicMock
import requests

# --- Code under test ---
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

# --- Tests ---

@patch("requests.get")
def test_successful_response(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"temperature": 22.5, "city": "London"}
    mock_response.raise_for_status.return_value = None   # no-op on success
    mock_get.return_value = mock_response

    client = WeatherClient()
    temp = client.get_temperature("London")

    assert temp == 22.5
    mock_get.assert_called_once_with(
        "https://api.weather.example.com/current?city=London"
    )

@patch("requests.get")
def test_api_error_raises_connection_error(mock_get):
    mock_response = MagicMock()
    # raise_for_status raises HTTPError for 4xx/5xx status codes
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    client = WeatherClient()
    with pytest.raises(ConnectionError, match="API error"):
        client.get_temperature("Unknown")

    mock_get.assert_called_once_with(
        "https://api.weather.example.com/current?city=Unknown"
    )

@patch("requests.get")
def test_network_timeout_raises_timeout_error(mock_get):
    # side_effect on the mock itself (not .raise_for_status) simulates a network-level timeout
    mock_get.side_effect = requests.exceptions.Timeout()

    client = WeatherClient()
    with pytest.raises(TimeoutError, match="Request timed out for city: Paris"):
        client.get_temperature("Paris")

@patch("requests.get")
def test_malformed_json_raises_key_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    # json() returns a dict that is missing the "temperature" key
    mock_response.json.return_value = {"humidity": 80}
    mock_get.return_value = mock_response

    client = WeatherClient()
    with pytest.raises(KeyError):
        client.get_temperature("Tokyo")
```

Key points:
- `raise_for_status` is a method on the response object; configure it with `side_effect` to simulate HTTP errors
- Setting `side_effect` directly on `mock_get` (the patched function) simulates errors before any response is created
- Each test only asserts what it owns — no test checks things belonging to another test's scenario

---

## Q4. Share Fixtures with conftest.py

```python
# conftest.py — shared fixtures, no import needed in test files
import pytest

class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance

    def deposit(self, amount):
        self._balance += amount

    def get_balance(self):
        return self._balance

@pytest.fixture                      # function scope (default)
def bank_account():
    # Created fresh before EVERY test function that requests it.
    # A test that deposits $100 does NOT affect any other test.
    return BankAccount(balance=100)

@pytest.fixture(scope="module")      # module scope
def sample_transactions():
    # Created ONCE per test module (file), not per test function.
    # Use when the fixture is expensive to build (e.g. parsing a file,
    # seeding a database) and tests only READ from it — never mutate it.
    return [
        {"id": 1, "amount": 50.0,  "type": "deposit"},
        {"id": 2, "amount": 30.0,  "type": "withdraw"},
        {"id": 3, "amount": 100.0, "type": "deposit"},
    ]
```

```python
# test_account.py
# No imports needed — conftest.py is automatically discovered by pytest

def test_initial_balance(bank_account):
    assert bank_account.get_balance() == 100

def test_deposit(bank_account):
    bank_account.deposit(50)
    assert bank_account.get_balance() == 150
    # bank_account here is a DIFFERENT object from the one in test_initial_balance
```

```python
# test_transaction.py

def test_transaction_count(sample_transactions):
    assert len(sample_transactions) == 3

def test_first_transaction_is_deposit(sample_transactions):
    assert sample_transactions[0]["type"] == "deposit"
    # sample_transactions is the SAME object as in test_account.py
    # because its scope is "module" — but here it's a separate module,
    # so it was re-created once for this file.
```

Key points:
- `conftest.py` is automatically discovered by pytest — no imports required
- `scope="function"` (default) — new fixture instance before every test function
- `scope="module"` — one instance for the whole test file; reset at the next module
- `scope="session"` — one instance for the entire test run; never reset until all tests finish
- Choose a wider scope only when the fixture is expensive and safe to share (immutable data, read-only connections)

---

## Q5. Unit Tests vs Integration Tests

```python
# test_order_unit.py
#
# UNIT TESTS — What they verify:
#   The OrderProcessor logic in isolation. Every external dependency
#   (Inventory, PaymentGateway, Notifier) is replaced with a MagicMock,
#   so we are only testing the branching logic inside place_order itself.
#
# What they do NOT verify:
#   Whether the real Inventory correctly tracks stock, whether the real
#   PaymentGateway charges the right amount, or whether the Notifier
#   sends actual emails. Those are each tested separately in their own
#   unit tests.
#
# When to run: on every commit, in CI, before code review — they are
#   fast (milliseconds) and require no external setup.
#
# Speed: very fast — no I/O, no database, no HTTP calls.

from unittest.mock import MagicMock
import pytest

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

@pytest.fixture
def deps():
    inv  = MagicMock()
    pay  = MagicMock()
    note = MagicMock()
    inv.check_stock.return_value = True   # stock available by default
    return inv, pay, note

def test_place_order_returns_confirmed(deps):
    inv, pay, note = deps
    processor = OrderProcessor(inv, pay, note)
    result = processor.place_order("apple", 2, 5.00)
    assert result == {"status": "confirmed", "item": "apple", "qty": 2}

def test_place_order_charges_payment(deps):
    inv, pay, note = deps
    processor = OrderProcessor(inv, pay, note)
    processor.place_order("apple", 2, 5.00)
    pay.charge.assert_called_once_with(5.00)

def test_place_order_insufficient_stock_raises(deps):
    inv, pay, note = deps
    inv.check_stock.return_value = False   # override: no stock
    processor = OrderProcessor(inv, pay, note)
    with pytest.raises(ValueError, match="Insufficient stock"):
        processor.place_order("apple", 100, 50.00)
    pay.charge.assert_not_called()         # payment must NOT be charged
```

```python
# test_order_integration.py
#
# INTEGRATION TESTS — What they verify:
#   That OrderProcessor works correctly when wired to real (in-memory)
#   implementations of Inventory, PaymentGateway, and Notifier.
#   These tests catch wiring bugs — cases where units work individually
#   but interact incorrectly.
#
# What they do NOT verify:
#   External systems (real databases, real payment APIs, real SMTP).
#   The fake implementations here are still in-memory.
#
# When to run: before merging a feature branch, in a nightly build,
#   or as part of a pre-release smoke test.
#
# Speed: slightly slower than unit tests but still fast here because
#   everything is in-memory. Real integration tests touching live
#   services can take seconds or minutes.

import pytest

# --- Minimal real implementations (no mocks) ---
class FakeInventory:
    def __init__(self):
        self._stock = {}

    def add_stock(self, item, qty):
        self._stock[item] = self._stock.get(item, 0) + qty

    def check_stock(self, item, qty):
        return self._stock.get(item, 0) >= qty

    def deduct(self, item, qty):
        self._stock[item] -= qty

class FakePaymentGateway:
    def __init__(self):
        self.charged = []

    def charge(self, amount):
        self.charged.append(amount)

class FakeNotifier:
    def __init__(self):
        self.sent = []

    def send_confirmation(self, item, qty):
        self.sent.append((item, qty))

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

@pytest.fixture
def system():
    inv  = FakeInventory()
    pay  = FakePaymentGateway()
    note = FakeNotifier()
    inv.add_stock("apple", 50)
    return OrderProcessor(inv, pay, note), inv, pay, note

def test_successful_order_integration(system):
    processor, inv, pay, note = system
    result = processor.place_order("apple", 5, 10.00)
    assert result["status"] == "confirmed"
    assert pay.charged == [10.00]              # real charge recorded
    assert note.sent == [("apple", 5)]         # real notification recorded
    assert inv.check_stock("apple", 50) is False   # stock was deducted

def test_order_depletes_stock_integration(system):
    processor, inv, pay, note = system
    processor.place_order("apple", 50, 100.00)
    with pytest.raises(ValueError, match="Insufficient stock"):
        processor.place_order("apple", 1, 2.00)  # now out of stock
```

---

## Q6. Test Async Code with pytest-asyncio

```python
# Install: pip install pytest-asyncio
# Add to pytest.ini or pyproject.toml: asyncio_mode = auto
# OR decorate each test with @pytest.mark.asyncio

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# --- Code under test ---
import aiohttp

async def fetch_temperature(session, city):
    url = f"https://api.weather.example.com/current?city={city}"
    async with session.get(url) as response:
        if response.status != 200:
            raise ConnectionError(f"Failed to fetch data for {city}")
        data = await response.json()
        return data["temperature"]

# --- Tests ---

@pytest.mark.asyncio
async def test_successful_fetch():
    # Build a mock session with an async context manager on .get()
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"temperature": 18.5})

    mock_cm = MagicMock()                    # context manager object
    mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
    mock_cm.__aexit__  = AsyncMock(return_value=False)

    mock_session = MagicMock()
    mock_session.get.return_value = mock_cm

    result = await fetch_temperature(mock_session, "London")
    assert result == 18.5

@pytest.mark.asyncio
async def test_failed_fetch_raises():
    mock_response = MagicMock()
    mock_response.status = 404             # non-200 → should raise

    mock_cm = MagicMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
    mock_cm.__aexit__  = AsyncMock(return_value=False)

    mock_session = MagicMock()
    mock_session.get.return_value = mock_cm

    with pytest.raises(ConnectionError, match="Failed to fetch data for Tokyo"):
        await fetch_temperature(mock_session, "Tokyo")

@pytest.mark.asyncio
async def test_concurrent_fetches():
    # Build two separate mock responses for two different cities
    def make_mock_session(temperature):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"temperature": temperature})
        mock_cm = MagicMock()
        mock_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_cm.__aexit__  = AsyncMock(return_value=False)
        mock_session = MagicMock()
        mock_session.get.return_value = mock_cm
        return mock_session

    session_a = make_mock_session(20.0)
    session_b = make_mock_session(35.0)

    # asyncio.gather runs both coroutines concurrently
    results = await asyncio.gather(
        fetch_temperature(session_a, "London"),
        fetch_temperature(session_b, "Dubai"),
    )
    assert results == [20.0, 35.0]
```

Key points:
- `AsyncMock` is used for coroutines (functions called with `await`)
- `__aenter__` and `__aexit__` are needed to mock `async with` context managers
- `@pytest.mark.asyncio` tells pytest to run the test function inside an event loop
- `asyncio.gather` schedules multiple coroutines to run concurrently

---

## Q7. Improve Coverage from 60% to 95%

```python
# calculator.py
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

```python
# test_calculator.py
#
# Coverage command (run from project root):
#   pytest --cov=calculator --cov-report=term-missing
#
# After initial minimal tests the output looks like:
#   Name           Stmts   Miss  Cover   Missing
#   calculator        20      8    60%   5, 10-11, 14-15, 20-21, 25
#
# The "Missing" column lists every line that was never reached.
# Adding tests for those branches brings coverage to ~100%.

from calculator import safe_divide, grade, bmi
import pytest

# ── Initial tests (~60% coverage) ──────────────────────────────────
def test_safe_divide_normal():
    assert safe_divide(10, 2) == 5.0

def test_grade_a():
    assert grade(95) == "A"

def test_bmi_normal():
    assert bmi(70, 1.75) == "Normal"   # BMI ≈ 22.9

# ── Additional tests to reach 95% ──────────────────────────────────

# COVERAGE: covers safe_divide zero-divisor branch (line 3)
def test_safe_divide_by_zero():
    assert safe_divide(10, 0) is None

# COVERAGE: covers grade B branch (line 10-11)
def test_grade_b():
    assert grade(85) == "B"

# COVERAGE: covers grade C branch (line 12-13)
def test_grade_c():
    assert grade(75) == "C"

# COVERAGE: covers grade D branch (line 14-15)
def test_grade_d():
    assert grade(65) == "D"

# COVERAGE: covers grade F (else) branch (line 16-17)
def test_grade_f():
    assert grade(55) == "F"

# COVERAGE: covers bmi invalid height branch (line 20)
def test_bmi_invalid_height():
    with pytest.raises(ValueError, match="Height must be positive"):
        bmi(70, 0)

# COVERAGE: covers bmi Underweight branch (line 23)
def test_bmi_underweight():
    assert bmi(45, 1.70) == "Underweight"   # BMI ≈ 15.6

# COVERAGE: covers bmi Overweight branch (line 25)
def test_bmi_overweight():
    assert bmi(85, 1.70) == "Overweight"    # BMI ≈ 29.4

# COVERAGE: covers bmi Obese (else) branch (line 27)
def test_bmi_obese():
    assert bmi(100, 1.70) == "Obese"        # BMI ≈ 34.6
```

Coverage insight: after adding these tests the report shows:
```
Name           Stmts   Miss  Cover
calculator        20      1    95%
```
The remaining uncovered line is typically an edge-case branch that requires extreme input. For this module, 95% is excellent and chasing 100% would add low-value tests.
