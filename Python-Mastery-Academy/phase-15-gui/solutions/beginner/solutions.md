# Phase 15 — Beginner Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/beginner/exercises.md`
>
> Every solution uses the recommended `class App(tk.Tk)` pattern.
> Copy any solution into a `.py` file and run it directly.

---

## A1 — Hello Tkinter

```python
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My First App")
        self.geometry("400x200")
        self._build()

    def _build(self):
        # StringVar lets us update the label text without keeping a Label reference
        self._label_text = tk.StringVar(value="Hello, Tkinter!")
        label = tk.Label(self, textvariable=self._label_text, font=("Arial", 14))
        # expand=True centres the widget vertically in the remaining space
        label.pack(expand=True)

        btn = tk.Button(self, text="Click Me", command=self._on_click)
        btn.pack(pady=10)

    def _on_click(self):
        # Update the StringVar — the label refreshes automatically
        self._label_text.set("Button clicked!")


if __name__ == "__main__":
    App().mainloop()
```

---

## A2 — Greeting Popup

```python
import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Greeting App")
        self.geometry("300x150")
        self._build()

    def _build(self):
        tk.Label(self, text="Enter your name:").pack(pady=(16, 4))

        self._name_var = tk.StringVar()
        self._entry = tk.Entry(self, textvariable=self._name_var, width=26)
        self._entry.pack()

        tk.Button(self, text="Greet", command=self._greet).pack(pady=10)

    def _greet(self):
        name = self._name_var.get().strip()
        if not name:
            messagebox.showwarning("No name", "Please enter a name.")
            return
        messagebox.showinfo("Hello!", f"Hello, {name}! Welcome to Tkinter.")


if __name__ == "__main__":
    App().mainloop()
```

---

## A3 — User Details Form

```python
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("User Details Form")
        self.geometry("320x180")
        self._build()

    def _build(self):
        fields = ["Name", "Email", "Age"]
        self._entries = {}

        for row, field in enumerate(fields):
            tk.Label(self, text=f"{field}:").grid(
                row=row, column=0, padx=12, pady=6, sticky="e"
            )
            entry = tk.Entry(self, width=22)
            entry.grid(row=row, column=1, padx=12, pady=6)
            self._entries[field] = entry

        # columnspan=2 centres the button across both label and entry columns
        tk.Button(self, text="Print Details", command=self._print_details).grid(
            row=len(fields), column=0, columnspan=2, pady=12
        )

    def _print_details(self):
        for field, entry in self._entries.items():
            print(f"{field}:  {entry.get()}")


if __name__ == "__main__":
    App().mainloop()
```

---

## A4 — Fruit Selector

```python
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fruit Selector")
        self.geometry("280x240")
        self._build()

    def _build(self):
        tk.Label(self, text="Select a fruit:").pack(pady=(12, 4))

        self._listbox = tk.Listbox(self, height=5, width=26)
        for fruit in ["Apple", "Banana", "Cherry", "Mango", "Orange"]:
            self._listbox.insert(tk.END, fruit)
        self._listbox.pack(padx=16)

        tk.Button(
            self, text="Show Selection", command=self._show_selection
        ).pack(pady=10)

    def _show_selection(self):
        # curselection() returns a tuple of selected indices (empty if none)
        selected = self._listbox.curselection()
        if selected:
            print(self._listbox.get(selected[0]))
        else:
            print("No fruit selected.")


if __name__ == "__main__":
    App().mainloop()
```

---

## A5 — Multi-line Text Pad

```python
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Pad")
        self.geometry("380x280")
        self._build()

    def _build(self):
        self._text = tk.Text(self, width=40, height=10)
        self._text.pack(padx=10, pady=(10, 4))

        tk.Button(self, text="Clear Text", command=self._clear).pack(pady=6)

    def _clear(self):
        # "1.0" = line 1, character 0 — the very beginning of the Text widget
        self._text.delete("1.0", tk.END)


if __name__ == "__main__":
    App().mainloop()
```

---

> **Exercises:** → [../../exercises/beginner/exercises.md](../../exercises/beginner/exercises.md)
