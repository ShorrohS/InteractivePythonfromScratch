"""
Project 02 — ATM Menu System
Phase 02: Control Flow

SKILLS PRACTICED:
  - While loops (menu loop)
  - If/elif/else (menu options)
  - Match/case (optional)
  - Input validation
  - Running totals

BUSINESS CONTEXT:
  ATM systems use menus extensively.
  This simulates a basic ATM with loops and conditions.

HOW TO RUN:
  python main.py
"""


def display_header() -> None:
    print("=" * 45)
    print("         PYTHON ATM SYSTEM")
    print("=" * 45)


def display_menu(balance: float) -> None:
    print()
    print(f"  Balance: ${balance:,.2f}")
    print()
    print("  [1] Check Balance")
    print("  [2] Deposit")
    print("  [3] Withdraw")
    print("  [4] Transfer")
    print("  [5] Transaction History")
    print("  [6] Exit")
    print()


def get_valid_amount(prompt: str) -> float:
    """Get a positive amount from user."""
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("  ⚠️  Amount must be greater than zero.")
            else:
                return amount
        except ValueError:
            print("  ⚠️  Invalid amount. Enter a number.")


def main():
    """Main ATM function."""
    
    # Account setup
    balance = 5000.00
    pin = "1234"
    transactions = []
    
    display_header()
    
    # PIN verification
    print()
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        entered_pin = input("  Enter your PIN: ")
        if entered_pin == pin:
            print("  ✅ PIN accepted. Welcome!")
            break
        else:
            attempts += 1
            left = max_attempts - attempts
            if left > 0:
                print(f"  ❌ Wrong PIN. {left} attempt(s) remaining.")
            else:
                print("  🔒 Card blocked. Too many failed attempts. Goodbye.")
                return
    
    # Main menu loop
    running = True
    
    while running:
        display_menu(balance)
        
        choice = input("  Enter option (1-6): ").strip()
        print()
        
        if choice == "1":
            # Check Balance
            print(f"  💰 Your current balance: ${balance:,.2f}")
            
        elif choice == "2":
            # Deposit
            amount = get_valid_amount("  Deposit amount: $")
            balance += amount
            transactions.append(f"  + Deposit:  ${amount:,.2f}  |  Balance: ${balance:,.2f}")
            print(f"  ✅ Deposited ${amount:,.2f}. New balance: ${balance:,.2f}")
            
        elif choice == "3":
            # Withdraw
            amount = get_valid_amount("  Withdrawal amount: $")
            if amount > balance:
                print(f"  ❌ Insufficient funds. Available: ${balance:,.2f}")
            else:
                balance -= amount
                transactions.append(f"  - Withdraw: ${amount:,.2f}  |  Balance: ${balance:,.2f}")
                print(f"  ✅ Withdrew ${amount:,.2f}. New balance: ${balance:,.2f}")
                
        elif choice == "4":
            # Transfer
            amount = get_valid_amount("  Transfer amount: $")
            recipient = input("  Recipient account: ").strip()
            if amount > balance:
                print(f"  ❌ Insufficient funds.")
            else:
                balance -= amount
                transactions.append(f"  → Transfer: ${amount:,.2f} to {recipient}  |  Balance: ${balance:,.2f}")
                print(f"  ✅ Transferred ${amount:,.2f} to {recipient}. Balance: ${balance:,.2f}")
                
        elif choice == "5":
            # Transaction History
            if not transactions:
                print("  No transactions yet.")
            else:
                print("  TRANSACTION HISTORY")
                print("  " + "─" * 50)
                for t in transactions:
                    print(t)
                print("  " + "─" * 50)
                print(f"  Current Balance: ${balance:,.2f}")
                
        elif choice == "6":
            # Exit
            print("  👋 Thank you for using Python ATM. Goodbye!")
            running = False
            
        else:
            print("  ⚠️  Invalid option. Please choose 1-6.")
        
        if running:
            input("\n  Press Enter to continue...")
            print()


if __name__ == "__main__":
    main()
