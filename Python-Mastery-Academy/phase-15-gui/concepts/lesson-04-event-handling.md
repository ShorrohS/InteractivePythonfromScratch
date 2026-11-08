# Lesson 04 — Event Handling and Callbacks

**Phase:** 15 — GUI Applications | **Time:** ~35 min

---

## Part 1: What is an Event?

Every time a user interacts with a GUI — clicks a button, types a key, moves the mouse — Tkinter generates an **event**. Your job is to connect those events to **callback** functions that respond to them.

**Analogy:** Events are like a doorbell. You do not stand at the door and keep checking — you register a callback ("open the door when the bell rings"), then go about your work. When the bell rings, your callback runs automatically.

```
User action → Tkinter detects event → Calls your callback function → Updates UI
```

---

## Part 2: command= on Button

The simplest event connection is the `command=` option on a `Button`. It calls a function when the user clicks.

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x150")

def handle_click():
    print("Button was clicked!")
    status_label.config(text="Clicked!")

status_label = ttk.Label(root, text="Waiting...")
status_label.pack(pady=10)

ttk.Button(root, text="Click Me", command=handle_click).pack()

root.mainloop()
```

**Common mistake:** `command=handle_click` is correct (pass the function).  
`command=handle_click()` is wrong — it calls the function immediately at widget creation time and passes its return value (`None`) as the command.

---

## Part 3: bind() for Keyboard and Mouse Events

`bind(event_string, callback)` wires any event to any widget. The callback receives an `event` object automatically.

```python
root = tk.Tk()
root.geometry("350x250")

label = ttk.Label(root, text="Interact with the window")
label.pack(pady=20)

# Left mouse click
def on_left_click(event):
    label.config(text=f"Left click at ({event.x}, {event.y})")

# Double-click
def on_double_click(event):
    label.config(text="Double-clicked!")

# Any key press
def on_key(event):
    label.config(text=f"Key pressed: {event.keysym}")

# Enter key specifically
def on_return(event):
    label.config(text="Enter was pressed!")

root.bind("<Button-1>",        on_left_click)
root.bind("<Double-Button-1>", on_double_click)
root.bind("<Button-3>",        lambda e: label.config(text="Right click"))
root.bind("<Key>",             on_key)
root.bind("<Return>",          on_return)

# Focus events on an Entry
entry = ttk.Entry(root, width=20)
entry.pack(pady=10)
entry.bind("<FocusIn>",  lambda e: print("Entry focused"))
entry.bind("<FocusOut>", lambda e: print("Entry lost focus"))

root.mainloop()
```

### Common event strings

| String | Triggered by |
|--------|-------------|
| `<Button-1>` | Left mouse click |
| `<Button-3>` | Right mouse click |
| `<Double-Button-1>` | Double left click |
| `<Motion>` | Mouse moved |
| `<Key>` | Any key pressed |
| `<Return>` | Enter key |
| `<Escape>` | Escape key |
| `<FocusIn>` | Widget gains keyboard focus |
| `<FocusOut>` | Widget loses keyboard focus |
| `<<ListboxSelect>>` | Listbox item selected |

---

## Part 4: The Event Object

Callback functions registered with `bind()` receive an `event` object with useful attributes.

```python
def inspect_event(event):
    print(f"Widget:  {event.widget}")          # which widget fired the event
    print(f"Type:    {event.type}")            # ButtonPress, KeyPress, etc.
    print(f"X, Y:   {event.x}, {event.y}")    # mouse coordinates (widget-relative)
    print(f"X root: {event.x_root}, {event.y_root}")  # screen coordinates
    print(f"Key:    {event.keysym}")           # key symbol for keyboard events
    print(f"Char:   {event.char}")             # character typed (keyboard events)

root.bind("<Key>", inspect_event)
```

Note: `command=` callbacks receive **no** event object. `bind()` callbacks always receive one. If you use `bind()` but do not need the event, accept it anyway to avoid a `TypeError`:

```python
entry.bind("<Return>", lambda event: submit())   # event received, not used
```

---

## Part 5: Passing Arguments with lambda

`command=` only accepts a zero-argument callable. Use `lambda` to pass arguments.

```python
def set_bg_color(color: str):
    root.configure(bg=color)

# WRONG — calls set_bg_color("red") immediately at creation time
# ttk.Button(root, text="Red", command=set_bg_color("red"))

# CORRECT — lambda delays the call until the button is clicked
ttk.Button(root, text="Red",   command=lambda: set_bg_color("red")).pack(side="left", padx=5)
ttk.Button(root, text="Green", command=lambda: set_bg_color("green")).pack(side="left", padx=5)
ttk.Button(root, text="Blue",  command=lambda: set_bg_color("blue")).pack(side="left", padx=5)
```

### Loop pitfall — late binding

```python
# BUG: all three buttons print 2 because i is evaluated at call time
for i in range(3):
    ttk.Button(root, text=str(i), command=lambda: print(i)).pack()

# FIX: capture the current value of i with a default argument
for i in range(3):
    ttk.Button(root, text=str(i), command=lambda n=i: print(n)).pack()
```

---

## Part 6: Reactive UI with StringVar and trace()

`StringVar`, `IntVar`, `BooleanVar`, and `DoubleVar` are special variables that notify you when their value changes — no button required.

```python
root = tk.Tk()
root.geometry("350x150")
root.title("Reactive Label")

choice_var = tk.StringVar(value="option1")

def on_change(*args):
    print(f"Value changed to: {choice_var.get()}")

# trace_add fires the callback on every write to the variable
choice_var.trace_add("write", on_change)

for label, value in [("Option A", "option1"), ("Option B", "option2"), ("Option C", "option3")]:
    ttk.Radiobutton(root, text=label, variable=choice_var, value=value).pack(anchor="w", padx=20)

root.mainloop()
```

---

## Part 7: Complete Example — Live Character Counter

A counter label that updates on every keystroke — no button needed.

```python
import tkinter as tk
from tkinter import ttk

class CharacterCounterApp(tk.Tk):
    """Demonstrates reactive UI using StringVar and trace."""

    LIMIT = 50

    def __init__(self):
        super().__init__()
        self.title("Character Counter")
        self.geometry("400x180")
        self.resizable(False, False)

        self.text_var = tk.StringVar()
        self.text_var.trace_add("write", self._update_counter)
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Enter text below:").pack(pady=(20, 5))

        self.entry = ttk.Entry(self, textvariable=self.text_var, width=40)
        self.entry.pack(pady=5)
        self.entry.focus()   # cursor lands here when the app opens

        self.counter_label = ttk.Label(
            self,
            text=f"0 / {self.LIMIT} characters",
            font=("Arial", 11)
        )
        self.counter_label.pack(pady=8)

        ttk.Button(self, text="Clear", command=self._clear).pack()

    def _update_counter(self, *args):
        count = len(self.text_var.get())
        color = "red" if count > self.LIMIT else "black"
        self.counter_label.config(
            text=f"{count} / {self.LIMIT} characters",
            foreground=color
        )

    def _clear(self):
        self.text_var.set("")
        self.entry.focus()


if __name__ == "__main__":
    app = CharacterCounterApp()
    app.mainloop()
```

Every keystroke triggers `_update_counter` through the StringVar trace — this is reactive UI: the display stays in sync with the data automatically.

---

## Practice Exercises

1. Create a window with a Button that changes its own text to "Clicked!" after being pressed once, then to "Clicked again!" on the second press. Use `command=`.

2. Bind `<Motion>` to the root window and display the current mouse (x, y) coordinates in a Label, updating in real time as the mouse moves.

3. Add a StringVar-backed Entry and a Label that shows "Valid" when the text is a number and "Invalid" otherwise (use a try/except around `int()` inside the trace callback).

4. Create three Buttons ("Small", "Medium", "Large") that change the font size of a Label to 10, 14, and 20 respectively, using `lambda` to pass the size argument to a shared handler.

---

## Next Lesson

**[Lesson 05 → Building a Complete GUI Application](lesson-05-complete-gui-app.md)**
