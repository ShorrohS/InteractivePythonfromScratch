# Phase 07 — Intermediate Solutions: OOP

---

## Q1. Vehicle Hierarchy

```python
class Vehicle:
    def __init__(self, make: str, model: str, year: int):
        self.make, self.model, self.year = make, model, year

    def describe(self) -> str:
        return f"{self.year} {self.make} {self.model}"

    def start(self) -> str:
        return f"{self.make} {self.model}: engine starting."


class Car(Vehicle):
    def __init__(self, make, model, year, num_doors: int = 4):
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def start(self) -> str:
        return f"{self.make} {self.model}: {self.num_doors}-door ready."


class ElectricCar(Vehicle):
    def __init__(self, make, model, year, battery_kwh: float):
        super().__init__(make, model, year)
        self.battery_kwh = battery_kwh

    def start(self) -> str:
        return f"{self.make} {self.model}: silent electric start."

    def describe(self) -> str:
        return super().describe() + f" (EV, {self.battery_kwh}kWh)"


class Truck(Vehicle):
    def __init__(self, make, model, year, payload_kg: float):
        super().__init__(make, model, year)
        self.payload_kg = payload_kg

    def start(self) -> str:
        return f"{self.make} {self.model}: heavy diesel engine starts."


vehicles = [
    Vehicle("Toyota",  "Corolla", 2020),
    Car("Honda",       "Civic",   2022, 4),
    ElectricCar("Tesla","Model 3",2023, 75),
    Truck("Ford",      "F-350",   2021, 3500),
]
for v in vehicles:
    print(v.describe())
    print(f"  → {v.start()}")
```

---

## Q2. Person and Employee with Properties

```python
class Person:
    def __init__(self, first_name: str, last_name: str, age: int):
        self.first_name = first_name
        self.last_name  = last_name
        self._age       = 0
        self.age        = age

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("age must be int")
        if not 0 <= value <= 150:
            raise ValueError(f"age must be 0–150, got {value}")
        self._age = value


class Employee(Person):
    def __init__(self, first_name, last_name, age,
                 salary: float, department: str):
        super().__init__(first_name, last_name, age)
        self._salary    = 0.0
        self.salary     = salary
        self.department = department

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if value < 0:
            raise ValueError("salary cannot be negative")
        self._salary = round(float(value), 2)

    @property
    def monthly_salary(self) -> float:
        return round(self._salary / 12, 2)

    def get_summary(self) -> str:
        return (f"{self.full_name} | age {self.age} | "
                f"{self.department} | ${self.salary:,.2f}/yr "
                f"(${self.monthly_salary:,.2f}/mo)")


e = Employee("Alice", "Smith", 32, 84000, "Engineering")
print(e.get_summary())
print(e.full_name)
```

---

## Q3. Date Class

```python
from datetime import datetime, date as _date
import math

class Date:
    def __init__(self, year: int, month: int, day: int):
        if not Date.is_valid(year, month, day):
            raise ValueError(f"Invalid date: {year}-{month}-{day}")
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_string(cls, s: str) -> "Date":
        y, m, d = map(int, s.split("-"))
        return cls(y, m, d)

    @classmethod
    def today(cls) -> "Date":
        n = datetime.now()
        return cls(n.year, n.month, n.day)

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @staticmethod
    def is_valid(year: int, month: int, day: int) -> bool:
        try:
            _date(year, month, day)
            return True
        except ValueError:
            return False

    def days_until(self, other: "Date") -> int:
        a = _date(self.year, self.month, self.day)
        b = _date(other.year, other.month, other.day)
        return (b - a).days

    def __str__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

    def __repr__(self) -> str:
        return f"Date({self.year}, {self.month}, {self.day})"


d1 = Date.from_string("2024-01-01")
d2 = Date.today()
print(d1, d2)
print(f"2024 leap? {Date.is_leap_year(2024)}")
print(f"Days from {d1} to {d2}: {d1.days_until(d2)}")
```

---

## Q4. Shape ABC

```python
import math
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

    @abstractmethod
    def perimeter(self) -> float: ...

    def describe(self) -> str:
        return (f"{self.__class__.__name__}: "
                f"area={self.area():.2f}, perimeter={self.perimeter():.2f}")

    def __str__(self) -> str:
        return self.describe()


class Circle(Shape):
    def __init__(self, radius: float): self.radius = radius
    def area(self)      -> float: return math.pi * self.radius ** 2
    def perimeter(self) -> float: return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width, self.height = width, height
    def area(self)      -> float: return self.width * self.height
    def perimeter(self) -> float: return 2 * (self.width + self.height)


class Square(Rectangle):
    def __init__(self, side: float):
        super().__init__(side, side)


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a, self.b, self.c = a, b, c
    def perimeter(self) -> float:
        return self.a + self.b + self.c
    def area(self) -> float:
        s = self.perimeter() / 2
        return math.sqrt(s * (s-self.a) * (s-self.b) * (s-self.c))


shapes = [Circle(5), Rectangle(4, 6), Square(4), Triangle(3, 4, 5)]
for s in shapes:
    print(s)

largest = max(shapes, key=lambda s: s.area())
print(f"Largest area: {largest}")
```

---

## Q5. Library with Composition

```python
class Book:
    def __init__(self, title: str, author: str, isbn: str, pages: int):
        self.title  = title
        self.author = author
        self.isbn   = isbn
        self.pages  = pages

    def __str__(self) -> str:
        return f'"{self.title}" by {self.author} [{self.isbn}]'

    def __repr__(self) -> str:
        return f"Book({self.title!r}, {self.author!r}, {self.isbn!r}, {self.pages})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Book) and self.isbn == other.isbn


class Library:
    def __init__(self, name: str):
        self.name   = name
        self._books: list = []

    def add(self, book: Book) -> None:
        self._books.append(book)

    def remove(self, isbn: str) -> bool:
        before = len(self._books)
        self._books = [b for b in self._books if b.isbn != isbn]
        return len(self._books) < before

    def find_by_author(self, author: str) -> list:
        return [b for b in self._books
                if author.lower() in b.author.lower()]

    def find_by_title(self, keyword: str) -> list:
        return [b for b in self._books
                if keyword.lower() in b.title.lower()]

    def __len__(self) -> int:
        return len(self._books)

    def __iter__(self):
        return iter(self._books)

    def __contains__(self, book: Book) -> bool:
        return book in self._books


lib = Library("City Library")
lib.add(Book("Clean Code",      "Robert Martin",  "978-0132350884", 431))
lib.add(Book("The Pragmatic",   "Andrew Hunt",    "978-0201616224", 352))
lib.add(Book("Design Patterns", "Gang of Four",   "978-0201633610", 395))
lib.add(Book("Refactoring",     "Robert Martin",  "978-0134757599", 448))
lib.add(Book("Python Fluent",   "Luciano Ramalho","978-1492056355", 792))

print(f"Library: {len(lib)} books")
print("By Robert Martin:")
for b in lib.find_by_author("Robert Martin"):
    print(f"  {b}")
print("All titles:")
for b in lib:
    print(f"  {b.title}")
```

---

## Q6. Vector with Operator Overloading

```python
import math

class Vector:
    def __init__(self, x: float, y: float, z: float = 0.0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x-other.x, self.y-other.y, self.z-other.z)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x*scalar, self.y*scalar, self.z*scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y, -self.z)

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Vector) and
                self.x == other.x and self.y == other.y and self.z == other.z)

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def dot(self, other: "Vector") -> float:
        return self.x*other.x + self.y*other.y + self.z*other.z

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return str(self)


v1 = Vector(1, 2, 3)
v2 = Vector(4, 5, 6)
print(f"v1 + v2  = {v1 + v2}")
print(f"v1 - v2  = {v1 - v2}")
print(f"v1 * 3   = {v1 * 3}")
print(f"3 * v1   = {3 * v1}")
print(f"-v1      = {-v1}")
print(f"abs(v1)  = {abs(v1):.4f}")
print(f"v1.dot(v2) = {v1.dot(v2)}")
```

---

## Q7. Animal Polymorphism

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name: str, species: str):
        self.name, self.species = name, species

    @abstractmethod
    def sound(self) -> str: ...

    @abstractmethod
    def move(self) -> str: ...

    def __str__(self) -> str:
        return f"{self.species} named {self.name}"


class Lion(Animal):
    def __init__(self, name): super().__init__(name, "Lion")
    def sound(self) -> str: return f"{self.name} roars: ROARRR!"
    def move(self)  -> str: return f"{self.name} runs on four legs."


class Eagle(Animal):
    def __init__(self, name): super().__init__(name, "Eagle")
    def sound(self) -> str: return f"{self.name} screeches!"
    def move(self)  -> str: return f"{self.name} soars through the sky."


class Dolphin(Animal):
    def __init__(self, name): super().__init__(name, "Dolphin")
    def sound(self) -> str: return f"{self.name} clicks and whistles."
    def move(self)  -> str: return f"{self.name} leaps through waves."


class Snake(Animal):
    def __init__(self, name): super().__init__(name, "Snake")
    def sound(self) -> str: return f"{self.name} hisses: ssssss."
    def move(self)  -> str: return f"{self.name} slithers silently."


class Zoo:
    def __init__(self, name: str):
        self.name    = name
        self._animals: list = []

    def add_animal(self, animal: Animal) -> None:
        self._animals.append(animal)

    def all_sounds(self) -> None:
        for a in self._animals:
            print(f"  {a.sound()}")

    def count_by_type(self) -> dict:
        counts: dict = {}
        for a in self._animals:
            counts[a.species] = counts.get(a.species, 0) + 1
        return counts


zoo = Zoo("City Zoo")
for a in [Lion("Simba"), Eagle("Sam"), Dolphin("Dory"),
          Snake("Monty"), Lion("Nala")]:
    zoo.add_animal(a)

zoo.all_sounds()
print(zoo.count_by_type())
```

---

## Q8. Mixin Classes

```python
class LogMixin:
    def log(self, message: str) -> None:
        print(f"[{self.__class__.__name__}] {message}")


class SerializeMixin:
    def to_dict(self) -> dict:
        return vars(self).copy()

    @classmethod
    def from_dict(cls, d: dict):
        obj = cls.__new__(cls)
        obj.__dict__.update(d)
        return obj


class User(LogMixin, SerializeMixin):
    def __init__(self, username: str, email: str, role: str):
        self.username = username
        self.email    = email
        self.role     = role

    def __repr__(self) -> str:
        return f"User({self.username!r}, {self.role!r})"


u = User("alice", "alice@example.com", "admin")
u.log("User logged in")
u.log("Access granted to /admin")

data = u.to_dict()
print(f"Serialised: {data}")

u2 = User.from_dict(data)
print(f"Restored:   {u2}")
u2.log("Restored from dict")
```

---

## Q9. Stack with Container Dunders

```python
class Stack:
    def __init__(self):
        self._items: list = []

    def push(self, item) -> None:
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return len(self._items) > 0   # empty stack is falsy

    def __iter__(self):
        return reversed(self._items)  # top-to-bottom

    def __contains__(self, item) -> bool:
        return item in self._items

    def __repr__(self) -> str:
        top = self._items[-1] if self._items else "empty"
        return f"Stack(top={top!r}, size={len(self)})"


s = Stack()
print(f"Empty stack bool: {bool(s)}")
for v in [10, 20, 30, 40, 50]:
    s.push(v)
print(f"{s}")
print(f"Contains 30: {30 in s}")
print(f"Contains 99: {99 in s}")
print(f"Iterating top→bottom: {list(s)}")
print(f"Popped: {s.pop()}")
print(f"Peek:   {s.peek()}")
print(f"After pop: {s}")
```

---

## Q10. Cached Property Pattern

```python
import math

class DataSet:
    def __init__(self, numbers: list):
        self._numbers = list(numbers)
        self._cache: dict = {}

    def add(self, number: float) -> None:
        self._numbers.append(number)
        self.invalidate_cache()

    def invalidate_cache(self) -> None:
        self._cache.clear()

    def _compute(self, key: str, func):
        if key not in self._cache:
            print(f"  [computing {key}...]")
            self._cache[key] = func()
        return self._cache[key]

    @property
    def mean(self) -> float:
        return self._compute("mean",
            lambda: sum(self._numbers) / len(self._numbers))

    @property
    def median(self) -> float:
        def _median():
            s = sorted(self._numbers)
            n = len(s)
            return s[n//2] if n % 2 else (s[n//2-1] + s[n//2]) / 2
        return self._compute("median", _median)

    @property
    def std_dev(self) -> float:
        def _std():
            m = self.mean
            variance = sum((x - m)**2 for x in self._numbers) / len(self._numbers)
            return math.sqrt(variance)
        return self._compute("std_dev", _std)


ds = DataSet([10, 20, 30, 40, 50])
print("First access — should compute:")
print(f"  mean={ds.mean}, median={ds.median}, std_dev={ds.std_dev:.2f}")
print("Second access — cached, no recompute:")
print(f"  mean={ds.mean}, median={ds.median}, std_dev={ds.std_dev:.2f}")
print("After adding 60 — cache invalidated:")
ds.add(60)
print(f"  mean={ds.mean:.2f}")
```
