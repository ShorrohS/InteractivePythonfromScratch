# Lesson 01 — Introduction to GUI Programming and Tkinter

**Phase:** 15 — GUI Applications | **Time:** ~30 min

---

## Part 1: What is GUI Programming?

A **Graphical User Interface (GUI)** lets users interact with software using visual elements — buttons, text boxes, menus, and windows — instead of typing commands in a terminal.

**Examples you use every day:** file explorer, calculator app, text editor, web browser.

**Why desktop apps still matter:**
- Internal business tools do not need a web server
- Offline applications that work without an internet connection
- Quick utilities for analysts, admins, and developers
- Learning fundamental event-driven programming patterns

---

## Part 2: Why Tkinter?

Tkinter is Python's **built-in** GUI library — it ships with every standard Python installation.

| Feature | Tkinter | PyQt | wxPython |
|---------|---------|------|---------|
| Installation | None needed | pip install | pip install |
| Cross-platform | ✅ Yes | ✅ Yes | ✅ Yes |
| Learning curve | Low | High | Medium |
| Best for | Learning, utilities | Full apps | Native look |

For learning and building utility tools, tkinter is the right choice: zero setup, works everywhere, and the skills transfer directly to larger frameworks.

```python
import tkinter as tk           # the core module
from tkinter import ttk        # themed widget set (modern look)
from tkinter import messagebox # dialog boxes
```

---

## Part 3: Creating Your First Window

The main window is created with `tk.Tk()`. It is the root of your entire GUI.

```python
import tkinter as tk

# Step 1: Create the root window
root = tk.Tk()

# Step 2: Set the window title (shown in the title bar)
root.title("My First App")

# Step 3: Set the window size — "widthxheight" in pixels
root.geometry("400x300")

# Step 4: Control whether the user can resize the window
root.resizable(True, True)   # (allow_horizontal, allow_vertical)

# Step 5: Start the event loop (this line BLOCKS — put it last)
root.mainloop()
```

Running this gives you a blank 400×300 window. Try changing the numbers in `geometry()` to see the effect.

---

## Part 4: The Event Loop

`mainloop()` is what makes your window stay open and respond to user actions.

**Analogy:** Think of `mainloop()` as a receptionist sitting at a desk, waiting for visitors (events). When someone clicks a button, types a key, or moves the mouse, the receptionist handles the request and goes back to waiting. Without the receptionist at the desk, the office (your window) closes immediately.

```python
root.mainloop()   # NEVER forget this — the window disappears instantly without it
```

What `mainloop()` actually does:
1. Keeps the window visible on screen
2. Listens for user events (clicks, key presses, mouse moves)
3. Dispatches events to the right callback functions
4. Runs until the window is closed

---

## Part 5: Adding a Label Widget

A window with nothing in it is not very useful. A `Label` is the simplest widget — it displays text.

```python
import tkinter as tk

root = tk.Tk()
root.title("Hello App")
root.geometry("400x200")

# Create a label and attach it to the root window
label = tk.Label(
    root,                      # parent widget (the window)
    text="Hello, World!",      # text to display
    font=("Arial", 20),        # font family and size
    fg="navy"                  # foreground (text) color
)

# Add the label to the window layout
label.pack(pady=40)            # pack() places it; pady adds vertical space

root.mainloop()
```

---

## Part 6: Minimal Hello World GUI

Here is the complete, minimal Hello World GUI — every line explained:

```python
import tkinter as tk          # import the tkinter module

# Create the main window
root = tk.Tk()
root.title("Hello, World!")   # text in the title bar
root.geometry("300x150")      # 300 pixels wide, 150 pixels tall

# Create a Label widget
hello_label = tk.Label(
    root,
    text="Hello, World!",
    font=("Helvetica", 16, "bold")
)
hello_label.pack(expand=True)  # center vertically with expand=True

# Start the event loop — THIS MUST BE THE LAST LINE
root.mainloop()
```

Save this as `hello_gui.py` and run it with `python hello_gui.py`. You should see a small window with "Hello, World!" centered inside.

---

## Part 7: Common Beginner Mistakes

### Mistake 1: Forgetting mainloop()

```python
# WRONG — window appears and immediately vanishes
root = tk.Tk()
label = tk.Label(root, text="Hello")
label.pack()
# (no mainloop — program ends instantly)

# CORRECT
root = tk.Tk()
label = tk.Label(root, text="Hello")
label.pack()
root.mainloop()   # keeps the window open
```

### Mistake 2: Wrong import path

```python
# WRONG — these are outdated or cause name conflicts
import Tkinter        # Python 2 name — does not work in Python 3
from tkinter import * # imports everything, pollutes the namespace

# CORRECT — explicit imports
import tkinter as tk
from tkinter import ttk, messagebox
```

### Mistake 3: Calling mainloop() too early

```python
# WRONG — widgets created after mainloop() never appear
root = tk.Tk()
root.mainloop()                           # blocks here
label = tk.Label(root, text="Never seen") # never reached
label.pack()

# CORRECT — build all widgets first, then start the loop
root = tk.Tk()
label = tk.Label(root, text="This appears")
label.pack()
root.mainloop()   # last line
```

---

## Practice Exercises

1. Create a window titled "My Profile" with a size of 350×200 that displays your name in a label using an 18pt font.

2. Change the background color of the window by calling `root.configure(bg="lightblue")` before `mainloop()`. Try a few different colors.

3. Add two labels to the same window: one for your name and one for your city. Run the program and observe how `pack()` stacks them vertically by default.

4. Try removing `root.mainloop()` and run the program. Describe what happens.

---

## Summary

| Concept | Code |
|---------|------|
| Create window | `root = tk.Tk()` |
| Set title | `root.title("name")` |
| Set size | `root.geometry("WxH")` |
| Control resize | `root.resizable(w, h)` |
| Add a label | `tk.Label(root, text="...")` |
| Display a widget | `.pack()` |
| Start event loop | `root.mainloop()` |

---

## Next Lesson

**[Lesson 02 → Widgets](lesson-02-widgets.md)**
