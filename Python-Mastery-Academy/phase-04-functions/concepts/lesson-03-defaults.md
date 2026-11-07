# Lesson 03 — Default Arguments

**Phase:** 04 — Functions | **Time:** ~20 min

---

## Part 1: What are Default Arguments?

Default arguments let you define a parameter that has a value if the caller doesn't supply one.

```python
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

print(greet("Alice"))              # Hello, Alice!
print(greet("Bob", "Good morning"))# Good morning, Bob!
print(greet("Carol", "Hi"))        # Hi, Carol!
```

---

## Part 2: Rules

```python
# Rule: default parameters MUST come after non-default ones

def connect(host: str, port: int = 5432, ssl: bool = True):  # CORRECT
    pass

def connect(host: str = "localhost", port: int):  # SyntaxError!
    pass
```

---

## Part 3: Practical Examples

```python
def format_currency(amount: float,
                    symbol: str = "$",
                    decimals: int = 2,
                    thousands: bool = True) -> str:
    """Format a number as currency."""
    if thousands:
        return f"{symbol}{amount:,.{decimals}f}"
    else:
        return f"{symbol}{amount:.{decimals}f}"

print(format_currency(1234567.89))              # $1,234,567.89
print(format_currency(1234.5, symbol="€"))      # €1,234.50
print(format_currency(9999.99, decimals=0))     # $10,000
print(format_currency(500, thousands=False))    # $500.00


def send_email(to: str, subject: str, body: str,
               cc: str = "",
               priority: str = "normal",
               html: bool = False) -> dict:
    """Simulate sending an email."""
    return {
        "to": to, "subject": subject,
        "body": body, "cc": cc,
        "priority": priority, "html": html
    }

# Most common usage — minimal args
email1 = send_email("alice@example.com", "Hello", "Hi Alice!")

# Override specific defaults
email2 = send_email(
    "bob@example.com",
    "URGENT: Meeting",
    "Please join immediately.",
    priority="high"
)
```

---

## Part 4: The Mutable Default Trap (Important!)

```python
# NEVER use a mutable value as a default
def add_tag(item: str, tags: list = []) -> list:  # DANGEROUS
    tags.append(item)
    return tags

print(add_tag("python"))    # ['python']
print(add_tag("flask"))     # ['python', 'flask']  ← WRONG!

# The list is created ONCE at function definition time
# Every call shares the same list object

# ALWAYS use None as the sentinel
def add_tag(item: str, tags: list = None) -> list:   # CORRECT
    if tags is None:
        tags = []    # fresh list each call
    tags.append(item)
    return tags

print(add_tag("python"))    # ['python']
print(add_tag("flask"))     # ['flask']  ← correct
```

---

## Practice Exercises

1. Write a `create_report(title, author="Anonymous", format="PDF", include_summary=True)` function.

2. Write a `repeat_string(text, times=2, separator=" ")` function.

3. What prints?
   ```python
   def f(x, y=10, z=20):
       return x + y + z
   print(f(1))
   print(f(1, 2))
   print(f(1, z=5))
   ```

---

## Next Lesson

**[Lesson 04 → *args and **kwargs](lesson-04-args-kwargs.md)**
