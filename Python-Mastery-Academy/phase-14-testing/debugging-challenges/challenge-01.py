"""
Debugging Challenge 01 — Phase 14: Testing
===========================================

INSTRUCTIONS:
  This file contains 7 bugs spread across a BankAccount class
  and a test suite for it.

  Find and fix every bug.
  When all bugs are fixed, every test method will pass and
  running the file will print "All bugs fixed — 7 tests passed!"

HINTS:
  - Read every error or failure message carefully
  - Some bugs cause errors; some cause tests to pass when they should fail
  - Fix one bug at a time, run the file, then move to the next
  - The bug hints are intentionally vague — work it out yourself first

STRUCTURE:
  Part 1 — BankAccount (the code under test)
  Part 2 — TestBankAccount (the test class)

DO NOT LOOK AT THE ANSWERS BELOW UNTIL YOU HAVE TRIED!
"""

# =============================================================================
# PART 1 — CODE UNDER TEST
# =============================================================================

class BankAccount:
    """A simple bank account with deposit, withdraw, and balance operations."""

    def __init__(self, owner, initial_balance=0):
        self.owner   = owner
        self._balance = initial_balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        return self._balance

    def get_balance(self):
        return self._balance

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"


# =============================================================================
# PART 2 — TEST CLASS
# =============================================================================

import unittest
from unittest.mock import patch


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        # Fresh account with $1000 before every test
        self.account = BankAccount("Alice", initial_balance=1000)

    # --- BUG 1 ---
    def test_initial_balance(self):
        # hint: check what value setUp gives the account
        self.assertEqual(self.account.get_balance(), 500)  # BUG 1: wrong expected value

    # --- BUG 2 ---
    def test_deposit_increases_balance(account):          # BUG 2: missing first parameter
        account.account.deposit(200)
        account.assertEqual(account.account.get_balance(), 1200)

    # --- BUG 3 ---
    def test_withdraw_reduces_balance(self):
        self.account.withdraw(400)
        self.assertEqual(self.account.get_balance(), 600)

    # --- BUG 4 ---
    def test_withdraw_raises_on_insufficient_funds(self):
        # hint: assertRaises must wrap the call that raises — not a different call
        with self.assertRaises(ValueError):
            self.account.get_balance()   # BUG 3: wrapping the wrong method

    # --- BUG 4 (fixture name mismatch demo using pytest style) ---
    # The test below is written as if it uses a pytest fixture called `fresh_account`,
    # but setUp creates `self.account`. This method ignores setUp entirely and tries
    # to use an undefined name.
    def test_deposit_with_wrong_fixture_name(self):
        fresh_account = BankAccount("Bob", 0)    # BUG 4: should use self.account from setUp,
        fresh_account.deposit(50)                #         not a locally constructed account
        self.assertEqual(self.account.get_balance(), 50)  # mismatch: self.account still has 1000

    # --- BUG 5 ---
    # This test mocks the wrong path.
    # The function `notify_low_balance` lives in THIS module (__main__),
    # but the patch target points to `banking_app.notify_low_balance`.
    @patch("banking_app.notify_low_balance")     # BUG 5: wrong import path
    def test_low_balance_notification(self, mock_notify):
        self.account.withdraw(950)               # balance → 50
        notify_low_balance(self.account)
        mock_notify.assert_called_once()

    # --- BUG 6 ---
    def test_balance_never_negative(self):
        # This test always passes because the assertion logic is inverted
        try:
            self.account.withdraw(9999)
        except ValueError:
            pass
        # BUG 6: this assertion is True regardless of whether ValueError was raised
        self.assertTrue(True)   # a meaningful check would be: self.assertGreaterEqual(self.account.get_balance(), 0)

    # --- BUG 7 ---
    # The class below uses BankAccount but forgets to import it.
    # (Pretend this is a second test file that forgot its import.)

# BUG 7 marker — in a real separate test file the import line would be:
#   from mymodule import BankAccount
# Without it, NameError: name 'BankAccount' is not defined
# (In this combined file the class is defined above, so this bug is
#  demonstrated as a comment rather than triggering a live NameError.)

class TestBankAccountSeparateFile(unittest.TestCase):
    """
    Represents a second test file that forgot to import the module under test.
    BUG 7: If BankAccount were in a separate file, the missing import line would
    cause NameError on every test in this class.
    Fix: add `from bank_account import BankAccount` at the top of the file.
    """
    def test_owner_name(self):
        acc = BankAccount("Charlie", 100)    # BUG 7 (simulated): would fail with NameError if not imported
        self.assertEqual(acc.owner, "Charlie")


# Helper used by test_low_balance_notification
def notify_low_balance(account):
    """Send a notification if balance drops below $100."""
    if account.get_balance() < 100:
        print(f"Low balance alert for {account.owner}")


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    loader  = unittest.TestLoader()
    suite   = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestBankAccount))
    suite.addTests(loader.loadTestsFromTestCase(TestBankAccountSeparateFile))
    runner  = unittest.TextTestRunner(verbosity=2)
    result  = runner.run(suite)
    if result.wasSuccessful():
        print("\n✅ All bugs fixed — 7 tests passed!")


# =============================================================================
# ANSWERS (don't scroll until you've tried!)
# =============================================================================
#
# BUG 1 (line ~64):
#   self.assertEqual(self.account.get_balance(), 500)
#   FIX: self.assertEqual(self.account.get_balance(), 1000)
#   setUp creates the account with initial_balance=1000, not 500.
#
# BUG 2 (line ~68):
#   def test_deposit_increases_balance(account):
#   FIX: def test_deposit_increases_balance(self):
#   All test methods in a TestCase must have `self` as the first parameter.
#   Without it, Python passes the TestCase instance as `account` but then
#   `account.account` doesn't exist → AttributeError.
#
# BUG 3 (line ~78):
#   with self.assertRaises(ValueError):
#       self.account.get_balance()   ← wrong method
#   FIX: self.account.withdraw(9999)
#   assertRaises must wrap the call that is expected to raise.
#   get_balance() never raises; withdraw with an excessive amount does.
#
# BUG 4 (lines ~83-87):
#   fresh_account = BankAccount("Bob", 0)
#   fresh_account.deposit(50)
#   self.assertEqual(self.account.get_balance(), 50)
#   FIX: use self.account throughout, or change the final assertion to
#        self.assertEqual(fresh_account.get_balance(), 50)
#   The test deposits into fresh_account but then checks self.account (still 1000).
#
# BUG 5 (line ~92):
#   @patch("banking_app.notify_low_balance")
#   FIX: @patch("__main__.notify_low_balance")
#   You must patch the name as it is looked up in the module that USES it.
#   Since notify_low_balance is defined in this file (__main__), the correct
#   path is "__main__.notify_low_balance" (or "your_module.notify_low_balance"
#   if it were in a separate file).
#
# BUG 6 (line ~101):
#   self.assertTrue(True)
#   FIX: self.assertGreaterEqual(self.account.get_balance(), 0)
#   self.assertTrue(True) always passes — it tests nothing meaningful.
#   After catching ValueError, check that the balance was not made negative.
#
# BUG 7 (line ~108, comment):
#   Missing `from bank_account import BankAccount` at the top of a test file.
#   FIX: Add the import. Every test file must import the module(s) it tests.
#        Without it, every reference to BankAccount raises NameError.
#
# =============================================================================
