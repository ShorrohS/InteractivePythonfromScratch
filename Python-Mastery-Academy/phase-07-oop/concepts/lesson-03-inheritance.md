# Lesson 03 — Inheritance

**Phase:** 07 — OOP | **Time:** ~45 min

---

## Part 1: What is Inheritance?

Inheritance allows a class to **inherit** (reuse) attributes and methods from another class.

**Analogy:**
- Parent class = general blueprint
- Child class = specialized blueprint that extends the parent

```
Vehicle (parent)
├── Car (child)
├── Truck (child)
└── Motorcycle (child)
```

All are vehicles — they share speed, fuel, drive(). But each has unique features.

---

## Part 2: Basic Inheritance

```python
# PARENT CLASS (Base class)
class Animal:
    """Base class for all animals."""
    
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.is_alive = True
    
    def eat(self, food: str) -> str:
        return f"{self.name} eats {food}."
    
    def sleep(self) -> str:
        return f"{self.name} is sleeping."
    
    def __str__(self) -> str:
        return f"{self.species}: {self.name}"


# CHILD CLASS (Derived class)
class Dog(Animal):   # Dog inherits from Animal
    """Dog class — extends Animal."""
    
    def __init__(self, name: str, breed: str):
        # Call parent's __init__ using super()
        super().__init__(name, species="Canis lupus familiaris")
        self.breed = breed
        self.tricks = []
    
    # New method — only in Dog
    def bark(self) -> str:
        return f"{self.name} says: Woof!"
    
    # New method — only in Dog
    def learn_trick(self, trick: str) -> None:
        self.tricks.append(trick)
    
    # Override parent method
    def __str__(self) -> str:
        return f"Dog({self.name}, {self.breed})"


class Cat(Animal):
    """Cat class — extends Animal."""
    
    def __init__(self, name: str, is_indoor: bool = True):
        super().__init__(name, species="Felis catus")
        self.is_indoor = is_indoor
    
    def meow(self) -> str:
        return f"{self.name} says: Meow!"
    
    def purr(self) -> str:
        return f"{self.name} purrs contentedly."


# Usage
dog = Dog("Buddy", "Labrador")
cat = Cat("Whiskers")

# Inherited methods
print(dog.eat("kibble"))     # Buddy eats kibble.  (from Animal)
print(dog.sleep())            # Buddy is sleeping.   (from Animal)
print(cat.eat("tuna"))        # Whiskers eats tuna.

# Dog-specific methods
print(dog.bark())             # Buddy says: Woof!
dog.learn_trick("sit")
dog.learn_trick("shake")
print(dog.tricks)             # ['sit', 'shake']

# Cat-specific methods
print(cat.meow())             # Whiskers says: Meow!

# isinstance() checks
print(isinstance(dog, Dog))      # True
print(isinstance(dog, Animal))   # True — dog IS an Animal
print(isinstance(cat, Dog))      # False
```

---

## Part 3: super()

`super()` calls the parent class's method:

```python
class Vehicle:
    def __init__(self, make: str, model: str, year: int):
        self.make = make
        self.model = model
        self.year = year
        self.speed = 0
    
    def start(self) -> str:
        return f"{self.make} {self.model} engine started."
    
    def accelerate(self, amount: int) -> None:
        self.speed += amount

class ElectricCar(Vehicle):
    def __init__(self, make: str, model: str, year: int, battery_kwh: float):
        super().__init__(make, model, year)   # Call Vehicle's __init__
        self.battery_kwh = battery_kwh
        self.charge_level = 100.0
    
    def start(self) -> str:
        parent_msg = super().start()   # Call Vehicle's start()
        return f"{parent_msg} (silent — electric!)"
    
    def charge(self, hours: float) -> None:
        added = hours * 10   # 10 kWh per hour
        self.charge_level = min(100.0, self.charge_level + added)

tesla = ElectricCar("Tesla", "Model 3", 2024, 75.0)
print(tesla.start())      # Tesla Model 3 engine started. (silent — electric!)
tesla.accelerate(30)
print(tesla.speed)         # 30  (inherited from Vehicle)
```

---

## Part 4: Employee Hierarchy — Real Example

```python
class Employee:
    """Base employee class."""
    
    def __init__(self, name: str, employee_id: str, base_salary: float):
        self.name = name
        self.employee_id = employee_id
        self.base_salary = base_salary
    
    def calculate_pay(self) -> float:
        """Override in subclasses for different pay structures."""
        return self.base_salary
    
    def display_info(self) -> str:
        pay = self.calculate_pay()
        return f"{self.employee_id} | {self.name:<20} | ${pay:>10,.2f}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r})"


class FullTimeEmployee(Employee):
    """Salaried employee."""
    
    def __init__(self, name, emp_id, salary, benefits_value: float = 5000):
        super().__init__(name, emp_id, salary)
        self.benefits_value = benefits_value
    
    def calculate_pay(self) -> float:
        return self.base_salary    # Annual salary


class HourlyEmployee(Employee):
    """Hourly / part-time employee."""
    
    def __init__(self, name, emp_id, hourly_rate: float, hours_per_week: float = 40):
        super().__init__(name, emp_id, hourly_rate * hours_per_week * 52)
        self.hourly_rate = hourly_rate
        self.hours_per_week = hours_per_week
    
    def calculate_pay(self) -> float:
        return self.hourly_rate * self.hours_per_week * 52


class CommissionEmployee(Employee):
    """Sales employee with base + commission."""
    
    def __init__(self, name, emp_id, base_salary: float, commission_rate: float):
        super().__init__(name, emp_id, base_salary)
        self.commission_rate = commission_rate
        self.sales_total = 0.0
    
    def record_sale(self, amount: float) -> None:
        self.sales_total += amount
    
    def calculate_pay(self) -> float:
        return self.base_salary + (self.sales_total * self.commission_rate)


# Create employees of different types
employees = [
    FullTimeEmployee("Alice Johnson", "FT001", 85000),
    HourlyEmployee("Bob Smith", "HT001", 25.0, 40),
    CommissionEmployee("Carol Davis", "CM001", 40000, 0.05),
]

employees[2].record_sale(300000)    # Carol made $300k in sales

# Polymorphism: same method, different behavior
print(f"{'ID':<8} {'Name':<22} {'Annual Pay':>12}")
print("─" * 45)
for emp in employees:
    print(emp.display_info())   # Each calculates pay differently!
```

---

## Part 5: Multiple Inheritance

```python
class Flyable:
    def fly(self) -> str:
        return f"{self.__class__.__name__} is flying!"

class Swimmable:
    def swim(self) -> str:
        return f"{self.__class__.__name__} is swimming!"

class Duck(Animal, Flyable, Swimmable):
    def quack(self) -> str:
        return "Quack!"

donald = Duck("Donald", "Duck")
print(donald.fly())     # Duck is flying!
print(donald.swim())    # Duck is swimming!
print(donald.quack())   # Quack!
print(donald.eat("bread"))  # Donald eats bread.  (from Animal)
```

---

## Practice Exercises

1. Create a `Shape` parent class with `area()` and `perimeter()`. Create children: `Circle`, `Rectangle`, `Triangle`.

2. Create a `Person → Employee → Manager` hierarchy where Manager has a `team` list and `add_to_team()`.

3. Create a `Vehicle → Car → ElectricCar` hierarchy with appropriate attributes.

4. What does `isinstance(obj, ParentClass)` return for child class instances?

---

## Next Lesson

**[Lesson 05 → Encapsulation](lesson-05-encapsulation.md)**
