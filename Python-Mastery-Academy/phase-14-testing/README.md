# 🧪 Phase 14 — Testing

> **Goal:** Write automated tests that verify your code works correctly.

---

## Why Write Tests?

```
Without tests:
  - You manually run the program each time you make changes
  - Bugs creep in silently
  - Refactoring is terrifying
  - "I think it works" is your confidence level

With tests:
  - Run 100 tests in 2 seconds
  - Immediately know if a change broke something
  - Refactor confidently
  - "Tests pass" is your confidence level
```

---

## Installation

```bash
pip install pytest pytest-cov
```

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-unittest.md](concepts/lesson-01-unittest.md) | Python unittest |
| 02 | [lesson-02-pytest.md](concepts/lesson-02-pytest.md) | pytest fundamentals |
| 03 | [lesson-03-fixtures.md](concepts/lesson-03-fixtures.md) | pytest fixtures |
| 04 | [lesson-04-mocking.md](concepts/lesson-04-mocking.md) | Mocking external dependencies |
| 05 | [lesson-05-coverage.md](concepts/lesson-05-coverage.md) | Test coverage |
| 06 | [lesson-06-tdd.md](concepts/lesson-06-tdd.md) | Test-Driven Development |

---

## Core pytest Syntax

```python
# test_calculator.py
import pytest
from calculator import add, divide

def test_add_positive_numbers():
    assert add(3, 5) == 8

def test_add_negative_numbers():
    assert add(-1, 1) == 0

def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_returns_float():
    result = divide(7, 2)
    assert isinstance(result, float)
    assert result == 3.5

# Fixtures
@pytest.fixture
def sample_data():
    return {"name": "Alice", "score": 95}

def test_with_fixture(sample_data):
    assert sample_data["name"] == "Alice"
    assert sample_data["score"] > 90
```

Run tests:
```bash
pytest                          # Run all tests
pytest test_calculator.py       # Specific file
pytest -v                       # Verbose output
pytest --cov=src --cov-report=html  # With coverage report
```

---

## Naming Conventions

```
test files:     test_*.py or *_test.py
test functions: test_*
test classes:   Test*
```

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [Calculator Tests](guided-projects/project-01-calculator-tests/) | Complete test suite for calculator |

---

## ✅ Completion Checklist

- [ ] Can write pytest test functions
- [ ] Use assert statements correctly
- [ ] Test both happy path and error cases
- [ ] Use fixtures for shared test data
- [ ] Run tests and check coverage report
- [ ] Aim for 80%+ coverage on new code

---

## Previous: [Phase 13](../phase-13-data-analysis/README.md) | Next: [Phase 15](../phase-15-gui/README.md)
