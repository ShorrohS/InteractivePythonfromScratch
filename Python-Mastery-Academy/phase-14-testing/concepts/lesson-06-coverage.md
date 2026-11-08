# Lesson 06 — Code Coverage and Best Practices

**Phase:** 14 — Testing | **Time:** ~35 min

---

## Part 1: What Coverage Measures

**Line coverage** — which lines of code were executed during the test run.
A line never reached cannot be tested.

**Branch coverage** — which `if/else` paths were taken. A function can reach
100% line coverage and still leave entire logic paths untested.

```python
def discount_price(price: float, member: bool) -> float:
    if member:
        return price * 0.9    # only covered when member=True
    return price               # never reached if all tests pass member=True
```

With only `member=True` tests: line coverage 100%, branch coverage 50%.
Branch coverage is the more honest number.

---

## Part 2: Installing and Running pytest-cov

```bash
pip install pytest-cov
```

```bash
# Basic terminal report
pytest --cov=src

# Show the specific lines NOT covered
pytest --cov=src --cov-report=term-missing

# HTML report — open htmlcov/index.html in a browser
pytest --cov=src --cov-report=html

# Combined output
pytest --cov=src --cov-report=term-missing --cov-report=html

# Fail the build if coverage drops below a threshold
pytest --cov=src --cov-fail-under=80
```

Example terminal output:

```
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
src/calculator.py      18      2    89%   34, 41
src/cart.py            42      0   100%
src/notifier.py        15      5    67%   28-32
-------------------------------------------------
TOTAL                  75      7    91%
```

The `Missing` column shows exactly which line numbers have no tests yet.

---

## Part 3: The .coveragerc Configuration File

Place `.coveragerc` in the project root to persist coverage settings:

```ini
[run]
source = src
omit =
    src/migrations/*
    src/config.py
branch = true

[report]
fail_under = 80
show_missing = true
exclude_lines =
    pragma: no cover
    if __name__ == .__main__.:
    raise NotImplementedError

[html]
directory = htmlcov
```

Mark a single line to exclude from coverage with a comment:

```python
def debug_dump(self):     # pragma: no cover
    print(vars(self))     # debug helper — not worth a test
```

---

## Part 4: Reading the HTML Report

After running `pytest --cov=src --cov-report=html`, open `htmlcov/index.html`:

- **Green lines** — executed during at least one test
- **Red lines** — never executed (a test case is missing)
- **Yellow lines** — partial branch (one path taken, the other never tested)

Click any filename to see line-by-line highlighting. Red and yellow lines
are your test backlog — work through them from most important to least.

---

## Part 5: Coverage Pitfalls

**100% line coverage does not mean bug-free.**

```python
def add(a, b):
    return a + b

def test_add():
    add(3, 4)    # executes the line — but no assert!
```

Coverage is 100%. The test catches nothing. Coverage measures execution,
not correctness.

**Chasing a number produces meaningless tests.**

```python
# Written purely to bump the percentage
def test_cart_for_coverage():
    cart = ShoppingCart()
    cart.add_item("X", 1.0, 1)
    cart.total()    # no assertion
```

Practical targets that balance effort and value:

| Module type | Target |
|-------------|--------|
| Business logic (calculations, validation, rules) | 80–95% |
| API handlers / controllers | 70–80% |
| CLI entry points, glue code | 50–70% |
| Auto-generated code, migrations | Omit from reports |

---

## Part 6: Testing Best Practices

**1. One scenario per test function.** Multiple asserts are fine when they
all verify the same scenario.

```python
# ✅ One scenario — both asserts relate to the deposit
def test_deposit_increases_balance():
    acc = BankAccount("Alice", 100)
    acc.deposit(50)
    assert acc.balance == 150
    assert acc.balance > 0

# ❌ Two unrelated scenarios — split into two tests
def test_account_operations():
    acc = BankAccount("Alice", 100)
    acc.deposit(50)
    assert acc.balance == 150       # scenario 1
    acc.withdraw(300)               # scenario 2 buried here
```

**2. Descriptive test names** — name the function, the condition, and the result:

```python
# ❌
def test_account(): ...

# ✅
def test_withdraw_when_balance_insufficient_raises_value_error(): ...
def test_deposit_negative_amount_raises_value_error(): ...
```

**3. Fixtures for shared setup** — never duplicate setup logic across tests.

**4. Mirror source structure** — test files parallel source files:

```
src/
    calculator.py
    cart.py
tests/
    test_calculator.py
    test_cart.py
```

**5. Keep tests independent** — no test should depend on state created by
another. Each test must run correctly in any order, including alone.

**6. Run tests before every commit** — a broken commit wastes the next developer's time.

```bash
pytest -x --tb=short    # stop on first failure, compact traceback
```

---

## Part 7: CI Integration

Run tests automatically on every push with GitHub Actions:

```yaml
# .github/workflows/tests.yml

name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests with coverage
        run: pytest --cov=src --cov-fail-under=80 --tb=short
```

Every pull request runs the full suite. A red badge blocks the merge.
Tests that are too slow for CI belong in a separate `slow` marker and run nightly.

---

## Practice Exercises

1. Run `pytest --cov=src --cov-report=term-missing` on any project. Find two
   uncovered lines and write the specific test cases that cover them.

2. Create a `.coveragerc` file that omits `tests/` and `src/config.py`, enables
   branch coverage, and fails the build if coverage falls below 75%.

3. Identify everything wrong with this test, then rewrite it correctly:
   ```python
   def test_everything():
       cart = ShoppingCart()
       cart.add_item("A", 10, 1)
       cart.add_item("B", 5, 2)
       assert cart.total() == 20
       cart.apply_discount(50)
       assert cart.total() == 10
       cart.remove_item("A")
       assert cart.total() == 5
   ```

4. Write a minimal GitHub Actions YAML workflow that installs dependencies from
   `requirements.txt` and runs pytest with a coverage threshold of 80%.

---

## Next Lesson

**Phase 14 complete — well done! Next: [Phase 15 → GUI Programming](../../phase-15-gui/concepts/lesson-01-tkinter-basics.md)**
