# 📝 Phase 15 — Advanced Exercises: GUI Applications

> These require multi-widget coordination, architectural decisions, and complete apps.
> Write a **complete, runnable Python script** for each task.
> Solutions: `../../solutions/advanced/solutions.md`

---

## Q1 — Contact Manager

**Goal:** Build a contact-book app with full CRUD operations.

**Required widgets:**
- A `ttk.Treeview` with three columns: Name, Phone, Email
- `Add`, `Edit`, and `Delete` Buttons

**Required behaviour:**
- **Add:** Opens a `tk.Toplevel` modal dialog with Entry fields for Name, Phone, Email, and OK/Cancel buttons. On OK, validates that Name is not empty and inserts the new contact into the Treeview.
- **Edit:** Opens the same dialog pre-filled with the selected row's values. On OK, updates the Treeview row.
- **Delete:** Asks `messagebox.askyesno` for confirmation, then removes the selected row.
- If no row is selected when Edit or Delete is clicked, show a `messagebox.showwarning`.

**Data storage:** Keep contacts in a Python list of dicts `[{"name": ..., "phone": ..., "email": ...}]` and keep the Treeview in sync with it.

---

## Q2 — Multi-Tab Profile App

**Goal:** Build a three-tab application using `ttk.Notebook`.

**Tab 1 — Profile:**
- Entry fields for First Name, Last Name, and Email
- A `Save Profile` Button that stores the values and shows a `messagebox.showinfo` confirmation

**Tab 2 — Settings:**
- A `Checkbutton` for "Enable notifications"
- Three `Radiobutton`s for theme: Light, Dark, System
- A `Save Settings` Button that prints the current settings to the console

**Tab 3 — About:**
- A `Label` with multi-line app info (name, version, author)
- A `ttk.Separator`
- A clickable `Label` styled like a hyperlink (blue, underlined, `cursor="hand2"`) that opens a URL using `webbrowser.open`

**Required:** All three tabs must be visible as named tabs at the top of the `Notebook` widget.

---

## Q3 — Canvas Drawing App

**Goal:** Build an interactive drawing tool using `tk.Canvas`.

**Required behaviour:**
- Left-clicking on the canvas draws a filled circle (radius 15) at the click position.
- Right-clicking draws a filled square (30×30) centred at the click position.
- Each shape is filled with a random colour chosen from a predefined list of at least 6 colours.
- A `Clear Canvas` Button removes all drawn shapes and resets the counters.
- A status `Label` shows: `Circles: N | Squares: M`

**Required widgets:**
- A `tk.Canvas` of at least 500×400 pixels
- A `Clear Canvas` Button
- A status `Label`

**Hint:** Bind `<Button-1>` for left-click and `<Button-3>` for right-click to the Canvas widget.

---

## Q4 — Stopwatch

**Goal:** Build a precision stopwatch using `after()` for real-time updates.

**Required widgets:**
- A large display `Label` showing elapsed time as `MM:SS.t` (minutes, seconds, tenths)
- `Start`, `Stop`, and `Reset` Buttons

**Required behaviour:**
- **Start:** begins ticking — updates the Label every 100 ms using `self.after(100, self._tick)`.
- **Stop:** pauses the timer without resetting it.
- **Reset:** stops and resets the display to `00:00.0`.
- Starting after a Stop resumes from the paused time, not from zero.
- Buttons enable/disable appropriately: Start is disabled while running; Stop is disabled while paused.

**Hint:** Store elapsed time as an integer count of 100 ms ticks. For formatting: `ticks // 100 // 60` gives minutes, `(ticks // 100) % 60` gives seconds, `ticks % 10` gives the tenths digit.

---

## Q5 — MVC Contact App

**Goal:** Implement a simple contact list using a strict Model-View-Controller architecture split across three distinct classes.

**Model (`ContactModel`):**
- Stores a list of contact dicts in memory.
- Methods: `add_contact(name, phone)`, `delete_contact(index)`, `get_all()`.
- Must contain **no tkinter imports**.

**View (`ContactView(tk.Frame)`):**
- Builds the entire UI: a `Listbox`, an input row with two `Entry` widgets and an Add Button, and a Delete Selected Button.
- Exposes a public interface for the Controller: `set_contacts(items)`, `get_name()`, `get_phone()`, `clear_inputs()`, `get_selection()`.
- Contains **no business logic** and makes **no direct calls to the Model**.

**Controller (`ContactController`):**
- Receives a Model and a View in `__init__`.
- Wires the View's button commands to Model methods and then calls View update methods.
- Owns all coordination logic.

**Required:** Comment each class with its layer name (MODEL / VIEW / CONTROLLER) and a one-sentence description of its responsibility.

---

## Q6 — CSV Viewer

**Goal:** Build a spreadsheet-style CSV viewer with sortable columns.

**Required behaviour:**
- A `Load CSV…` Button opens `filedialog.askopenfilename` filtered to `.csv` files.
- The chosen file is read with the `csv` module; the first row becomes column headers.
- A `ttk.Treeview` is built dynamically with one column per header.
- All data rows are inserted into the Treeview.
- Clicking a column heading sorts all rows by that column — first click ascending, second click on the same heading descending (toggle).
- Vertical and horizontal `Scrollbar`s allow navigating large files.
- A status `Label` shows: `Loaded: filename.csv | Rows: N | Columns: M`

**Hint:** Store all data in a list of tuples. When a heading is clicked, sort the list and reload the Treeview. Try sorting numerically when the column values look like numbers, and alphabetically otherwise.

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
