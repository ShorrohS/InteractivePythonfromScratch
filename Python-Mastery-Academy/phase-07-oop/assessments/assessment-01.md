# Phase 07 — Completion Assessment

> Pass mark: 80% | Time: 35 minutes

---

## PART A: Design and Code

**Task 1.** Design and implement a `Vehicle` hierarchy:
- `Vehicle(ABC)` with abstract `start()`, `fuel_type` property
- `ElectricCar` — battery_kwh, silent start
- `GasCar` — engine_size, loud start
- Add `@property` for `range_km` to each (different formula)
- Add `__str__` to each

---

**Task 2.** Create a `BankAccount` class with:
- `balance` property with validation (no negatives)
- `deposit(amount)` and `withdraw(amount)` with custom exceptions
- `__str__` showing owner and balance
- A `SavingsAccount` subclass with `minimum_balance` that blocks withdrawals below it

---

**Task 3.** Build a `Playlist` class demonstrating the container protocol:
- `__len__`, `__iter__`, `__contains__`, `__getitem__`
- `__str__` and `__repr__`
- Add/remove songs
- Demonstrate: `len(p)`, `"song" in p`, `p[0]`, `for song in p`

---

## PART B: Predict the Output

**Q4.**
```python
class Animal:
    def speak(self): return "..."
class Dog(Animal):
    def speak(self): return "Woof"
class Cat(Animal):
    def speak(self): return "Meow"

animals = [Dog(), Cat(), Animal()]
for a in animals:
    print(a.speak())
```

**Q5.**
```python
class Counter:
    count = 0
    def __init__(self):
        Counter.count += 1

c1 = Counter()
c2 = Counter()
c3 = Counter()
print(Counter.count)
print(c1.count)
```

---

## PART C: Design Questions

**Q6.** When would you use composition instead of inheritance? Give an example.

**Q7.** What is the Liskov Substitution Principle and why does it matter?

---

## Answers

**Q4:** `Woof / Meow / ...`

**Q5:** `3 / 3` — count is a class attribute, shared and mutated by all instances

**Q6 example:** A `Car` has an `Engine` (composition) rather than IS an Engine (which would be wrong inheritance). Use composition when the relationship is "has a" rather than "is a". Also prefer composition when you need to swap implementations at runtime.

**Q7:** Liskov Substitution Principle: a child class must be usable wherever the parent class is expected, without breaking the program. Example: if `SavingsAccount` extends `BankAccount`, any code that accepts `BankAccount` must work correctly with `SavingsAccount`. Violating LSP means your inheritance is wrong — composition might be better.
