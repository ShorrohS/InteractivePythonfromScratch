# 🖥️ Phase 15 — GUI Applications

> **Goal:** Build desktop applications with graphical user interfaces using Tkinter.

---

## What is Tkinter?

Tkinter is Python's built-in GUI library. It comes with Python — no installation needed.

**When to use:**
- Internal desktop tools
- Simple data entry forms
- Desktop utilities
- Learning GUI concepts

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-basics.md](concepts/lesson-01-basics.md) | Window and widgets |
| 02 | [lesson-02-layout.md](concepts/lesson-02-layout.md) | Layout managers (pack, grid, place) |
| 03 | [lesson-03-events.md](concepts/lesson-03-events.md) | Event handling |
| 04 | [lesson-04-forms.md](concepts/lesson-04-forms.md) | Forms and input validation |
| 05 | [lesson-05-dialogs.md](concepts/lesson-05-dialogs.md) | Dialogs and file choosers |

---

## Basic Tkinter Structure

```python
import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("400x300")
        self.setup_ui()
    
    def setup_ui(self):
        # Label
        self.label = tk.Label(self, text="Hello, Tkinter!")
        self.label.pack(pady=10)
        
        # Entry
        self.entry = ttk.Entry(self, width=30)
        self.entry.pack(pady=5)
        
        # Button
        self.btn = ttk.Button(self, text="Click Me", command=self.on_click)
        self.btn.pack(pady=10)
    
    def on_click(self):
        name = self.entry.get()
        if name:
            messagebox.showinfo("Greeting", f"Hello, {name}!")
        else:
            messagebox.showwarning("Warning", "Please enter your name.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
```

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [Calculator GUI](guided-projects/project-01-calculator-gui/) | Full calculator with buttons |
| [Student Manager GUI](guided-projects/project-02-student-manager-gui/) | CRUD with treeview |

---

## ✅ Completion Checklist

- [ ] Can create a window with widgets
- [ ] Can use pack and grid layout
- [ ] Can handle button click events
- [ ] Can read from Entry fields
- [ ] Can show dialogs
- [ ] Built Calculator and Student Manager

---

## Previous: [Phase 14](../phase-14-testing/README.md) | Next: [Phase 16](../phase-16-web-development/README.md)
