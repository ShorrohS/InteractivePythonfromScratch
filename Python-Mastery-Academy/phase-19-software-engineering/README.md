# 🏛️ Phase 19 — Professional Software Engineering

> **Goal:** Write code that professionals are proud to maintain.

---

## Why This Phase Matters

You can write code that works. This phase teaches you to write code that:
- Works correctly
- Is easy to read
- Is easy to change
- Is easy to test
- Is easy to deploy

These are the skills that get developers promoted.

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-solid.md](concepts/lesson-01-solid.md) | SOLID Principles |
| 02 | [lesson-02-design-patterns.md](concepts/lesson-02-design-patterns.md) | Design Patterns |
| 03 | [lesson-03-clean-code.md](concepts/lesson-03-clean-code.md) | Clean Code |
| 04 | [lesson-04-logging.md](concepts/lesson-04-logging.md) | Logging |
| 05 | [lesson-05-config.md](concepts/lesson-05-config.md) | Configuration Management |
| 06 | [lesson-06-structure.md](concepts/lesson-06-structure.md) | Project Structure |
| 07 | [lesson-07-documentation.md](concepts/lesson-07-documentation.md) | Documentation |
| 08 | [lesson-08-cicd.md](concepts/lesson-08-cicd.md) | CI/CD Basics |

---

## SOLID Principles Summary

```
S — Single Responsibility Principle
    Every class/function should have ONE job.
    
O — Open/Closed Principle
    Open for extension, closed for modification.
    Add new features without changing existing code.
    
L — Liskov Substitution Principle
    Child classes should be substitutable for parent classes.
    
I — Interface Segregation Principle
    Don't force classes to implement methods they don't use.
    
D — Dependency Inversion Principle
    Depend on abstractions, not implementations.
```

---

## Design Patterns (Key Ones)

```python
# FACTORY PATTERN
class PaymentProcessorFactory:
    @staticmethod
    def create(payment_type: str):
        if payment_type == "stripe":
            return StripeProcessor()
        elif payment_type == "paypal":
            return PayPalProcessor()
        raise ValueError(f"Unknown payment type: {payment_type}")

# SINGLETON PATTERN
class DatabaseConnection:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

# OBSERVER PATTERN
class EventBus:
    _subscribers: dict = {}
    
    @classmethod
    def subscribe(cls, event: str, handler):
        cls._subscribers.setdefault(event, []).append(handler)
    
    @classmethod
    def publish(cls, event: str, data=None):
        for handler in cls._subscribers.get(event, []):
            handler(data)

# REPOSITORY PATTERN
class UserRepository:
    def find_by_id(self, user_id: int): ...
    def find_all(self): ...
    def save(self, user): ...
    def delete(self, user_id: int): ...
```

---

## Logging Setup

```python
import logging
import logging.handlers
from pathlib import Path

def setup_logging(name: str, log_file: str = "app.log", level=logging.INFO):
    """Configure application logging."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10_000_000, backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging(__name__)
logger.info("Application started")
logger.warning("Low disk space")
logger.error("Database connection failed")
```

---

## Environment Variables

```python
# .env file (never commit to git!)
# DATABASE_URL=postgresql://user:pass@localhost/dbname
# SECRET_KEY=very-secret-key
# DEBUG=false

import os
from dotenv import load_dotenv    # pip install python-dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set!")
```

---

## Professional Project Structure

```
my-application/
├── .env                    # Secrets (NEVER commit)
├── .env.example            # Template (DO commit)
├── .gitignore
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── setup.py (or pyproject.toml)
│
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── user_service.py
│       ├── repositories/
│       │   ├── __init__.py
│       │   └── user_repository.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   └── integration/
│
├── docs/
│   ├── architecture.md
│   └── api.md
│
└── scripts/
    ├── setup.sh
    └── deploy.sh
```

---

## Clean Code Principles

```python
# ❌ BAD
def calc(a, b, c, d):
    return a * b * (1 - c) + d

# ✅ GOOD
def calculate_final_price(
    quantity: int,
    unit_price: float,
    discount_rate: float,
    shipping_fee: float
) -> float:
    """Calculate final order price including discount and shipping."""
    subtotal = quantity * unit_price
    discount_amount = subtotal * discount_rate
    return subtotal - discount_amount + shipping_fee

# ❌ BAD comments
# Multiply a by b
result = a * b

# ✅ GOOD comments  
# Apply 20% holiday discount for orders over $100
discount = base_price * 0.20 if base_price > 100 else 0

# ❌ BAD function (does too much)
def process():
    # validate input
    # calculate price
    # save to database
    # send email
    # generate report

# ✅ GOOD (Single Responsibility)
def validate_order(order): ...
def calculate_total(order): ...
def save_order(order): ...
def send_confirmation(order): ...
def generate_receipt(order): ...
```

---

## ✅ Completion Checklist

- [ ] Can explain all 5 SOLID principles with examples
- [ ] Know Factory, Singleton, Observer, Repository patterns
- [ ] Write self-documenting code with good names
- [ ] Configure logging properly in projects
- [ ] Use environment variables for configuration
- [ ] Follow professional project structure

---

## Previous: [Phase 18](../phase-18-business-projects/) | Next: [Phase 20](../phase-20-capstone/)
