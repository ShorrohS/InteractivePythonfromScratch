"""
Project 02 - Inventory Management App (SQLite)
Phase 09: Databases

SKILLS PRACTICED:
  - SQLite with Python
  - Full CRUD operations
  - Parameterized queries (SQL injection prevention)
  - Aggregate queries (low stock, category totals)
  - Transaction management

HOW TO RUN:
  python main.py

DATABASE:
  Creates inventory.db in the current directory
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_FILE = "inventory.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT    NOT NULL UNIQUE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                sku          TEXT    NOT NULL UNIQUE,
                name         TEXT    NOT NULL,
                category_id  INTEGER REFERENCES categories(id),
                price        REAL    NOT NULL CHECK(price >= 0),
                cost         REAL    NOT NULL CHECK(cost >= 0),
                quantity     INTEGER NOT NULL DEFAULT 0,
                reorder_pt   INTEGER NOT NULL DEFAULT 5,
                created_at   TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id  INTEGER NOT NULL REFERENCES products(id),
                type        TEXT    NOT NULL,  -- IN / OUT / ADJUST
                quantity    INTEGER NOT NULL,
                note        TEXT,
                created_at  TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


def seed_data() -> None:
    with get_conn() as conn:
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count > 0:
            return
        cats = ["Electronics", "Furniture", "Stationery", "Accessories"]
        for cat in cats:
            conn.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))

        products = [
            ("SKU-001","Laptop Pro 15",  "Electronics", 1299.99, 800.00, 15, 5),
            ("SKU-002","Wireless Mouse", "Electronics",   29.99,  12.00, 80, 20),
            ("SKU-003","Office Chair",   "Furniture",    249.99, 140.00,  8,  3),
            ("SKU-004","Standing Desk",  "Furniture",    599.99, 350.00,  3,  2),
            ("SKU-005","Notebook Pack",  "Stationery",     8.99,   3.50,120, 30),
            ("SKU-006","USB-C Hub",      "Accessories",   39.99,  18.00,  4, 10),
        ]
        for sku, name, cat, price, cost, qty, reorder in products:
            cat_id = conn.execute(
                "SELECT id FROM categories WHERE name=?", (cat,)
            ).fetchone()["id"]
            conn.execute("""
                INSERT INTO products (sku, name, category_id, price, cost, quantity, reorder_pt)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (sku, name, cat_id, price, cost, qty, reorder))
        conn.commit()
    print("  Sample data loaded.")


# ── CRUD FUNCTIONS ──────────────────────────────────────────────────────────

def get_all_products() -> list:
    with get_conn() as conn:
        return conn.execute("""
            SELECT p.*, c.name AS category
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            ORDER BY p.name
        """).fetchall()


def search_products(query: str) -> list:
    q = f"%{query}%"
    with get_conn() as conn:
        return conn.execute("""
            SELECT p.*, c.name AS category
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.name LIKE ? OR p.sku LIKE ? OR c.name LIKE ?
        """, (q, q, q)).fetchall()


def add_product(sku: str, name: str, category: str,
                price: float, cost: float, qty: int, reorder: int) -> int:
    with get_conn() as conn:
        cat_row = conn.execute(
            "SELECT id FROM categories WHERE name=?", (category,)
        ).fetchone()
        if not cat_row:
            cursor = conn.execute(
                "INSERT INTO categories (name) VALUES (?)", (category,)
            )
            cat_id = cursor.lastrowid
        else:
            cat_id = cat_row["id"]
        cursor = conn.execute("""
            INSERT INTO products (sku, name, category_id, price, cost, quantity, reorder_pt)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sku, name, cat_id, price, cost, qty, reorder))
        conn.commit()
        return cursor.lastrowid


def adjust_stock(product_id: int, qty_change: int, txn_type: str, note: str = "") -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE products SET quantity = quantity + ? WHERE id = ?",
            (qty_change, product_id)
        )
        conn.execute("""
            INSERT INTO transactions (product_id, type, quantity, note)
            VALUES (?, ?, ?, ?)
        """, (product_id, txn_type, abs(qty_change), note))
        conn.commit()


def low_stock_report() -> list:
    with get_conn() as conn:
        return conn.execute("""
            SELECT p.*, c.name AS category
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.quantity <= p.reorder_pt
            ORDER BY p.quantity ASC
        """).fetchall()


def category_summary() -> list:
    with get_conn() as conn:
        return conn.execute("""
            SELECT c.name AS category,
                   COUNT(p.id)               AS products,
                   SUM(p.quantity)            AS total_units,
                   SUM(p.quantity * p.cost)   AS stock_value,
                   SUM(p.quantity * p.price)  AS retail_value
            FROM categories c
            LEFT JOIN products p ON p.category_id = c.id
            GROUP BY c.name
            ORDER BY retail_value DESC
        """).fetchall()


# ── DISPLAY ──────────────────────────────────────────────────────────────────

def display_products(products: list) -> None:
    if not products:
        print("  No products found.")
        return
    print(f"\n  {'ID':<4} {'SKU':<10} {'Name':<22} {'Category':<14} "
          f"{'Price':>8} {'Qty':>5} {'Status':>8}")
    print("  " + "-" * 76)
    for p in products:
        if p["quantity"] == 0:
            status = "OUT"
        elif p["quantity"] <= p["reorder_pt"]:
            status = "LOW"
        else:
            status = "OK"
        print(f"  {p['id']:<4} {p['sku']:<10} {p['name']:<22} "
              f"{(p['category'] or 'N/A'):<14} ${p['price']:>7.2f} "
              f"{p['quantity']:>5} {status:>8}")


def main():
    init_db()
    seed_data()

    print("=" * 60)
    print("  INVENTORY MANAGEMENT SYSTEM (SQLite)")
    print("=" * 60)

    while True:
        all_p = get_all_products()
        total_val = sum(p["quantity"] * p["cost"] for p in all_p)
        print(f"\n  Products: {len(all_p)}  |  Stock Value: ${total_val:,.2f}")
        print("\n  [1] View All      [2] Search       [3] Add Product")
        print("  [4] Stock In      [5] Stock Out     [6] Low Stock")
        print("  [7] Category Summary               [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            display_products(get_all_products())

        elif choice == "2":
            q = input("  Search: ").strip()
            display_products(search_products(q))

        elif choice == "3":
            sku      = input("  SKU: ").strip().upper()
            name     = input("  Name: ").strip()
            category = input("  Category: ").strip().title()
            try:
                price   = float(input("  Sell price ($): "))
                cost    = float(input("  Cost price ($): "))
                qty     = int(input("  Initial quantity: "))
                reorder = int(input("  Reorder point: "))
                pid = add_product(sku, name, category, price, cost, qty, reorder)
                print(f"  Added product ID: {pid}")
            except (ValueError, sqlite3.IntegrityError) as e:
                print(f"  Error: {e}")

        elif choice == "4":
            try:
                pid  = int(input("  Product ID: "))
                qty  = int(input("  Quantity received: "))
                note = input("  Note: ").strip()
                adjust_stock(pid, qty, "IN", note)
                print(f"  Stock updated (+{qty})")
            except ValueError:
                print("  Invalid input.")

        elif choice == "5":
            try:
                pid  = int(input("  Product ID: "))
                qty  = int(input("  Quantity sold/removed: "))
                note = input("  Note: ").strip()
                adjust_stock(pid, -qty, "OUT", note)
                print(f"  Stock updated (-{qty})")
            except ValueError:
                print("  Invalid input.")

        elif choice == "6":
            products = low_stock_report()
            if not products:
                print("  All products adequately stocked.")
            else:
                print(f"\n  {len(products)} LOW/OUT OF STOCK ITEM(S):")
                display_products(products)

        elif choice == "7":
            rows = category_summary()
            print(f"\n  {'Category':<14} {'Products':>9} {'Units':>7} "
                  f"{'Cost Value':>12} {'Retail Value':>13}")
            print("  " + "-" * 60)
            for r in rows:
                print(f"  {r['category']:<14} {r['products']:>9} "
                      f"{(r['total_units'] or 0):>7} "
                      f"${(r['stock_value'] or 0):>11,.2f} "
                      f"${(r['retail_value'] or 0):>12,.2f}")

        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
