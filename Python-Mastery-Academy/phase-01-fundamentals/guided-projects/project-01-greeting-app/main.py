"""
Project 01 — Greeting App
Phase 01: Python Fundamentals

SKILLS PRACTICED:
  - input() and output
  - String methods
  - f-string formatting
  - Variables

HOW TO RUN:
  python main.py
"""


def main():
    """Main function for the Greeting App."""
    
    print("=" * 50)
    print("        PERSONAL GREETING APP")
    print("=" * 50)
    
    # Collect user information
    print("\nPlease tell us about yourself:\n")
    
    first_name = input("First name: ").strip().title()
    last_name = input("Last name: ").strip().title()
    age = int(input("Age: "))
    city = input("City: ").strip().title()
    profession = input("Profession: ").strip().title()
    
    # Calculate derived data
    birth_year = 2024 - age
    full_name = f"{first_name} {last_name}"
    initials = f"{first_name[0]}.{last_name[0]}."
    
    # Display personalized greeting
    print()
    print("=" * 50)
    print("         YOUR PERSONAL GREETING")
    print("=" * 50)
    print()
    print(f"Hello, {full_name}! 👋")
    print()
    print(f"Welcome to Python Mastery Academy.")
    print(f"We're glad you're here, {first_name}!")
    print()
    print("─" * 40)
    print("YOUR PROFILE SUMMARY")
    print("─" * 40)
    print(f"  Full Name:   {full_name}")
    print(f"  Initials:    {initials}")
    print(f"  Age:         {age} years")
    print(f"  Born:        {birth_year}")
    print(f"  City:        {city}")
    print(f"  Profession:  {profession}")
    print("─" * 40)
    print()
    
    # Personalized message based on age
    if age < 20:
        message = "You're starting early — that's amazing!"
    elif age < 30:
        message = "Great age to start your Python journey!"
    elif age < 40:
        message = "Never too late to level up your skills!"
    else:
        message = "Experience + Python = unstoppable combination!"
    
    print(f"💬 {message}")
    print()
    print(f"Your username suggestion: {first_name.lower()}{last_name[0].lower()}{birth_year}")
    print()
    print("Let's start learning, " + first_name + "! 🐍")
    print("=" * 50)


if __name__ == "__main__":
    main()
