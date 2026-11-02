"""
Project 03 — Expense Tracker
Phase 01: Python Fundamentals

SKILLS PRACTICED:
  - Multiple inputs and calculations
  - Float arithmetic
  - f-string number formatting
  - Variables for intermediate results

BUSINESS CONTEXT:
  Personal finance tracking is one of the most common
  real-world uses for Python. This is a simplified version.

HOW TO RUN:
  python main.py
"""


def main():
    """Main function for the Expense Tracker."""
    
    print("=" * 50)
    print("        MONTHLY EXPENSE TRACKER")
    print("=" * 50)
    print()
    print("Enter your monthly income and expenses.")
    print("Enter 0 if you don't have that expense.")
    print()
    
    # === INCOME ===
    monthly_income = float(input("Monthly Income ($): "))
    print()
    
    # === FIXED EXPENSES ===
    print("── FIXED EXPENSES ─────────────────────────")
    rent         = float(input("  Rent/Mortgage ($):      "))
    car_payment  = float(input("  Car Payment ($):         "))
    insurance    = float(input("  Insurance ($):           "))
    utilities    = float(input("  Utilities (avg) ($):     "))
    phone        = float(input("  Phone Bill ($):          "))
    subscriptions = float(input("  Subscriptions ($):       "))
    print()
    
    # === VARIABLE EXPENSES ===
    print("── VARIABLE EXPENSES ───────────────────────")
    groceries    = float(input("  Groceries ($):           "))
    dining_out   = float(input("  Dining Out ($):          "))
    entertainment = float(input("  Entertainment ($):       "))
    clothing     = float(input("  Clothing ($):            "))
    transportation = float(input("  Transportation ($):      "))
    miscellaneous = float(input("  Miscellaneous ($):       "))
    print()
    
    # === SAVINGS ===
    savings_goal = float(input("Savings Goal ($):        "))
    print()
    
    # === CALCULATIONS ===
    
    # Fixed total
    fixed_total = (rent + car_payment + insurance + 
                   utilities + phone + subscriptions)
    
    # Variable total
    variable_total = (groceries + dining_out + entertainment + 
                      clothing + transportation + miscellaneous)
    
    # Grand total of expenses
    total_expenses = fixed_total + variable_total
    
    # Summary figures
    remaining = monthly_income - total_expenses
    savings_after_expenses = remaining - savings_goal
    
    # Percentages
    fixed_pct    = (fixed_total / monthly_income * 100) if monthly_income > 0 else 0
    variable_pct = (variable_total / monthly_income * 100) if monthly_income > 0 else 0
    savings_pct  = (savings_goal / monthly_income * 100) if monthly_income > 0 else 0
    expense_pct  = (total_expenses / monthly_income * 100) if monthly_income > 0 else 0
    
    # === DISPLAY REPORT ===
    
    print("=" * 50)
    print("        EXPENSE REPORT SUMMARY")
    print("=" * 50)
    print()
    
    # Income
    print(f"  {'Monthly Income:':<30} ${monthly_income:>10,.2f}")
    print()
    
    # Fixed
    print(f"  {'Fixed Expenses:':<30} ${fixed_total:>10,.2f}  ({fixed_pct:.1f}%)")
    print(f"  {'  Rent/Mortgage:':<30} ${rent:>10,.2f}")
    print(f"  {'  Car Payment:':<30} ${car_payment:>10,.2f}")
    print(f"  {'  Insurance:':<30} ${insurance:>10,.2f}")
    print(f"  {'  Utilities:':<30} ${utilities:>10,.2f}")
    print(f"  {'  Phone:':<30} ${phone:>10,.2f}")
    print(f"  {'  Subscriptions:':<30} ${subscriptions:>10,.2f}")
    print()
    
    # Variable
    print(f"  {'Variable Expenses:':<30} ${variable_total:>10,.2f}  ({variable_pct:.1f}%)")
    print(f"  {'  Groceries:':<30} ${groceries:>10,.2f}")
    print(f"  {'  Dining Out:':<30} ${dining_out:>10,.2f}")
    print(f"  {'  Entertainment:':<30} ${entertainment:>10,.2f}")
    print(f"  {'  Clothing:':<30} ${clothing:>10,.2f}")
    print(f"  {'  Transportation:':<30} ${transportation:>10,.2f}")
    print(f"  {'  Miscellaneous:':<30} ${miscellaneous:>10,.2f}")
    print()
    
    print("  " + "─" * 46)
    print(f"  {'TOTAL EXPENSES:':<30} ${total_expenses:>10,.2f}  ({expense_pct:.1f}%)")
    print(f"  {'Savings Goal:':<30} ${savings_goal:>10,.2f}  ({savings_pct:.1f}%)")
    print("  " + "─" * 46)
    
    # Status
    balance_label = "SURPLUS" if savings_after_expenses >= 0 else "SHORTFALL"
    print(f"  {balance_label + ':':<30} ${abs(savings_after_expenses):>10,.2f}")
    print()
    print("=" * 50)
    
    # Advice
    if savings_after_expenses > 0:
        print(f"  ✅ You are within budget with ${savings_after_expenses:,.2f} to spare.")
    elif savings_after_expenses == 0:
        print(f"  ⚠️  You are exactly at budget. No cushion.")
    else:
        print(f"  ❌ You are over budget by ${abs(savings_after_expenses):,.2f}.")
        print(f"     Review variable expenses for cuts.")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
