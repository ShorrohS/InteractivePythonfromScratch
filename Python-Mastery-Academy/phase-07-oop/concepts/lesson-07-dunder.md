# Lesson 07 — Dunder (Magic) Methods

**Phase:** 07 — OOP | **Time:** ~30 min

---

## Part 1: What are Dunder Methods?

Dunder methods (double underscore = `__method__`) let your objects work with Python's built-in syntax. They're "magic" because Python calls them automatically.

---

## Part 2: String Representation

```python
class Product:
    def __init__(self, name: str, price: float, qty: int):
        self.name  = name
        self.price = price
        self.qty   = qty

    def __str__(self) -> str:
        """Called by print() and str() — user-facing."""
        return f"{self.name}: ${self.price:.2f} (x{self.qty})"

    def __repr__(self) -> str:
        """Called by repr() — developer-facing, should be unambiguous."""
        return f"Product(name={self.name!r}, price={self.price}, qty={self.qty})"

p = Product("Laptop", 999.99, 5)

print(p)      # Laptop: $999.99 (x5)    ← uses __str__
print(repr(p)) # Product(name='Laptop', ...)   ← uses __repr__
```

---

## Part 3: Comparison Operators

```python
from functools import total_ordering

@total_ordering   # auto-generates <=, >=, > from just == and <
class Employee:
    def __init__(self, name: str, salary: float):
        self.name   = name
        self.salary = salary

    def __eq__(self, other) -> bool:
        if not isinstance(other, Employee):
            return NotImplemented
        return self.salary == other.salary

    def __lt__(self, other) -> bool:
        if not isinstance(other, Employee):
            return NotImplemented
        return self.salary < other.salary

alice = Employee("Alice", 85000)
bob   = Employee("Bob",   70000)

print(alice == bob)    # False
print(alice > bob)     # True   (from @total_ordering)
print(alice < bob)     # False

employees = [alice, bob, Employee("Carol", 95000)]
print(sorted(employees, key=lambda e: e.salary))
```

---

## Part 4: Arithmetic Operators

```python
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        import math
        return math.sqrt(self.x**2 + self.y**2)

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)    # Vector(4, 6)
print(v1 - v2)    # Vector(-2, -2)
print(v1 * 3)     # Vector(3, 6)
print(abs(v2))    # 5.0
```

---

## Part 5: Container Protocol

```python
class Playlist:
    def __init__(self, name: str):
        self.name  = name
        self._songs = []

    def add(self, song: str) -> None:
        self._songs.append(song)

    def __len__(self) -> int:
        return len(self._songs)

    def __getitem__(self, index) -> str:
        return self._songs[index]

    def __contains__(self, song: str) -> bool:
        return song in self._songs

    def __iter__(self):
        return iter(self._songs)

    def __str__(self) -> str:
        return f"Playlist({self.name!r}, {len(self)} songs)"

p = Playlist("Favourites")
p.add("Bohemian Rhapsody")
p.add("Hotel California")
p.add("Stairway to Heaven")

print(len(p))                             # 3
print(p[0])                               # Bohemian Rhapsody
print("Hotel California" in p)           # True
for song in p:                            # iteration works
    print(f"  - {song}")
print(p)                                  # Playlist('Favourites', 3 songs)
```

---

## Part 6: Context Manager Protocol

```python
class Timer:
    import time as _time

    def __enter__(self):
        self._start = Timer._time.perf_counter()
        return self    # bound to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = Timer._time.perf_counter() - self._start
        print(f"  Time: {elapsed:.4f}s")
        return False   # don't suppress exceptions

with Timer() as t:
    total = sum(range(1_000_000))
print(f"Sum: {total:,}")
```

---

## Key Dunder Methods Reference

| Method | Triggered by |
|--------|-------------|
| `__init__` | `ClassName()` |
| `__str__` | `print(obj)`, `str(obj)` |
| `__repr__` | `repr(obj)`, REPL display |
| `__len__` | `len(obj)` |
| `__getitem__` | `obj[key]` |
| `__setitem__` | `obj[key] = val` |
| `__contains__` | `item in obj` |
| `__iter__` | `for x in obj` |
| `__eq__` | `obj1 == obj2` |
| `__lt__` | `obj1 < obj2` |
| `__add__` | `obj1 + obj2` |
| `__enter__` | `with obj as x:` |
| `__exit__` | end of `with` block |
| `__call__` | `obj()` |

---

## Practice Exercises

1. Write a `ShoppingCart` class with `__len__`, `__iter__`, `__contains__`, and `__str__`.

2. Write a `Money(amount, currency)` class with `__add__`, `__sub__`, `__eq__`, `__str__`.

3. Write a `DatabaseConnection` class with `__enter__` and `__exit__` for use as a context manager.
