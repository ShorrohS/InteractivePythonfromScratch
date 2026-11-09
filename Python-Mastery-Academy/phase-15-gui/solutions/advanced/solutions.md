# Phase 15 — Advanced Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/advanced/exercises.md`
>
> Every solution is a complete, runnable Python script.

---

## A1 — Contact Manager

```python
import tkinter as tk
from tkinter import ttk, messagebox


class ContactDialog(tk.Toplevel):
    """Reusable modal dialog for Add and Edit operations."""

    def __init__(self, parent, title, initial=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.grab_set()          # make the dialog modal
        self.result = None
        self._build(initial or {"name": "", "phone": "", "email": ""})

    def _build(self, data):
        self._vars = {}
        for row, field in enumerate(["Name", "Phone", "Email"]):
            tk.Label(self, text=f"{field}:").grid(
                row=row, column=0, padx=12, pady=6, sticky="e"
            )
            var = tk.StringVar(value=data[field.lower()])
            self._vars[field.lower()] = var
            tk.Entry(self, textvariable=var, width=26).grid(
                row=row, column=1, padx=12, pady=6
            )

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="OK",     width=8, command=self._ok).pack(
            side="left", padx=6
        )
        tk.Button(btn_frame, text="Cancel", width=8, command=self.destroy).pack(
            side="left", padx=6
        )
        self.wait_window()   # block until dialog is closed

    def _ok(self):
        name = self._vars["name"].get().strip()
        if not name:
            messagebox.showwarning("Validation", "Name is required.", parent=self)
            return
        self.result = {k: v.get().strip() for k, v in self._vars.items()}
        self.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contact Manager")
        self.geometry("560x380")
        self._contacts: list[dict] = []
        self._build()

    def _build(self):
        # --- Treeview with scrollbar ---
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 4))

        cols = ("Name", "Phone", "Email")
        self._tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12)
        for col in cols:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=170)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # --- Action buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        for label, cmd in [("Add", self._add), ("Edit", self._edit), ("Delete", self._delete)]:
            tk.Button(btn_frame, text=label, width=8, command=cmd).pack(
                side="left", padx=6
            )

    def _refresh_tree(self):
        self._tree.delete(*self._tree.get_children())
        for c in self._contacts:
            self._tree.insert("", tk.END, values=(c["name"], c["phone"], c["email"]))

    def _selected_index(self):
        """Return list index of the selected Treeview row, or None."""
        sel = self._tree.selection()
        if not sel:
            return None
        return list(self._tree.get_children()).index(sel[0])

    def _add(self):
        dlg = ContactDialog(self, "Add Contact")
        if dlg.result:
            self._contacts.append(dlg.result)
            self._refresh_tree()

    def _edit(self):
        idx = self._selected_index()
        if idx is None:
            messagebox.showwarning("No selection", "Please select a contact to edit.")
            return
        dlg = ContactDialog(self, "Edit Contact", self._contacts[idx])
        if dlg.result:
            self._contacts[idx] = dlg.result
            self._refresh_tree()

    def _delete(self):
        idx = self._selected_index()
        if idx is None:
            messagebox.showwarning("No selection", "Please select a contact to delete.")
            return
        name = self._contacts[idx]["name"]
        if messagebox.askyesno("Confirm Delete", f"Delete contact '{name}'?"):
            self._contacts.pop(idx)
            self._refresh_tree()


if __name__ == "__main__":
    App().mainloop()
```

---

## A2 — Multi-Tab Profile App

```python
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Tab App")
        self.geometry("420x300")
        self._build()

    def _build(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        notebook.add(self._build_profile(notebook),  text="Profile")
        notebook.add(self._build_settings(notebook), text="Settings")
        notebook.add(self._build_about(notebook),    text="About")

    # ── Profile tab ──────────────────────────────────────────────────────
    def _build_profile(self, parent):
        frame = ttk.Frame(parent, padding=12)
        self._profile_vars = {}
        for row, field in enumerate(["First Name", "Last Name", "Email"]):
            ttk.Label(frame, text=f"{field}:").grid(
                row=row, column=0, sticky="e", pady=6, padx=4
            )
            var = tk.StringVar()
            self._profile_vars[field] = var
            ttk.Entry(frame, textvariable=var, width=26).grid(
                row=row, column=1, padx=8, pady=6
            )
        ttk.Button(frame, text="Save Profile", command=self._save_profile).grid(
            row=3, column=0, columnspan=2, pady=10
        )
        return frame

    def _save_profile(self):
        v = self._profile_vars
        name = f"{v['First Name'].get().strip()} {v['Last Name'].get().strip()}"
        messagebox.showinfo("Profile Saved", f"Profile saved for {name}.")

    # ── Settings tab ─────────────────────────────────────────────────────
    def _build_settings(self, parent):
        frame = ttk.Frame(parent, padding=12)
        self._notifications = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frame, text="Enable notifications", variable=self._notifications
        ).pack(anchor="w", pady=4)

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(frame, text="Theme:").pack(anchor="w")

        self._theme_var = tk.StringVar(value="Light")
        for theme in ("Light", "Dark", "System"):
            ttk.Radiobutton(
                frame, text=theme, variable=self._theme_var, value=theme
            ).pack(anchor="w", padx=20)

        ttk.Button(frame, text="Save Settings", command=self._save_settings).pack(pady=10)
        return frame

    def _save_settings(self):
        print(
            f"Notifications: {self._notifications.get()} | Theme: {self._theme_var.get()}"
        )

    # ── About tab ────────────────────────────────────────────────────────
    def _build_about(self, parent):
        frame = ttk.Frame(parent, padding=12)
        ttk.Label(
            frame,
            text="Multi-Tab Demo App\nVersion 1.0.0\nAuthor: Python Mastery Academy",
            justify="center",
        ).pack(pady=10)
        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=8)

        # Hyperlink-style label: blue, underlined, hand cursor
        link = tk.Label(
            frame, text="Visit python.org",
            fg="blue", cursor="hand2", font=("Arial", 10, "underline"),
        )
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open("https://www.python.org"))
        return frame


if __name__ == "__main__":
    App().mainloop()
```

---

## A3 — Canvas Drawing App

```python
import tkinter as tk
import random

COLOURS = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
RADIUS  = 15   # circle radius
HALF    = 15   # half-side of square


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Canvas Drawing App")
        self.geometry("560x490")
        self._circles = 0
        self._squares  = 0
        self._build()

    def _build(self):
        ctrl = tk.Frame(self)
        ctrl.pack(fill="x", padx=8, pady=4)
        tk.Button(ctrl, text="Clear Canvas", command=self._clear).pack(side="left")
        tk.Label(
            ctrl, text="Left-click: circle  |  Right-click: square", fg="grey"
        ).pack(side="left", padx=14)

        self._canvas = tk.Canvas(
            self, bg="white", width=540, height=410, relief="sunken", bd=2
        )
        self._canvas.pack(padx=8, pady=4)
        self._canvas.bind("<Button-1>", self._draw_circle)
        self._canvas.bind("<Button-3>", self._draw_square)

        self._status = tk.StringVar(value="Circles: 0 | Squares: 0")
        tk.Label(self, textvariable=self._status, anchor="w").pack(
            fill="x", padx=10, pady=2
        )

    def _colour(self):
        return random.choice(COLOURS)

    def _draw_circle(self, event):
        x, y = event.x, event.y
        self._canvas.create_oval(
            x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS,
            fill=self._colour(), outline=""
        )
        self._circles += 1
        self._update_status()

    def _draw_square(self, event):
        x, y = event.x, event.y
        self._canvas.create_rectangle(
            x - HALF, y - HALF, x + HALF, y + HALF,
            fill=self._colour(), outline=""
        )
        self._squares += 1
        self._update_status()

    def _clear(self):
        self._canvas.delete("all")
        self._circles = self._squares = 0
        self._update_status()

    def _update_status(self):
        self._status.set(f"Circles: {self._circles} | Squares: {self._squares}")


if __name__ == "__main__":
    App().mainloop()
```

---

## A4 — Stopwatch

```python
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stopwatch")
        self.geometry("280x200")
        self._ticks    = 0       # 1 tick = 100 ms
        self._running  = False
        self._after_id = None
        self._build()

    def _build(self):
        self._display = tk.Label(
            self, text="00:00.0", font=("Courier", 48, "bold")
        )
        self._display.pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack()

        self._start_btn = tk.Button(
            btn_frame, text="Start", width=7, command=self._start
        )
        self._stop_btn = tk.Button(
            btn_frame, text="Stop", width=7, command=self._stop, state="disabled"
        )
        self._reset_btn = tk.Button(
            btn_frame, text="Reset", width=7, command=self._reset
        )
        self._start_btn.pack(side="left", padx=4)
        self._stop_btn.pack(side="left",  padx=4)
        self._reset_btn.pack(side="left", padx=4)

    def _tick(self):
        if self._running:
            self._ticks += 1
            self._update_display()
            self._after_id = self.after(100, self._tick)

    def _update_display(self):
        total_s  = self._ticks // 10
        minutes  = total_s // 60
        seconds  = total_s % 60
        tenths   = self._ticks % 10
        self._display.config(text=f"{minutes:02d}:{seconds:02d}.{tenths}")

    def _start(self):
        if not self._running:
            self._running = True
            self._start_btn.config(state="disabled")
            self._stop_btn.config(state="normal")
            self._tick()

    def _stop(self):
        self._running = False
        if self._after_id:
            self.after_cancel(self._after_id)
        self._start_btn.config(state="normal")
        self._stop_btn.config(state="disabled")

    def _reset(self):
        self._stop()
        self._ticks = 0
        self._display.config(text="00:00.0")


if __name__ == "__main__":
    App().mainloop()
```

---

## A5 — MVC Contact App

```python
"""
MVC Contact App
===============
Model  — pure data + logic, zero tkinter
View   — pure UI, zero business logic
Controller — wires the two together
"""

import tkinter as tk
from tkinter import messagebox


# ============================================================
# MODEL — owns data and business rules, no UI
# ============================================================
class ContactModel:
    """Stores contacts in memory; exposes add, delete, get_all."""

    def __init__(self):
        self._contacts: list[dict] = []

    def add_contact(self, name: str, phone: str) -> None:
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        self._contacts.append({"name": name.strip(), "phone": phone.strip()})

    def delete_contact(self, index: int) -> None:
        if 0 <= index < len(self._contacts):
            self._contacts.pop(index)

    def get_all(self) -> list[dict]:
        return list(self._contacts)


# ============================================================
# VIEW — builds the UI; exposes a clean public interface
# ============================================================
class ContactView(tk.Frame):
    """Renders the UI. No business logic; no direct Model access."""

    def __init__(self, parent):
        super().__init__(parent)
        self._build()

    def _build(self):
        # Listbox
        list_frame = tk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self._listbox = tk.Listbox(list_frame, height=10, width=40)
        sb = tk.Scrollbar(list_frame, command=self._listbox.yview)
        self._listbox.config(yscrollcommand=sb.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Input row
        row = tk.Frame(self)
        row.pack(fill="x", padx=10, pady=(0, 4))
        tk.Label(row, text="Name:").pack(side="left")
        self._name_entry = tk.Entry(row, width=16)
        self._name_entry.pack(side="left", padx=4)
        tk.Label(row, text="Phone:").pack(side="left")
        self._phone_entry = tk.Entry(row, width=14)
        self._phone_entry.pack(side="left", padx=4)
        self.add_btn = tk.Button(row, text="Add")
        self.add_btn.pack(side="left", padx=4)

        # Delete button (Controller wires its command)
        self.delete_btn = tk.Button(self, text="Delete Selected")
        self.delete_btn.pack(pady=6)

    # Public interface for the Controller ──────────────────────────────

    def set_contacts(self, contacts: list[dict]) -> None:
        """Rebuild the Listbox from the provided contact list."""
        self._listbox.delete(0, tk.END)
        for c in contacts:
            self._listbox.insert(tk.END, f"{c['name']}  —  {c['phone']}")

    def get_name(self) -> str:
        return self._name_entry.get()

    def get_phone(self) -> str:
        return self._phone_entry.get()

    def clear_inputs(self) -> None:
        self._name_entry.delete(0, tk.END)
        self._phone_entry.delete(0, tk.END)

    def get_selection(self):
        sel = self._listbox.curselection()
        return sel[0] if sel else None


# ============================================================
# CONTROLLER — wires Model and View; owns all event logic
# ============================================================
class ContactController:
    """Coordinates Model ↔ View; handles user events."""

    def __init__(self, model: ContactModel, view: ContactView):
        self._model = model
        self._view  = view
        view.add_btn.config(command=self._on_add)
        view.delete_btn.config(command=self._on_delete)
        self._refresh()

    def _refresh(self):
        self._view.set_contacts(self._model.get_all())

    def _on_add(self):
        try:
            self._model.add_contact(self._view.get_name(), self._view.get_phone())
        except ValueError as exc:
            messagebox.showwarning("Validation", str(exc))
            return
        self._view.clear_inputs()
        self._refresh()

    def _on_delete(self):
        idx = self._view.get_selection()
        if idx is None:
            messagebox.showwarning("No selection", "Select a contact to delete.")
            return
        self._model.delete_contact(idx)
        self._refresh()


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("MVC Contact App")
    root.geometry("440x340")

    model = ContactModel()
    view  = ContactView(root)
    view.pack(fill="both", expand=True)
    ContactController(model, view)

    root.mainloop()
```

---

## A6 — CSV Viewer

```python
import tkinter as tk
from tkinter import ttk, filedialog
import csv
import os


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Viewer")
        self.geometry("720x480")
        self._data:    list[tuple] = []
        self._headers: list[str]  = []
        self._sort_col = None
        self._sort_asc = True
        self._build()

    def _build(self):
        # --- Toolbar ---
        toolbar = tk.Frame(self, bd=1, relief="flat")
        toolbar.pack(fill="x", padx=8, pady=6)
        tk.Button(toolbar, text="Load CSV…", command=self._load).pack(side="left")
        self._status_var = tk.StringVar(value="No file loaded.")
        tk.Label(toolbar, textvariable=self._status_var, fg="grey").pack(
            side="left", padx=12
        )

        # --- Treeview with scrollbars ---
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self._tree = ttk.Treeview(frame, show="headings")
        vsb = ttk.Scrollbar(frame, orient="vertical",   command=self._tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self._tree.xview)
        self._tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")
        self._tree.pack(fill="both", expand=True)

    def _load(self):
        path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return

        with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
            rows = list(csv.reader(fh))

        if not rows:
            self._status_var.set("File is empty.")
            return

        self._headers  = rows[0]
        self._data     = [tuple(r) for r in rows[1:]]
        self._sort_col = None
        self._sort_asc = True

        self._setup_columns()
        self._populate()

        fname = os.path.basename(path)
        self._status_var.set(
            f"Loaded: {fname}  |  Rows: {len(self._data)}  |  Columns: {len(self._headers)}"
        )

    def _setup_columns(self):
        self._tree.delete(*self._tree.get_children())
        self._tree["columns"] = self._headers
        for col in self._headers:
            self._tree.heading(col, text=col,
                               command=lambda c=col: self._sort_by(c))
            self._tree.column(col, width=120, minwidth=60)

    def _populate(self):
        self._tree.delete(*self._tree.get_children())
        for row in self._data:
            self._tree.insert("", tk.END, values=row)

    def _sort_by(self, col: str):
        idx = self._headers.index(col)

        # Toggle direction if same column clicked again
        if self._sort_col == col:
            self._sort_asc = not self._sort_asc
        else:
            self._sort_col = col
            self._sort_asc = True

        def key(row):
            val = row[idx]
            try:
                return (0, float(val))       # numeric sort when possible
            except (ValueError, TypeError):
                return (1, str(val).lower()) # fall back to alphabetic

        self._data.sort(key=key, reverse=not self._sort_asc)
        self._populate()

        # Refresh headings to show sort-direction arrow
        for h in self._headers:
            arrow = ""
            if h == col:
                arrow = " ↑" if self._sort_asc else " ↓"
            self._tree.heading(h, text=h + arrow,
                               command=lambda c=h: self._sort_by(c))


if __name__ == "__main__":
    App().mainloop()
```

---

> **Exercises:** → [../../exercises/advanced/exercises.md](../../exercises/advanced/exercises.md)
