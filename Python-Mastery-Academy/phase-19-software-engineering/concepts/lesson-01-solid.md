# Lesson 01 — SOLID Principles

**Phase:** 19 — Software Engineering | **Time:** ~45 min

---

## What is SOLID?

SOLID is five design principles that make code easier to maintain, extend, and test. Every professional developer is expected to know these.

```
S — Single Responsibility Principle
O — Open/Closed Principle
L — Liskov Substitution Principle
I — Interface Segregation Principle
D — Dependency Inversion Principle
```

---

## S — Single Responsibility Principle

**"A class should have only ONE reason to change."**

```python
# BAD — one class doing three jobs
class Employee:
    def __init__(self, name, salary):
        self.name   = name
        self.salary = salary

    def calculate_tax(self) -> float:
        return self.salary * 0.20       # payroll logic

    def save_to_database(self) -> None:
        # db.execute("INSERT ...")      # database logic
        pass

    def generate_report(self) -> str:
        return f"{self.name}: ${self.salary}"  # reporting logic

# GOOD — each class has one job
class Employee:
    def __init__(self, name: str, salary: float):
        self.name   = name
        self.salary = salary

class PayrollCalculator:
    @staticmethod
    def calculate_tax(employee: Employee) -> float:
        return employee.salary * 0.20

class EmployeeRepository:
    def save(self, employee: Employee) -> None:
        pass   # database logic here

class EmployeeReporter:
    def generate(self, employee: Employee) -> str:
        return f"{employee.name}: ${employee.salary}"
```

---

## O — Open/Closed Principle

**"Open for extension, closed for modification."**

Add new features without changing existing, tested code.

```python
# BAD — must modify class to add new payment type
class PaymentProcessor:
    def process(self, payment_type: str, amount: float) -> bool:
        if payment_type == "stripe":
            return self._charge_stripe(amount)
        elif payment_type == "paypal":
            return self._charge_paypal(amount)
        # To add a new type: must modify this class

# GOOD — add new types without touching existing code
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool:
        pass

class StripeGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        print(f"  Stripe: charging ${amount}")
        return True

class PayPalGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        print(f"  PayPal: charging ${amount}")
        return True

# NEW payment type — no modification to existing code!
class CryptoGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        print(f"  Crypto: charging ${amount}")
        return True

class OrderProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def checkout(self, amount: float) -> bool:
        return self.gateway.charge(amount)

# Usage
processor = OrderProcessor(StripeGateway())
processor.checkout(99.99)
```

---

## L — Liskov Substitution Principle

**"A child class must be substitutable for its parent class."**

```python
# BAD — Square breaks Rectangle
class Rectangle:
    def __init__(self, width: float, height: float):
        self.width  = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side: float):
        super().__init__(side, side)

    @Rectangle.width.setter   # overrides setter
    def width(self, value: float) -> None:
        self._width  = value
        self._height = value   # BUG: breaks Rectangle behaviour

# Code that works with Rectangle breaks with Square
def resize_and_area(r: Rectangle) -> float:
    r.width  = 5
    r.height = 10
    return r.area()   # Rectangle: 50, Square: 100 (wrong!)

# GOOD — don't inherit when it violates LSP
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: pass

class Rectangle(Shape):
    def __init__(self, w, h): ...

class Square(Shape):
    def __init__(self, s): ...
```

---

## I — Interface Segregation Principle

**"Don't force classes to implement methods they don't use."**

```python
# BAD — one fat interface
class Printer(ABC):
    @abstractmethod
    def print(self): pass
    @abstractmethod
    def scan(self): pass
    @abstractmethod
    def fax(self): pass

class SimplePrinter(Printer):
    def print(self): pass
    def scan(self): raise NotImplementedError  # forced to implement!
    def fax(self):  raise NotImplementedError  # forced to implement!

# GOOD — segregated interfaces
class Printable(ABC):
    @abstractmethod
    def print(self): pass

class Scannable(ABC):
    @abstractmethod
    def scan(self): pass

class FaxCapable(ABC):
    @abstractmethod
    def fax(self): pass

class SimplePrinter(Printable):
    def print(self): pass     # only what it needs

class AllInOnePrinter(Printable, Scannable, FaxCapable):
    def print(self): pass
    def scan(self): pass
    def fax(self): pass
```

---

## D — Dependency Inversion Principle

**"Depend on abstractions, not implementations."**

```python
# BAD — high-level module depends on low-level detail
class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()  # tightly coupled!

    def save_order(self, order):
        self.db.insert("orders", order)

# GOOD — depend on abstraction
class Database(ABC):
    @abstractmethod
    def insert(self, table: str, data: dict) -> int: pass

class MySQLDatabase(Database):
    def insert(self, table, data): ...

class SQLiteDatabase(Database):
    def insert(self, table, data): ...

class OrderService:
    def __init__(self, db: Database):  # injected!
        self.db = db

    def save_order(self, order: dict) -> int:
        return self.db.insert("orders", order)

# Can swap databases without changing OrderService
dev_service  = OrderService(SQLiteDatabase())
prod_service = OrderService(MySQLDatabase())
test_service = OrderService(MockDatabase())   # for tests!
```

---

## SOLID Summary

| Principle | One-liner |
|-----------|-----------|
| **S** — Single Responsibility | One class = one job |
| **O** — Open/Closed | Extend without modifying |
| **L** — Liskov | Child works wherever parent works |
| **I** — Interface Segregation | Small, focused interfaces |
| **D** — Dependency Inversion | Depend on abstractions |

---

## Interview Questions

1. Explain each SOLID principle with a Python example.
2. How does SOLID reduce bugs in large codebases?
3. What is Dependency Injection and how does it relate to DIP?
4. When might you intentionally violate a SOLID principle?
