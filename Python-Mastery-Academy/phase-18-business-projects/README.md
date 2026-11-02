# 💼 Phase 18 — Business Projects (End-to-End)

> **Goal:** Build 5 enterprise-grade applications from requirements to deployment.

---

## These Are Your Flagship Projects

Each project follows the full professional development cycle:
```
Requirements → Architecture Design → Implementation → Testing → Documentation
```

---

## Projects

| # | Project | Technologies | Complexity |
|---|---------|-------------|-----------|
| 1 | [Employee Management System](employee-management-system/) | OOP, SQLite, Reports | ⭐⭐⭐⭐ |
| 2 | [Expense Management](expense-management/) | Pandas, CSV, Charts | ⭐⭐⭐⭐ |
| 3 | [Sales Analytics Dashboard](sales-analytics/) | Pandas, Matplotlib, Excel | ⭐⭐⭐⭐ |
| 4 | [Inventory Management](inventory-management/) | OOP, SQLite, REST API | ⭐⭐⭐⭐⭐ |
| 5 | [Ticket Management System](ticket-management/) | Full-stack, OOP, DB | ⭐⭐⭐⭐⭐ |

---

## Each Project Includes

```
project/
├── docs/
│   ├── requirements.md      ← What the system must do
│   ├── architecture.md      ← How it's designed
│   ├── design.md            ← Technical design decisions
│   ├── test-cases.md        ← Test plan
│   ├── user-guide.md        ← How to use it
│   └── deployment-guide.md  ← How to deploy it
│
├── src/                     ← Source code
│   ├── models/
│   ├── services/
│   ├── repositories/
│   └── main.py
│
├── tests/                   ← Test suite
└── README.md
```

---

## Project 1: Employee Management System

**Business Problem:** HR department needs to track employees, departments, roles, and payroll.

**Functional Requirements:**
- Add, update, deactivate employees
- Department and role management
- Monthly payroll calculation
- Salary report generation (CSV/Excel)
- Employee search and filtering
- Leave request tracking

**Technical Design:**
- OOP: Employee → (FullTimeEmployee, PartTimeEmployee, ContractEmployee)
- SQLite database with migrations
- Repository pattern for data access
- Service layer for business logic
- CLI menu interface

---

## Project 2: Expense Management Application

**Business Problem:** Finance team needs to track company expenses by department and category.

**Functional Requirements:**
- Record expenses by category, department, and date
- Monthly and annual budget tracking
- Variance analysis (actual vs budget)
- Export to Excel with charts
- Alert when department exceeds budget

**Technical Design:**
- Pandas for analysis
- SQLite for storage
- Matplotlib for charts
- Excel export with openpyxl

---

## Project 3: Sales Analytics Dashboard

**Business Problem:** Sales manager needs daily/weekly/monthly performance views.

**Functional Requirements:**
- Import sales data from CSV
- Region, product, rep performance views
- Year-over-year comparison
- Top performers leaderboard
- Forecast vs actual charts
- HTML report generation

---

## Project 4: Inventory Management System

**Business Problem:** Warehouse needs to track stock, reorder points, and supplier orders.

**Functional Requirements:**
- Product catalog management
- Stock level tracking (in/out)
- Low stock alerts
- Supplier management
- Purchase order generation
- REST API for integration

---

## Project 5: Ticket Management System

**Business Problem:** IT helpdesk needs to track support tickets and SLA compliance.

**Functional Requirements:**
- Create/assign/close tickets
- Priority levels (Critical/High/Medium/Low)
- SLA tracking
- Agent performance metrics
- Escalation rules
- Dashboard with charts

---

## ✅ Completion Checklist

For each project:
- [ ] Requirements document written
- [ ] Architecture designed
- [ ] Core functionality implemented
- [ ] Basic tests written
- [ ] README explains how to run

---

## Previous: [Phase 17](../phase-17-advanced-python/README.md) | Next: [Phase 19](../phase-19-software-engineering/README.md)
