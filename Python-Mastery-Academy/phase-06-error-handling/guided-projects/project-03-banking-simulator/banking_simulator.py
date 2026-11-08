"""
Project 03 - Banking Simulator
Phase 06: Error Handling

SKILLS PRACTICED:
  - Custom exception hierarchy (BankingError base class)
  - InsufficientFundsError with contextual attributes
  - InvalidAmountError
  - Defensive programming — validate before mutating state
  - Atomic transfer (reversal on failure)
  - Transaction history (list of dicts)
  - Catching at specific vs base-class level

HOW TO RUN:
  python banking_simulator.py
"""

from datetime import datetime


# ===========================================================
# STEP 1 — BankingError (base exception)
#
# All custom banking exceptions inherit from this class.
# This gives callers a single type they can catch to handle
# ANY banking problem — while still allowing specific catches
# when the caller needs to distinguish between error types.
#
# Pattern:
#   except BankingError:           ← catches every banking error
#   except InsufficientFundsError: ← catches only overdrafts
# ===========================================================

class BankingError(Exception):
    """Base exception for all banking operations in this simulator."""


# ===========================================================
# STEP 2 — InsufficientFundsError
#
# Raised when a withdrawal or transfer would overdraw the account.
#
# WHY store attributes?
# The caller may need the numbers to build a helpful UI message
# (e.g. "You need $250 more — would you like to transfer a smaller
# amount?").  Storing them as attributes avoids string-parsing.
# ===========================================================

class InsufficientFundsError(BankingError):
    """
    Raised when a withdrawal or transfer exceeds the available balance.

    Attributes:
        balance   — the account's balance at the time of the attempt
        amount    — the amount that was requested
        shortfall — how much more money would be needed (amount - balance)
    """

    def __init__(self, balance: float, amount: float):
        self.balance   = balance
        self.amount    = amount
        self.shortfall = amount - balance   # always positive when raised

        # Build a descriptive message that surfaces the key numbers.
        # Callers who just print(e) get all the context they need.
        super().__init__(
            f"Insufficient funds. "
            f"Requested: ${amount:,.2f} | "
            f"Balance: ${balance:,.2f} | "
            f"Shortfall: ${self.shortfall:,.2f}"
        )


# ===========================================================
# STEP 3 — InvalidAmountError
#
# Raised for zero, negative, or non-numeric amounts.
# Storing 'amount' lets callers log the bad value or show it
# back to the user without parsing the error string.
# ===========================================================

class InvalidAmountError(BankingError):
    """
    Raised when an amount is invalid: zero, negative, or not a number.

    Attributes:
        amount — the value that was rejected
    """

    def __init__(self, amount):
        self.amount = amount
        super().__init__(
            f"Invalid amount: {amount!r}. "
            "Amount must be a positive number."
        )


# ===========================================================
# STEP 4 — BankAccount
#
# Design decisions worth noting:
#
# 1. __balance is name-mangled (private).  External code cannot
#    write self.__balance; they can only read through @property.
#    This enforces the invariant that balance only changes via
#    deposit() / withdraw() — never by accident.
#
# 2. Every public method calls _validate_amount() BEFORE changing
#    any state.  The account is therefore never left in a broken
#    intermediate state if an exception is raised.
#
# 3. transfer() is atomic: if the deposit to 'target' fails after
#    the withdrawal has already happened, we reverse the withdrawal.
# ===========================================================

class BankAccount:
    """
    A bank account with defensive programming and transaction history.
    """

    def __init__(self, owner: str, initial_balance: float = 0.0):
        # ── Preconditions ──────────────────────────────────────
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("owner must be a non-empty string")
        if isinstance(initial_balance, bool):
            raise InvalidAmountError(initial_balance)
        if not isinstance(initial_balance, (int, float)):
            raise InvalidAmountError(initial_balance)
        if initial_balance < 0:
            raise InvalidAmountError(initial_balance)

        self.owner                   = owner.strip()
        self.__balance               = float(initial_balance)
        self.transaction_history: list = []

    # ─────────────────────────────────────────────────────────
    # Read-only property
    # Callers can READ balance but cannot SET it directly.
    # ─────────────────────────────────────────────────────────

    @property
    def balance(self) -> float:
        return self.__balance

    # ─────────────────────────────────────────────────────────
    # Private helpers
    # ─────────────────────────────────────────────────────────

    def _validate_amount(self, amount) -> float:
        """
        Central validation for all monetary amounts.

        Returns the amount as a float if it is valid.
        Raises InvalidAmountError otherwise.

        Using a helper avoids duplicating the same type/range
        checks in deposit(), withdraw(), and transfer().
        """
        # bool is a subclass of int, so we reject it explicitly
        # to avoid treating True (1) as a valid $1 deposit.
        if isinstance(amount, bool):
            raise InvalidAmountError(amount)
        if not isinstance(amount, (int, float)):
            raise InvalidAmountError(amount)
        if amount <= 0:
            raise InvalidAmountError(amount)
        return float(amount)

    def _record(self, txn_type: str, amount: float,
                note: str = "") -> None:
        """Append one entry to the transaction history."""
        self.transaction_history.append({
            "type":          txn_type,
            "amount":        amount,
            "balance_after": self.__balance,
            "timestamp":     datetime.now().strftime("%H:%M:%S"),
            "note":          note,
        })

    # ─────────────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────────────

    def deposit(self, amount) -> None:
        """
        Add funds to the account.

        Raises:
            InvalidAmountError — if amount is not a positive number
        """
        # Validate FIRST — state only changes after this line.
        amount = self._validate_amount(amount)

        self.__balance += amount
        self._record("DEPOSIT", amount)
        print(f"  {self.owner} deposits ${amount:,.2f}   "
              f"→ balance: ${self.__balance:,.2f}")

    def withdraw(self, amount) -> None:
        """
        Remove funds from the account.

        We check balance BEFORE decrementing so the account
        is never left in a partially-updated state.

        Raises:
            InvalidAmountError     — if amount is not a positive number
            InsufficientFundsError — if balance < amount
        """
        amount = self._validate_amount(amount)

        # Check funds before touching state.
        if amount > self.__balance:
            raise InsufficientFundsError(self.__balance, amount)

        self.__balance -= amount
        self._record("WITHDRAW", amount)
        print(f"  {self.owner} withdraws ${amount:,.2f}  "
              f"→ balance: ${self.__balance:,.2f}")

    def transfer(self, amount, target: "BankAccount") -> None:
        """
        Move funds from this account to 'target'.

        Atomicity: the withdrawal and the deposit are treated as
        a single unit.  If the deposit to 'target' fails for any
        reason AFTER the withdrawal has already happened, we
        reverse the withdrawal so both accounts stay consistent.

        Raises:
            InvalidAmountError     — if amount is not a positive number
            InsufficientFundsError — if this account cannot cover amount
        """
        amount = self._validate_amount(amount)

        # ── Step 1: withdraw from self ─────────────────────────
        # Check balance before changing state (same pattern as withdraw).
        if amount > self.__balance:
            raise InsufficientFundsError(self.__balance, amount)

        self.__balance -= amount
        self._record("TRANSFER_OUT", amount, note=f"→ {target.owner}")

        # ── Step 2: deposit to target ─────────────────────────
        # Wrapped in try/except so any unexpected failure here
        # triggers an automatic reversal of the withdrawal above.
        try:
            # Direct attribute access via name-mangling from within
            # the same class is fine — this is intentional encapsulation.
            target._BankAccount__balance += amount
            target._record("TRANSFER_IN", amount, note=f"← {self.owner}")
            print(f"  Transfer ${amount:,.2f} from {self.owner} "
                  f"to {target.owner}")
            print(f"    {self.owner}: ${self.__balance:,.2f}  |  "
                  f"{target.owner}: ${target._BankAccount__balance:,.2f}")
        except Exception as original_error:
            # Reversal — put the money back so neither account is wrong.
            self.__balance += amount
            self.transaction_history.pop()    # remove the TRANSFER_OUT
            raise BankingError(
                f"Transfer to {target.owner} failed; "
                f"withdrawal reversed. Cause: {original_error}"
            ) from original_error

    def get_statement(self) -> None:
        """Print a formatted account statement."""
        print(f"\n  Statement — {self.owner}")
        print(
            f"  {'Date/Time':<12} {'Type':<14} "
            f"{'Amount':>10}  {'Balance':>12}"
        )
        print("  " + "─" * 52)

        if not self.transaction_history:
            print("  No transactions recorded.")
        else:
            for txn in self.transaction_history:
                sign   = ("+" if txn["type"] in ("DEPOSIT", "TRANSFER_IN")
                          else "-")
                amount = f"{sign}${txn['amount']:,.2f}"
                bal    = f"${txn['balance_after']:,.2f}"
                note   = f"  {txn['note']}" if txn["note"] else ""
                print(
                    f"  {txn['timestamp']:<12} {txn['type']:<14} "
                    f"{amount:>10}  {bal:>12}{note}"
                )

        print(f"\n  Current balance: ${self.__balance:,.2f}")


# ===========================================================
# STEP 5 — main()
#
# Demonstrates the full exception hierarchy:
#   1. Successful transactions (no exceptions)
#   2. InvalidAmountError — negative deposit
#   3. InsufficientFundsError — overdraft
#   4. Both caught at base-class (BankingError) level
#   5. Formatted statements for both accounts
# ===========================================================

def main():
    print("=" * 60)
    print("BANKING SIMULATOR — Phase 06 Error Handling Project")
    print("=" * 60)

    # ── Create two accounts ──────────────────────────────────
    print("\n--- Creating accounts ---")
    alice = BankAccount("Alice", initial_balance=1000.00)
    bob   = BankAccount("Bob",   initial_balance=500.00)
    print(f"  Alice's account opened with ${alice.balance:,.2f}")
    print(f"  Bob's account opened with ${bob.balance:,.2f}")

    # ── Successful transactions ──────────────────────────────
    print("\n--- Successful transactions ---")
    alice.deposit(200)
    alice.withdraw(150)
    alice.transfer(300, bob)

    # ── Error scenarios ──────────────────────────────────────
    print("\n--- Error scenarios ---")

    # InvalidAmountError — negative deposit
    # We catch the specific type so we can access e.amount as an attribute.
    print("  Attempting negative deposit (-50):")
    try:
        alice.deposit(-50)
    except InvalidAmountError as e:
        print(f"  InvalidAmountError: {e}")
        print(f"    Rejected amount: {e.amount!r}")

    # InsufficientFundsError — requesting more than the balance
    # We catch specifically to access e.shortfall.
    print("\n  Attempting overdraft (request $2,000):")
    try:
        alice.withdraw(2000)
    except InsufficientFundsError as e:
        print(f"  InsufficientFundsError: {e}")
        print(f"    Shortfall: ${e.shortfall:,.2f}")

    # ── Catching at base-class level ─────────────────────────
    # BankingError catches BOTH subclasses.  type(e).__name__
    # tells us which specific one fired — useful for logging.
    print("\n--- Catching at base-class level ---")

    problem_ops = [
        lambda: alice.deposit(0),       # zero amount  → InvalidAmountError
        lambda: bob.withdraw(9999),     # overdraft    → InsufficientFundsError
    ]

    for op in problem_ops:
        try:
            op()
        except BankingError as e:
            print(f"  BankingError caught ({type(e).__name__}): {e}")

    # ── Print full statements ────────────────────────────────
    print("\n--- Account statements ---")
    alice.get_statement()
    bob.get_statement()


if __name__ == "__main__":
    main()
