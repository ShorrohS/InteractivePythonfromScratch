# ✅ Phase 00 — Beginner Exercise Solutions

> **Stop!** Have you attempted all questions first?
> Solutions are only useful after you've tried on your own.

---

## Section A: Concept Questions

**A1. What is a program?**

A program is a set of instructions written in a programming language that tells a computer what to do. Computers follow these instructions exactly as written. We write programs to automate tasks, solve problems, and create useful tools.

---

**A2. Hardware Matching:**

| Component | Answer |
|-----------|--------|
| CPU | B. Processes and executes instructions |
| RAM | C. Temporary memory cleared when powered off |
| SSD/HDD | A. Permanent storage that survives shutdown |

---

**A3. Compiled vs Interpreted:**

Python is **interpreted**, which means the Python interpreter reads and runs your code line by line at runtime, without first translating the entire program into machine code.

---

**A4. Fill in the blanks:**

```
1. Python reads the .py file from   STORAGE (SSD/HDD)
2. The code is loaded into          RAM (Memory)
3. The Python Interpreter sends it to the  CPU
4. Output is displayed on the       SCREEN (Monitor)
```

---

**A5. What happens to a variable when program ends?**

**Answer: B) It is lost from memory**

Variables live in RAM. When the program ends, RAM is cleared. To persist data, you must save it to a file or database.

---

## Section B: Terminal Commands

**A6. Terminal commands:**

```bash
a) pwd                                          # show current directory
b) cd Desktop/projects                          # navigate to projects
c) mkdir python-practice                        # create folder
d) ls    (Mac/Linux)  or  dir  (Windows)        # list files
e) cd ..                                         # go to parent folder
```

---

**A7. What each command does:**

```bash
cd ..
→ Goes to: /Users/alice (parent of Documents)

cd projects/phase-01
→ Goes to: /Users/alice/Documents/projects/phase-01

cd ~
→ Goes to: /Users/alice  (home directory)
```

---

**A8. What will pwd output?**

```
C:\Users\Alice\learning\python
```

Explanation: Each `cd` command moves into the specified folder. The final `pwd` shows the full path after all navigation.

---

## Section C: Virtual Environments

**A9. Correct order:**

```
C → B → D → A → E

C. mkdir my-project && cd my-project  (create and enter project folder)
B. python -m venv venv                 (create virtual environment)
D. source venv/bin/activate            (activate it)
A. pip install requests                (install packages)
E. pip freeze > requirements.txt       (save package list)
```

---

**A10. Why NOT commit venv/:**

**Correct answers: A and B**

- A) It's very large (hundreds of MB — no point bloating git history)
- B) It's machine-specific (absolute paths inside venv won't work on other machines)

C is incorrect (venv doesn't contain passwords unless you accidentally put them there)
D is incorrect (GitHub accepts Python files)

---

## Section D: Git

**A11. git add vs git commit:**

`git add` moves files to the **staging area** — a holding zone for files you plan to commit. It says "I want to include this file in my next snapshot."

`git commit` takes everything in the staging area and **saves a permanent snapshot** to the repository history with a message describing what changed.

Analogy: `git add` = putting items in a shipping box. `git commit` = sealing and labeling the box and sending it.

---

**A12. Git commands:**

| Command | What it does |
|---------|-------------|
| `git init` | Initializes a new Git repository in the current folder |
| `git status` | Shows current state: modified, staged, and untracked files |
| `git add .` | Stages ALL changed files in the current directory |
| `git commit -m "message"` | Saves a permanent snapshot with a descriptive message |
| `git log` | Shows the full history of all commits |

---

**A13. Correct Git order:**

```
C → D → B → A

C. git init           (initialize repository)
D. # create hello.py  (create the file)
B. git add hello.py   (stage the file)
A. git commit -m ...  (commit the snapshot)
```

---

**A14. Better commit messages:**

Bad: `"fix"` → Better: `"Fix divide-by-zero bug in calculator"`  
Bad: `"stuff"` → Better: `"Add user authentication module"`  
Bad: `"changes"` → Better: `"Update README with installation instructions"`  

---

**A15. The .gitignore file:**

**Answer: B) .gitignore**

---

## Section E: Practical Tasks

**A16.** (Your output will vary based on your installed version)

```
python --version  → Python 3.12.x  (or whichever version you installed)
pip --version     → pip 24.x.x from C:\...\pip (python 3.12)
```

---

**A17. Commands to create folder structure:**

```bash
mkdir my-academy
cd my-academy
mkdir phase-00 phase-01
cd phase-00

# Windows PowerShell:
New-Item notes.txt
New-Item hello.py

# Mac/Linux:
touch notes.txt
touch hello.py

cd ../phase-01

# Windows:
New-Item notes.txt

# Mac/Linux:
touch notes.txt

cd ..
```

---

**A18. Complete .gitignore:**

```
# Add virtual environment folder
venv/

# Add Python cache folder
__pycache__/

# Add the .env file for secrets
.env
```

---

## Bonus

**A19. VS Code shortcuts:**

a) Open terminal: `` Ctrl + ` ``  
b) Command palette: `Ctrl + Shift + P`  
c) Comment toggle: `Ctrl + /`  

---

**A20. Absolute vs Relative paths:**

**Absolute path:** `C:\Users\Alice\Desktop\project\main.py`
- Starts from the root of the file system
- Works from anywhere on the computer
- Use when you need to reference a specific file regardless of where your program is running

**Relative path:** `project\main.py`
- Starts from your current directory
- Only works if you're in the right place (`C:\Users\Alice\Desktop`)
- Use inside your project when referring to files relative to the project root
- Portable — works on other people's machines at different absolute paths

---

*If you answered 16+ correctly — great job! Move to the intermediate exercises.*
*If you answered fewer than 12 — re-read the lessons and try again.*
