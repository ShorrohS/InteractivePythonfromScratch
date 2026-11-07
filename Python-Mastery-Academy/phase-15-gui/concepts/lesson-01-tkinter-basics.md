# Lesson 01 — Tkinter Basics

**Phase:** 15 — GUI Applications | **Time:** ~35 min

---

## Part 1: What is Tkinter?

Tkinter is Python's **built-in** GUI library — no installation needed.

```python
import tkinter as tk          # core tkinter
from tkinter import ttk       # themed widgets (better looking)
from tkinter import messagebox, filedialog, simpledialog
```

---

## Part 2: Your First Window

```python
import tkinter as tk

# Create main window
root = tk.Tk()
root.title("My First GUI")
root.geometry("400x300")         # width x height
root.resizable(True, True)       # allow resize

# Add a label widget
label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16))
label.pack(pady=20)              # add to window with padding

# Add a button
button = tk.Button(root, text="Click Me", command=lambda: print("Clicked!"))
button.pack()

# Start the event loop (MUST be last line)
root.mainloop()
```

---

## Part 3: Core Widgets

```python
# Label — display text
tk.Label(parent, text="Hello", font=("Arial", 12), fg="blue")

# Button — trigger action
tk.Button(parent, text="Submit", command=callback, width=15)

# Entry — single line input
entry = tk.Entry(parent, width=30)
value = entry.get()             # read value
entry.delete(0, tk.END)         # clear
entry.insert(0, "default text") # set text

# Text — multi-line input
text = tk.Text(parent, height=5, width=40)
content = text.get("1.0", tk.END)   # read all
text.delete("1.0", tk.END)          # clear

# Listbox — scrollable list
listbox = tk.Listbox(parent, height=6)
listbox.insert(tk.END, "Item 1")
listbox.insert(tk.END, "Item 2")
selected = listbox.curselection()   # selected index(es)

# Checkbutton — checkbox
var = tk.BooleanVar()
tk.Checkbutton(parent, text="Enable", variable=var)
is_checked = var.get()

# Radiobutton — select one of many
choice = tk.StringVar(value="option1")
tk.Radiobutton(parent, text="Option 1", variable=choice, value="option1")
tk.Radiobutton(parent, text="Option 2", variable=choice, value="option2")
selected = choice.get()

# Combobox (ttk) — dropdown
from tkinter import ttk
combo = ttk.Combobox(parent, values=["Red", "Green", "Blue"])
combo.set("Red")    # default
combo.get()         # current value

# Scale — slider
scale = tk.Scale(parent, from_=0, to=100, orient=tk.HORIZONTAL)
value = scale.get()

# Spinbox — number selector
spin = ttk.Spinbox(parent, from_=0, to=10, width=5)
```

---

## Part 4: Layout Managers

### pack() — Simple stacking

```python
# Stacks vertically by default
widget.pack()
widget.pack(side=tk.LEFT)   # or TOP, RIGHT, BOTTOM
widget.pack(fill=tk.X)      # fill horizontal
widget.pack(fill=tk.BOTH, expand=True)  # fill all space
widget.pack(padx=10, pady=5)  # external padding
widget.pack(ipadx=5, ipady=5) # internal padding
```

### grid() — Row/column layout (most flexible)

```python
widget.grid(row=0, column=0)
widget.grid(row=0, column=1, columnspan=2)  # span 2 cols
widget.grid(row=1, column=0, sticky="ew")   # stretch E-W
widget.grid(padx=5, pady=5)

# Configure column weights (for resizing)
parent.columnconfigure(0, weight=1)
parent.rowconfigure(0, weight=1)
```

### place() — Absolute positioning

```python
widget.place(x=50, y=100)
widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # centered
```

---

## Part 5: Variables

Tkinter variables track widget values:

```python
str_var  = tk.StringVar(value="default")
int_var  = tk.IntVar(value=0)
double_var = tk.DoubleVar(value=0.0)
bool_var = tk.BooleanVar(value=False)

# Read
str_var.get()

# Write
str_var.set("new value")

# Trace — callback when value changes
str_var.trace_add("write", lambda *args: print("Changed!"))

# Link to widget
entry = tk.Entry(parent, textvariable=str_var)
```

---

## Part 6: OOP Pattern (Professional)

```python
import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("450x350")
        self._setup_variables()
        self._build_ui()

    def _setup_variables(self):
        self.name_var = tk.StringVar()
        self.age_var  = tk.IntVar(value=18)

    def _build_ui(self):
        # Frame groups related widgets
        frame = ttk.LabelFrame(self, text="User Info", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1)

        ttk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w")
        ttk.Spinbox(frame, from_=0, to=120,
                    textvariable=self.age_var, width=10).grid(row=1, column=1)

        ttk.Button(frame, text="Submit",
                   command=self._on_submit).grid(row=2, column=0, columnspan=2)

    def _on_submit(self):
        name = self.name_var.get().strip()
        age  = self.age_var.get()
        if not name:
            messagebox.showwarning("Error", "Name is required!")
            return
        messagebox.showinfo("Success", f"Hello, {name}! Age: {age}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
```

---

## Practice Exercises

1. Create a window with a label, entry, and button that shows an alert with the text you typed.

2. Add input validation: show an error if the entry is empty.

3. Create a window with a counter: two buttons (+ and -) and a label showing the current count.

---

## Next Lesson

**[Lesson 02 → Layout Managers](lesson-02-layout.md)**
