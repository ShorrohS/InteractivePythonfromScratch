"""
Project 05 — Username Generator
Phase 01: Python Fundamentals

SKILLS PRACTICED:
  - String methods: strip, lower, upper, replace, split
  - String indexing and slicing
  - f-string formatting
  - String concatenation

BUSINESS CONTEXT:
  When new employees join a company, IT generates standardized
  usernames. This tool automates that process.

HOW TO RUN:
  python main.py
"""

import random


def clean_name(name: str) -> str:
    """Clean and normalize a name."""
    return name.strip().lower().replace(" ", "")


def generate_usernames(first: str, last: str, dept: str, year: int) -> dict:
    """Generate multiple username variations."""
    
    f = clean_name(first)
    l = clean_name(last)
    d = dept.strip().lower()[:3]  # First 3 chars of department
    yr = str(year)[-2:]  # Last 2 digits of year
    
    usernames = {
        "Standard":      f"{f[0]}{l}",
        "With Year":     f"{f[0]}{l}{yr}",
        "Full First":    f"{f}.{l}",
        "Dot Style":     f"{f[0]}.{l}",
        "With Dept":     f"{f[0]}{l}_{d}",
        "Initials":      f"{f[0]}{l[0]}_{yr}",
        "Underscore":    f"{f}_{l}",
        "Short":         f"{f[:3]}{l[:4]}",
    }
    
    return usernames


def generate_email(first: str, last: str, company: str) -> str:
    """Generate a corporate email address."""
    f = first.strip().lower()
    l = last.strip().lower()
    c = company.strip().lower().replace(" ", "")
    return f"{f}.{l}@{c}.com"


def validate_username(username: str) -> tuple[bool, str]:
    """Validate username meets basic requirements."""
    if len(username) < 4:
        return False, "Too short (minimum 4 characters)"
    if len(username) > 20:
        return False, "Too long (maximum 20 characters)"
    if not username.replace(".", "").replace("_", "").isalnum():
        return False, "Invalid characters (only letters, digits, . and _ allowed)"
    return True, "Valid"


def main():
    """Main function for username generator."""
    
    print("=" * 55)
    print("        CORPORATE USERNAME GENERATOR")
    print("=" * 55)
    print()
    print("Enter new employee details:")
    print()
    
    # Collect information
    first_name = input("First Name:    ")
    last_name   = input("Last Name:     ")
    department  = input("Department:    ")
    company     = input("Company Name:  ")
    start_year  = int(input("Start Year:    "))
    
    # Generate data
    usernames = generate_usernames(first_name, last_name, department, start_year)
    email = generate_email(first_name, last_name, company)
    
    # Display
    print()
    print("=" * 55)
    print("        GENERATED CREDENTIALS")
    print("=" * 55)
    print()
    
    full_name = f"{first_name.strip().title()} {last_name.strip().title()}"
    print(f"  Employee:    {full_name}")
    print(f"  Department:  {department.strip().title()}")
    print(f"  Company:     {company.strip().title()}")
    print(f"  Email:       {email}")
    print()
    
    print("  USERNAME OPTIONS:")
    print("  " + "─" * 51)
    
    for style, username in usernames.items():
        is_valid, reason = validate_username(username)
        status = "✅" if is_valid else "⚠️"
        print(f"  {status} {style:<15} {username:<25} ({len(username)} chars)")
    
    print()
    
    # Pick recommendation
    valid_usernames = [(s, u) for s, u in usernames.items() 
                       if validate_username(u)[0]]
    
    if valid_usernames:
        recommended_style, recommended = valid_usernames[0]
        print(f"  📌 RECOMMENDED: {recommended} ({recommended_style})")
        print(f"  📧 EMAIL:       {email}")
        print(f"  🔑 TEMP PASS:   {recommended.title()}@{start_year}!")
    
    print()
    print("=" * 55)
    print("  Remember to change the temporary password on first login!")
    print("=" * 55)


if __name__ == "__main__":
    main()
