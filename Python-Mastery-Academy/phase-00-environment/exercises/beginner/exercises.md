# 📝 Phase 00 — Beginner Exercises

> **Rules:**
> - Attempt every question before checking solutions
> - All answers are in `../../solutions/beginner/solutions.md`
> - Write your answers on paper or in a text file first

---

## Section A: Concept Questions (No coding required)

**Q1.** In your own words, what is a program? Write 2-3 sentences.

---

**Q2.** Match each hardware component to its description:

| Component | Description |
|-----------|-------------|
| CPU | A. Permanent storage that survives shutdown |
| RAM | B. Processes and executes instructions |
| SSD/HDD | C. Temporary memory cleared when powered off |

---

**Q3.** Is Python compiled or interpreted? Explain what that means in one sentence.

---

**Q4.** Fill in the blanks:

```
When you run: python hello.py

1. Python reads the .py file from _____________
2. The code is loaded into _____________
3. The Python Interpreter translates each line and sends it to the _____________
4. Output is displayed on the _____________
```

---

**Q5.** What happens to a Python variable when the program finishes running?

```
A) It is saved to the hard drive
B) It is lost from memory
C) It stays in RAM forever
D) It is sent to the CPU
```

---

## Section B: Terminal Commands

**Q6.** Write the terminal command to:

a) Show your current directory  
b) Navigate to a folder called `projects` on the Desktop  
c) Create a new folder called `python-practice`  
d) List all files in the current folder  
e) Go back to the parent folder  

---

**Q7.** You are in folder `/Users/alice/Documents`.
What does each command do?

```bash
cd ..
```
→ Goes to: _______________

```bash
cd projects/phase-01
```
→ Goes to: _______________

```bash
cd ~
```
→ Goes to: _______________

---

**Q8.** Look at this terminal session:

```bash
C:\Users\Alice> mkdir learning
C:\Users\Alice> cd learning
C:\Users\Alice\learning> mkdir python
C:\Users\Alice\learning> cd python
C:\Users\Alice\learning\python> pwd
```

What will `pwd` output?

---

## Section C: Virtual Environments

**Q9.** Put these virtual environment steps in the correct order:

```
A. pip install requests
B. python -m venv venv
C. mkdir my-project && cd my-project
D. source venv/bin/activate
E. pip freeze > requirements.txt
```

Correct order: ___, ___, ___, ___, ___

---

**Q10.** Why should you NEVER commit the `venv/` folder to Git?

Select all that apply:
```
A) It's very large (hundreds of MB)
B) It's machine-specific (won't work on other computers)
C) It might contain passwords
D) GitHub doesn't allow Python files
```

---

## Section D: Git

**Q11.** What is the difference between `git add` and `git commit`?

Write your explanation:
```

```

---

**Q12.** What does each Git command do?

| Command | What it does |
|---------|-------------|
| `git init` | |
| `git status` | |
| `git add .` | |
| `git commit -m "message"` | |
| `git log` | |

---

**Q13.** Arrange these Git commands in the correct order to save your first Python file:

```
A. git commit -m "Add first Python file"
B. git add hello.py
C. git init
D. # (create hello.py)
```

Correct order: ___, ___, ___, ___

---

**Q14.** Write a better commit message for each bad one:

Bad: `"fix"`  
Better: _______________

Bad: `"stuff"`  
Better: _______________

Bad: `"changes"`  
Better: _______________

---

**Q15.** What file tells Git which files to ignore?

```
A) .gitconfig
B) .gitignore
C) .gitexclude
D) ignore.txt
```

---

## Section E: Practical Tasks

**Q16.** Open your terminal and do this. Write what you see:

```bash
python --version
```

Your output: _______________

```bash
pip --version
```

Your output: _______________

---

**Q17.** Create this folder structure using ONLY the terminal:

```
my-academy/
├── phase-00/
│   ├── notes.txt
│   └── hello.py
└── phase-01/
    └── notes.txt
```

Write the exact commands you used:

```bash
# Write your commands here:

```

---

**Q18.** Complete this `.gitignore` file by adding the missing entries:

```
# Add virtual environment folder
_____________

# Add Python cache folder  
_____________

# Add the .env file for secrets
_____________
```

---

## Bonus Questions

**Q19.** What is the keyboard shortcut in VS Code to:

a) Open the terminal: _______________  
b) Open the command palette: _______________  
c) Comment/uncomment a line: _______________  

---

**Q20.** Explain the difference between these two paths:

```
Absolute: C:\Users\Alice\Desktop\project\main.py
Relative: project\main.py
```

When would you use each?

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
>
> Only open this file after attempting all questions.
