# Phase 02 — Completion Assessment

> Pass mark: 80% | Time: 25 minutes

---

## PART A: Write the Code

**Task 1.** Write a program that asks for a student's score (0–100) and:
- Validates input is in range (keep asking if not)
- Outputs: letter grade, GPA, "Pass" or "Fail", and a motivational message based on the grade

---

**Task 2.** Write a program using a `while` loop that:
- Asks the user to enter employee names (type "done" to stop)
- Stores count of entries
- At the end prints: total employees entered

---

**Task 3.** Write a program that uses nested loops to print this pattern (rows = 5):
```
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5
```

---

## PART B: Predict the Output

**Q4.**
```python
for i in range(2, 12, 3):
    print(i, end=" ")
```

**Q5.**
```python
nums = [1, 2, 3, 4, 5, 6]
evens = []
for n in nums:
    if n % 2 != 0:
        continue
    evens.append(n)
print(evens)
```

**Q6.**
```python
found = False
for n in [10, 20, 30, 40]:
    if n > 25:
        found = True
        break
print(found, n)
```

---

## PART C: Find the Bugs

**Q7.** Find 3 bugs:
```python
x = 50
if x > 100
    print("large")
elif x = 50:
    print("medium")
else
    print("small")
```

**Q8.** Why doesn't this terminate?
```python
i = 0
while i < 5:
    print(i)
```

---

## PART D: Short Answer

**Q9.** What is the difference between `break` and `continue`?

**Q10.** When would you use `match/case` instead of `if/elif`?

---

## Answers

**Q4:** `2 5 8 11`

**Q5:** `[2, 4, 6]`

**Q6:** `True 30`

**Q7 bugs:**
1. Missing `:` after `if x > 100`
2. `elif x = 50` — assignment, should be `==`
3. Missing `:` after `else`

**Q8:** `i` is never incremented. Add `i += 1` inside the loop.

**Q9:** `break` exits the entire loop. `continue` skips the rest of the current iteration and jumps to the next one.

**Q10:** `match/case` is cleaner when checking a single variable against many fixed values. `if/elif` is better for complex multi-variable conditions.
