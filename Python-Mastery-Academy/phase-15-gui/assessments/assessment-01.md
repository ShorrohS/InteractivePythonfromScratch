# Phase 15 — Completion Assessment: GUI Applications

> Complete this before moving to Phase 16.
> **Pass mark: 80%** | **Time: 50 minutes**
>
> Build all four tasks as a **single Python file** — each task extends the previous one.
> Your submission is a complete, runnable tkinter application.

---

## Task 1 — Unit Converter (25 points)

Build a Unit Converter GUI app with the following widgets:

- An `OptionMenu` (or `ttk.Combobox`) to select the conversion type:
  - km → miles
  - miles → km
  - kg → lbs
  - lbs → kg
  - °C → °F
  - °F → °C
- An `Entry` field for the input value
- A `Convert` Button
- A `Label` that displays the result

**Required behaviour:**
- Clicking Convert reads the Entry, applies the selected conversion formula, and shows the result in the result Label.

**Conversion formulas:**
```
km  → miles : value × 0.621371
miles → km  : value × 1.60934
kg  → lbs   : value × 2.20462
lbs → kg    : value × 0.453592
°C  → °F    : (value × 9/5) + 32
°F  → °C    : (value − 32) × 5/9
```

---

## Task 2 — Input Validation (20 points)

Extend Task 1 to add input validation:

- If the Entry is empty or not a valid number, display an error message in **red** text below the Entry (not a messagebox).
- The red error message disappears automatically when the user starts typing a new value (bind `<KeyRelease>` to clear it).
- The result Label is only updated when the input is valid.

---

## Task 3 — Conversion History (35 points)

Extend Task 2 to add a History section below the converter:

- A `Label` heading: `Conversion History`
- A `Listbox` that records every successful conversion in this format:
  ```
  42 km → miles = 26.1
  ```
- A `Clear History` Button that empties the Listbox.
- A `Save History` Button that:
  - Opens `filedialog.asksaveasfilename` (default extension `.txt`, filtered to `.txt` and All files)
  - Writes each history entry on its own line to the chosen file
  - Shows a `messagebox.showinfo` confirming how many entries were saved

---

## Task 4 — Architecture Commentary (20 points)

Without changing how the app runs, add comments to your code that answer the following:

1. Which part of your code is the **Model** (data + business logic)?
2. Which part is the **View** (widgets, layout)?
3. Which part is the **Controller** (event handling, coordination)?
4. If you were to refactor this app into three separate classes, what would each class be called and what would it do?

Your comments should be meaningful sentences, not one-word labels.

---

## Scoring

| Score | Action |
|-------|--------|
| 80–100 | Move to Phase 16 |
| 65–79  | Review weak areas, then proceed |
| < 65   | Revisit Phase 15 lessons before continuing |

---

## Answer Key

> Complete working solution follows. Study this only after submitting your own attempt.

```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# ── Conversion formulas ──────────────────────────────────────────────────────
# MODEL: pure data — conversion names, units, and calculation functions.
# No tkinter here; these could live in a separate module.

CONVERSIONS = {
    "km → miles":  ("km",     "miles", lambda v: v * 0.621371),
    "miles → km":  ("miles",  "km",    lambda v: v * 1.60934),
    "kg → lbs":    ("kg",     "lbs",   lambda v: v * 2.20462),
    "lbs → kg":    ("lbs",    "kg",    lambda v: v * 0.453592),
    "°C → °F":     ("°C",     "°F",    lambda v: (v * 9 / 5) + 32),
    "°F → °C":     ("°F",     "°C",    lambda v: (v - 32) * 5 / 9),
}


class UnitConverterApp(tk.Tk):
    """
    VIEW + CONTROLLER combined in one class (common pattern for small apps).

    MODEL  : the CONVERSIONS dict above — pure data and logic.
    VIEW   : all widget creation in _build_converter() and _build_history().
    CONTROLLER: event methods _convert(), _clear_history(), _save_history().

    MVC REFACTOR NOTE (Task 4):
      To split into three classes you would create:
        - ConversionModel  : wraps CONVERSIONS and the history list;
                             exposes convert(key, value), get_history(), clear_history()
        - ConverterView    : all tk widget construction; exposes set_result(),
                             set_error(), get_input(), get_conversion_type(),
                             add_history_entry(), clear_history_display()
        - ConverterController: __init__ receives model + view; wires button
                             commands to model calls then updates the view.
    """

    def __init__(self):
        super().__init__()
        self.title("Unit Converter")
        self.geometry("420x480")
        self.resizable(False, False)
        self._history: list[str] = []   # MODEL: history data lives here
        self._build()

    # ── UI Construction (VIEW) ────────────────────────────────────────────

    def _build(self):
        self._build_converter()
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=10, pady=8)
        self._build_history()

    def _build_converter(self):
        frame = ttk.LabelFrame(self, text="Converter", padding=10)
        frame.pack(fill="x", padx=10, pady=(10, 0))

        # Conversion type selector
        ttk.Label(frame, text="Conversion:").grid(row=0, column=0, sticky="e", pady=4)
        self._conv_var = tk.StringVar(value=list(CONVERSIONS.keys())[0])
        ttk.OptionMenu(frame, self._conv_var, self._conv_var.get(),
                       *CONVERSIONS.keys()).grid(row=0, column=1, sticky="w", padx=8)

        # Input field
        ttk.Label(frame, text="Value:").grid(row=1, column=0, sticky="e", pady=4)
        self._input_var = tk.StringVar()
        self._entry = ttk.Entry(frame, textvariable=self._input_var, width=18)
        self._entry.grid(row=1, column=1, sticky="w", padx=8, pady=4)

        # Task 2: inline error label in red
        self._error_var = tk.StringVar()
        self._error_lbl = tk.Label(frame, textvariable=self._error_var,
                                   fg="red", font=("Arial", 9))
        self._error_lbl.grid(row=2, column=1, sticky="w", padx=8)

        # Clear error when user starts typing again
        self._input_var.trace_add("write", lambda *_: self._error_var.set(""))

        # Convert button
        ttk.Button(frame, text="Convert", command=self._convert).grid(
            row=3, column=0, columnspan=2, pady=8
        )

        # Result label
        self._result_var = tk.StringVar(value="—")
        tk.Label(frame, textvariable=self._result_var,
                 font=("Arial", 13, "bold")).grid(row=4, column=0, columnspan=2)

    def _build_history(self):
        frame = ttk.LabelFrame(self, text="Conversion History", padding=10)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Listbox + scrollbar
        list_frame = tk.Frame(frame)
        list_frame.pack(fill="both", expand=True)
        self._history_lb = tk.Listbox(list_frame, height=7)
        sb = ttk.Scrollbar(list_frame, command=self._history_lb.yview)
        self._history_lb.configure(yscrollcommand=sb.set)
        self._history_lb.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # History buttons
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=(6, 0))
        ttk.Button(btn_frame, text="Clear History",
                   command=self._clear_history).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Save History",
                   command=self._save_history).pack(side="left", padx=4)

    # ── Event Handlers (CONTROLLER) ───────────────────────────────────────

    def _convert(self):
        """Validate input, run conversion, update result and history."""
        raw = self._input_var.get().strip()

        # Task 2: validate input
        try:
            value = float(raw)
        except ValueError:
            self._error_var.set("Please enter a valid number.")
            self._result_var.set("—")
            return

        key = self._conv_var.get()
        from_unit, to_unit, formula = CONVERSIONS[key]
        result = formula(value)

        # Round to 4 significant figures for display
        self._result_var.set(f"{value} {from_unit} = {result:.4g} {to_unit}")

        # Task 3: record in history
        entry = f"{value} {from_unit} → {to_unit} = {result:.4g}"
        self._history.append(entry)
        self._history_lb.insert(tk.END, entry)

    def _clear_history(self):
        """Clear both the history list and the Listbox display."""
        self._history.clear()
        self._history_lb.delete(0, tk.END)

    def _save_history(self):
        """Write history entries to a user-chosen .txt file."""
        if not self._history:
            messagebox.showinfo("Nothing to save", "History is empty.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save History As",
        )
        if not path:
            return  # user cancelled

        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(self._history))

        messagebox.showinfo(
            "Saved", f"{len(self._history)} entries saved to:\n{path}"
        )


if __name__ == "__main__":
    UnitConverterApp().mainloop()
```

---

### Task scoring breakdown

| Task | Points | Key requirements |
|------|--------|-----------------|
| 1 | 25 | OptionMenu, Entry, Convert button, result Label, correct formulas |
| 2 | 20 | Red inline error label, clears on keystroke, no messagebox for errors |
| 3 | 35 | History Listbox, Clear button, Save with filedialog + showinfo confirmation |
| 4 | 20 | Comments identify Model/View/Controller sections and describe a 3-class refactor |
