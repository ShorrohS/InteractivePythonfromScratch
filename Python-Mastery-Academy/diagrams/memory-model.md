# 🔷 Diagram: Python Memory Model

> How Python stores and manages data in memory.

---

## Variables Are References, Not Boxes

```
COMMON MISCONCEPTION:

  x = 42

  People think:     x  [  42  ]   ← variable IS the value

REALITY IN PYTHON:

  x = 42

  Python creates:   42  (object in memory at address 0x7f1a)
                    x   ──────────────────────────► 0x7f1a

  x is a NAME that POINTS TO an object, not the object itself.
```

---

## Object Identity

```python
x = 42
y = 42
z = x
```

```
MEMORY:
┌────────────────────────────────────────┐
│           INTEGER OBJECT               │
│           value: 42                    │◄── x
│           id: 0x7f1a                   │◄── y  (same object!)
│                                        │◄── z  (same object!)
└────────────────────────────────────────┘

Why? Python caches small integers (-5 to 256) for efficiency.

Check with:
  print(id(x))   # memory address
  print(x is y)  # True — same object
  print(x == y)  # True — same value
```

---

## Mutable vs Immutable

```
IMMUTABLE (cannot be changed in-place)
────────────────────────────────────────
  int, float, str, tuple, bool

  x = "hello"
  x = "world"   ← Creates a NEW string object
                  x now points to new object
                  "hello" is garbage collected

  Objects: [hello 0x1a] [world 0x1b]
  x: 0x1a → 0x1b  (x was reassigned)


MUTABLE (can be changed in-place)
──────────────────────────────────
  list, dict, set

  nums = [1, 2, 3]
  nums.append(4)    ← Modifies the SAME object
                      No new object created

  nums: 0x2a → [1, 2, 3] → [1, 2, 3, 4]  (same address!)
```

---

## The Mutation Trap

```python
a = [1, 2, 3]
b = a           # b points to SAME list

b.append(4)

print(a)        # [1, 2, 3, 4]  ← a was changed too!
print(b)        # [1, 2, 3, 4]
```

```
MEMORY:
Before:
  a ──► [1, 2, 3]  at 0x5a
  b ──► [1, 2, 3]  at 0x5a  (same object!)

After b.append(4):
  a ──► [1, 2, 3, 4]  at 0x5a
  b ──► [1, 2, 3, 4]  at 0x5a  (same object — BOTH changed!)

Fix — make a copy:
  b = a.copy()     # shallow copy
  b = a[:]         # also shallow copy
  b = list(a)      # also shallow copy
```

---

## Stack vs Heap

```
┌───────────────────────────────────────────────────────┐
│                    PYTHON MEMORY                      │
├───────────────────────────────────────────────────────┤
│                                                       │
│  STACK (Call Stack)           HEAP (Object Store)     │
│  ─────────────────            ──────────────────      │
│                                                       │
│  Function calls               All Python objects      │
│  Local variable names         live here               │
│  Return addresses                                     │
│                               int, str, list,         │
│  fast, limited size           dict, etc.              │
│  automatically managed        managed by GC           │
│                                                       │
│  Example:                     Example:                │
│  ┌───────────┐                ┌────────────────┐      │
│  │ main()    │                │ "Alice" (str)  │      │
│  │  name ────┼──────────────► │  id: 0x1a     │      │
│  │  age  ────┼──►  30 (int)  │                │      │
│  └───────────┘                └────────────────┘      │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

## Scope and Namespaces

```
LEGB Rule — Python looks up names in this order:

L — Local      (inside current function)
E — Enclosing  (outer function, for closures)
G — Global     (module level)
B — Built-in   (Python's built-ins: print, len, etc.)

Example:
┌─────────────────────────────────────────────────┐
│  BUILT-IN: print, len, range, int, str...        │
│  ┌────────────────────────────────────────────┐  │
│  │  GLOBAL: x = 10, name = "academy"          │  │
│  │  ┌──────────────────────────────────────┐  │  │
│  │  │  ENCLOSING: outer function scope     │  │  │
│  │  │  ┌────────────────────────────────┐  │  │  │
│  │  │  │  LOCAL: variables inside func  │  │  │  │
│  │  │  └────────────────────────────────┘  │  │  │
│  │  └──────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## Garbage Collection

```
When does Python free memory?

REFERENCE COUNTING:
  Every object has a count of how many names point to it.

  x = [1, 2, 3]   ← ref count: 1
  y = x            ← ref count: 2
  del x            ← ref count: 1
  del y            ← ref count: 0  → GARBAGE COLLECTED

CYCLIC GC:
  Handles reference cycles that counting can't resolve.
  Runs periodically.

YOU DON'T MANAGE THIS.
Python does it automatically.
Just know: when nothing references an object, it's freed.
```

---

## Practical Implications for Your Code

```
1. Immutable strings mean string ops create new objects:
   s = "hello"
   s = s + " world"   ← new string object each time
   → Use "".join() for building large strings in loops

2. Mutable list default argument bug:
   def add_item(item, lst=[]):   ← DANGEROUS
       lst.append(item)
       return lst
   Correct:
   def add_item(item, lst=None):
       if lst is None:
           lst = []
       lst.append(item)
       return lst

3. Copying large data:
   import copy
   deep = copy.deepcopy(nested_structure)   ← copies all levels
```

---

## Quick Reference

| Type | Mutable? | Copy needed? |
|------|----------|-------------|
| int | No | N/A |
| float | No | N/A |
| str | No | N/A |
| bool | No | N/A |
| tuple | No | N/A |
| list | Yes | Yes — use .copy() |
| dict | Yes | Yes — use .copy() |
| set | Yes | Yes — use .copy() |
