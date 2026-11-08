# Phase 04 — Advanced Solutions: Functions

---

## Q1. Functional Pipeline

```python
from functools import partial

# ── enrich ───────────────────────────────────────────────────────────────────
def enrich(records):
    """Add derived fields to every sales record.

    We build a new list of shallow copies so the original data is never
    mutated — keeping this function pure and safe to call multiple times.
    """
    result = []
    for r in records:
        rec = dict(r)                           # shallow copy; avoids mutating caller's list
        sales = rec["sales"]
        rec["total"] = sum(sales)               # cumulative revenue across all periods
        rec["avg"]   = rec["total"] / len(sales)  # mean sale per period
        # best_month is 1-indexed so humans can match it to a calendar month
        rec["best_month"] = sales.index(max(sales)) + 1
        result.append(rec)
    return result

# ── filter_above ─────────────────────────────────────────────────────────────
def filter_above(records, threshold):
    """Keep only records where the per-period average exceeds threshold.

    Using a list comprehension keeps this a one-liner and returns a new list,
    which is consistent with our functional (no-mutation) style throughout.
    """
    return [r for r in records if r["avg"] > threshold]

# ── rank ─────────────────────────────────────────────────────────────────────
def rank(records):
    """Add a 1-based rank field sorted by total revenue (highest = rank 1).

    sorted() returns a brand-new list, so we never sort the input in place.
    enumerate(start=1) produces clean 1-indexed ranks without an off-by-one
    addition later.
    """
    ranked = sorted(records, key=lambda r: r["total"], reverse=True)
    for position, record in enumerate(ranked, start=1):
        record["rank"] = position   # mutating the dict entries is fine here
    return ranked                   # returning the newly ordered list

# ── format_report ─────────────────────────────────────────────────────────────
def format_report(records):
    """Convert enriched + ranked records into a human-readable string.

    Building a list of lines and joining at the end is more efficient than
    repeated string concatenation (avoids creating O(n) intermediate strings).
    Right-align rank and amounts; left-align the name for easy scanning.
    """
    lines = ["Sales Performance Report", "=" * 56]
    for r in records:
        lines.append(
            f"#{r['rank']:>2}  {r['name']:<12}  "
            f"Total: ${r['total']:>8,.2f}  "
            f"Avg: ${r['avg']:>7,.2f}  "
            f"Best Month: {r['best_month']}"
        )
    lines.append("=" * 56)
    return "\n".join(lines)

# ── pipeline ──────────────────────────────────────────────────────────────────
def pipeline(*functions):
    """Return a single callable that threads its argument through every function.

    Prefer left-to-right composition (data flows in reading order) over nested
    calls like f(g(h(data))), which reads inside-out and is harder to follow.

    The returned `run` closure captures `functions` via the enclosing scope —
    a practical example of how closures carry state without classes.
    """
    def run(data):
        result = data
        for func in functions:
            result = func(result)   # each stage receives the previous stage's output
        return result
    return run

# ── demo ──────────────────────────────────────────────────────────────────────
data = [
    {"name": "Alice", "sales": [1200, 800, 1500,  950]},
    {"name": "Bob",   "sales": [ 900, 1100, 750, 1300]},
    {"name": "Carol", "sales": [1800, 2100, 1700, 1900]},
    {"name": "Dave",  "sales": [ 600,  550,  700,  480]},  # avg ≈ 582 — filtered out
]

# partial() freezes `threshold=1000` so filter_above fits the
# single-argument contract that pipeline() requires of every stage.
process = pipeline(
    enrich,
    partial(filter_above, threshold=1000),
    rank,
    format_report,
)
print(process(data))
```

---

## Q2. Recursive Tree Processor

```python
# ── sample org-chart ─────────────────────────────────────────────────────────
org = {
    "name": "CEO", "salary": 200000,
    "reports": [
        {
            "name": "CTO", "salary": 150000,
            "reports": [
                {"name": "Lead Dev", "salary": 90000, "reports": []},
                {"name": "DevOps",   "salary": 85000, "reports": []},
            ],
        },
        {
            "name": "CFO", "salary": 140000,
            "reports": [
                {"name": "Accountant", "salary": 70000, "reports": []},
            ],
        },
    ],
}

# ── total_headcount ───────────────────────────────────────────────────────────
def total_headcount(node):
    """Count every employee in the subtree rooted at node.

    Base case : a leaf node (no reports) contributes exactly 1.
    Recursive : this node (1) + the headcount of every subtree.
    Using node.get("reports") safely handles nodes where the key is absent.
    """
    if not node.get("reports"):     # empty list or missing key → leaf
        return 1
    return 1 + sum(total_headcount(r) for r in node["reports"])

# ── total_payroll ─────────────────────────────────────────────────────────────
def total_payroll(node):
    """Sum all salaries in the subtree — same leaf/branch pattern as headcount."""
    if not node.get("reports"):
        return node["salary"]
    return node["salary"] + sum(total_payroll(r) for r in node["reports"])

# ── find_by_name ──────────────────────────────────────────────────────────────
def find_by_name(node, name):
    """DFS search; returns the matching dict or None.

    Early return (short-circuit) stops searching the rest of the tree the
    moment we find a match — important for large org-charts.
    Names are assumed unique; first match wins.
    """
    if node["name"] == name:
        return node
    for report in node.get("reports", []):
        found = find_by_name(report, name)
        if found:                   # truthy dict means we found it; stop searching
            return found
    return None                     # explicit None signals "not in this subtree"

# ── max_depth ─────────────────────────────────────────────────────────────────
def max_depth(node):
    """Return the depth of the deepest leaf (root counts as depth 1).

    A single-employee company has depth 1.
    Each level of reports adds 1 to the deepest branch.
    max() picks the longest path; we never look at the shortest.
    """
    if not node.get("reports"):
        return 1                    # leaf: only itself
    return 1 + max(max_depth(r) for r in node["reports"])

# ── flatten_org ───────────────────────────────────────────────────────────────
def flatten_org(node, depth=0):
    """Produce a flat list of (depth, name, salary) for every node.

    depth=0 for the CEO, depth=1 for direct reports, etc.
    Passing depth as a parameter (not a global or class variable) keeps the
    function re-entrant and easy to call on any subtree independently.
    list.extend() avoids creating many intermediate lists compared to + concat.
    """
    result = [(depth, node["name"], node["salary"])]
    for report in node.get("reports", []):
        result.extend(flatten_org(report, depth + 1))   # recurse one level deeper
    return result

# ── demo ──────────────────────────────────────────────────────────────────────
print("Headcount:", total_headcount(org))               # 6
print("Payroll:  $", f"{total_payroll(org):,}")         # $735,000
cto = find_by_name(org, "CTO")
print("Found:    ", cto["name"], f"(${cto['salary']:,})")
print("Max depth:", max_depth(org))                     # 3  (CEO → CTO → Lead Dev)

print("\nOrg chart:")
for depth, name, salary in flatten_org(org):
    indent = "  " * depth
    print(f"{indent}{name}: ${salary:,}")
```

---

## Q3. Decorator Factory

```python
import time
import logging
import functools

# ── retry ─────────────────────────────────────────────────────────────────────
def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """Retry the decorated function up to max_attempts times on failure.

    Only catches the specified exception types — anything else propagates
    immediately so genuine programming errors are never silently swallowed.

    Linear back-off (delay * attempt_number) avoids hammering a failing service
    while still retrying quickly on the first attempt.

    functools.wraps preserves __name__, __doc__, and signature so the decorated
    function looks identical to the original from outside.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)    # success → return immediately
                except exceptions as err:
                    last_error = err
                    if attempt < max_attempts:
                        time.sleep(delay * attempt)  # linear back-off between retries
            raise last_error    # all attempts exhausted; re-raise the last exception
        return wrapper
    return decorator

# ── log_calls ─────────────────────────────────────────────────────────────────
def log_calls(logger=None, level="DEBUG"):
    """Log every call's arguments and return value at the chosen log level.

    getattr(logging_obj, level.lower()) resolves the string "DEBUG" to the
    actual .debug() method at decoration time, not on every call — one lookup
    instead of repeated string comparisons at runtime.

    Passing logger=None falls back to the root logger so the decorator works
    without a pre-configured Logger object.
    """
    log_obj = logging.getLogger(logger)         # getLogger(None) → root logger
    log_fn  = getattr(log_obj, level.lower())   # e.g. log_obj.debug

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log_fn(f"→ {func.__name__}  args={args}  kwargs={kwargs}")
            result = func(*args, **kwargs)
            log_fn(f"← {func.__name__} returned {result!r}")
            return result
        return wrapper
    return decorator

# ── validate_args ─────────────────────────────────────────────────────────────
def validate_args(**rules):
    """Validate keyword arguments against predicate callables.

    Each key in rules maps to a predicate: validate_args(amount=lambda x: x>0).
    Only keyword arguments that are both present in the call AND listed in rules
    are checked — so positional-only calls are unaffected, and extra keyword
    arguments silently pass through without error.

    Raises ValueError with a descriptive message so callers get useful feedback
    rather than a cryptic downstream failure.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg_name, predicate in rules.items():
                if arg_name in kwargs:              # only validate if explicitly passed
                    if not predicate(kwargs[arg_name]):
                        raise ValueError(
                            f"Argument '{arg_name}={kwargs[arg_name]!r}' "
                            f"failed validation"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ── demo ──────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.DEBUG, format="%(name)s  %(levelname)s  %(message)s")
my_logger = "payment"

# Decorators are applied bottom-up: validate_args runs first, then log_calls,
# then retry wraps the whole thing.  Stack order matters for observability —
# log_calls sits inside retry so each individual attempt is logged.
@retry(max_attempts=3, delay=0.1, exceptions=(ConnectionError,))
@log_calls(logger=my_logger, level="DEBUG")
@validate_args(amount=lambda x: x > 0)
def process_payment(amount: float, currency: str = "USD") -> dict:
    return {"status": "ok", "amount": amount, "currency": currency}

print(process_payment(amount=99.99, currency="GBP"))

try:
    process_payment(amount=-5)      # validate_args rejects negative amounts
except ValueError as e:
    print(f"Caught: {e}")
```

---

## Q4. Generic Aggregator

```python
from collections import defaultdict

def aggregate(data, group_by, *metrics):
    """Group records by a field and compute multiple aggregate metrics at once.

    Parameters
    ----------
    data      : iterable of dicts
    group_by  : str — the field name to group by (e.g. "region")
    *metrics  : variable number of (result_name, field, func) tuples
                func receives a plain list of field values for the group

    Returns a list of dicts — one per unique group value — each containing
    the group key and every computed metric.

    Two-phase design:
      Phase 1 — bucket raw values into defaultdict(list) per group.
                This separates data gathering from aggregation, and means
                each metric function sees the full list rather than a running
                accumulator, which is required for functions like median().
      Phase 2 — apply each metric function to its bucket and build output rows.
                Each function is called once per group per metric — not once
                per record — keeping complexity O(groups × metrics).
    """
    # Phase 1: collect raw field values per group
    # buckets[group_value][field_name] = [val1, val2, ...]
    buckets = defaultdict(lambda: defaultdict(list))
    for record in data:
        group_value = record[group_by]
        for _, field, _ in metrics:             # only collect fields we'll aggregate
            buckets[group_value][field].append(record[field])

    # Phase 2: apply metric functions to each group's collected values
    result = []
    for group_value, field_lists in buckets.items():
        row = {group_by: group_value}           # start with the group key itself
        for metric_name, field, func in metrics:
            row[metric_name] = func(field_lists[field])   # e.g. sum([1200, 800, 1100])
        result.append(row)

    return result

# ── demo ──────────────────────────────────────────────────────────────────────
sales_data = [
    {"region": "North", "amount": 1200, "rep": "Alice"},
    {"region": "North", "amount":  800, "rep": "Bob"},
    {"region": "South", "amount": 1500, "rep": "Carol"},
    {"region": "South", "amount":  900, "rep": "Dave"},
    {"region": "North", "amount": 1100, "rep": "Eve"},
]

result = aggregate(
    sales_data,
    "region",
    ("total",   "amount", sum),
    ("average", "amount", lambda x: round(sum(x) / len(x), 2)),
    ("count",   "amount", len),
    ("max",     "amount", max),
)
for row in result:
    print(row)
# {'region': 'North', 'total': 3100, 'average': 1033.33, 'count': 3, 'max': 1200}
# {'region': 'South', 'total': 2400, 'average': 1200.0,  'count': 2, 'max': 1500}
```

---

## Q5. Lazy Evaluation

```python
from itertools import islice

class Query:
    """Lazy, chainable query builder for sequences of dicts.

    Each method returns a *new* Query instance so calls can be chained
    without mutating any existing state (immutable builder pattern).

    No data is consumed until the Query is iterated (via __iter__).
    This means you can construct a query once and iterate it many times,
    or pass it to functions without worrying about side effects.

    Execution order: filter → project → sort → limit.
    Sorting requires materialising the stream (you can't sort a generator),
    so it is placed as late as possible — after all cheap lazy operations.
    """

    def __init__(self, source):
        self._source      = source   # any iterable: list, generator, file, ...
        self._predicates  = []       # list of filter lambdas (all must pass)
        self._projection  = None     # optional transform; applied after filtering
        self._sort_key    = None     # field name for ascending sort
        self._limit_n     = None     # maximum records to yield

    # ── builder methods ───────────────────────────────────────────────────────

    def where(self, predicate):
        """Add a filter predicate.  Multiple .where() calls are AND-ed."""
        q = self._clone()
        q._predicates.append(predicate)  # accumulate; all must be True to pass
        return q

    def select(self, projection):
        """Transform each record with projection(record).
        Replaces any previous projection — only one transform is active."""
        q = self._clone()
        q._projection = projection
        return q

    def order_by(self, key):
        """Sort results ascending by the named field.
        Applied after all filters so we sort the minimal result set."""
        q = self._clone()
        q._sort_key = key
        return q

    def limit(self, n):
        """Yield at most n records.  Uses itertools.islice so it stays lazy."""
        q = self._clone()
        q._limit_n = n
        return q

    # ── internal helpers ──────────────────────────────────────────────────────

    def _clone(self):
        """Shallow-copy this query so chained methods don't share mutable state.

        Lists are copied (not aliased) so appending a predicate to a derived
        query doesn't affect the parent query — each branch is independent.
        """
        q = Query(self._source)
        q._predicates = list(self._predicates)   # new list, same lambda objects
        q._projection = self._projection
        q._sort_key   = self._sort_key
        q._limit_n    = self._limit_n
        return q

    # ── execution ─────────────────────────────────────────────────────────────

    def __iter__(self):
        """Execute the query lazily; each operation wraps the previous generator.

        Generator chaining means only the records that pass every filter are
        ever projected or sorted, avoiding unnecessary work on large datasets.
        """
        stream = iter(self._source)

        # Layer each predicate as a lazy generator filter (AND semantics)
        for pred in self._predicates:
            stream = (r for r in stream if pred(r))

        # Projection: transform lazily before sorting
        if self._projection:
            stream = (self._projection(r) for r in stream)

        # Sorting must materialise the stream — unavoidable for a full sort
        if self._sort_key:
            key = self._sort_key                  # capture for the lambda
            stream = iter(sorted(stream, key=lambda r: r[key]))

        # islice keeps memory bounded even after the sort materialised the data
        if self._limit_n is not None:
            stream = islice(stream, self._limit_n)

        yield from stream   # delegate iteration to the final composed generator

# ── demo ──────────────────────────────────────────────────────────────────────
employees = [
    {"name": "Alice",  "dept": "Engineering", "salary": 95000},
    {"name": "Bob",    "dept": "Marketing",   "salary": 55000},
    {"name": "Carol",  "dept": "Engineering", "salary": 72000},
    {"name": "Dave",   "dept": "Finance",     "salary": 68000},
    {"name": "Eve",    "dept": "Engineering", "salary": 88000},
    {"name": "Frank",  "dept": "Marketing",   "salary": 61000},
    {"name": "Grace",  "dept": "Finance",     "salary": 75000},
]

# Build the query once; nothing runs yet
query = (
    Query(employees)
    .where(lambda e: e["salary"] > 60000)       # exclude Bob (55k)
    .select(lambda e: {"name": e["name"], "dept": e["dept"]})  # drop salary
    .order_by("name")                           # alphabetical
    .limit(5)                                   # top 5 results
)

# Iteration triggers execution
for record in query:
    print(record)
# {'name': 'Alice',  'dept': 'Engineering'}
# {'name': 'Carol',  'dept': 'Engineering'}
# {'name': 'Dave',   'dept': 'Finance'}
# {'name': 'Eve',    'dept': 'Engineering'}
# {'name': 'Frank',  'dept': 'Marketing'}
```
