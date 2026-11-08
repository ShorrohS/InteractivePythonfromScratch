# Phase 07 — Intermediate Exercises: OOP

> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. Vehicle Hierarchy**

Build an inheritance hierarchy:
- `Vehicle(make, model, year)` — `describe()` returns `"YEAR MAKE MODEL"`; `start()` returns a generic message
- `Car(make, model, year, num_doors=4)` — override `start()` to mention the doors
- `ElectricCar(make, model, year, battery_kwh)` — override `start()` with a silent-start message; override `describe()` to add `(EV, Xkwh)` using `super()`
- `Truck(make, model, year, payload_kg)` — override `start()` with a heavy-engine message

Create one of each and call `describe()` and `start()` on them.

---

**Q2. Person and Employee with Properties**

Create:
- `Person(first_name, last_name, age)` with:
  - Read-only `full_name` property (computed)
  - `age` with a setter that rejects values outside 0–150
- `Employee(first_name, last_name, age, salary, department)` inheriting `Person` with:
  - `salary` setter rejecting negative values
  - Computed `monthly_salary` property
  - `get_summary()` method

---

**Q3. Date Class — @classmethod and @staticmethod**

Build a `Date(year, month, day)` class with:
- `@classmethod from_string(cls, s)` parsing `"YYYY-MM-DD"`
- `@classmethod today(cls)` using `datetime.now()`
- `@staticmethod is_valid(year, month, day)` returning `True`/`False`
- `@staticmethod is_leap_year(year)` returning `True`/`False`
- `days_until(other_date)` instance method (return integer, may be negative)
- `__str__` returning `"YYYY-MM-DD"`; `__repr__` for copy-paste

---

**Q4. Shape ABC**

Using `abc.ABC` and `@abstractmethod`:
- `Shape` — abstract `area()` and `perimeter()`; concrete `describe()` and `__str__`
- `Circle(radius)`, `Rectangle(width, height)`, `Square(side)` (inherits `Rectangle`), `Triangle(a, b, c)` (Heron's formula)

Create a list of mixed shapes; print all descriptions; print the shape with the largest area.

---

**Q5. Library with Composition**

Build with composition (NOT inheritance — a library is not a kind of book):
- `Book(title, author, isbn, pages)` — `__str__`, `__repr__`
- `Library(name)` — `add(book)`, `remove(isbn)`, `find_by_author(author)`, `find_by_title(keyword)`, `__len__`, `__iter__`, `__contains__`

Add 5 books to a library. Search by author. Iterate and print all titles.

---

**Q6. Vector with Operator Overloading**

Build a `Vector(x, y, z)` class with:
- `__add__`, `__sub__`, `__mul__` (scalar), `__rmul__`, `__neg__`
- `__eq__`, `__abs__` (magnitude — use `abs(v)`)
- `dot(other)` method
- `__str__` returning `"Vector(x, y, z)"`

Demonstrate: `v1 + v2`, `v1 - v2`, `v1 * 3`, `3 * v1`, `-v1`, `abs(v1)`, `v1.dot(v2)`.

---

**Q7. Animal Polymorphism**

Create a `Zoo` that holds `Animal` objects:
- `Animal(name, species)` — abstract `sound()` and `move()` methods
- `Lion`, `Eagle`, `Dolphin`, `Snake` — each with unique `sound()` and `move()` implementations
- `Zoo(name)` — `add_animal(a)`, `all_sounds()` prints every animal's sound, `count_by_type()` returns a dict of species → count

---

**Q8. Mixin Classes**

Define two mixins (no `__init__`, no instance state):
- `LogMixin` — adds `log(message)` that prints `[ClassName] message`
- `SerializeMixin` — adds `to_dict()` returning `vars(self)` and `from_dict(cls, d)` classmethod

Create a `User(username, email, role)` class that mixes in both. Show logging and serialisation working.

---

**Q9. Stack with Container Dunders**

Build a generic `Stack` class with:
- `push(item)`, `pop()`, `peek()`
- `__len__`, `__bool__` (empty stack is falsy), `__iter__` (top-to-bottom)
- `__contains__`, `__repr__`

Demonstrate pushing 5 items, iterating, `in` checks, `bool()`, and `pop()`.

---

**Q10. Cached Property Pattern**

Build a `DataSet(numbers: list)` class where:
- `mean`, `median`, `std_dev` are **computed once and cached** — not recomputed on every access
- Implement the cache manually using a `_cache` dict (no `functools.cached_property`)
- Add an `invalidate_cache()` method
- Add `add(number)` which adds to the dataset AND invalidates the cache

Show the cache working by printing "computing..." only on first access.

---

> **Solutions:** `../../solutions/intermediate/solutions.md`
