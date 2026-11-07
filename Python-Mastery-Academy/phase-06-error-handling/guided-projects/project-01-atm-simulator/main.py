"""
Project 01 - ATM Simulator with Error Handling
Phase 06: Error Handling

SKILLS PRACTICED:
  - Custom exceptions
  - try/except/finally
  - Defensive programming
  - Input validation with clear error messages

HOW TO RUN:
  python main.py
"""

# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================

class ATMError(Exception):
    """Base ATM exception."""

class InsufficientFundsError(ATMError):
    def __init__(self, balance: float, requested: float):
        self.balance   = balance
        self.requested = requested
        super().__init__(
            f"Insufficient funds. Balance: ${balance:.2f}, Requested: ${requested:.2f}"
        )

class InvalidAmountError(ATMError):
    def __init__(self, amount):
        super().__init__(f"Invalid amount: {amount!r}. Must be a positive number.")

class DailyLimitError(ATMError):
    def __init__(self, limit: float, withdrawn: float):
        super().__init__(
            f"Daily withdrawal limit (${limit:.2f}) exceeded. "
            f"Already withdrawn today: ${withdrawn:.2f}"
        )

class CardBlockedError(ATMError):
    pass

class AccountInactiveError(ATMError):
    pass


# ============================================================
# ACCOUNT CLASS
# ============================================================

class ATMAccount:
    DAILY_LIMIT = 1000.0
    MAX_PIN_ATTEMPTS = 3

    def __init__(self, account_no: str, pin: str, balance: float):
        self._account_no = account_no
        self._pin        = pin
        self._balance    = balance
        self._active     = True
        self._blocked    = False
        self._pin_attempts = 0
        self._withdrawn_today = 0.0
        self._transactions: list[dict] = []

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def is_blocked(self) -> bool:
        return self._blocked

    def verify_pin(self, pin: str) -> bool:
        if self._blocked:
            raise CardBlockedError("Card is blocked. Contact your bank.")

        if pin == self._pin:
            self._pin_attempts = 0
            return True
        else:
            self._pin_attempts += 1
            remaining = self.MAX_PIN_ATTEMPTS - self._pin_attempts
            if remaining <= 0:
                self._blocked = True
                raise CardBlockedError(
                    "Too many incorrect PINs. Card blocked. Contact your bank."
                )
            raise ATMError(f"Wrong PIN. {remaining} attempt(s) remaining.")

    def deposit(self, amount: float) -> None:
        if not self._active:
            raise AccountInactiveError("Account is inactive.")
        self._validate_amount(amount)
        self._balance += amount
        self._record("DEPOSIT", amount)

    def withdraw(self, amount: float) -> None:
        if not self._active:
            raise AccountInactiveError("Account is inactive.")
        self._validate_amount(amount)

        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)

        new_daily = self._withdrawn_today + amount
        if new_daily > self.DAILY_LIMIT:
            remaining = self.DAILY_LIMIT - self._withdrawn_today
            raise DailyLimitError(self.DAILY_LIMIT, self._withdrawn_today)

        self._balance -= amount
        self._withdrawn_today += amount
        self._record("WITHDRAW", amount)

    def _validate_amount(self, amount) -> None:
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise InvalidAmountError(amount)
        if amount <= 0:
            raise InvalidAmountError(amount)

    def _record(self, txn_type: str, amount: float) -> None:
        from datetime import datetime
        self._transactions.append({
            "type":    txn_type,
            "amount":  amount,
            "balance": self._balance,
            "time":    datetime.now().strftime("%H:%M:%S")
        })

    def statement(self) -> list:
        return self._transactions.copy()


# ============================================================
# ATM INTERFACE
# ============================================================

def get_amount(prompt: str) -> float:
    """Get and validate amount from user."""
    raw = input(prompt).strip()
    try:
        amount = float(raw)
        if amount <= 0:
            raise InvalidAmountError(raw)
        return amount
    except ValueError:
        raise InvalidAmountError(raw)


def run_atm(account: ATMAccount) -> None:
    print("\n" + "=" * 45)
    print("  PYTHON ATM SIMULATOR")
    print("=" * 45)

    # PIN verification
    authenticated = False
    while not authenticated:
        try:
            pin = input("\n  Enter your PIN: ").strip()
            account.verify_pin(pin)
            print("  Access granted.")
            authenticated = True
        except CardBlockedError as e:
            print(f"\n  CARD BLOCKED: {e}")
            return
        except ATMError as e:
            print(f"  {e}")

    # Main menu
    while True:
        print(f"\n  Balance: ${account.balance:,.2f}")
        print("\n  [1] Check Balance")
        print("  [2] Deposit")
        print("  [3] Withdraw")
        print("  [4] Statement")
        print("  [5] Exit")

        choice = input("\n  Option: ").strip()

        try:
            if choice == "1":
                print(f"\n  Current balance: ${account.balance:,.2f}")

            elif choice == "2":
                amount = get_amount("  Deposit amount: $")
                account.deposit(amount)
                print(f"  Deposited ${amount:,.2f}. New balance: ${account.balance:,.2f}")

            elif choice == "3":
                amount = get_amount("  Withdrawal amount: $")
                account.withdraw(amount)
                print(f"  Withdrawn ${amount:,.2f}. New balance: ${account.balance:,.2f}")

            elif choice == "4":
                txns = account.statement()
                if not txns:
                    print("  No transactions yet.")
                else:
                    print(f"\n  {'Time':<10} {'Type':<10} {'Amount':>10} {'Balance':>12}")
                    print("  " + "-" * 46)
                    for t in txns:
                        print(f"  {t['time']:<10} {t['type']:<10} "
                              f"${t['amount']:>9,.2f} ${t['balance']:>11,.2f}")

            elif choice == "5":
                print("\n  Thank you. Goodbye!")
                break
            else:
                print("  Invalid option. Choose 1-5.")

        except InsufficientFundsError as e:
            print(f"\n  DECLINED: {e}")
        except DailyLimitError as e:
            print(f"\n  LIMIT REACHED: {e}")
        except InvalidAmountError as e:
            print(f"\n  INVALID INPUT: {e}")
        except AccountInactiveError as e:
            print(f"\n  ACCOUNT INACTIVE: {e}")
        except ATMError as e:
            print(f"\n  ATM ERROR: {e}")


def main():
    account = ATMAccount(
        account_no="ACC-001234",
        pin="1234",
        balance=2500.00
    )
    run_atm(account)


if __name__ == "__main__":
    main()
