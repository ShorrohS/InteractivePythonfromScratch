# Lesson 04 — Polymorphism

**Phase:** 07 — OOP | **Time:** ~25 min

---

## Part 1: What is Polymorphism?

Polymorphism means "many forms." In OOP it means the same method name works differently depending on the object type.

**Analogy:** The "speak" action means different things for a dog (bark), a cat (meow), and a parrot (speak words). Same action name, different behaviour.

---

## Part 2: Method Overriding

A child class provides its own implementation of a parent method:

```python
class Shape:
    def area(self) -> float:
        raise NotImplementedError("Subclass must implement area()")

    def describe(self) -> str:
        return f"I am a {self.__class__.__name__} with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width  = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base   = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height


# POLYMORPHISM IN ACTION — same code works for all shapes
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]

for shape in shapes:
    print(shape.describe())    # each calls ITS OWN area()
    # No if/elif needed!

total_area = sum(s.area() for s in shapes)
print(f"Total area: {total_area:.2f}")
```

---

## Part 3: Duck Typing

Python's "if it walks like a duck and quacks like a duck, it IS a duck." You don't need inheritance — just the same method name:

```python
class Dog:
    def speak(self) -> str:
        return "Woof!"

class Cat:
    def speak(self) -> str:
        return "Meow!"

class Parrot:
    def speak(self) -> str:
        return "Polly wants a cracker!"

class Robot:
    def speak(self) -> str:
        return "BEEP BOOP"

# Works for ANY object with a speak() method — no inheritance needed
def make_them_speak(speakers: list) -> None:
    for speaker in speakers:
        print(f"  {type(speaker).__name__}: {speaker.speak()}")

make_them_speak([Dog(), Cat(), Parrot(), Robot()])
```

---

## Part 4: Business Example — Payment Processing

```python
class PaymentProcessor:
    """Base processor."""
    def charge(self, amount: float) -> dict:
        raise NotImplementedError

    def refund(self, transaction_id: str) -> bool:
        raise NotImplementedError


class StripeProcessor(PaymentProcessor):
    def charge(self, amount: float) -> dict:
        print(f"  Charging ${amount:.2f} via Stripe...")
        return {"id": "stripe_txn_123", "status": "success", "amount": amount}

    def refund(self, transaction_id: str) -> bool:
        print(f"  Refunding {transaction_id} via Stripe...")
        return True


class PayPalProcessor(PaymentProcessor):
    def charge(self, amount: float) -> dict:
        print(f"  Charging ${amount:.2f} via PayPal...")
        return {"id": "pp_txn_456", "status": "success", "amount": amount}

    def refund(self, transaction_id: str) -> bool:
        print(f"  Refunding {transaction_id} via PayPal...")
        return True


def process_order(amount: float, processor: PaymentProcessor) -> None:
    """Works with ANY PaymentProcessor — polymorphism."""
    result = processor.charge(amount)
    if result["status"] == "success":
        print(f"  Payment successful: {result['id']}")
    else:
        print("  Payment failed!")

# Swap processors without changing process_order
process_order(99.99, StripeProcessor())
process_order(49.99, PayPalProcessor())
```

---

## Practice Exercises

1. Create `Animal → Dog/Cat/Bird` with `speak()` and `move()` methods overridden in each.

2. Create a `Notifier` base class with `send(message)`. Implement `EmailNotifier`, `SMSNotifier`, `SlackNotifier`.

3. Create a function `total_pay(employees)` that works for `FullTimeEmployee`, `HourlyEmployee`, `CommissionEmployee` — each with their own `calculate_pay()`.

---

## Next Lesson

**[Lesson 05 → Encapsulation & @property](lesson-05-encapsulation.md)**
