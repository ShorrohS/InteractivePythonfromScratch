"""
Project 03 - Customer Data Processor
Phase 05: File Handling

SKILLS PRACTICED:
  - JSON for persistent storage
  - CSV for data export
  - File path management
  - Data validation on load/save

HOW TO RUN:
  python main.py
"""

import json
import csv
import os
from datetime import datetime

DATA_FILE = "customers.json"


def load_customers() -> list:
    """Load customers from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_customers(customers: list) -> None:
    """Save customers to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(customers, f, indent=2)


def generate_id(customers: list) -> str:
    """Generate next customer ID."""
    if not customers:
        return "C001"
    last_id = max(int(c["id"][1:]) for c in customers)
    return f"C{last_id + 1:03d}"


def add_customer(name: str, email: str, phone: str,
                 segment: str = "Regular") -> dict:
    """Add a new customer."""
    customers = load_customers()

    # Check duplicate email
    if any(c["email"].lower() == email.lower() for c in customers):
        print(f"  Email {email} already exists.")
        return None

    customer = {
        "id":         generate_id(customers),
        "name":       name.strip().title(),
        "email":      email.strip().lower(),
        "phone":      phone.strip(),
        "segment":    segment,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "active":     True,
        "orders":     0,
        "total_spent": 0.0
    }
    customers.append(customer)
    save_customers(customers)
    print(f"  Added: {customer['name']} ({customer['id']})")
    return customer


def display_customers(customers: list = None) -> None:
    """Display customer table."""
    customers = customers or load_customers()
    if not customers:
        print("  No customers found.")
        return
    print(f"\n  {'ID':<6} {'Name':<22} {'Email':<28} {'Segment':<10} {'Spent':>9}")
    print("  " + "-" * 80)
    for c in sorted(customers, key=lambda x: x["name"]):
        status = "" if c["active"] else "[inactive]"
        print(f"  {c['id']:<6} {c['name']:<22} {c['email']:<28} "
              f"{c['segment']:<10} ${c['total_spent']:>8,.2f} {status}")


def search_customers(query: str) -> list:
    """Search by name, email, or ID."""
    q = query.lower()
    return [
        c for c in load_customers()
        if q in c["name"].lower()
        or q in c["email"].lower()
        or q in c["id"].lower()
    ]


def update_customer(cid: str, **updates) -> bool:
    """Update a customer record."""
    customers = load_customers()
    for c in customers:
        if c["id"] == cid:
            c.update(updates)
            save_customers(customers)
            print(f"  Updated {c['name']}.")
            return True
    print(f"  Customer {cid} not found.")
    return False


def record_purchase(cid: str, amount: float) -> None:
    """Record a purchase for a customer."""
    customers = load_customers()
    for c in customers:
        if c["id"] == cid:
            c["orders"]      += 1
            c["total_spent"] += amount
            save_customers(customers)
            print(f"  Recorded ${amount:.2f} for {c['name']}. "
                  f"Total: ${c['total_spent']:.2f}")
            return
    print(f"  Customer {cid} not found.")


def export_to_csv(filename: str = None) -> str:
    """Export customer data to CSV."""
    customers = load_customers()
    if not customers:
        print("  No data to export.")
        return None

    if filename is None:
        filename = f"customers_export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

    fieldnames = ["id", "name", "email", "phone", "segment",
                  "created_at", "active", "orders", "total_spent"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(customers)

    print(f"  Exported {len(customers)} records to: {filename}")
    return filename


def customer_stats() -> None:
    """Display customer analytics."""
    customers = load_customers()
    if not customers:
        print("  No data.")
        return

    active    = [c for c in customers if c["active"]]
    segments  = {}
    for c in active:
        seg = c["segment"]
        segments[seg] = segments.get(seg, {"count": 0, "spent": 0})
        segments[seg]["count"] += 1
        segments[seg]["spent"] += c["total_spent"]

    top_spenders = sorted(active, key=lambda c: c["total_spent"], reverse=True)[:3]

    print(f"\n  CUSTOMER ANALYTICS")
    print(f"  {'Total customers:':<25} {len(customers)}")
    print(f"  {'Active:':<25} {len(active)}")
    print(f"  {'Total revenue:':<25} ${sum(c['total_spent'] for c in active):,.2f}")

    print(f"\n  SEGMENTS:")
    for seg, data in sorted(segments.items()):
        print(f"    {seg:<12} {data['count']:>4} customers  ${data['spent']:>10,.2f}")

    print(f"\n  TOP SPENDERS:")
    for i, c in enumerate(top_spenders, 1):
        print(f"    #{i} {c['name']:<20} ${c['total_spent']:,.2f}")


def main():
    print("=" * 55)
    print("  CUSTOMER DATA PROCESSOR")
    print("=" * 55)

    # Seed data if empty
    if not load_customers():
        print("  Adding sample customers...")
        add_customer("Alice Johnson", "alice@email.com", "555-0101", "Premium")
        add_customer("Bob Smith",     "bob@email.com",   "555-0202", "Regular")
        add_customer("Carol Davis",   "carol@email.com", "555-0303", "Premium")
        record_purchase("C001", 1500.00)
        record_purchase("C001", 2200.00)
        record_purchase("C002", 350.00)

    while True:
        print("\n  [1] View All Customers")
        print("  [2] Add Customer")
        print("  [3] Search")
        print("  [4] Record Purchase")
        print("  [5] Customer Analytics")
        print("  [6] Export to CSV")
        print("  [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            display_customers()

        elif choice == "2":
            name    = input("  Full name: ").strip()
            email   = input("  Email: ").strip()
            phone   = input("  Phone: ").strip()
            segment = input("  Segment (Regular/Premium) [Regular]: ").strip() or "Regular"
            add_customer(name, email, phone, segment)

        elif choice == "3":
            q = input("  Search (name/email/ID): ").strip()
            results = search_customers(q)
            if results:
                display_customers(results)
            else:
                print("  No matches found.")

        elif choice == "4":
            cid = input("  Customer ID: ").strip().upper()
            try:
                amount = float(input("  Purchase amount ($): "))
                record_purchase(cid, amount)
            except ValueError:
                print("  Invalid amount.")

        elif choice == "5":
            customer_stats()

        elif choice == "6":
            export_to_csv()

        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
