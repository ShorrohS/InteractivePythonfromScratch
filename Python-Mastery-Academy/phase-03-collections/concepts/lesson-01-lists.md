# Lesson 01 — Lists

**Phase:** 03 — Collections | **Time:** ~45 min

---

## Part 1: What is a List?

A list is an **ordered, mutable** collection of items.

```python
# Creating lists
empty = []
numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Carol"]
mixed = [1, "hello", 3.14, True]    # can mix types
nested = [[1, 2], [3, 4]]           # lists of lists
```

---

## Part 2: Accessing Items

```python
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# Positive indexing (0-based)
print(fruits[0])     # apple
print(fruits[2])     # cherry
print(fruits[-1])    # elderberry (last item)
print(fruits[-2])    # date (second from last)

# Slicing
print(fruits[1:3])   # ['banana', 'cherry']
print(fruits[:3])    # ['apple', 'banana', 'cherry']
print(fruits[2:])    # ['cherry', 'date', 'elderberry']
print(fruits[::2])   # ['apple', 'cherry', 'elderberry'] (every 2nd)
print(fruits[::-1])  # Reversed list
```

---

## Part 3: Modifying Lists

```python
cart = ["apple", "banana", "cherry"]

# Add items
cart.append("date")         # Add to end: ['apple', 'banana', 'cherry', 'date']
cart.insert(1, "blueberry") # Insert at index: ['apple', 'blueberry', ...]
cart.extend(["mango", "kiwi"])  # Add multiple items

# Remove items
cart.remove("banana")       # Remove by value (first occurrence)
popped = cart.pop()         # Remove and return last item
popped = cart.pop(0)        # Remove and return item at index 0
del cart[0]                 # Delete at index
cart.clear()                # Remove all items

# Modify
cart[0] = "grape"           # Change item at index 0
```

---

## Part 4: List Methods

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]

print(numbers.count(1))    # 2 — how many times 1 appears
print(numbers.index(5))    # 4 — index of first 5
numbers.sort()             # Sort in-place: [1, 1, 2, 3, 4, 5, 5, 6, 9]
numbers.sort(reverse=True) # Reverse sort
numbers.reverse()          # Reverse in-place
copy = numbers.copy()      # Shallow copy
print(len(numbers))        # 9 — length

# Non-mutating sort (returns new list)
sorted_nums = sorted(numbers)
sorted_desc = sorted(numbers, reverse=True)
```

---

## Part 5: Iterating Lists

```python
employees = ["Alice", "Bob", "Carol", "Dave"]

# Basic iteration
for emp in employees:
    print(emp)

# With index
for i, emp in enumerate(employees):
    print(f"{i+1}. {emp}")

# Iterating with range
for i in range(len(employees)):
    print(f"Index {i}: {employees[i]}")

# Check membership
if "Alice" in employees:
    print("Alice is in the list")
```

---

## Part 6: List Comprehensions

```python
# Traditional
squares = []
for i in range(1, 11):
    squares.append(i ** 2)

# Comprehension (much cleaner)
squares = [i ** 2 for i in range(1, 11)]

# With condition
evens = [i for i in range(1, 21) if i % 2 == 0]

# Transform existing list
prices = [10.0, 15.5, 8.0, 20.0]
discounted = [p * 0.9 for p in prices]

# Extract data
employees = [("Alice", 75000), ("Bob", 65000), ("Carol", 90000)]
names_only = [emp[0] for emp in employees]
high_earners = [emp[0] for emp in employees if emp[1] >= 70000]
```

---

## Part 7: Business Example — Shopping Cart

```python
"""Simple shopping cart with list operations."""

cart = []
prices = {}

print("=" * 40)
print("  SHOPPING CART")
print("=" * 40)

while True:
    print("\n[1] Add item  [2] Remove  [3] View  [4] Checkout  [5] Exit")
    choice = input("Option: ")
    
    if choice == "1":
        item = input("Item name: ").strip().title()
        price = float(input(f"Price of {item}: $"))
        cart.append(item)
        prices[item] = price
        print(f"✅ {item} added.")
        
    elif choice == "2":
        if not cart:
            print("Cart is empty.")
        else:
            item = input("Remove which item: ").strip().title()
            if item in cart:
                cart.remove(item)
                del prices[item]
                print(f"✅ {item} removed.")
            else:
                print(f"❌ {item} not in cart.")
                
    elif choice == "3":
        if not cart:
            print("Cart is empty.")
        else:
            print(f"\n  {'Item':<20} {'Price':>10}")
            print("  " + "─" * 30)
            for item in cart:
                print(f"  {item:<20} ${prices[item]:>9.2f}")
            print("  " + "─" * 30)
            total = sum(prices[item] for item in cart)
            print(f"  {'Items: ' + str(len(cart)):<20} ${total:>9.2f}")
            
    elif choice == "4":
        if not cart:
            print("Cart is empty.")
        else:
            total = sum(prices[item] for item in cart)
            tax = total * 0.08
            grand_total = total + tax
            print(f"\n  Subtotal: ${total:.2f}")
            print(f"  Tax (8%): ${tax:.2f}")
            print(f"  Total:    ${grand_total:.2f}")
            print("  ✅ Thank you for your purchase!")
            break
            
    elif choice == "5":
        print("Goodbye!")
        break
```

---

## Common Mistakes

```python
# Mistake 1: IndexError
items = [1, 2, 3]
print(items[3])    # IndexError: list index out of range
                   # Valid indices: 0, 1, 2

# Mistake 2: Modifying list while iterating
for item in items:
    if item == 2:
        items.remove(item)   # Dangerous! Skips items
# Fix: iterate over a copy
for item in items[:]:
    if item == 2:
        items.remove(item)

# Mistake 3: Assignment vs copy
a = [1, 2, 3]
b = a       # b IS a (same object!)
b.append(4) # also modifies a!
# Fix:
b = a.copy()   # proper copy
```

---

## Next Lesson

**[Lesson 02 → Tuples](lesson-02-tuples.md)**
