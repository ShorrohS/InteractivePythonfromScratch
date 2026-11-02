# 🔷 Diagram: CPU, Memory & Storage

> Visual reference for understanding how hardware relates to programming.

---

## The Hardware Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                            │
│                                                             │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────────┐  │
│  │     CPU      │   │     RAM      │   │    STORAGE     │  │
│  │  (Processor) │◄──│  (Memory)    │◄──│  (HDD / SSD)   │  │
│  │              │   │              │   │                │  │
│  │  • Executes  │   │  • Temporary │   │  • Permanent   │  │
│  │    instructions│  │  • Very fast │   │  • Slower      │  │
│  │  • Does math │   │  • Lost on   │   │  • Survives    │  │
│  │  • Runs logic│   │    shutdown  │   │    shutdown    │  │
│  │              │   │              │   │                │  │
│  │  Speed:      │   │  Speed:      │   │  Speed:        │  │
│  │  Billions/sec│   │  GB/sec      │   │  MB/sec        │  │
│  └──────────────┘   └──────────────┘   └────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              OPERATING SYSTEM                        │   │
│  │  Manages all above hardware                          │   │
│  │  Windows / macOS / Linux                             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Real-World Analogy

```
┌──────────────────────────────────────────────────────────┐
│                   RESTAURANT ANALOGY                     │
│                                                          │
│  CPU = CHEF                                              │
│  └── Does the actual cooking (processing)                │
│                                                          │
│  RAM = KITCHEN COUNTER                                   │
│  └── Holds ingredients being used RIGHT NOW              │
│  └── Gets cleared when the restaurant closes             │
│                                                          │
│  STORAGE = PANTRY / REFRIGERATOR                         │
│  └── Stores everything long-term                         │
│  └── Chef walks to pantry to get ingredients             │
│                                                          │
│  OS = RESTAURANT MANAGER                                 │
│  └── Coordinates everything                              │
│  └── Ensures no two chefs collide                        │
└──────────────────────────────────────────────────────────┘
```

---

## Python Program Lifecycle

```
Step 1: STORAGE → RAM
┌────────────────────────────────────┐
│  your_program.py lives on disk     │
│  When you run it → loaded into RAM │
└────────────────────────────────────┘
           │
           ▼
Step 2: RAM → CPU
┌────────────────────────────────────┐
│  Python reads code from RAM        │
│  Interprets each line              │
│  Sends instructions to CPU         │
└────────────────────────────────────┘
           │
           ▼
Step 3: CPU EXECUTES
┌────────────────────────────────────┐
│  CPU runs the actual computation   │
│  Results stored back in RAM        │
│  Output sent to screen             │
└────────────────────────────────────┘
           │
           ▼
Step 4: OUTPUT
┌────────────────────────────────────┐
│  Result displayed on monitor       │
│  Or saved back to storage          │
└────────────────────────────────────┘
```

---

## Variables in Memory

```python
name = "Alice"
age  = 30
```

```
RAM VISUALIZATION:
┌─────────────────────────────────┐
│   MEMORY (RAM)                  │
│                                 │
│   Address  │  Name  │  Value    │
│   ─────────┼────────┼────────   │
│   0x7f4a1  │  name  │ "Alice"   │
│   0x7f4a2  │  age   │  30       │
│                                 │
│   When program ends → CLEARED   │
└─────────────────────────────────┘
```

---

## Key Comparisons

| Property | CPU | RAM | Storage |
|----------|-----|-----|---------|
| Speed | Fastest | Fast | Slowest |
| Capacity | Tiny (cache) | 4–64 GB | 128 GB – several TB |
| Persistence | None | Temporary | Permanent |
| Cost per GB | Very high | High | Low |
| Python use | Runs code | Stores running data | Reads/writes files |

---

## What Python Uses

```
When you run:   python my_script.py
                        │
                        ▼
┌───────────────────────────────────────────────┐
│  Python Interpreter loads my_script.py        │
│  from STORAGE into RAM                         │
├───────────────────────────────────────────────┤
│  Variables you create → stored in RAM          │
│  Functions you call → executed by CPU          │
│  Files you open → read from STORAGE into RAM   │
│  Files you save → written from RAM to STORAGE  │
└───────────────────────────────────────────────┘
```

---

## Interview Questions on This Topic

1. What is the difference between RAM and storage?
2. Why does a variable disappear when a Python program ends?
3. Why is it important to close files after opening them in Python?
4. If RAM is temporary, how do we persist data in Python?
5. What does the CPU actually do when Python runs `2 + 2`?

---

## Answer Key

1. **RAM** is temporary, fast, and holds data while the program runs. **Storage** is permanent and slower.
2. Variables live in RAM. When the program ends, RAM is cleared.
3. Open files use RAM resources. Closing them frees memory and flushes data to storage.
4. We use files, databases, or external storage to make data permanent.
5. Python translates `2 + 2` to machine instructions. The CPU's ALU (Arithmetic Logic Unit) adds 4 and returns the result.
