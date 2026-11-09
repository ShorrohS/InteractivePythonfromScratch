# Phase 14 — Quiz 01: Testing

**Questions:** 18 | **Pass:** 14/18 | **Time:** 20 min (no notes)

---

## Section 1: unittest Basics (Q1–Q4)

**Q1.** What is the output of this code?

```python
import unittest

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(2 + 2, 5)

if __name__ == "__main__":
    unittest.main()
```
```
A) Nothing — the test passes silently
B) FAIL — AssertionError: 4 != 5
C) ERROR — TypeError
D) PASSED
```

---

**Q2.** Which method should you use to verify that calling `my_func()` raises a `ValueError`?

```python
class TestMyFunc(unittest.TestCase):
    def test_raises(self):
        # which assertion goes here?
        pass
```
```
A) self.assertEqual(my_func(), ValueError)
B) self.assertRaises(ValueError, my_func)
C) self.assertTrue(raises(ValueError))
D) self.assertIsInstance(my_func(), ValueError)
```

---

**Q3.** What is the purpose of `setUp` in a `unittest.TestCase`?

```
A) It runs once before all tests in the class
B) It runs before every individual test method
C) It runs after every individual test method
D) It is optional boilerplate with no special meaning
```

---

**Q4.** What is wrong with this test class?

```python
class TestCalc(unittest.TestCase):
    def add_test(self):
        self.assertEqual(1 + 1, 2)
```
```
A) The class doesn't inherit from TestCase correctly
B) assertEqual is the wrong assertion
C) The method is named add_test instead of test_add — pytest/unittest won't discover it
D) Nothing is wrong
```

---

## Section 2: pytest Fundamentals (Q5–Q9)

**Q5.** Which of these is valid pytest output when a test fails?

```python
def test_values():
    result = [1, 2, 3]
    assert result == [1, 2, 4]
```
```
A) ValueError: lists are not equal
B) AssertionError: assert [1, 2, 3] == [1, 2, 4] — with a diff showing the mismatch
C) TypeError: cannot compare lists
D) Nothing — pytest passes because most elements match
```

---

**Q6.** What does `pytest -v` do?

```
A) Runs only verbose (DEBUG-level) test functions
B) Validates the test files without running them
C) Shows each test's full name and PASSED/FAILED result instead of dots
D) Runs tests in parallel using multiple CPU cores
```

---

**Q7.** A file is named `helpers.py` and contains a function called `check_data`. Will pytest discover it automatically?

```
A) Yes — pytest discovers all Python files
B) No — pytest only discovers files named test_*.py or *_test.py
C) Yes — if the function starts with "check"
D) No — pytest requires a conftest.py to locate test files
```

---

**Q8.** What does this test verify?

```python
import pytest

def test_empty_list_raises():
    my_list = []
    with pytest.raises(IndexError):
        _ = my_list[0]
```
```
A) That an empty list raises IndexError when you access index 0
B) That IndexError is imported correctly
C) That my_list is actually empty
D) That pytest.raises is a valid context manager
```

---

**Q9.** What is the output of running this test with `pytest`?

```python
@pytest.mark.parametrize("n, expected", [(2, 4), (3, 9), (4, 16)])
def test_square(n, expected):
    assert n ** 2 == expected
```
```
A) One test runs; it passes if all three cases pass
B) Three separate tests run; each case is an independent PASS or FAIL
C) SyntaxError — parametrize requires a class
D) The decorator is ignored; pytest runs one test with no arguments
```

---

## Section 3: Fixtures (Q10–Q12)

**Q10.** What is a pytest fixture?

```
A) A special assertion that checks test environment setup
B) A function decorated with @pytest.fixture that provides a reusable value or object to tests
C) A configuration file that tells pytest where to find tests
D) A class that replaces unittest.TestCase
```

---

**Q11.** A test file has this fixture and two tests:

```python
@pytest.fixture
def counter():
    return [0]

def test_first(counter):
    counter[0] += 1
    assert counter[0] == 1

def test_second(counter):
    assert counter[0] == 0   # what happens here?
```

What is the result of `test_second`?

```
A) FAIL — counter[0] is 1 because test_first modified it
B) PASS — each test gets a fresh fixture; counter[0] starts at 0
C) ERROR — counter is not defined in test_second's scope
D) PASS — lists are always reset between tests automatically
```

---

**Q12.** Which fixture scope should you choose for an object that is expensive to create and that multiple tests only READ from (never mutate)?

```
A) scope="function"   — create a new one for every test
B) scope="module"     — create one per test file, reused across all tests in that file
C) scope="class"      — create one per test class only
D) scope="call"       — create one per test call (same as function)
```

---

## Section 4: Mocking (Q13–Q15)

**Q13.** What does this test actually test?

```python
from unittest.mock import patch

@patch("requests.get")
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"name": "Alice"}
    result = get_user(1)
    assert result == {"name": "Alice"}
```
```
A) That requests.get correctly connects to the network
B) That get_user() processes a mocked response correctly — no real HTTP call is made
C) That mock_get is callable
D) That requests is installed correctly
```

---

**Q14.** What is the difference between `Mock` and `MagicMock`?

```
A) Mock is for functions; MagicMock is for classes
B) MagicMock supports Python magic/dunder methods (like __len__, __iter__) automatically; Mock does not
C) Mock raises AttributeError on any attribute access; MagicMock raises TypeError
D) They are identical — one is just an alias for the other
```

---

**Q15.** A test calls `mock_obj.save(user)` and you want to confirm it was called once with `{"name": "Alice"}`. Which assertion is correct?

```
A) assert mock_obj.save == {"name": "Alice"}
B) mock_obj.save.assert_called_once_with({"name": "Alice"})
C) assert mock_obj.save.call_count == 1 and mock_obj.save.args == [{"name": "Alice"}]
D) mock_obj.assert_called_with("save", {"name": "Alice"})
```

---

## Section 5: Coverage & TDD (Q16–Q18)

**Q16.** You run `pytest --cov=mymodule --cov-report=term-missing` and see:

```
Name        Stmts   Miss  Cover   Missing
mymodule       20      6    70%   12-14, 22, 25-26
```

What does this tell you?

```
A) 70% of the test functions in mymodule were run
B) 6 lines in mymodule (lines 12–14, 22, 25–26) were never reached by any test
C) 70% of tests passed
D) mymodule has 70 statements and 6 errors
```

---

**Q17.** In TDD, what is the correct order of the red-green-refactor cycle?

```
A) Write implementation → run tests → write tests
B) Write tests → run tests (confirm fail) → write minimum code to pass → clean up
C) Write tests → write implementation → delete tests → ship
D) Refactor first → write tests → run tests
```

---

**Q18.** Which statement about test coverage is TRUE?

```
A) 100% line coverage guarantees there are no bugs
B) A test that always passes is just as valuable as a test that can fail
C) High coverage (e.g. 90%+) reduces confidence — it means you wrote too many tests
D) Coverage shows which lines were executed, but not whether the assertions are meaningful
```

---

## Answers

.
.
.
.
.
.

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | B | `assertEqual(4, 5)` fails — unittest prints `FAIL` with an `AssertionError` showing the mismatch |
| 2 | B | `assertRaises(ExceptionType, callable)` is the unittest way; or use `with self.assertRaises(...)` |
| 3 | B | `setUp` runs before **every** test method; `setUpClass` runs once before all tests in the class |
| 4 | C | unittest (and pytest) only discover methods named `test_*`; `add_test` is silently ignored |
| 5 | B | pytest rewrites `assert` and shows a detailed diff including which element differed |
| 6 | C | `-v` (verbose) prints each test's full name and status; without it pytest shows dots |
| 7 | B | pytest discovers files matching `test_*.py` or `*_test.py` by default; `helpers.py` is skipped |
| 8 | A | The `with pytest.raises(IndexError)` block verifies that accessing `my_list[0]` raises `IndexError` |
| 9 | B | `@parametrize` generates one independent test per tuple; three separate tests appear in the output |
| 10 | B | A fixture is a `@pytest.fixture`-decorated function that provides setup data or objects to tests |
| 11 | B | Default fixture scope is `function` — a fresh `[0]` is returned for each test; modifications don't bleed |
| 12 | B | `scope="module"` creates the fixture once per file; ideal for read-only, expensive-to-build objects |
| 13 | B | `@patch` replaces the real `requests.get` with a mock — no network call is made; the logic of `get_user` is what's tested |
| 14 | B | `MagicMock` pre-configures magic methods (`__len__`, `__iter__`, etc.); `Mock` raises `AttributeError` if you use them without setup |
| 15 | B | `assert_called_once_with(...)` is the correct Mock method; it checks both call count and arguments |
| 16 | B | The `Missing` column lists the exact line numbers never executed; 6 lines were skipped by all tests |
| 17 | B | Red (write failing test) → Green (make it pass) → Refactor (clean up) is the TDD cycle |
| 18 | D | Coverage measures execution, not correctness; a test with a wrong assertion can pass and still show 100% coverage |
