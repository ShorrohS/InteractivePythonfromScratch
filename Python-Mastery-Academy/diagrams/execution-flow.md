# 🔷 Diagram: Python Code Execution Flow

> How your Python code goes from text file to running program.

---

## Full Execution Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                  PYTHON EXECUTION PIPELINE                      │
└─────────────────────────────────────────────────────────────────┘

YOU                    PYTHON INTERPRETER              COMPUTER
─────────────────────────────────────────────────────────────────

┌──────────────┐
│ Write Code   │
│              │
│ print("Hi")  │
└──────┬───────┘
       │  Save as .py file
       ▼
┌──────────────┐
│ Source Code  │   ← Human-readable text
│   (.py file) │     stored on disk (SSD/HDD)
└──────┬───────┘
       │  python your_file.py
       ▼
┌──────────────┐
│   LEXER      │   ← Breaks code into tokens
│              │     "print" → KEYWORD
│              │     "("    → LPAREN
│              │     "Hi"   → STRING
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   PARSER     │   ← Builds Abstract Syntax Tree (AST)
│              │     Checks grammar rules
│              │     Finds SyntaxErrors here
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  COMPILER    │   ← Converts AST to bytecode
│              │     Creates .pyc files
│              │     (cached for speed)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  PVM         │   ← Python Virtual Machine
│  (Runtime)   │     Executes bytecode
│              │     Manages memory
│              │     Calls C libraries
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  OUTPUT      │   ← Results appear on screen
│              │     Files written to disk
│  Hi          │     Network calls made
└──────────────┘
```

---

## Simplified View (What You Need to Know)

```
.py file  →  Python Interpreter  →  Output
  (you)         (Python does this)    (screen)
```

---

## Where Errors Occur

```
┌─────────────────────────────────────────────────────────────┐
│                     ERROR LOCATIONS                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SYNTAX ERROR — caught during parsing (before running)     │
│  Example:                                                   │
│    print("Hello"          ← missing closing parenthesis    │
│                                                             │
│  RUNTIME ERROR — occurs while program is running           │
│  Example:                                                   │
│    x = 10 / 0             ← ZeroDivisionError              │
│                                                             │
│  LOGIC ERROR — program runs but gives wrong output         │
│  Example:                                                   │
│    area = length + width  ← should be * not +              │
│    (No error raised, but result is wrong)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Compiled vs Interpreted

```
COMPILED LANGUAGE (e.g., C++)
──────────────────────────────
Source Code (.cpp)
      │
      ▼  (compile once)
Machine Code (.exe)
      │
      ▼  (run directly)
Output

→ Faster execution
→ Platform-specific binary
→ Must recompile to change


INTERPRETED LANGUAGE (Python)
──────────────────────────────
Source Code (.py)
      │
      ▼  (interpret each time)
Bytecode → PVM → Output

→ Slightly slower
→ Platform-independent
→ Run immediately after editing
→ Easier to debug interactively
```

---

## Python .pyc Cache Files

```
When you run: python main.py

Python creates: __pycache__/main.cpython-311.pyc

Why?
→ Compiled bytecode is cached
→ Next run skips compilation step
→ Faster startup time

You can ignore these files.
Add __pycache__/ to .gitignore
```

---

## Interactive Mode vs Script Mode

```
SCRIPT MODE
───────────
python my_program.py
→ Runs entire file top to bottom
→ Exits when done
→ How most programs run

INTERACTIVE MODE (REPL)
────────────────────────
>>> python
>>> print("Hello")
Hello
>>> 2 + 2
4
→ Type one line, see result immediately
→ Great for testing ideas
→ Exit with: exit() or Ctrl+D
```

---

## What Happens When You Import

```python
import math
```

```
1. Python looks for 'math' module
   → First: built-in modules
   → Then: site-packages (pip installs)
   → Then: current directory

2. Runs the module code once

3. Stores module object in memory

4. You access it with: math.sqrt(16)
```

---

## Memory Management (Simplified)

```
When you write:
    x = 42

Python:
    1. Allocates memory in RAM
    2. Stores the integer 42
    3. Creates a name 'x' pointing to that memory
    4. Returns the address

When nothing points to 42 anymore:
    Garbage Collector frees the memory
    (automatic — you don't manage this manually)
```

---

## Key Takeaways

| Concept | What It Means Practically |
|---------|--------------------------|
| Interpreted | Edit and run immediately, no compile step |
| Bytecode | Python does compile, just internally |
| PVM | The heart of Python — runs your bytecode |
| Garbage Collection | Memory is managed for you |
| SyntaxError | Caught before running — check your code |
| RuntimeError | Caught while running — use try/except |
| LogicError | Never caught — write tests to find these |
