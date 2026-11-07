# ⚡ Phase 19 Cheat Sheet — Software Engineering

---

## SOLID Principles

```
S — Single Responsibility  One class/function = one job
O — Open/Closed            Extend without modifying
L — Liskov Substitution    Child is substitutable for parent
I — Interface Segregation  Small, focused interfaces
D — Dependency Inversion   Depend on abstractions, not implementations
```

---

## Design Patterns (Key Ones)

```python
# Factory — create objects via interface
class ShapeFactory:
    def create(self, kind: str) -> Shape:
        if kind == "circle": return Circle()
        if kind == "rect":   return Rectangle()

# Singleton — one instance
class Config:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

# Observer / Event
class EventBus:
    _subs: dict[str, list] = {}
    @classmethod
    def subscribe(cls, event, fn): ...
    @classmethod
    def publish(cls, event, data): ...

# Repository — abstract data access
class UserRepo(ABC):
    @abstractmethod
    def find(self, id): pass
    @abstractmethod
    def save(self, user): pass

# Strategy — swappable algorithm
class Sorter:
    def __init__(self, strategy): self.strategy = strategy
    def sort(self, data): return self.strategy(data)
```

---

## Clean Code Rules

```
1. Meaningful names
   BAD:  x, d, tmp, flag
   GOOD: employee_count, days_elapsed, is_active

2. Functions do ONE thing
   BAD:  def process_and_save_and_email()
   GOOD: def process() / def save() / def send_email()

3. Functions are SHORT (< 20 lines ideally)

4. Comments explain WHY, not WHAT
   BAD:  # increment i
   GOOD: # Start at 1 to skip header row

5. No magic numbers
   BAD:  if score >= 60:
   GOOD: PASSING_SCORE = 60 / if score >= PASSING_SCORE:

6. Don't Repeat Yourself (DRY)
   Extract repeated code into functions

7. Fail fast, fail clearly
   Validate inputs at the start of functions
```

---

## Logging

```python
import logging

# Setup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Use
logger.debug("Entering function with params: %s", params)
logger.info("User %d logged in", user_id)
logger.warning("Retry attempt %d/3", attempt)
logger.error("Payment failed: %s", error_msg)
logger.critical("Database unreachable!")

# With exception info
try:
    risky()
except Exception as e:
    logger.error("Failed", exc_info=True)
```

---

## Environment Variables

```python
import os
from dotenv import load_dotenv   # pip install python-dotenv

load_dotenv()   # reads .env file

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")
SECRET_KEY   = os.getenv("SECRET_KEY")
DEBUG        = os.getenv("DEBUG", "false").lower() == "true"

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set!")

# .env file (never commit):
# DATABASE_URL=postgresql://user:pass@localhost/prod
# SECRET_KEY=abc123verylongrandombytes
# DEBUG=false
```

---

## Project Structure

```
my-app/
├── .env                  ← secrets (gitignored)
├── .env.example          ← template (committed)
├── .gitignore
├── README.md
├── requirements.txt      ← production deps
├── requirements-dev.txt  ← dev + test deps
│
├── src/myapp/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py         ← Settings class
│   ├── models/
│   ├── services/         ← business logic
│   ├── repositories/     ← data access
│   └── utils/
│
└── tests/
    ├── conftest.py
    ├── unit/
    └── integration/
```

---

## Type Hints (Professional Standard)

```python
from typing import Optional, Union, Any
from collections.abc import Generator

def greet(name: str) -> str: ...
def maybe_int(x: str) -> int | None: ...
def process(items: list[dict[str, Any]]) -> None: ...

# Protocols (duck typing with hints)
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    obj.draw()   # works for ANY class with draw()
```
