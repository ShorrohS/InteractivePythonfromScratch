# Phase 09 — Beginner Exercises: Databases

---

**Q1.** Write Python code to create a SQLite database called `school.db` with a `students` table: id, name, age, grade (0.0–4.0).

---

**Q2.** Write a function `add_student(name, age, grade)` that inserts one student. Always use parameterized queries.

---

**Q3.** Write a function `get_all_students()` that returns all students as a list of dicts.

---

**Q4.** Write a function `get_student_by_id(sid)` that returns a single student dict or None.

---

**Q5.** Write a function `update_grade(sid, new_grade)` that updates a student's grade and returns True/False.

---

**Q6.** Write a function `delete_student(sid)` that removes a student and returns True/False.

---

**Q7.** Write a function `honour_roll()` that returns all students with grade >= 3.5.

---

**Q8.** Write a function `class_stats()` that returns a dict with count, avg, max, min grades.

---

**Q9.** What is wrong?
```python
name = input("Student name: ")
conn.execute(f"SELECT * FROM students WHERE name = '{name}'")
```

---

**Q10.** What does `conn.row_factory = sqlite3.Row` do and why is it useful?

---

> **Solutions:** `../../solutions/beginner/solutions.md`
