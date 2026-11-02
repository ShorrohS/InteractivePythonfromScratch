# Lesson 01 — Decorators

**Phase:** 17 — Advanced Python | **Time:** ~45 min

---

## Part 1: What is a Decorator?

A decorator is a function that wraps another function to add behavior without modifying the original function.

**Analogy:** A decorator is like a gift wrapper. The gift (function) stays the same inside. The wrapper adds presentation without changing the gift.

```
Original function → Decorator wraps it → Enhanced function
```

---

## Part 2: Functions are Objects

To understand decorators, you first need to know that functions are first-class objects in Python:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Functions can be assigned to variables
say_hello = greet
print(say_hello("Alice"))   # Hello, Alice!

# Functions can be passed as arguments
def run_twice(func, name):
    print(func(name))
    print(func(name))

run_twice(greet, "Bob")

# Functions can be returned from functions
def get_greeter():
    def inner(name):
        return f"Hi there, {name}!"
    return inner

greeter = get_greeter()
print(greeter("Carol"))
```

---

## Part 3: Your First Decorator

```python
from functools import wraps

def uppercase_result(func):
    """Decorator that converts function's return value to uppercase."""
    
    @wraps(func)   # Preserves original function's metadata
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)    # Call original function
        return result.upper()             # Modify result
    
    return wrapper

# APPLY with @ syntax
@uppercase_result
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Alice"))    # HELLO, ALICE!

# Without @ — equivalent manually:
# greet = uppercase_result(greet)
```

---

## Part 4: Practical Decorators

### Timer Decorator

```python
import time
from functools import wraps

def timer(func):
    """Measures how long a function takes to run."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱️  {func.__name__}() took {elapsed:.4f} seconds")
        return result
    return wrapper

@timer
def calculate_primes(n: int) -> list:
    """Find all primes up to n."""
    return [i for i in range(2, n) if all(i % j != 0 for j in range(2, i))]

primes = calculate_primes(1000)
print(f"Found {len(primes)} primes")
```

### Logger Decorator

```python
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)

def log_calls(func):
    """Logs every function call with arguments."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ", ".join([repr(a) for a in args])
        kwargs_str = ", ".join([f"{k}={v!r}" for k, v in kwargs.items()])
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        logging.info(f"Calling {func.__name__}({all_args})")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

@log_calls
def add(a: int, b: int) -> int:
    return a + b

add(3, 5)
# INFO: Calling add(3, 5)
# INFO: add returned 8
```

### Retry Decorator

```python
import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0, exceptions=(Exception,)):
    """Retry a function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    print(f"  Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError,))
def fetch_data(url: str) -> str:
    # Simulates an unreliable network call
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network timeout")
    return f"Data from {url}"
```

### Validate Arguments Decorator

```python
def require_positive(*arg_names):
    """Raise ValueError if any specified argument is not positive."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            for name in arg_names:
                if name in bound.arguments:
                    val = bound.arguments[name]
                    if val <= 0:
                        raise ValueError(f"Argument '{name}' must be positive, got {val}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_positive("amount", "rate")
def calculate_interest(amount: float, rate: float, years: int) -> float:
    return amount * rate * years

calculate_interest(1000, 0.05, 3)     # Works
calculate_interest(-100, 0.05, 3)     # ValueError: 'amount' must be positive
```

---

## Part 5: Stacking Decorators

```python
@timer
@log_calls
def complex_operation(data: list) -> int:
    return sum(data)

# Execution order: timer wraps (log_calls wraps (complex_operation))
# Runs: timer → log_calls → complex_operation → log_calls result → timer result
```

---

## Part 6: Class Decorators (Built-in)

```python
class Temperature:
    def __init__(self):
        self._celsius = 0
    
    @property
    def celsius(self) -> float:
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32
    
    @staticmethod
    def convert_to_kelvin(celsius: float) -> float:
        return celsius + 273.15
    
    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> "Temperature":
        temp = cls()
        temp.celsius = (fahrenheit - 32) * 5/9
        return temp

t = Temperature()
t.celsius = 25
print(t.fahrenheit)    # 77.0

t2 = Temperature.from_fahrenheit(98.6)
print(t2.celsius)      # ~37.0
```

---

## Practice Exercises

1. Write a `deprecated` decorator that prints a warning when the function is called.

2. Write a `memoize` decorator that caches function results (memoization).

3. Write a `rate_limit(calls_per_second)` decorator.

4. Write a `validate_types` decorator that checks argument types match type hints.

---

## Next Lesson

**[Lesson 02 → Generators](lesson-02-generators.md)**
