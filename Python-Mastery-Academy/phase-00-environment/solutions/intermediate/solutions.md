# Phase 00 — Intermediate Exercise Solutions

> Stop! Have you attempted the questions first?
> File: `../../exercises/intermediate/exercises.md`

---

## A1. Creating folder structure

```bash
mkdir dev-workspace
cd dev-workspace
mkdir projects notes archive
cd projects
mkdir python web
cd ../..
```

Verify:
```bash
ls -R dev-workspace    # Mac/Linux
dir /s dev-workspace   # Windows
```

---

## A2. Create folder without navigating

```bash
# You're in Documents, creating folder on Desktop:
mkdir C:\Users\YourName\Desktop\2024-backup    # Windows
mkdir ~/Desktop/2024-backup                     # Mac/Linux
```

The key: use an **absolute path** — no need to `cd` first.

---

## A3. Organise files by type

```bash
mkdir reports data

# Move .txt files (Mac/Linux)
mv report_jan.txt report_feb.txt report_mar.txt reports/

# Move .csv files
mv data_jan.csv data_feb.csv data/

# Windows PowerShell equivalent:
Move-Item report_*.txt reports/
Move-Item data_*.csv data/
```

---

## A4. Command explanations

| Command | What it does |
|---------|-------------|
| `cd ~` | Navigate to your home directory |
| `cd -` | Go back to the previous directory |
| `pwd` | Print current working directory |
| `ls -la` | List all files (including hidden) with permissions and sizes |
| `rm -rf folder/` | Recursively and forcefully delete a folder and all its contents (irreversible!) |

---

## A5. Python not recognised — causes and fixes

**Cause 1: Python not installed**
Fix: Download from python.org and install

**Cause 2: Python not in PATH**
Fix: Reinstall Python, check "Add Python to PATH" during installation

**Cause 3: Wrong command for your OS**
Fix: Try `python3` instead of `python` (common on macOS/Linux)

Verification:
```bash
where python      # Windows
which python3     # Mac/Linux
```

---

## B6. Where pip installs packages

When you run `pip install requests` inside an active venv:

1. pip downloads `requests` from PyPI (Python Package Index)
2. Extracts it to: `venv/Lib/site-packages/requests/` (Windows) or `venv/lib/python3.x/site-packages/requests/` (Mac/Linux)
3. Also installs its dependencies (certifi, charset-normalizer, idna, urllib3)
4. Records the installation in `venv/Lib/site-packages/requests-x.x.x.dist-info/`

The package is **isolated** — only this venv can see it.

---

## B7. Setting up a project without venv folder

```bash
# 1. Clone the repository
git clone https://github.com/colleague/my-project.git
cd my-project

# 2. Create your own virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\Activate.ps1          # Windows PowerShell
source venv/bin/activate            # Mac/Linux

# 4. Install dependencies from requirements.txt
pip install -r requirements.txt

# 5. Verify everything installed
pip list

# 6. Run the project
python main.py
```

---

## B8. pip freeze vs pip list

| Command | Output | Use case |
|---------|--------|---------|
| `pip list` | Human-readable table of packages and versions | Checking what's installed |
| `pip freeze` | Machine-readable `package==version` format | Generating `requirements.txt` |

```bash
# Use pip list when:
pip list              # just want to see what's installed

# Use pip freeze when:
pip freeze > requirements.txt    # saving for teammates to recreate your environment
```

---

## C9. Full Git branching workflow

```bash
# 1. Create and switch to new branch
git switch -c feature-login

# 2. Make some changes, then commit
# (edit files first)
git add login.py
git commit -m "Add user login validation"

# 3. Switch back to main
git switch main

# 4. Merge feature branch
git merge feature-login

# 5. Delete the branch (clean up)
git branch -d feature-login

# 6. Verify it's gone
git branch
```

---

## C10. git log --oneline --graph --all

Shows a visual tree of ALL branches and their commit history:
```
* a3f1b2c (HEAD -> main) Add README
* 9e8d7c6 (feature-login) Add login module
| * b4c5d6e (feature-dashboard) Add dashboard
|/
* 7f8g9h0 Initial commit
```

Useful when: working with multiple branches and you want to see how they relate.

---

## C11. Fix last commit message (not yet pushed)

```bash
git commit --amend -m "Correct commit message here"
```

**Important:** Only use `--amend` on commits that have NOT been pushed. Amending a pushed commit rewrites history and causes problems for teammates.

---

## C12. Commit granularity — Scenario B is better

**Scenario A** is bad because:
- One commit contains unrelated changes
- If you need to undo a change, you lose everything
- Future developers can't understand what changed why

**Scenario B** is professional because:
- Each commit is a single logical change
- Easy to revert one feature without affecting others
- History tells a story: "who added what and why"
- Makes code review much easier

**Rule:** Each commit should answer: *"What one thing did I change and why?"*

---

## D13. Full project setup from scratch

```bash
# 1. Create project folder
mkdir my-project && cd my-project

# 2. Initialise git
git init

# 3. Create virtual environment
python -m venv venv

# 4. Create .gitignore BEFORE first commit
New-Item .gitignore    # Windows
touch .gitignore       # Mac/Linux

# 5. Add these lines to .gitignore:
# venv/
# __pycache__/
# .env
# *.pyc

# 6. Create project files
New-Item main.py README.md requirements.txt

# 7. Activate venv
venv\Scripts\Activate.ps1

# 8. Make first commit (with .gitignore in place!)
git add .gitignore README.md main.py requirements.txt
git commit -m "Initial project setup"
```

---

## D14. Which files does .gitignore ignore?

```
venv/lib/python3.12/site.py          ← YES (matches venv/)
main.pyc                              ← YES (matches *.pyc)
config.env                            ← NO  (.env matches exact name, not suffix)
.env                                  ← YES (exact match)
settings.py                           ← NO  (normal .py file, not .pyc)
__pycache__/utils.cpython-312.pyc    ← YES (matches *.pyc AND the folder is usually ignored too)
```

To also ignore `config.env`, add `*.env` to `.gitignore`.

---

## D15. Why secrets should never be committed

Even in a private repository:

1. **Access can be breached** — if your GitHub account is compromised, all repos are exposed
2. **Git history is permanent** — even if you delete the file later, it lives in git history forever
3. **Accidental visibility** — private repos can accidentally be made public
4. **Team members** — everyone with repo access sees the secrets
5. **Third-party services** — GitHub, CI/CD tools scan for committed secrets automatically and will alert you

**Correct approach:**
```
Store secrets in .env files → load with python-dotenv
Add .env to .gitignore
Share secrets securely (password manager, encrypted chat)
Provide .env.example with placeholder values
```
