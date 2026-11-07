"""
Project 01 — Shopping Cart
Phase 03: Collections

SKILLS PRACTICED:
  - Lists (add, remove, iterate)
  - Dictionaries (product catalogue lookup)
  - List comprehensions
  - Accumulating values

HOW TO RUN:
  python main.py
"""

CATALOG = {
    "001": {"name": "Laptop",       "price": 999.99, "stock": 5},
    "002": {"name": "Mouse",        "price": 29.99,  "stock": 50},
    "003": {"name": "Keyboard",     "price": 79.99,  "stock": 20},
    "004": {"name": "Monitor",      "price": 349.99, "stock": 8},
    "005": {"name": "USB Hub",      "price": 39.99,  "stock": 30},
    "006": {"name": "Webcam",       "price": 89.99,  "stock": 15},
    "007": {"name": "Headphones",   "price": 149.99, "stock": 12},
    "008": {"name": "Desk Lamp",    "price": 49.99,  "stock": 25},
}

TAX_RATE = 0.08


def display_catalog() -> None:
    print("\n  PRODUCT CATALOGUE")
    print(f"  {'Code':<6} {'Product':<20} {'Price':>9} {'Stock':>6}")
    print("  " + "-" * 45)
    for code, product in CATALOG.items():
        stock_label = f"{product['stock']}" if product["stock"] > 0 else "OUT"
        print(f"  {code:<6} {product['name']:<20} ${product['price']:>8.2f} {stock_label:>6}")


def display_cart(cart: list) -> None:
    if not cart:
        print("\n  Cart is empty.")
        return
    print("\n  YOUR CART")
    print(f"  {'Product':<20} {'Qty':>4} {'Unit':>9} {'Total':>10}")
    print("  " + "-" * 47)
    for item in cart:
        line_total = item["qty"] * item["price"]
        print(f"  {item['name']:<20} {item['qty']:>4} ${item['price']:>8.2f} ${line_total:>9.2f}")


def get_cart_total(cart: list) -> float:
    return sum(item["qty"] * item["price"] for item in cart)


def find_in_cart(cart: list, code: str):
    for item in cart:
        if item["code"] == code:
            return item
    return None


def main():
    cart = []

    print("=" * 55)
    print("  PYTHON SHOPPING CART")
    print("=" * 55)

    while True:
        print()
        print("  [1] Browse Catalogue")
        print("  [2] Add Item")
        print("  [3] Remove Item")
        print("  [4] View Cart")
        print("  [5] Checkout")
        print("  [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            display_catalog()

        elif choice == "2":
            display_catalog()
            code = input("\n  Enter product code: ").strip().upper()
            if code not in CATALOG:
                print("  Invalid code.")
                continue
            product = CATALOG[code]
            if product["stock"] == 0:
                print(f"  {product['name']} is out of stock.")
                continue
            try:
                qty = int(input(f"  Quantity (max {product['stock']}): "))
                if qty <= 0 or qty > product["stock"]:
                    print(f"  Invalid quantity.")
                    continue
            except ValueError:
                print("  Invalid input.")
                continue

            existing = find_in_cart(cart, code)
            if existing:
                existing["qty"] += qty
                print(f"  Updated {product['name']} qty to {existing['qty']}.")
            else:
                cart.append({
                    "code": code,
                    "name": product["name"],
                    "price": product["price"],
                    "qty": qty
                })
                print(f"  Added {qty}x {product['name']} to cart.")

        elif choice == "3":
            if not cart:
                print("  Cart is empty.")
                continue
            display_cart(cart)
            code = input("\n  Enter code to remove: ").strip().upper()
            item = find_in_cart(cart, code)
            if item:
                cart.remove(item)
                print(f"  Removed {item['name']}.")
            else:
                print("  Item not in cart.")

        elif choice == "4":
            display_cart(cart)
            if cart:
                subtotal = get_cart_total(cart)
                tax = subtotal * TAX_RATE
                print(f"\n  {'Subtotal:':<20} ${subtotal:>9.2f}")
                print(f"  {'Tax (8%):':<20} ${tax:>9.2f}")
                print(f"  {'TOTAL:':<20} ${subtotal+tax:>9.2f}")

        elif choice == "5":
            if not cart:
                print("  Cart is empty. Add items before checking out.")
                continue
            display_cart(cart)
            subtotal = get_cart_total(cart)
            tax = subtotal * TAX_RATE
            total = subtotal + tax
            print(f"\n  {'Subtotal:':<20} ${subtotal:>9.2f}")
            print(f"  {'Tax (8%):':<20} ${tax:>9.2f}")
            print(f"  {'TOTAL:':<20} ${total:>9.2f}")
            confirm = input("\n  Confirm purchase? (yes/no): ").strip().lower()
            if confirm in ("yes", "y"):
                for item in cart:
                    CATALOG[item["code"]]["stock"] -= item["qty"]
                print("\n  Order confirmed! Thank you for shopping.")
                print(f"  Receipt total: ${total:.2f}")
                cart.clear()
            else:
                print("  Purchase cancelled.")

        elif choice == "0":
            print("\n  Thank you for visiting. Goodbye!")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
