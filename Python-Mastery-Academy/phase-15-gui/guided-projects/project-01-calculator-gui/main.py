"""
Project 01 - GUI Calculator
Phase 15: GUI Applications

SKILLS PRACTICED:
  - Tkinter widgets (Button, Label, Entry)
  - Grid layout manager
  - Event handling (button clicks)
  - StringVar for reactive display
  - eval() for safe-ish calculation

HOW TO RUN:
  python main.py
"""

import tkinter as tk
from tkinter import ttk
import math


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Calculator")
        self.geometry("320x480")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        self._expression = ""
        self._display_var = tk.StringVar(value="0")
        self._history: list[str] = []

        self._build_ui()
        self.bind("<Key>", self._key_press)

    def _build_ui(self):
        # Display
        display_frame = tk.Frame(self, bg="#1e1e2e", pady=10)
        display_frame.pack(fill=tk.X, padx=10)

        # History label
        self._history_var = tk.StringVar(value="")
        tk.Label(display_frame, textvariable=self._history_var,
                 font=("Courier", 10), fg="#888", bg="#1e1e2e",
                 anchor="e").pack(fill=tk.X)

        # Main display
        tk.Label(display_frame, textvariable=self._display_var,
                 font=("Courier", 28, "bold"), fg="white", bg="#1e1e2e",
                 anchor="e", padx=10).pack(fill=tk.X)

        # Buttons
        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

        buttons = [
            ("C",    0, 0, "#e74c3c", "#c0392b"),
            ("CE",   0, 1, "#e74c3c", "#c0392b"),
            ("%",    0, 2, "#6c5ce7", "#5d4fd6"),
            ("/",    0, 3, "#6c5ce7", "#5d4fd6"),
            ("7",    1, 0, "#2d3436", "#3d4446"),
            ("8",    1, 1, "#2d3436", "#3d4446"),
            ("9",    1, 2, "#2d3436", "#3d4446"),
            ("*",    1, 3, "#6c5ce7", "#5d4fd6"),
            ("4",    2, 0, "#2d3436", "#3d4446"),
            ("5",    2, 1, "#2d3436", "#3d4446"),
            ("6",    2, 2, "#2d3436", "#3d4446"),
            ("-",    2, 3, "#6c5ce7", "#5d4fd6"),
            ("1",    3, 0, "#2d3436", "#3d4446"),
            ("2",    3, 1, "#2d3436", "#3d4446"),
            ("3",    3, 2, "#2d3436", "#3d4446"),
            ("+",    3, 3, "#6c5ce7", "#5d4fd6"),
            ("+/-",  4, 0, "#2d3436", "#3d4446"),
            ("0",    4, 1, "#2d3436", "#3d4446"),
            (".",    4, 2, "#2d3436", "#3d4446"),
            ("=",    4, 3, "#00b894", "#00a381"),
        ]

        for text, row, col, bg, hover_bg in buttons:
            btn = tk.Button(
                btn_frame, text=text, font=("Arial", 16, "bold"),
                bg=bg, fg="white", activebackground=hover_bg,
                activeforeground="white", relief=tk.FLAT,
                cursor="hand2", bd=0,
                command=lambda t=text: self._button_click(t)
            )
            btn.grid(row=row, column=col, padx=3, pady=3,
                     sticky="nsew", ipady=12)
            btn_frame.rowconfigure(row, weight=1)
            btn_frame.columnconfigure(col, weight=1)

    def _button_click(self, value: str):
        if value == "C":
            self._expression = ""
            self._display_var.set("0")
            self._history_var.set("")
        elif value == "CE":
            self._expression = self._expression[:-1]
            self._display_var.set(self._expression or "0")
        elif value == "=":
            self._calculate()
        elif value == "+/-":
            try:
                current = float(self._expression or "0")
                self._expression = str(-current)
                self._display_var.set(self._expression)
            except ValueError:
                pass
        elif value == "%":
            try:
                current = float(self._expression or "0")
                self._expression = str(current / 100)
                self._display_var.set(self._expression)
            except ValueError:
                pass
        else:
            if self._expression == "Error":
                self._expression = ""
            self._expression += value
            self._display_var.set(self._expression)

    def _calculate(self):
        try:
            expression = self._expression
            self._history_var.set(expression + " =")
            result = eval(expression, {"__builtins__": {}}, {
                "math": math, "abs": abs, "round": round
            })
            # Format result
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self._expression = str(result)
            self._display_var.set(self._expression)
            self._history.append(f"{expression} = {result}")
        except ZeroDivisionError:
            self._display_var.set("Error: Div/0")
            self._expression = "Error"
        except Exception:
            self._display_var.set("Error")
            self._expression = "Error"

    def _key_press(self, event: tk.Event):
        key = event.char
        if key in "0123456789+-*/.":
            self._button_click(key)
        elif event.keysym == "Return":
            self._calculate()
        elif event.keysym in ("BackSpace", "Delete"):
            self._button_click("CE")
        elif event.keysym == "Escape":
            self._button_click("C")


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
