# Phase 05 — Quiz 01: File Handling

**Questions:** 15 | **Pass:** 12/15 | **Time:** 15 min

---

**Q1.** Which file mode creates a new file or OVERWRITES an existing one?
`A) a  B) r  C) w  D) x`

**Q2.** What does the `with` statement guarantee?
`A) The file is read correctly  B) The file is always closed  C) The file exists  D) No errors occur`

**Q3.** What does `f.readlines()` return?
`A) A single string  B) A list of lines (each with \n)  C) A generator  D) An integer`

**Q4.** What mode opens a file for both reading and writing without clearing it?
`A) "rw"  B) "wr"  C) "r+"  D) "w+"`

**Q5.** What is `newline=""` used for in CSV file operations?
`A) Removes all newlines from data  B) Prevents double newlines on Windows  C) Required for all file operations  D) Makes the file read-only`

**Q6.** How do you check if a file exists before reading?
`A) try: open(file) except: ...  B) os.path.exists(file)  C) Both A and B work  D) file.check()`

**Q7.** What does `csv.DictReader` return for each row?
`A) A list  B) A tuple  C) An OrderedDict/dict  D) A string`

**Q8.** After reading a CSV with DictReader, what type is a numeric column like "price"?
`A) float  B) int  C) str  D) number`

**Q9.** What does `json.dump(data, f)` do?
`A) Reads JSON from f  B) Writes Python data as JSON to file f  C) Validates JSON  D) Converts data to string`

**Q10.** What is the difference between `json.dump` and `json.dumps`?
`A) No difference  B) dump writes to file; dumps returns a string  C) dumps is faster  D) dump is for dicts; dumps is for lists`

**Q11.** What does `Path("a") / "b" / "c.txt"` produce?
`A) "a/b/c.txt" (string)  B) A Path object: a/b/c.txt  C) A list  D) Error`

**Q12.** How do you list all `.json` files recursively with pathlib?
`A) Path(".").list("*.json")  B) Path(".").rglob("*.json")  C) os.find("*.json")  D) glob.glob("**/*.json")`

**Q13.** What happens when you open a file with mode `"x"` and the file exists?
`A) It overwrites the file  B) FileExistsError is raised  C) It appends to the file  D) Nothing`

**Q14.** Why should you always use `with open(...)` instead of `f = open(...)`?
`A) with is faster  B) Ensures the file is closed even if an error occurs  C) Required for CSV  D) Makes the file read-only`

**Q15.** You have a CSV with columns: name, age, salary. After reading with DictReader, how do you get the salary as a float?
`A) row.salary  B) float(row["salary"])  C) row["salary"].float()  D) It's already a float`

---

## Answers

| Q | A | Q | A | Q | A |
|---|---|---|---|---|---|
| 1 | C | 6 | C | 11 | B |
| 2 | B | 7 | C | 12 | B |
| 3 | B | 8 | C | 13 | B |
| 4 | C | 9 | B | 14 | B |
| 5 | B | 10 | B | 15 | B |
