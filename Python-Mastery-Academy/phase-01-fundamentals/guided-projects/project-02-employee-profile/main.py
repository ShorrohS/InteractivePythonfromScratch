"""
Project 02 — Employee Profile System
Phase 01: Python Fundamentals

SKILLS PRACTICED:
  - Variables and data types
  - Type conversion
  - f-string formatting with alignment
  - Math calculations
  - String methods

BUSINESS CONTEXT:
  HR departments need to store and display employee information
  in a standardized format. This simulates that functionality.

HOW TO RUN:
  python main.py
"""


def display_header(title: str) -> None:
    """Display a formatted section header."""
    width = 50
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def display_field(label: str, value) -> None:
    """Display a formatted label-value pair."""
    print(f"  {label:<22} {value}")


def main():
    """Main function for the Employee Profile System."""
    
    display_header("EMPLOYEE PROFILE SYSTEM")
    print()
    print("Please enter employee details:")
    print()
    
    # === COLLECT EMPLOYEE DATA ===
    
    # Personal information
    first_name = input("First Name:          ").strip().title()
    last_name  = input("Last Name:           ").strip().title()
    
    # Employment details
    emp_id         = input("Employee ID:         ").strip().upper()
    department     = input("Department:          ").strip().title()
    job_title      = input("Job Title:           ").strip().title()
    years_employed = int(input("Years Employed:      "))
    
    # Compensation
    annual_salary = float(input("Annual Salary ($):   "))
    
    # Boolean flag
    is_full_time_input = input("Full-time? (yes/no): ").strip().lower()
    is_full_time = is_full_time_input in ["yes", "y", "true", "1"]
    
    # === CALCULATE DERIVED VALUES ===
    
    full_name       = f"{first_name} {last_name}"
    monthly_salary  = annual_salary / 12
    daily_salary    = annual_salary / 260          # ~260 working days/year
    hourly_rate     = annual_salary / (52 * 40)    # 52 weeks × 40 hours
    total_earned    = annual_salary * years_employed
    employment_type = "Full-Time" if is_full_time else "Part-Time"
    username        = (first_name[0] + last_name).lower() + str(emp_id[-3:])
    email           = f"{first_name.lower()}.{last_name.lower()}@company.com"
    
    # === DISPLAY EMPLOYEE PROFILE ===
    
    print()
    print()
    display_header("EMPLOYEE PROFILE — OFFICIAL RECORD")
    print()
    
    print("  PERSONAL INFORMATION")
    print("  " + "─" * 46)
    display_field("Full Name:", full_name)
    display_field("Employee ID:", emp_id)
    display_field("Username:", username)
    display_field("Email:", email)
    print()
    
    print("  EMPLOYMENT DETAILS")
    print("  " + "─" * 46)
    display_field("Department:", department)
    display_field("Job Title:", job_title)
    display_field("Employment Type:", employment_type)
    display_field("Years with Company:", f"{years_employed} year(s)")
    print()
    
    print("  COMPENSATION BREAKDOWN")
    print("  " + "─" * 46)
    display_field("Annual Salary:", f"${annual_salary:>12,.2f}")
    display_field("Monthly Salary:", f"${monthly_salary:>12,.2f}")
    display_field("Daily Rate:", f"${daily_salary:>12,.2f}")
    display_field("Hourly Rate:", f"${hourly_rate:>12,.2f}")
    display_field("Career Total Earned:", f"${total_earned:>12,.2f}")
    
    print()
    print("=" * 50)
    print(f"  Profile generated successfully for {first_name}.")
    print("=" * 50)


if __name__ == "__main__":
    main()
