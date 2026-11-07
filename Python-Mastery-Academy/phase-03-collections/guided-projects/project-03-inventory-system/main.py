"""
Project 03 — Inventory System
Phase 03: Collections

SKILLS PRACTICED:
  - Nested dicts (catalogue as primary structure)
  - List comprehensions for filtering/reporting
  - Set operations (categories)
  - Sorting dicts by values

HOW TO RUN:
  python main.py
"""

from datetime import datetime

# ── Inventory data structure ─────────────────────────────────────────────────
inventory = {
    "P001": {"name": "Laptop Pro 15",    "category": "Electronics", "price": 1299.99, "qty": 15, "reorder": 5},
    "P002": {"name": "Wireless Mouse",   "category": "Electronics", "price": 29.99,   "qty": 80, "reorder": 20},
    "P003": {"name": "Office Chair",     "category": "Furniture",   "price": 249.99,  "qty": 8,  "reorder": 3},
    "P004": {"name": "Standing Desk",    "category": "Furniture",   "price": 599.99,  "qty": 4,  "reorder": 2},
    "P005": {"name": "Python Book",      "category": "Books",       "price": 45.99,   "qty": 30, "reorder": 10},
    "P006": {"name": "USB-C Hub",        "category": "Electronics", "price": 39.99,   "qty": 3,  "reorder": 10},
    "P007": {"name": "Monitor 27-inch",  "category": "Electronics", "price": 349.99,  "qty": 0,  "reorder": 5},
    "P008": {"name": "Notebook Pack",    "category": "Stationery",  "price": 8.99,    "qty": 120,"reorder": 30},
}


def total_value(product: dict) -> float:
    return product["price"] * product["qty"]


def display_inventory(items: dict = None, title: str = "INVENTORY") -> None:
    items = items or inventory
    print(f"\n  {title}")
    print(f"  {'Code':<6} {'Name':<22} {'Category':<12} {'Price':>8} {'Qty':>5} {'Value':>10} {'Status':>8}")
    print("  " + "-" * 78)
    for code, p in sorted(items.items()):
        value = total_value(p)
        if p["qty"] == 0:
            status = "OUT"
        elif p["qty"] <= p["reorder"]:
            status = "LOW"
        else:
            status = "OK"
        print(f"  {code:<6} {p['name']:<22} {p['category']:<12} "
              f"${p['price']:>7.2f} {p['qty']:>5} ${value:>9.2f} {status:>8}")


def add_product(code: str, name: str, category: str,
                price: float, qty: int, reorder: int) -> None:
    inventory[code] = {
        "name": name, "category": category,
        "price": price, "qty": qty, "reorder": reorder
    }
    print(f"  Added: {name} ({code})")


def restock(code: str, qty: int) -> None:
    if code not in inventory:
        print(f"  Product {code} not found.")
        return
    inventory[code]["qty"] += qty
    print(f"  Restocked {inventory[code]['name']}: +{qty} units "
          f"(new total: {inventory[code]['qty']})")


def sell(code: str, qty: int) -> bool:
    if code not in inventory:
        print(f"  Product {code} not found.")
        return False
    p = inventory[code]
    if p["qty"] < qty:
        print(f"  Insufficient stock. Have {p['qty']}, need {qty}.")
        return False
    p["qty"] -= qty
    print(f"  Sold {qty}x {p['name']}. Remaining: {p['qty']}")
    return True


def low_stock_report() -> None:
    low = {code: p for code, p in inventory.items() if p["qty"] <= p["reorder"]}
    if not low:
        print("  All products adequately stocked.")
        return
    print(f"\n  LOW STOCK / OUT OF STOCK ALERT")
    print(f"  {'Code':<6} {'Product':<22} {'Current':>8} {'Reorder':>8} {'Status':>8}")
    print("  " + "-" * 57)
    for code, p in low.items():
        status = "OUT" if p["qty"] == 0 else "LOW"
        print(f"  {code:<6} {p['name']:<22} {p['qty']:>8} {p['reorder']:>8} {status:>8}")


def category_report() -> None:
    categories = {p["category"] for p in inventory.values()}
    print(f"\n  CATEGORY SUMMARY")
    print(f"  {'Category':<14} {'Items':>6} {'Total Value':>13} {'Avg Price':>10}")
    print("  " + "-" * 48)
    for cat in sorted(categories):
        cat_items = [p for p in inventory.values() if p["category"] == cat]
        cat_value = sum(total_value(p) for p in cat_items)
        cat_avg   = sum(p["price"] for p in cat_items) / len(cat_items)
        print(f"  {cat:<14} {len(cat_items):>6} ${cat_value:>12,.2f} ${cat_avg:>9.2f}")


def value_report() -> None:
    total = sum(total_value(p) for p in inventory.values())
    by_value = sorted(inventory.items(), key=lambda x: total_value(x[1]), reverse=True)
    print(f"\n  INVENTORY VALUE REPORT")
    print(f"  Total inventory value: ${total:,.2f}")
    print(f"\n  Top 5 by value:")
    for code, p in by_value[:5]:
        print(f"    {p['name']:<22} ${total_value(p):,.2f}")


def search(query: str) -> dict:
    q = query.lower()
    return {
        code: p for code, p in inventory.items()
        if q in p["name"].lower() or q in p["category"].lower()
    }


def main():
    print("=" * 60)
    print("  INVENTORY MANAGEMENT SYSTEM")
    print("=" * 60)

    while True:
        print()
        print("  [1] View All Inventory")
        print("  [2] Add Product")
        print("  [3] Restock Product")
        print("  [4] Record Sale")
        print("  [5] Low Stock Report")
        print("  [6] Category Report")
        print("  [7] Value Report")
        print("  [8] Search")
        print("  [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            display_inventory()

        elif choice == "2":
            code     = input("  Product code: ").strip().upper()
            name     = input("  Name: ").strip().title()
            category = input("  Category: ").strip().title()
            try:
                price   = float(input("  Price ($): "))
                qty     = int(input("  Initial quantity: "))
                reorder = int(input("  Reorder point: "))
                add_product(code, name, category, price, qty, reorder)
            except ValueError:
                print("  Invalid number input.")

        elif choice == "3":
            code = input("  Product code: ").strip().upper()
            try:
                qty = int(input("  Quantity to add: "))
                restock(code, qty)
            except ValueError:
                print("  Invalid quantity.")

        elif choice == "4":
            code = input("  Product code: ").strip().upper()
            try:
                qty = int(input("  Quantity sold: "))
                sell(code, qty)
            except ValueError:
                print("  Invalid quantity.")

        elif choice == "5":
            low_stock_report()

        elif choice == "6":
            category_report()

        elif choice == "7":
            value_report()

        elif choice == "8":
            q = input("  Search: ").strip()
            results = search(q)
            if results:
                display_inventory(results, f"SEARCH: '{q}'")
            else:
                print("  No matches found.")

        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
