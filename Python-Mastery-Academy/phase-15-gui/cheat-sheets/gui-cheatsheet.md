# ⚡ Phase 15 Cheat Sheet — Tkinter GUI

---

## Minimal Window

```python
import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("My App")
root.geometry("400x300")
root.mainloop()   # ALWAYS last line
```

---

## OOP Pattern (Recommended)

```python
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App")
        self.geometry("400x300")
        self._build()

    def _build(self):
        ttk.Label(self, text="Hello").pack()
        ttk.Button(self, text="OK", command=self._on_ok).pack()

    def _on_ok(self):
        messagebox.showinfo("OK", "Clicked!")

if __name__ == "__main__":
    App().mainloop()
```

---

## Widgets

```python
# Display
ttk.Label(parent, text="Hello", font=("Arial", 12))

# Input
ttk.Entry(parent, textvariable=str_var, width=25)
tk.Text(parent, height=5, width=40)
ttk.Spinbox(parent, from_=0, to=100)
ttk.Scale(parent, from_=0, to=100, orient=tk.HORIZONTAL)

# Selection
ttk.Checkbutton(parent, text="Check", variable=bool_var)
ttk.Radiobutton(parent, text="Opt1", variable=str_var, value="opt1")
ttk.Combobox(parent, values=["A","B","C"], textvariable=str_var)
tk.Listbox(parent, height=6, selectmode=tk.SINGLE)

# Action
ttk.Button(parent, text="Click", command=callback)

# Containers
ttk.Frame(parent)
ttk.LabelFrame(parent, text="Group")
ttk.Notebook(parent)   # tabbed

# Tables
ttk.Treeview(parent, columns=("Col1","Col2"), show="headings")
```

---

## Variables

```python
str_var  = tk.StringVar(value="default")
int_var  = tk.IntVar(value=0)
bool_var = tk.BooleanVar(value=False)

str_var.get()          # read
str_var.set("new")     # write

# Trace changes
str_var.trace_add("write", lambda *a: callback())
```

---

## Layout: grid (Recommended)

```python
widget.grid(row=0, column=0)
widget.grid(row=0, column=1, columnspan=2)
widget.grid(sticky="ew")      # stretch East-West
widget.grid(padx=5, pady=5)

# Make rows/cols expand
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
```

---

## Layout: pack

```python
widget.pack()                       # vertical stack
widget.pack(side=tk.LEFT)           # horizontal
widget.pack(fill=tk.BOTH, expand=True)  # fill all space
widget.pack(padx=10, pady=5)
```

---

## Dialogs

```python
from tkinter import messagebox, filedialog, simpledialog

messagebox.showinfo("Title", "Message")
messagebox.showwarning("Title", "Warning")
messagebox.showerror("Title", "Error")
result = messagebox.askyesno("Title", "Continue?")  # bool

name = simpledialog.askstring("Input", "Enter name:")
num  = simpledialog.askfloat("Input", "Enter amount:")

path = filedialog.askopenfilename(
    filetypes=[("CSV files", "*.csv"), ("All", "*.*")]
)
save_path = filedialog.asksaveasfilename(
    defaultextension=".csv"
)
```

---

## Treeview (Table)

```python
tree = ttk.Treeview(parent, columns=("Name","Age"), show="headings")
tree.heading("Name", text="Full Name")
tree.column("Name", width=150)

# Add row
tree.insert("", tk.END, values=("Alice", 30))

# Get selected
selection = tree.selection()
vals = tree.item(selection[0])["values"]

# Clear all
tree.delete(*tree.get_children())

# Scrollbar
sb = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=sb.set)
```

---

## Binding Events

```python
widget.bind("<Button-1>", callback)     # left click
widget.bind("<Return>", callback)        # Enter key
widget.bind("<Key>", callback)           # any key
widget.bind("<<ComboboxSelected>>", cb) # combobox change
root.bind("<Control-s>", save)          # keyboard shortcut
```
