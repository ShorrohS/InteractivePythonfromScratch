# ⚡ Phase 15 — Quick Reference: Tkinter GUI

---

## Widget Creation Table

| Widget | Import | Typical constructor |
|--------|--------|---------------------|
| `Label` | `tk` | `tk.Label(parent, text="Hello", font=("Arial", 12))` |
| `Entry` | `tk` | `tk.Entry(parent, textvariable=str_var, width=20)` |
| `Button` | `tk` | `tk.Button(parent, text="OK", command=callback)` |
| `Checkbutton` | `tk` | `tk.Checkbutton(parent, text="Enable", variable=bool_var)` |
| `Radiobutton` | `tk` | `tk.Radiobutton(parent, text="A", variable=str_var, value="a")` |
| `Listbox` | `tk` | `tk.Listbox(parent, height=6, selectmode="single")` |
| `Text` | `tk` | `tk.Text(parent, width=40, height=8)` |
| `Canvas` | `tk` | `tk.Canvas(parent, width=400, height=300, bg="white")` |
| `Combobox` | `ttk` | `ttk.Combobox(parent, values=["A","B"], textvariable=str_var)` |
| `Treeview` | `ttk` | `ttk.Treeview(parent, columns=("Name","Age"), show="headings")` |
| `Notebook` | `ttk` | `ttk.Notebook(parent)` |
| `Frame` | `ttk` | `ttk.Frame(parent, padding=10)` |
| `LabelFrame` | `ttk` | `ttk.LabelFrame(parent, text="Group")` |
| `Scrollbar` | `ttk` | `ttk.Scrollbar(parent, orient="vertical", command=widget.yview)` |

---

## Common Config Options

| Option | Type | Description |
|--------|------|-------------|
| `text` | str | Static display text |
| `textvariable` | StringVar | Auto-updating text source |
| `variable` | IntVar / BooleanVar / StringVar | Linked variable for Checkbutton / Radiobutton |
| `command` | callable | Callback for Button (no parentheses!) |
| `width` | int | Width in characters (Entry/Text) or pixels (Canvas) |
| `height` | int | Height in lines (Text/Listbox) or pixels (Canvas) |
| `bg` / `background` | str | Background colour (`"white"`, `"#3498db"`) |
| `fg` / `foreground` | str | Text colour |
| `font` | tuple | `("Arial", 12)` or `("Courier", 10, "bold")` |
| `relief` | str | `"flat"`, `"raised"`, `"sunken"`, `"groove"`, `"ridge"` |
| `padx` / `pady` | int | Internal padding (pixels) |
| `state` | str | `"normal"`, `"disabled"`, `"readonly"` |
| `cursor` | str | Mouse cursor: `"hand2"`, `"arrow"`, `"crosshair"` |

---

## Layout Manager Comparison

### pack — vertical / horizontal stacking

```python
widget.pack()                            # stack vertically (default)
widget.pack(side=tk.LEFT)                # stack horizontally
widget.pack(fill=tk.X)                   # stretch horizontally
widget.pack(fill=tk.BOTH, expand=True)   # fill all available space
widget.pack(padx=10, pady=5)             # outer padding
widget.pack(anchor="w")                  # align: n s e w ne nw se sw center
```

### grid — row/column table

```python
widget.grid(row=0, column=0)
widget.grid(row=0, column=1, columnspan=2)   # span two columns
widget.grid(sticky="ew")                     # stretch East↔West
widget.grid(sticky="nsew")                   # fill entire cell
widget.grid(padx=6, pady=4)                  # outer padding
widget.grid(ipadx=4, ipady=4)                # inner padding

# Make a column/row expand when window is resized:
parent.columnconfigure(1, weight=1)
parent.rowconfigure(0, weight=1)
```

### place — exact pixel positioning

```python
widget.place(x=50, y=100)                # absolute position
widget.place(relx=0.5, rely=0.5,         # centred (50% × 50%)
             anchor="center")
widget.place(relwidth=1.0, relheight=1.0) # fill parent exactly
```

> **Rule:** All widgets in the same parent must use the **same** layout manager.  
> Mixing `pack` and `grid` in one parent raises `TclError`.

---

## Event Binding Table

| Event string | Triggered when |
|---|---|
| `"<Button-1>"` | Left mouse button clicked |
| `"<Button-3>"` | Right mouse button clicked |
| `"<Double-Button-1>"` | Left button double-clicked |
| `"<Return>"` | Enter key pressed |
| `"<Key>"` | Any key pressed |
| `"<KeyRelease>"` | Any key released |
| `"<FocusIn>"` | Widget receives keyboard focus |
| `"<FocusOut>"` | Widget loses keyboard focus |
| `"<Configure>"` | Widget resized or moved |
| `"<<ComboboxSelected>>"` | ttk.Combobox item chosen |
| `"<Control-s>"` | Ctrl+S keyboard shortcut |

```python
# Usage:
widget.bind("<Return>", self.on_enter)   # event arg is passed automatically

def on_enter(self, event):               # always accept the event parameter
    print(event.x, event.y)             # mouse coords (for mouse events)
    print(event.char)                   # character typed (for key events)
```

---

## Variable Classes

```python
str_var  = tk.StringVar(value="default")   # for Entry, Label, Combobox
int_var  = tk.IntVar(value=0)              # for Spinbox, Scale
bool_var = tk.BooleanVar(value=False)      # for Checkbutton

str_var.get()             # read current value
str_var.set("new value")  # write value — linked widgets update automatically

# Watch for changes:
str_var.trace_add("write", lambda *args: callback())
```

---

## Dialog Shortcuts

```python
from tkinter import messagebox, filedialog, simpledialog

# Information dialogs
messagebox.showinfo("Title",    "Message")
messagebox.showwarning("Title", "Warning")
messagebox.showerror("Title",   "Error")

# Question dialogs (return bool)
yes = messagebox.askyesno("Title", "Continue?")   # True / False

# Input dialogs
name = simpledialog.askstring("Input", "Enter name:")
num  = simpledialog.askfloat("Input",  "Enter amount:")

# File dialogs
open_path = filedialog.askopenfilename(
    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
)
save_path = filedialog.asksaveasfilename(
    defaultextension=".txt",
    filetypes=[("Text files", "*.txt")]
)
```

---

## Treeview (Table)

```python
tree = ttk.Treeview(parent, columns=("Name", "Age"), show="headings")
tree.heading("Name", text="Full Name", command=lambda: sort_by("Name"))
tree.column("Name", width=150, minwidth=80)

tree.insert("", tk.END, values=("Alice", 30))   # add a row
tree.delete(*tree.get_children())                # clear all rows

# Get selected row values
sel = tree.selection()
if sel:
    vals = tree.item(sel[0])["values"]

# Scrollbar attachment
vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
```

---

## after() — Timed Callbacks

```python
# Run callback once after 2000 ms (2 seconds):
self.after(2000, self.my_callback)

# Repeating timer (call after() again inside the callback):
def _tick(self):
    self._count += 1
    self._label.config(text=str(self._count))
    self._job = self.after(1000, self._tick)   # schedule next tick

# Cancel a pending callback:
self.after_cancel(self._job)
```

---

## ttk.Style — Custom Themes

```python
from tkinter import ttk

style = ttk.Style()
style.theme_use("clam")   # "clam", "alt", "default", "classic"

# Custom style for a specific widget type:
style.configure("Accent.TButton", foreground="white", background="#3498db",
                font=("Arial", 10, "bold"))
ttk.Button(parent, text="OK", style="Accent.TButton")
```

---

## Recommended App Skeleton

```python
import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("400x300")
        self._build()

    def _build(self):
        # Create all widgets here
        ttk.Label(self, text="Hello").pack(pady=10)
        ttk.Button(self, text="Click", command=self._on_click).pack()

    def _on_click(self):
        messagebox.showinfo("Hi", "Button clicked!")

if __name__ == "__main__":
    App().mainloop()
```

---

## ⚠️ Common Gotchas

| Mistake | Fix |
|---------|-----|
| Window opens and immediately closes | You forgot `mainloop()` |
| `TclError: cannot use geometry manager grid inside ... which already has slaves managed by pack` | All widgets in one parent must use the same layout manager |
| Button callback fires at startup, not on click | `command=self.save()` → change to `command=self.save` |
| Lambda in loop — all buttons run same code | `lambda: print(x)` → `lambda x=x: print(x)` |
| Entry reads as empty or wrong type | `entry.get()` returns a `str`; cast with `int()` or `float()` |
| `widget.get()` called on Label instead of Entry | Labels have no `.get()`; use `StringVar.get()` |
| Text widget appears read-only when you try to insert | Set `state="normal"` before inserting, then back to `"disabled"` |
| Toplevel dialog doesn't block the main window | Add `dialog.grab_set()` and `dialog.wait_window()` |
