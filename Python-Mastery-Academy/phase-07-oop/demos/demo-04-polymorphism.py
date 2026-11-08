"""
Demo 04 - Polymorphism
Phase 07: OOP

Run: python demo-04-polymorphism.py
"""

import math
from abc import ABC, abstractmethod

print("=" * 55)
print("DEMO 04 - Polymorphism")
print("=" * 55)

# --- 1. DUCK TYPING ---
print("\n1. Duck typing — 'if it quacks like a duck...':")

# Python doesn't care about the TYPE — only whether the object has
# the method/attribute the code needs.  No shared base class required.

class Duck:
    def speak(self) -> str:
        return "Quack!"

class Dog:
    def speak(self) -> str:
        return "Woof!"

class Robot:
    def speak(self) -> str:
        return "Beep boop."

class TextToSpeech:
    def speak(self) -> str:
        return "I am synthesised speech."

def make_noise(thing) -> None:
    """Works for ANY object with a .speak() method — no isinstance check."""
    print(f"  {type(thing).__name__}: {thing.speak()}")

things = [Duck(), Dog(), Robot(), TextToSpeech()]
for t in things:
    make_noise(t)


# --- 2. ABSTRACT BASE CLASSES ---
print("\n2. Abstract Base Classes (ABC):")

class Shape(ABC):
    """
    Defines a guaranteed interface.
    Any class inheriting Shape MUST implement area() and perimeter(),
    or Python raises TypeError at instantiation time.
    """

    @abstractmethod
    def area(self) -> float:
        """Subclass must implement this."""

    @abstractmethod
    def perimeter(self) -> float:
        """Subclass must implement this."""

    def describe(self) -> str:
        """Concrete method — shared by all shapes, uses the abstract ones."""
        return (f"{self.__class__.__name__}: "
                f"area={self.area():.2f}, perimeter={self.perimeter():.2f}")

class Circle(Shape):
    def __init__(self, r: float): self.r = r
    def area(self)      -> float: return math.pi * self.r ** 2
    def perimeter(self) -> float: return 2 * math.pi * self.r

class Rectangle(Shape):
    def __init__(self, w: float, h: float): self.w = w; self.h = h
    def area(self)      -> float: return self.w * self.h
    def perimeter(self) -> float: return 2 * (self.w + self.h)

class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a, self.b, self.c = a, b, c
    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s-self.a) * (s-self.b) * (s-self.c))
    def perimeter(self) -> float:
        return self.a + self.b + self.c

shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
for s in shapes:
    print(f"  {s.describe()}")

total_area = sum(s.area() for s in shapes)
print(f"  Total area: {total_area:.2f}")

# Can't instantiate an ABC directly
try:
    Shape()
except TypeError as e:
    print(f"  Shape() → TypeError: Can't instantiate abstract class")


# --- 3. METHOD OVERRIDING WITH super() ---
print("\n3. Method overriding and super():")

class Vehicle:
    def __init__(self, make: str, model: str, year: int):
        self.make  = make
        self.model = model
        self.year  = year

    def start(self) -> str:
        return f"{self.make} {self.model}: engine starting..."

    def describe(self) -> str:
        return f"{self.year} {self.make} {self.model}"

class ElectricVehicle(Vehicle):
    def __init__(self, make: str, model: str, year: int, battery_kwh: float):
        super().__init__(make, model, year)   # reuse parent __init__
        self.battery_kwh = battery_kwh

    def start(self) -> str:
        # Override — replace parent behaviour entirely
        return f"{self.make} {self.model}: silent electric start."

    def describe(self) -> str:
        # Extend — add to parent behaviour using super()
        return super().describe() + f" (EV, {self.battery_kwh}kWh)"

class HybridVehicle(ElectricVehicle):
    def start(self) -> str:
        return f"{self.make} {self.model}: starting on battery, engine ready."

vehicles = [
    Vehicle("Toyota", "Corolla", 2020),
    ElectricVehicle("Tesla", "Model 3", 2023, 75),
    HybridVehicle("Toyota", "Prius", 2022, 8.8),
]

for v in vehicles:
    print(f"  {v.describe()}")
    print(f"    → {v.start()}")


# --- 4. OPERATOR OVERLOADING ---
print("\n4. Operator overloading — __add__, __mul__, __eq__:")

class Vector:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        """Handles scalar * vector (not just vector * scalar)."""
        return self.__mul__(scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"  v1 = {v1}  |magnitude: {v1.magnitude():.2f}")
print(f"  v2 = {v2}")
print(f"  v1 + v2 = {v1 + v2}")
print(f"  v1 - v2 = {v1 - v2}")
print(f"  v1 * 2  = {v1 * 2}")
print(f"  3 * v2  = {3 * v2}   (via __rmul__)")
print(f"  v1 == v1: {v1 == v1}")
print(f"  v1 == v2: {v1 == v2}")
