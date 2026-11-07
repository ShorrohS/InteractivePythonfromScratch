# Phase 02 — Quiz 01: Control Flow

**Questions:** 20 | **Pass:** 16/20 | **Time:** 20 min

---

## Section 1: if / elif / else (Q1–Q5)

**Q1.** What is printed?
```python
x = 15
if x > 10:
    print("A")
if x > 20:
    print("B")
print("C")
```
`A) A  B) A C  C) A B C  D) C`

**Q2.** How many `elif` clauses can an `if` statement have?
`A) 1  B) 2  C) 10  D) As many as needed`

**Q3.** What is the output?
```python
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
print(grade)
```
`A) A  B) B  C) C  D) Error`

**Q4.** Which is a valid ternary expression?
```
A) x = if a > b then a else b
B) x = a if a > b else b
C) x = (a > b) ? a : b
D) x = a when a > b otherwise b
```

**Q5.** What is missing?
```python
age = 20
if age >= 18
    print("Adult")
```
`A) Colon after if statement  B) Parentheses  C) Quotes  D) Nothing`

---

## Section 2: Loops (Q6–Q12)

**Q6.** How many times does this print?
```python
for i in range(3, 8):
    print(i)
```
`A) 3  B) 4  C) 5  D) 8`

**Q7.** What does `range(1, 10, 2)` produce?
`A) [1,3,5,7,9]  B) [1,2,3,...,10]  C) [2,4,6,8,10]  D) [1,3,5,7]`

**Q8.** What is the output?
```python
total = 0
for i in range(1, 5):
    total += i
print(total)
```
`A) 10  B) 15  C) 4  D) 0`

**Q9.** When does a `while True` loop stop?
`A) After 1 iteration  B) Never, unless broken with break  C) After 100 iterations  D) When variable changes`

**Q10.** What does `continue` do inside a loop?
`A) Exits the loop  B) Skips the rest of current iteration  C) Restarts from scratch  D) Does nothing`

**Q11.** What is the output?
```python
for i in range(5):
    if i == 3:
        break
    print(i, end=" ")
```
`A) 0 1 2 3  B) 0 1 2  C) 1 2 3  D) 0 1 2 3 4`

**Q12.** When does the `else` clause of a for loop run?
`A) Always  B) Only if the loop ran zero iterations  C) Only if loop completed without break  D) Never`

---

## Section 3: Nested Loops & Patterns (Q13–Q16)

**Q13.** How many total iterations in this nested loop?
```python
for i in range(3):
    for j in range(4):
        pass
```
`A) 7  B) 12  C) 3  D) 4`

**Q14.** What does this print?
```python
for i in range(1, 4):
    print("*" * i)
```
```
A)              B)   C)    D)
*               *    ***   *
**              **   **    **
***             ***  *     ***
```

**Q15.** How do you break out of BOTH nested loops?
`A) break break  B) Use a flag variable  C) double break  D) exit()`

**Q16.** What is `pass` used for?
`A) Skip to next iteration  B) Exit the loop  C) Placeholder — do nothing  D) End the program`

---

## Section 4: match/case & Logic (Q17–Q20)

**Q17.** Which Python version introduced match/case?
`A) 3.8  B) 3.9  C) 3.10  D) 3.12`

**Q18.** What is the default case in a match statement?
`A) default:  B) else:  C) case _:  D) case *:`

**Q19.** What does this evaluate to?
```python
x = 5
print(x > 0 and x < 10)
```
`A) True  B) False  C) 5  D) Error`

**Q20.** Which correctly checks if `day` is Saturday OR Sunday?
```
A) if day == "Saturday" and day == "Sunday":
B) if day == "Saturday" or day == "Sunday":
C) if day in "SaturdaySunday":
D) if day == ("Saturday", "Sunday"):
```

---

## Answers

| Q | Answer | Key Point |
|---|--------|-----------|
| 1 | B | Two separate `if` statements — both run independently |
| 2 | D | Unlimited elif clauses |
| 3 | B | 85 >= 80 triggers the B branch |
| 4 | B | Python ternary: `value if condition else other` |
| 5 | A | Missing `:` after `if age >= 18` |
| 6 | C | range(3,8) = 3,4,5,6,7 → 5 values |
| 7 | A | Start 1, stop before 10, step 2 |
| 8 | A | 1+2+3+4 = 10 |
| 9 | B | Only `break` exits a `while True` |
| 10 | B | `continue` skips current iteration body |
| 11 | B | Prints 0,1,2 then breaks when i==3 |
| 12 | C | else runs only when no break occurred |
| 13 | B | 3 × 4 = 12 iterations |
| 14 | A | Increasing stars: *, **, *** |
| 15 | B | Use a flag variable + check after inner loop |
| 16 | C | `pass` is a do-nothing placeholder |
| 17 | C | match/case introduced in Python 3.10 |
| 18 | C | `case _:` is the catch-all default |
| 19 | A | 5 > 0 is True AND 5 < 10 is True |
| 20 | B | Use `or` to check either/or |
