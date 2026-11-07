# Phase 03 — Quiz 01: Collections

**Questions:** 20 | **Pass:** 16/20 | **Time:** 20 min

---

**Q1.** Which collection type is ordered AND mutable?
`A) tuple  B) set  C) list  D) frozenset`

**Q2.** What does `[1,2,3,4,5][2:4]` return?
`A) [2,3]  B) [3,4]  C) [2,3,4]  D) [3,4,5]`

**Q3.** Which removes and returns the last element?
`A) .delete()  B) .pop()  C) .remove()  D) del`

**Q4.** What is `{1,2,3} & {2,3,4}`?
`A) {1,2,3,4}  B) {2,3}  C) {1,4}  D) {2,3,2,3}`

**Q5.** How do you safely get a dict value without KeyError?
`A) dict[key]  B) dict.find(key)  C) dict.get(key)  D) dict.fetch(key)`

**Q6.** What does `list.append([1,2])` do?
`A) Adds 1 and 2 separately  B) Adds [1,2] as a single element  C) Error  D) Extends the list`

**Q7.** Can tuples be used as dictionary keys?
`A) No  B) Yes  C) Only if they contain strings  D) Only in Python 3.10+`

**Q8.** What is `len({"a":1,"b":2,"c":3})`?
`A) 6  B) 3  C) 2  D) Error`

**Q9.** What does `[x**2 for x in range(1,4)]` produce?
`A) [1,4,9]  B) [1,2,3]  C) [2,4,8]  D) [1,4,8]`

**Q10.** Which removes duplicates from a list?
`A) list(dict(items))  B) list(set(items))  C) list(tuple(items))  D) list(sorted(items))`

**Q11.** What is the output?
```python
d = {"a":1,"b":2}
d["c"] = 3
del d["a"]
print(list(d.keys()))
```
`A) ['a','b','c']  B) ['b','c']  C) ['c']  D) ['a','b']`

**Q12.** How does a set differ from a list?
`A) Sets are ordered  B) Sets have no duplicates and are unordered  C) Sets are immutable  D) Sets use () not {}`

**Q13.** What is `[n for n in range(10) if n%2==0]`?
`A) [1,3,5,7,9]  B) [0,2,4,6,8]  C) [2,4,6,8,10]  D) [0,1,2,...,9]`

**Q14.** What does `.items()` return on a dict?
`A) Just keys  B) Just values  C) Key-value tuple pairs  D) A list of lists`

**Q15.** Which line MODIFIES the original list?
`A) sorted(nums)  B) nums[:]  C) list(nums)  D) nums.sort()`

**Q16.** How do you check if "Alice" is a key in `staff = {"Alice": 30}`?
`A) staff.has("Alice")  B) "Alice" in staff  C) staff.contains("Alice")  D) find("Alice", staff)`

**Q17.** What is the result of `s1 - s2` where `s1={1,2,3}`, `s2={2,3,4}`?
`A) {1,4}  B) {1}  C) {4}  D) {1,2,3,4}`

**Q18.** What does `dict.update(other_dict)` do?
`A) Returns a merged dict  B) Modifies dict in-place with other_dict's pairs  C) Removes matching keys  D) Checks for differences`

**Q19.** What is `{k:v for k,v in [("a",1),("b",2)]}`?
`A) [("a",1),("b",2)]  B) {"a":1,"b":2}  C) {"a","b"}  D) Error`

**Q20.** What does `nums.pop(0)` do?
`A) Removes last item  B) Removes and returns first item  C) Returns first item without removing  D) Error`

---

## Answers

|Q|A|Q|A|Q|A|Q|A|
|--|--|--|--|--|--|--|--|
|1|C|6|B|11|B|16|B|
|2|B|7|B|12|B|17|B|
|3|B|8|B|13|B|18|B|
|4|B|9|A|14|C|19|B|
|5|C|10|B|15|D|20|B|
