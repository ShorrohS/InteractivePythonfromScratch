# Lesson 02 — Match / Case (Pattern Matching)

**Phase:** 02 — Control Flow | **Time:** ~25 min | **Python:** 3.10+

---

## Part 1: What is Match/Case?

`match`/`case` is Python's pattern matching statement, introduced in Python 3.10. It's cleaner than long `if`/`elif` chains when checking one value against many possibilities.

**Analogy:** A phone menu. "Press 1 for sales, press 2 for support..." The match statement is how Python handles those menus.

---

## Part 2: Basic Syntax

```python
match variable:
    case value1:
        action1
    case value2:
        action2
    case _:          # _ is the default (like else)
        default_action
```

---

## Part 3: Examples

### Menu System

```python
print("1. View account")
print("2. Deposit")
print("3. Withdraw")
print("4. Exit")

choice = input("Select option: ")

match choice:
    case "1":
        print("Showing balance...")
    case "2":
        print("Enter deposit amount...")
    case "3":
        print("Enter withdrawal amount...")
    case "4":
        print("Goodbye!")
    case _:
        print("Invalid option. Choose 1-4.")
```

### Day of Week

```python
day = input("Enter day (Mon-Sun): ").strip().title()

match day:
    case "Saturday" | "Sunday":      # | = OR for cases
        print("Weekend!")
    case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
        print("Weekday")
    case _:
        print("Invalid day")
```

### HTTP Status Codes

```python
def http_message(code: int) -> str:
    match code:
        case 200:
            return "OK"
        case 201:
            return "Created"
        case 400:
            return "Bad Request"
        case 401:
            return "Unauthorized"
        case 403:
            return "Forbidden"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:
            return f"Unknown code: {code}"

for code in [200, 404, 500, 999]:
    print(f"  {code}: {http_message(code)}")
```

---

## Part 4: match vs if/elif

```python
# With if/elif
def get_day_type_if(day):
    if day in ("Saturday", "Sunday"):
        return "Weekend"
    elif day in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"):
        return "Weekday"
    else:
        return "Invalid"

# With match (cleaner)
def get_day_type_match(day):
    match day:
        case "Saturday" | "Sunday":
            return "Weekend"
        case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
            return "Weekday"
        case _:
            return "Invalid"
```

**Use match when:** checking one value against many fixed options.
**Use if/elif when:** checking complex conditions with different variables.

---

## Part 5: Restaurant Menu Project

```python
"""Restaurant menu using match/case."""

MENU = {
    "1": ("Burger",  8.99),
    "2": ("Pizza",  12.99),
    "3": ("Pasta",  10.99),
    "4": ("Salad",   7.99),
}

print("=" * 35)
print("   PYTHON RESTAURANT")
print("=" * 35)
for key, (name, price) in MENU.items():
    print(f"  [{key}] {name:<15} ${price:.2f}")
print("  [5] View Order")
print("  [0] Exit")
print("=" * 35)

order = []

while True:
    choice = input("\nSelect: ").strip()
    match choice:
        case "1" | "2" | "3" | "4":
            item, price = MENU[choice]
            order.append((item, price))
            print(f"  Added: {item}")
        case "5":
            if not order:
                print("  Order is empty.")
            else:
                total = sum(p for _, p in order)
                print("\n  YOUR ORDER:")
                for item, price in order:
                    print(f"    {item:<15} ${price:.2f}")
                print(f"  {'TOTAL':<15} ${total:.2f}")
        case "0":
            print("  Thank you! Goodbye.")
            break
        case _:
            print("  Invalid option.")
```

---

## Practice Exercises

1. Build an ATM menu using match/case with options: check balance, deposit, withdraw, exit.

2. Write a match statement that maps a score range to a grade letter. (Hint: use guards with `case x if x >= 90`)

3. Create a currency converter menu (USD, EUR, GBP, JPY) using match/case.

---

## Next Lesson

**[Lesson 03 → While Loops](lesson-03-while-loops.md)**
