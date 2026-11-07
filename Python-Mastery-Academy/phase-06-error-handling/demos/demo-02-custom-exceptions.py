"""
Demo 02 - Custom Exceptions
Phase 06: Error Handling

Run: python demo-02-custom-exceptions.py
"""

print("=" * 55)
print("DEMO 02 - Custom Exceptions")
print("=" * 55)

# --- EXCEPTION HIERARCHY ---
print("\n1. Creating a custom exception hierarchy:")

class AppError(Exception):
    """Base exception for this application."""

class ValidationError(AppError):
    """Input validation failure."""
    def __init__(self, field: str, value, message: str):
        self.field   = field
        self.value   = value
        self.message = message
        super().__init__(f"[{field}] {message} (got: {value!r})")

class NotFoundError(AppError):
    """Resource not found."""
    def __init__(self, resource: str, identifier):
        self.resource   = resource
        self.identifier = identifier
        super().__init__(f"{resource} not found: {identifier!r}")

class BusinessRuleError(AppError):
    """Business rule violation."""

# --- RAISING CUSTOM EXCEPTIONS ---
print("\n2. Raising custom exceptions:")

def validate_age(age: int) -> None:
    if not isinstance(age, int):
        raise ValidationError("age", age, "Must be an integer")
    if age < 0 or age > 150:
        raise ValidationError("age", age, "Must be between 0 and 150")

def find_employee(emp_id: str) -> dict:
    db = {"E001": {"name": "Alice", "salary": 85000}}
    if emp_id not in db:
        raise NotFoundError("Employee", emp_id)
    return db[emp_id]

def apply_raise(employee: dict, percentage: float) -> dict:
    if percentage > 50:
        raise BusinessRuleError(
            f"Raise of {percentage}% exceeds company policy maximum (50%)"
        )
    employee["salary"] *= (1 + percentage / 100)
    return employee

# Test each
for test_age in [30, -5, "abc", 200]:
    try:
        validate_age(test_age)
        print(f"  Age {test_age}: valid")
    except ValidationError as e:
        print(f"  ValidationError: {e}")

print()
for emp_id in ["E001", "E999"]:
    try:
        emp = find_employee(emp_id)
        print(f"  Found: {emp['name']}")
    except NotFoundError as e:
        print(f"  NotFoundError: {e}")

print()
try:
    emp = {"name": "Bob", "salary": 60000}
    apply_raise(emp, 75)
except BusinessRuleError as e:
    print(f"  BusinessRuleError: {e}")

# --- CATCHING BY BASE CLASS ---
print("\n3. Catching by base class:")
operations = [
    lambda: validate_age(-1),
    lambda: find_employee("MISSING"),
    lambda: apply_raise({"salary": 1}, 99),
]

for op in operations:
    try:
        op()
    except AppError as e:
        # Catches ANY of our custom errors
        print(f"  AppError ({type(e).__name__}): {e}")

print("\n4. Exception chaining with 'from':")
try:
    data = "abc"
    try:
        value = int(data)
    except ValueError as e:
        raise ValidationError("amount", data, "Must be numeric") from e
except ValidationError as e:
    print(f"  Caught: {e}")
    print(f"  Caused by: {e.__cause__}")
