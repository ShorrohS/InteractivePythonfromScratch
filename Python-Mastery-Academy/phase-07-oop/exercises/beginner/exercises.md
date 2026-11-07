# Phase 07 — Beginner Exercises: OOP

---

**Q1.** Create a `Dog` class with `name` and `breed` attributes and a `bark()` method. Create two dogs with different names.

---

**Q2.** Create a `Rectangle` class with `width` and `height`. Add methods: `area()`, `perimeter()`, `is_square()`.

---

**Q3.** What is the output?
```python
class Counter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1

c = Counter()
c.increment()
c.increment()
c.increment()
print(c.count)
```

---

**Q4.** Create a `Student` class with name and grades list. Add methods: `add_grade(score)`, `average()`, `highest()`, `lowest()`.

---

**Q5.** What is wrong?
```python
class Car:
    def __init__(name, speed):
        name = name
        speed = speed
```

---

**Q6.** Create a `Circle` class with a `radius` attribute. Add computed methods (not properties yet): `area()` and `circumference()` using `math.pi`.

---

**Q7.** Create a `BankAccount` class with `owner` and `balance`. Add: `deposit(amount)`, `withdraw(amount)` (no overdraft), `get_balance()`.

---

**Q8.** What does `__str__` do? Add one to the `BankAccount` class above.

---

**Q9.** Create a `Product` class and a `Cart` class. Cart has a `products` list and methods: `add(product)`, `total()`, `count()`.

---

**Q10.** Which OOP principle does `@property` support and why?

---

> **Solutions:** `../../solutions/beginner/solutions.md`
