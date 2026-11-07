# Phase 00 — Advanced Exercises

> These are real-world scenario challenges. Think carefully before answering.
> Solutions: `../../solutions/advanced/solutions.md`

---

## Challenge 1 — Automate Project Setup

Write a shell script (or sequence of terminal commands) that:

1. Creates a new Python project folder with the name passed as an argument
2. Initialises a git repository
3. Creates a virtual environment
4. Creates the files: `main.py`, `README.md`, `.gitignore`, `requirements.txt`
5. Populates `.gitignore` with standard Python entries
6. Makes the first commit with message `"Initial project setup"`

Example usage:
```bash
./setup-project.sh my-new-app
```

Write the script step by step and explain what each section does.

---

## Challenge 2 — Git Disaster Recovery

You are working on a project with this git history:

```
a1b2c3 (HEAD -> main) Accidentally committed passwords.txt
d4e5f6 Add database module
g7h8i9 Initial commit
```

Tasks:
1. How do you remove `passwords.txt` from the latest commit (it hasn't been pushed)?
2. If it WAS pushed to GitHub, what must you do?
3. What should you do to prevent this from happening again?

---

## Challenge 3 — Dependency Conflict

You inherit a Python project with this `requirements.txt`:
```
requests==2.28.0
flask==2.1.0
```

When you run `pip install -r requirements.txt`, you get:
```
ERROR: flask 2.1.0 requires Werkzeug>=2.0, but you have Werkzeug 1.0.1
```

Explain:
1. Why this error occurs
2. Three ways to resolve it
3. How virtual environments prevent this problem spreading to other projects

---

## Challenge 4 — Multi-Environment Setup

A professional Python project often has THREE environments:
- Development (local machine)
- Staging (test server)
- Production (live server)

Design a file structure and explain how you would manage:
1. Different `requirements.txt` for dev vs production
2. Different environment variables for each environment
3. Ensuring production secrets never end up in the dev environment

---

## Challenge 5 — Terminal Scripting

Write a sequence of terminal commands that:
1. Searches for all `.py` files in a folder recursively
2. Counts how many there are
3. Prints their full paths
4. Creates a file called `python_files.txt` containing all the paths

Use only terminal commands (no Python code).

---

> **Solutions:** `../../solutions/advanced/solutions.md`
