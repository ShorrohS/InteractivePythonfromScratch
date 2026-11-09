"""
Debugging Challenge 01 — Phase 15: GUI Applications
====================================================

INSTRUCTIONS:
  This file contains 7 bugs inside a small tkinter BMI Calculator app.
  Find and fix every bug.

  When all bugs are fixed the app should:
    1. Open a window titled "BMI Calculator"
    2. Accept weight (kg) and height (m) in Entry fields
    3. Show the calculated BMI in the result label when Calculate is clicked
    4. Show a messagebox.showerror for invalid (non-numeric) input

  BUG TYPES hidden below:
    - Forgetting to call mainloop()
    - Using a positional argument where a keyword argument is required
    - Mixing pack() and grid() on the same parent container
    - Forgetting .get() when reading an Entry value
    - Lambda capturing a loop variable by reference instead of by value
    - Not converting an Entry string to float before arithmetic
    - Passing command=self.method() (immediate call) instead of command=self.method

  Strategy: fix one bug at a time, then read the code again.
  DO NOT scroll to the ANSWERS section until you have tried!
"""

import tkinter as tk
from tkinter import messagebox


class BMIApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("BMI Calculator")
        self.geometry("340x260")
        self._build()

    def _build(self):
        # BUG 1: tk.Label() requires a keyword argument text=, not a positional one
        lbl_w = tk.Label(self, "Weight (kg):")          # hint: tk.Label(parent, text="...")
        lbl_w.grid(row=0, column=0, padx=12, pady=8, sticky="e")

        self._weight = tk.Entry(self, width=14)
        self._weight.grid(row=0, column=1, padx=12, pady=8)

        lbl_h = tk.Label(self, text="Height (m):")
        lbl_h.grid(row=1, column=0, padx=12, pady=8, sticky="e")

        self._height = tk.Entry(self, width=14)
        self._height.grid(row=1, column=1, padx=12, pady=8)

        # BUG 2: command= receives the return value of _calculate() instead of the method itself
        btn = tk.Button(
            self, text="Calculate BMI",
            command=self._calculate()        # hint: remove the () to pass a reference
        )
        btn.grid(row=2, column=0, columnspan=2, pady=8)

        self._result_var = tk.StringVar(value="Enter values above")
        result_lbl = tk.Label(
            self, textvariable=self._result_var, font=("Arial", 11, "bold")
        )
        result_lbl.grid(row=3, column=0, columnspan=2, pady=4)

        # BUG 3: result_lbl already uses grid() above; calling pack() on the same widget
        #        in the same parent mixes two layout managers — this will raise a TclError
        result_lbl.pack()                    # hint: delete this line

        # BUG 4 (conceptual — lambda loop capture):
        # The four buttons below should each print their own category name when clicked.
        # As written, every button will print the LAST value of `cat` ("Obese"),
        # because the lambda captures the variable by reference, not by value.
        categories = ["Underweight", "Normal", "Overweight", "Obese"]
        for i, cat in enumerate(categories):
            tk.Button(
                self,
                text=cat,
                command=lambda: print(cat),  # hint: lambda cat=cat: print(cat)
            ).grid(row=4 + i, column=0, columnspan=2, sticky="w", padx=50, pady=2)

    def _calculate(self):
        # BUG 5: weight_raw holds the Entry widget object, not its text value
        weight_raw = self._weight            # hint: call .get() on the Entry widget

        height_raw = self._height.get()

        try:
            # BUG 6: weight_raw is still a string (or widget) here — must convert to float
            weight = weight_raw              # hint: float(weight_raw)
            height = float(height_raw)
            if height <= 0:
                raise ValueError("Height must be positive.")
            bmi = weight / (height ** 2)    # raises TypeError if weight is not a number
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Please enter valid numeric values.")
            return

        self._result_var.set(f"BMI: {bmi:.1f}")


if __name__ == "__main__":
    app = BMIApp()
    # BUG 7: mainloop() is never called — the window appears briefly then exits
    # hint: add app.mainloop() on the next line


# =====================================================================
# ANSWERS  (do not scroll until you have tried!)
# =====================================================================
#
# BUG 1  lbl_w = tk.Label(self, "Weight (kg):")
#        FIX:  tk.Label(self, text="Weight (kg):")
#              tk.Label's second positional arg is the parent, not the text.
#              All other options must be keyword arguments.
#
# BUG 2  command=self._calculate()
#        FIX:  command=self._calculate
#              Adding () calls the method immediately at widget-creation time.
#              Without (), tkinter receives a callable reference and calls it later.
#
# BUG 3  result_lbl.pack()  (line after result_lbl.grid(...))
#        FIX:  delete result_lbl.pack()
#              A widget (and all siblings in the same parent) must use only one
#              layout manager.  Mixing grid and pack raises a TclError.
#
# BUG 4  command=lambda: print(cat)  (inside the for-loop)
#        FIX:  command=lambda cat=cat: print(cat)
#              Without a default argument, the lambda looks up `cat` at call time,
#              not at definition time.  By the time any button is clicked the loop
#              has finished, so `cat` is "Obese" for every button.
#
# BUG 5  weight_raw = self._weight
#        FIX:  weight_raw = self._weight.get()
#              Entry.get() returns the current text as a string.
#              Without .get() you have the widget object, not its text.
#
# BUG 6  weight = weight_raw
#        FIX:  weight = float(weight_raw)
#              Entry.get() always returns a str.  Division requires a number.
#
# BUG 7  (missing line at the bottom)
#        FIX:  app.mainloop()
#              Without mainloop() the window is created then the script exits
#              immediately.  mainloop() starts the tkinter event loop.
#
# =====================================================================
