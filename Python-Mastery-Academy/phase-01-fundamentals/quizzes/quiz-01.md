# Phase 01 — Quiz 01: Python Fundamentals

**Questions:** 20 | **Pass:** 16/20 | **Time:** 20 min (no notes)

---

## Section 1: Variables & Data Types (Q1–Q6)

**Q1.** What is the type of `x` after: `x = "3.14"`?
```
A) float   B) int   C) str   D) number
```

**Q2.** Which statement creates an integer variable?
```
A) age = "30"    B) age = 30.0    C) age = 30    D) age = True
```

**Q3.** What is the output?
```python
a = 10
b = a
a = 99
print(b)
```
```
A) 99    B) 10    C) None    D) Error
```

**Q4.** Which variable name is invalid in Python?
```
A) _score    B) total2024    C) first-name    D) myVariable
```

**Q5.** What does `type(True)` return?
```
A) <class 'int'>    B) <class 'bool'>    C) <class 'str'>    D) <class 'NoneType'>
```

**Q6.** After this code, what is `x`?
```python
x = 5
x *= 3
x -= 4
```
```
A) 15    B) 11    C) 8    D) 19
```

---

## Section 2: Input & Output (Q7–Q10)

**Q7.** `input()` always returns which type?
```
A) int    B) float    C) str    D) depends on what user types
```

**Q8.** Which f-string formats a number as `$1,234.56`?
```
A) f"${x:.2}"    B) f"${x:,.2f}"    C) f"${x:2.f}"    D) f"${x,.2}"
```

**Q9.** What is wrong with this code?
```python
age = input("Age: ")
print("Next year: " + age + 1)
```
```
A) Missing quotes around 1
B) Can't add str + int — needs int(age)
C) input() doesn't work like that
D) print() can't use +
```

**Q10.** What does this print?
```python
name = "Alice"
print(f"Hello {'name'}!")
```
```
A) Hello Alice!
B) Hello name!
C) Hello {'name'}!
D) SyntaxError
```

---

## Section 3: Operators (Q11–Q14)

**Q11.** What is the result of `17 % 5`?
```
A) 3    B) 3.4    C) 2    D) 12
```

**Q12.** What does `//` do?
```
A) Comment     B) Integer division (no decimal)
C) Regular division    D) Power operator
```

**Q13.** What is `2 + 3 * 4`?
```
A) 20    B) 14    C) 24    D) 100
```

**Q14.** Which comparison checks if two values are equal?
```
A) =    B) ==    C) ===    D) is
```

---

## Section 4: Strings (Q15–Q18)

**Q15.** What does `"Hello"[1]` return?
```
A) H    B) e    C) l    D) Hello
```

**Q16.** What does `"hello world".title()` return?
```
A) HELLO WORLD    B) Hello world    C) Hello World    D) hello World
```

**Q17.** Which method splits a string into a list?
```
A) .break()    B) .split()    C) .list()    D) .divide()
```

**Q18.** What is `len("Python")` ?
```
A) 5    B) 6    C) 7    D) Error
```

---

## Section 5: Boolean Logic (Q19–Q20)

**Q19.** What does `bool("")` return?
```
A) True    B) False    C) None    D) Error
```

**Q20.** What is the output?
```python
x = 10
print(x > 5 and x < 20)
```
```
A) True    B) False    C) 10    D) Error
```

---

## Answers

.
.
.
.
.
.

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | C | Quotes make it a string regardless of content |
| 2 | C | `30` with no quotes or decimal is int |
| 3 | B | `b = a` copies the value 10; changing `a` later doesn't change `b` |
| 4 | C | Hyphens not allowed — they're the subtraction operator |
| 5 | B | `True` is of type `bool` |
| 6 | B | 5 * 3 = 15, 15 - 4 = 11 |
| 7 | C | Always returns str — you must convert |
| 8 | B | `:,` adds commas, `.2f` gives 2 decimal places |
| 9 | B | `age` is a str from input; can't add str + int |
| 10 | B | `{'name'}` has quotes inside — it's a literal string, not a variable |
| 11 | C | 17 = 3×5 + 2 → remainder is 2 |
| 12 | B | `//` is floor (integer) division |
| 13 | B | Multiplication first: 3*4=12, then 2+12=14 |
| 14 | B | `==` compares values; `=` assigns |
| 15 | B | Index 0 = H, index 1 = e |
| 16 | C | `.title()` capitalises first letter of each word |
| 17 | B | `.split()` splits on whitespace by default |
| 18 | B | P-y-t-h-o-n = 6 characters |
| 19 | B | Empty string is falsy |
| 20 | A | 10 > 5 is True AND 10 < 20 is True → True |
