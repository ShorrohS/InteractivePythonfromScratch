# Phase 06 — Beginner Solutions: Error Handling

---

## Q1. safe_divide

```python
def safe_divide(a: float, b: float) -> float | None:
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
        return None

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # Error message, returns None
```

---

## Q2. Number input loop

```python
while True:
    raw = input("Enter a number (or 'quit'): ").strip()
    if raw.lower() == "quit":
        print("Exiting.")
        break
    try:
        number = float(raw)
        print(f"You entered: {number}")
    except ValueError:
        print("That's not a valid number. Try again.")
```

---

## Q3. Output prediction

```
ValueError caught
Done
```

- `int("hello")` raises ValueError
- First matching except runs ("ValueError caught")
- `finally` always runs ("Done")
- The `Exception` block is NOT reached (ValueError was caught first)

---

## Q4. Safe file read

```python
import os

def read_file_safe(filename: str) -> str:
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

content = read_file_safe("missing.txt")
print(repr(content))   # ''
```

---

## Q5. Bug: using bare `except`

Bare `except:` catches ALL exceptions including `KeyboardInterrupt` (Ctrl+C) and `SystemExit`. Always specify the exception type:

```python
try:
    result = 10 / 2
except Exception as e:
    print(f"error: {e}")
print(result)
```

The code actually works here (10/2 = 5.0), but the bare except is bad practice.

---

## Q6. to_float with default

```python
def to_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

print(to_float("3.14"))    # 3.14
print(to_float("abc"))     # 0.0
print(to_float(None))      # 0.0
print(to_float("10", 99))  # 10.0
```

---

## Q7. raise vs raise (no args)

```python
raise ValueError("bad input")   # Creates and raises a new ValueError

# Inside an except block:
try:
    int("abc")
except ValueError as e:
    print(f"Logging: {e}")
    raise    # Re-raises the SAME ValueError (with original traceback)
```

`raise` with no args re-raises the current exception unchanged. Useful for logging then re-raising.

---

## Q8. Create file if not found

```python
filename = "data.txt"
try:
    with open(filename, "r") as f:
        content = f.read()
    print(f"Read existing file: {content}")
except FileNotFoundError:
    with open(filename, "w") as f:
        f.write("Created fresh")
    print("File created fresh.")
```

---

## Q9. validate_score

```python
def validate_score(score: float) -> None:
    if not isinstance(score, (int, float)):
        raise TypeError(f"Score must be a number, got {type(score).__name__}")
    if score < 0:
        raise ValueError(f"Score cannot be negative: {score}")
    if score > 100:
        raise ValueError(f"Score cannot exceed 100: {score}")

validate_score(75)     # OK
validate_score(150)    # ValueError
validate_score("A+")   # TypeError
```

---

## Q10. finally — always runs

```python
def write_report(filename: str, data: str) -> bool:
    f = None
    try:
        f = open(filename, "w")
        f.write(data)
        return True
    except PermissionError:
        print("Cannot write to file.")
        return False
    finally:
        if f:
            f.close()   # ALWAYS closes the file, error or not
        print("Cleanup done.")

# without finally, if an error occurs before f.close(), the file stays open
```
