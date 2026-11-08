# Phase 07 — Advanced Exercises: OOP

> These require combining multiple OOP concepts.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. Full Inventory System**

Build a complete inventory system using a proper OOP hierarchy:

```
Item (ABC)
├── PhysicalItem(weight_kg, dimensions)
│   ├── Book(title, author, isbn)
│   └── Electronics(brand, warranty_months)
└── DigitalItem(file_size_mb, format)
    ├── EBook(title, author, isbn)
    └── SoftwareLicense(product_name, seats)
```

Requirements:
- `Item` has abstract `category()` and `display_price()` methods; concrete `apply_discount(pct)` and `__str__`
- Each leaf class implements its own `category()` and `display_price()`
- `Inventory` class: `add(item)`, `remove(sku)`, `search(query)`, `total_value()`, `by_category()`, `low_stock_report(threshold=5)`
- All classes have `__repr__` and proper `__eq__` (by SKU)

---

**Q2. Comparable Sorted Container**

Build a generic `SortedList` class that keeps items in order automatically:
- Accepts any comparable type (int, float, custom objects with `__lt__`)
- `add(item)`, `remove(item)`, `__len__`, `__iter__`, `__contains__`, `__getitem__`
- `min()`, `max()`, `median()`, `__repr__`
- Uses binary search (`bisect` module) for O(log n) insertion
- Write a `Person(name, age)` with `__lt__` by age and demonstrate a `SortedList` of persons

---

**Q3. Descriptor Protocol**

Implement two descriptors:
- `TypedField(expected_type)` — a data descriptor that raises `TypeError` if the value is the wrong type
- `RangeField(min_val, max_val)` — raises `ValueError` if out of range

Use both in a `Product` class:
```python
class Product:
    name   = TypedField(str)
    price  = RangeField(0, 1_000_000)
    stock  = RangeField(0, 99_999)
    active = TypedField(bool)
```

A descriptor must implement `__set_name__`, `__get__`, and `__set__`.  
Demonstrate valid and invalid usage.

---

**Q4. Mixin-Based Design**

Build a flexible mixin system for a content management system:

```python
class JSONMixin:      # to_json(), from_json(cls, json_str)
class CSVMixin:       # to_csv_row(), headers (classmethod)
class ValidateMixin:  # validate() — checks required fields are not empty
class TimestampMixin: # created_at, updated_at auto-set; touch() updates updated_at
```

Use these to compose:
```python
class Article(TimestampMixin, ValidateMixin, JSONMixin, CSVMixin):
    required_fields = ["title", "author", "body"]
    ...
```

Show serialising to JSON, validating, and CSV export. Also build a `Comment` that uses only `TimestampMixin` and `ValidateMixin`.

---

**Q5. Observer Pattern**

Implement the Observer design pattern:
- `Observable` mixin — `subscribe(event, callback)`, `unsubscribe(event, callback)`, `emit(event, **data)`
- `EventLog` observer — prints `[EVENT] key=value ...` for every event
- `MetricsCollector` observer — counts events by name; `report()` shows counts

Apply it to a `BankAccount` class: `deposit` and `withdraw` emit events (`amount`, `balance`). Demonstrate subscribing/unsubscribing and showing the event log and metrics after a series of transactions.

---

> **Solutions:** `../../solutions/advanced/solutions.md`
