# Lesson 06 — Type Hints

**Phase:** 17 — Advanced Python | **Time:** ~40 min

---

## Part 1: Why Type Hints Matter

Python is dynamically typed — variables have no declared type. Type hints are optional annotations that describe what types a function expects and returns.

**Three key benefits:**

1. **IDE autocomplete** — your editor knows what methods are available on a value, so suggestions are accurate
2. **Early error detection** — static analysers catch bugs before you run the code
3. **Self-documenting signatures** — a reader understands a function without reading its body

```
Without hints:   def process(data, threshold):
                     → What types? What does it return? Unknown without reading the body.

With hints:      def process(data: list[float], threshold: float) -> list[float]:
                     → Crystal clear from the signature alone.
```

Type hints are checked by tools like **mypy** at development time, not at runtime. Python itself still runs the code regardless — hints are never enforced by the interpreter.

---

## Part 2: Basic Annotations

```python
# ── Variable annotations ──────────────────────────────────────────
name: str = "Alice"           # must be a string
age: int = 30                 # must be an integer
score: float = 98.5           # must be a float
active: bool = True           # must be a boolean

# You can annotate without assigning (declares intent, no value yet)
total: float

# ── Function annotations ──────────────────────────────────────────
def greet(name: str, greeting: str = "Hello") -> str:
    """Return a formatted greeting string."""
    return f"{greeting}, {name}!"

# -> None means the function returns nothing useful
def log_event(message: str, level: str = "INFO") -> None:
    print(f"[{level}] {message}")

# Calling with wrong types still works at runtime —
# but mypy catches it statically before you run anything:
greet("Alice")           # fine
greet(42)                # mypy: Argument 1 has incompatible type "int"; expected "str"
```

---

## Part 3: Container Types

Python 3.9+ lets you use built-in collection types directly as annotations:

```python
# Python 3.9+ syntax (preferred)
def average(numbers: list[int]) -> float:
    return sum(numbers) / len(numbers)

def count_words(text: str) -> dict[str, int]:
    """Count occurrences of each word."""
    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts

def rgb_to_hex(color: tuple[int, int, int]) -> str:
    """Convert (r, g, b) to a hex colour string."""
    return "#{:02X}{:02X}{:02X}".format(*color)

def unique_tags(items: list[str]) -> set[str]:
    return set(items)

# ── Older style for Python 3.8 and below (typing module) ─────────
from typing import List, Dict, Tuple, Set

def old_style(items: List[int]) -> Dict[str, int]:
    ...   # works in 3.8, prefer the lowercase form in 3.9+
```

**Optional and Union:**

```python
from typing import Optional, Union

# Optional[str] means the value can be str OR None
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)         # returns None if not found

# Union[str, int] means the value can be str OR int
def parse_id(value: Union[str, int]) -> int:
    return int(value)

# ── Python 3.10+ shorthand with the | operator ────────────────────
def find_user_modern(user_id: int) -> str | None:     # same as Optional[str]
    ...

def parse_id_modern(value: str | int) -> int:         # same as Union[str, int]
    return int(value)
```

---

## Part 4: Advanced Types

### TypedDict — typed dictionary structures

```python
from typing import TypedDict

class Employee(TypedDict):
    """A typed dict describing a single employee record."""
    id: int
    name: str
    department: str
    salary: float
    active: bool

# mypy verifies both the keys and value types
employee: Employee = {
    "id": 1,
    "name": "Alice",
    "department": "Engineering",
    "salary": 95000.0,
    "active": True,
}

# mypy catches wrong types and missing/extra keys
bad: Employee = {"id": "not-an-int", "name": "Alice"}   # two errors flagged
```

### Protocol — structural subtyping (duck typing with safety)

```python
from typing import Protocol

class Drawable(Protocol):
    """Any object that has a draw() method satisfies this protocol."""
    def draw(self) -> None:
        ...

class Circle:
    def draw(self) -> None:
        print("Drawing a circle")

class Square:
    def draw(self) -> None:
        print("Drawing a square")

# Both Circle and Square satisfy Drawable — no inheritance needed
def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())   # works — Circle has draw()
render(Square())   # works — Square has draw()
```

### TypeVar — generic functions

```python
from typing import TypeVar

T = TypeVar("T")   # T represents any consistent type

def first(items: list[T]) -> T:
    """Return the first element, preserving its exact type."""
    return items[0]

result: int = first([1, 2, 3])           # T inferred as int
name: str   = first(["Alice", "Bob"])    # T inferred as str
```

### Callable — function type hints

```python
from typing import Callable

# Callable[[arg_types, ...], return_type]
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    """Apply a two-argument integer function to a and b."""
    return func(a, b)

apply(lambda x, y: x + y, 3, 5)   # 8
apply(max, 10, 20)                  # 20
```

---

## Part 5: Running mypy

**Install and run:**

```bash
pip install mypy
mypy app.py         # check a single file
mypy src/           # check an entire package
```

**Common mypy errors and fixes:**

```
error: Argument 1 to "greet" has incompatible type "int"; expected "str"
    → You passed the wrong type. Fix the call site or broaden the annotation.

error: Item "None" of "str | None" has no attribute "upper"
    → You called a method on something that could be None.
    → Fix: add a None check — if value is not None: value.upper()

error: Incompatible return value type (got "int", expected "str")
    → Your function returns a different type than its -> annotation says.
```

**Configure mypy in pyproject.toml:**

```toml
[tool.mypy]
python_version = "3.11"
strict = true                   # enables all strict checks (recommended for new projects)
ignore_missing_imports = true   # don't error on untyped third-party libraries
```

---

## Part 6: Complete Example

A fully type-annotated service class using `TypedDict`, `Optional`, and `list[Employee]`:

```python
from typing import Optional, TypedDict

class Employee(TypedDict):
    id: int
    name: str
    department: str
    salary: float
    active: bool

class EmployeeService:
    """Manages a collection of employees with full type annotations."""

    def __init__(self) -> None:
        self._employees: list[Employee] = []   # typed list of employee records
        self._next_id: int = 1

    def add_employee(
        self, name: str, department: str, salary: float
    ) -> Employee:
        """Create, store, and return a new employee record."""
        employee: Employee = {
            "id":         self._next_id,
            "name":       name,
            "department": department,
            "salary":     salary,
            "active":     True,
        }
        self._employees.append(employee)
        self._next_id += 1
        return employee

    def find_by_name(self, name: str) -> Optional[Employee]:
        """Return the first employee matching the name, or None."""
        for emp in self._employees:
            if emp["name"].lower() == name.lower():
                return emp
        return None

    def get_department(self, department: str) -> list[Employee]:
        """Return all active employees in the given department."""
        return [
            emp for emp in self._employees
            if emp["department"] == department and emp["active"]
        ]

    def give_raise(self, employee_id: int, amount: float) -> bool:
        """Apply a salary raise. Returns True if the employee was found."""
        for emp in self._employees:
            if emp["id"] == employee_id:
                emp["salary"] += amount
                return True
        return False

    def headcount(self) -> dict[str, int]:
        """Return the number of active employees per department."""
        counts: dict[str, int] = {}
        for emp in self._employees:
            if emp["active"]:
                dept = emp["department"]
                counts[dept] = counts.get(dept, 0) + 1
        return counts


# ── Usage ─────────────────────────────────────────────────────────
service = EmployeeService()
service.add_employee("Alice", "Engineering", 95000.0)
service.add_employee("Bob",   "Engineering", 88000.0)
service.add_employee("Carol", "Marketing",   75000.0)

alice = service.find_by_name("Alice")
if alice is not None:          # None check required — mypy will flag the omission
    print(alice["name"])       # Alice
    service.give_raise(alice["id"], 5000.0)

print(service.headcount())     # {'Engineering': 2, 'Marketing': 1}
```

---

## Practice Exercises

1. Annotate a function `merge_dicts(a, b)` so mypy knows both dicts have `str` keys and `int` values, and the return value does too.

2. Create a `Protocol` called `Serialisable` with a `to_json() -> str` method. Write two classes that satisfy it without inheriting from it.

3. Write a generic function `last(items: list[T]) -> T` that returns the last element and preserves its type.

4. Run mypy on a file that has a missing `None` check. Read the error, add the guard, and confirm the error disappears.

---

## Next Lesson

**[Lesson 07 → Functional Programming](lesson-07-functional-programming.md)**
