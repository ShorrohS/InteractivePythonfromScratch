# Phase 12 — Quiz 01: Automation

**Questions: 20 | Pass: 16/20 | Time: 20 min**

---

## Section 1: pathlib and os (Q1–Q5)

**Q1.** What is the key advantage of `Path("src") / "data"` over `os.path.join("src", "data")`?

```
A) It is faster at runtime
B) It returns a Path object with a readable, cross-platform syntax — no escaping needed
C) It works only on Windows
D) It is required by Python 3.12+
```

---

**Q2.** What is the difference between `Path("logs").glob("*.log")` and `Path("logs").rglob("*.log")`?

```
A) glob is case-sensitive; rglob is not
B) glob searches only the immediate directory; rglob searches all subdirectories recursively
C) rglob returns strings; glob returns Path objects
D) They are identical — glob and rglob are aliases
```

---

**Q3.** `Path("data.csv").stat().st_size` returns the file size in what unit?

```
A) Kilobytes
B) Megabytes
C) Bytes
D) Bits
```

---

**Q4.** What does `Path("archive.tar.gz").suffix` return?

```
A) ".tar.gz"
B) ".tar"
C) ".gz"
D) "archive"
```

---

**Q5.** What does `Path("mydir").iterdir()` return?

```
A) A list of filenames as strings
B) A generator yielding a Path object for every entry in the directory (files and subdirectories)
C) Only files — directories are excluded automatically
D) Only subdirectories — files are excluded automatically
```

---

## Section 2: shutil and Archives (Q6–Q10)

**Q6.** What is the key difference between `shutil.copy()` and `shutil.copy2()`?

```
A) copy2 is significantly faster for large files
B) copy2 also copies file metadata (timestamps, permissions); copy copies only the file data
C) copy can handle directories; copy2 cannot
D) They are identical in all versions of Python
```

---

**Q7.** What happens when `shutil.move(src, dest)` is called and `dest` already exists as a file?

```
A) Raises FileExistsError
B) Silently skips the operation and returns None
C) Overwrites the destination file with the source
D) Creates a numbered backup copy (e.g. dest.1)
```

---

**Q8.** What does `shutil.rmtree(path)` do?

```
A) Removes only empty directories (raises an error for non-empty ones)
B) Recursively deletes the entire directory tree — all files and subdirectories
C) Moves the directory to the system trash/recycle bin
D) Creates a compressed archive before deleting
```

---

**Q9.** Which of the following is NOT a valid format string for `shutil.make_archive(..., format=...)`?

```
A) "zip"
B) "tar"
C) "gztar"
D) "7zip"
```

---

**Q10.** Which mode opens a `zipfile.ZipFile` for reading an existing archive?

```
A) "w"
B) "a"
C) "r"
D) "x"
```

---

## Section 3: CSV and Data Files (Q11–Q15)

**Q11.** What is the main practical difference between `csv.reader` and `csv.DictReader`?

```
A) DictReader is faster for large files
B) csv.reader yields each row as a list; DictReader yields each row as a dict keyed by column name
C) DictReader always requires you to supply fieldnames manually
D) csv.reader can only read files, not write them
```

---

**Q12.** Why is `open("data.csv", "w", newline="")` required instead of `open("data.csv", "w")` when writing CSV on Windows?

```
A) The newline="" argument is required on macOS only, not Windows
B) Without it, Windows adds an extra \r to each line, causing blank rows between data rows in the output
C) It prevents non-ASCII characters from being written incorrectly
D) It speeds up file writing by disabling buffering
```

---

**Q13.** What does `csv.writer(f, quoting=csv.QUOTE_ALL)` produce?

```
A) Skips quoting entirely — no quotes around any field
B) Quotes only fields that contain commas, quotes, or newlines
C) Wraps every field in double quotes, regardless of content
D) Raises a ValueError for any field that contains a comma
```

---

**Q14.** How do you open an existing Excel file with openpyxl without discarding its contents?

```
A) Workbook("file.xlsx")
B) openpyxl.open("file.xlsx")
C) load_workbook("file.xlsx")
D) Workbook.load("file.xlsx")
```

---

**Q15.** How do you read the value of cell A1 from a sheet named "Sheet1" in an openpyxl workbook `wb`?

```
A) wb.Sheet1.A1
B) wb["Sheet1"]["A1"].value
C) wb["Sheet1"].cell("A1")
D) wb.get("Sheet1").get("A1")
```

---

## Section 4: Scheduling and Email (Q16–Q20)

**Q16.** Which code correctly schedules `my_func` to run every 5 minutes using the `schedule` library?

```
A) schedule.every(5).minutes.run(my_func)
B) schedule.run(my_func, minutes=5)
C) schedule.every(5).minutes.do(my_func)
D) schedule.add(my_func, interval=5)
```

---

**Q17.** What does `schedule.run_pending()` do?

```
A) Runs all registered tasks immediately, ignoring their scheduled intervals
B) Executes only the tasks that are due at the current moment based on their schedule
C) Starts the scheduler's background thread
D) Cancels all currently pending tasks
```

---

**Q18.** When should you use `smtplib.SMTP_SSL` instead of `smtplib.SMTP`?

```
A) When connecting on port 587 with STARTTLS
B) When the server requires SSL from the very start of the connection (typically port 465)
C) For all Gmail connections regardless of port
D) When the server does not support user authentication
```

---

**Q19.** What does `msg.attach(part)` do when `msg` is a `MIMEMultipart` object?

```
A) Immediately sends the attachment to the SMTP server
B) Adds a MIME part (body text or file attachment) as a child section of the message
C) Sets the MIME content type of the entire email
D) Encodes the entire message in base64 format
```

---

**Q20.** What is the purpose of calling `server.starttls()` before `server.login()`?

```
A) It verifies the SMTP server's SSL certificate against a trusted authority
B) It upgrades the plaintext SMTP connection to an encrypted TLS channel before credentials are sent
C) It is optional and only required when connecting to port 465
D) It sets the sender's email address on the server
```

---

## Answers

| Q  | Answer | Key Point |
|----|--------|-----------|
| 1  | B | `Path` uses `/` operator — readable, cross-platform, no escaping |
| 2  | B | `glob` = immediate directory only; `rglob` = full recursive tree |
| 3  | C | `st_size` is always in bytes; divide by 1024 for KB |
| 4  | C | `suffix` returns only the last extension — `.gz`, not `.tar.gz` |
| 5  | B | `iterdir()` yields all entries (files + dirs) as Path objects |
| 6  | B | `copy2` preserves metadata (timestamps, permissions); `copy` does not |
| 7  | C | `shutil.move` overwrites an existing destination file |
| 8  | B | `rmtree` recursively deletes everything — use with caution |
| 9  | D | `"7zip"` is not supported; valid formats: zip, tar, gztar, bztar, xztar |
| 10 | C | `"r"` = read; `"w"` = write new; `"a"` = append; `"x"` = create new |
| 11 | B | `DictReader` → dict per row; `reader` → list per row |
| 12 | B | Windows universal newlines conflict with csv's own `\r\n` handling |
| 13 | C | `QUOTE_ALL` wraps every field in double quotes |
| 14 | C | `load_workbook("file.xlsx")` opens existing files |
| 15 | B | `wb["Sheet1"]["A1"].value` is the correct cell access syntax |
| 16 | C | `.do(func)` registers the job; `.run(func)` does not exist |
| 17 | B | `run_pending()` only fires tasks whose scheduled time has arrived |
| 18 | B | `SMTP_SSL` = implicit SSL from the start (port 465); `SMTP` + `starttls()` = explicit upgrade (port 587) |
| 19 | B | `attach()` adds a MIME part to the multipart container |
| 20 | B | `starttls()` encrypts the channel before the password is transmitted |
