# ⚡ Phase 12 Cheat Sheet — Automation

---

## File System (pathlib)

```python
from pathlib import Path
import shutil, os

p = Path("folder/file.txt")
p.exists()
p.is_file()
p.is_dir()
p.suffix          # ".txt"
p.stem            # "file"
p.name            # "file.txt"
p.parent          # Path("folder")

# Create
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("content")
p.write_bytes(bytes_data)

# Read
content = p.read_text()

# Copy / move / delete
shutil.copy(src, dst)
shutil.copytree(src_dir, dst_dir)
shutil.move(src, dst)
p.unlink()              # delete file
shutil.rmtree(directory) # delete folder

# List files
for f in Path("dir").iterdir():    # one level
for f in Path("dir").rglob("*.py"):# recursive
for f in Path("dir").glob("*.csv"):# pattern
```

---

## Excel with openpyxl

```bash
pip install openpyxl
```

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

# Create
wb = Workbook()
ws = wb.active
ws.title = "Data"

# Write
ws["A1"] = "Name"
ws.cell(row=2, column=1, value="Alice")
ws.append(["Bob", 30, 75000])      # add row

# Style
ws["A1"].font = Font(bold=True, size=12)
ws["A1"].fill = PatternFill("solid", fgColor="4472C4")

# Formula
ws["D2"] = "=B2*C2"

# Column width
ws.column_dimensions["A"].width = 20

# Save
wb.save("report.xlsx")

# Load existing
wb = load_workbook("existing.xlsx")
ws = wb.active
for row in ws.iter_rows(min_row=2, values_only=True):
    print(row)
```

---

## Email (smtplib)

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email(to: str, subject: str, body: str) -> None:
    msg = MIMEMultipart()
    msg["From"]    = os.getenv("EMAIL_FROM")
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASS"))
        server.send_message(msg)
```

---

## Scheduling (schedule library)

```bash
pip install schedule
```

```python
import schedule, time

def job():
    print("Running...")

schedule.every(10).seconds.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("09:00").do(job)
schedule.every().monday.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```
