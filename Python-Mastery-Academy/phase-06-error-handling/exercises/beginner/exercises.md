# Phase 06 — Beginner Exercises: Error Handling

---

**Q1.** Write a function `safe_divide(a, b)` that returns `a / b` or prints an error and returns `None` if b is zero.

---

**Q2.** Write a loop that asks for a number, keeps asking if the user types non-numeric text, stops when they type 'quit'.

---

**Q3.** What is the output?
```python
try:
    x = int("hello")
except ValueError:
    print("ValueError caught")
except Exception:
    print("Exception caught")
finally:
    print("Done")
```

---

**Q4.** Write a function `read_file_safe(filename)` that returns file contents or an empty string if the file doesn't exist.

---

**Q5.** What is wrong?
```python
try:
    result = 10 / 2
except:
    print("error")
print(result)
```

---

**Q6.** Write a function `to_float(value, default=0.0)` that converts value to float or returns the default on error.

---

**Q7.** What is the difference between:
```python
raise ValueError("bad input")
```
and:
```python
raise
```

---

**Q8.** Write code that tries to open "data.txt", and if it doesn't exist, creates it with "Created fresh".

---

**Q9.** Write a function `validate_score(score)` that raises `ValueError` with a descriptive message if score is not 0–100.

---

**Q10.** What does the `finally` block do? Write an example where it's important.

---

> **Solutions:** `../../solutions/beginner/solutions.md`
