# Phase 00 — Intermediate Exercises

> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

## Section A: Advanced Terminal (Q1–Q5)

**Q1.** From the terminal only (no File Explorer), create this full structure in one session:

```
dev-workspace/
├── projects/
│   ├── python/
│   └── web/
├── notes/
└── archive/
```

Write every command you used in order.

---

**Q2.** You are inside `C:\Users\YourName\Documents`. Write a single command to create a folder called `2024-backup` on your Desktop without navigating away from Documents.

---

**Q3.** You have these files in a folder:
```
report_jan.txt   report_feb.txt   report_mar.txt
data_jan.csv     data_feb.csv     notes.md
```
Write terminal commands to:
- Move all `.txt` files into a new subfolder called `reports/`
- Move all `.csv` files into a new subfolder called `data/`
- Leave `notes.md` where it is

---

**Q4.** What does each of these do? Explain in one sentence each:
```bash
cd ~
cd -
pwd
ls -la
rm -rf folder/
```

---

**Q5.** You ran a Python file and got this error:
```
python: The term 'python' is not recognized...
```
List three possible causes and how to fix each one.

---

## Section B: Virtual Environments — Deeper (Q6–Q8)

**Q6.** Explain what happens step by step when you run `pip install requests` inside an active virtual environment. Where does the package go physically on disk?

---

**Q7.** A colleague shares a Python project with you. The repo contains:
```
my-project/
├── main.py
├── requirements.txt
└── README.md
```
There is NO `venv/` folder. Write every terminal command to get this project running on your machine from clone to execution.

---

**Q8.** What is the difference between these two commands?
```bash
pip freeze > requirements.txt
pip list
```
When would you use each?

---

## Section C: Git — Branching & Workflow (Q9–Q12)

**Q9.** You are working on a project and want to add a new feature without breaking the main code. Write the full Git workflow:
- Create a branch called `feature-login`
- Make a commit on that branch
- Switch back to main
- Merge the feature branch
- Delete the feature branch

---

**Q10.** What does `git log --oneline --graph --all` show? When is it useful?

---

**Q11.** You committed a file with a typo in the commit message. The commit has NOT been pushed. How do you fix the message?

---

**Q12.** Explain the difference between these two scenarios:
```bash
# Scenario A
git add .
git commit -m "all changes"

# Scenario B
git add login.py
git commit -m "Add login validation function"
git add dashboard.py
git commit -m "Add dashboard route"
```
Which is better practice and why?

---

## Section D: Project Structure & Config (Q13–Q15)

**Q13.** You need a Python project that:
- Has a virtual environment
- Tracks dependencies
- Is under version control
- Has a `.gitignore` that excludes `venv/`, `__pycache__/`, and `.env`

Write every command and file creation step needed from scratch.

---

**Q14.** Look at this `.gitignore`:
```
venv/
*.pyc
.env
```
Which of the following files will Git ignore?
```
venv/lib/python3.12/site.py
main.pyc
config.env
.env
settings.py
__pycache__/utils.cpython-312.pyc
```

---

**Q15.** Why should secrets (API keys, passwords) never be committed to Git even in a private repository?

---

> **Solutions:** `../../solutions/intermediate/solutions.md`
