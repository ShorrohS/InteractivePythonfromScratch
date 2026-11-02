# 📋 Phase 00 — Quiz 01

**Time:** ~15 minutes  
**Questions:** 15  
**Pass Score:** 12/15  

> Answer each question before checking. Answers at the bottom (no peeking!).

---

## Section 1: Multiple Choice

**Q1.** What does RAM stand for and what is it used for?

```
A) Remote Access Memory — stores files permanently
B) Random Access Memory — temporary working memory
C) Read And Memorize — CPU instruction cache
D) Rapid Application Memory — stores installed programs
```

**Q2.** Which command verifies Python is installed correctly?

```
A) python install --check
B) verify python
C) python --version
D) python -check
```

**Q3.** What does the `cd ..` command do?

```
A) Creates a directory called ".."
B) Deletes the current directory
C) Moves up one level to the parent directory
D) Changes directory to the root
```

**Q4.** Which of these is the correct way to activate a virtual environment on Windows PowerShell?

```
A) venv/activate
B) source venv/bin/activate
C) venv\Scripts\Activate.ps1
D) activate venv
```

**Q5.** What does `pip freeze > requirements.txt` do?

```
A) Checks if requirements are met
B) Saves the list of all installed packages and versions to a file
C) Installs all packages listed in requirements.txt
D) Deletes all packages
```

**Q6.** Which file tells Git to ignore certain files?

```
A) .gitconfig
B) .gitignore
C) .gitskip
D) ignore.list
```

**Q7.** What is the correct order of operations in the Git workflow?

```
A) commit → add → push → status
B) status → add → commit → push
C) add → commit → status → push
D) push → commit → add → status
```

**Q8.** What does `git log --oneline` show?

```
A) The most recent commit only
B) A compact list of all commits
C) Just the commit IDs
D) Only unpushed commits
```

---

## Section 2: True / False

**Q9.** You should commit the `venv/` folder to Git so your teammates can use it.

```
True / False
```

**Q10.** Python is an interpreted language, meaning it runs code line by line.

```
True / False
```

**Q11.** You must activate a virtual environment before installing packages with pip.

```
True / False
```

**Q12.** `git add .` stages all changed files in the current directory.

```
True / False
```

---

## Section 3: Fill in the Blank

**Q13.** Complete the command to create a virtual environment called `venv`:

```bash
python ___ venv venv
```

**Q14.** To go back to the parent directory in the terminal, use:

```bash
cd ___
```

**Q15.** A good commit message should be:

```
A) "fix"
B) Short but descriptive, explaining what changed
C) A random word
D) The same as the last commit
```

---

## Answers (Don't peek until finished!)

.

.

.

.

.

.

.

.

.

.

---

## ✅ Answer Key

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | B | RAM = Random Access Memory, temporary, cleared on shutdown |
| 2 | C | `python --version` prints the installed Python version |
| 3 | C | `cd ..` navigates to the parent folder |
| 4 | C | Windows PowerShell uses `venv\Scripts\Activate.ps1` |
| 5 | B | `pip freeze > file` saves the current package list |
| 6 | B | `.gitignore` specifies files Git should not track |
| 7 | B | status → add → commit → push is the correct flow |
| 8 | B | Shows all commits in compact one-line format |
| 9 | False | `venv/` is machine-specific and large — use `requirements.txt` instead |
| 10 | True | Python interprets and runs code line by line |
| 11 | True | Must activate first so pip installs into the venv |
| 12 | True | `.` means all files in current directory |
| 13 | `-m` | `python -m venv venv` |
| 14 | `..` | `cd ..` |
| 15 | B | Descriptive commit messages help everyone understand history |

---

## Score

- **15/15** — Perfect! You're ready for Phase 01.
- **12-14/15** — Great! Review any wrong answers then proceed.
- **9-11/15** — Good, but re-read the lessons you struggled with.
- **< 9/15** — Re-read Phase 00 concepts before continuing.

---

**→ Next: [Phase 01 — Python Fundamentals](../../phase-01-fundamentals/README.md)**
