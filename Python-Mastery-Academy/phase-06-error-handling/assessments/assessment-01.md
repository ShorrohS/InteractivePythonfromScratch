# Phase 06 — Completion Assessment

> Pass mark: 80% | Time: 25 minutes

---

## PART A: Write the Code

**Task 1.** Build a robust data validator that:
- Validates: name (non-empty string), age (int 0–120), salary (positive float), email (contains @ and .)
- Returns `(True, {})` on success or `(False, {field: error_msg})` on failure
- Does NOT raise exceptions — returns the result

---

**Task 2.** Create a custom exception hierarchy for an e-commerce system:
- `EcommerceError` (base)
- `OutOfStockError(product, requested_qty, available_qty)`
- `PaymentDeclinedError(reason, amount)`
- `ShippingError(address, reason)`

Write a function `place_order(product, qty, payment)` that raises appropriate errors.

---

**Task 3.** Write a `batch_process(records, processor_func)` function that:
- Calls `processor_func(record)` for each record
- Catches any exceptions per record without stopping the batch
- Returns `{"success": [...], "failed": [{"record": ..., "error": ...}]}`

---

## PART B: Predict the Output

**Q4.**
```python
try:
    x = 1 / 0
except ZeroDivisionError:
    print("zero")
else:
    print("success")
finally:
    print("done")
```

**Q5.**
```python
def f():
    try:
        return "try"
    finally:
        return "finally"
print(f())
```

---

## PART C: Fix the Bugs

**Q6.**
```python
try:
    data = fetch_data()
except:     # Bug 1
    pass    # Bug 2
```

**Q7.**
```python
class MyError(Exception):
    def __init__(message):    # Bug
        super().__init__(message)
```

---

## Answers

**Q4:** `zero` then `done` (else skipped — exception occurred)

**Q5:** `"finally"` — finally's return overrides try's return. (This is a known Python quirk — avoid return in finally.)

**Q6 fixes:**
1. Bare `except:` → use `except Exception as e:`
2. Silently swallowing → at minimum `logger.error(e)` or `raise`

**Q7 fix:** Missing `self` parameter:
```python
def __init__(self, message):
    super().__init__(message)
```
