# Lesson 01 — try / except

**Phase:** 06 — Error Handling | **Time:** ~30 min

---

## Part 1: What are Exceptions?

An exception is an error that occurs while the program is running. Without handling, it crashes your program.

```python
# This crashes:
age = int("abc")    # ValueError: invalid literal for int()
print(age)          # Never reaches here
```

```python
# This handles it gracefully:
try:
    age = int("abc")
except ValueError:
    print("Please enter a valid number.")
    age = 0
print(f"Age: {age}")   # Continues running
```

---

## Part 2: Basic try/except

```python
try:
    # Try this code
    result = 10 / 0
except ZeroDivisionError:
    # If ZeroDivisionError occurs, run this
    print("Cannot divide by zero!")
    result = 0

print(f"Result: {result}")
```

---

## Part 3: Catching Multiple Exceptions

```python
def safe_divide(a: float, b: float) -> float | None:
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None
    except TypeError:
        print("Error: Both arguments must be numbers")
        return None

# Multiple exceptions in one line (same handling)
def parse_number(text: str) -> int | None:
    try:
        return int(text)
    except (ValueError, TypeError):
        return None

# Access the exception message
try:
    x = int("hello")
except ValueError as e:
    print(f"Caught: {e}")    # invalid literal for int() with base 10: 'hello'
```

---

## Part 4: try / except / else / finally

```python
def read_file(filename: str) -> str | None:
    try:
        with open(filename, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except PermissionError:
        print(f"Permission denied reading '{filename}'.")
        return None
    else:
        # Runs ONLY if no exception occurred
        print(f"Successfully read {len(content)} characters.")
        return content
    finally:
        # ALWAYS runs, exception or not
        print("File operation complete.")

result = read_file("data.txt")
```

---

## Part 5: Input Validation Pattern

```python
def get_integer(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Get a validated integer from user."""
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  Must be at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"  Must be at most {max_val}.")
                continue
            return value
        except ValueError:
            print("  Invalid input. Please enter a whole number.")

age = get_integer("Enter age: ", min_val=0, max_val=120)
score = get_integer("Enter score (0-100): ", min_val=0, max_val=100)
```

---

## Part 6: Business Example — Safe Data Import

```python
"""Process a list of employee data with error handling."""

raw_data = [
    ("Alice", "75000", "Engineering"),
    ("Bob", "abc", "Sales"),        # Invalid salary
    ("Carol", "90000", ""),          # Empty department
    ("Dave", "-5000", "Marketing"),  # Negative salary
    ("Eve", "85000", "Finance"),
]

processed = []
errors = []

for name, salary_str, dept in raw_data:
    try:
        salary = float(salary_str)
        if salary <= 0:
            raise ValueError(f"Salary must be positive (got {salary})")
        if not dept:
            raise ValueError("Department cannot be empty")
        processed.append({"name": name, "salary": salary, "dept": dept})
    except ValueError as e:
        errors.append({"name": name, "error": str(e)})

print(f"✅ Processed: {len(processed)} records")
print(f"❌ Errors: {len(errors)} records")
print()

for record in processed:
    print(f"  ✅ {record['name']:<10} ${record['salary']:,.0f}  {record['dept']}")
for error in errors:
    print(f"  ❌ {error['name']:<10} ERROR: {error['error']}")
```

---

## Part 7: Common Mistakes

```python
# Mistake 1: Bare except (catches EVERYTHING including KeyboardInterrupt)
try:
    risky_code()
except:               # NEVER do this
    pass

# CORRECT: always specify the exception type
try:
    risky_code()
except ValueError:
    handle_value_error()
except Exception as e:
    handle_general_error(e)

# Mistake 2: Silently swallowing exceptions
try:
    result = int(input("Number: "))
except ValueError:
    pass    # User will never know what happened!

# CORRECT: at minimum, inform the user
except ValueError:
    print("Invalid input. Using default value 0.")
    result = 0

# Mistake 3: Too broad handling
try:
    data = load_data()
    process(data)
    save(data)
except Exception:
    print("Something failed")    # Which of the 3 operations? No idea!

# CORRECT: handle at the appropriate granularity
try:
    data = load_data()
except FileNotFoundError:
    print("Data file not found.")
    return
# ... etc.
```

---

## Practice Exercises

1. Write a safe number converter: `safe_int(text)` that returns an int or None.

2. Create a file reader that handles FileNotFoundError gracefully.

3. Write a safe division function that handles ZeroDivisionError and TypeError.

4. Create a robust input loop: keep asking for a positive number until the user provides one.

5. What is wrong?
   ```python
   try:
       result = 10 / x
   except:
       print("error")
   ```

---

## Next Lesson

**[Lesson 04 → raise and Custom Exceptions](lesson-04-raise.md)**
