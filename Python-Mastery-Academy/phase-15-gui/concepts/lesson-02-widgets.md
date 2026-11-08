# Lesson 02 — Widgets

**Phase:** 15 — GUI Applications | **Time:** ~40 min

---

## Part 1: What is a Widget?

A **widget** is a building block of a GUI — a button, a text box, a checkbox, a label. Every visible element in a Tkinter window is a widget.

**Analogy:** Widgets are like furniture in a room. Each piece (chair, table, lamp) serves a specific purpose and can be styled and positioned independently.

Two widget sets are available:
- `tk` — the classic, older widget set
- `ttk` (themed tk) — the modern replacement with a native look

**Always prefer `ttk` widgets when available.** The API is nearly identical, and they look better on every platform.

```python
import tkinter as tk
from tkinter import ttk   # themed widgets

root = tk.Tk()
root.geometry("450x400")
```

---

## Part 2: Label and Button

### Label — display text or images

```python
# Classic label with styling options
tk.Label(
    root,
    text="Classic Label",
    font=("Arial", 14),
    fg="navy",           # text color
    bg="lightyellow",    # background color
    width=20,            # width in text units
    height=2,            # height in text units
    relief="groove"      # border style: flat, raised, sunken, groove, ridge
).pack(pady=5)

# Themed label — prefer this for a modern look
ttk.Label(root, text="Themed Label", font=("Arial", 14)).pack(pady=5)
```

### Button — trigger an action

```python
def on_click():
    print("Button was clicked!")

# Themed button (preferred)
btn = ttk.Button(
    root,
    text="Click Me",
    command=on_click,   # function to call when clicked
    width=15
)
btn.pack(pady=5)

# Disable so the user cannot interact with it
btn.configure(state="disabled")   # use state="normal" to re-enable
```

---

## Part 3: Entry and Text

### Entry — single-line text input

```python
# Create an entry field
entry = ttk.Entry(
    root,
    width=30,
    show=""          # use show="*" to make a password field
)
entry.pack(pady=5)
entry.insert(0, "Default text")    # pre-fill on creation

# Read the value
value = entry.get()

# Clear the field
entry.delete(0, tk.END)            # delete from position 0 to end
```

### Text — multi-line text input

```python
text_box = tk.Text(
    root,
    height=6,     # height in lines
    width=40,     # width in characters
    wrap="word"   # wrap at word boundaries (or "char", "none")
)
text_box.pack(pady=5)

# Read all content ("line.char" format; "1.0" = first line, char 0)
content = text_box.get("1.0", tk.END)

# Insert text at the end
text_box.insert(tk.END, "New text here")

# Clear everything
text_box.delete("1.0", tk.END)
```

---

## Part 4: Checkbutton and Radiobutton

### Checkbutton — a toggle option

```python
agree_var = tk.BooleanVar(value=False)

check = ttk.Checkbutton(
    root,
    text="I agree to the terms",
    variable=agree_var    # links the widget to the variable
)
check.pack(pady=5)

# Read the current state
if agree_var.get():
    print("User agreed")
```

### Radiobutton — select exactly one option from a group

```python
size_var = tk.StringVar(value="medium")   # default selection

for size in ["small", "medium", "large"]:
    ttk.Radiobutton(
        root,
        text=size.capitalize(),
        variable=size_var,    # all radios in the group share ONE variable
        value=size
    ).pack(anchor="w", padx=20)

selected = size_var.get()    # "small", "medium", or "large"
```

---

## Part 5: Listbox

A `Listbox` displays a scrollable list of items.

```python
listbox = tk.Listbox(
    root,
    height=5,
    width=30,
    selectmode="single"   # or "extended" to allow multiple selection
)
listbox.pack(pady=5)

# Populate with items
for item in ["Apple", "Banana", "Cherry", "Date", "Elderberry"]:
    listbox.insert(tk.END, item)

# React when the user selects an item
def on_select(event):
    selection = listbox.curselection()   # tuple of selected indices
    if selection:
        index = selection[0]
        print(listbox.get(index))

listbox.bind("<<ListboxSelect>>", on_select)
```

---

## Part 6: Frame — Grouping Widgets

A `Frame` is a rectangular container that groups related widgets. It is invisible itself but gives structure to your layout.

**Use Frames to:**
- Organize widgets into logical sections
- Apply different layout managers in separate regions
- Apply a background color or border to a group

```python
# LabelFrame adds a visible border and a text label
section = ttk.LabelFrame(root, text="User Details", padding=10)
section.pack(fill="x", padx=10, pady=10)

ttk.Label(section, text="Name:").grid(row=0, column=0, sticky="w")
ttk.Entry(section, width=25).grid(row=0, column=1, padx=5)

ttk.Label(section, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
ttk.Entry(section, width=25).grid(row=1, column=1, padx=5)
```

---

## Part 7: Changing Widgets After Creation

Use `.config()` (or `.configure()`) to change a widget's properties after it is created. This is how you update the UI in response to user actions.

```python
label = ttk.Label(root, text="Status: Ready")
label.pack(pady=10)

def set_error():
    label.config(text="Status: Error!", foreground="red")

def set_ok():
    label.config(text="Status: OK", foreground="green")

ttk.Button(root, text="Simulate Error", command=set_error).pack(pady=2)
ttk.Button(root, text="Reset",          command=set_ok).pack(pady=2)
```

---

## Part 8: Reading Widget Values

```python
entry      = ttk.Entry(root, width=20)
entry_var  = tk.StringVar()
linked_entry = ttk.Entry(root, textvariable=entry_var)

text_box   = tk.Text(root, height=4, width=30)
check_var  = tk.BooleanVar(value=True)
radio_var  = tk.StringVar(value="A")

# Reading values
entry.get()                        # read directly from widget
entry_var.get()                    # read via linked StringVar (same result)
text_box.get("1.0", tk.END)        # read all text content
check_var.get()                    # True or False
radio_var.get()                    # the currently selected value string
```

---

## Practice Exercises

1. Create a form with a Label "What is your name?", an Entry, and a Button. When clicked, print the entry's value to the console.

2. Create a window with three Checkbuttons for toppings (Cheese, Bacon, Mushroom), each backed by a BooleanVar. Add a Button that prints which toppings are selected.

3. Add a Listbox with five country names. Print the selected country to the console when the user clicks one.

4. Create a LabelFrame titled "Preferences" containing two Radiobuttons for "Light Mode" and "Dark Mode". Add a Button that prints the current selection.

---

## Next Lesson

**[Lesson 03 → Layout Managers](lesson-03-layout-managers.md)**
