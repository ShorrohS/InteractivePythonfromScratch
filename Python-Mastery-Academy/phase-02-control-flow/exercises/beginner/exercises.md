# 📝 Phase 02 — Beginner Exercises

> Attempt all before checking solutions.
> Solutions: `../../solutions/beginner/solutions.md`

---

## Section A: If / Elif / Else (Q1–Q7)

**Q1.** Write a program that asks for a number and prints whether it's positive, negative, or zero.

---

**Q2.** Write a traffic light simulator:
- "red" → "STOP"
- "yellow" → "SLOW DOWN"
- "green" → "GO"
- anything else → "INVALID SIGNAL"

---

**Q3.** Write a temperature classifier:
- Above 35°C → "Extreme Heat"
- 25-35°C → "Hot"
- 15-24°C → "Warm"
- 5-14°C → "Cool"
- Below 5°C → "Cold"

---

**Q4.** What is the output?
```python
x = 10
if x > 5:
    print("A")
    if x > 8:
        print("B")
    print("C")
print("D")
```

---

**Q5.** Write a grade classifier: Given a score 0-100, print the letter grade (A=90+, B=80+, C=70+, D=60+, F=below 60) AND whether it's Pass or Fail.

---

**Q6.** Fix this code:
```python
score = 75
if score >= 90
    print("A")
elif score = 80:
    print("B")
else
    print("Other")
```

---

**Q7.** Write a simple login: if username is "admin" AND password is "1234", print "Access granted". Otherwise print "Access denied".

---

## Section B: While Loops (Q8–Q12)

**Q8.** Write a multiplication table generator: ask for a number N, print N × 1 through N × 12 using a while loop.

---

**Q9.** Write a "guess the number" game: generate a random number 1-10, ask user to guess, count attempts, end when correct.

---

**Q10.** What is the output of this code?
```python
total = 0
i = 1
while i <= 5:
    total += i
    i += 1
print(total)
```

---

**Q11.** Write a program that keeps asking for a password until the user types one that is at least 8 characters long.

---

**Q12.** Fix this code (currently infinite loop):
```python
count = 0
while count < 10:
    print(count)
```

---

## Section C: For Loops (Q13–Q17)

**Q13.** Using a for loop, print all even numbers from 2 to 20.

---

**Q14.** Write a program that takes a list of 5 numbers and uses a for loop to find the sum, count, maximum, and minimum (without using sum(), max(), min()).

---

**Q15.** What is the output?
```python
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit.upper()}")
```

---

**Q16.** Write a for loop that prints the first 10 fibonacci numbers (0, 1, 1, 2, 3, 5, 8, 13, 21, 34).

---

**Q17.** Write a nested loop to print a multiplication table for numbers 1-5 × 1-5.

---

## Section D: Break, Continue, Patterns (Q18–Q20)

**Q18.** Write a program that reads numbers until the user types 0, then prints the sum of all entered numbers.

---

**Q19.** Using continue, print all numbers from 1 to 20 that are NOT divisible by 3.

---

**Q20.** Write code to print this pattern (using nested loops):
```
*
**
***
****
*****
```

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
