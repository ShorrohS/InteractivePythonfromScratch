# Lesson 06 — Git Fundamentals

**Phase:** 00 — Environment Setup
**Time:** ~45 minutes
**Prerequisite:** Terminal competency (Lesson 04)

---

## Part 1: What is Git?

Git is a **version control system** — it tracks every change you make to your code.

```
WITHOUT GIT:
  my_project_v1.py
  my_project_v2.py
  my_project_FINAL.py
  my_project_FINAL_REAL.py
  my_project_FINAL_REAL_v2.py
  (sound familiar?)

WITH GIT:
  my_project.py     ← only ONE file
  Git remembers every version automatically
  You can go back to any version at any time
```

---

## Part 2: Why Git Matters

```
BACKUP          → Your code is safe even if you delete files
HISTORY         → See every change ever made
COLLABORATION   → Multiple developers work on the same code
BRANCHING       → Try new features without breaking working code
DEPLOYMENT      → Most deployment systems use Git
PROFESSIONALISM → Every tech company uses Git
```

---

## Part 3: Installing Git

### Windows

Download from: **https://git-scm.com/download/win**

Run the installer (accept defaults).

After installation, verify:
```bash
git --version
```

### macOS

```bash
git --version
# If not installed, macOS will prompt to install Xcode Command Line Tools
```

Or with Homebrew:
```bash
brew install git
```

### Linux (Ubuntu/Debian)

```bash
sudo apt install git
```

---

## Part 4: First-Time Git Configuration

Run these ONCE after installing Git:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Verify:
```bash
git config --list
```

These details appear in every commit you make.

---

## Part 5: Core Git Concepts

```
REPOSITORY (repo)
  A folder tracked by Git.
  Contains all your files + Git's hidden .git folder

COMMIT
  A snapshot of your code at a specific moment.
  Like a save point in a video game.
  Has: message, timestamp, author, unique ID

WORKING DIRECTORY
  Files you're currently editing

STAGING AREA (Index)
  Files you've selected for the next commit
  Like a "waiting room" before committing

BRANCH
  An independent line of development
  Default branch: main (or master)

REMOTE
  A version of your repo hosted online (GitHub, GitLab, Bitbucket)
```

---

## Part 6: The Git Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    GIT WORKFLOW                             │
│                                                             │
│  WORKING DIRECTORY          STAGING AREA        REPOSITORY │
│  ──────────────────         ─────────────        ───────── │
│  Files you edit             Selected files       Committed  │
│                             for next commit      snapshots  │
│                                                             │
│  Edit files                                                 │
│      │                                                      │
│      ▼                                                      │
│  git add filename ────────► File appears here               │
│                                   │                         │
│                                   ▼                         │
│                             git commit ──────────► New      │
│                             -m "message"           commit   │
│                                                   saved     │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 7: Essential Git Commands

### `git init` — Initialize a Repository

```bash
cd my-project
git init
```

Output:
```
Initialized empty Git repository in /path/my-project/.git/
```

This creates a hidden `.git` folder. Never delete it.

---

### `git status` — Check Current State

```bash
git status
```

Output (when files have changed):
```
On branch main

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        hello.py
        README.md
```

Run this constantly. It tells you everything.

---

### `git add` — Stage Files

```bash
# Stage a specific file
git add hello.py

# Stage multiple files
git add hello.py README.md

# Stage all changed files in current directory
git add .

# Stage all changed files in entire project
git add -A
```

After `git add`:
```
Changes to be committed:
        new file:   hello.py
```

---

### `git commit` — Save a Snapshot

```bash
git commit -m "Add hello world program"
```

The `-m` flag adds a commit message. Always write meaningful messages:

```bash
# GOOD commit messages:
git commit -m "Add user login function"
git commit -m "Fix bug in expense calculation"
git commit -m "Add CSV export feature"
git commit -m "Update README with setup instructions"

# BAD commit messages:
git commit -m "fix"
git commit -m "stuff"
git commit -m "asdfgh"
git commit -m "changes"
```

---

### `git log` — View History

```bash
git log
```

Output:
```
commit a3f1b2c (HEAD -> main)
Author: Your Name <email@example.com>
Date:   Mon Jan 1 10:00:00 2024

    Add hello world program

commit 9e8d7c6
Author: Your Name <email@example.com>
Date:   Mon Jan 1 09:30:00 2024

    Initial commit
```

Compact view:
```bash
git log --oneline
```

Output:
```
a3f1b2c Add hello world program
9e8d7c6 Initial commit
```

---

### `git diff` — See Changes

```bash
# See unstaged changes
git diff

# See staged changes
git diff --staged
```

---

### `git branch` — Work with Branches

```bash
# List branches
git branch

# Create new branch
git branch feature-login

# Switch to branch
git checkout feature-login
# Or (modern syntax):
git switch feature-login

# Create and switch in one command
git checkout -b feature-login
git switch -c feature-login   # modern

# Delete branch (after merging)
git branch -d feature-login
```

---

### `git merge` — Combine Branches

```bash
# Switch to main branch first
git checkout main

# Merge feature branch into main
git merge feature-login
```

---

### Remote Repository Commands

```bash
# Connect to remote (GitHub, etc.)
git remote add origin https://github.com/username/repo.git

# Push to remote
git push -u origin main   # First time
git push                  # Subsequent times

# Pull from remote
git pull

# Clone a repository
git clone https://github.com/username/repo.git
```

---

## Part 8: First Project — Complete Git Workflow

Follow these steps exactly:

```bash
# 1. Create project folder
mkdir my-first-git-project
cd my-first-git-project

# 2. Initialize git
git init

# 3. Create a Python file
# Windows:
New-Item hello.py

# 4. Write content to hello.py (open in VS Code and type this)
# print("Hello from my first Git project!")
# code .

# 5. Check status
git status
# Should show: Untracked files: hello.py

# 6. Stage the file
git add hello.py

# 7. Check status again
git status
# Should show: Changes to be committed: hello.py

# 8. Make first commit
git commit -m "Initial commit: add hello world"

# 9. View history
git log --oneline
# Should show 1 commit

# 10. Make a change — open hello.py, add a new line:
# print("Git is tracking this change!")

# 11. Check status
git status
# Shows: modified: hello.py

# 12. See what changed
git diff

# 13. Stage and commit the change
git add hello.py
git commit -m "Add second greeting line"

# 14. View history
git log --oneline
# Shows 2 commits
```

---

## Part 9: .gitignore

Tell Git which files to ignore:

```
# .gitignore file

# Virtual environment
venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/

# Secrets (IMPORTANT!)
.env
secrets.py
config_private.py

# OS files
.DS_Store      # macOS
Thumbs.db      # Windows
```

Create it:
```bash
New-Item .gitignore   # Windows
touch .gitignore      # Mac/Linux
```

---

## Part 10: Professional Git Habits

```
1. Commit early, commit often
   Small, frequent commits are better than one giant commit.

2. Write meaningful commit messages
   Your future self will thank you.

3. Never commit secrets
   API keys, passwords, database credentials → use .env files

4. Use branches for new features
   Never develop directly on main.

5. Review changes before committing
   Run git diff and git status before every commit.

6. Keep .gitignore updated
   Add files you don't want to track before they accidentally commit.
```

---

## Common Git Mistakes

| Mistake | Fix |
|---------|-----|
| Committed to wrong branch | `git cherry-pick` or `git reset` |
| Forgot to add a file | `git add file && git commit --amend` |
| Committed secrets | Remove from git history (complex) — don't commit them! |
| Want to undo last commit | `git reset HEAD~1` (keeps changes) |
| Want to discard all changes | `git checkout -- .` (careful!) |

---

## Git Cheat Sheet

```
SETUP:
  git config --global user.name "Name"
  git config --global user.email "email"

START:
  git init              Create new repo
  git clone URL         Copy existing repo

EVERYDAY:
  git status            What changed?
  git add file          Stage a file
  git add .             Stage all changes
  git commit -m "msg"   Save a snapshot
  git log --oneline     View history

BRANCHES:
  git branch             List branches
  git switch -c name     Create + switch
  git switch main        Switch to main
  git merge feature      Merge into current

REMOTE:
  git push               Upload commits
  git pull               Download updates
```

---

## Next

You have completed all Phase 00 concepts.

**→ [Guided Project 01: First Python Project](../guided-projects/project-01-first-python-project/README.md)**
