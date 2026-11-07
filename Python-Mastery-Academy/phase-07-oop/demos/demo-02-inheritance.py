"""
Demo 02 - Inheritance and Polymorphism
Phase 07: OOP

Run: python demo-02-inheritance.py
"""

import math

print("=" * 55)
print("DEMO 02 - Inheritance and Polymorphism")
print("=" * 55)

# --- BASIC INHERITANCE ---
print("\n1. Basic inheritance:")

class Animal:
    def __init__(self, name: str, species: str):
        self.name    = name
        self.species = species

    def eat(self, food: str) -> str:
        return f"{self.name} eats {food}."

    def __str__(self) -> str:
        return f"{self.species}: {self.name}"

class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name, species="Dog")
        self.breed = breed

    def bark(self) -> str:
        return f"{self.name}: Woof!"

    def __str__(self) -> str:
        return f"Dog({self.name}, {self.breed})"

class Cat(Animal):
    def __init__(self, name: str):
        super().__init__(name, species="Cat")

    def purr(self) -> str:
        return f"{self.name}: Purrr..."

dog = Dog("Rex", "German Shepherd")
cat = Cat("Luna")

print(f"  {dog.eat('kibble')}")   # inherited from Animal
print(f"  {dog.bark()}")
print(f"  {cat.eat('tuna')}")
print(f"  {cat.purr()}")
print(f"  isinstance(dog, Animal): {isinstance(dog, Animal)}")

# --- POLYMORPHISM ---
print("\n2. Polymorphism — same interface, different behaviour:")

class Shape:
    def area(self) -> float:
        raise NotImplementedError

    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}"

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return math.pi * self.r ** 2

class Rectangle(Shape):
    def __init__(self, w, h): self.w = w; self.h = h
    def area(self): return self.w * self.h

class Triangle(Shape):
    def __init__(self, b, h): self.b = b; self.h = h
    def area(self): return 0.5 * self.b * self.h

shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]
for shape in shapes:
    print(f"  {shape.describe()}")

# SAME function works for all shapes
total = sum(s.area() for s in shapes)
print(f"  Total area: {total:.2f}")

# --- METHOD RESOLUTION ORDER ---
print("\n3. Method Resolution Order (MRO):")

class A:
    def method(self): return "A"
class B(A):
    def method(self): return "B"
class C(A):
    def method(self): return "C"
class D(B, C):       # Multiple inheritance
    pass

d = D()
print(f"  D.method(): {d.method()}")   # B (left-to-right)
print(f"  MRO: {[c.__name__ for c in D.__mro__]}")
