# 📝 Phase 15 — Beginner Exercises: GUI Applications

> Each task describes the required UI and behaviour. Write a **complete, runnable Python script**.
> There is no stdin/stdout matching — the goal is a working tkinter window.
> Attempt all tasks before opening solutions.
> Solutions: `../../solutions/beginner/solutions.md`

---

## Q1 — Hello Tkinter

**Goal:** Create a window titled `My First App` sized 400×200 pixels.

**Required widgets:**
- A `Label` displayed in the centre of the window showing the text `Hello, Tkinter!`
- A `Button` labelled `Click Me`

**Required behaviour:**
- When the Button is clicked the Label's text changes to `Button clicked!`

**Expected window appearance:**
```
┌────────────────────────────────┐  ← title bar: My First App
│                                │
│        Hello, Tkinter!         │  ← Label (centred)
│                                │
│           [Click Me]           │  ← Button
└────────────────────────────────┘
      400 px wide × 200 px tall
```

**Hints:**
- Use `tk.StringVar` and `textvariable=` on the Label so the text updates automatically.
- `label.pack(expand=True)` centres the label vertically.
- Pass the callback to `command=` on the Button (no parentheses).

---

## Q2 — Greeting Popup

**Goal:** Create a name-greeting app with a messagebox response.

**Required widgets:**
- A `Label` saying `Enter your name:`
- An `Entry` field for the user to type their name
- A `Button` labelled `Greet`

**Required behaviour:**
- When Greet is clicked, a `messagebox.showinfo` popup appears with the title `Hello!` and the message `Hello, [name]! Welcome to Tkinter.` where `[name]` is whatever was typed in the Entry.
- If the Entry is empty, a `messagebox.showwarning` shows instead with the message `Please enter a name.`

**Expected window appearance:**
```
┌──────────────────────────────┐
│  Enter your name:            │
│  [__________________________]│  ← Entry field
│  [          Greet           ]│  ← Button
└──────────────────────────────┘
```

**Hints:**
- Use `.get()` to read the Entry's current text.
- `.strip()` the value before checking if it is empty.

---

## Q3 — User Details Form

**Goal:** Build a three-field data-entry form using the `grid` layout manager.

**Required widgets:**
- Three `Label` + `Entry` pairs in a grid:
  - Row 0: `Name`
  - Row 1: `Email`
  - Row 2: `Age`
- A `Print Details` Button below all three rows

**Required behaviour:**
- When Print Details is clicked, each field value is printed to the console in this format:
  ```
  Name:  Alice
  Email: alice@example.com
  Age:   30
  ```

**Expected window appearance:**
```
┌──────────────────────────────────┐
│  Name:   [____________________]  │
│  Email:  [____________________]  │
│  Age:    [____________________]  │
│                                  │
│          [Print Details]         │
└──────────────────────────────────┘
```

**Hints:**
- `label.grid(row=r, column=0, sticky="e")` right-aligns the labels.
- `entry.grid(row=r, column=1)` places entries in the second column.
- `button.grid(columnspan=2)` spans the button across both columns.

---

## Q4 — Fruit Selector

**Goal:** Build a window with a Listbox and a selection button.

**Required widgets:**
- A `Label` saying `Select a fruit:`
- A `Listbox` containing exactly these 5 items in order: Apple, Banana, Cherry, Mango, Orange
- A `Button` labelled `Show Selection`

**Required behaviour:**
- When Show Selection is clicked, the currently selected fruit name is printed to the console.
- If no item is selected, print `No fruit selected.`

**Expected window appearance:**
```
┌──────────────────────────────┐
│  Select a fruit:             │
│  ┌────────────────────────┐  │
│  │ Apple                  │  │
│  │ Banana                 │  │
│  │ Cherry                 │  │
│  │ Mango                  │  │
│  │ Orange                 │  │
│  └────────────────────────┘  │
│        [Show Selection]      │
└──────────────────────────────┘
```

**Hints:**
- Insert items with `listbox.insert(tk.END, item)`.
- Read the selection with `listbox.curselection()` — it returns a tuple of integer indices.
- Retrieve the text with `listbox.get(index)`.

---

## Q5 — Multi-line Text Pad

**Goal:** Build a simple text area with a clear button.

**Required widgets:**
- A `Text` widget that is 40 characters wide and 10 lines tall
- A `Clear Text` Button below it

**Required behaviour:**
- The Text widget accepts free-form typing.
- When Clear Text is clicked, every character in the Text widget is removed.

**Expected window appearance:**
```
┌────────────────────────────────────────┐
│ ┌──────────────────────────────────┐   │
│ │                                  │   │
│ │          (typing area)           │   │  ← Text widget, 10 rows tall
│ │                                  │   │
│ └──────────────────────────────────┘   │
│              [Clear Text]              │
└────────────────────────────────────────┘
```

**Hints:**
- Delete all text with `text_widget.delete("1.0", tk.END)`.
- `"1.0"` means line 1, character 0 — the very start of the widget.

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
