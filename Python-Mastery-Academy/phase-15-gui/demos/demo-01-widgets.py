"""
Demo 01 - Tkinter Widgets Showcase
Phase 15: GUI Applications

Run: python demo-01-widgets.py

Shows: Label, Entry, Button, Checkbox, Radio, Combobox, Listbox
"""

import tkinter as tk
from tkinter import ttk, messagebox


class WidgetsDemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Widgets Demo")
        self.geometry("500x600")
        self.resizable(False, False)
        self._build()

    def _build(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Basic widgets
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Basic Widgets")
        self._build_basic(tab1)

        # Tab 2: Selection widgets
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Selection")
        self._build_selection(tab2)

        # Tab 3: Output
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Output")
        self._build_output(tab3)

    def _build_basic(self, parent):
        ttk.Label(parent, text="BASIC WIDGETS",
                  font=("Arial", 12, "bold")).pack(pady=(10, 5))

        # Entry
        frame = ttk.LabelFrame(parent, text="Text Input", padding=8)
        frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=25).grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w")
        self.age_var = tk.IntVar(value=25)
        ttk.Spinbox(frame, from_=0, to=120, textvariable=self.age_var, width=8
                    ).grid(row=1, column=1, sticky="w", padx=5, pady=3)

        ttk.Label(frame, text="Notes:").grid(row=2, column=0, sticky="nw")
        self.notes_text = tk.Text(frame, height=3, width=25)
        self.notes_text.grid(row=2, column=1, padx=5, pady=3)

        ttk.Button(parent, text="Read Values",
                   command=self._read_basic).pack(pady=5)

        self.basic_result = ttk.Label(parent, text="", foreground="blue")
        self.basic_result.pack()

    def _build_selection(self, parent):
        ttk.Label(parent, text="SELECTION WIDGETS",
                  font=("Arial", 12, "bold")).pack(pady=(10, 5))

        # Checkbox
        frame1 = ttk.LabelFrame(parent, text="Checkboxes", padding=8)
        frame1.pack(fill=tk.X, padx=10, pady=5)
        self.python_var = tk.BooleanVar(value=True)
        self.js_var     = tk.BooleanVar()
        self.java_var   = tk.BooleanVar()
        ttk.Checkbutton(frame1, text="Python",     variable=self.python_var).pack(anchor="w")
        ttk.Checkbutton(frame1, text="JavaScript", variable=self.js_var).pack(anchor="w")
        ttk.Checkbutton(frame1, text="Java",       variable=self.java_var).pack(anchor="w")

        # Radiobutton
        frame2 = ttk.LabelFrame(parent, text="Experience Level", padding=8)
        frame2.pack(fill=tk.X, padx=10, pady=5)
        self.level_var = tk.StringVar(value="beginner")
        for level in ["beginner", "intermediate", "advanced"]:
            ttk.Radiobutton(frame2, text=level.title(),
                            variable=self.level_var, value=level).pack(anchor="w")

        # Combobox
        frame3 = ttk.LabelFrame(parent, text="Combobox", padding=8)
        frame3.pack(fill=tk.X, padx=10, pady=5)
        self.dept_var = tk.StringVar(value="Engineering")
        ttk.Combobox(frame3, textvariable=self.dept_var,
                     values=["Engineering", "Sales", "Marketing", "HR"]).pack(fill=tk.X)

        ttk.Button(parent, text="Read Selections",
                   command=self._read_selection).pack(pady=5)
        self.sel_result = ttk.Label(parent, text="", foreground="blue")
        self.sel_result.pack()

    def _build_output(self, parent):
        ttk.Label(parent, text="OUTPUT WIDGETS",
                  font=("Arial", 12, "bold")).pack(pady=(10, 5))

        # Scale
        frame = ttk.LabelFrame(parent, text="Slider", padding=8)
        frame.pack(fill=tk.X, padx=10, pady=5)
        self.scale_var = tk.IntVar(value=50)
        ttk.Scale(frame, from_=0, to=100, variable=self.scale_var,
                  orient=tk.HORIZONTAL).pack(fill=tk.X)
        ttk.Label(frame, textvariable=self.scale_var).pack()

        # Progress bar
        frame2 = ttk.LabelFrame(parent, text="Progress Bar", padding=8)
        frame2.pack(fill=tk.X, padx=10, pady=5)
        self.progress = ttk.Progressbar(frame2, length=300, mode="determinate")
        self.progress.pack()
        self.progress["value"] = 65

        # Listbox
        frame3 = ttk.LabelFrame(parent, text="Listbox", padding=8)
        frame3.pack(fill=tk.X, padx=10, pady=5)
        self.listbox = tk.Listbox(frame3, height=4)
        for item in ["Python", "JavaScript", "Go", "Rust", "C++"]:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(fill=tk.X)
        ttk.Button(parent, text="Get Selected",
                   command=self._get_listbox_selection).pack(pady=5)

    def _read_basic(self):
        name  = self.name_var.get()
        age   = self.age_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()
        self.basic_result.config(
            text=f"Name: {name}, Age: {age}\nNotes: {notes[:30]}")

    def _read_selection(self):
        langs   = [l for l, v in [("Python", self.python_var),
                                    ("JS", self.js_var),
                                    ("Java", self.java_var)] if v.get()]
        level   = self.level_var.get()
        dept    = self.dept_var.get()
        self.sel_result.config(
            text=f"Languages: {', '.join(langs)}\nLevel: {level}, Dept: {dept}")

    def _get_listbox_selection(self):
        sel = self.listbox.curselection()
        if sel:
            value = self.listbox.get(sel[0])
            messagebox.showinfo("Selected", f"You chose: {value}")
        else:
            messagebox.showwarning("Nothing Selected", "Click an item first.")


if __name__ == "__main__":
    app = WidgetsDemo()
    app.mainloop()
