# Lesson 04 — Terminal Mastery

**Phase:** 00 — Environment Setup
**Time:** ~45 minutes (includes practice)
**Prerequisite:** Python + VS Code installed

---

## Part 1: Why Learn the Terminal?

```
Every professional developer uses the terminal daily.

With terminal you can:
  ✓ Navigate your file system without a mouse
  ✓ Run programs, scripts, and servers
  ✓ Install packages and tools
  ✓ Use Git for version control
  ✓ Deploy code to servers (servers have no GUI)
  ✓ Automate repetitive tasks
  ✓ Diagnose problems faster

Without terminal knowledge:
  ✗ Stuck on basic setup issues
  ✗ Can't use Git properly
  ✗ Can't run Python from command line
  ✗ Can't deploy or work on remote servers
```

---

## Part 2: Opening the Terminal

**Windows — PowerShell (Recommended):**
- Press `Win + X` → "Windows PowerShell"
- Or press `Win + R` → type `powershell` → Enter
- Or open VS Code → `Ctrl + `` ` ``

**Windows — Command Prompt (older):**
- Press `Win + R` → type `cmd` → Enter

**macOS:**
- Press `Cmd + Space` → type "Terminal" → Enter
- Or: Applications → Utilities → Terminal

**Linux:**
- `Ctrl + Alt + T` (most distributions)

---

## Part 3: Understanding the Prompt

```bash
# Windows PowerShell
PS C:\Users\YourName>

# macOS / Linux
yourname@computer:~$
```

Breaking it down:
```
PS               → PowerShell indicator
C:\Users\YourName → Your current location (working directory)
>                → Waiting for your command

~                → Home directory (shortcut)
$                → Regular user prompt
#                → Root/admin user prompt (Linux)
```

---

## Part 4: Essential Commands

### `pwd` — Print Working Directory

Shows where you currently are in the file system.

```bash
pwd
```

Output (Windows):
```
C:\Users\YourName
```

Output (Mac/Linux):
```
/Users/yourname
```

---

### `ls` / `dir` — List Files and Folders

```bash
ls          # Mac/Linux
dir         # Windows CMD
Get-ChildItem  # Windows PowerShell (or just ls — PowerShell accepts both)
```

Output:
```
Desktop    Documents    Downloads    projects    Desktop
```

Useful variations:

```bash
ls -la      # Mac/Linux: detailed view including hidden files
ls -l       # Mac/Linux: detailed list
dir /a      # Windows CMD: show all including hidden
```

---

### `cd` — Change Directory

Navigate between folders.

```bash
# Go into a folder
cd Desktop
cd Documents/projects

# Go back one level (parent folder)
cd ..

# Go back two levels
cd ../..

# Go to home directory
cd ~              # Mac/Linux
cd %USERPROFILE%  # Windows CMD
cd $HOME          # Windows PowerShell

# Go to root
cd /              # Mac/Linux
cd C:\            # Windows
```

**Practice sequence:**
```bash
pwd               # See where you are
cd Desktop        # Go to Desktop
pwd               # Confirm location
cd ..             # Go back
pwd               # Back to original
```

---

### `mkdir` — Make Directory (Create Folder)

```bash
mkdir projects
mkdir "my projects"         # Use quotes for names with spaces
mkdir projects/python       # Create nested folder
mkdir phase-01 phase-02    # Create multiple folders at once
```

---

### `touch` / `New-Item` — Create Empty File

```bash
# Mac/Linux
touch hello.py
touch README.md

# Windows PowerShell
New-Item hello.py
New-Item README.md
New-Item -ItemType File -Name hello.py  # explicit
```

---

### `cat` / `Get-Content` — View File Contents

```bash
# Mac/Linux
cat hello.py

# Windows PowerShell
Get-Content hello.py
cat hello.py    # PowerShell also accepts cat
```

---

### `cp` / `Copy-Item` — Copy Files

```bash
# Mac/Linux
cp hello.py hello_copy.py
cp -r folder1 folder2      # Copy entire folder

# Windows PowerShell
Copy-Item hello.py hello_copy.py
Copy-Item -Recurse folder1 folder2
```

---

### `mv` / `Move-Item` — Move or Rename Files

```bash
# Mac/Linux
mv hello.py greet.py              # Rename
mv hello.py /Desktop/projects/    # Move

# Windows PowerShell
Move-Item hello.py greet.py       # Rename
Move-Item hello.py C:\Desktop\    # Move
```

---

### `rm` / `Remove-Item` — Delete Files

```bash
# Mac/Linux
rm hello.py                 # Delete file
rm -rf folder_name          # Delete folder and all contents (CAREFUL!)

# Windows PowerShell
Remove-Item hello.py        # Delete file
Remove-Item -Recurse -Force folder_name  # Delete folder
```

⚠️ **Warning:** Deleted files from terminal do NOT go to the Recycle Bin on most systems. They are gone permanently.

---

### `clear` / `cls` — Clear Screen

```bash
clear    # Mac/Linux
cls      # Windows CMD
clear    # Windows PowerShell also accepts this
```

---

### `history` — View Command History

```bash
history         # Mac/Linux + PowerShell — shows all previous commands
```

**Navigation shortcuts:**
- `↑` arrow key — previous command
- `↓` arrow key — next command
- `Ctrl + R` — search through history

---

## Part 5: File Paths Explained

```
ABSOLUTE PATH — starts from the root
─────────────────────────────────────
Windows: C:\Users\YourName\Desktop\projects\hello.py
Mac:     /Users/yourname/Desktop/projects/hello.py

RELATIVE PATH — starts from where you currently are
────────────────────────────────────────────────────
If you're in C:\Users\YourName:
  Desktop\projects\hello.py

If you're in C:\Users\YourName\Desktop:
  projects\hello.py

SPECIAL SYMBOLS
───────────────
.    → Current directory
..   → Parent directory
~    → Home directory

Example:
  cd ./projects        same as cd projects
  cd ../Documents      go up then into Documents
  cd ~/Downloads       go to home/Downloads
```

---

## Part 6: Running Python from Terminal

```bash
# Run a Python file
python hello.py
python my_script.py

# Run Python interactively
python

# Run Python one-liner
python -c "print('Hello from command line')"

# Check Python version
python --version

# Run module
python -m http.server   # Starts a local web server
python -m pip install requests   # Install a package
```

---

## Part 7: Tab Completion

The terminal auto-completes file/folder names when you press `Tab`.

```bash
cd Des[TAB]        # Completes to: cd Desktop
python hel[TAB]    # Completes to: python hello.py
```

Press `Tab` twice to see all options when multiple matches exist.

---

## Part 8: Practical Exercise Session

**Do these in order. Use only the terminal.**

### Exercise Set A — Navigation

```bash
# 1. Open terminal
# 2. Find where you are
pwd

# 3. Go to Desktop
cd Desktop       # or cd ~/Desktop on Mac/Linux

# 4. Confirm you're on Desktop
pwd
```

### Exercise Set B — Creating Structure

```bash
# 1. Create a project folder
mkdir python-academy

# 2. Enter it
cd python-academy

# 3. Create subfolders
mkdir phase-00 phase-01 phase-02

# 4. Enter phase-00
cd phase-00

# 5. Create files
touch notes.txt
New-Item hello.py    # Windows PowerShell

# 6. Go back to python-academy
cd ..

# 7. List everything to confirm
ls
```

### Exercise Set C — File Operations

```bash
# 1. Copy a file
cp phase-00/hello.py phase-01/hello.py

# 2. Move and rename
mv phase-00/notes.txt phase-00/my-notes.txt

# 3. View the file tree
ls -R    # Mac/Linux (recursive)
tree     # Windows (if installed)
```

---

## Part 9: Cheat Sheet — Side by Side

| Task | Windows (PowerShell) | Mac / Linux |
|------|---------------------|-------------|
| Where am I? | `pwd` | `pwd` |
| List files | `ls` or `dir` | `ls` |
| Change directory | `cd folder` | `cd folder` |
| Go up | `cd ..` | `cd ..` |
| Home directory | `cd $HOME` | `cd ~` |
| Create folder | `mkdir name` | `mkdir name` |
| Create file | `New-Item name.py` | `touch name.py` |
| View file | `cat file.py` | `cat file.py` |
| Copy file | `Copy-Item src dst` | `cp src dst` |
| Move/rename | `Move-Item src dst` | `mv src dst` |
| Delete file | `Remove-Item file` | `rm file` |
| Delete folder | `Remove-Item -Recurse folder` | `rm -rf folder` |
| Clear screen | `clear` or `cls` | `clear` |
| History | `history` | `history` |
| Run Python | `python file.py` | `python3 file.py` |

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `cd C:/Users` | Wrong separator on Windows | Use `cd C:\Users` |
| `mkdir my folder` | Creates two folders | Use `mkdir "my folder"` |
| `rm -rf /` | Destroys entire system | Never run this |
| Spaces in file names | Commands break | Use underscores: `my_file.py` |
| `python` shows Python 2 | Wrong version | Use `python3` |

---

## Interview Questions

1. What is the difference between absolute and relative paths?
2. What does `..` mean in a file path?
3. Why would a developer use the terminal instead of a GUI?
4. What command shows your current directory?
5. How do you create a nested directory structure in one command?

---

## Next Lesson

**[Lesson 05 → Virtual Environments](lesson-05-virtual-environments.md)**
