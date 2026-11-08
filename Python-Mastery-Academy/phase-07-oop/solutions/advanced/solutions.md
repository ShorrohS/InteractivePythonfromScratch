# Phase 07 — Advanced Solutions: OOP

---

## Q1. Full Inventory System

```python
from abc import ABC, abstractmethod
import uuid

class Item(ABC):
    def __init__(self, name: str, price: float, stock: int = 0):
        self.sku   = str(uuid.uuid4())[:8].upper()
        self.name  = name
        self._price = 0.0
        self.price  = price
        self.stock  = stock

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = round(float(value), 2)

    def apply_discount(self, pct: float) -> None:
        if not 0 <= pct <= 100:
            raise ValueError("pct must be 0–100")
        self._price = round(self._price * (1 - pct / 100), 2)

    @abstractmethod
    def category(self) -> str: ...

    @abstractmethod
    def display_price(self) -> str: ...

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Item) and self.sku == other.sku

    def __str__(self) -> str:
        return f"[{self.sku}] {self.name} — {self.display_price()} ({self.category()})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}, {self._price})"


class PhysicalItem(Item):
    def __init__(self, name, price, stock, weight_kg: float,
                 dimensions: tuple):
        super().__init__(name, price, stock)
        self.weight_kg  = weight_kg
        self.dimensions = dimensions   # (l, w, h) in cm


class DigitalItem(Item):
    def __init__(self, name, price, file_size_mb: float, fmt: str):
        super().__init__(name, price, stock=999)
        self.file_size_mb = file_size_mb
        self.format       = fmt


class Book(PhysicalItem):
    def __init__(self, title, author, isbn, price, stock=10,
                 weight_kg=0.4, dims=(21, 14, 2)):
        super().__init__(title, price, stock, weight_kg, dims)
        self.author, self.isbn = author, isbn
    def category(self)      -> str: return "Books"
    def display_price(self) -> str: return f"${self._price:.2f} (print)"


class Electronics(PhysicalItem):
    def __init__(self, name, brand, price, stock, warranty_months,
                 weight_kg=0.5, dims=(20, 15, 5)):
        super().__init__(name, price, stock, weight_kg, dims)
        self.brand, self.warranty_months = brand, warranty_months
    def category(self)      -> str: return "Electronics"
    def display_price(self) -> str:
        return f"${self._price:.2f} ({self.warranty_months}mo warranty)"


class EBook(DigitalItem):
    def __init__(self, title, author, isbn, price, size_mb=5):
        super().__init__(title, price, size_mb, "epub")
        self.author, self.isbn = author, isbn
    def category(self)      -> str: return "eBooks"
    def display_price(self) -> str: return f"${self._price:.2f} (digital)"


class SoftwareLicense(DigitalItem):
    def __init__(self, product_name, price, seats, size_mb=200):
        super().__init__(product_name, price, size_mb, "license")
        self.seats = seats
    def category(self)      -> str: return "Software"
    def display_price(self) -> str:
        return f"${self._price:.2f} ({self.seats} seats)"


class Inventory:
    def __init__(self):
        self._items: list = []

    def add(self, item: Item) -> None:
        self._items.append(item)

    def remove(self, sku: str) -> bool:
        before = len(self._items)
        self._items = [i for i in self._items if i.sku != sku]
        return len(self._items) < before

    def search(self, query: str) -> list:
        q = query.lower()
        return [i for i in self._items if q in i.name.lower()]

    def total_value(self) -> float:
        return sum(i.price * getattr(i, "stock", 0) for i in self._items)

    def by_category(self) -> dict:
        cats: dict = {}
        for i in self._items:
            cats.setdefault(i.category(), []).append(i)
        return cats

    def low_stock_report(self, threshold: int = 5) -> list:
        return [i for i in self._items
                if getattr(i, "stock", 999) <= threshold]


inv = Inventory()
inv.add(Book("Clean Code", "R. Martin", "978-0132350884", 39.99, stock=8))
inv.add(Electronics("Keyboard", "Logitech", 79.99, 12, 24))
inv.add(EBook("Fluent Python", "L. Ramalho", "978-1492056355", 29.99))
inv.add(SoftwareLicense("PyCharm Pro", 199.00, 5))
inv.add(Book("Refactoring", "R. Martin", "978-0134757599", 44.99, stock=3))

print(f"Total inventory value: ${inv.total_value():,.2f}")
for cat, items in inv.by_category().items():
    print(f"\n{cat}:")
    for item in items:
        print(f"  {item}")
print("\nLow stock (≤5):")
for item in inv.low_stock_report(5):
    print(f"  {item} — stock: {getattr(item,'stock','N/A')}")
```

---

## Q2. Comparable Sorted Container

```python
import bisect

class SortedList:
    """Generic sorted list using binary search for O(log n) insertion."""

    def __init__(self):
        self._items: list = []

    def add(self, item) -> None:
        bisect.insort(self._items, item)

    def remove(self, item) -> None:
        idx = bisect.bisect_left(self._items, item)
        if idx < len(self._items) and self._items[idx] == item:
            self._items.pop(idx)
        else:
            raise ValueError(f"{item!r} not in SortedList")

    def min(self):
        if not self._items: raise IndexError("min of empty SortedList")
        return self._items[0]

    def max(self):
        if not self._items: raise IndexError("max of empty SortedList")
        return self._items[-1]

    def median(self):
        n = len(self._items)
        if n == 0: raise IndexError("median of empty SortedList")
        return self._items[n // 2] if n % 2 else (
            self._items[n//2-1], self._items[n//2]
        )

    def __len__(self)          -> int:  return len(self._items)
    def __iter__(self):                 return iter(self._items)
    def __contains__(self, item) -> bool: return item in self._items
    def __getitem__(self, index):       return self._items[index]
    def __repr__(self) -> str:          return f"SortedList({self._items})"


import functools

@functools.total_ordering
class Person:
    def __init__(self, name: str, age: int):
        self.name, self.age = name, age
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Person) and self.age == other.age
    def __lt__(self, other: "Person") -> bool:
        return self.age < other.age
    def __repr__(self) -> str:
        return f"Person({self.name!r}, {self.age})"


people = SortedList()
for p in [Person("Alice",32), Person("Bob",25), Person("Carol",45),
          Person("Dave",19),  Person("Eve", 38)]:
    people.add(p)

print(f"Sorted: {list(people)}")
print(f"Youngest: {people.min()}")
print(f"Oldest:   {people.max()}")
print(f"Median:   {people.median()}")
```

---

## Q3. Descriptor Protocol

```python
class TypedField:
    """Data descriptor that enforces a specific type."""

    def __set_name__(self, owner, name: str) -> None:
        self.public_name  = name
        self.private_name = f"_{name}"

    def __init__(self, expected_type: type):
        self.expected_type = expected_type

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value) -> None:
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.public_name!r} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(obj, self.private_name, value)


class RangeField:
    """Data descriptor that enforces a numeric range."""

    def __set_name__(self, owner, name: str) -> None:
        self.public_name  = name
        self.private_name = f"_{name}"

    def __init__(self, min_val, max_val):
        self.min_val, self.max_val = min_val, max_val

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"{self.public_name!r} must be numeric, "
                f"got {type(value).__name__}"
            )
        if not self.min_val <= value <= self.max_val:
            raise ValueError(
                f"{self.public_name!r} must be between "
                f"{self.min_val} and {self.max_val}, got {value}"
            )
        setattr(obj, self.private_name, value)


class Product:
    name   = TypedField(str)
    price  = RangeField(0, 1_000_000)
    stock  = RangeField(0, 99_999)
    active = TypedField(bool)

    def __init__(self, name, price, stock, active=True):
        self.name   = name
        self.price  = price
        self.stock  = stock
        self.active = active

    def __repr__(self) -> str:
        return (f"Product({self.name!r}, ${self.price:.2f}, "
                f"stock={self.stock}, active={self.active})")


p = Product("Laptop", 999.99, 10)
print(p)

for bad, msg in [
    (lambda: Product(123, 10.0, 5),         "name type"),
    (lambda: Product("X", -1,   5),         "price range"),
    (lambda: Product("X", 10.0, 100_000),   "stock range"),
]:
    try:
        bad()
    except (TypeError, ValueError) as e:
        print(f"  {msg}: {e}")
```

---

## Q4. Mixin-Based Design

```python
import json
from datetime import datetime

class TimestampMixin:
    def __init_timestamp(self):
        if not hasattr(self, "created_at"):
            self.created_at = datetime.now().isoformat(timespec="seconds")
        self.updated_at = datetime.now().isoformat(timespec="seconds")

    def _ensure_timestamps(self):
        self.__init_timestamp()

    def touch(self):
        self.updated_at = datetime.now().isoformat(timespec="seconds")


class ValidateMixin:
    required_fields: list = []

    def validate(self) -> list:
        """Returns list of error messages (empty = valid)."""
        errors = []
        for field in self.required_fields:
            val = getattr(self, field, None)
            if not val:
                errors.append(f"{field!r} is required and cannot be empty")
        return errors


class JSONMixin:
    def to_json(self) -> str:
        return json.dumps(vars(self), indent=2, default=str)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        obj  = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj


class CSVMixin:
    @classmethod
    def headers(cls) -> list:
        # Returns the instance var names from the first object — or defined list
        return list(getattr(cls, "_csv_fields", []))

    def to_csv_row(self) -> str:
        fields = self.__class__.headers() or list(vars(self).keys())
        values = [str(getattr(self, f, "")) for f in fields]
        return ",".join(values)


class Article(TimestampMixin, ValidateMixin, JSONMixin, CSVMixin):
    required_fields = ["title", "author", "body"]
    _csv_fields     = ["title", "author", "created_at"]

    def __init__(self, title: str, author: str, body: str):
        self.title  = title
        self.author = author
        self.body   = body
        self._ensure_timestamps()

    def __repr__(self) -> str:
        return f"Article({self.title!r} by {self.author!r})"


class Comment(TimestampMixin, ValidateMixin):
    required_fields = ["text", "author"]

    def __init__(self, text: str, author: str):
        self.text   = text
        self.author = author
        self._ensure_timestamps()


a = Article("Python OOP Deep Dive", "Alice", "OOP in Python is powerful...")
print(a)
errors = a.validate()
print(f"Valid: {not errors}")
print(f"JSON:\n{a.to_json()}")
print(f"CSV row: {a.to_csv_row()}")

bad = Article("", "Bob", "")
print(f"Errors: {bad.validate()}")
```

---

## Q5. Observer Pattern

```python
from collections import defaultdict

class Observable:
    """Mixin — gives any class publish/subscribe capability."""

    def _get_subscribers(self) -> dict:
        if not hasattr(self, "_subscribers"):
            self._subscribers: dict = defaultdict(list)
        return self._subscribers

    def subscribe(self, event: str, callback) -> None:
        self._get_subscribers()[event].append(callback)

    def unsubscribe(self, event: str, callback) -> None:
        subs = self._get_subscribers()[event]
        if callback in subs:
            subs.remove(callback)

    def emit(self, event: str, **data) -> None:
        for cb in self._get_subscribers().get(event, []):
            cb(event=event, **data)


class EventLog:
    def __call__(self, event: str, **data) -> None:
        parts = " ".join(f"{k}={v}" for k, v in data.items())
        print(f"  [EVENT:{event}] {parts}")


class MetricsCollector:
    def __init__(self):
        self._counts: dict = defaultdict(int)

    def __call__(self, event: str, **data) -> None:
        self._counts[event] += 1

    def report(self) -> None:
        print("  Metrics:")
        for event, count in sorted(self._counts.items()):
            print(f"    {event}: {count} time(s)")


class BankAccount(Observable):
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner    = owner
        self._balance = float(balance)

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        self._balance += amount
        self.emit("deposit", amount=amount, balance=self._balance)

    def withdraw(self, amount: float) -> None:
        if amount > self._balance:
            self.emit("overdraft_attempt", amount=amount, balance=self._balance)
            return
        self._balance -= amount
        self.emit("withdraw", amount=amount, balance=self._balance)


log     = EventLog()
metrics = MetricsCollector()

acc = BankAccount("Alice", 1000)
acc.subscribe("deposit",          log)
acc.subscribe("deposit",          metrics)
acc.subscribe("withdraw",         log)
acc.subscribe("withdraw",         metrics)
acc.subscribe("overdraft_attempt", log)
acc.subscribe("overdraft_attempt", metrics)

acc.deposit(500)
acc.deposit(250)
acc.withdraw(300)
acc.withdraw(2000)   # overdraft attempt

print(f"\nFinal balance: ${acc.balance:,.2f}")
metrics.report()

# Unsubscribe and show log goes silent
acc.unsubscribe("deposit", log)
print("\nAfter unsubscribing log from 'deposit':")
acc.deposit(100)    # metrics still fires, log does not
metrics.report()
```
