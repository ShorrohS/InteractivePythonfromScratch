# Phase 19 — Software Engineering Cheat Sheet

---

## SOLID at a Glance

| Letter | Principle | One-line definition |
|--------|-----------|---------------------|
| **S** | Single Responsibility | A class has exactly one reason to change |
| **O** | Open/Closed | Open for extension, closed for modification |
| **L** | Liskov Substitution | A subclass must be usable wherever its parent is expected |
| **I** | Interface Segregation | Clients should not be forced to implement methods they don't use |
| **D** | Dependency Inversion | Depend on abstractions, not on concrete implementations |

### S — Single Responsibility
```python
# Bad: one class does two things
class UserService:
    def save(self, user): ...        # persistence
    def send_welcome(self, user): ...  # email

# Good: separate responsibilities
class UserRepository:
    def save(self, user): ...

class WelcomeMailer:
    def send(self, user): ...
```

### O — Open/Closed
```python
# Bad: edit this function every time a new format is added
def export(data, fmt):
    if fmt == 'csv': ...
    elif fmt == 'json': ...

# Good: extend by adding a class, not editing existing code
class CsvExporter(Exporter):
    def export(self, data) -> str: ...

class JsonExporter(Exporter):
    def export(self, data) -> str: ...
```

### L — Liskov Substitution
```python
# Bad: ReadOnlyFile breaks File's write() contract
class File:
    def write(self, text): ...

class ReadOnlyFile(File):
    def write(self, text):
        raise PermissionError   # LSP violation

# Good: split at the capability boundary
class ReadableFile(ABC):
    def read(self) -> str: ...

class WritableFile(ReadableFile):
    def write(self, text) -> None: ...
```

### I — Interface Segregation
```python
# Bad: Robot is forced to implement eat() it doesn't need
class Worker(ABC):
    def work(self): ...
    def eat(self): ...   # robots don't eat

# Good: split interfaces
class Workable(ABC):
    def work(self): ...

class Feedable(ABC):
    def eat(self): ...
```

### D — Dependency Inversion
```python
# Bad: high-level module creates its own dependency
class ReportService:
    def __init__(self):
        self.db = MySQLDatabase()   # tightly coupled

# Good: depend on an abstraction, inject the concrete
class ReportService:
    def __init__(self, db: Database) -> None:
        self.db = db
```

---

## Design Patterns Quick Reference

### Factory
```python
class Animal(ABC):
    @abstractmethod
    def speak(self) -> str: ...

class Dog(Animal):
    def speak(self) -> str: return "Woof"

class AnimalFactory:
    _MAP = {'dog': Dog, 'cat': Cat}
    @classmethod
    def create(cls, kind: str) -> Animal:
        return cls._MAP[kind]()
```

### Singleton
```python
class Config:
    _instance: 'Config | None' = None

    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Observer
```python
class EventEmitter:
    def __init__(self):
        self._listeners: list = []

    def subscribe(self, fn): self._listeners.append(fn)
    def unsubscribe(self, fn): self._listeners.remove(fn)

    def emit(self, event, *args):
        for fn in self._listeners:
            fn(event, *args)
```

### Repository
```python
class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, uid: int) -> User: ...
    @abstractmethod
    def save(self, user: User) -> None: ...

class SqliteUserRepository(UserRepository):
    def find_by_id(self, uid: int) -> User:
        ...  # SQL lives here, nowhere else
```

### Strategy
```python
class Sorter:
    def __init__(self, strategy: Callable):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy(data)

# Usage:
sorter = Sorter(strategy=sorted)
sorter = Sorter(strategy=lambda d: sorted(d, reverse=True))
```

### Command
```python
class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...

class Editor:
    def __init__(self):
        self._history: list[Command] = []

    def do(self, cmd: Command) -> None:
        cmd.execute()
        self._history.append(cmd)

    def undo(self) -> None:
        if self._history:
            self._history.pop().undo()
```

---

## Clean Code Naming Rules

| Element | Convention | Example |
|---------|-----------|---------|
| Variables | `snake_case`, descriptive noun | `order_total`, `is_active` |
| Functions | `snake_case`, verb + noun | `calculate_tax()`, `send_email()` |
| Classes | `PascalCase`, noun | `OrderService`, `UserRepository` |
| Constants | `UPPER_SNAKE_CASE` | `TAX_RATE`, `MAX_RETRIES` |
| Private | leading underscore | `_cache`, `_notify_all()` |
| Booleans | `is_`, `has_`, `can_` prefix | `is_valid`, `has_permission` |

**Avoid:** single letters (except loop counters), abbreviations (`calc`, `proc`, `mgr`), generic names (`data`, `info`, `handler`, `manager`).

---

## Google-Style Docstring Format

```python
def calculate_discount(price: float, rate: float) -> float:
    """Apply a fractional discount rate to a price.

    Args:
        price: The original price in USD. Must be non-negative.
        rate:  The discount fraction between 0.0 and 1.0.
               A value of 0.2 represents a 20% discount.

    Returns:
        The discounted price as a float, rounded to 2 decimal places.

    Raises:
        ValueError: If rate is outside the range [0, 1].

    Example:
        >>> calculate_discount(100.0, 0.2)
        80.0
    """
    if not 0 <= rate <= 1:
        raise ValueError(f"rate must be between 0 and 1, got {rate}")
    return round(price * (1 - rate), 2)
```

---

## Type Hints Quick Reference

```python
from typing import (
    Any, Callable, Dict, List, Literal, Optional,
    Protocol, Tuple, Type, TypeVar, Union,
)
from typing import TypedDict  # structured dict
from collections.abc import Iterator, Generator, Sequence

# Basic
x: int = 5
name: str = "Alice"
items: list[str] = []
mapping: dict[str, int] = {}

# Optional (can be None)
def find(id: int) -> str | None: ...        # Python 3.10+
def find(id: int) -> Optional[str]: ...     # older style

# Callable
handler: Callable[[str, int], bool]

# TypeVar — generic functions
T = TypeVar('T')
def first(items: list[T]) -> T:
    return items[0]

# Protocol — structural subtyping (duck typing with type safety)
class Drawable(Protocol):
    def draw(self) -> None: ...

# Literal — restrict to specific values
def set_mode(mode: Literal['read', 'write', 'append']) -> None: ...

# TypedDict — typed dict shape
class Config(TypedDict):
    host: str
    port: int
    debug: bool
```

---

## `pyproject.toml` Minimal Template

```toml
[build-system]
requires      = ["hatchling"]
build-backend = "hatchling.build"

[project]
name            = "mypackage"
version         = "1.0.0"
description     = "Short description"
readme          = "README.md"
requires-python = ">=3.10"
license         = { text = "MIT" }

dependencies = [
    "requests>=2.31",
    "click>=8.1",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "ruff>=0.1",
    "mypy>=1.5",
]

[project.scripts]
mypackage = "mypackage.cli:main"

[project.urls]
Homepage   = "https://github.com/you/mypackage"
Repository = "https://github.com/you/mypackage"
```

Install with extras: `pip install mypackage[dev]`
Editable install: `pip install -e ".[dev]"`

---

## GitHub Actions Minimal CI Template

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}

      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy src/
      - run: pytest --cov=src --cov-report=xml
```

---

## pre-commit Config Template

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-merge-conflict
```

Install: `pip install pre-commit && pre-commit install`
Run manually: `pre-commit run --all-files`

---

## Code Review Checklist

**Correctness**
- [ ] Does the code do what the PR description says?
- [ ] Are edge cases handled (empty lists, None, zero, negative numbers)?
- [ ] Are error paths tested?

**Design**
- [ ] Does each class/function have a single responsibility?
- [ ] Are new dependencies injected rather than created internally?
- [ ] Is new behaviour added via extension, not modification?

**Readability**
- [ ] Are names descriptive and consistent with the codebase?
- [ ] Is nesting ≤ 2 levels? (If not, are guard clauses used?)
- [ ] Are magic numbers extracted to named constants?

**Documentation**
- [ ] Do public methods have docstrings?
- [ ] Are type hints present on parameters and return values?
- [ ] Is the commit message descriptive (`feat:`, `fix:`, `refactor:`)?

**Testing**
- [ ] Is new logic covered by unit tests?
- [ ] Do tests test behaviour, not implementation details?
- [ ] Can tests run without a database, network, or filesystem?

**Security**
- [ ] Are no secrets hardcoded? (Use environment variables or a secrets manager)
- [ ] Is user input validated before use?
- [ ] Are SQL queries parameterised (no string formatting into queries)?
