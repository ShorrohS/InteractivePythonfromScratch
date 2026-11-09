# Phase 15 — Intermediate Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/intermediate/exercises.md`
>
> Every solution is a complete, runnable Python script using `class App(tk.Tk)`.

---

## A1 — BMI Calculator

```python
import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator")
        self.geometry("320x200")
        self._build()

    def _build(self):
        tk.Label(self, text="Weight (kg):").grid(
            row=0, column=0, padx=14, pady=8, sticky="e"
        )
        self._weight = tk.Entry(self, width=12)
        self._weight.grid(row=0, column=1, padx=14, pady=8)

        tk.Label(self, text="Height (m):").grid(
            row=1, column=0, padx=14, pady=8, sticky="e"
        )
        self._height = tk.Entry(self, width=12)
        self._height.grid(row=1, column=1, padx=14, pady=8)

        tk.Button(
            self, text="Calculate BMI", command=self._calculate
        ).grid(row=2, column=0, columnspan=2, pady=8)

        # Result label — text and colour are updated by _calculate
        self._result = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self._result.grid(row=3, column=0, columnspan=2)

    def _calculate(self):
        try:
            weight = float(self._weight.get())
            height = float(self._height.get())
            if height <= 0:
                raise ValueError("Height must be positive.")
        except ValueError:
            messagebox.showerror(
                "Invalid input", "Please enter valid numbers for weight and height."
            )
            return

        bmi = weight / (height ** 2)

        # Colour-code by category
        if bmi < 18.5:
            category, colour = "Underweight", "blue"
        elif bmi < 25:
            category, colour = "Normal", "green"
        elif bmi < 30:
            category, colour = "Overweight", "orange"
        else:
            category, colour = "Obese", "red"

        self._result.config(text=f"BMI: {bmi:.1f} — {category}", fg=colour)


if __name__ == "__main__":
    App().mainloop()
```

---

## A2 — To-Do List

```python
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List")
        self.geometry("340x320")
        self._build()

    def _build(self):
        # --- Input row ---
        input_frame = tk.Frame(self)
        input_frame.pack(fill="x", padx=10, pady=(10, 4))

        self._task_var = tk.StringVar()
        self._entry = tk.Entry(input_frame, textvariable=self._task_var, width=26)
        self._entry.pack(side="left", padx=(0, 6))
        tk.Button(input_frame, text="Add Task", command=self._add).pack(side="left")

        # --- Listbox with scrollbar ---
        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=4)

        self._listbox = tk.Listbox(list_frame, height=10, selectmode="single")
        sb = tk.Scrollbar(list_frame, command=self._listbox.yview)
        self._listbox.config(yscrollcommand=sb.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # --- Delete button ---
        tk.Button(self, text="Delete Selected", command=self._delete).pack(pady=6)

    def _add(self):
        task = self._task_var.get().strip()
        if not task:
            return
        self._listbox.insert(tk.END, task)
        self._task_var.set("")          # clear entry
        self._entry.focus_set()         # return focus to entry

    def _delete(self):
        selected = self._listbox.curselection()
        if selected:
            self._listbox.delete(selected[0])


if __name__ == "__main__":
    App().mainloop()
```

---

## A3 — Background Colour Picker

```python
import tkinter as tk

COLOURS = ["Red", "Blue", "Green", "Yellow", "White"]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Colour Picker")
        self.geometry("260x220")
        self._build()

    def _build(self):
        tk.Label(self, text="Choose a background colour:").pack(pady=(14, 6))

        # Start with White selected
        self._colour_var = tk.StringVar(value="White")
        self.configure(bg="White")

        for colour in COLOURS:
            tk.Radiobutton(
                self,
                text=colour,
                variable=self._colour_var,
                value=colour,
                command=self._change_bg,
            ).pack(anchor="w", padx=30)

    def _change_bg(self):
        # Reconfigure both the window and all child widgets that inherit bg
        self.configure(bg=self._colour_var.get())


if __name__ == "__main__":
    App().mainloop()
```

---

## A4 — Validated Registration Form

```python
import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registration Form")
        self.geometry("400x230")
        self._build()

    def _build(self):
        self._entries = {}   # field name -> Entry widget
        self._errors  = {}   # field name -> error Label widget

        field_specs = ["Name", "Email", "Age"]

        for row, field in enumerate(field_specs):
            tk.Label(self, text=f"{field}:").grid(
                row=row, column=0, padx=12, pady=6, sticky="e"
            )
            entry = tk.Entry(self, width=22)
            entry.grid(row=row, column=1, padx=4, pady=6, sticky="w")

            err_lbl = tk.Label(self, text="", fg="red", font=("Arial", 9))
            err_lbl.grid(row=row, column=2, padx=4, sticky="w")

            self._entries[field] = entry
            self._errors[field]  = err_lbl

        tk.Button(self, text="Submit", command=self._submit).grid(
            row=len(field_specs), column=0, columnspan=3, pady=14
        )

    def _submit(self):
        name  = self._entries["Name"].get().strip()
        email = self._entries["Email"].get().strip()
        age   = self._entries["Age"].get().strip()

        errors = {}

        if not name:
            errors["Name"] = "Name is required"

        if email.count("@") != 1:
            errors["Email"] = "Invalid email address"

        try:
            age_int = int(age)
            if not 1 <= age_int <= 120:
                raise ValueError
        except ValueError:
            errors["Age"] = "Age must be 1–120"

        # Apply error messages (empty string clears a passing field)
        for field, lbl in self._errors.items():
            lbl.config(text=errors.get(field, ""))

        if not errors:
            messagebox.showinfo("Success", "Form submitted successfully!")


if __name__ == "__main__":
    App().mainloop()
```

---

## A5 — File Reader

```python
import tkinter as tk
from tkinter import filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Reader")
        self.geometry("580x420")
        self._build()

    def _build(self):
        # --- Toolbar ---
        top = tk.Frame(self)
        top.pack(fill="x", padx=10, pady=8)

        tk.Button(top, text="Browse…", command=self._browse).pack(side="left")
        self._path_label = tk.Label(top, text="No file selected", anchor="w", fg="grey")
        self._path_label.pack(side="left", padx=10)

        # --- Text widget + scrollbars ---
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self._text = tk.Text(
            frame, state="disabled", wrap="none", font=("Courier", 10)
        )
        vsb = tk.Scrollbar(frame, command=self._text.yview)
        hsb = tk.Scrollbar(frame, orient="horizontal", command=self._text.xview)
        self._text.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")
        self._text.pack(fill="both", expand=True)

    def _browse(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return  # user cancelled

        self._path_label.config(text=path, fg="black")

        with open(path, encoding="utf-8", errors="replace") as fh:
            content = fh.read()

        # Must temporarily enable the widget before inserting text
        self._text.config(state="normal")
        self._text.delete("1.0", tk.END)
        self._text.insert("1.0", content)
        self._text.config(state="disabled")


if __name__ == "__main__":
    App().mainloop()
```

---

## A6 — Number Guessing Game

```python
import tkinter as tk
from tkinter import messagebox
import random


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Guessing Game")
        self.geometry("320x250")
        self._build()
        self._new_game()

    def _build(self):
        tk.Label(
            self, text="Guess a number between 1 and 100", font=("Arial", 11)
        ).pack(pady=(16, 4))

        self._tries_label = tk.Label(self, text="Tries: 0")
        self._tries_label.pack()

        # --- Input row ---
        row = tk.Frame(self)
        row.pack(pady=8)

        self._guess_var = tk.StringVar()
        self._entry = tk.Entry(
            row, textvariable=self._guess_var,
            width=8, font=("Arial", 14), justify="center"
        )
        self._entry.pack(side="left", padx=4)

        self._guess_btn = tk.Button(row, text="Guess", command=self._guess)
        self._guess_btn.pack(side="left", padx=4)

        self._feedback = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self._feedback.pack(pady=8)

        tk.Button(self, text="New Game", command=self._new_game).pack()

    def _new_game(self):
        self._secret = random.randint(1, 100)
        self._tries  = 0
        self._guess_var.set("")
        self._feedback.config(text="", fg="black")
        self._tries_label.config(text="Tries: 0")
        self._entry.config(state="normal")
        self._guess_btn.config(state="normal")
        self._entry.focus_set()

    def _guess(self):
        try:
            guess = int(self._guess_var.get())
        except ValueError:
            messagebox.showerror("Bad input", "Please enter a whole number.")
            return

        self._tries += 1
        self._tries_label.config(text=f"Tries: {self._tries}")
        self._guess_var.set("")

        if guess < self._secret:
            self._feedback.config(text="Too low!", fg="blue")
        elif guess > self._secret:
            self._feedback.config(text="Too high!", fg="red")
        else:
            self._feedback.config(
                text=f"Correct! You guessed it in {self._tries} tries.", fg="green"
            )
            self._entry.config(state="disabled")
            self._guess_btn.config(state="disabled")


if __name__ == "__main__":
    App().mainloop()
```

---

> **Exercises:** → [../../exercises/intermediate/exercises.md](../../exercises/intermediate/exercises.md)
