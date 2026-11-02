# ⚡ Environment Cheat Sheet

> Print this or keep it open while working. Quick reference for Phase 00.

---

## Terminal Commands

```bash
# NAVIGATION
pwd                    # Where am I?
ls / dir               # List files here
cd folder_name         # Enter folder
cd ..                  # Go up one level
cd ~                   # Go to home directory
cd /                   # Go to root (Mac/Linux)

# CREATE
mkdir folder_name              # Create folder
touch file.py                  # Create file (Mac/Linux)
New-Item file.py               # Create file (Windows)

# VIEW / EDIT
cat file.py                    # View file (Mac/Linux)
Get-Content file.py            # View file (Windows)
code .                         # Open current folder in VS Code
code file.py                   # Open specific file in VS Code

# COPY / MOVE / DELETE
cp src dst         # Copy file (Mac/Linux)
mv src dst         # Move/rename (Mac/Linux)
rm file.py         # Delete file (Mac/Linux)
Copy-Item src dst             # Copy (Windows)
Move-Item src dst             # Move/rename (Windows)
Remove-Item file.py           # Delete (Windows)

# UTILITIES
clear / cls                    # Clear terminal screen
history                        # Show command history
↑ / ↓ arrows                  # Navigate command history
Tab                            # Auto-complete
Ctrl + C                       # Stop a running program
```

---

## Python Commands

```bash
python --version               # Check Python version
python                         # Start interactive shell
python filename.py             # Run a script
python -c "print('hello')"     # Run one-liner
exit()                         # Exit interactive shell
```

---

## Virtual Environments

```bash
# CREATE
python -m venv venv

# ACTIVATE
venv\Scripts\Activate.ps1      # Windows PowerShell
source venv/bin/activate        # Mac/Linux

# DEACTIVATE
deactivate

# VERIFY ACTIVE
which python                    # Mac/Linux
where python                    # Windows
# Should show path inside venv folder
```

---

## pip — Package Manager

```bash
pip install package_name        # Install package
pip install package==version    # Install specific version
pip uninstall package           # Remove package
pip list                        # List installed packages
pip show package                # Details about a package
pip freeze                      # All packages with versions
pip freeze > requirements.txt   # Save to file
pip install -r requirements.txt # Install from file
pip install --upgrade package   # Upgrade package
```

---

## Git

```bash
# SETUP (one time only)
git config --global user.name "Your Name"
git config --global user.email "email@example.com"

# START
git init                        # New repository
git clone URL                   # Copy existing repository

# DAILY WORKFLOW
git status                      # What changed?
git diff                        # What exactly changed?
git add filename                # Stage one file
git add .                       # Stage all changes
git commit -m "message"         # Commit with message
git log                         # Full history
git log --oneline               # Compact history

# BRANCHES
git branch                      # List branches
git switch -c branch-name       # Create and switch
git switch main                 # Switch to main
git merge branch-name           # Merge into current

# REMOTE (GitHub etc.)
git remote add origin URL       # Link to remote
git push -u origin main         # First push
git push                        # Subsequent pushes
git pull                        # Get remote changes
```

---

## VS Code Shortcuts

```
ESSENTIAL:
Ctrl + `          Open/close terminal
Ctrl + Shift + P  Command palette
Ctrl + P          Quick open file
Ctrl + S          Save file
Ctrl + Z          Undo

EDITING:
Ctrl + /          Toggle comment
Alt + Up/Down     Move line up/down
Ctrl + D          Select next match
Ctrl + Shift + K  Delete line
Tab / Shift+Tab   Indent / outdent

RUNNING PYTHON:
Right-click → "Run Python File in Terminal"
F5            Run with debugger
```

---

## Standard Project Structure

```
my-project/
├── .gitignore          ← Always have this
├── README.md           ← Always have this
├── requirements.txt    ← Generated with pip freeze
├── venv/               ← Never commit this
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
└── docs/
    └── usage.md
```

---

## .gitignore Template

```
# Virtual Environment
venv/
env/
.venv/

# Python Cache
__pycache__/
*.pyc
*.pyo

# Secrets
.env
secrets.py

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## Troubleshooting Quick Fixes

| Problem | Fix |
|---------|-----|
| `python` not found | Reinstall Python, check "Add to PATH" |
| `pip` not found | `python -m pip install pip` |
| `venv` activation fails (Windows) | Run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Can't open file in VS Code | `code filename.py` from terminal |
| Git "not a repository" error | Run `git init` first |
| Forgot to activate venv | Run activation command, then `pip list` to confirm |
