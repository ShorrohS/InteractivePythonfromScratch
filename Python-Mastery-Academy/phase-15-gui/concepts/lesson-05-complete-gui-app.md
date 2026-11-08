# Lesson 05 — Building a Complete GUI Application

**Phase:** 15 — GUI Applications | **Time:** ~50 min

---

## Part 1: Class-Based Architecture

Small scripts work fine with a procedural approach. Real applications need structure. The standard pattern is to subclass `tk.Tk` and put all UI construction in a private method.

```python
import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()          # initialize the Tk window
        self.title("My App")
        self.geometry("500x400")
        self.resizable(True, True)
        self._build_ui()            # separate method keeps __init__ clean

    def _build_ui(self):
        pass   # create and arrange widgets here
```

**Why inherit from `tk.Tk` instead of keeping `root = tk.Tk()` as an attribute?**
- `self` IS the window — pass `self` as the parent to every widget
- Window methods like `self.title()` and `self.mainloop()` are available directly
- The class cleanly encapsulates all window state and behavior

---

## Part 2: Separation of Concerns

Split your code into three layers so each part has one job:

| Layer | Responsibility | Example methods |
|-------|---------------|----------------|
| UI layer | Create and arrange widgets | `_build_ui`, `_create_toolbar` |
| Event layer | Handle user actions, validate input | `_on_add`, `_on_delete` |
| Data layer | Manage application data | `self._tasks`, `_refresh_list` |

The UI layer should **never** contain business logic. The data layer should **never** touch widgets directly. The full Task Manager in Part 5 shows each layer in action.

---

## Part 3: Multiple Frames and Switching Views

For multi-page applications, stack all frames in the same grid cell and use `tkraise()` to bring one to the front.

```python
class MultiPageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page App")
        self.geometry("400x300")

        # Container that holds all pages
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._pages: dict[str, ttk.Frame] = {}
        for name, PageClass in [("Home", HomePage), ("Settings", SettingsPage)]:
            page = PageClass(container, self)
            page.grid(row=0, column=0, sticky="nsew")
            self._pages[name] = page

        self.show_page("Home")

    def show_page(self, name: str):
        self._pages[name].tkraise()   # bring the named page to the front


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Home Page", font=("Arial", 18)).pack(pady=30)
        ttk.Button(
            self, text="Go to Settings",
            command=lambda: controller.show_page("Settings")
        ).pack()


class SettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Settings Page", font=("Arial", 18)).pack(pady=30)
        ttk.Button(
            self, text="Back to Home",
            command=lambda: controller.show_page("Home")
        ).pack()
```

---

## Part 4: Form Validation

Always validate input before processing. Use `messagebox` to give the user clear, actionable feedback.

```python
def _validate_and_submit(self):
    name  = self._name_var.get().strip()
    email = self._email_var.get().strip()
    age   = self._age_var.get().strip()

    # Required field
    if not name:
        messagebox.showwarning("Validation Error", "Name is required.")
        self._name_entry.focus()
        return

    # Basic format check
    if "@" not in email or "." not in email:
        messagebox.showwarning("Validation Error", "Please enter a valid email address.")
        self._email_entry.focus()
        return

    # Type and range check
    try:
        age_int = int(age)
        if not 0 <= age_int <= 130:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Validation Error", "Age must be a number between 0 and 130.")
        return

    # All checks passed — proceed
    messagebox.showinfo("Success", f"Welcome, {name}!")
```

---

## Part 5: Complete Task Manager Application

A full working Task Manager demonstrating every concept from this phase:

```python
import tkinter as tk
from tkinter import ttk, messagebox


class TaskManagerApp(tk.Tk):
    """Complete task manager: add, display, and delete tasks."""

    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("480x380")
        self.resizable(True, True)
        self.columnconfigure(0, weight=1)

        self._tasks: list[str] = []   # in-memory data store
        self._task_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        # Header
        ttk.Label(
            self, text="Task Manager", font=("Arial", 16, "bold")
        ).pack(pady=(15, 5))

        # Input row: entry + Add button side by side
        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", padx=15, pady=5)
        input_frame.columnconfigure(0, weight=1)

        self._entry = ttk.Entry(input_frame, textvariable=self._task_var, width=35)
        self._entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self._entry.bind("<Return>", lambda e: self._on_add())  # Enter adds task

        ttk.Button(input_frame, text="Add Task", command=self._on_add).grid(row=0, column=1)

        # Task list with scrollbar
        list_frame = ttk.LabelFrame(self, text="Tasks", padding=5)
        list_frame.pack(fill="both", expand=True, padx=15, pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self._listbox = tk.Listbox(list_frame, selectmode="single", font=("Arial", 11))
        self._listbox.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical",
                                   command=self._listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._listbox.configure(yscrollcommand=scrollbar.set)

        # Button row + status
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))

        ttk.Button(
            btn_frame, text="Delete Selected", command=self._on_delete
        ).pack(side="left", padx=(0, 5))
        ttk.Button(
            btn_frame, text="Clear All", command=self._on_clear_all
        ).pack(side="left")

        self._status_var = tk.StringVar(value="0 tasks")
        ttk.Label(btn_frame, textvariable=self._status_var).pack(side="right")

        self._entry.focus()

    def _on_add(self):
        task = self._task_var.get().strip()

        if not task:
            messagebox.showwarning("Validation", "Please enter a task name.")
            self._entry.focus()
            return

        if task in self._tasks:
            messagebox.showwarning("Duplicate", f"'{task}' is already in the list.")
            return

        self._tasks.append(task)
        self._task_var.set("")
        self._refresh_list()
        self._entry.focus()

    def _on_delete(self):
        selection = self._listbox.curselection()
        if not selection:
            messagebox.showinfo("Delete", "Select a task to delete first.")
            return

        index = selection[0]
        task  = self._tasks[index]

        if messagebox.askyesno("Confirm Delete", f"Delete '{task}'?"):
            self._tasks.pop(index)
            self._refresh_list()

    def _on_clear_all(self):
        if not self._tasks:
            return
        if messagebox.askyesno("Confirm Clear", "Delete all tasks?"):
            self._tasks.clear()
            self._refresh_list()

    def _refresh_list(self):
        self._listbox.delete(0, tk.END)
        for task in self._tasks:
            self._listbox.insert(tk.END, task)
        count = len(self._tasks)
        self._status_var.set(f"{count} task{'s' if count != 1 else ''}")


if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()
```

---

## Part 6: Best Practices Recap

| Tip | Reason |
|-----|--------|
| Use `ttk` widgets | Native look on every platform |
| Put `mainloop()` once at the bottom | Only one event loop per application |
| Use `StringVar` for labels that change | Cleaner than calling `.config()` everywhere |
| Always validate before processing | Prevents crashes and bad data |
| Separate UI, events, and data | Easier to read, test, and extend |
| Use `LabelFrame` to group related fields | Gives visual structure for the user |
| Attach a `Scrollbar` to every `Listbox` | Lists can grow beyond the visible area |

---

## Practice Exercises

1. Add a "Mark as Done" feature to the Task Manager: double-clicking a task should prepend "✅ " to its text in the list.

2. Save tasks to a plain text file (`tasks.txt`) when the app closes. Load them back on startup. Hint: override `destroy()` to save, and load in `__init__` before `_build_ui()`.

3. Build a two-page app (Home and About) using the multi-page pattern from Part 3. The Home page shows a greeting and the About page shows your name and today's date.

---

## Phase 15 Complete

You can now build real desktop applications with Python. The skills learned here — event-driven thinking, layout management, validation, and clean class-based structure — transfer directly to larger GUI frameworks like PyQt and wxPython.

**[Back to Phase 15 README](../README.md)**
