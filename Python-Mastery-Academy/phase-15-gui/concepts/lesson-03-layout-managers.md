# Lesson 03 — Layout Managers

**Phase:** 15 — GUI Applications | **Time:** ~35 min

---

## Part 1: Why Layout Managers?

In many GUI toolkits you place widgets using exact pixel coordinates: "put this button at x=120, y=80." That breaks the moment the window is resized or the font size changes on a different machine.

**Layout managers** handle positioning automatically. You describe relationships — "stack this below that" or "put this in row 1, column 2" — and Tkinter works out the pixel arithmetic.

Tkinter has three layout managers:

| Manager | Best for |
|---------|---------|
| `pack` | Simple top-to-bottom or side-by-side stacks |
| `grid` | Forms, tables, anything with rows and columns |
| `place` | Rare cases needing exact pixel positioning |

**Critical rule:** never mix `pack` and `grid` on widgets inside the same parent container. Use nested `Frame`s to keep them separate.

---

## Part 2: pack()

`pack()` stacks widgets along one edge of their parent, one after another.

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x250")

# Default: stacks top to bottom
ttk.Label(root, text="First").pack()
ttk.Label(root, text="Second").pack()
ttk.Label(root, text="Third").pack()

root.mainloop()
```

### Key options

```python
# side — which edge to stack against (default: "top")
ttk.Button(root, text="Left").pack(side="left")
ttk.Button(root, text="Right").pack(side="right")
ttk.Button(root, text="Bottom").pack(side="bottom")

# fill — expand to fill available space
ttk.Label(root, text="Fill X").pack(fill="x")                   # stretch horizontally
ttk.Label(root, text="Fill Both").pack(fill="both", expand=True) # fill all space

# expand — claim extra space when the window is resized
ttk.Label(root, text="Centered").pack(expand=True)

# padx, pady — external padding in pixels
ttk.Button(root, text="Padded").pack(padx=10, pady=5)
```

### Practical pack example — toolbar

```python
toolbar = ttk.Frame(root)
toolbar.pack(side="top", fill="x")

ttk.Button(toolbar, text="New").pack(side="left",  padx=2, pady=2)
ttk.Button(toolbar, text="Open").pack(side="left", padx=2, pady=2)
ttk.Button(toolbar, text="Save").pack(side="left", padx=2, pady=2)
ttk.Button(toolbar, text="Quit").pack(side="right", padx=2, pady=2)
```

`pack` is ideal for toolbars and simple vertical stacks. Once layout gets more complex, switch to `grid`.

---

## Part 3: grid()

`grid()` places widgets in a table of rows and columns. It is the most flexible manager and the best choice for forms.

```python
root = tk.Tk()
root.geometry("350x200")

# Basic two-column form
ttk.Label(root, text="Name:").grid(row=0, column=0)
ttk.Entry(root, width=25).grid(row=0, column=1)

ttk.Label(root, text="Email:").grid(row=1, column=0)
ttk.Entry(root, width=25).grid(row=1, column=1)

ttk.Button(root, text="Submit").grid(row=2, column=0, columnspan=2)
```

### Key options

```python
# padx, pady — space around the cell
widget.grid(row=0, column=0, padx=5, pady=5)

# sticky — anchor or stretch within the cell (compass directions)
# "w"    — align left
# "e"    — align right
# "ew"   — stretch left-right
# "nsew" — fill the entire cell
ttk.Label(root, text="Label:").grid(row=0, column=0, sticky="w")
ttk.Entry(root, width=20).grid(row=0, column=1, sticky="ew")

# columnspan / rowspan — merge multiple cells
ttk.Button(root, text="Wide Button").grid(row=3, column=0, columnspan=3)

# Make columns and rows resize with the window
root.columnconfigure(1, weight=1)   # column 1 stretches when window widens
root.rowconfigure(2, weight=1)
```

### Practical grid example — login form

```python
root = tk.Tk()
root.title("Login")
root.geometry("300x150")
root.columnconfigure(1, weight=1)

fields = [("Username:", 0), ("Password:", 1)]
entries = {}

for label_text, row in fields:
    ttk.Label(root, text=label_text).grid(
        row=row, column=0, sticky="w", padx=10, pady=8
    )
    show_char = "*" if "Password" in label_text else ""
    e = ttk.Entry(root, width=20, show=show_char)
    e.grid(row=row, column=1, sticky="ew", padx=10)
    entries[label_text] = e

ttk.Button(root, text="Log In").grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
```

---

## Part 4: place()

`place()` positions a widget using exact coordinates. Use it rarely — only when layout managers cannot achieve what you need.

```python
btn = ttk.Button(root, text="Exact Position")
btn.place(x=50, y=80)           # absolute pixels from top-left corner

# Relative positioning (0.0 to 1.0 — scales with window size)
btn2 = ttk.Button(root, text="Centered")
btn2.place(relx=0.5, rely=0.5, anchor="center")
```

**When `place()` makes sense:**
- Overlapping widgets (e.g., a badge on top of an icon)
- Canvas-like custom drawing areas
- Animating a widget to a specific position

For anything else, prefer `pack` or `grid`.

---

## Part 5: pack vs grid — Side-by-Side Comparison

The same two-field form with a Submit button, built both ways:

### With pack — awkward for forms

```python
# pack requires wrapping each row in its own Frame to align labels and entries
row1 = ttk.Frame(root)
row1.pack(fill="x", padx=10, pady=5)
ttk.Label(row1, text="Name:", width=10).pack(side="left")
ttk.Entry(row1).pack(side="left", fill="x", expand=True)

row2 = ttk.Frame(root)
row2.pack(fill="x", padx=10, pady=5)
ttk.Label(row2, text="Email:", width=10).pack(side="left")
ttk.Entry(row2).pack(side="left", fill="x", expand=True)

ttk.Button(root, text="Submit").pack(pady=10)
```

### With grid — cleaner for forms

```python
# grid lines up labels and entries naturally
root.columnconfigure(1, weight=1)

ttk.Label(root, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
ttk.Entry(root).grid(row=0, column=1, sticky="ew", padx=10)

ttk.Label(root, text="Email:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
ttk.Entry(root).grid(row=1, column=1, sticky="ew", padx=10)

ttk.Button(root, text="Submit").grid(row=2, column=0, columnspan=2, pady=10)
```

**Rule of thumb:** use `pack` for toolbars and simple vertical stacks; use `grid` for anything with two or more columns.

---

## Part 6: Mixing Managers Safely with Frames

You cannot call both `pack` and `grid` on widgets inside the same container — Tkinter will raise a runtime error. The solution is nested `Frame`s:

```python
root = tk.Tk()
root.geometry("400x300")

# Top section: toolbar using pack
toolbar = ttk.Frame(root)
toolbar.pack(side="top", fill="x")

ttk.Button(toolbar, text="File").pack(side="left", padx=2, pady=2)
ttk.Button(toolbar, text="Edit").pack(side="left", padx=2, pady=2)

# Main section: form using grid — lives in a separate Frame
main = ttk.Frame(root)
main.pack(fill="both", expand=True, padx=10, pady=10)
main.columnconfigure(1, weight=1)

ttk.Label(main, text="Name:").grid(row=0, column=0, sticky="w")
ttk.Entry(main).grid(row=0, column=1, sticky="ew", padx=5)

ttk.Label(main, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
ttk.Entry(main).grid(row=1, column=1, sticky="ew", padx=5)

root.mainloop()
```

The toolbar uses `pack`; the form uses `grid`. They live in separate `Frame`s, so there is no conflict.

---

## Practice Exercises

1. Use `pack()` to create a window with a title label at the top, a large Text area in the middle that expands to fill the available space, and a "Save" button at the bottom.

2. Use `grid()` to build a 3-field registration form (Name, Email, Phone) with a Submit button spanning both columns.

3. Using `place()`, center a label in a 400×300 window with `relx=0.5, rely=0.5, anchor="center"`.

4. Create a window with a toolbar (using `pack`) at the top and a login form (using `grid`) below it, each in its own `Frame` so the managers do not conflict.

---

## Next Lesson

**[Lesson 04 → Event Handling and Callbacks](lesson-04-event-handling.md)**
