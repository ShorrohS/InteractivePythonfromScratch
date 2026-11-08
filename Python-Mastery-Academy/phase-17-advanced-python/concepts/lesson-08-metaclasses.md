# Lesson 08 — Metaclasses

**Phase:** 17 — Advanced Python | **Time:** ~45 min

---

## Part 1: What Is a Metaclass?

In Python, **everything is an object** — including classes themselves.

```python
class Dog:
    pass

fido = Dog()

print(type(fido))    # <class '__main__.Dog'>   — fido is an instance of Dog
print(type(Dog))     # <class 'type'>           — Dog is an instance of type
print(type(int))     # <class 'type'>
print(type(str))     # <class 'type'>
```

The built-in `type` is the **metaclass** of every regular class. A metaclass is the class of a class — it controls how classes are created, just as a class controls how its instances are created.

```
Normal object model
─────────────────────────────────────────────────────
fido        →  instance of  →  Dog
Dog         →  instance of  →  type    (the metaclass)
type        →  instance of  →  type    (type is its own metaclass)
```

### Creating a class dynamically with type()

`type` can be called with three arguments to create a class at runtime:

```python
# type(name, bases, namespace) → new class object
Dog = type(
    "Dog",              # class name (shows in repr and errors)
    (object,),          # base classes as a tuple
    {                   # class body as a namespace dict
        "species": "Canis lupus",
        "speak": lambda self: "Woof!",
    }
)

fido = Dog()
print(fido.speak())     # Woof!
print(Dog.species)      # Canis lupus
print(type(Dog))        # <class 'type'>
```

This is exactly what the `class` keyword does internally.

---

## Part 2: How Python Creates a Class

When Python encounters a `class` statement it follows these steps:

```
1. Execute the class body to collect attributes into a namespace dict
2. Determine the metaclass (explicit metaclass= arg, or inherit from bases, or default: type)
3. Call metaclass.__new__(mcs, name, bases, namespace)  →  creates the class object
4. Call metaclass.__init__(cls,  name, bases, namespace) →  initialises it
5. Bind the resulting class to the name in the enclosing scope
```

```python
# The class statement…
class Animal:
    sound = "..."

    def speak(self) -> str:
        return self.sound

# …is roughly equivalent to:
namespace  = {"sound": "...", "speak": lambda self: self.sound}
Animal     = type("Animal", (object,), namespace)
```

You can intercept steps 3 and 4 by writing a custom metaclass that overrides `__new__` or `__init__`.

---

## Part 3: Creating a Custom Metaclass

### Minimal structure

```python
class Meta(type):
    """A custom metaclass — inherits from type."""

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        # Called when a class using this metaclass is defined.
        # mcs       = Meta itself
        # name      = the new class's name  ("MyClass")
        # bases     = tuple of its base classes
        # namespace = dict of everything defined in the class body

        # Optionally modify namespace here before the class is created
        print(f"  Creating class: {name}")
        cls = super().__new__(mcs, name, bases, namespace)   # let type do the actual work
        return cls

    def __init__(cls, name: str, bases: tuple, namespace: dict):
        # Called after __new__ to initialise the class object.
        super().__init__(name, bases, namespace)


# Apply the metaclass with the metaclass= keyword
class MyClass(metaclass=Meta):
    pass
# → prints: Creating class: MyClass
```

### Practical example — auto-registering subclasses

A classic real-world pattern: a plugin or handler system where every subclass registers itself automatically — no manual `HANDLERS["csv"] = CSVHandler` needed.

```python
class PluginMeta(type):
    """Metaclass that records every non-base subclass in a central registry."""

    registry: dict[str, type] = {}    # shared dict, lives on the metaclass

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:                        # skip the Plugin base class itself
            mcs.registry[name] = cls     # register by class name
        return cls


class Plugin(metaclass=PluginMeta):
    """Base class for all plugins."""
    def run(self) -> str:
        raise NotImplementedError


class CSVPlugin(Plugin):       # registered automatically at class definition time
    def run(self) -> str:
        return "Processing CSV"


class JSONPlugin(Plugin):      # also auto-registered
    def run(self) -> str:
        return "Processing JSON"


# Look up and instantiate a plugin by name — zero manual registration
plugin_class = PluginMeta.registry["CSVPlugin"]
print(plugin_class().run())       # Processing CSV

print(PluginMeta.registry)
# {'CSVPlugin': <class 'CSVPlugin'>, 'JSONPlugin': <class 'JSONPlugin'>}
```

---

## Part 4: __init_subclass__ (Simpler Alternative)

Python 3.6 introduced `__init_subclass__`, a class method called automatically whenever the class is subclassed. It solves most use cases that previously required a metaclass — with far less boilerplate.

```python
class Plugin:
    """Base class with automatic subclass registration — no metaclass needed."""

    _registry: dict[str, type] = {}

    def __init_subclass__(cls, **kwargs):
        """Called automatically each time Plugin (or a subclass) is subclassed."""
        super().__init_subclass__(**kwargs)
        Plugin._registry[cls.__name__] = cls   # register the new subclass

    def run(self) -> str:
        raise NotImplementedError


class CSVPlugin(Plugin):      # __init_subclass__ fires here
    def run(self) -> str:
        return "Processing CSV"


class JSONPlugin(Plugin):     # and here
    def run(self) -> str:
        return "Processing JSON"


print(Plugin._registry)
# {'CSVPlugin': <class 'CSVPlugin'>, 'JSONPlugin': <class 'JSONPlugin'>}
```

`__init_subclass__` also accepts keyword arguments passed in the class header:

```python
class DataPlugin:
    def __init_subclass__(cls, format: str = "unknown", **kwargs):
        super().__init_subclass__(**kwargs)
        cls.format = format    # attach the keyword argument as a class attribute

class XMLHandler(DataPlugin, format="xml"):
    pass

class CSVHandler(DataPlugin, format="csv"):
    pass

print(XMLHandler.format)   # xml
print(CSVHandler.format)   # csv
```

**Prefer `__init_subclass__` over metaclasses** for registration and validation — it's simpler, more readable, and composes more easily with multiple inheritance.

---

## Part 5: Real-World Metaclass Patterns

You rarely write metaclasses yourself, but they power the frameworks you use every day.

### Abstract Base Classes (ABCMeta)

`ABCMeta` enforces that any concrete subclass implements all methods marked `@abstractmethod`:

```python
from abc import ABCMeta, abstractmethod

class Shape(metaclass=ABCMeta):

    @abstractmethod
    def area(self) -> float:
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius


circle = Circle(5)
print(f"area: {circle.area():.2f}")          # area: 78.54
print(f"perimeter: {circle.perimeter():.2f}")# perimeter: 31.42

# ABCMeta raises TypeError if a subclass forgets an abstract method:
# class BadShape(Shape): pass
# → TypeError: Can't instantiate abstract class BadShape with abstract methods area, perimeter
```

The `abc.ABC` convenience base class uses `ABCMeta` internally — both are equivalent:

```python
from abc import ABC, abstractmethod

class Shape(ABC):       # shorthand — identical effect to metaclass=ABCMeta
    @abstractmethod
    def area(self) -> float: ...
```

### Major frameworks

```
Django ORM
  class Employee(models.Model):
      name = models.CharField(max_length=100)
  ModelBase metaclass reads the field descriptors and builds the
  SQL schema, manager, and query API at class creation time.

SQLAlchemy
  class User(Base):
      __tablename__ = "users"
      id = Column(Integer, primary_key=True)
  DeclarativeMeta maps Column descriptors to the table definition
  and wires up the ORM mapper.

Pydantic
  class Employee(BaseModel):
      name: str
      salary: float
  ModelMetaclass reads type annotations at class creation time
  and generates validators, serialisers, and JSON schema.
```

---

## Part 6: When NOT to Use Metaclasses

> "Metaclasses are deeper magic than 99% of users should ever worry about. If you wonder whether you need them, you don't." — Tim Peters

Metaclasses add significant complexity. Before reaching for one, work through this decision guide:

| Problem | Recommended tool |
|---------|-----------------|
| Run code whenever a class is subclassed | `__init_subclass__` |
| Auto-register subclasses in a registry | `__init_subclass__` |
| Add or modify attributes at access time | Descriptor (`__get__` / `__set__`) |
| Add methods or class-level behaviour | Class decorator |
| Enforce abstract method implementation | `abc.ABC` + `@abstractmethod` |
| Validate the class definition on creation | Class decorator or `__init_subclass__` |
| **None of the above fit your case** | Custom metaclass (last resort) |

**Side-by-side comparison** — enforcing that a subclass provides a `validate()` method:

```python
# ── Metaclass version — complex ───────────────────────────────────
class ValidateMeta(type):
    def __new__(mcs, name, bases, ns):
        if bases and "validate" not in ns:
            raise TypeError(f"{name} must implement validate()")
        return super().__new__(mcs, name, bases, ns)

class Form(metaclass=ValidateMeta):
    pass

class UserForm(Form):
    def validate(self) -> bool:
        return True


# ── Class decorator version — same effect, much simpler ───────────
def requires_validate(cls):
    if "validate" not in cls.__dict__:
        raise TypeError(f"{cls.__name__} must implement validate()")
    return cls

@requires_validate
class UserForm:
    def validate(self) -> bool:
        return True


# ── __init_subclass__ version — composable and readable ──────────
class Form:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "validate" not in cls.__dict__:
            raise TypeError(f"{cls.__name__} must implement validate()")

class UserForm(Form):
    def validate(self) -> bool:
        return True
```

All three enforce the same rule. The metaclass version is the hardest to read and the hardest to compose with other metaclasses. Reach for it only when you need to intercept class creation before the class object exists — which is rare.

---

## Practice Exercises

1. Write a metaclass `UpperCaseMethods` that converts all method names defined in a class to lowercase automatically. Test it on a class with a `MyMethod` and a `DoSomething`.

2. Rewrite the plugin registry from Part 3 using `__init_subclass__` instead of a metaclass. Compare the two versions line-by-line.

3. Create an abstract base class `Serialisable` with abstract methods `to_json() -> str` and `from_json(data: str)`. Implement it in two concrete classes.

4. When would you choose a class decorator over `__init_subclass__`? Write one example of each doing the same job, and explain when each is the better choice.

---

## Next Lesson

This is the final lesson in Phase 17 — Advanced Python. You are now ready for the Phase 17 projects.

**[← Back to Phase 17 Overview](../README.md)**
