# Lesson 02 — Design Patterns

**Phase:** 19 — Software Engineering | **Time:** ~45 min

---

## What are Design Patterns?

Design patterns are proven, reusable solutions to commonly occurring software design problems. They are templates — not code — that you adapt to your situation.

Three categories:
- **Creational** — how objects are created
- **Structural** — how classes/objects are composed
- **Behavioral** — how objects communicate

---

## Pattern 1: Singleton

**Problem:** Ensure only ONE instance of a class ever exists.
**Use case:** Database connection pool, configuration manager, logger.

```python
class DatabasePool:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connections = []
            print("  Database pool created (once)")
        return cls._instance

    def get_connection(self):
        return "connection"

# Both variables point to the SAME object
pool1 = DatabasePool()
pool2 = DatabasePool()
print(pool1 is pool2)   # True

# More Pythonic: use a module
# config.py — module-level variables are already singletons
```

---

## Pattern 2: Factory

**Problem:** Create objects without specifying the exact class.
**Use case:** Creating different database adapters, payment processors, report formats.

```python
from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> bool: pass

class EmailNotification(Notification):
    def send(self, message: str) -> bool:
        print(f"  EMAIL: {message}")
        return True

class SMSNotification(Notification):
    def send(self, message: str) -> bool:
        print(f"  SMS: {message}")
        return True

class SlackNotification(Notification):
    def send(self, message: str) -> bool:
        print(f"  SLACK: {message}")
        return True

class NotificationFactory:
    _registry: dict[str, type] = {
        "email": EmailNotification,
        "sms":   SMSNotification,
        "slack": SlackNotification,
    }

    @classmethod
    def create(cls, channel: str) -> Notification:
        if channel not in cls._registry:
            raise ValueError(f"Unknown channel: {channel}")
        return cls._registry[channel]()

    @classmethod
    def register(cls, name: str, klass: type) -> None:
        cls._registry[name] = klass

# Usage
notifier = NotificationFactory.create("email")
notifier.send("System maintenance at 2am")
```

---

## Pattern 3: Observer

**Problem:** When one object changes, notify multiple dependents automatically.
**Use case:** Event systems, real-time dashboards, pub/sub.

```python
from abc import ABC, abstractmethod

class EventBus:
    """Simple observer/event system."""
    _subscribers: dict[str, list] = {}

    @classmethod
    def subscribe(cls, event: str, handler) -> None:
        if event not in cls._subscribers:
            cls._subscribers[event] = []
        cls._subscribers[event].append(handler)

    @classmethod
    def publish(cls, event: str, data=None) -> None:
        for handler in cls._subscribers.get(event, []):
            handler(data)

# Usage
def send_welcome_email(user):
    print(f"  Email: Welcome, {user['name']}!")

def create_user_profile(user):
    print(f"  Profile: Creating for {user['name']}")

def log_registration(user):
    print(f"  Log: User {user['id']} registered")

EventBus.subscribe("user.registered", send_welcome_email)
EventBus.subscribe("user.registered", create_user_profile)
EventBus.subscribe("user.registered", log_registration)

# Fire the event
new_user = {"id": 42, "name": "Alice"}
EventBus.publish("user.registered", new_user)
# All three handlers run automatically
```

---

## Pattern 4: Repository

**Problem:** Separate data access logic from business logic.
**Use case:** Database abstraction, testability.

```python
from abc import ABC, abstractmethod
from typing import Optional

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[dict]: pass

    @abstractmethod
    def find_all(self) -> list[dict]: pass

    @abstractmethod
    def save(self, user: dict) -> dict: pass

    @abstractmethod
    def delete(self, user_id: int) -> bool: pass


class InMemoryUserRepository(UserRepository):
    """For testing — no database needed."""

    def __init__(self):
        self._db: dict[int, dict] = {}
        self._counter = 0

    def find_by_id(self, user_id: int):
        return self._db.get(user_id)

    def find_all(self):
        return list(self._db.values())

    def save(self, user: dict):
        if "id" not in user:
            self._counter += 1
            user["id"] = self._counter
        self._db[user["id"]] = user
        return user

    def delete(self, user_id: int):
        return self._db.pop(user_id, None) is not None


class SQLiteUserRepository(UserRepository):
    """Production implementation."""

    def __init__(self, db_path: str):
        import sqlite3
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def find_by_id(self, user_id: int):
        row = self.conn.execute(
            "SELECT * FROM users WHERE id=?", (user_id,)
        ).fetchone()
        return dict(row) if row else None

    def find_all(self):
        return [dict(r) for r in self.conn.execute("SELECT * FROM users").fetchall()]

    def save(self, user: dict):
        ...  # SQLite implementation

    def delete(self, user_id: int):
        ...  # SQLite implementation


# Business logic depends on abstraction, not implementation
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, name: str, email: str) -> dict:
        user = {"name": name, "email": email}
        return self.repo.save(user)

# Swap implementations without changing UserService
test_service = UserService(InMemoryUserRepository())
prod_service = UserService(SQLiteUserRepository("prod.db"))
```

---

## Pattern 5: Strategy

**Problem:** Select an algorithm at runtime without changing the client code.
**Use case:** Sorting strategies, pricing rules, data export formats.

```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: pass

class BubbleSort(SortStrategy):
    def sort(self, data): ...   # O(n²)

class QuickSort(SortStrategy):
    def sort(self, data):
        return sorted(data)     # O(n log n)

class DataProcessor:
    def __init__(self, strategy: SortStrategy = None):
        self.strategy = strategy or QuickSort()

    def set_strategy(self, strategy: SortStrategy) -> None:
        self.strategy = strategy

    def process(self, data: list) -> list:
        return self.strategy.sort(data)
```

---

## Interview Questions

1. What is the difference between a design pattern and an algorithm?
2. Which patterns are most commonly used in Python web development?
3. Give an example where you would use Factory over Singleton.
4. How does the Repository pattern improve testability?
