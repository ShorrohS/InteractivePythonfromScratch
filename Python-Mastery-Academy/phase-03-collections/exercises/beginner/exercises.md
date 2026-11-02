# 📝 Phase 03 — Collections Exercises

> Attempt all questions before checking solutions.
> Solutions: `../../solutions/beginner/solutions.md`

---

## Section A: Lists (Q1–Q6)

**Q1.** Create a list of 5 of your favorite movies. Print:
- The first movie
- The last movie  
- The list in reverse order
- The number of movies

---

**Q2.** Given `scores = [72, 85, 90, 68, 95, 78, 82]`, write code to:
- Find the highest score
- Find the lowest score
- Calculate the average
- Count scores above 80

---

**Q3.** What is the output?
```python
numbers = [1, 2, 3, 4, 5]
numbers.append(6)
numbers.insert(0, 0)
numbers.remove(3)
print(numbers)
print(len(numbers))
```

---

**Q4.** Write a list comprehension that creates a list of squares for numbers 1-10, but only includes even squares.

---

**Q5.** Write a shopping cart program: start with an empty list, let user add items, then display all items and the count.

---

**Q6.** What is wrong with this code and how do you fix it?
```python
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)
print(items)
```

---

## Section B: Tuples (Q7–Q9)

**Q7.** Create a tuple storing GPS coordinates: `(latitude, longitude, altitude)`. Explain why a tuple is better than a list here.

---

**Q8.** What is the output?
```python
point = (3, 7)
x, y = point
print(f"X: {x}, Y: {y}")
print(point[0] + point[1])
```

---

**Q9.** Given a list of tuples `[(name, score)]`, sort them by score in descending order.

---

## Section C: Sets (Q10–Q13)

**Q10.** Given two sets of website visitors: Monday: `{1001, 1002, 1003, 1004}` and Tuesday: `{1002, 1003, 1005, 1006}`:
- Who visited BOTH days? (intersection)
- Who visited EITHER day? (union)
- Who visited ONLY on Monday? (difference)

---

**Q11.** Given `emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com", "b@x.com"]`, how do you find all UNIQUE emails?

---

**Q12.** What is the output?
```python
s1 = {1, 2, 3}
s2 = {2, 3, 4}
print(s1 | s2)
print(s1 & s2)
print(s1 - s2)
```

---

**Q13.** Sets are unordered. What does this mean practically?

---

## Section D: Dictionaries (Q14–Q18)

**Q14.** Create a dictionary for a student: name, age, GPA, courses (list). Print each field nicely formatted.

---

**Q15.** Given `employees = {"Alice": 75000, "Bob": 65000, "Carol": 90000}`, write code to:
- Print the employee with the highest salary
- Give everyone a 10% raise
- Print all employees earning over $70,000

---

**Q16.** What is the output?
```python
d = {"a": 1, "b": 2, "c": 3}
d["d"] = 4
del d["a"]
print(d.get("a", "Not found"))
print(list(d.keys()))
```

---

**Q17.** Write a word frequency counter: given a sentence, count how many times each word appears using a dictionary.

---

**Q18.** What is the difference between `d["key"]` and `d.get("key")`? When would you use each?

---

## Section E: Comprehensions (Q19–Q20)

**Q19.** Write a dictionary comprehension that maps each word in a list to its length.

**Q20.** Given `data = [{"name": "Alice", "score": 92}, {"name": "Bob", "score": 78}]`, use a comprehension to create a dict of `{name: score}`.

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
