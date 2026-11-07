"""
Debugging Challenge 01 - Phase 07: OOP
=======================================

8 bugs related to classes, inheritance, methods, and properties.
"""

print("=" * 50)
print("DEBUGGING CHALLENGE - OOP")
print("=" * 50)

# BUG 1: Missing 'self' in method parameter
print("\nBug 1 - Missing self:")
class Greeter:
    def __init__(self, name):
        self.name = name

    def greet():   # BUG: missing 'self'
        return f"Hello, {self.name}!"

g = Greeter("Alice")
print(g.greet())


# BUG 2: Accessing attribute before it's set
print("\nBug 2 - Attribute before assignment:")
class Config:
    def __init__(self):
        self.settings = {}

    def set(self, key, value):
        self.settings[key] = value

c = Config()
print(c.settings["theme"])   # BUG: "theme" key doesn't exist yet


# BUG 3: Forgetting super().__init__() in child
print("\nBug 3 - Missing super().__init__:")
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        # BUG: forgot super().__init__(name)
        self.breed = breed

    def speak(self):
        return f"{self.name} says Woof!"   # will fail: self.name not set

d = Dog("Rex", "Labrador")
print(d.speak())


# BUG 4: Class attribute modified through instance (mutation trap)
print("\nBug 4 - Class attribute mutation:")
class Team:
    members = []   # BUG: mutable class attribute shared by ALL instances

    def add_member(self, name):
        self.members.append(name)

t1 = Team()
t2 = Team()
t1.add_member("Alice")
t1.add_member("Bob")
t2.add_member("Carol")

print(f"t1 members: {t1.members}")   # Should be ['Alice', 'Bob']
print(f"t2 members: {t2.members}")   # Should be ['Carol']


# BUG 5: @property getter defined after setter
print("\nBug 5 - Property order:")
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @celsius.setter    # BUG: setter defined before getter — NameError
    def celsius(self, value):
        self._celsius = value

    @property
    def celsius(self):
        return self._celsius

t = Temperature(20)
t.celsius = 30
print(t.celsius)


# BUG 6: Calling method without parentheses
print("\nBug 6 - Missing parentheses:")
class Calculator:
    def __init__(self, value):
        self.value = value

    def doubled(self):
        return self.value * 2

calc = Calculator(5)
result = calc.doubled    # BUG: missing () — gets method object, not result
print(f"Doubled: {result}")


# BUG 7: Wrong comparison in __eq__
print("\nBug 7 - Wrong __eq__:")
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x   # BUG: only checks x, ignores y

p1 = Point(1, 2)
p2 = Point(1, 3)   # different y
print(f"p1 == p2: {p1 == p2}")   # Should be False


# BUG 8: Instantiating abstract class
print("\nBug 8 - Instantiating abstract class:")
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): pass

s = Shape()   # BUG: TypeError — can't instantiate abstract class
print(f"Area: {s.area()}")

print("\n" + "=" * 50)
print("Fixed all 8 bugs?")

# ============================================================
# ANSWERS
# ============================================================
#
# Bug 1: def greet(self):
#
# Bug 2: print(c.settings.get("theme", "default"))
#         or: c.set("theme", "dark") before reading
#
# Bug 3: super().__init__(name) at start of Dog.__init__
#
# Bug 4: def __init__(self):
#             self.members = []    (instance attribute, not class)
#
# Bug 5: Define @property FIRST, then @celsius.setter
#
# Bug 6: result = calc.doubled()   (add parentheses)
#
# Bug 7: return self.x == other.x and self.y == other.y
#
# Bug 8: Create a concrete subclass:
#   class Circle(Shape):
#       def area(self): return 0
#   s = Circle()
