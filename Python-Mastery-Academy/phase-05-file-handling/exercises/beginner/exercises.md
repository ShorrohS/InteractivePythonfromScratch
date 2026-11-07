# Phase 05 — Beginner Exercises: File Handling

> Attempt all before checking solutions.
> Solutions: `../../solutions/beginner/solutions.md`

---

**Q1.** Write a program that creates a file called `hello.txt`, writes "Hello, World!" to it, then reads it back and prints the content.

---

**Q2.** Write a program that appends 5 lines (numbered) to a file called `log.txt`. Then read the file and print the total line count.

---

**Q3.** What is the output of this code and what mistake does it contain?
```python
with open("data.txt", "r") as f:
    f.write("Hello")
```

---

**Q4.** Write a function `file_exists(filename)` that returns `True` if the file exists, `False` otherwise.

---

**Q5.** Write a program that reads a list of names from `names.txt` (one per line) and prints them in alphabetical order. Create the file first.

---

**Q6.** Write a function `count_lines(filename)` that returns the number of lines in a text file.

---

**Q7.** What is the difference between:
```python
open("file.txt", "w")
open("file.txt", "a")
```

---

**Q8.** Write a function `save_list(filename, items)` that writes a list of strings to a file, one per line.

---

**Q9.** Write a function `load_list(filename)` that reads a file and returns a list of stripped lines.

---

**Q10.** What is wrong?
```python
f = open("data.txt", "r")
content = f.read()
# (forgot to close)
```
How do you fix it using `with`?

---

> **Solutions:** `../../solutions/beginner/solutions.md`
