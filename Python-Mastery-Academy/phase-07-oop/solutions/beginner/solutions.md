# Phase 07 — Beginner Solutions: OOP

---

## Q1. Dog class

```python
class Dog:
    def __init__(self, name: str, breed: str):
        self.name  = name
        self.breed = breed

    def bark(self) -> str:
        return f"{self.name} says: Woof!"

d1 = Dog("Buddy", "Labrador")
d2 = Dog("Max",   "Poodle")

print(d1.bark())   # Buddy says: Woof!
print(d2.bark())   # Max says: Woof!
```

---

## Q2. Rectangle class

```python
class Rectangle:
    def __init__(self, width: float, height: float):
        self.width  = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def is_square(self) -> bool:
        return self.width == self.height

r1 = Rectangle(4, 6)
r2 = Rectangle(5, 5)

print(r1.area())       # 24
print(r1.perimeter())  # 20
print(r1.is_square())  # False
print(r2.is_square())  # True
```

---

## Q3. Predict output

```
3
```

`c.increment()` is called three times, each time adding 1 to `self.count`. Starting at 0, the final value is 3.

---

## Q4. Student class

```python
class Student:
    def __init__(self, name: str):
        self.name   = name
        self.grades = []

    def add_grade(self, score: float) -> None:
        self.grades.append(score)

    def average(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def highest(self) -> float:
        return max(self.grades) if self.grades else 0.0

    def lowest(self) -> float:
        return min(self.grades) if self.grades else 0.0

s = Student("Alice")
for score in [88, 92, 75, 95, 83]:
    s.add_grade(score)

print(f"Average: {s.average():.1f}")   # 86.6
print(f"Highest: {s.highest()}")       # 95
print(f"Lowest:  {s.lowest()}")        # 75
```

---

## Q5. Fix the code

The bug is that `__init__` is missing `self` as the first parameter, and assignments use the parameter names directly instead of `self.`:

```python
# Original (broken)
class Car:
    def __init__(name, speed):   # ← missing 'self'
        name = name              # ← assigns local variable, not attribute
        speed = speed

# Fixed
class Car:
    def __init__(self, name: str, speed: int):
        self.name  = name    # ← stores on the instance
        self.speed = speed

c = Car("Tesla", 150)
print(c.name, c.speed)   # Tesla 150
```

---

## Q6. Circle class

```python
import math

class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def circumference(self) -> float:
        return 2 * math.pi * self.radius

c = Circle(5)
print(f"Area:          {c.area():.2f}")           # 78.54
print(f"Circumference: {c.circumference():.2f}")  # 31.42
```

---

## Q7. BankAccount class

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner   = owner
        self._balance = max(0.0, float(balance))

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self._balance += amount
        print(f"Deposited ${amount:.2f}. Balance: ${self._balance:.2f}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self._balance:
            print(f"Insufficient funds. Balance: ${self._balance:.2f}")
            return
        self._balance -= amount
        print(f"Withdrew ${amount:.2f}. Balance: ${self._balance:.2f}")

    def get_balance(self) -> float:
        return self._balance

acc = BankAccount("Alice", 1000)
acc.deposit(500)
acc.withdraw(200)
acc.withdraw(2000)    # insufficient
print(f"Balance: ${acc.get_balance():.2f}")
```

---

## Q8. Adding __str__ to BankAccount

`__str__` is called when you pass an object to `print()`, `str()`, or an f-string. It should return a human-readable string that describes the object.

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner    = owner
        self._balance = float(balance)

    def __str__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance=${self._balance:,.2f})"

    # ... deposit/withdraw/get_balance from Q7 ...

acc = BankAccount("Alice", 1250.00)
print(acc)   # BankAccount(owner='Alice', balance=$1,250.00)
```

---

## Q9. Product and Cart classes

```python
class Product:
    def __init__(self, name: str, price: float):
        self.name  = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.name} (${self.price:.2f})"

    def __repr__(self) -> str:
        return f"Product({self.name!r}, {self.price})"


class Cart:
    def __init__(self):
        self.products = []

    def add(self, product: Product) -> None:
        self.products.append(product)

    def total(self) -> float:
        return sum(p.price for p in self.products)

    def count(self) -> int:
        return len(self.products)

    def __str__(self) -> str:
        lines = [f"  {p}" for p in self.products]
        lines.append(f"  Total: ${self.total():.2f}")
        return "\n".join(lines)


cart = Cart()
cart.add(Product("Laptop", 999.99))
cart.add(Product("Mouse",   29.99))
cart.add(Product("Keyboard", 79.99))

print(f"Items: {cart.count()}")
print(cart)
```

---

## Q10. @property and encapsulation

`@property` is the key mechanism Python uses to implement **encapsulation**: the OOP principle of hiding internal state and only exposing it through a controlled interface.

Without `@property`, you either expose a raw attribute (anyone can change it to anything) or write verbose `get_x()`/`set_x()` methods. `@property` gives you the clean attribute syntax AND the ability to validate, compute, or restrict access.

```python
class Circle:
    def __init__(self, radius: float):
        self._radius = 0.0
        self.radius  = radius     # runs the setter

    @property
    def radius(self) -> float:
        return self._radius       # getter

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = float(value)

    @property
    def area(self) -> float:
        import math
        return math.pi * self._radius ** 2   # read-only computed property

c = Circle(5)
print(c.area)       # 78.54...
c.radius = 10       # setter validates
print(c.area)       # 314.15...

try:
    c.radius = -1   # raises ValueError
except ValueError as e:
    print(e)
```

`@property` supports encapsulation by letting you: guard state behind validation logic, expose computed values without storing them, and make attributes read-only (no setter defined).
