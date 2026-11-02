# 📦 Phase 03 — Collections

> **Goal:** Store, organize, and manipulate groups of data using Python's four collection types.

---

## Why Collections Matter

Before collections: you'd need 100 variables to store 100 students.
With collections: one list handles 100 or 100,000 students identically.

---

## The 4 Collection Types

```
┌─────────────┬──────────────┬───────────┬──────────────────────────────┐
│ Type        │ Example      │ Ordered?  │ Use Case                     │
├─────────────┼──────────────┼───────────┼──────────────────────────────┤
│ list        │ [1, 2, 3]    │ ✅ Yes    │ Ordered, changeable data     │
│ tuple       │ (1, 2, 3)    │ ✅ Yes    │ Fixed, unchangeable data     │
│ set         │ {1, 2, 3}    │ ❌ No     │ Unique values, fast lookups  │
│ dict        │ {"k": "v"}   │ ✅ Yes*   │ Key-value pairs              │
└─────────────┴──────────────┴───────────┴──────────────────────────────┘
* dict maintains insertion order since Python 3.7
```

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-lists.md](concepts/lesson-01-lists.md) | List operations |
| 02 | [lesson-02-tuples.md](concepts/lesson-02-tuples.md) | Immutable sequences |
| 03 | [lesson-03-sets.md](concepts/lesson-03-sets.md) | Unique value collections |
| 04 | [lesson-04-dictionaries.md](concepts/lesson-04-dictionaries.md) | Key-value storage |
| 05 | [lesson-05-comprehensions.md](concepts/lesson-05-comprehensions.md) | List/dict comprehensions |
| 06 | [lesson-06-nested.md](concepts/lesson-06-nested.md) | Nested data structures |

---

## Guided Projects

| Project | Skills |
|---------|--------|
| [Shopping Cart](guided-projects/project-01-shopping-cart/) | Lists, calculations |
| [Student Management](guided-projects/project-02-student-management/) | Dictionaries, sorting |
| [Inventory System](guided-projects/project-03-inventory-system/) | Full CRUD with collections |

---

## ✅ Completion Checklist

- [ ] Can create and modify lists
- [ ] Know when to use tuple vs list
- [ ] Can perform set operations (union, intersection, difference)
- [ ] Can create dictionaries and use all dict methods
- [ ] Can write list and dictionary comprehensions
- [ ] Built Shopping Cart, Student Manager, Inventory

---

## Previous: [Phase 02](../phase-02-control-flow/README.md) | Next: [Phase 04](../phase-04-functions/README.md)
