# Lesson 05 — Encapsulation & @property

**Phase:** 07 — OOP | **Time:** ~25 min

---

## Part 1: What is Encapsulation?

Encapsulation means bundling data (attributes) and the methods that operate on them together, and controlling access to the internal state.

**Analogy:** A vending machine. You see the buttons and the output slot. You can't reach inside and take snacks directly. The machine controls all access to its internals.

---

## Part 2: Access Conventions in Python

Python uses naming conventions (not strict enforcement):

```python
class BankAccount:
    def __init__(self):
        self.public_info   = "visible to everyone"   # public
        self._protected    = "convention: internal"  # one underscore
        self.__private     = "name-mangled"          # two underscores

acc = BankAccount()
print(acc.public_info)        # OK
print(acc._protected)          # OK but not recommended
print(acc.__private)           # AttributeError!
print(acc._BankAccount__private)  # works but bad practice
```

---

## Part 3: The @property Decorator

`@property` lets you control attribute access while keeping a clean interface:

```python
class Employee:
    def __init__(self, name: str, salary: float):
        self.name   = name
        self._salary = salary    # store internally

    @property
    def salary(self) -> float:
        """Getter — called when you read emp.salary"""
        return self._salary

    @salary.setter
    def salary(self, amount: float) -> None:
        """Setter — called when you write emp.salary = value"""
        if amount < 0:
            raise ValueError(f"Salary cannot be negative: {amount}")
        if amount > 1_000_000:
            raise ValueError(f"Salary ${amount:,} exceeds maximum")
        self._salary = amount

    @salary.deleter
    def salary(self) -> None:
        """Deleter — called when you do del emp.salary"""
        raise AttributeError("Cannot delete salary")


emp = Employee("Alice", 75000)

# Reads cleanly — no () needed
print(emp.salary)   # 75000

# Uses the setter — validation runs automatically
emp.salary = 80000     # OK
emp.salary = -500      # ValueError!
emp.salary = 5000000   # ValueError!
```

---

## Part 4: Computed Properties

```python
class Rectangle:
    def __init__(self, width: float, height: float):
        self._width  = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value

    # COMPUTED PROPERTIES — derived from other attributes
    @property
    def area(self) -> float:
        return self._width * self._height

    @property
    def perimeter(self) -> float:
        return 2 * (self._width + self._height)

    @property
    def is_square(self) -> bool:
        return self._width == self._height

r = Rectangle(4, 6)
print(r.area)          # 24  (computed, no () needed)
print(r.perimeter)     # 20
print(r.is_square)     # False

r.width = 6
print(r.is_square)     # True
```

---

## Part 5: Full Professional Example

```python
class Product:
    def __init__(self, name: str, price: float, quantity: int):
        self.name      = name
        self._price    = 0.0
        self._quantity = 0
        self.price    = price     # use setter for validation
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be numeric")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = round(float(value), 2)

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity must be integer")
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value

    @property
    def stock_value(self) -> float:
        """Computed: price × quantity."""
        return self._price * self._quantity

    @property
    def in_stock(self) -> bool:
        return self._quantity > 0
```

---

## Practice Exercises

1. Create a `Circle` class with a `radius` property that validates radius > 0, and computed properties `area` and `circumference`.

2. Create a `Temperature` class where celsius is a property that validates >= -273.15, and fahrenheit/kelvin are computed read-only properties.

---

## Next Lesson

**[Lesson 06 → Abstraction](lesson-06-abstraction.md)**
