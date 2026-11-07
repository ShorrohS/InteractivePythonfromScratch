# Phase 03 — Completion Assessment

> Pass mark: 80% | Time: 30 minutes

---

## PART A: Write the Code

**Task 1.** Create a list of 5 employees (each a dict with name, dept, salary). Write code to:
- Print all employees sorted by salary (highest first)
- Find the average salary
- Filter only employees with salary > 70,000
- Create a dict of `{name: salary}` using a dict comprehension

---

**Task 2.** Given this data:
```python
orders = [
    {"item": "Laptop",  "qty": 2, "price": 999.99},
    {"item": "Mouse",   "qty": 5, "price": 29.99},
    {"item": "Monitor", "qty": 1, "price": 349.99},
]
```
Write code that:
- Calculates total for each order (qty × price)
- Finds the highest value order
- Calculates the grand total
- Creates a new list with totals included using a list comprehension

---

**Task 3.** Using sets:
- Create two sets of website visitors for Monday and Tuesday
- Find visitors who came both days
- Find visitors who came on Monday only
- Find total unique visitors across both days

---

## PART B: Predict the Output

**Q4.**
```python
items = [3, 1, 4, 1, 5, 9, 2, 6]
items.sort()
print(items)
print(items[0], items[-1])
```

**Q5.**
```python
d = {"x": 10, "y": 20}
d.update({"z": 30, "x": 99})
print(d)
```

**Q6.**
```python
words = ["apple", "banana", "cherry"]
result = {w: len(w) for w in words if len(w) > 5}
print(result)
```

---

## PART C: Fix the Bug

**Q7.**
```python
names = ["Alice", "Bob", "Carol"]
for i in range(len(names)):
    if names[i] == "Bob":
        names.remove("Bob")    # Bug: modifying list while iterating
print(names)
```
Explain the bug and write a safe alternative.

**Q8.**
```python
config = {"db": {"host": "localhost"}}
port = config["db"]["port"]    # Bug: missing key
```
Fix with a safe alternative.

---

## PART D: Short Answer

**Q9.** When would you choose a tuple over a list?

**Q10.** What is the time complexity advantage of checking `x in my_set` vs `x in my_list`?

---

## Answers

**Q4:** `[1,1,2,3,4,5,6,9]`, `1 9`

**Q5:** `{'x': 99, 'y': 20, 'z': 30}` — update overwrites x, adds z

**Q6:** `{'banana': 6, 'cherry': 6}` — apple has 5 chars (not > 5), excluded

**Q7 fix:**
```python
names = [n for n in names if n != "Bob"]
# OR: names.remove("Bob") before/after the loop
```

**Q8 fix:**
```python
port = config.get("db", {}).get("port", 5432)   # default 5432
```

**Q9:** Use a tuple when: the data should not change (coordinates, config values), as dict keys, for multiple return values, or when immutability is a feature not a bug.

**Q10:** Set lookup is O(1) (constant time). List lookup is O(n) (linear — scans entire list). For large collections, sets are dramatically faster.
