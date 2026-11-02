# ⚡ OOP Cheat Sheet — Phase 07

---

## Class Structure

```python
class ClassName:
    """Docstring."""
    
    class_attribute = "shared by all"    # Class attribute
    
    def __init__(self, name: str):       # Constructor
        self.name = name                 # Instance attribute
        self._private = "convention"     # "Private" (by convention)
        self.__mangled = "name mangled"  # Name mangling
    
    def instance_method(self):           # Instance method
        return self.name
    
    @classmethod
    def class_method(cls):               # Class method
        return cls.class_attribute
    
    @staticmethod
    def static_method():                 # Static method
        return "no self or cls needed"
    
    @property
    def value(self):                     # Property getter
        return self._value
    
    @value.setter
    def value(self, new_val):            # Property setter
        self._value = new_val
    
    def __str__(self):                   # print() representation
        return f"ClassName({self.name})"
    
    def __repr__(self):                  # Developer representation
        return f"ClassName(name={self.name!r})"
    
    def __len__(self):                   # len() support
        return 0
    
    def __eq__(self, other):             # == support
        return self.name == other.name
```

---

## Inheritance

```python
class Parent:
    def __init__(self, x):
        self.x = x
    def method(self):
        return f"Parent: {self.x}"

class Child(Parent):
    def __init__(self, x, y):
        super().__init__(x)      # Call parent __init__
        self.y = y
    
    def method(self):            # Override parent method
        parent_result = super().method()   # Call parent method
        return f"{parent_result}, Child: {self.y}"

# Check inheritance
isinstance(Child(1, 2), Child)    # True
isinstance(Child(1, 2), Parent)   # True
issubclass(Child, Parent)         # True
```

---

## Encapsulation

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance    # Convention: don't access directly
    
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount

acc = BankAccount(100)
print(acc.balance)        # 100  (via property)
acc.balance = 200         # Uses setter
acc._balance = -50        # Possible but violates convention
```

---

## Abstract Classes

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    def describe(self):                # Concrete method
        return f"Area: {self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):                    # Must implement
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):               # Must implement
        import math
        return 2 * math.pi * self.radius

# Shape()       # TypeError: Can't instantiate abstract class
Circle(5)       # OK — implements all abstract methods
```

---

## Dunder Methods

| Method | Triggered by |
|--------|-------------|
| `__init__` | `ClassName()` |
| `__str__` | `print(obj)`, `str(obj)` |
| `__repr__` | `repr(obj)` |
| `__len__` | `len(obj)` |
| `__eq__` | `obj1 == obj2` |
| `__lt__` | `obj1 < obj2` |
| `__add__` | `obj1 + obj2` |
| `__getitem__` | `obj[key]` |
| `__setitem__` | `obj[key] = value` |
| `__contains__` | `item in obj` |
| `__iter__` | `for x in obj` |
| `__del__` | Object destroyed |
| `__enter__` | `with obj as x:` |
| `__exit__` | End of `with` block |

---

## The 4 Pillars

```
ENCAPSULATION:
  Bundle data + methods together
  Control access with @property
  Private by convention: self._attr

INHERITANCE:
  Child class extends parent class
  super() calls parent methods
  Method overriding

POLYMORPHISM:
  Same interface, different behavior
  def area() means different things for Circle vs Rectangle
  Works through method overriding and duck typing

ABSTRACTION:
  Hide implementation details
  Show only what's needed
  ABC + @abstractmethod enforces interface
```
