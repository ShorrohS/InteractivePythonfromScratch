"""
Demo 03 - Encapsulation
Phase 07: OOP

Run: python demo-03-encapsulation.py
"""

import math
from datetime import datetime

print("=" * 55)
print("DEMO 03 - Encapsulation")
print("=" * 55)

# --- 1. SINGLE vs DOUBLE UNDERSCORE ---
print("\n1. Name conventions — _ and __:")

class BankCard:
    def __init__(self, owner: str, number: str):
        self.owner    = owner           # public — anyone can read/write
        self._pin     = "0000"          # _single: private BY CONVENTION
        self.__number = number          # __double: name-mangled by Python

    def show_masked(self) -> str:
        # Inside the class __number works normally
        return f"{self.owner}: **** **** **** {self.__number[-4:]}"

card = BankCard("Alice", "1234567890123456")
print(f"  {card.show_masked()}")
print(f"  _pin (accessible but shouldn't be): {card._pin}")

try:
    print(card.__number)            # AttributeError: name-mangled
except AttributeError:
    print("  card.__number → AttributeError (name is mangled)")

# Python renames it to _ClassName__attr — still reachable if you must
print(f"  Actual name: {card._BankCard__number}")


# --- 2. @property (GETTER / SETTER) ---
print("\n2. @property — getter, setter, computed:")

class Temperature:
    def __init__(self, celsius: float):
        self._celsius = 0.0
        self.celsius  = celsius     # goes through the setter immediately

    @property
    def celsius(self) -> float:
        """Getter — runs when you READ .celsius"""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Setter — runs when you WRITE .celsius = x"""
        if not isinstance(value, (int, float)):
            raise TypeError("celsius must be a number")
        self._celsius = float(value)

    @property
    def fahrenheit(self) -> float:
        """Computed read-only property — no setter defined."""
        return self._celsius * 9 / 5 + 32

    @property
    def kelvin(self) -> float:
        return self._celsius + 273.15

t = Temperature(100)
print(f"  {t.celsius}°C = {t.fahrenheit}°F = {t.kelvin:.2f}K")
t.celsius = 0
print(f"  {t.celsius}°C = {t.fahrenheit}°F = {t.kelvin:.2f}K")

try:
    t.fahrenheit = 50       # no setter → AttributeError
except AttributeError:
    print("  fahrenheit is read-only (no setter defined)")

try:
    t.celsius = "hot"
except TypeError as e:
    print(f"  TypeError: {e}")


# --- 3. @classmethod AND @staticmethod ---
print("\n3. @classmethod and @staticmethod:")

class Date:
    def __init__(self, year: int, month: int, day: int):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_string(cls, date_str: str) -> "Date":
        """
        Alternative constructor — receives the CLASS as first arg (cls).
        Using cls instead of Date means subclasses inherit this correctly.
        """
        y, m, d = map(int, date_str.split("-"))
        return cls(y, m, d)

    @classmethod
    def today(cls) -> "Date":
        n = datetime.now()
        return cls(n.year, n.month, n.day)

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """
        Utility function — logically belongs with Date but needs
        no instance or class data.  Called as Date.is_leap_year(2024).
        """
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def __str__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

d1 = Date.from_string("2024-06-15")
d2 = Date.today()
print(f"  from_string: {d1}")
print(f"  today:       {d2}")
print(f"  2024 leap? {Date.is_leap_year(2024)} | 2023 leap? {Date.is_leap_year(2023)}")


# --- 4. FULL ENCAPSULATION PATTERN ---
print("\n4. Full encapsulation — read-only ID, validated salary, computed bonus:")

class Employee:
    _count = 0

    def __init__(self, emp_id: str, name: str, salary: float):
        self._emp_id = emp_id   # read-only: set once, no setter
        self._name   = name
        self._salary = 0.0
        self.salary  = salary   # through validated setter
        Employee._count += 1

    @property
    def emp_id(self) -> str:
        return self._emp_id     # no setter → read-only

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not str(value).strip():
            raise ValueError("name cannot be empty")
        self._name = value.strip()

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("salary must be numeric")
        if value < 0:
            raise ValueError("salary cannot be negative")
        self._salary = round(float(value), 2)

    @property
    def annual_bonus(self) -> float:
        """Computed — always 10% of current salary, never stored separately."""
        return round(self._salary * 0.10, 2)

    @classmethod
    def headcount(cls) -> int:
        return cls._count

    def __str__(self) -> str:
        return f"Employee({self._emp_id}, {self._name}, ${self._salary:,.2f})"

e1 = Employee("E001", "Alice", 85000)
e2 = Employee("E002", "Bob",   72000)
print(f"  {e1}  bonus=${e1.annual_bonus:,.2f}")
print(f"  {e2}  bonus=${e2.annual_bonus:,.2f}")
print(f"  Headcount: {Employee.headcount()}")

try:
    e1.emp_id = "HACK"      # AttributeError — no setter
except AttributeError:
    print("  emp_id is read-only — cannot be changed after init")

try:
    e1.salary = -1000
except ValueError as e:
    print(f"  ValueError: {e}")
