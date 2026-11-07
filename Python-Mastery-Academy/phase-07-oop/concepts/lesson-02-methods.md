# Lesson 02 — Instance, Class, and Static Methods

**Phase:** 07 — OOP | **Time:** ~30 min

---

## Part 1: Three Types of Methods

```python
class Employee:

    company = "TechCorp"    # class attribute

    def __init__(self, name, salary):
        self.name   = name       # instance attribute
        self.salary = salary

    # INSTANCE METHOD — needs 'self', operates on instance data
    def get_info(self) -> str:
        return f"{self.name}: ${self.salary:,}"

    # CLASS METHOD — needs 'cls', operates on class-level data
    @classmethod
    def get_company(cls) -> str:
        return cls.company

    @classmethod
    def from_string(cls, data: str) -> "Employee":
        """Factory method: create Employee from 'name:salary' string."""
        name, salary = data.split(":")
        return cls(name.strip(), float(salary.strip()))

    # STATIC METHOD — no self or cls, utility function in namespace
    @staticmethod
    def validate_salary(salary: float) -> bool:
        return isinstance(salary, (int, float)) and salary >= 0
```

---

## Part 2: Instance Methods — Most Common

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        self.owner   = owner
        self._balance = balance    # underscore = private by convention

    def deposit(self, amount: float) -> None:
        """Modifies the instance."""
        self._balance += amount

    def withdraw(self, amount: float) -> bool:
        """Returns a value based on instance state."""
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def get_balance(self) -> float:
        """Read instance state."""
        return self._balance

    def __str__(self) -> str:
        return f"Account({self.owner}, ${self._balance:.2f})"
```

---

## Part 3: Class Methods — Factory Patterns

```python
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius

    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> "Temperature":
        """Create from Fahrenheit."""
        return cls((fahrenheit - 32) * 5/9)

    @classmethod
    def from_kelvin(cls, kelvin: float) -> "Temperature":
        """Create from Kelvin."""
        return cls(kelvin - 273.15)

    @property
    def celsius(self) -> float:
        return round(self._celsius, 2)

    @property
    def fahrenheit(self) -> float:
        return round(self._celsius * 9/5 + 32, 2)

# Usage — three ways to create the same object
t1 = Temperature(100)
t2 = Temperature.from_fahrenheit(212)
t3 = Temperature.from_kelvin(373.15)

print(t1.celsius, t2.celsius, t3.celsius)   # all 100
```

---

## Part 4: Static Methods — Utility Functions

```python
class DateUtils:
    """Utility class — no state needed."""

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @staticmethod
    def days_in_month(month: int, year: int) -> int:
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if month == 2 and DateUtils.is_leap_year(year):
            return 29
        return days[month - 1]

# No instance needed
print(DateUtils.is_leap_year(2024))       # True
print(DateUtils.days_in_month(2, 2024))   # 29
```

---

## Part 5: When to Use Each

| Method type | Use when |
|-------------|----------|
| Instance method | Need to read or modify `self` |
| Class method | Factory patterns, class-level operations |
| Static method | Utility function that logically belongs to the class |

---

## Practice Exercises

1. Add a `@classmethod create_from_csv_row(cls, row)` to an `Employee` class.

2. Add a `@staticmethod validate_email(email) -> bool` to a `User` class.

3. Write a `Counter` class with an instance method `increment()`, a class method `reset_all()`, and a static method `is_valid_count(n)`.

---

## Next Lesson

**[Lesson 04 → Polymorphism](lesson-04-polymorphism.md)**
