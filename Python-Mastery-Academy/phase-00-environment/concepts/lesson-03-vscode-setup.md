# Lesson 03 — VS Code Setup

**Phase:** 00 — Environment Setup
**Time:** ~30 minutes
**Prerequisite:** Python installed (Lesson 02)

---

## Part 1: Why VS Code?

```
VS Code is the industry-standard editor for Python development.

FREE          → Completely free from Microsoft
LIGHTWEIGHT   → Starts fast, uses minimal resources
EXTENSIBLE    → Thousands of extensions
DEBUGGING     → Built-in visual debugger
GIT BUILT-IN  → Source control integrated
TERMINAL      → Integrated terminal — no switching windows
INTELLISENSE  → Auto-complete as you type
CROSS-PLATFORM → Windows, macOS, Linux
```

---

## Part 2: Installing VS Code

### Step 1 — Download

Go to: **https://code.visualstudio.com/**

Click the blue download button for your OS.

### Step 2 — Install (Windows)

Run the downloaded installer.

During installation, check these options:
- ✅ **Add to PATH**
- ✅ **Register Code as an editor for supported file types**
- ✅ **Add "Open with Code" action to Windows Explorer file context menu**
- ✅ **Add "Open with Code" action to Windows Explorer directory context menu**

Click Install.

### Step 3 — Open VS Code

After installation, open VS Code.

---

## Part 3: Essential Extensions

Extensions are add-ons that extend VS Code's functionality.

### Installing the Python Extension

1. Open VS Code
2. Press `Ctrl + Shift + X` (Extensions panel)
3. Search: **Python**
4. Install the one by **Microsoft** (first result, 100M+ downloads)
5. Reload VS Code when prompted

### Recommended Extensions for This Course

| Extension | Publisher | What It Does |
|-----------|-----------|-------------|
| **Python** | Microsoft | Python support, IntelliSense, debugging |
| **Pylance** | Microsoft | Fast type checking (installs with Python) |
| **GitLens** | GitKraken | Enhanced Git integration |
| **indent-rainbow** | oderwat | Colorizes indentation levels |
| **Better Comments** | Aaron Bond | Color-coded comments |
| **Python Snippets** | frhtylcn | Useful code snippets |
| **Material Icon Theme** | Philipp Kief | Better file icons |

**How to install each:**
1. `Ctrl + Shift + X`
2. Search the extension name
3. Click Install

---

## Part 4: VS Code Interface Tour

```
┌──────────────────────────────────────────────────────────────┐
│  FILE     EDIT    SELECTION    VIEW    ...          [min][max]│
├──────┬───────────────────────────────────────────────────────┤
│      │                                                       │
│  A   │                   EDITOR AREA                         │
│  C   │                                                       │
│  T   │   This is where you write code                        │
│  I   │                                                       │
│  V   │                                                       │
│  I   ├───────────────────────────────────────────────────────┤
│  T   │                                                       │
│  Y   │              INTEGRATED TERMINAL                      │
│  B   │                                                       │
│  A   │   $ python demo.py                                    │
│  R   │   Hello World                                         │
│      │                                                       │
└──────┴───────────────────────────────────────────────────────┘

LEFT SIDEBAR ICONS (top to bottom):
📄  Explorer          → File/folder tree
🔍  Search            → Search across files
🌿  Source Control    → Git integration
🐞  Run & Debug       → Debugger
🧩  Extensions        → Install extensions
```

---

## Part 5: Essential VS Code Shortcuts

Learn these. They will save hours every week.

### Navigation
| Shortcut | Action |
|----------|--------|
| `Ctrl + P` | Quick open file |
| `Ctrl + Shift + P` | Command palette |
| `Ctrl + B` | Toggle sidebar |
| `` Ctrl + ` `` | Toggle terminal |
| `Ctrl + Tab` | Switch between open files |
| `Ctrl + \` | Split editor |

### Editing
| Shortcut | Action |
|----------|--------|
| `Ctrl + D` | Select next occurrence of word |
| `Alt + Up/Down` | Move line up/down |
| `Shift + Alt + Up/Down` | Copy line up/down |
| `Ctrl + Shift + K` | Delete line |
| `Ctrl + /` | Toggle comment |
| `Ctrl + Z` | Undo |
| `Ctrl + Shift + Z` | Redo |
| `Tab` | Indent |
| `Shift + Tab` | Outdent |
| `Ctrl + L` | Select entire line |

### Running Python
| Shortcut | Action |
|----------|--------|
| `F5` | Run with debugger |
| `Ctrl + F5` | Run without debugger |
| `Shift + Enter` | Run selection in terminal |

---

## Part 6: Configuring Python in VS Code

### Select Python Interpreter

1. Open any `.py` file
2. Bottom-left corner: click the Python version indicator
3. Or: `Ctrl + Shift + P` → type "Python: Select Interpreter"
4. Choose the Python 3.x.x version you installed

**Why this matters:** VS Code needs to know which Python to use, especially when you have virtual environments.

### Configure Settings (Optional but Recommended)

Press `Ctrl + Shift + P` → "Open User Settings (JSON)"

Add these settings:

```json
{
    "editor.formatOnSave": true,
    "editor.rulers": [79],
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "python.languageServer": "Pylance",
    "files.autoSave": "afterDelay",
    "terminal.integrated.defaultProfile.windows": "PowerShell"
}
```

---

## Part 7: The Integrated Terminal

VS Code has a built-in terminal. Use it instead of switching windows.

**Open terminal:** `` Ctrl + ` `` (backtick)

```bash
# The terminal opens at your workspace folder

# Run Python files directly
python filename.py

# Navigate
cd folder_name
dir       # Windows (list files)
ls        # Mac/Linux (list files)
```

**Split the terminal:** Click the split icon (⊞) in the terminal toolbar to have multiple terminals open simultaneously.

---

## Part 8: Opening a Project Folder

**Best practice:** Always open the entire project folder, not individual files.

```bash
# Method 1: From terminal
code .        # Opens current folder in VS Code

# Method 2: From VS Code
File → Open Folder → (select your project folder)

# Method 3: Drag folder
Drag the project folder onto the VS Code icon
```

This ensures:
- File explorer shows the full project
- Terminal defaults to project root
- Python imports work correctly

---

## Part 9: The Debugger

The debugger is one of the most valuable tools in VS Code.

### Setting a Breakpoint

1. Click in the gutter (left margin) next to a line number
2. A red dot appears — this is a breakpoint
3. Press `F5` to start debugging
4. Program pauses at the breakpoint

### Debug Panel

When paused at a breakpoint:
```
VARIABLES panel → Shows all current variable values
WATCH panel     → Monitor specific expressions
CALL STACK      → Shows which functions were called
BREAKPOINTS     → List of all breakpoints
```

**Stepping through code:**
- `F10` — Step over (run next line, don't go into functions)
- `F11` — Step into (go inside function call)
- `Shift + F11` — Step out (finish current function)
- `F5` — Continue to next breakpoint

---

## Part 10: Themes

Customize VS Code's appearance:

```
Ctrl + Shift + P → "Color Theme"

Popular themes:
- One Dark Pro
- Dracula Official
- GitHub Dark
- Monokai Pro
- Night Owl
```

Install themes from the Extensions marketplace (`Ctrl + Shift + X`).

---

## Verification — VS Code is Ready When:

- [ ] VS Code opens without errors
- [ ] Python extension is installed (see bottom status bar)
- [ ] Opening a .py file shows syntax highlighting (colored code)
- [ ] Pressing `` Ctrl + ` `` opens a terminal
- [ ] Running `python --version` in VS Code terminal works
- [ ] You can see the file explorer in the sidebar

---

## Quick Reference Card

```
OPEN TERMINAL:    Ctrl + `
COMMAND PALETTE:  Ctrl + Shift + P
QUICK OPEN FILE:  Ctrl + P
RUN FILE:         Right-click → Run Python File
COMMENT TOGGLE:   Ctrl + /
MOVE LINE:        Alt + Up/Down
DELETE LINE:      Ctrl + Shift + K
FORMAT CODE:      Shift + Alt + F
FIND IN FILE:     Ctrl + F
FIND ALL FILES:   Ctrl + Shift + F
```

---

## Next Lesson

**[Lesson 04 → Terminal Mastery](lesson-04-terminal-mastery.md)**
