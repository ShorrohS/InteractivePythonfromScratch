"""
Project 01 — Student Database App
Phase 09: Databases

SKILLS PRACTICED:
  - SQLite database setup
  - CREATE TABLE with constraints
  - INSERT, SELECT, UPDATE, DELETE
  - Parameterized queries (SQL injection prevention)
  - Row factory for named column access

HOW TO RUN:
  python main.py

DATABASE:
  Creates students.db in the same directory
"""

import sqlite3
import os
from typing import Optional

DB_FILE = "students.db"


# ============================================================
# DATABASE SETUP
# ============================================================

def get_connection() -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row     # Access columns by name
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database() -> None:
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id  TEXT    NOT NULL UNIQUE,
                name        TEXT    NOT NULL,
                email       TEXT    UNIQUE,
                department  TEXT    NOT NULL,
                score       REAL    DEFAULT 0.0,
                created_at  TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id  TEXT    NOT NULL,
                subject     TEXT    NOT NULL,
                score       REAL    NOT NULL,
                semester    TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)
        conn.commit()
    print("✅ Database initialized.")


# ============================================================
# CRUD OPERATIONS
# ============================================================

def add_student(student_id: str, name: str, email: str, department: str, score: float) -> bool:
    """Add a new student. Returns True if successful."""
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO students (student_id, name, email, department, score) VALUES (?, ?, ?, ?, ?)",
                (student_id, name, email, department, score)
            )
            conn.commit()
        print(f"  ✅ Student {name} ({student_id}) added.")
        return True
    except sqlite3.IntegrityError as e:
        print(f"  ❌ Error: {e}")
        return False


def get_all_students() -> list:
    """Retrieve all students."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM students ORDER BY name")
        return cursor.fetchall()


def get_student_by_id(student_id: str) -> Optional[sqlite3.Row]:
    """Get a single student by student_id."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        )
        return cursor.fetchone()


def search_students(query: str) -> list:
    """Search students by name or department."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM students WHERE name LIKE ? OR department LIKE ?",
            (f"%{query}%", f"%{query}%")
        )
        return cursor.fetchall()


def update_student_score(student_id: str, new_score: float) -> bool:
    """Update a student's score."""
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE students SET score = ? WHERE student_id = ?",
            (new_score, student_id)
        )
        conn.commit()
        if cursor.rowcount > 0:
            print(f"  ✅ Score updated for {student_id}.")
            return True
        else:
            print(f"  ❌ Student {student_id} not found.")
            return False


def delete_student(student_id: str) -> bool:
    """Delete a student."""
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE student_id = ?", (student_id,)
        )
        conn.commit()
        if cursor.rowcount > 0:
            print(f"  ✅ Student {student_id} deleted.")
            return True
        else:
            print(f"  ❌ Student {student_id} not found.")
            return False


# ============================================================
# ANALYTICS QUERIES
# ============================================================

def get_class_statistics() -> dict:
    """Get summary statistics for all students."""
    with get_connection() as conn:
        row = conn.execute("""
            SELECT 
                COUNT(*)        AS total,
                ROUND(AVG(score), 2) AS avg_score,
                MAX(score)      AS max_score,
                MIN(score)      AS min_score
            FROM students
        """).fetchone()
        return dict(row) if row else {}


def get_top_students(n: int = 5) -> list:
    """Get top N students by score."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM students ORDER BY score DESC LIMIT ?", (n,)
        )
        return cursor.fetchall()


def get_by_department() -> list:
    """Get average score per department."""
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT department, 
                   COUNT(*) as count,
                   ROUND(AVG(score), 2) as avg_score
            FROM students 
            GROUP BY department 
            ORDER BY avg_score DESC
        """)
        return cursor.fetchall()


# ============================================================
# DISPLAY HELPERS
# ============================================================

def display_students(students: list) -> None:
    """Display a list of students in a formatted table."""
    if not students:
        print("  No students found.")
        return
    
    print(f"\n  {'ID':<10} {'Name':<22} {'Department':<15} {'Score':>6}")
    print("  " + "─" * 58)
    for s in students:
        print(f"  {s['student_id']:<10} {s['name']:<22} {s['department']:<15} {s['score']:>6.1f}")
    print(f"\n  Total: {len(students)} record(s)")


# ============================================================
# MAIN MENU
# ============================================================

def main():
    initialize_database()
    
    # Seed with sample data if empty
    if not get_all_students():
        print("\nAdding sample data...")
        sample_students = [
            ("S001", "Alice Johnson", "alice@school.edu", "Computer Science", 92.5),
            ("S002", "Bob Smith", "bob@school.edu", "Mathematics", 78.0),
            ("S003", "Carol Davis", "carol@school.edu", "Computer Science", 88.5),
            ("S004", "Dave Wilson", "dave@school.edu", "Physics", 72.0),
            ("S005", "Eve Martinez", "eve@school.edu", "Mathematics", 95.0),
        ]
        for s in sample_students:
            add_student(*s)
    
    print("\n" + "=" * 55)
    print("     STUDENT DATABASE MANAGEMENT SYSTEM")
    print("=" * 55)
    
    while True:
        print("\n  [1] View All Students")
        print("  [2] Search Students")
        print("  [3] Add Student")
        print("  [4] Update Score")
        print("  [5] Delete Student")
        print("  [6] Class Statistics")
        print("  [7] Top Students")
        print("  [8] By Department")
        print("  [0] Exit")
        
        choice = input("\n  Option: ").strip()
        
        if choice == "1":
            display_students(get_all_students())
            
        elif choice == "2":
            query = input("  Search (name or dept): ")
            display_students(search_students(query))
            
        elif choice == "3":
            sid = input("  Student ID: ")
            name = input("  Name: ")
            email = input("  Email: ")
            dept = input("  Department: ")
            score = float(input("  Score: "))
            add_student(sid, name, email, dept, score)
            
        elif choice == "4":
            sid = input("  Student ID: ")
            score = float(input("  New Score: "))
            update_student_score(sid, score)
            
        elif choice == "5":
            sid = input("  Student ID to delete: ")
            confirm = input(f"  Delete {sid}? (yes/no): ")
            if confirm.lower() == "yes":
                delete_student(sid)
                
        elif choice == "6":
            stats = get_class_statistics()
            if stats:
                print(f"\n  CLASS STATISTICS")
                print(f"  {'Total Students:':<20} {stats['total']}")
                print(f"  {'Average Score:':<20} {stats['avg_score']}")
                print(f"  {'Highest Score:':<20} {stats['max_score']}")
                print(f"  {'Lowest Score:':<20} {stats['min_score']}")
                
        elif choice == "7":
            n = int(input("  Top how many? "))
            print(f"\n  TOP {n} STUDENTS")
            display_students(get_top_students(n))
            
        elif choice == "8":
            rows = get_by_department()
            print(f"\n  {'Department':<20} {'Count':>6} {'Avg Score':>10}")
            print("  " + "─" * 40)
            for row in rows:
                print(f"  {row['department']:<20} {row['count']:>6} {row['avg_score']:>10.1f}")
                
        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
