"""
Demo 02 - CSV Files
Phase 05: File Handling

Run: python demo-02-csv-files.py
"""

import csv
import os

print("=" * 55)
print("DEMO 02 - CSV Files")
print("=" * 55)

# --- WRITING CSV ---
print("\n1. Writing CSV with csv.writer:")
employees = [
    ["name", "department", "salary", "active"],
    ["Alice Johnson", "Engineering", 85000, True],
    ["Bob Smith",     "Sales",       65000, True],
    ["Carol Davis",   "Engineering", 92000, True],
    ["Dave Wilson",   "Marketing",   71000, False],
]

with open("employees.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(employees)
print("  Written: employees.csv")

# --- READING CSV with reader ---
print("\n2. Reading with csv.reader:")
with open("employees.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)    # skip header
    print(f"  Header: {header}")
    for row in reader:
        print(f"  Row:    {row}")

# --- WRITING with DictWriter ---
print("\n3. Writing with DictWriter (column-name based):")
data = [
    {"product": "Laptop", "price": 999.99, "stock": 15, "category": "Electronics"},
    {"product": "Mouse",  "price": 29.99,  "stock": 80, "category": "Electronics"},
    {"product": "Desk",   "price": 249.99, "stock": 10, "category": "Furniture"},
]

with open("products.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["product", "price", "stock", "category"])
    writer.writeheader()
    writer.writerows(data)
print("  Written: products.csv")

# --- READING with DictReader ---
print("\n4. Reading with DictReader (access by column name):")
with open("products.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Convert types — DictReader returns everything as str
        product = row["product"]
        price   = float(row["price"])
        stock   = int(row["stock"])
        print(f"  {product:<10} ${price:.2f} ({stock} in stock)")

# --- AGGREGATION ---
print("\n5. Aggregation on CSV data:")
with open("products.csv", "r") as f:
    records = [
        {**r, "price": float(r["price"]), "stock": int(r["stock"])}
        for r in csv.DictReader(f)
    ]

total_value = sum(r["price"] * r["stock"] for r in records)
most_stock  = max(records, key=lambda r: r["stock"])
print(f"  Total inventory value: ${total_value:,.2f}")
print(f"  Most stock: {most_stock['product']} ({most_stock['stock']} units)")

# Cleanup
for f in ["employees.csv", "products.csv"]:
    os.remove(f)
print("\n  Cleaned up demo files.")
print("=" * 55)
