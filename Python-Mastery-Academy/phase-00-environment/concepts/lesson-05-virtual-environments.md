# Lesson 05 — Virtual Environments

**Phase:** 00 — Environment Setup
**Time:** ~30 minutes
**Prerequisite:** Terminal competency (Lesson 04)

---

## Part 1: The Problem Virtual Environments Solve

Imagine you have two projects:

```
Project A: requires requests==2.28.0
Project B: requires requests==2.31.0
```

Without virtual environments, you can only have one version installed globally. One project will break.

**With virtual environments:**

```
Project A has its OWN Python + its OWN packages
Project B has its OWN Python + its OWN packages

They never conflict.
```

---

## Part 2: What is a Virtual Environment?

A virtual environment is an **isolated Python installation** for a specific project.

```
YOUR COMPUTER
│
├── Global Python (system-wide)
│   └── packages: pip, setuptools
│
├── projects/
│   │
│   ├── project-a/
│   │   ├── venv/           ← Virtual environment
│   │   │   ├── python.exe  ← Project's own Python
│   │   │   └── site-packages/  ← Project's own packages
│   │   │       ├── requests 2.28
│   │   │       └── flask 2.0
│   │   └── main.py
│   │
│   └── project-b/
│       ├── venv/           ← Separate virtual environment
│       │   ├── python.exe
│       │   └── site-packages/
│       │       ├── requests 2.31
│       │       └── django 4.0
│       └── main.py
```

Each project's packages are completely isolated.

---

## Part 3: Creating a Virtual Environment

### Navigate to Your Project Folder First

```bash
cd Desktop
mkdir my-python-project
cd my-python-project
```

### Create the Virtual Environment

```bash
python -m venv venv
```

Breaking this down:
- `python` — use Python
- `-m venv` — run the venv module
- `venv` — name for the virtual environment folder (convention: use "venv")

This creates a `venv/` folder in your project:

```
my-python-project/
└── venv/
    ├── Scripts/      ← Windows
    │   ├── python.exe
    │   ├── pip.exe
    │   └── activate  ← Activation script
    └── Lib/
        └── site-packages/  ← Packages install here
```

---

## Part 4: Activating the Virtual Environment

You must **activate** the virtual environment before using it.

### Windows (PowerShell):

```bash
venv\Scripts\Activate.ps1
```

### Windows (Command Prompt):

```bash
venv\Scripts\activate.bat
```

### macOS / Linux:

```bash
source venv/bin/activate
```

**After activation, your prompt changes:**

```bash
# Before activation
C:\Users\You\project>

# After activation (Windows)
(venv) C:\Users\You\project>

# After activation (Mac/Linux)
(venv) yourname@computer:~/project$
```

The `(venv)` prefix confirms the virtual environment is active.

---

## Part 5: Deactivating

When you're done working on a project:

```bash
deactivate
```

Your prompt returns to normal. The virtual environment is no longer active.

---

## Part 6: Installing Packages with pip

**Only install packages AFTER activating the virtual environment.**

```bash
# Install a single package
pip install requests

# Install a specific version
pip install requests==2.31.0

# Install multiple packages
pip install requests flask pandas

# Install from a requirements file
pip install -r requirements.txt

# Upgrade a package
pip install --upgrade requests

# Uninstall a package
pip uninstall requests
```

---

## Part 7: requirements.txt — Sharing Dependencies

The `requirements.txt` file lists all packages your project needs.

### Generate requirements.txt

```bash
pip freeze > requirements.txt
```

This creates a file like:

```
certifi==2024.2.2
charset-normalizer==3.3.2
idna==3.6
requests==2.31.0
urllib3==2.2.1
```

### Install from requirements.txt

Someone else clones your project and runs:

```bash
python -m venv venv
venv\Scripts\Activate.ps1    # or source venv/bin/activate
pip install -r requirements.txt
```

They get the exact same package versions as you. ✅

---

## Part 8: pip Commands Reference

```bash
# List installed packages
pip list

# Show info about a specific package
pip show requests

# Search for a package
pip search package_name

# Check for outdated packages
pip list --outdated

# Show what pip freeze generates
pip freeze

# Generate requirements file
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

---

## Part 9: .gitignore for Virtual Environments

Never commit your `venv/` folder to Git.

Create a `.gitignore` file in your project:

```bash
# Windows PowerShell
New-Item .gitignore

# Mac/Linux
touch .gitignore
```

Add this content to `.gitignore`:

```
# Virtual environment
venv/
env/
.env/
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo

# IDE files
.vscode/
.idea/

# Environment variables
.env
```

Git will now ignore the `venv/` folder.

---

## Part 10: Complete Workflow — Every New Project

This is the professional workflow for every new Python project:

```bash
# 1. Create project folder
mkdir project-name
cd project-name

# 2. Initialize git
git init

# 3. Create virtual environment
python -m venv venv

# 4. Activate it
venv\Scripts\Activate.ps1   # Windows
source venv/bin/activate     # Mac/Linux

# 5. Create .gitignore
# Add venv/, __pycache__/, .env to it

# 6. Install dependencies
pip install requests flask   # whatever your project needs

# 7. Create requirements.txt
pip freeze > requirements.txt

# 8. Create your main Python file
New-Item main.py   # Windows
touch main.py      # Mac/Linux

# 9. Start coding!
# code .   ← opens VS Code in current folder
```

---

## Part 11: Common Mistakes

### Mistake 1: Installing packages without activating venv

```bash
# WRONG — installs globally, pollutes system Python
pip install requests

# CORRECT — activate first
venv\Scripts\Activate.ps1
pip install requests
```

### Mistake 2: Committing venv/ to Git

```
Don't commit the venv folder.
It's hundreds of MB and machine-specific.
Use requirements.txt instead.
```

### Mistake 3: Not recreating venv after cloning

```bash
# After cloning someone's project:
git clone https://github.com/...
cd project

# Create NEW venv (don't copy theirs)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Mistake 4: Windows PowerShell execution policy error

```bash
# Error: "cannot be loaded because running scripts is disabled"
# Fix:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try activating again
```

---

## Summary

| Command | What it does |
|---------|-------------|
| `python -m venv venv` | Create virtual environment |
| `venv\Scripts\Activate.ps1` | Activate (Windows) |
| `source venv/bin/activate` | Activate (Mac/Linux) |
| `deactivate` | Deactivate |
| `pip install package` | Install package (while active) |
| `pip list` | See installed packages |
| `pip freeze > requirements.txt` | Save package list |
| `pip install -r requirements.txt` | Install from saved list |

---

## Next Lesson

**[Lesson 06 → Git Fundamentals](lesson-06-git-fundamentals.md)**
