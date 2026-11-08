# 🏦 Guided Project 03 — Banking Simulator

**Phase:** 06 — Error Handling
**Difficulty:** ⭐⭐ Intermediate
**Time:** ~60–90 minutes

---

## Project Goal

Build a `BankAccount` class that uses a custom exception hierarchy to communicate exactly what went wrong — and why — when a transaction fails. You will practise defensive programming throughout, implement a full transaction history, and catch exceptions at both the specific and base-class level.

---

## Learning Objectives

By completing this project you will be able to:

1. Design a custom exception hierarchy (`BankingError` → `InsufficientFundsError`, `InvalidAmountError`)
2. Attach business-relevant data to exception objects (`balance`, `amount`, `shortfall`) so callers can make informed decisions
3. Apply defensive programming in `deposit()`, `withdraw()`, and `transfer()` — validate before mutating state
4. Implement atomic transactions: if a `transfer()` partially fails, reverse the changes
5. Catch the same error at the specific level and at the base-class level
6. Build a transaction history (list of dicts) and print a formatted account statement

---

## Prerequisites

- Completed Phase 06 Lessons 01–05
- Familiar with custom exceptions (see Demo 02)
- Comfortable with Python classes and `@property`

---

## How to Run

```bash
python banking_simulator.py
```

No external input or files needed — `main()` runs a complete demo automatically.

---

## What You Will Build

Follow the comments inside `banking_simulator.py`. Each section is labelled **STEP N**.

### Step 1 — BankingError base exception

A simple base class so callers can catch *any* banking error with one `except` clause when they don't care about the specific type.

### Step 2 — InsufficientFundsError

Raised when a withdrawal or transfer would overdraw the account.

Stores three attributes so the caller can use the numbers programmatically:
- `balance` — what the account currently holds
- `amount` — what was requested
- `shortfall` — `amount - balance` (always positive when this exception is raised)

### Step 3 — InvalidAmountError

Raised when an amount is zero, negative, or not a number at all. Stores the rejected `amount` value.

### Step 4 — BankAccount class

- Private `__balance` (name-mangled) with a read-only `@property` — prevents accidental external mutation
- `deposit(amount)` — validates amount, updates balance, records transaction
- `withdraw(amount)` — validates amount, checks funds, records transaction
- `transfer(amount, target)` — withdraws from self, deposits to target; if the deposit step fails for any reason the withdrawal is reversed (atomicity)
- `transaction_history` — list of dicts with `type`, `amount`, `balance_after`, `timestamp`, `note`
- `get_statement()` — prints a formatted mini bank statement

### Step 5 — main()

Runs a complete demo:
1. Creates two accounts (Alice and Bob)
2. Successful deposit, withdrawal, and transfer
3. Triggers `InvalidAmountError` (negative deposit) — inspects `e.amount`
4. Triggers `InsufficientFundsError` (overdraft) — inspects `e.shortfall`
5. Catches both at the base-class level using `except BankingError`
6. Prints full statements for both accounts

---

## Sample Expected Output

```
============================================================
BANKING SIMULATOR — Phase 06 Error Handling Project
============================================================

--- Creating accounts ---
  Alice's account opened with $1,000.00
  Bob's account opened with $500.00

--- Successful transactions ---
  Alice deposits $200.00    → balance: $1,200.00
  Alice withdraws $150.00   → balance: $1,050.00
  Transfer $300.00 from Alice to Bob
    Alice: $750.00  |  Bob: $800.00

--- Error scenarios ---
  Attempting negative deposit (-50):
  InvalidAmountError: Invalid amount: -50. Amount must be a positive number.
    Rejected amount: -50

  Attempting overdraft (request $2,000):
  InsufficientFundsError: Insufficient funds. Requested: $2,000.00 | Balance: $750.00 | Shortfall: $1,250.00
    Shortfall: $1,250.00

--- Catching at base-class level ---
  BankingError caught (InvalidAmountError): Invalid amount: 0. ...
  BankingError caught (InsufficientFundsError): Insufficient funds. ...

--- Account statements ---

  Statement — Alice
  Date/Time    Type            Amount       Balance
  ────────────────────────────────────────────────────
  HH:MM:SS     DEPOSIT         +$200.00     $1,200.00
  HH:MM:SS     WITHDRAW        -$150.00     $1,050.00
  HH:MM:SS     TRANSFER_OUT    -$300.00       $750.00  → Bob

  Current balance: $750.00

  Statement — Bob
  Date/Time    Type            Amount       Balance
  ────────────────────────────────────────────────────
  HH:MM:SS     TRANSFER_IN     +$300.00     $800.00   ← Alice

  Current balance: $800.00
```

---

## Extension Challenges

Once the base project works, try these:

1. Add a `minimum_balance` parameter that prevents the account from going below a floor — define a new `MinimumBalanceError`
2. Add a `daily_withdrawal_limit` (like Project 01 — ATM Simulator)
3. Add a `freeze()` / `unfreeze()` method and raise a `FrozenAccountError` on any transaction attempt
4. Persist `transaction_history` to a JSON file using `json.dump` when the account object is deleted (`__del__`)

---

## Key Concepts Practiced

| Concept | Where Used |
|---------|-----------|
| Exception hierarchy | `BankingError` → `InsufficientFundsError`, `InvalidAmountError` |
| Exception attributes | `shortfall` on `InsufficientFundsError` |
| Defensive programming | `_validate_amount()` called at start of every method |
| State consistency | `transfer()` reverses withdrawal if deposit fails |
| Property encapsulation | `@property balance` — read-only external access |
| Transaction history | List of dicts built up over time |
| Base-class catching | `except BankingError` catches all subclasses |

---

## Next

**→ [Phase 07 — Object-Oriented Programming](../../../phase-07-oop/README.md)**
