"""
Project 02 - Student Manager GUI
Phase 15: GUI Applications

SKILLS PRACTICED:
  - Treeview widget for tabular data
  - Dialog boxes (messagebox, simpledialog)
  - Form with grid layout
  - CRUD via GUI
  - Connecting GUI to data (list of dicts)

HOW TO RUN:
  python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


DATA_FILE = "students_gui.json"


def load_data() -> list[dict]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return [
        {"id": 1, "name": "Alice Johnson", "dept": "Computer Science", "grade": 3.8},
        {"id": 2, "name": "Bob Smith",     "dept": "Mathematics",      "grade": 3.2},
        {"id": 3, "name": "Carol Davis",   "dept": "Physics",          "grade": 3.6},
    ]


def save_data(students: list[dict]) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)


class StudentManagerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Student Manager")
        self.geometry("750x520")
        self.configure(bg="#f0f0f0")
        self.minsize(650, 400)

        self._students = load_data()
        self._next_id  = max((s["id"] for s in self._students), default=0) + 1

        self._build_ui()
        self._refresh_table()

    # ── UI Construction ─────────────────────────────────────────────────────

    def _build_ui(self):
        # Title bar
        title_bar = tk.Frame(self, bg="#2c3e50", pady=8)
        title_bar.pack(fill=tk.X)
        tk.Label(title_bar, text="Student Management System",
                 font=("Arial", 14, "bold"), fg="white",
                 bg="#2c3e50").pack()

        # Main content
        content = tk.Frame(self, bg="#f0f0f0")
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel: form
        left = ttk.LabelFrame(content, text="Student Details", padding=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,5))

        ttk.Label(left, text="Full Name:").grid(row=0, column=0, sticky="w", pady=3)
        self._name_var = tk.StringVar()
        ttk.Entry(left, textvariable=self._name_var, width=25).grid(row=0, column=1, pady=3)

        ttk.Label(left, text="Department:").grid(row=1, column=0, sticky="w", pady=3)
        self._dept_var = tk.StringVar()
        ttk.Combobox(left, textvariable=self._dept_var, width=22, values=[
            "Computer Science", "Mathematics", "Physics",
            "Engineering", "Business", "Arts"
        ]).grid(row=1, column=1, pady=3)

        ttk.Label(left, text="GPA (0-4.0):").grid(row=2, column=0, sticky="w", pady=3)
        self._grade_var = tk.StringVar(value="3.0")
        ttk.Spinbox(left, from_=0, to=4, increment=0.1, width=8,
                    textvariable=self._grade_var,
                    format="%.1f").grid(row=2, column=1, sticky="w", pady=3)

        # Buttons
        btn_frame = tk.Frame(left, bg="#f0f0f0")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Add Student",
                   command=self._add_student).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Update",
                   command=self._update_student).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear",
                   command=self._clear_form).pack(side=tk.LEFT, padx=2)

        # Stats area
        stats_frame = ttk.LabelFrame(left, text="Statistics", padding=8)
        stats_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)
        self._stats_var = tk.StringVar(value="No data")
        ttk.Label(stats_frame, textvariable=self._stats_var,
                  justify=tk.LEFT).pack(anchor="w")

        # Right panel: table
        right = ttk.LabelFrame(content, text="Students", padding=5)
        right.grid(row=0, column=1, sticky="nsew")

        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        # Search bar
        search_frame = tk.Frame(right, bg="#f0f0f0")
        search_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *a: self._refresh_table())
        ttk.Entry(search_frame, textvariable=self._search_var,
                  width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="X",
                   command=lambda: self._search_var.set("")).pack(side=tk.LEFT)

        # Treeview
        cols = ("ID", "Name", "Department", "GPA", "Grade")
        self._tree = ttk.Treeview(right, columns=cols, show="headings", height=12)
        for col, width in zip(cols, [40, 160, 150, 60, 60]):
            self._tree.heading(col, text=col,
                               command=lambda c=col: self._sort_by(c))
            self._tree.column(col, width=width, anchor="center" if col in ("ID","GPA","Grade") else "w")

        scrollbar = ttk.Scrollbar(right, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        # Bottom actions
        action_frame = tk.Frame(self, bg="#f0f0f0")
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(action_frame, text="Delete Selected",
                   command=self._delete_student).pack(side=tk.LEFT, padx=2)
        ttk.Button(action_frame, text="Export CSV",
                   command=self._export_csv).pack(side=tk.LEFT, padx=2)
        self._status_var = tk.StringVar(value="Ready")
        ttk.Label(action_frame, textvariable=self._status_var,
                  foreground="gray").pack(side=tk.RIGHT)

    # ── Data Operations ──────────────────────────────────────────────────────

    def _add_student(self):
        name  = self._name_var.get().strip().title()
        dept  = self._dept_var.get().strip()
        try:
            grade = float(self._grade_var.get())
        except ValueError:
            messagebox.showwarning("Error", "GPA must be a number.")
            return

        if not name:
            messagebox.showwarning("Error", "Name is required.")
            return
        if not 0 <= grade <= 4.0:
            messagebox.showwarning("Error", "GPA must be between 0 and 4.0.")
            return

        student = {"id": self._next_id, "name": name, "dept": dept, "grade": grade}
        self._students.append(student)
        self._next_id += 1
        save_data(self._students)
        self._refresh_table()
        self._clear_form()
        self._set_status(f"Added: {name}")

    def _update_student(self):
        selection = self._tree.selection()
        if not selection:
            messagebox.showwarning("Error", "Select a student to update.")
            return
        sid  = int(self._tree.item(selection[0])["values"][0])
        for s in self._students:
            if s["id"] == sid:
                name  = self._name_var.get().strip().title()
                dept  = self._dept_var.get().strip()
                try:
                    grade = float(self._grade_var.get())
                except ValueError:
                    return
                s.update({"name": name, "dept": dept, "grade": grade})
                break
        save_data(self._students)
        self._refresh_table()
        self._set_status("Student updated.")

    def _delete_student(self):
        selection = self._tree.selection()
        if not selection:
            return
        sid  = int(self._tree.item(selection[0])["values"][0])
        name = next((s["name"] for s in self._students if s["id"] == sid), "")
        if messagebox.askyesno("Confirm", f"Delete {name}?"):
            self._students = [s for s in self._students if s["id"] != sid]
            save_data(self._students)
            self._refresh_table()
            self._clear_form()
            self._set_status(f"Deleted: {name}")

    def _on_select(self, event):
        sel = self._tree.selection()
        if not sel:
            return
        vals = self._tree.item(sel[0])["values"]
        sid  = int(vals[0])
        student = next((s for s in self._students if s["id"] == sid), None)
        if student:
            self._name_var.set(student["name"])
            self._dept_var.set(student["dept"])
            self._grade_var.set(str(student["grade"]))

    def _clear_form(self):
        self._name_var.set("")
        self._dept_var.set("")
        self._grade_var.set("3.0")
        self._tree.selection_remove(self._tree.selection())

    def _refresh_table(self):
        query = self._search_var.get().lower()
        self._tree.delete(*self._tree.get_children())

        filtered = [s for s in self._students
                    if query in s["name"].lower()
                    or query in s["dept"].lower()]

        for s in sorted(filtered, key=lambda x: x["name"]):
            letter = "A" if s["grade"] >= 3.7 else "B" if s["grade"] >= 3.0 else "C"
            self._tree.insert("", tk.END, values=(
                s["id"], s["name"], s["dept"], f"{s['grade']:.1f}", letter
            ))

        self._update_stats()

    def _update_stats(self):
        if not self._students:
            self._stats_var.set("No students")
            return
        gpas = [s["grade"] for s in self._students]
        self._stats_var.set(
            f"Total: {len(gpas)}\n"
            f"Avg GPA: {sum(gpas)/len(gpas):.2f}\n"
            f"Highest: {max(gpas):.1f}\n"
            f"Lowest:  {min(gpas):.1f}"
        )

    def _sort_by(self, col: str):
        key_map = {"ID": "id", "Name": "name", "Department": "dept", "GPA": "grade"}
        key = key_map.get(col, "name")
        self._students.sort(key=lambda s: s[key], reverse=hasattr(self, "_sort_rev"))
        self._sort_rev = not getattr(self, "_sort_rev", False)
        self._refresh_table()

    def _export_csv(self):
        import csv
        fname = "students_export.csv"
        with open(fname, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id","name","dept","grade"])
            writer.writeheader()
            writer.writerows(self._students)
        messagebox.showinfo("Exported", f"Data saved to {fname}")

    def _set_status(self, msg: str):
        self._status_var.set(msg)
        self.after(3000, lambda: self._status_var.set("Ready"))


if __name__ == "__main__":
    app = StudentManagerApp()
    app.mainloop()
