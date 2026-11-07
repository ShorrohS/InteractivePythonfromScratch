# Phase 00 — Completion Assessment

> Complete this assessment before moving to Phase 01.
> Pass mark: 80% (12/15 correct)
> Time: 20 minutes (no reference materials)

---

## PART A: Practical Tasks (Complete these actions)

**Task 1.** Open your terminal and run the following. Write down the exact output you see:

```bash
python --version
pip --version
```

Your output:
```
Python: _______________
pip:    _______________
```

---

**Task 2.** Using only the terminal, create this structure and confirm it exists:

```
assessment-workspace/
├── src/
│   └── main.py
└── tests/
```

Write the commands you used:
```bash



```

---

**Task 3.** Set up a virtual environment inside `assessment-workspace/`, activate it, install `requests`, and generate a `requirements.txt`.

Write every command:
```bash



```

---

**Task 4.** Initialise a git repository in `assessment-workspace/`, stage all files (except venv), and make a commit with message `"Assessment workspace setup"`.

Write every command:
```bash



```

---

## PART B: Concept Questions

**Q5.** What does `PATH` mean in operating systems, and why does adding Python to PATH matter?

Answer:
```



```

---

**Q6.** Describe in your own words what a virtual environment is, using an analogy that is NOT the one from the lessons.

Answer:
```



```

---

**Q7.** What command shows you which Python executable is being used (i.e. whether your virtual environment Python or system Python is active)?

```bash
# Windows:

# Mac/Linux:
```

---

**Q8.** A teammate says: "Just commit the venv folder — it saves time setting up." Give three reasons why this is wrong.

1.
2.
3.

---

**Q9.** What are the THREE types of errors Git uses to track files? Describe each in one line.

1. (Untracked)
2. (Modified)
3. (Staged)

---

**Q10.** Write the `.gitignore` content needed for a standard Python project (minimum 5 entries):

```
# My .gitignore



```

---

## PART C: Scenario Questions

**Q11.** You clone a repository. When you run `python main.py` you get `ModuleNotFoundError: No module named 'flask'`. What are the two most likely causes?

1.
2.

---

**Q12.** You made 3 commits locally but haven't pushed. Your internet is down. Can you still work with git? What commands can you still use?

Answer:
```



```

---

**Q13.** What is the difference between `git add .` and `git add filename.py`? When should you use each?

Answer:
```



```

---

**Q14.** You accidentally typed `rm -rf venv/` and deleted your virtual environment. How do you recover? (No backup exists.)

Answer:
```



```

---

**Q15.** A developer creates an `.env` file containing:
```
DATABASE_PASSWORD=supersecret123
API_KEY=abc123xyz
```
They forget to add `.env` to `.gitignore` and push to GitHub. What should they do immediately?

Answer:
```



```

---

## Scoring Guide

| Score | Result |
|-------|--------|
| 13-15 | Excellent — move to Phase 01 immediately |
| 11-12 | Good — review weak areas, then proceed |
| 8-10  | Review Phase 00 lessons and retry |
| < 8   | Re-read all lessons before continuing |

---

## Self-Assessment Checklist

Before moving to Phase 01, confirm every box:

- [ ] I can open a terminal without help
- [ ] I can navigate folders using cd, ls/dir, pwd
- [ ] I can create folders and files from the terminal
- [ ] python --version works and shows Python 3.x
- [ ] I can create, activate, and deactivate a virtual environment
- [ ] I can install packages with pip inside a venv
- [ ] I know what requirements.txt is and how to generate it
- [ ] I have made at least one git commit
- [ ] I understand why venv/ and .env go in .gitignore
- [ ] VS Code opens .py files with syntax highlighting
