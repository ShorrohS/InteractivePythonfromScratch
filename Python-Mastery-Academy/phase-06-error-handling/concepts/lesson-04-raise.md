# Lesson 04 — raise and Custom Exceptions

**Phase:** 06 — Error Handling | **Time:** ~30 min

---

## Part 1: raise

You can deliberately raise exceptions when conditions are violated:

```python
def set_age(age: int) -> None:
    if age < 0:
        raise ValueError(f"Age cannot be negative: {age}")
    if age > 150:
        raise ValueError(f"Age {age} is unrealistically high")
    print(f"Age set to: {age}")

set_age(25)    # Works
set_age(-5)    # ValueError: Age cannot be negative: -5
```

---

## Part 2: When to Use raise

```python
# 1. Validate inputs to functions
def calculate_discount(price: float, pct: float) -> float:
    if price < 0:
        raise ValueError(f"Price cannot be negative: {price}")
    if not 0 <= pct <= 100:
        raise ValueError(f"Discount must be 0-100, got {pct}")
    return price * (1 - pct / 100)

# 2. Re-raise after logging
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    raise    # Re-raises the original exception

# 3. Convert low-level exceptions to meaningful ones
try:
    conn = connect_to_database()
except ConnectionError as e:
    raise DatabaseConnectionError(f"Cannot connect to DB: {e}") from e
```

---

## Part 3: Custom Exception Classes

Create your own exception hierarchy:

```python
# Base exception for your application
class AppError(Exception):
    """Base class for all application errors."""
    pass


# Specific exceptions inherit from AppError
class ValidationError(AppError):
    """Raised when input data fails validation."""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")


class AuthenticationError(AppError):
    """Raised when authentication fails."""
    pass


class InsufficientFundsError(AppError):
    """Raised when account has insufficient funds."""
    def __init__(self, balance: float, required: float):
        self.balance = balance
        self.required = required
        super().__init__(
            f"Insufficient funds: need ${required:.2f}, have ${balance:.2f}"
        )

# Using custom exceptions
def transfer_money(from_account, to_account, amount: float) -> None:
    if amount <= 0:
        raise ValidationError("amount", "Must be positive")
    if from_account.balance < amount:
        raise InsufficientFundsError(from_account.balance, amount)
    from_account.balance -= amount
    to_account.balance += amount

# Catching custom exceptions
try:
    transfer_money(account_a, account_b, 1000)
except ValidationError as e:
    print(f"Invalid input: {e.field} — {e.message}")
except InsufficientFundsError as e:
    print(f"Transfer failed: {e}")
    print(f"  Balance: ${e.balance:.2f}")
    print(f"  Needed:  ${e.required:.2f}")
except AppError as e:
    print(f"Application error: {e}")
```

---

## Part 4: Exception Hierarchy Best Practices

```python
class BankingError(Exception):
    """Root exception for banking system."""

class AccountError(BankingError):
    """Account-related errors."""

class TransactionError(BankingError):
    """Transaction-related errors."""

class InsufficientFundsError(TransactionError):
    """Not enough money for transaction."""

class AccountClosedError(AccountError):
    """Operation on closed account."""

class InvalidAmountError(TransactionError):
    """Invalid transaction amount."""

# Benefits:
# 1. Catch specific type: except InsufficientFundsError
# 2. Catch group: except TransactionError
# 3. Catch all app errors: except BankingError
# 4. Never accidentally catch system errors
```

---

## Part 5: Practice Exercises

1. Write a `safe_divide(a, b)` function that raises `ValueError` with a descriptive message when b is 0.

2. Create a `UserError` hierarchy with `UsernameError` and `PasswordError`. Raise appropriate ones in a registration function.

3. Write a function that validates email format and raises `ValidationError` if invalid.

4. Write a temperature converter that raises `ValueError` for temperatures below absolute zero (-273.15°C).

---

## Next Lesson

**→ Build the [ATM Simulator Project](../guided-projects/project-01-atm-simulator/)**
