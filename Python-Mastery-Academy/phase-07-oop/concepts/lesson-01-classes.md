# Lesson 01 — Classes and Objects

**Phase:** 07 — OOP | **Time:** ~45 min

---

## Part 1: What is a Class?

A class is a **blueprint** for creating objects.
An object is an **instance** of a class.

**Analogy:**
- Class = Blueprint of a house
- Object = An actual house built from that blueprint
- You can build 100 houses from one blueprint — all similar, all distinct

---

## Part 2: Your First Class

```python
class Dog:
    """A simple Dog class."""
    
    # Class attribute (shared by all instances)
    species = "Canis lupus familiaris"
    
    def __init__(self, name: str, breed: str, age: int):
        """
        Constructor — runs when you create a new Dog.
        self = the instance being created
        """
        # Instance attributes (unique to each instance)
        self.name = name
        self.breed = breed
        self.age = age
    
    def bark(self) -> str:
        """Make the dog bark."""
        return f"{self.name} says: Woof!"
    
    def describe(self) -> str:
        """Describe the dog."""
        return f"{self.name} is a {self.age}-year-old {self.breed}."

# CREATE OBJECTS (instances)
dog1 = Dog("Buddy", "Labrador", 3)
dog2 = Dog("Max", "German Shepherd", 5)

# ACCESS ATTRIBUTES
print(dog1.name)      # Buddy
print(dog2.breed)     # German Shepherd
print(dog1.age)       # 3

# CALL METHODS
print(dog1.bark())        # Buddy says: Woof!
print(dog2.describe())    # Max is a 5-year-old German Shepherd.

# CLASS ATTRIBUTE (same for all)
print(Dog.species)         # Canis lupus familiaris
print(dog1.species)        # Also works
```

---

## Part 3: The `__init__` Method

`__init__` is the constructor. It runs automatically when you create a new instance.

```python
class Product:
    """Represents a product in an inventory system."""
    
    total_products = 0    # Class attribute — tracks count
    
    def __init__(self, name: str, price: float, quantity: int):
        # Instance attributes
        self.name = name
        self.price = price
        self.quantity = quantity
        self.is_available = quantity > 0    # Derived attribute
        
        # Update class attribute
        Product.total_products += 1
        self.product_id = f"P{Product.total_products:04d}"
    
    def get_total_value(self) -> float:
        """Calculate total stock value."""
        return self.price * self.quantity
    
    def sell(self, units: int) -> bool:
        """Sell units. Returns True if successful."""
        if units > self.quantity:
            return False
        self.quantity -= units
        self.is_available = self.quantity > 0
        return True
    
    def __str__(self) -> str:
        """String representation — what print() shows."""
        return f"[{self.product_id}] {self.name} — ${self.price:.2f} ({self.quantity} in stock)"

# Create products
laptop = Product("Laptop Pro 15", 1299.99, 50)
mouse = Product("Wireless Mouse", 29.99, 200)
keyboard = Product("Mechanical Keyboard", 79.99, 75)

print(laptop)                      # [P0001] Laptop Pro 15 — $1299.99 (50 in stock)
print(mouse)                       # [P0002] Wireless Mouse — $29.99 (200 in stock)
print(f"Total products: {Product.total_products}")   # 3

print(f"Laptop value: ${laptop.get_total_value():,.2f}")   # $64,999.50

laptop.sell(5)
print(f"After selling 5: {laptop.quantity} remaining")
```

---

## Part 4: Instance vs Class Attributes

```python
class Employee:
    # CLASS ATTRIBUTE — shared by ALL employees
    company_name = "Python Corp"
    employee_count = 0
    
    def __init__(self, name: str, salary: float):
        # INSTANCE ATTRIBUTES — unique to each employee
        self.name = name
        self.salary = salary
        Employee.employee_count += 1

alice = Employee("Alice", 75000)
bob = Employee("Bob", 65000)

# Instance attributes — different for each
print(alice.name)     # Alice
print(bob.name)       # Bob

# Class attributes — same for all
print(alice.company_name)    # Python Corp
print(bob.company_name)      # Python Corp
print(Employee.company_name) # Python Corp

# Instance attribute change — only affects that instance
alice.company_name = "New Company"    # Creates instance attribute, shadows class attr
print(alice.company_name)             # New Company (instance attr)
print(bob.company_name)               # Python Corp (still class attr)

# Class attribute change — affects all instances that haven't overridden
Employee.company_name = "Updated Corp"
print(bob.company_name)    # Updated Corp
```

---

## Part 5: Methods

```python
class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner = owner
        self._balance = initial_balance    # _ prefix = "private by convention"
    
    # INSTANCE METHOD — needs self, operates on instance data
    def deposit(self, amount: float) -> None:
        if amount > 0:
            self._balance += amount
            print(f"Deposited ${amount:.2f}. Balance: ${self._balance:.2f}")
    
    def withdraw(self, amount: float) -> bool:
        if amount > self._balance:
            print("Insufficient funds.")
            return False
        self._balance -= amount
        print(f"Withdrew ${amount:.2f}. Balance: ${self._balance:.2f}")
        return True
    
    def get_balance(self) -> float:
        return self._balance
    
    # CLASS METHOD — uses cls, can access class-level data
    @classmethod
    def create_savings_account(cls, owner: str) -> "BankAccount":
        """Factory method — creates a savings account with $100 minimum."""
        account = cls(owner, 100.0)
        return account
    
    # STATIC METHOD — belongs to class but doesn't need self or cls
    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Validate that amount is positive."""
        return amount > 0
    
    def __str__(self) -> str:
        return f"Account({self.owner}, ${self._balance:.2f})"

acc = BankAccount("Alice", 1000)
acc.deposit(500)
acc.withdraw(200)
print(acc.get_balance())

savings = BankAccount.create_savings_account("Bob")
print(savings)
```

---

## Part 6: Business Example — Employee Class

```python
from datetime import datetime

class Employee:
    """Represents a company employee."""
    
    EMPLOYMENT_TYPES = ("full-time", "part-time", "contract")
    
    def __init__(
        self,
        name: str,
        department: str,
        salary: float,
        employment_type: str = "full-time"
    ):
        if employment_type not in self.EMPLOYMENT_TYPES:
            raise ValueError(f"Invalid type: {employment_type}")
        
        self.name = name
        self.department = department
        self._salary = salary
        self.employment_type = employment_type
        self.hire_date = datetime.now()
        self.is_active = True
    
    @property
    def salary(self) -> float:
        return self._salary
    
    @salary.setter
    def salary(self, new_salary: float) -> None:
        if new_salary < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = new_salary
    
    def give_raise(self, percentage: float) -> float:
        increase = self._salary * (percentage / 100)
        self._salary += increase
        return self._salary
    
    def annual_cost(self) -> float:
        """Total annual cost including 30% employer overhead."""
        return self._salary * 1.30
    
    def years_employed(self) -> float:
        delta = datetime.now() - self.hire_date
        return delta.days / 365
    
    def __repr__(self) -> str:
        return f"Employee('{self.name}', '{self.department}', ${self._salary:,.0f})"
    
    def __str__(self) -> str:
        return f"{self.name} — {self.department} — ${self._salary:,.0f}/yr"

# Usage
emp = Employee("Alice Johnson", "Engineering", 85000)
print(emp)                           # Alice Johnson — Engineering — $85,000/yr

emp.give_raise(10)
print(f"After raise: ${emp.salary:,.2f}")   # $93,500.00

emp.salary = 90000                   # Uses @property setter
print(f"Updated: ${emp.salary:,.2f}")
```

---

## Common Mistakes

```python
# Mistake 1: Forgetting self
class Counter:
    def __init__(self):
        count = 0      # WRONG — local variable, not instance attribute
        self.count = 0 # CORRECT

# Mistake 2: Forgetting self in method call
class Dog:
    def bark(self):
        return "Woof!"
    
    def describe(self):
        return bark()      # WRONG — NameError
        return self.bark() # CORRECT

# Mistake 3: Modifying class attribute via instance
class Config:
    db_host = "localhost"

c1 = Config()
c1.db_host = "production"   # Creates instance attribute (doesn't affect class)
print(Config.db_host)        # Still "localhost"

# To change for ALL instances:
Config.db_host = "production"
```

---

## Practice Exercises

1. Create a `Rectangle` class with `width` and `height`. Add methods: `area()`, `perimeter()`, `is_square()`.

2. Create a `Student` class with name, grades list, methods: `add_grade()`, `average()`, `highest_grade()`, `lowest_grade()`.

3. Create a `Car` class with make, model, year, mileage. Add `drive(miles)` and `fuel_efficiency(miles, gallons)`.

4. Create a `ShoppingCart` class that can `add_item()`, `remove_item()`, `calculate_total()`, `apply_discount()`.

---

## Next Lesson

**[Lesson 03 → Inheritance](lesson-03-inheritance.md)**
