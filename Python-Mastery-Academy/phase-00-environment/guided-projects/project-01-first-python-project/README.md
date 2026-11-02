# 🏗️ Guided Project 01 — First Python Project

**Phase:** 00 — Environment Setup
**Difficulty:** ⭐ Beginner
**Time:** ~45 minutes

---

## Project Goal

Build a properly structured Python project using the terminal. Every professional Python project follows this structure. You will practice it from day one.

---

## What You Will Build

```
my-first-project/
├── .gitignore              ← Tells Git what to ignore
├── README.md               ← Project documentation
├── requirements.txt        ← Package dependencies
├── venv/                   ← Virtual environment (not committed)
└── src/
    ├── main.py             ← Entry point
    └── greet.py            ← Helper module
```

---

## Instructions — Follow Step by Step

### Step 1 — Create the Project Folder

Open your terminal and navigate to a good location:

```bash
cd Desktop
mkdir my-first-project
cd my-first-project
```

Verify:
```bash
pwd
```
Should show: `.../Desktop/my-first-project`

---

### Step 2 — Initialize Git

```bash
git init
```

Output:
```
Initialized empty Git repository in .../my-first-project/.git/
```

---

### Step 3 — Create Virtual Environment

```bash
python -m venv venv
```

Verify it was created:
```bash
ls        # Mac/Linux
dir       # Windows
```

You should see the `venv/` folder.

---

### Step 4 — Activate Virtual Environment

```bash
# Windows PowerShell:
venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat

# macOS / Linux:
source venv/bin/activate
```

Your prompt should now show `(venv)` at the start.

---

### Step 5 — Create .gitignore

**Windows PowerShell:**
```bash
New-Item .gitignore
```

**macOS / Linux:**
```bash
touch .gitignore
```

Open `.gitignore` in VS Code and add:
```
venv/
__pycache__/
*.pyc
.env
.DS_Store
```

---

### Step 6 — Create README.md

**Windows:**
```bash
New-Item README.md
```

**Mac/Linux:**
```bash
touch README.md
```

Open `README.md` and add:
```markdown
# My First Python Project

A greeting application built while learning Python.

## Setup

1. Clone this repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python src/main.py`
```

---

### Step 7 — Create the Source Directory and Files

```bash
mkdir src
```

**Windows:**
```bash
New-Item src\greet.py
New-Item src\main.py
```

**Mac/Linux:**
```bash
touch src/greet.py
touch src/main.py
```

---

### Step 8 — Write the Code

Open VS Code in the project folder:
```bash
code .
```

**Write this in `src/greet.py`:**

```python
"""
greet.py — Helper module for greeting functions.
"""


def create_greeting(name: str) -> str:
    """Create a personalized greeting message."""
    return f"Hello, {name}! Welcome to Python."


def create_farewell(name: str) -> str:
    """Create a personalized farewell message."""
    return f"Goodbye, {name}! Keep coding."


def display_banner() -> None:
    """Display the application banner."""
    print("=" * 45)
    print("   MY FIRST PYTHON PROJECT")
    print("   Phase 00 — Environment Setup Complete!")
    print("=" * 45)
```

**Write this in `src/main.py`:**

```python
"""
main.py — Entry point for the greeting application.

This is my first Python project!
Created while completing Phase 00 of Python Mastery Academy.
"""

from greet import create_greeting, create_farewell, display_banner


def main():
    """Main function — runs the greeting application."""
    display_banner()
    
    print()
    name = input("Enter your name: ")
    
    print()
    greeting = create_greeting(name)
    print(greeting)
    
    print()
    input("Press Enter to continue...")
    
    farewell = create_farewell(name)
    print(farewell)
    print()
    print("✅ Phase 00 Complete!")
    print("Next: Open phase-01-fundamentals/README.md")


if __name__ == "__main__":
    main()
```

---

### Step 9 — Run the Program

```bash
cd src
python main.py
```

You should see the banner and be prompted to enter your name.

---

### Step 10 — Install a Package (Practice)

Go back to project root:
```bash
cd ..
```

Install a package:
```bash
pip install colorama
```

Verify:
```bash
pip list
```

Save dependencies:
```bash
pip freeze > requirements.txt
```

View the file:
```bash
cat requirements.txt    # Mac/Linux
Get-Content requirements.txt  # Windows
```

---

### Step 11 — Make Your First Commit

Check what Git sees:
```bash
git status
```

Stage the files (NOT venv):
```bash
git add .gitignore
git add README.md
git add requirements.txt
git add src/
```

Verify staging:
```bash
git status
```

Commit:
```bash
git commit -m "Initial commit: first Python project with greet module"
```

View history:
```bash
git log --oneline
```

---

### Step 12 — Make a Change and Commit Again

Open `src/greet.py` and add this function:

```python
def get_python_fact() -> str:
    """Return a fun Python fact."""
    return "Python was named after Monty Python, not the snake!"
```

Save the file. Then:

```bash
git status                    # Shows modified file
git diff                      # Shows exactly what changed
git add src/greet.py
git commit -m "Add Python fact function to greet module"
git log --oneline             # Shows 2 commits
```

---

## ✅ Verification Checklist

After completing this project:

- [ ] Project folder exists with correct structure
- [ ] Virtual environment was created and activated
- [ ] .gitignore exists and includes `venv/`
- [ ] At least 2 commits in `git log --oneline`
- [ ] `python src/main.py` runs without errors
- [ ] `requirements.txt` exists
- [ ] README.md explains the project

---

## What You Practiced

| Skill | Practiced |
|-------|----------|
| Terminal navigation | ✅ |
| Creating folders/files via terminal | ✅ |
| Virtual environment setup | ✅ |
| pip install + freeze | ✅ |
| Git init + add + commit | ✅ |
| VS Code for coding | ✅ |
| Writing a README | ✅ |
| Professional project structure | ✅ |

---

## Next

**→ [Phase 01 — Python Fundamentals](../../../phase-01-fundamentals/README.md)**
