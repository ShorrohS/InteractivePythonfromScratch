# Lesson 04 — Email Automation with smtplib

**Phase:** 12 — Automation | **Time:** ~50 min

---

## Part 1: SMTP Basics — SSL vs STARTTLS

SMTP (Simple Mail Transfer Protocol) is the protocol Python uses to send email.
There are two ways to secure the connection:

| Mode | Port | How it works |
|------|------|-------------|
| `SMTP_SSL` | 465 | SSL/TLS from the very first byte — simpler, preferred for Gmail |
| `SMTP` + STARTTLS | 587 | Starts unencrypted, then upgrades to TLS via `starttls()` |

```python
import smtplib

# ── SSL (port 465) ──────────────────────────────────────────────────────────
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, recipient, raw_message)

# ── STARTTLS (port 587) ─────────────────────────────────────────────────────
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.ehlo()         # identify ourselves to the server
    server.starttls()     # upgrade the connection to TLS
    server.login(sender_email, password)
    server.sendmail(sender_email, recipient, raw_message)
```

Both approaches work with Gmail. Port 465 with `SMTP_SSL` is simpler and
is used in all examples in this lesson.

---

## Part 2: Never Hardcode Credentials

Credentials in source code get committed, shared, and leaked. Always load
them from environment variables.

```python
import os
from dotenv import load_dotenv    # pip install python-dotenv

load_dotenv()    # reads .env file in the current directory

SENDER   = os.environ["EMAIL_SENDER"]
PASSWORD = os.environ["EMAIL_PASSWORD"]   # an App Password, not your login
```

Your `.env` file (add to `.gitignore` the moment you create it):

```
EMAIL_SENDER=yourname@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
```

**Gmail App Password setup:**
1. Enable 2-Factor Authentication on your Google account.
2. Go to **Google Account → Security → App Passwords**.
3. Create a new App Password (select "Mail" + your device).
4. Copy the 16-character code — that is your `EMAIL_PASSWORD`.

This way your real Google password is never in your code.

---

## Part 3: Sending a Plain Text Email

```python
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
SENDER   = os.environ["EMAIL_SENDER"]
PASSWORD = os.environ["EMAIL_PASSWORD"]


def send_text_email(to: str, subject: str, body: str) -> None:
    """Send a plain text email via Gmail SMTP_SSL."""
    msg = MIMEText(body, "plain")
    msg["From"]    = SENDER
    msg["To"]      = to
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, to, msg.as_string())

    print(f"Email sent to {to}")


# Test it
send_text_email(
    to="colleague@example.com",
    subject="Automated Report Ready",
    body=(
        "Hi,\n\n"
        "This week's sales report has been generated.\n"
        "Please check the shared drive for the latest figures.\n\n"
        "Regards,\nAutomation Bot"
    ),
)
```

---

## Part 4: Sending an HTML Email

HTML emails look more professional. Always include a plain text fallback
for email clients that cannot render HTML.

```python
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()
SENDER   = os.environ["EMAIL_SENDER"]
PASSWORD = os.environ["EMAIL_PASSWORD"]


def send_html_email(to: str, subject: str, html: str, plain: str) -> None:
    """Send an HTML email with a plain-text fallback."""
    # MIMEMultipart("alternative") — client picks the best version it can show
    msg = MIMEMultipart("alternative")
    msg["From"]    = SENDER
    msg["To"]      = to
    msg["Subject"] = subject

    # Attach plain text first — email clients prefer the LAST attached part
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html,  "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, to, msg.as_string())

    print(f"HTML email sent to {to}")


# Example call
html_body = """\
<html><body>
  <h2 style="color:#003366">Weekly Sales Summary</h2>
  <p>Your automated report is ready. <strong>Total revenue: $42,800</strong></p>
</body></html>"""

plain_body = "Weekly Sales Summary\n\nYour automated report is ready. Total revenue: $42,800"

send_html_email("manager@example.com", "Weekly Sales Summary", html_body, plain_body)
```

---

## Part 5: Adding File Attachments

```python
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from pathlib import Path


def add_attachment(msg: MIMEMultipart, filepath: str) -> None:
    """Read a file and attach it to a MIMEMultipart message."""
    path = Path(filepath)
    with open(path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{path.name}"',
    )
    msg.attach(part)


# Usage — add multiple attachments to one message
msg = MIMEMultipart("mixed")
add_attachment(msg, "reports/weekly_summary.xlsx")
add_attachment(msg, "reports/chart_q1.png")
```

---

## Part 6: Sending to Multiple Recipients

```python
import smtplib
import time
from email.mime.text import MIMEText


def send_bulk(
    recipients: list[str],
    subject: str,
    body: str,
    delay_seconds: float = 1.5,
) -> None:
    """
    Send the same email to each recipient individually.
    The delay avoids triggering Gmail rate-limit protections.
    """
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        for recipient in recipients:
            msg = MIMEText(body, "plain")
            msg["From"]    = SENDER
            msg["To"]      = recipient
            msg["Subject"] = subject
            server.sendmail(SENDER, recipient, msg.as_string())
            print(f"Sent → {recipient}")
            time.sleep(delay_seconds)


# CC and BCC — include all addresses in sendmail() even if not in headers
msg["CC"]  = "manager@example.com"
msg["BCC"] = "archive@example.com"   # BCC header is optional — usually omitted
all_recipients = ["to@example.com", "manager@example.com", "archive@example.com"]
server.sendmail(SENDER, all_recipients, msg.as_string())
```

---

## Part 7: Complete Example — Weekly Sales Summary Email

```python
"""
weekly_email.py
Reads sales_summary.csv, builds an HTML table, and emails it with
the CSV attached, to a distribution list.
"""

import csv
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
SENDER     = os.environ["EMAIL_SENDER"]
PASSWORD   = os.environ["EMAIL_PASSWORD"]
CSV_PATH   = Path("data/sales_summary.csv")
RECIPIENTS = ["manager@example.com", "director@example.com"]


def load_csv_rows(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def rows_to_html_table(rows: list[dict]) -> str:
    if not rows:
        return "<p>No data available.</p>"
    headers = list(rows[0].keys())
    th      = "".join(f"<th>{h}</th>" for h in headers)
    tr_rows = "".join(
        "<tr>" + "".join(f"<td>{v}</td>" for v in row.values()) + "</tr>"
        for row in rows
    )
    return (
        '<table border="1" cellpadding="6" cellspacing="0" '
        'style="border-collapse:collapse;font-family:Arial,sans-serif">'
        f'<thead style="background:#003366;color:white"><tr>{th}</tr></thead>'
        f"<tbody>{tr_rows}</tbody></table>"
    )


def send_weekly_report() -> None:
    rows  = load_csv_rows(CSV_PATH)
    table = rows_to_html_table(rows)
    week  = date.today().strftime("%B %d, %Y")

    html = (
        "<html><body>"
        f'<h2 style="color:#003366">Weekly Sales Summary — {week}</h2>'
        f"{table}"
        '<p style="color:#666;font-size:11px">Generated automatically.</p>'
        "</body></html>"
    )
    plain = f"Weekly Sales Summary — {week}\n\nSee the attached CSV for full figures.\n"

    # Outer message holds alternative text + attachment
    msg = MIMEMultipart("mixed")
    msg["From"]    = SENDER
    msg["To"]      = ", ".join(RECIPIENTS)
    msg["Subject"] = f"Weekly Sales Summary — {week}"

    # Alternative part: plain + HTML
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(plain, "plain"))
    alt.attach(MIMEText(html, "html"))
    msg.attach(alt)

    # CSV attachment
    with open(CSV_PATH, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{CSV_PATH.name}"')
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECIPIENTS, msg.as_string())

    print(f"Weekly report sent to {len(RECIPIENTS)} recipients.")


if __name__ == "__main__":
    send_weekly_report()
```

---

## Practice Exercises

1. Write a `send_error_alert(error: Exception)` function that emails you
   whenever it is called. Wrap a block of file-processing code in a
   `try/except` that calls `send_error_alert` in the `except` branch.

2. Modify `send_bulk()` to accept `recipients: list[tuple[str, str]]`
   (each tuple is `(name, email)`). Personalise the greeting in each email
   with the recipient's first name: "Hi Alice," instead of "Hi,".

3. Write a function that checks whether a given file path exists.
   If it does, email the file as an attachment. If it does not,
   send a plain-text notification: "Report file not found: {path}".

4. Combine Lessons 03 and 04: use `schedule` to send a test email to
   yourself every day at a fixed time. Confirm the scheduler fires by
   checking your inbox after the scheduled time.

---

## Next Lesson

**[Lesson 05 → CSV and Excel Automation](lesson-05-csv-excel-automation.md)**
