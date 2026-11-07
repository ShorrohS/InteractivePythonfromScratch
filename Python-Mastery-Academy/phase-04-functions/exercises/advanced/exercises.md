# Phase 04 — Advanced Exercises: Functions

> These require combining multiple function concepts.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. Functional Pipeline**

Build a data processing pipeline using only functions:

```python
data = [
    {"name": "Alice", "sales": [1200, 800, 1500, 950]},
    {"name": "Bob",   "sales": [900, 1100, 750, 1300]},
    # ...
]
```

Write:
- `enrich(records)` → adds `total`, `avg`, `best_month` to each record
- `filter_above(records, threshold)` → keeps records where avg > threshold
- `rank(records)` → adds `rank` field
- `format_report(records)` → returns formatted string
- `pipeline(*functions)` → applies a sequence of functions in order

Call: `pipeline(enrich, partial(filter_above, threshold=1000), rank, format_report)(data)`

---

**Q2. Recursive Tree Processor**

Given a company org-chart as nested dicts:
```python
org = {
    "name": "CEO",
    "salary": 200000,
    "reports": [
        {"name": "CTO", "salary": 150000, "reports": [...]},
        ...
    ]
}
```

Write recursive functions:
- `total_headcount(org)` → count all employees
- `total_payroll(org)` → sum all salaries
- `find_by_name(org, name)` → return that employee's node
- `max_depth(org)` → depth of the deepest reporting chain
- `flatten_org(org, depth=0)` → list of (depth, name, salary) tuples

---

**Q3. Decorator Factory**

Build a production-quality decorator factory:

```python
@retry(max_attempts=3, delay=1.0, exceptions=(ConnectionError,))
@log_calls(logger=my_logger, level="DEBUG")
@validate_args(amount=lambda x: x > 0)
def process_payment(amount: float, currency: str = "USD") -> dict:
    ...
```

Implement all three decorators from scratch.

---

**Q4. Generic Aggregator**

Write a `aggregate(data, group_by, *metrics)` function where each metric is a `(name, key, func)` tuple:

```python
result = aggregate(
    sales_data,
    group_by="region",
    ("total", "amount", sum),
    ("average", "amount", lambda x: sum(x)/len(x)),
    ("count", "amount", len),
    ("max", "amount", max),
)
```

---

**Q5. Lazy Evaluation**

Using generators and closures, build a lazy query system:

```python
query = (
    Query(employees)
    .where(lambda e: e["salary"] > 60000)
    .select(lambda e: {"name": e["name"], "dept": e["dept"]})
    .order_by("name")
    .limit(5)
)
for record in query:
    print(record)
```

---

> **Solutions:** `../../solutions/advanced/solutions.md`
