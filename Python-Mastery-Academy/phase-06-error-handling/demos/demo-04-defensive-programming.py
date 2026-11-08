"""
Demo 04 - Defensive Programming
Phase 06: Error Handling

Run: python demo-04-defensive-programming.py
"""

print("=" * 55)
print("DEMO 04 - Defensive Programming")
print("=" * 55)

# --- 1. INPUT VALIDATION ---
print("\n1. Input validation:")

def validate_age(age) -> None:
    """
    Validates that 'age' is an int in the range 0–150.

    Raises TypeError  — if age is not an int (catches bool too,
                        since bool is a subclass of int).
    Raises ValueError — if age is an int but out of range.

    Defensive rule: check TYPE first, then VALUE.
    """
    # bool is a subclass of int, so isinstance(True, int) is True.
    # We reject booleans explicitly before the int check.
    if isinstance(age, bool):
        raise TypeError(f"age must be int, got bool")
    if not isinstance(age, int):
        raise TypeError(
            f"age must be int, got {type(age).__name__!r}"
        )
    if not 0 <= age <= 150:
        raise ValueError(
            f"age must be between 0 and 150, got {age}"
        )

test_values = [25, -1, 200, 3.5, "thirty", True, None]
for v in test_values:
    try:
        validate_age(v)
        print(f"  {v!r:12} → valid age")
    except TypeError as e:
        print(f"  {v!r:12} → TypeError:  {e}")
    except ValueError as e:
        print(f"  {v!r:12} → ValueError: {e}")


# --- 2. TYPE CHECKING ---
print("\n2. Type checking with isinstance():")

def calculate_area(side) -> float:
    """
    Accepts int or float; rejects anything else (including bool).
    Returns the area of a square with the given side length.

    Key lesson: isinstance(x, (int, float)) handles both numeric
    types with one call.  Always check bool BEFORE int because
    bool is a subclass of int.
    """
    if isinstance(side, bool):
        raise TypeError("Expected int or float, got bool")
    if not isinstance(side, (int, float)):
        raise TypeError(
            f"Expected int or float, got {type(side).__name__!r}"
        )
    if side <= 0:
        raise ValueError(f"Side length must be positive, got {side}")
    return float(side ** 2)

for v in [4, 3.5, True, "5", None, -2, 0]:
    try:
        area = calculate_area(v)
        print(f"  calculate_area({v!r:8}) = {area}")
    except (TypeError, ValueError) as e:
        print(f"  calculate_area({v!r:8}) → {type(e).__name__}: {e}")


# --- 3. GUARD CLAUSES ---
print("\n3. Guard clauses — early-return vs deep nesting:")

# ── BAD: deeply nested — hard to follow the happy path ──────
def process_order_nested(order: dict) -> str:
    if order is not None:
        if "user" in order:
            if "items" in order:
                if len(order["items"]) > 0:
                    if order.get("paid", False):
                        return "Order processed!"
                    else:
                        return "Order not paid"
                else:
                    return "No items in order"
            else:
                return "Missing 'items' key"
        else:
            return "Missing 'user' key"
    else:
        return "Order is None"

# ── GOOD: guard clauses — fail fast, flat structure ──────────
def process_order(order: dict) -> str:
    """
    Each guard clause handles one failure case and returns immediately.
    The happy path (last line) is reached only when every check passes.
    Flat is better than nested — one of Python's core design principles.
    """
    if order is None:
        return "Order is None"
    if "user" not in order:
        return "Missing 'user' key"
    if "items" not in order:
        return "Missing 'items' key"
    if len(order["items"]) == 0:
        return "No items in order"
    if not order.get("paid", False):
        return "Order not paid"

    return "Order processed!"   # happy path — one clear line

test_orders = [
    None,
    {},
    {"user": "Alice"},
    {"user": "Alice", "items": []},
    {"user": "Alice", "items": ["book"], "paid": False},
    {"user": "Alice", "items": ["book"], "paid": True},
]

print("  Nested version:")
for o in test_orders:
    print(f"    {str(o):<55} → {process_order_nested(o)}")

print("  Guard-clause version (same results, cleaner code):")
for o in test_orders:
    print(f"    {str(o):<55} → {process_order(o)}")


# --- 4. ASSERT STATEMENTS ---
print("\n4. assert statements — developer preconditions:")

def compute_discount(price: float, pct: float) -> float:
    """
    Compute a percentage discount on a price.

    assert is for DEVELOPER errors — things that should never
    happen if the calling code is correct.  Use assert to document
    and enforce your assumptions.

    Important: do NOT use assert for user-input validation.
    assert can be disabled with 'python -O', so user-facing
    checks must always use explicit 'if ... raise' instead.
    """
    assert isinstance(price, (int, float)) and not isinstance(price, bool), \
        "price must be numeric"
    assert price > 0,           f"price must be positive, got {price}"
    assert 0 <= pct <= 100,     f"pct must be 0–100, got {pct}"

    return price * (pct / 100)

print("  Valid calls:")
print(f"  10% of $50.00  = ${compute_discount(50.0,  10):.2f}")
print(f"  25% of $80.00  = ${compute_discount(80.0,  25):.2f}")
print(f"  100% of $20.00 = ${compute_discount(20.0, 100):.2f}")

print("  AssertionError for developer mistakes:")
try:
    compute_discount(-10, 20)       # violates price > 0
except AssertionError as e:
    print(f"  AssertionError: {e}")

try:
    compute_discount(100, 150)      # violates 0 <= pct <= 100
except AssertionError as e:
    print(f"  AssertionError: {e}")


# --- 5. LBYL vs EAFP ---
print("\n5. LBYL vs EAFP — two styles of defensive code:")

config = {
    "host":  "localhost",
    "port":  5432,
    "debug": True,
}

# ── LBYL — Look Before You Leap ─────────────────────────────
# Check that the key exists before accessing it.
# Downside: in multi-threaded code, the dict could change between
# the 'in' check and the access (TOCTOU race).  Also gets verbose
# when checking deeply nested structures.
def read_config_lbyl(d: dict, key: str):
    if key in d:
        return d[key]
    return None

# ── EAFP — Easier to Ask Forgiveness than Permission ────────
# Just try to do it; handle the failure if it occurs.
# This is idiomatic Python and avoids the TOCTOU issue.
# More readable for deeply nested access (e.g. d["a"]["b"]["c"]).
def read_config_eafp(d: dict, key: str):
    try:
        return d[key]
    except KeyError:
        return None

print("  LBYL results:")
for k in ["host", "port", "missing_key"]:
    val = read_config_lbyl(config, k)
    print(f"    read_config_lbyl({k!r:<15}) = {val!r}")

print("  EAFP results (identical output):")
for k in ["host", "port", "missing_key"]:
    val = read_config_eafp(config, k)
    print(f"    read_config_eafp({k!r:<15}) = {val!r}")

print("""
  Trade-off summary:
    LBYL — clear intent; good when the check is cheap and atomic.
    EAFP — idiomatic Python; better for file I/O, dict/attr access,
           and anywhere the access itself IS the only reliable test.
""")


# --- 6. PRECONDITION / POSTCONDITION ---
print("\n6. Preconditions and postconditions:")

import math

def safe_sqrt(value) -> float:
    """
    Compute the square root of a number.

    Precondition  — checked at START:  input must be usable.
    Postcondition — checked at END:    output must be correct.

    This pattern catches two classes of bug:
      1. Bad caller input  (precondition fires)
      2. Logic bugs in our own code  (postcondition fires)
    """
    # ── Preconditions ──────────────────────────────────────
    if isinstance(value, bool):
        raise TypeError("Expected a number, got bool")
    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Expected a number, got {type(value).__name__!r}"
        )
    if value < 0:
        raise ValueError(
            f"Cannot take sqrt of a negative number: {value}"
        )

    # ── Core logic ─────────────────────────────────────────
    result = math.sqrt(value)

    # ── Postcondition ──────────────────────────────────────
    # result² should equal value within floating-point tolerance.
    # If this assert fires, there is a bug in our logic — not in
    # the caller's input.
    assert abs(result * result - value) < 1e-9, (
        f"Postcondition failed: sqrt({value})² = {result * result} ≠ {value}"
    )

    return result

print("  Valid inputs:")
for v in [0, 4, 9, 2.25, 100]:
    print(f"  safe_sqrt({v!r:<6}) = {safe_sqrt(v):.4f}")

print("  Invalid inputs (preconditions):")
for v in [-1, "9", None, True]:
    try:
        safe_sqrt(v)
    except (TypeError, ValueError) as e:
        print(f"  safe_sqrt({v!r:<6}) → {type(e).__name__}: {e}")
