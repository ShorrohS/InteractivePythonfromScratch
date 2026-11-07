"""
Demo 02 - Parameters, Return Values & Defaults
Phase 04: Functions

Run: python demo-02-parameters.py
"""

print("=" * 55)
print("DEMO 02 - Parameters & Return Values")
print("=" * 55)

# --- POSITIONAL vs KEYWORD ---
print("\n1. Positional vs Keyword arguments:")

def describe(name: str, price: float, qty: int) -> str:
    return f"{qty}x {name} @ ${price:.2f} = ${price * qty:.2f}"

print(f"  Positional: {describe('Laptop', 999.99, 2)}")
print(f"  Keyword:    {describe(price=999.99, name='Laptop', qty=2)}")
print(f"  Mixed:      {describe('Laptop', qty=2, price=999.99)}")

# --- DEFAULT ARGUMENTS ---
print("\n2. Default arguments:")

def send_notification(message: str,
                      recipient: str = "all",
                      priority: str = "normal",
                      send_email: bool = True) -> dict:
    return {"msg": message, "to": recipient,
            "priority": priority, "email": send_email}

n1 = send_notification("System maintenance at 2am")
n2 = send_notification("ALERT: disk full", "admin", "high")
n3 = send_notification("Weekly report", send_email=False)

for n in [n1, n2, n3]:
    print(f"  {n}")

# --- MULTIPLE RETURN VALUES ---
print("\n3. Multiple return values:")

def analyse_list(nums: list[float]) -> tuple:
    return min(nums), max(nums), sum(nums) / len(nums), sum(nums)

data = [72, 88, 95, 61, 83, 77, 90]
low, high, avg, total = analyse_list(data)
print(f"  Data: {data}")
print(f"  Min: {low}, Max: {high}, Avg: {avg:.1f}, Sum: {total}")

# --- MUTABLE DEFAULT TRAP ---
print("\n4. Mutable default trap (correct approach):")

def add_to_order(item: str, order: list = None) -> list:
    if order is None:
        order = []
    order.append(item)
    return order

order1 = add_to_order("laptop")
order2 = add_to_order("mouse")          # fresh list, not shared!
order3 = add_to_order("keyboard", order1)  # pass existing list

print(f"  order1: {order1}")
print(f"  order2: {order2}")
print(f"  order3: {order3}")

# --- REAL BUSINESS EXAMPLE ---
print("\n5. Invoice calculator:")

def calculate_invoice(items: list[dict],
                      tax_rate: float = 0.08,
                      discount_pct: float = 0.0) -> dict:
    subtotal = sum(i["qty"] * i["unit_price"] for i in items)
    discount = subtotal * discount_pct
    taxable  = subtotal - discount
    tax      = taxable * tax_rate
    return {"subtotal": subtotal, "discount": discount,
            "tax": round(tax, 2), "total": round(taxable + tax, 2)}

order = [
    {"name": "Laptop",   "qty": 1, "unit_price": 999.99},
    {"name": "Mouse",    "qty": 2, "unit_price": 29.99},
]

inv = calculate_invoice(order, discount_pct=0.10)
print(f"  {'Subtotal':<12}: ${inv['subtotal']:.2f}")
print(f"  {'Discount':<12}: ${inv['discount']:.2f}")
print(f"  {'Tax (8%)':<12}: ${inv['tax']:.2f}")
print(f"  {'TOTAL':<12}: ${inv['total']:.2f}")
