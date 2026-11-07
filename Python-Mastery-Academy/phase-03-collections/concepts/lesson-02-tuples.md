# Lesson 02 — Tuples & Immutability

**Phase:** 03 — Collections | **Time:** ~30 min | **Prerequisite:** Lesson 01 (Lists)

---

## Part 1: What is a Tuple?

A tuple is an **ordered, immutable** collection of items.
Unlike lists (which use square brackets `[]`), tuples use parentheses `()` or comma separation.

```python
# Creating tuples
coordinates = (10, 20)
rgb_color = (255, 128, 0)
single_item = (42,)          # Note the trailing comma!
mixed_tuple = ("Alice", 28, True, [1, 2])
without_parens = 1, 2, 3     # Tuple packing
empty_tuple = ()

print(type(coordinates))     # <class 'tuple'>
print(coordinates)           # (10, 20)
```

> [!IMPORTANT]
> A single-item tuple MUST have a trailing comma: `(42,)`. Without the comma, `(42)` is treated as just the integer `42` in parentheses!

---

## Part 2: Immutability — Why and When?

Once created, you **cannot** change, add, or remove items from a tuple.

```python
point = (5, 10)

# This will raise a TypeError:
# point[0] = 7   # TypeError: 'tuple' object does not support item assignment
```

### Why use Tuples over Lists?
1. **Safety:** Protects data that should never change (coordinates, configurations, DB credentials).
2. **Performance:** Tuples are slightly faster and consume less memory than lists.
3. **Dictionary Keys:** Because tuples are immutable, they can be used as keys in dictionaries (lists cannot!).

```python
# Tuple as dictionary key
locations = {
    (40.7128, -74.0060): "New York City",
    (34.0522, -118.2437): "Los Angeles",
    (51.5074, -0.1278): "London"
}

nyc_coords = (40.7128, -74.0060)
print(locations[nyc_coords])  # New York City
```

---

## Part 3: Indexing and Slicing

Tuples support the exact same indexing and slicing syntax as lists:

```python
planets = ("Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn")

# Indexing
print(planets[0])     # Mercury
print(planets[-1])    # Saturn

# Slicing (creates a new tuple)
print(planets[1:4])   # ('Venus', 'Earth', 'Mars')
print(planets[::-1])  # Reversed tuple
```

---

## Part 4: Tuple Packing & Unpacking

Packing puts values into a tuple; unpacking extracts them into variables.

```python
# Packing
user = ("Sarah", "Engineer", 95000)

# Unpacking
name, role, salary = user
print(f"{name} is a {role} earning ${salary:,}")

# Extended unpacking with * (rest)
numbers = (1, 2, 3, 4, 5, 6)
first, *middle, last = numbers
print(first)   # 1
print(middle)  # [2, 3, 4, 5] (captured as a list)
print(last)    # 6
```

### Swapping Variables Without Temp Variable
Python uses tuple packing/unpacking behind the scenes:
```python
a = 10
b = 20
a, b = b, a   # Clean, pythonic swap!
print(a, b)   # 20 10
```

---

## Part 5: Tuple Methods

Because tuples are immutable, they only have two built-in methods:

```python
scores = (10, 20, 30, 20, 40, 20, 50)

# .count(x) — how many times x appears
print(scores.count(20))   # 3

# .index(x) — position of first occurrence of x
print(scores.index(30))   # 2
```

---

## Part 6: Summary & Best Practices

| Feature | List `[]` | Tuple `()` |
| :--- | :--- | :--- |
| **Mutability** | Mutable (can change) | Immutable (read-only) |
| **Syntax** | `[1, 2, 3]` | `(1, 2, 3)` |
| **Use Case** | Collections that grow/shrink | Fixed records, constant coordinates |
| **Memory** | Higher overhead | Lightweight & fast |
| **Dict Key** | ❌ Cannot be key | ✅ Can be key |
