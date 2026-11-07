# Lesson 06 — Abstraction & Abstract Classes

**Phase:** 07 — OOP | **Time:** ~20 min

---

## Part 1: What is Abstraction?

Abstraction means hiding implementation complexity and showing only what's necessary.

**Analogy:** When you drive a car, you use the steering wheel, accelerator, and brakes. You don't need to know how the engine, transmission, or fuel injection works. The interface is simple; the implementation is hidden.

---

## Part 2: Abstract Base Classes (ABC)

An abstract class defines a template that subclasses MUST follow:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class — cannot be instantiated directly."""

    @abstractmethod
    def area(self) -> float:
        """Every concrete Shape must implement area()."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Every concrete Shape must implement perimeter()."""
        pass

    # CONCRETE method — shared implementation all subclasses use
    def describe(self) -> str:
        return (
            f"{self.__class__.__name__}: "
            f"area={self.area():.2f}, "
            f"perimeter={self.perimeter():.2f}"
        )

# Shape() raises TypeError — can't instantiate abstract class
```

---

## Part 3: Implementing Abstract Classes

```python
import math

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Square(Shape):
    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return self.side ** 2

    def perimeter(self) -> float:
        return 4 * self.side


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        s = self.perimeter() / 2
        return math.sqrt(s * (s-self.a) * (s-self.b) * (s-self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c


shapes = [Circle(5), Square(4), Triangle(3, 4, 5)]
for s in shapes:
    print(s.describe())
```

---

## Part 4: Abstract Properties

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def max_speed(self) -> float:
        """Maximum speed in km/h."""
        pass

    @property
    @abstractmethod
    def fuel_type(self) -> str:
        pass

    @abstractmethod
    def start(self) -> str:
        pass

    def info(self) -> str:
        return f"{self.__class__.__name__}: max {self.max_speed}km/h, {self.fuel_type}"


class ElectricCar(Vehicle):
    @property
    def max_speed(self) -> float:
        return 250.0

    @property
    def fuel_type(self) -> str:
        return "Electric"

    def start(self) -> str:
        return "Silent start..."


class DieselTruck(Vehicle):
    @property
    def max_speed(self) -> float:
        return 120.0

    @property
    def fuel_type(self) -> str:
        return "Diesel"

    def start(self) -> str:
        return "VROOM..."
```

---

## Part 5: When to Use ABC

```
Use ABC when:
  - You have a family of related classes
  - All must implement a specific interface
  - You want Python to enforce this at class creation time
  - You want to write code that works with ANY implementation

Don't use ABC when:
  - A simple base class with NotImplementedError is enough
  - You have only one concrete implementation
  - Simple duck typing would work
```

---

## Practice Exercises

1. Create a `DataSource(ABC)` with abstract methods `connect()`, `read()`, `close()`. Implement `CSVDataSource` and `JSONDataSource`.

2. Create a `Report(ABC)` with abstract `generate()` and `export(format)`. Implement `SalesReport` and `InventoryReport`.

---

## Next Lesson

**[Lesson 07 → Dunder Methods](lesson-07-dunder.md)**
