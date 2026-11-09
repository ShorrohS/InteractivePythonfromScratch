# 📝 Phase 15 — Intermediate Exercises: GUI Applications

> Each task describes the required UI and behaviour. Write a **complete, runnable Python script**.
> Attempt all tasks before opening solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

## Q1 — BMI Calculator

**Goal:** Build a Body Mass Index calculator with colour-coded output.

**Required widgets:**
- `Label` + `Entry` for weight in kilograms
- `Label` + `Entry` for height in metres
- A `Calculate BMI` Button
- A result `Label` that shows the BMI value and category

**Required behaviour:**
- On Calculate: compute `BMI = weight / height²` and display it rounded to 1 decimal place.
- Colour the result label based on BMI category:
  - `< 18.5` → **Underweight** → blue text
  - `18.5–24.9` → **Normal** → green text
  - `25–29.9` → **Overweight** → orange text
  - `≥ 30` → **Obese** → red text
- If either field is empty or non-numeric, show a `messagebox.showerror`.

**Example result label text:** `BMI: 22.4 — Normal`

---

## Q2 — To-Do List

**Goal:** Build a functional to-do list app.

**Required widgets:**
- An `Entry` field for typing a new task
- An `Add Task` Button
- A `Listbox` displaying all current tasks
- A `Delete Selected` Button

**Required behaviour:**
- **Add Task:** appends the Entry text to the Listbox and clears the Entry. Does nothing if the Entry is empty.
- **Delete Selected:** removes the currently highlighted Listbox item. Does nothing if no item is selected.

**Expected window appearance:**
```
┌──────────────────────────────────┐
│  [____________________________]  │  ← Entry
│  [Add Task]   [Delete Selected]  │  ← Buttons
│  ┌────────────────────────────┐  │
│  │ Buy groceries              │  │
│  │ Write report               │  │  ← Listbox
│  └────────────────────────────┘  │
└──────────────────────────────────┘
```

---

## Q3 — Background Colour Picker

**Goal:** Let the user change the window background colour using Radiobuttons.

**Required widgets:**
- A `Label` saying `Choose a background colour:`
- Five `Radiobutton` widgets sharing one `tk.StringVar`, one for each colour: Red, Blue, Green, Yellow, White

**Required behaviour:**
- When a Radiobutton is selected the window background immediately changes to that colour — no extra button needed.
- The window should start with White selected and a white background.

**Hint:** `self.configure(bg=colour)` changes the window background colour.

---

## Q4 — Validated Registration Form

**Goal:** Build a form that enforces input rules before accepting submission.

**Required fields and rules:**
- **Name** — must not be empty
- **Email** — must contain exactly one `@` character
- **Age** — must be an integer between 1 and 120 inclusive

**Required widgets per field:** a field-name `Label`, an `Entry`, and an error `Label` that shows validation feedback in red.

**Required behaviour:**
- A `Submit` Button runs all three validations when clicked.
- Each failing field shows a specific error message in red (e.g. `Name is required`, `Invalid email address`, `Age must be 1–120`).
- Passing fields have their error label cleared.
- When ALL three fields pass, a `messagebox.showinfo` appears: `Form submitted successfully!`

---

## Q5 — File Reader

**Goal:** Build a text file viewer using a file-open dialog.

**Required widgets:**
- A `Browse…` Button
- A `Label` showing the path of the selected file (default text: `No file selected`)
- A `Text` widget with a vertical `Scrollbar` for displaying file contents

**Required behaviour:**
- Clicking Browse opens `filedialog.askopenfilename` filtered to `.txt` files (plus All files).
- After a file is chosen its full path appears in the Label and its contents fill the Text widget.
- The Text widget must be read-only (users cannot type into it).

**Hint:** To write to a read-only Text widget: set `state="normal"`, insert text, then set `state="disabled"`.

---

## Q6 — Number Guessing Game

**Goal:** Build a complete single-player number guessing game.

**Required behaviour:**
- On launch a random integer 1–100 is chosen (`random.randint`).
- The player types a guess in an `Entry` and clicks `Guess`.
- A feedback `Label` shows `Too low!`, `Too high!`, or `Correct! You guessed it in N tries.`
- A tries counter `Label` tracks the number of attempts.
- When the correct number is guessed the Entry and Guess button are disabled.
- A `New Game` Button resets everything: new random number, cleared Entry, zeroed counter, cleared feedback.

**Required widgets:**
- Title/instructions `Label`
- `Entry` for the guess
- `Guess` and `New Game` Buttons
- Feedback `Label`
- Tries counter `Label`

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
