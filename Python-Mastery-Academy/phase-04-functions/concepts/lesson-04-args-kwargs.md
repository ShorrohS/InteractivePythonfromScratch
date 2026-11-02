# Lesson 04 — *args and **kwargs

**Phase:** 04 — Functions | **Time:** ~30 min

---

## Part 1: The Problem

What if you don't know how many arguments a function will receive?

```python
# This only works for exactly 2 numbers:
def add(a, b):
    return a + b

# What about 3 numbers? 10 numbers? 100 numbers?
```

---

## Part 2: *args — Variable Positional Arguments

`*args` collects any number of positional arguments into a **tuple**:

```python
def add(*numbers: float) -> float:
    """Add any number of values."""
    return sum(numbers)

print(add(1, 2))              # 3
print(add(1, 2, 3))           # 6
print(add(1, 2, 3, 4, 5))    # 15
print(add())                  # 0

# numbers is a tuple inside the function
def show_args(*args):
    print(type(args))    # <class 'tuple'>
    for i, arg in enumerate(args):
        print(f"  arg[{i}] = {arg}")

show_args("Alice", 30, True, 75000)
```

---

## Part 3: **kwargs — Variable Keyword Arguments

`**kwargs` collects any number of keyword arguments into a **dict**:

```python
def create_profile(**info) -> dict:
    """Create a profile from any keyword arguments."""
    return info

alice = create_profile(name="Alice", age=30, city="NYC", salary=75000)
print(alice)
# {'name': 'Alice', 'age': 30, 'city': 'NYC', 'salary': 75000}

def display_record(**kwargs) -> None:
    print("─" * 30)
    for key, value in kwargs.items():
        print(f"  {key.title():<15} {value}")
    print("─" * 30)

display_record(name="Bob", department="Sales", years=3)
```

---

## Part 4: Combining All Parameter Types

Order matters: `normal → *args → keyword-only → **kwargs`

```python
def full_report(title: str, *items: str, separator: str = "-", **metadata) -> None:
    """
    title: required positional
    *items: any number of items
    separator: keyword-only argument
    **metadata: any keyword arguments
    """
    width = 50
    print("=" * width)
    print(f"  {title.upper()}")
    print(separator * width)
    
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item}")
    
    if metadata:
        print(separator * width)
        for k, v in metadata.items():
            print(f"  {k}: {v}")
    print("=" * width)

full_report(
    "Quarterly Report",
    "Revenue up 15%",
    "New clients: 23",
    "Churn rate: 2.1%",
    separator="─",
    quarter="Q3 2024",
    author="Analytics Team"
)
```

---

## Part 5: Unpacking with * and **

```python
# Unpack list/tuple into positional args
def add(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
print(add(*numbers))    # 6  (unpacks list)

# Unpack dict into keyword args
def greet(first, last, title="Mr."):
    return f"{title} {first} {last}"

person = {"first": "Alice", "last": "Johnson", "title": "Dr."}
print(greet(**person))    # Dr. Alice Johnson
```

---

## Practice Exercises

1. Write `max_of_any(*numbers)` that returns the largest number from any count of inputs.

2. Write `build_sentence(*words, separator=" ")` that joins words with a separator.

3. Write `format_table(**columns)` that prints a simple table where keys are headers.

4. Write a function that accepts both positional (names) and keyword (scores) to build a student dictionary.

---

## Next Lesson

**[Lesson 05 → Scope](lesson-05-scope.md)**
