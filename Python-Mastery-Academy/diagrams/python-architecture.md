# 🔷 Diagram: Python Architecture

> How Python works under the hood.

---

## Python's Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR CODE (.py file)                      │
│                                                             │
│   name = "Alice"                                            │
│   print(f"Hello, {name}!")                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   CPYTHON (The Standard Python)             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. TOKENIZER (Lexer)                               │   │
│  │     Breaks code into tokens                         │   │
│  │     "name" → NAME token                             │   │
│  │     "=" → EQUAL token                               │   │
│  │     '"Alice"' → STRING token                        │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────────┐   │
│  │  2. PARSER                                          │   │
│  │     Builds Abstract Syntax Tree (AST)               │   │
│  │     Checks grammar rules                            │   │
│  │     SyntaxErrors caught HERE                        │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────────┐   │
│  │  3. COMPILER                                        │   │
│  │     Converts AST → Bytecode                         │   │
│  │     Saves to __pycache__/*.pyc                      │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────────┐   │
│  │  4. PYTHON VIRTUAL MACHINE (PVM)                    │   │
│  │     Executes bytecode instructions                  │   │
│  │     Manages memory (stack + heap)                   │   │
│  │     Calls C libraries for I/O, math, etc.           │   │
│  │     Runs garbage collector                          │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
└───────────────────────────┼─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  OPERATING SYSTEM                           │
│  Memory Management | File System | Network | Process Mgmt  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     HARDWARE                                │
│            CPU | RAM | SSD | Network Card                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Python Standard Library

```
Python comes with "batteries included":

IO & Files:     os, pathlib, shutil, io
Data:           json, csv, sqlite3, pickle
Network:        http, urllib, socket, email
Text:           re, string, textwrap, difflib
Numbers:        math, decimal, fractions, statistics
Time:           datetime, time, calendar
Data Types:     collections, heapq, itertools, functools
Concurrency:    threading, multiprocessing, asyncio
Testing:        unittest, doctest
Misc:           sys, platform, logging, warnings
```

---

## Python Object Model

```
EVERYTHING in Python is an object:

  42            → int object
  "hello"       → str object
  [1,2,3]       → list object
  def foo(): →  function object
  class Bar: →  type object

Every object has:
  id()    → unique identifier (memory address)
  type()  → its class
  value   → its data
```

---

## Memory Model Summary

```
┌──────────────────────────────────────────────────────────┐
│  STACK (call stack)          HEAP (object store)         │
│  ─────────────────           ────────────────────        │
│                                                          │
│  main()                      "Alice"  (str object)       │
│   └─ name ──────────────────► id=0x1a                    │
│                                                          │
│  greet("Alice")              function greet              │
│   └─ local: name ────────────► id=0x2b                   │
│                                                          │
│  When main() returns:        Garbage Collector           │
│  Stack frame is deleted      frees unused objects        │
└──────────────────────────────────────────────────────────┘
```

---

## Python Implementations

```
CPython    → Reference implementation (written in C). What you installed.
PyPy       → JIT-compiled, much faster for loops
Jython     → Python on the JVM (Java)
IronPython → Python on .NET (C#)
MicroPython → Python for microcontrollers (IoT)
```

For learning and most professional work, CPython is what you use.

---

## The GIL (Global Interpreter Lock)

```
CPython has a GIL: only ONE thread runs Python code at a time.

This means:
  - Multi-threading doesn't improve CPU-bound tasks
  - For CPU-bound parallel work → use multiprocessing
  - For I/O-bound work → threading works fine (GIL released during I/O)
  - For async I/O → asyncio (best for network/web)

Python 3.12+ is working toward removing the GIL.
```

---

## How Import Works

```python
import math

# Python:
# 1. Checks sys.modules cache (already imported?)
# 2. Finds math module (built-in? site-packages? local dir?)
# 3. Loads and executes the module code once
# 4. Stores in sys.modules
# 5. Binds name 'math' to the module object
```

---

## Interview Questions

1. What happens when you run `python script.py`?
2. What is bytecode and where is it stored?
3. What is the GIL and when does it matter?
4. What does `id()` return and what does it mean?
5. Why are integers and strings immutable in Python?
6. What is a Python object?
7. How does garbage collection work in Python?
