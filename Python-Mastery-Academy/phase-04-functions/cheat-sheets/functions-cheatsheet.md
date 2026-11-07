# ⚡ Phase 04 Cheat Sheet — Functions

---

## Defining Functions

```python
def function_name(param1: type, param2: type = default) -> return_type:
    """Docstring."""
    return result
```

---

## Parameter Types

```python
def f(pos, /, normal, *, kw_only):   # pos=positional-only, kw_only=keyword-only
    pass

def f(required, optional=default):   # optional has default
    pass

def f(*args):           # any number of positional args → tuple
    pass

def f(**kwargs):        # any number of keyword args → dict
    pass

def f(*args, **kwargs): # both combined
    pass
```

---

## Return Values

```python
return value            # single value
return a, b, c          # multiple values (returns tuple)
a, b = func()           # unpack multiple returns
return None             # explicitly return None
# (no return = returns None)
```

---

## Type Hints

```python
from typing import Optional, Union

def f(x: int) -> str: ...
def f(x: float | None) -> list[str]: ...
def f(x: Optional[int] = None): ...    # Optional = can be None
```

---

## Lambda

```python
fn = lambda x: x ** 2
fn = lambda x, y: x + y
fn = lambda x, y=10: x + y

# Common uses
sorted(items, key=lambda x: x["salary"])
filtered = filter(lambda x: x > 0, nums)
mapped   = map(lambda x: x * 2, nums)
```

---

## Scope (LEGB)

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"   # shadows both

# global keyword (avoid if possible)
def f():
    global x
    x = "modified"

# nonlocal keyword
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
```

---

## Closures

```python
def make_multiplier(n):
    return lambda x: x * n    # n captured from enclosing scope

double = make_multiplier(2)
double(5)   # 10
```

---

## Recursion

```python
def factorial(n):
    if n <= 1:       # base case
        return 1
    return n * factorial(n - 1)   # recursive case

# Always need a base case!
# Python default recursion limit: 1000
```

---

## Mutable Default Trap

```python
# WRONG
def f(items=[]):
    items.append(1)
    return items

# CORRECT
def f(items=None):
    if items is None:
        items = []
    items.append(1)
    return items
```

---

## map / filter / sorted

```python
doubled  = list(map(lambda x: x*2, nums))
evens    = list(filter(lambda x: x%2==0, nums))
ordered  = sorted(records, key=lambda r: r["score"], reverse=True)

# Comprehension alternative (often cleaner)
doubled = [x*2 for x in nums]
evens   = [x for x in nums if x%2==0]
```

---

## Best Practices

```python
# 1. One function = one job
# 2. Functions should be short (< 20 lines ideally)
# 3. Use type hints
# 4. Write docstrings
# 5. Use return values, not global mutations
# 6. Name clearly: get_user, calculate_tax, is_valid
# 7. Test each function independently
```
