# Lesson 04 — Dataclasses

**Phase:** 17 — Advanced Python | **Time:** ~25 min

---

## Part 1: What is a Dataclass?

A dataclass auto-generates `__init__`, `__repr__`, `__eq__` from field annotations. Less boilerplate, more readable.

```python
# Traditional class — lots of boilerplate
class Product:
    def __init__(self, name: str, price: float, qty: int):
        self.name  = name
        self.price = price
        self.qty   = qty
    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price})"
    def __eq__(self, other):
        return (self.name, self.price, self.qty) == (other.name, other.price, other.qty)

# Dataclass — same result, 4 lines instead of 12
from dataclasses import dataclass

@dataclass
class Product:
    name:  str
    price: float
    qty:   int = 0
```

---

## Part 2: Basic Usage

```python
from dataclasses import dataclass, field

@dataclass
class Employee:
    name:       str
    salary:     float
    department: str
    skills:     list[str] = field(default_factory=list)  # mutable default!
    active:     bool = True

# Auto-generated __init__
alice = Employee("Alice", 85000, "Engineering", ["Python", "SQL"])
print(alice)
# Employee(name='Alice', salary=85000, department='Engineering', skills=['Python', 'SQL'], active=True)

# Auto-generated __eq__
e1 = Employee("Bob", 65000, "Sales")
e2 = Employee("Bob", 65000, "Sales")
print(e1 == e2)   # True (compares field by field)
```

---

## Part 3: Field Options

```python
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class Order:
    # Required fields (no default) first
    product_name: str
    quantity:     int

    # Optional fields (with defaults) after
    unit_price:   float = 0.0
    discount_pct: float = 0.0
    tags:         list[str] = field(default_factory=list)

    # Not included in __init__ or __repr__
    internal_id: str = field(default="", repr=False, compare=False)

    # Class variable — not a dataclass field
    TAX_RATE: ClassVar[float] = 0.08

    def total(self) -> float:
        subtotal = self.quantity * self.unit_price
        discount = subtotal * self.discount_pct
        tax      = (subtotal - discount) * self.TAX_RATE
        return round(subtotal - discount + tax, 2)
```

---

## Part 4: post_init

```python
from dataclasses import dataclass

@dataclass
class Circle:
    radius: float

    def __post_init__(self):
        # Called after __init__
        if self.radius <= 0:
            raise ValueError(f"Radius must be positive: {self.radius}")

    @property
    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

c = Circle(5.0)
print(c.area)     # 78.54

try:
    Circle(-1)    # ValueError
except ValueError as e:
    print(e)
```

---

## Part 5: frozen, order, slots

```python
from dataclasses import dataclass

# Immutable dataclass (like a named tuple)
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 5.0  → FrozenInstanceError!

# Can be used as dict key or in sets
points = {Point(0, 0), Point(1, 1)}

# Enable comparison operators (< > <= >=)
@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int

v1 = Version(1, 2, 0)
v2 = Version(2, 0, 0)
print(v1 < v2)    # True
print(sorted([v2, v1]))  # [Version(1,2,0), Version(2,0,0)]
```

---

## Part 6: vs NamedTuple vs dict

| | dict | NamedTuple | dataclass |
|--|------|-----------|----------|
| Access | `d["key"]` | `t.field` | `obj.field` |
| Mutable | Yes | No | Yes (default) |
| Type hints | Optional | Yes | Yes |
| Methods | No | Limited | Yes |
| Default values | Any | No | Yes |
| JSON compatible | Yes | Close | With asdict() |

```python
from dataclasses import asdict, astuple

@dataclass
class Config:
    host: str = "localhost"
    port: int = 5432

c = Config()
print(asdict(c))   # {'host': 'localhost', 'port': 5432}
```

---

## Practice Exercises

1. Create an `Address` dataclass with street, city, country, postal_code.

2. Create an `Invoice` dataclass with items (list of product dicts), tax_rate, and a `total()` method.

3. When would you choose a frozen dataclass?

---

## Next Lesson

**[Lesson 05 → Async/Await](lesson-05-async.md)**
