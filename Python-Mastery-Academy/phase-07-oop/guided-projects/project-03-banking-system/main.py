"""
Project 03 — Banking System (OOP)
Phase 07: Object-Oriented Programming

SKILLS PRACTICED:
  - Classes and objects
  - Inheritance
  - Encapsulation (@property)
  - Custom exceptions
  - Polymorphism
  - Class methods

HOW TO RUN:
  python main.py
"""

from datetime import datetime
from abc import ABC, abstractmethod


# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================

class BankError(Exception):
    """Base exception for banking errors."""
    pass

class InsufficientFundsError(BankError):
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Insufficient funds: balance ${balance:.2f}, needed ${amount:.2f}")

class InvalidAmountError(BankError):
    def __init__(self, amount: float):
        super().__init__(f"Invalid amount: ${amount:.2f}. Must be positive.")

class AccountClosedError(BankError):
    pass


# ============================================================
# TRANSACTION CLASS
# ============================================================

class Transaction:
    """Records a single account transaction."""
    
    def __init__(self, transaction_type: str, amount: float, balance_after: float, description: str = ""):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.description = description
        self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        sign = "+" if self.transaction_type == "credit" else "-"
        desc = f"  {self.description}" if self.description else ""
        return f"  {time_str}  {sign}${self.amount:>9.2f}  Balance: ${self.balance_after:>10.2f}{desc}"


# ============================================================
# ABSTRACT ACCOUNT BASE CLASS
# ============================================================

class Account(ABC):
    """Abstract base class for all bank accounts."""
    
    _account_counter = 1000
    
    def __init__(self, owner_name: str, initial_deposit: float = 0.0):
        Account._account_counter += 1
        self._account_number = f"ACC{Account._account_counter:06d}"
        self._owner_name = owner_name
        self._balance = 0.0
        self._transactions: list[Transaction] = []
        self._is_active = True
        self._opened_date = datetime.now()
        
        if initial_deposit > 0:
            self._deposit_internal(initial_deposit, "Initial deposit")
    
    # ── Properties ──────────────────────────────────────
    
    @property
    def account_number(self) -> str:
        return self._account_number
    
    @property
    def owner_name(self) -> str:
        return self._owner_name
    
    @property
    def balance(self) -> float:
        return self._balance
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    # ── Internal helpers ────────────────────────────────
    
    def _validate_amount(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError(amount)
    
    def _check_active(self) -> None:
        if not self._is_active:
            raise AccountClosedError(f"Account {self._account_number} is closed.")
    
    def _deposit_internal(self, amount: float, description: str = "") -> None:
        self._balance += amount
        txn = Transaction("credit", amount, self._balance, description)
        self._transactions.append(txn)
    
    # ── Public methods ──────────────────────────────────
    
    def deposit(self, amount: float) -> None:
        self._check_active()
        self._validate_amount(amount)
        self._deposit_internal(amount, "Deposit")
        print(f"  ✅ Deposited ${amount:.2f}. New balance: ${self._balance:.2f}")
    
    @abstractmethod
    def withdraw(self, amount: float) -> None:
        """Withdrawal logic varies by account type."""
        pass
    
    def get_statement(self, last_n: int = None) -> None:
        transactions = self._transactions if last_n is None else self._transactions[-last_n:]
        print(f"\n  Account: {self._account_number}")
        print(f"  Owner:   {self._owner_name}")
        print(f"  Opened:  {self._opened_date.strftime('%Y-%m-%d')}")
        print(f"  Status:  {'Active' if self._is_active else 'Closed'}")
        print()
        print(f"  {'DATE & TIME':<22} {'AMOUNT':>11}  {'BALANCE':>12}  DESC")
        print("  " + "─" * 70)
        for txn in transactions:
            print(txn)
        print("  " + "─" * 70)
        print(f"  {'Current Balance:':>35} ${self._balance:>12.2f}")
    
    def close(self) -> None:
        self._is_active = False
        print(f"  Account {self._account_number} closed.")
    
    def __str__(self) -> str:
        status = "Active" if self._is_active else "Closed"
        return f"{self._account_number} | {self._owner_name:<20} | ${self._balance:>10.2f} | {status}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self._owner_name}', {self._balance})"


# ============================================================
# SAVINGS ACCOUNT
# ============================================================

class SavingsAccount(Account):
    """High-interest savings account with withdrawal limits."""
    
    INTEREST_RATE = 0.04     # 4% annual
    MAX_WITHDRAWALS = 6      # per month
    MIN_BALANCE = 500.0
    
    def __init__(self, owner_name: str, initial_deposit: float = 500.0):
        super().__init__(owner_name, initial_deposit)
        self._withdrawals_this_month = 0
    
    def withdraw(self, amount: float) -> None:
        self._check_active()
        self._validate_amount(amount)
        
        if self._withdrawals_this_month >= self.MAX_WITHDRAWALS:
            raise BankError("Monthly withdrawal limit (6) reached.")
        
        if self._balance - amount < self.MIN_BALANCE:
            raise BankError(f"Must maintain minimum balance of ${self.MIN_BALANCE:.2f}")
        
        if amount > self._balance:
            raise InsufficientFundsError(self._balance, amount)
        
        self._balance -= amount
        self._withdrawals_this_month += 1
        txn = Transaction("debit", amount, self._balance, "Withdrawal")
        self._transactions.append(txn)
        print(f"  ✅ Withdrew ${amount:.2f}. Balance: ${self._balance:.2f}")
    
    def apply_interest(self) -> float:
        """Apply monthly interest."""
        monthly_rate = self.INTEREST_RATE / 12
        interest = self._balance * monthly_rate
        self._deposit_internal(interest, f"Interest ({self.INTEREST_RATE*100:.0f}% p.a.)")
        return interest
    
    def __str__(self) -> str:
        return f"[SAVINGS] {super().__str__()}"


# ============================================================
# CHECKING ACCOUNT
# ============================================================

class CheckingAccount(Account):
    """Standard checking account with overdraft protection."""
    
    OVERDRAFT_LIMIT = 500.0
    OVERDRAFT_FEE = 35.0
    
    def __init__(self, owner_name: str, initial_deposit: float = 0.0):
        super().__init__(owner_name, initial_deposit)
    
    def withdraw(self, amount: float) -> None:
        self._check_active()
        self._validate_amount(amount)
        
        if self._balance - amount < -self.OVERDRAFT_LIMIT:
            raise InsufficientFundsError(self._balance + self.OVERDRAFT_LIMIT, amount)
        
        self._balance -= amount
        txn = Transaction("debit", amount, self._balance, "Withdrawal")
        self._transactions.append(txn)
        
        if self._balance < 0:
            self._balance -= self.OVERDRAFT_FEE
            fee_txn = Transaction("debit", self.OVERDRAFT_FEE, self._balance, "Overdraft fee")
            self._transactions.append(fee_txn)
            print(f"  ⚠️  Overdraft! Withdrew ${amount:.2f} + ${self.OVERDRAFT_FEE:.2f} fee. Balance: ${self._balance:.2f}")
        else:
            print(f"  ✅ Withdrew ${amount:.2f}. Balance: ${self._balance:.2f}")
    
    def __str__(self) -> str:
        return f"[CHECKING] {super().__str__()}"


# ============================================================
# BANK CLASS
# ============================================================

class Bank:
    """Manages all accounts at the bank."""
    
    def __init__(self, name: str):
        self.name = name
        self._accounts: dict[str, Account] = {}
    
    def open_savings(self, owner: str, initial: float = 500.0) -> SavingsAccount:
        acc = SavingsAccount(owner, initial)
        self._accounts[acc.account_number] = acc
        print(f"  ✅ Savings account opened: {acc.account_number}")
        return acc
    
    def open_checking(self, owner: str, initial: float = 0.0) -> CheckingAccount:
        acc = CheckingAccount(owner, initial)
        self._accounts[acc.account_number] = acc
        print(f"  ✅ Checking account opened: {acc.account_number}")
        return acc
    
    def get_account(self, account_number: str) -> Account:
        if account_number not in self._accounts:
            raise BankError(f"Account {account_number} not found.")
        return self._accounts[account_number]
    
    def transfer(self, from_num: str, to_num: str, amount: float) -> None:
        from_acc = self.get_account(from_num)
        to_acc = self.get_account(to_num)
        from_acc.withdraw(amount)
        to_acc.deposit(amount)
        print(f"  ✅ Transfer complete: ${amount:.2f} from {from_num} to {to_num}")
    
    def show_all_accounts(self) -> None:
        print(f"\n  {self.name} — All Accounts")
        print("  " + "─" * 65)
        total = 0.0
        for acc in self._accounts.values():
            print(f"  {acc}")
            if acc.is_active:
                total += acc.balance
        print("  " + "─" * 65)
        print(f"  {'Total deposits on file:':>40} ${total:>12,.2f}")


# ============================================================
# MAIN — DEMO
# ============================================================

def main():
    print("=" * 65)
    print("     PYTHON BANKING SYSTEM")
    print("     Built with OOP Principles")
    print("=" * 65)
    
    # Create bank
    bank = Bank("Python National Bank")
    
    print("\n1. Opening accounts...")
    savings = bank.open_savings("Alice Johnson", 2000.0)
    checking = bank.open_checking("Alice Johnson", 500.0)
    savings_bob = bank.open_savings("Bob Smith", 1500.0)
    
    print("\n2. Transactions...")
    savings.deposit(1000)
    savings.withdraw(500)
    checking.deposit(300)
    checking.withdraw(200)
    
    print("\n3. Applying savings interest...")
    interest = savings.apply_interest()
    print(f"  Interest earned: ${interest:.2f}")
    
    print("\n4. Transfer...")
    bank.transfer(checking.account_number, savings.account_number, 100)
    
    print("\n5. All accounts:")
    bank.show_all_accounts()
    
    print("\n6. Savings statement (last 5 transactions):")
    savings.get_statement(last_n=5)
    
    print("\n7. Error handling demo...")
    try:
        savings.withdraw(10000)
    except (InsufficientFundsError, BankError) as e:
        print(f"  ❌ {e}")
    
    print("\n" + "=" * 65)
    print("     Banking System Demo Complete!")
    print("=" * 65)


if __name__ == "__main__":
    main()
