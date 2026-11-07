"""
Demo 01 - Classes and Objects
Phase 07: OOP

Run: python demo-01-classes.py
"""

print("=" * 55)
print("DEMO 01 - Classes and Objects")
print("=" * 55)

# --- BASIC CLASS ---
print("\n1. Basic class:")

class Dog:
    species = "Canis lupus familiaris"   # class attribute

    def __init__(self, name: str, breed: str, age: int):
        self.name  = name    # instance attributes
        self.breed = breed
        self.age   = age

    def bark(self) -> str:
        return f"{self.name} says: Woof!"

    def info(self) -> str:
        return f"{self.name}: {self.breed}, {self.age} years old"

    def __str__(self) -> str:
        return f"Dog({self.name!r}, {self.breed})"

    def __repr__(self) -> str:
        return f"Dog(name={self.name!r}, breed={self.breed!r}, age={self.age})"

d1 = Dog("Buddy", "Labrador", 3)
d2 = Dog("Max",   "German Shepherd", 5)

print(f"  {d1.bark()}")
print(f"  {d2.info()}")
print(f"  str:  {d1}")
print(f"  repr: {repr(d1)}")
print(f"  Species: {Dog.species}")

# --- PROPERTIES ---
print("\n2. @property with validation:")

class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self.owner    = owner
        self._balance = max(0.0, balance)

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = round(float(amount), 2)

    def deposit(self, amount: float) -> None:
        self._balance += amount
        print(f"  Deposited ${amount:,.2f}. Balance: ${self._balance:,.2f}")

    def __str__(self) -> str:
        return f"Account({self.owner!r}, ${self._balance:,.2f})"

acc = BankAccount("Alice", 1000)
acc.deposit(500)
acc.deposit(250)
print(f"  {acc}")

# --- CLASS vs INSTANCE ATTRIBUTES ---
print("\n3. Class vs instance attributes:")

class Employee:
    company = "TechCorp"   # shared by all
    count   = 0

    def __init__(self, name: str, salary: float):
        self.name   = name
        self.salary = salary
        Employee.count += 1

e1 = Employee("Alice", 85000)
e2 = Employee("Bob",   65000)

print(f"  Company (class):    {Employee.company}")
print(f"  Company (instance): {e1.company}")
print(f"  Total employees:    {Employee.count}")
print(f"  e1.name: {e1.name}")
print(f"  e2.name: {e2.name}")

# --- DUNDER METHODS ---
print("\n4. Dunder methods:")

class Product:
    def __init__(self, name: str, price: float, qty: int):
        self.name  = name
        self.price = price
        self.qty   = qty

    def __str__(self)  -> str: return f"{self.name}: ${self.price:.2f}"
    def __repr__(self) -> str: return f"Product({self.name!r}, {self.price})"
    def __len__(self)  -> int: return self.qty
    def __eq__(self, other) -> bool:
        return isinstance(other, Product) and self.name == other.name

products = [Product("Laptop", 999.99, 5), Product("Mouse", 29.99, 50)]
for p in products:
    print(f"  {p}  (stock: {len(p)})")

print(f"  Same product: {Product('Laptop',999,5) == Product('Laptop',100,1)}")
