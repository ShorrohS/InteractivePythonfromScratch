# Lesson 04 — Test-Driven Development

**Phase:** 14 — Testing | **Time:** ~50 min

---

## Part 1: The Red-Green-Refactor Cycle

Test-Driven Development (TDD) inverts the usual order. You write the test
before you write any production code.

```
   ┌─────────┐
   │   RED   │  Write a failing test for the next small piece of functionality
   └────┬────┘
        │
   ┌────▼────┐
   │  GREEN  │  Write the minimal code to make the test pass — no more
   └────┬────┘
        │
   ┌────▼────────┐
   │  REFACTOR   │  Clean up the code while keeping all tests green
   └─────────────┘
        │
        └─────────────── repeat ──────────────────────────────┐
```

**RED** — The test fails. This is expected. A test that can never fail is
useless. The failing test defines what "done" means for this increment.

**GREEN** — Write the absolute minimum code needed to pass the test. Resist the
urge to generalize or add features. If hardcoding `return 0` makes the test
pass, hardcode it — the next test will force you to generalize.

**REFACTOR** — Now that tests are green, improve the code: rename variables,
extract methods, remove duplication. The tests tell you immediately if you
break anything.

---

## Part 2: Why TDD Leads to Better Design

TDD forces you to think about the interface before the implementation.

- **Simpler code** — you only write what a failing test demands. No speculative features.
- **Testable by construction** — code that is hard to test in TDD is hard to test later. Pain in TDD is a design signal.
- **Tests document intent** — the test suite reads like a specification. New developers understand the system by reading the tests.
- **Confidence to refactor** — every refactoring step is protected by green tests.

The 3 Laws of TDD (Uncle Bob Martin):

1. You may not write production code unless it is to make a failing unit test pass.
2. You may not write more of a unit test than is sufficient to fail.
3. You may not write more production code than is sufficient to pass the failing test.

---

## Part 3: TDD Step by Step — ShoppingCart

We will build a `ShoppingCart` class from scratch using TDD. Each section shows
the test first, then the implementation.

**Step 1 — RED: empty cart has zero total**

```python
# test_cart.py
from cart import ShoppingCart

def test_empty_cart_has_zero_total():
    cart = ShoppingCart()
    assert cart.total() == 0.0
```

Run: `pytest test_cart.py` → **FAIL** (no module `cart`)

**Step 1 — GREEN: implement just enough**

```python
# cart.py
class ShoppingCart:
    def __init__(self):
        self._items = []

    def total(self) -> float:
        return 0.0          # hardcoded — sufficient to pass the one test
```

Run: **PASS** ✅

---

**Step 2 — RED: adding an item changes the total**

```python
def test_add_one_item_updates_total():
    cart = ShoppingCart()
    cart.add_item("Apple", price=1.50, qty=3)
    assert cart.total() == 4.50
```

Run: **FAIL** (`ShoppingCart` has no `add_item`)

**Step 2 — GREEN: implement add_item and real total**

```python
class ShoppingCart:
    def __init__(self):
        self._items = []

    def add_item(self, name: str, price: float, qty: int = 1) -> None:
        self._items.append({"name": name, "price": price, "qty": qty})

    def total(self) -> float:
        return sum(item["price"] * item["qty"] for item in self._items)
```

Run: **PASS** ✅  
Both tests pass — previous test still green.

---

**Step 3 — RED: removing an item decreases the total**

```python
def test_remove_item_decreases_total():
    cart = ShoppingCart()
    cart.add_item("Apple", price=1.50, qty=2)
    cart.add_item("Banana", price=0.75, qty=4)
    cart.remove_item("Apple")
    assert cart.total() == pytest.approx(3.00)

def test_remove_nonexistent_item_raises():
    cart = ShoppingCart()
    with pytest.raises(KeyError):
        cart.remove_item("Ghost")
```

Run: **FAIL** (no `remove_item`)

**Step 3 — GREEN: implement remove_item**

```python
def remove_item(self, name: str) -> None:
    for i, item in enumerate(self._items):
        if item["name"] == name:
            del self._items[i]
            return
    raise KeyError(f"Item '{name}' not in cart")
```

Run: **PASS** ✅

---

**Step 4 — RED: apply a percentage discount**

```python
def test_apply_discount_reduces_total():
    cart = ShoppingCart()
    cart.add_item("Laptop", price=1000.0, qty=1)
    cart.apply_discount(10)   # 10% off
    assert cart.total() == pytest.approx(900.0)

def test_discount_over_100_raises():
    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.apply_discount(110)

def test_negative_discount_raises():
    cart = ShoppingCart()
    with pytest.raises(ValueError):
        cart.apply_discount(-5)
```

**Step 4 — GREEN: implement apply_discount**

```python
def apply_discount(self, percent: float) -> None:
    if not 0 <= percent <= 100:
        raise ValueError(f"Discount must be 0–100, got {percent}")
    self._discount = percent

def total(self) -> float:
    subtotal = sum(item["price"] * item["qty"] for item in self._items)
    discount = getattr(self, "_discount", 0)
    return subtotal * (1 - discount / 100)
```

Run: **PASS** ✅

**Step 4 — REFACTOR: clean up the initializer**

```python
def __init__(self):
    self._items = []
    self._discount = 0.0    # explicit default — cleaner than getattr
```

Run all tests: **still PASS** ✅ — refactoring was safe.

---

## Part 4: When TDD Is Most Valuable

TDD works best for:
- **New complex logic** — the interface is unclear; writing tests first forces clarity
- **Bug fixes** — write a test that reproduces the bug first, then fix it. The test proves the fix and prevents regression
- **Core business rules** — discount calculations, validation, financial logic

TDD is harder for:
- **Exploratory / prototype code** — when you are still discovering the design
- **UI and visual layout** — difficult to write meaningful tests before seeing the result
- **Very tight deadline** — writing tests first takes more upfront time (but saves time overall)

The key insight: TDD is a design tool as much as a testing tool. The discomfort
of writing a test first often signals a design problem that would have hurt you later.

---

## Practice Exercises

1. Using TDD, build a `Stack` class one test at a time. Start with
   `test_new_stack_is_empty`, then `test_push_increases_size`, then
   `test_pop_returns_last_pushed`. Show each RED→GREEN cycle.

2. A `BankAccount.withdraw()` has a bug: it allows negative withdrawals. Write
   the failing test first, then fix the implementation.

3. Add a `clear()` method to the ShoppingCart above using TDD. Write the test
   before adding any code to `cart.py`.

4. Explain in your own words why hardcoding `return 0` in Step 1 is the
   correct TDD move, even though it feels "wrong".

---

## Next Lesson

**[Lesson 05 → Mocking and Patching](lesson-05-mocking.md)**
