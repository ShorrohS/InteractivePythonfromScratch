# Phase 15 — Quiz 01: GUI Applications with Tkinter

**Questions:** 18 | **Pass:** 14/18 | **Time:** 20 min (no notes)

---

## Section 1: Widgets (Q1–Q5)

**Q1.** Which widget do you use to display a single line of static text?
```
A) tk.Entry      B) tk.Label      C) tk.Text      D) tk.Frame
```

---

**Q2.** What does `textvariable=my_var` do on a Label?
```
A) Sets the label text once and ignores future changes
B) Links the label to a tk.StringVar so it updates automatically when the variable changes
C) Creates a new variable named my_var
D) Makes the label read-only
```

---

**Q3.** What is wrong with this code?
```python
entry = tk.Entry(root)
value = entry           # user has typed "Alice"
print(value)
```
```
A) entry is not a valid widget
B) value holds the Entry widget object, not the text — use entry.get()
C) print() cannot display Entry values
D) Nothing is wrong; this prints "Alice"
```

---

**Q4.** You want the user to choose one option from a group where only one can be selected at a time. Which widget pair is correct?
```
A) tk.Checkbutton sharing one BooleanVar
B) tk.Radiobutton sharing one StringVar, each with a different value=
C) tk.Listbox with selectmode="multiple"
D) tk.Entry with a dropdown
```

---

**Q5.** What does this code produce?
```python
lb = tk.Listbox(root, height=4)
for fruit in ["Apple", "Banana", "Cherry"]:
    lb.insert(tk.END, fruit)
lb.pack()
```
```
A) A Listbox that is empty because insert() needs an index, not tk.END
B) A Listbox with three fruit names listed vertically
C) A dropdown menu with three options
D) An error — tk.END is not valid for Listbox
```

---

## Section 2: Layout Managers (Q6–Q9)

**Q6.** What does `widget.pack(expand=True, fill="both")` do?
```
A) Creates the widget and makes it fill the entire screen
B) Stretches the widget to fill all available space as the window resizes
C) Removes the widget from the layout
D) Sets the widget's background colour to expand
```

---

**Q7.** You are placing a Label and an Entry side by side in the same row using grid. Which code is correct?
```python
# Option A
label.grid(row=0, column=0)
entry.grid(row=0, column=1)

# Option B
label.grid(row=0, column=0)
entry.pack(side="left")
```
```
A) Option A — grid widgets in the same parent must all use grid
B) Option B — you can mix grid and pack freely
C) Both are correct
D) Neither; you must use place for side-by-side layout
```

---

**Q8.** What does `sticky="ew"` mean in a grid call?
```
A) The widget sticks to the East and West walls, stretching it horizontally
B) The widget is hidden (invisible)
C) The widget floats to the top-right corner
D) It is an error — sticky only accepts "n", "s", "e", "w"
```

---

**Q9.** How do you make a column in a grid layout expand to fill extra horizontal space when the window is resized?
```
A) widget.grid(fill="x")
B) parent.columnconfigure(column_index, weight=1)
C) widget.pack(side="left", expand=True)
D) parent.grid_weights(column=1)
```

---

## Section 3: Event Handling (Q10–Q13)

**Q10.** What is the correct way to call `self.save` when a Button is clicked?
```python
# Option A
tk.Button(self, text="Save", command=self.save())

# Option B
tk.Button(self, text="Save", command=self.save)
```
```
A) Option A — the parentheses are required to tell tkinter which method to use
B) Option B — command= takes a reference; parentheses call the method immediately
C) Both are correct
D) Neither; use bind("<Button-1>", self.save) instead
```

---

**Q11.** You bind a key event with `entry.bind("<Return>", self.on_enter)`. The `on_enter` method signature should be:
```
A) def on_enter(self):
B) def on_enter(self, event):
C) def on_enter(event, self):
D) def on_enter():
```

---

**Q12.** What does this code print when the user types "Hi" and presses Enter?
```python
import tkinter as tk

root = tk.Tk()
var = tk.StringVar()
entry = tk.Entry(root, textvariable=var)
entry.pack()

def show(event):
    print(var.get())

entry.bind("<Return>", show)
root.mainloop()
```
```
A) Nothing — bind does not work with Entry widgets
B) The event object
C) "Hi"
D) An error — var.get() is not valid inside a callback
```

---

**Q13.** Which of these correctly creates a Button that passes an argument to its callback?
```python
colours = ["red", "blue", "green"]

# Option A — inside a loop
for c in colours:
    tk.Button(root, text=c, command=lambda: print(c)).pack()

# Option B — inside a loop
for c in colours:
    tk.Button(root, text=c, command=lambda col=c: print(col)).pack()
```
```
A) Option A — each button prints its own colour
B) Option B — the default argument col=c captures the current value of c
C) Both work identically
D) Neither; you must use functools.partial
```

---

## Section 4: ttk and Dialogs (Q14–Q16)

**Q14.** What is the main advantage of using `ttk` widgets over plain `tk` widgets?
```
A) ttk widgets are faster to create
B) ttk widgets automatically apply the operating system's native visual theme
C) ttk widgets support more event types
D) ttk widgets do not require mainloop()
```

---

**Q15.** What does `messagebox.askyesno("Exit", "Are you sure?")` return?
```
A) The string "yes" or "no"
B) True if the user clicked Yes, False if No
C) None — it only shows a message
D) An integer: 1 for Yes, 0 for No
```

---

**Q16.** Which dialog function opens a file-picker and returns the selected file path?
```
A) filedialog.asksaveasfilename()
B) messagebox.askopenfile()
C) filedialog.askopenfilename()
D) simpledialog.askfile()
```

---

## Section 5: App Architecture (Q17–Q18)

**Q17.** In the recommended OOP pattern, a tkinter app is built as `class App(tk.Tk)`. What does calling `super().__init__()` do in the constructor?
```
A) Creates a new child window
B) Calls tk.Tk.__init__(), initialising the root window so tkinter is fully set up
C) Starts the event loop
D) Imports tkinter automatically
```

---

**Q18.** In an MVC-structured tkinter app, which layer should handle reading from the database and applying business rules?
```
A) View — it owns all widgets, so it should also manage data
B) Controller — it is the coordinator
C) Model — it is the data and logic layer, independent of the UI
D) It does not matter which layer handles it
```

---

## Answers

.
.
.
.
.
.

| Q  | Answer | Explanation |
|----|--------|-------------|
|  1 | B | `tk.Label` displays static (or variable-linked) text |
|  2 | B | `textvariable=` binds the label to a `tk.StringVar`; changes to the var auto-update the label |
|  3 | B | `entry.get()` is required to read the text; without it you get the widget object |
|  4 | B | `Radiobutton` widgets share one `StringVar`; each has a unique `value=` |
|  5 | B | `tk.END` appends to the end of the list — three items are inserted correctly |
|  6 | B | `expand=True` + `fill="both"` makes the widget grow with the window |
|  7 | A | Widgets in the same container must all use the same layout manager |
|  8 | A | `sticky="ew"` stretches the widget East-to-West (full width of its cell) |
|  9 | B | `columnconfigure(index, weight=1)` tells the grid to give that column extra space |
| 10 | B | `command=self.save` is a reference; `self.save()` calls it immediately at build time |
| 11 | B | `bind()` always passes an event object as the first argument after `self` |
| 12 | C | `var.get()` reads the StringVar bound to the Entry, returning "Hi" |
| 13 | B | Default argument `col=c` captures the current loop value; Option A captures the final value of `c` only |
| 14 | B | `ttk` widgets follow the OS theme (Aqua on macOS, Aero on Windows, etc.) |
| 15 | B | `askyesno` returns a `bool`: `True` for Yes, `False` for No |
| 16 | C | `filedialog.askopenfilename()` opens a file browser and returns the chosen path |
| 17 | B | `super().__init__()` initialises `tk.Tk`, setting up the root window |
| 18 | C | The Model layer owns data access and business logic; it has no knowledge of the UI |
