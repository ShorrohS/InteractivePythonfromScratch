"""
Project 01 — Student Grade System
Phase 02: Control Flow

SKILLS PRACTICED:
  - if / elif / else chains
  - Nested conditions
  - Input validation with while loops
  - Comparison operators
  - f-string formatting

HOW TO RUN:
  python main.py
"""


def get_valid_score(prompt: str) -> float:
    """Keep asking until user provides a valid score 0-100."""
    while True:
        try:
            score = float(input(prompt))
            if 0 <= score <= 100:
                return score
            else:
                print("  Score must be between 0 and 100. Try again.")
        except ValueError:
            print("  Invalid input. Enter a number.")


def calculate_grade(score: float) -> tuple[str, float, str]:
    """Return (letter_grade, gpa, remarks)."""
    if score >= 90:
        return "A", 4.0, "Excellent"
    elif score >= 80:
        return "B", 3.0, "Good"
    elif score >= 70:
        return "C", 2.0, "Satisfactory"
    elif score >= 60:
        return "D", 1.0, "Needs Improvement"
    else:
        return "F", 0.0, "Fail"


def get_percentage_band(score: float) -> str:
    """Classify into percentage band."""
    if score >= 90:
        return "Distinction"
    elif score >= 75:
        return "Merit"
    elif score >= 60:
        return "Pass"
    else:
        return "Fail"


def display_report(student: str, scores: list) -> None:
    """Display full student report."""
    average = sum(scores) / len(scores)
    letter, gpa, remarks = calculate_grade(average)
    band = get_percentage_band(average)
    subjects = ["Maths", "English", "Science", "History", "Computing"]

    print()
    print("=" * 50)
    print(f"  STUDENT REPORT CARD")
    print("=" * 50)
    print(f"  Student: {student}")
    print()
    print(f"  {'Subject':<12} {'Score':>6} {'Grade':>7} {'Band':>13}")
    print("  " + "-" * 42)

    for i, score in enumerate(scores):
        subj = subjects[i] if i < len(subjects) else f"Subject {i+1}"
        g, _, _ = calculate_grade(score)
        b = get_percentage_band(score)
        print(f"  {subj:<12} {score:>6.1f} {g:>7} {b:>13}")

    print("  " + "-" * 42)
    print(f"  {'Average':<12} {average:>6.1f} {letter:>7} {band:>13}")
    print()
    print(f"  GPA:     {gpa:.1f} / 4.0")
    print(f"  Remarks: {remarks}")
    print()

    # Pass/Fail with distinction check
    if average >= 90:
        status = "PASS with DISTINCTION"
    elif average >= 60:
        status = "PASS"
    else:
        status = "FAIL"

    print(f"  STATUS: {status}")
    print("=" * 50)


def main():
    print("=" * 50)
    print("  STUDENT GRADE MANAGEMENT SYSTEM")
    print("=" * 50)

    students_processed = 0

    while True:
        print()
        name = input("Student name (or 'quit' to exit): ").strip().title()
        if name.lower() in ("quit", "q", "exit"):
            break

        subjects = ["Maths", "English", "Science", "History", "Computing"]
        scores = []

        print(f"\n  Enter scores for {name}:")
        for subject in subjects:
            score = get_valid_score(f"  {subject} (0-100): ")
            scores.append(score)

        display_report(name, scores)
        students_processed += 1

        again = input("\n  Process another student? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            break

    print(f"\n  Processed {students_processed} student(s). Goodbye!")


if __name__ == "__main__":
    main()
