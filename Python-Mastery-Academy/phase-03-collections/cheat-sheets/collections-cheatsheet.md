# ⚡ Phase 03 Cheat Sheet — Collections

---

## Lists

```python
# Create
nums = [1, 2, 3]
empty = []

# Access
nums[0]         # first
nums[-1]        # last
nums[1:3]       # slice
nums[::-1]      # reversed

# Modify
nums.append(4)         # add to end
nums.insert(0, 0)      # insert at index
nums.extend([5, 6])    # add multiple
nums.remove(3)         # remove by value
nums.pop()             # remove last, return it
nums.pop(0)            # remove at index
del nums[0]
nums.clear()

# Query
len(nums)
nums.count(2)
nums.index(3)
3 in nums

# Sort
nums.sort()               # in-place, ascending
nums.sort(reverse=True)   # in-place, descending
sorted(nums)              # returns new list
```

---

## Tuples

```python
point = (3, 7)
x, y = point           # unpacking
point[0]               # access (read-only)

# Use tuples for:
# - fixed data (coordinates, RGB, configs)
# - dict keys
# - multiple return values

coords = {(0,0): "origin", (1,0): "right"}
```

---

## Sets

```python
s1 = {1, 2, 3}
s2 = {2, 3, 4}

s1 | s2     # union        {1,2,3,4}
s1 & s2     # intersection {2,3}
s1 - s2     # difference   {1}
s1 ^ s2     # symmetric diff {1,4}

# Remove duplicates from list
unique = list(set([1,2,2,3,3,3]))
```

---

## Dictionaries

```python
d = {"key": "value", "num": 42}

# Access
d["key"]                   # direct (KeyError if missing)
d.get("key", "default")    # safe

# Modify
d["new"] = "value"         # add / update
del d["key"]               # remove
d.pop("key", None)         # remove safely

# Iterate
for key in d:
for key, val in d.items():
for val in d.values():

# Methods
d.keys()
d.values()
d.items()
len(d)
"key" in d
d.update({"a": 1})         # merge/update
```

---

## Comprehensions

```python
# List
[expr for x in iterable]
[expr for x in iterable if condition]

squares  = [n**2 for n in range(10)]
evens    = [n for n in range(20) if n % 2 == 0]

# Dict
{k: v for k, v in pairs}
{word: len(word) for word in words}

# Set
{n**2 for n in nums}

# Filter + transform
high_earners = {name: sal for name, sal in salaries.items() if sal > 70000}
```

---

## Sorting

```python
# Sort list
items.sort()                           # in-place
items.sort(reverse=True)
sorted(items)                          # new list

# Sort by key
students.sort(key=lambda s: s["gpa"])
sorted(students, key=lambda s: s["name"])

# Sort dict by value
sorted(d.items(), key=lambda x: x[1])
```

---

## Nested Structures

```python
# List of dicts (common)
records = [{"name": "Alice", "score": 92}]
records[0]["name"]            # "Alice"

# Dict of dicts
db = {"id1": {"name": "Alice", "score": 92}}
db["id1"]["score"]            # 92

# Safe nested access
val = data.get("a", {}).get("b", {}).get("c", "default")
```
