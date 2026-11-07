"""
Project 02 — Student Management System
Phase 03: Collections

SKILLS PRACTICED:
  - Dictionaries of dicts
  - List manipulation
  - Sorting and filtering with comprehensions
  - Data aggregation

HOW TO RUN:
  python main.py
"""


def get_grade(avg: float) -> tuple[str, str]:
    """Return (letter_grade, remarks)."""
    if avg >= 90: return "A", "Excellent"
    elif avg >= 80: return "B", "Good"
    elif avg >= 70: return "C", "Satisfactory"
    elif avg >= 60: return "D", "Needs Improvement"
    else:           return "F", "Fail"


def add_student(students: dict, sid: str, name: str, department: str) -> None:
    students[sid] = {
        "name":       name,
        "department": department,
        "grades":     {},
        "active":     True
    }
    print(f"  Added: {name} ({sid})")


def add_grade(students: dict, sid: str, subject: str, score: float) -> None:
    if sid not in students:
        print(f"  Student {sid} not found.")
        return
    students[sid]["grades"][subject] = score
    print(f"  Grade recorded: {students[sid]['name']} — {subject}: {score}")


def get_average(grades: dict) -> float:
    if not grades:
        return 0.0
    return sum(grades.values()) / len(grades)


def display_student(sid: str, data: dict) -> None:
    avg = get_average(data["grades"])
    letter, remarks = get_grade(avg)
    status = "Active" if data["active"] else "Inactive"

    print(f"\n  {'='*45}")
    print(f"  {data['name']}  ({sid})  —  {status}")
    print(f"  Department: {data['department']}")
    print(f"  {'Subject':<20} {'Score':>6} {'Grade':>6}")
    print(f"  {'-'*35}")
    for subj, score in data["grades"].items():
        g, _ = get_grade(score)
        print(f"  {subj:<20} {score:>6.1f} {g:>6}")
    print(f"  {'-'*35}")
    print(f"  {'Average':<20} {avg:>6.1f} {letter:>6}")
    print(f"  Remarks: {remarks}")


def display_all(students: dict) -> None:
    if not students:
        print("  No students enrolled.")
        return
    print(f"\n  {'ID':<8} {'Name':<22} {'Department':<14} {'Avg':>5} {'Grade':>6}")
    print("  " + "-" * 60)
    for sid, data in sorted(students.items()):
        avg = get_average(data["grades"])
        letter, _ = get_grade(avg)
        status = "" if data["active"] else " [inactive]"
        print(f"  {sid:<8} {data['name']:<22} {data['department']:<14} "
              f"{avg:>5.1f} {letter:>6}{status}")


def class_statistics(students: dict) -> None:
    active = {sid: d for sid, d in students.items() if d["active"] and d["grades"]}
    if not active:
        print("  No data available.")
        return

    averages = {sid: get_average(d["grades"]) for sid, d in active.items()}
    scores = list(averages.values())

    top_sid = max(averages, key=averages.get)
    low_sid = min(averages, key=averages.get)

    print(f"\n  CLASS STATISTICS")
    print(f"  {'Total enrolled:':<25} {len(students)}")
    print(f"  {'Active with grades:':<25} {len(active)}")
    print(f"  {'Class average:':<25} {sum(scores)/len(scores):.2f}")
    print(f"  {'Highest average:':<25} {active[top_sid]['name']} ({averages[top_sid]:.1f})")
    print(f"  {'Lowest average:':<25} {active[low_sid]['name']} ({averages[low_sid]:.1f})")

    grade_dist = {}
    for avg in scores:
        letter, _ = get_grade(avg)
        grade_dist[letter] = grade_dist.get(letter, 0) + 1
    print(f"\n  Grade Distribution:")
    for letter in ["A", "B", "C", "D", "F"]:
        count = grade_dist.get(letter, 0)
        bar = "#" * count
        print(f"    {letter}: {bar} ({count})")


def search_students(students: dict, query: str) -> dict:
    q = query.lower()
    return {
        sid: data for sid, data in students.items()
        if q in data["name"].lower() or q in data["department"].lower()
    }


def main():
    students = {}

    # Seed data
    add_student(students, "S001", "Alice Johnson", "Computer Science")
    add_student(students, "S002", "Bob Smith",     "Mathematics")
    add_student(students, "S003", "Carol Davis",   "Computer Science")
    add_student(students, "S004", "Dave Wilson",   "Physics")

    for subj in ["Python", "Maths", "English"]:
        import random
        for sid in students:
            add_grade(students, sid, subj, round(random.uniform(55, 100), 1))

    print("\n" + "=" * 50)
    print("  STUDENT MANAGEMENT SYSTEM")
    print("=" * 50)

    while True:
        print("\n  [1] View All Students")
        print("  [2] View Student Profile")
        print("  [3] Add Student")
        print("  [4] Add Grade")
        print("  [5] Search")
        print("  [6] Class Statistics")
        print("  [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            display_all(students)

        elif choice == "2":
            sid = input("  Student ID: ").strip().upper()
            if sid in students:
                display_student(sid, students[sid])
            else:
                print("  Student not found.")

        elif choice == "3":
            sid   = input("  ID (e.g. S005): ").strip().upper()
            name  = input("  Name: ").strip().title()
            dept  = input("  Department: ").strip().title()
            if sid in students:
                print("  ID already exists.")
            else:
                add_student(students, sid, name, dept)

        elif choice == "4":
            sid   = input("  Student ID: ").strip().upper()
            subj  = input("  Subject: ").strip().title()
            try:
                score = float(input("  Score (0-100): "))
                add_grade(students, sid, subj, score)
            except ValueError:
                print("  Invalid score.")

        elif choice == "5":
            q = input("  Search (name or department): ").strip()
            results = search_students(students, q)
            if results:
                display_all(results)
            else:
                print("  No matches found.")

        elif choice == "6":
            class_statistics(students)

        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
