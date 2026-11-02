# Requirements — Employee Management System

**Project:** Employee Management System  
**Phase:** 18 — Business Projects  
**Version:** 1.0

---

## Business Problem

The HR department manually tracks employee information in spreadsheets. This is error-prone, time-consuming, and hard to share. They need a centralized system to manage all employee data.

---

## Functional Requirements

### Employee Management
- FR-001: System must allow creating new employee records
- FR-002: System must support viewing employee details by ID or name
- FR-003: System must allow updating employee information
- FR-004: System must support deactivating (soft-deleting) employees
- FR-005: System must track hire date automatically

### Department Management
- FR-006: System must support department CRUD operations
- FR-007: System must assign employees to departments
- FR-008: System must show department headcount and average salary

### Payroll
- FR-009: System must calculate monthly gross pay per employee
- FR-010: System must calculate tax deductions (20% flat rate)
- FR-011: System must generate payroll summary report
- FR-012: System must support salary updates with history

### Reporting
- FR-013: System must generate employee list (filterable by dept/status)
- FR-014: System must generate monthly payroll report as CSV
- FR-015: System must show department analytics (headcount, salary stats)
- FR-016: System must export data to CSV

---

## Non-Functional Requirements

- NFR-001: Application must run in Python 3.10+
- NFR-002: Data must persist between sessions (SQLite database)
- NFR-003: All operations must validate input before processing
- NFR-004: Sensitive operations must have confirmation prompts
- NFR-005: All errors must be handled gracefully with informative messages

---

## User Stories

**As an HR Manager, I want to:**
1. Add a new employee with complete profile in under 2 minutes
2. Look up any employee by name or ID instantly
3. Update an employee's salary and see the change reflected immediately
4. Generate a monthly payroll report that I can export to CSV
5. See which departments are understaffed or overpaid

---

## Data Model

### Employee
```
id           INTEGER PRIMARY KEY AUTOINCREMENT
employee_id  TEXT UNIQUE (e.g., EMP001)
first_name   TEXT NOT NULL
last_name    TEXT NOT NULL
email        TEXT UNIQUE
department   TEXT NOT NULL
job_title    TEXT
salary       REAL NOT NULL
hire_date    TEXT
status       TEXT (active/inactive)
created_at   TEXT
```

### Department
```
id           INTEGER PRIMARY KEY AUTOINCREMENT
name         TEXT UNIQUE NOT NULL
manager_id   INTEGER (FK to employees)
budget       REAL
created_at   TEXT
```

### Salary History
```
id           INTEGER PRIMARY KEY
employee_id  TEXT (FK)
old_salary   REAL
new_salary   REAL
changed_by   TEXT
changed_at   TEXT
reason       TEXT
```

---

## Acceptance Criteria

| ID | Criteria | Pass Condition |
|----|---------|---------------|
| AC-001 | Add employee | New employee appears in `get_all_employees()` |
| AC-002 | Search employee | Returns matching records with correct data |
| AC-003 | Update salary | New salary stored, history record created |
| AC-004 | Deactivate employee | Employee not in active list, marked inactive in DB |
| AC-005 | Payroll report | CSV with all active employees, calculations correct |
| AC-006 | Department stats | Correct headcount, avg/max/min salary |
