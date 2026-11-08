# Lesson 05 — ORM Basics with SQLAlchemy

**Phase:** 09 — Databases | **Time:** ~60 min

---

## Part 1: What is an ORM?

An **ORM** (Object-Relational Mapper) maps Python classes to database tables. Each class becomes a table, each instance becomes a row, each attribute becomes a column.

```
Python class           →   database table
class Product          →   CREATE TABLE products (...)
Product(name="Laptop") →   INSERT INTO products VALUES (...)
session.query(Product) →   SELECT * FROM products
```

SQLAlchemy is the most widely used ORM in Python. It supports SQLite, PostgreSQL, MySQL, and more with the same Python API — swap the connection string and the rest of your code stays the same.

---

## Part 2: Raw SQL vs ORM — Trade-offs

| Concern | Raw sqlite3 | SQLAlchemy ORM |
|---------|-------------|----------------|
| Boilerplate | High — manual SQL strings | Low — Python syntax |
| Python objects | Manual dict conversion | Native class instances |
| Database portability | SQLite-specific SQL | Swap engine string to switch DB |
| Full SQL control | Complete | Limited for complex queries |
| Learning curve | Low — SQL knowledge | Medium — ORM patterns |
| Performance | Slightly faster | Small overhead from abstraction |

**Use raw SQL** when you need fine-grained control, complex queries, or maximum performance.
**Use an ORM** for standard CRUD, rapid development, and apps that may switch databases.

---

## Part 3: Installation

```bash
pip install sqlalchemy
```

Verify the installation:

```python
import sqlalchemy
print(sqlalchemy.__version__)   # e.g. 2.0.30
```

This lesson uses **SQLAlchemy 2.0** (the current API). Older tutorials may show 1.x patterns — the differences are mainly in how sessions and queries are written.

---

## Part 4: Defining Models

```python
from sqlalchemy import (
    create_engine, Column, Integer, String,
    Float, Boolean, DateTime
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime

# Base class — every model must inherit from this
class Base(DeclarativeBase):
    pass

class Product(Base):
    """Maps to the 'products' table in the database."""

    __tablename__ = "products"

    # Primary key — auto-increments by default with SQLite
    id          = Column(Integer, primary_key=True)

    # String columns — nullable=False enforces NOT NULL
    name        = Column(String(100), nullable=False)
    sku         = Column(String(20),  nullable=False, unique=True)
    category    = Column(String(50),  nullable=True)

    # Numeric columns
    price       = Column(Float,   nullable=False)
    quantity    = Column(Integer, nullable=False, default=0)

    # Boolean and timestamp
    active      = Column(Boolean,  default=True)
    created_at  = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Product id={self.id} sku='{self.sku}' name='{self.name}'>"

    def __str__(self) -> str:
        return f"[{self.sku}] {self.name} — ${self.price:.2f} ({self.quantity} in stock)"
```

---

## Part 5: Creating the Engine and Tables

```python
# SQLite file database
engine = create_engine("sqlite:///inventory.db", echo=False)
# echo=True prints every generated SQL statement — very useful for debugging

# Other database examples (same code works for all):
# engine = create_engine("postgresql://user:password@localhost/mydb")
# engine = create_engine("mysql+pymysql://user:password@localhost/mydb")

# Create all tables defined in models that inherit from Base
Base.metadata.create_all(engine)
# Safe to call repeatedly — only creates tables that do not yet exist
```

---

## Part 6: Session Management

The session is SQLAlchemy's unit of work. All reads and writes go through it. Changes are buffered in memory until `commit()` flushes them to the database.

```python
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Factory — call SessionLocal() to get a new session
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_session():
    """Yield a database session; commit on success, rollback on exception."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
with get_session() as session:
    session.add(Product(name="Laptop", sku="LAP-001", price=999.99, quantity=50))
# commit() is called automatically when the with block exits cleanly
```

---

## Part 7: CRUD with SQLAlchemy

```python
from typing import Optional

# CREATE — add a new product
def add_product(name: str, sku: str, price: float, quantity: int) -> int:
    """
    Insert a product and return its new auto-generated id.
    """
    with get_session() as session:
        product = Product(name=name, sku=sku, price=price, quantity=quantity)
        session.add(product)
        session.flush()   # Sends INSERT so the id is populated before commit
        return product.id

# READ — get by primary key
def get_product(product_id: int) -> Optional[Product]:
    """Return a Product object or None if not found."""
    with get_session() as session:
        return session.get(Product, product_id)

# READ — get all active products
def get_all_products() -> list[Product]:
    """Return all active products ordered by name."""
    with get_session() as session:
        return (
            session.query(Product)
            .filter_by(active=True)
            .order_by(Product.name)
            .all()
        )

# UPDATE — fetch, modify, commit
def update_price(product_id: int, new_price: float) -> bool:
    """
    Update a product's price.

    Returns:
        True if the product was found and updated, False otherwise.
    """
    with get_session() as session:
        product = session.get(Product, product_id)
        if product is None:
            return False
        product.price = new_price
        return True   # session.commit() runs automatically via context manager

# DELETE — remove from session then commit
def delete_product(product_id: int) -> bool:
    """
    Hard-delete a product row.

    Returns:
        True if found and deleted, False otherwise.
    """
    with get_session() as session:
        product = session.get(Product, product_id)
        if product is None:
            return False
        session.delete(product)
        return True
```

---

## Part 8: Filtering and Querying

```python
def search_by_category(category: str) -> list[Product]:
    """Return all active products in a category, ordered by name."""
    with get_session() as session:
        return (
            session.query(Product)
            .filter(Product.category == category, Product.active == True)
            .order_by(Product.name)
            .all()
        )

def get_low_stock(threshold: int = 10) -> list[Product]:
    """Return active products below the reorder threshold."""
    with get_session() as session:
        return (
            session.query(Product)
            .filter(Product.quantity < threshold, Product.active == True)
            .order_by(Product.quantity)
            .all()
        )

def count_by_category(category: str) -> int:
    """Count active products in a category."""
    with get_session() as session:
        return (
            session.query(Product)
            .filter(Product.category == category, Product.active == True)
            .count()
        )

def get_products_in_price_range(low: float, high: float) -> list[Product]:
    """Return products priced between low and high, inclusive."""
    with get_session() as session:
        return (
            session.query(Product)
            .filter(Product.price >= low, Product.price <= high)
            .order_by(Product.price)
            .all()
        )
```

**filter_by** accepts keyword arguments for simple equality: `.filter_by(active=True)`.
**filter** accepts column expressions for any operator: `.filter(Product.price > 50)`. Use `filter` when you need anything beyond equality.

---

## Part 9: Introduction to Relationships

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"

    id       = Column(Integer, primary_key=True)
    name     = Column(String(50), nullable=False, unique=True)

    # Back-reference — Category.items returns the related Product objects
    items    = relationship("InventoryItem", back_populates="category")

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id          = Column(Integer, primary_key=True)
    name        = Column(String(100), nullable=False)
    price       = Column(Float,       nullable=False)
    quantity    = Column(Integer,     default=0)

    # Foreign key — links to categories.id
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Relationship — item.category returns the related Category object
    category    = relationship("Category", back_populates="items")

# Usage
with get_session() as session:
    cat = Category(name="Electronics")
    session.add(cat)
    session.flush()   # cat.id is now available

    item = InventoryItem(name="Laptop", price=999.99, quantity=25, category_id=cat.id)
    session.add(item)
# Both rows are committed together
```

Relationships let you navigate between related objects (`item.category.name`) without writing JOIN queries manually.

---

## Part 10: Same Operation — Raw sqlite3 vs SQLAlchemy

```python
# ── INSERT ─────────────────────────────────────────────────────────────────
# Raw sqlite3:
conn.execute(
    "INSERT INTO products (name, sku, price) VALUES (?, ?, ?)",
    ("Laptop", "LAP-001", 999.99)
)

# SQLAlchemy:
session.add(Product(name="Laptop", sku="LAP-001", price=999.99))
session.commit()

# ── SELECT one row ──────────────────────────────────────────────────────────
# Raw sqlite3:
cur = conn.execute("SELECT * FROM products WHERE id = ?", (1,))
row = dict(cur.fetchone())

# SQLAlchemy:
product = session.get(Product, 1)

# ── UPDATE ──────────────────────────────────────────────────────────────────
# Raw sqlite3:
conn.execute("UPDATE products SET price = ? WHERE id = ?", (1099.99, 1))

# SQLAlchemy:
product = session.get(Product, 1)
product.price = 1099.99
session.commit()

# ── DELETE ──────────────────────────────────────────────────────────────────
# Raw sqlite3:
conn.execute("DELETE FROM products WHERE id = ?", (1,))

# SQLAlchemy:
product = session.get(Product, 1)
session.delete(product)
session.commit()

# ── SELECT with filter ──────────────────────────────────────────────────────
# Raw sqlite3:
cur  = conn.execute("SELECT * FROM products WHERE price < ?", (100,))
rows = [dict(r) for r in cur.fetchall()]

# SQLAlchemy:
products = session.query(Product).filter(Product.price < 100).all()
```

---

## Practice Exercises

1. Add an `update_quantity(product_id: int, delta: int) -> bool` function that increments or decrements quantity by `delta` (e.g., `-5` for a sale, `+20` for a restock). Fetch the object, modify in Python, then commit.

2. Add a `deactivate_product(product_id: int) -> bool` function that sets `active = False` — a soft delete that keeps the row in the database.

3. Create a `Supplier` model with columns `id`, `name`, `email`, and `country`. Add a `supplier_id` ForeignKey to the `Product` model and set up the `relationship` on both sides.

4. Write a `get_inventory_value() -> float` function that returns the total value of all active stock. Use a SQLAlchemy query to iterate over active products and sum `price * quantity` in Python.

---

## Next Lesson

**[Phase 09 Practice Exercises → exercises/exercises-beginner.md](../exercises/exercises-beginner.md)**
