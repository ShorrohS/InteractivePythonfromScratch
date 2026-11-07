# Lesson 03 — Sets & Set Operations

**Phase:** 03 — Collections | **Time:** ~30 min | **Prerequisite:** Lesson 01 (Lists)

---

## Part 1: What is a Set?

A set is an **unordered collection of unique items**.
Sets use curly braces `{}` or the `set()` constructor.

```python
# Creating sets
numbers = {1, 2, 3, 4, 5}
fruits = {"apple", "banana", "cherry"}
empty_set = set()   # Note: {} creates an empty dict, not a set!

# Duplicates are automatically removed!
tags = {"python", "ai", "web", "python", "data", "ai"}
print(tags)   # {'python', 'ai', 'web', 'data'} (order may vary)
```

> [!NOTE]
> Sets are **unordered** and **unindexed**. You cannot access items via `tags[0]`.

---

## Part 2: Deduplication

One of the most common real-world uses of sets is removing duplicates from a list:

```python
user_ids = [101, 102, 101, 103, 104, 102, 105]
unique_ids = list(set(user_ids))
print(unique_ids)   # [101, 102, 103, 104, 105]
```

---

## Part 3: Adding and Removing Items

```python
colors = {"red", "green", "blue"}

# Add items
colors.add("yellow")
colors.update(["purple", "orange"])

# Remove items
colors.remove("red")      # Raises KeyError if item not found
colors.discard("black")   # Safe remove (does NOT raise error if missing)
popped = colors.pop()     # Removes and returns an arbitrary item
colors.clear()            # Clears all items
```

---

## Part 4: Set Theory Operations

Sets provide mathematical set operations that make comparisons lightning-fast.

```python
frontend_devs = {"Alice", "Bob", "Charlie", "Diana"}
backend_devs = {"Charlie", "Diana", "Evan", "Frank"}

# 1. Union (|): All developers (in either or both)
all_devs = frontend_devs | backend_devs
# or: frontend_devs.union(backend_devs)
print("All devs:", all_devs)

# 2. Intersection (&): Full-stack developers (in BOTH sets)
fullstack = frontend_devs & backend_devs
# or: frontend_devs.intersection(backend_devs)
print("Fullstack:", fullstack)  # {'Charlie', 'Diana'}

# 3. Difference (-): Frontend ONLY (not in backend)
frontend_only = frontend_devs - backend_devs
print("Frontend only:", frontend_only)  # {'Alice', 'Bob'}

# 4. Symmetric Difference (^): In ONE set, but NOT BOTH
specialists = frontend_devs ^ backend_devs
print("Single-specialty:", specialists)  # {'Alice', 'Bob', 'Evan', 'Frank'}
```

---

## Part 5: Membership Testing Performance

Checking if an element exists in a set (`item in my_set`) is **O(1) average time complexity** (instant lookup via hashing), compared to **O(n)** in a list (scanning every item).

```python
# Fast lookup in millions of records
banned_users = {f"user_{i}" for i in range(100_000)}

if "user_999" in banned_users:  # Runs in microseconds!
    print("Access Denied")
```

---

## Part 6: Frozensets (Immutable Sets)

A `frozenset` is an immutable version of a set. Once created, elements cannot be added or removed.
Because it is immutable, a `frozenset` can be used as a dictionary key or an element inside another set!

```python
frozen = frozenset([1, 2, 3, 4])
# frozen.add(5)  # AttributeError: 'frozenset' object has no attribute 'add'

# Frozenset as dict key:
group_scores = {
    frozenset({"Alice", "Bob"}): 98,
    frozenset({"Charlie", "Diana"}): 87
}
```
