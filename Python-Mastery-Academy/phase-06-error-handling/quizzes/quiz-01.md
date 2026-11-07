# Phase 06 — Quiz 01: Error Handling

**Questions:** 15 | **Pass:** 12/15 | **Time:** 15 min

---

**Q1.** What does a `try` block do?
`A) Prevents errors  B) Wraps code that might raise an exception  C) Logs errors  D) Checks types`

**Q2.** What does an `except` block do?
`A) Runs after try  B) Handles a specific exception type if it occurred  C) Catches all prints  D) Required with every try`

**Q3.** What does `finally` guarantee?
`A) The try block runs  B) The code runs only on error  C) The code ALWAYS runs (error or not)  D) Variables are cleaned up`

**Q4.** When does the `else` block run in try/except?
`A) Always  B) Only on error  C) Only if NO exception occurred  D) After finally`

**Q5.** Which exception type should you catch for `int("hello")`?
`A) TypeError  B) ValueError  C) AttributeError  D) InputError`

**Q6.** How do you access the exception message?
`A) except Error.message  B) except Error as e: print(e)  C) catch(e)  D) error.text`

**Q7.** What does `raise` with no arguments do?
`A) Raises a new exception  B) Re-raises the current exception  C) Clears the error  D) Logs the error`

**Q8.** What is a custom exception?
`A) A Python built-in  B) A class that inherits from Exception  C) A function that raises errors  D) A decorator`

**Q9.** What does `except (ValueError, TypeError):` do?
`A) Catches ValueError OR TypeError  B) Catches ValueError AND TypeError together  C) SyntaxError  D) Only works for ValueError`

**Q10.** Why is bare `except:` considered bad practice?
`A) It's too verbose  B) It catches everything including KeyboardInterrupt, hiding bugs  C) It's slow  D) It requires finally`

**Q11.** What is the output?
```python
try:
    print("A")
    raise ValueError
    print("B")
except ValueError:
    print("C")
print("D")
```
`A) A B C D  B) A C D  C) A D  D) C D`

**Q12.** What is defensive programming?
`A) Writing code without errors  B) Writing code that anticipates and handles failures gracefully  C) Using many try/except blocks  D) Avoiding user input`

**Q13.** Which is the correct exception hierarchy (parent → child)?
`A) ValueError → Exception → LookupError  B) Exception → LookupError → KeyError  C) KeyError → Exception → BaseException  D) TypeError → ValueError → Exception`

**Q14.** What should you always do when catching an exception silently?
`A) Nothing, it's fine  B) Log the error at minimum  C) Re-raise it  D) Print the traceback`

**Q15.** What does `raise ValueError("msg") from original_error` do?
`A) Raises two errors  B) Chains the new error to the original (exception chaining)  C) Converts the original error  D) Suppresses the original error`

---

## Answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | B | 6 | B | 11 | B |
| 2 | B | 7 | B | 12 | B |
| 3 | C | 8 | B | 13 | B |
| 4 | C | 9 | A | 14 | B |
| 5 | B | 10 | B | 15 | B |
