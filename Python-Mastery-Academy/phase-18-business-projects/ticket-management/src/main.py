"""
Ticket Management System
Phase 18: Business Projects

End-to-end helpdesk/ticketing application with:
  - SQLite database
  - Priority levels and SLA tracking
  - Agent assignment
  - Status workflow
  - Reporting and analytics

HOW TO RUN:
  python main.py
"""

import sqlite3
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from enum import Enum

DB = "tickets.db"


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH     = "high"
    MEDIUM   = "medium"
    LOW      = "low"


class Status(str, Enum):
    OPEN        = "open"
    IN_PROGRESS = "in_progress"
    PENDING     = "pending"
    RESOLVED    = "resolved"
    CLOSED      = "closed"


# SLA in hours per priority
SLA_HOURS = {
    Priority.CRITICAL: 4,
    Priority.HIGH:     8,
    Priority.MEDIUM:   24,
    Priority.LOW:      72,
}


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT    NOT NULL,
                description TEXT,
                priority    TEXT    NOT NULL DEFAULT 'medium',
                status      TEXT    NOT NULL DEFAULT 'open',
                requester   TEXT    NOT NULL,
                agent       TEXT,
                category    TEXT    DEFAULT 'General',
                created_at  TEXT    NOT NULL,
                updated_at  TEXT    NOT NULL,
                resolved_at TEXT,
                due_at      TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id   INTEGER NOT NULL,
                author      TEXT    NOT NULL,
                body        TEXT    NOT NULL,
                created_at  TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


def create_ticket(title: str, description: str, priority: str,
                  requester: str, category: str = "General") -> int:
    now  = datetime.now().isoformat()
    due  = (datetime.now() + timedelta(hours=SLA_HOURS.get(priority, 24))).isoformat()
    with get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO tickets (title, description, priority, status,
                                 requester, category, created_at, updated_at, due_at)
            VALUES (?, ?, ?, 'open', ?, ?, ?, ?, ?)
        """, (title, description, priority, requester, category, now, now, due))
        conn.commit()
        return cursor.lastrowid


def assign_ticket(ticket_id: int, agent: str) -> bool:
    with get_conn() as conn:
        cursor = conn.execute("""
            UPDATE tickets SET agent=?, status='in_progress', updated_at=?
            WHERE id=? AND status='open'
        """, (agent, datetime.now().isoformat(), ticket_id))
        conn.commit()
        return cursor.rowcount > 0


def update_status(ticket_id: int, new_status: str) -> bool:
    now  = datetime.now().isoformat()
    with get_conn() as conn:
        resolved_at = now if new_status in ("resolved", "closed") else None
        cursor = conn.execute("""
            UPDATE tickets SET status=?, updated_at=?, resolved_at=?
            WHERE id=?
        """, (new_status, now, resolved_at, ticket_id))
        conn.commit()
        return cursor.rowcount > 0


def add_comment(ticket_id: int, author: str, body: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO comments (ticket_id, author, body) VALUES (?,?,?)",
            (ticket_id, author, body)
        )
        conn.execute(
            "UPDATE tickets SET updated_at=? WHERE id=?",
            (datetime.now().isoformat(), ticket_id)
        )
        conn.commit()


def get_ticket(ticket_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()
        return dict(row) if row else None


def list_tickets(status: str = None, priority: str = None,
                 agent: str = None) -> list[dict]:
    query  = "SELECT * FROM tickets WHERE 1=1"
    params = []
    if status:   query += " AND status=?";   params.append(status)
    if priority: query += " AND priority=?"; params.append(priority)
    if agent:    query += " AND agent=?";    params.append(agent)
    query += " ORDER BY CASE priority WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END, created_at"
    with get_conn() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]


def overdue_tickets() -> list[dict]:
    now = datetime.now().isoformat()
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT * FROM tickets
            WHERE status NOT IN ('resolved','closed')
              AND due_at < ?
            ORDER BY due_at
        """, (now,)).fetchall()
        return [dict(r) for r in rows]


def dashboard_stats() -> dict:
    with get_conn() as conn:
        total   = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
        by_stat = dict(conn.execute(
            "SELECT status, COUNT(*) FROM tickets GROUP BY status").fetchall())
        by_pri  = dict(conn.execute(
            "SELECT priority, COUNT(*) FROM tickets GROUP BY priority").fetchall())
        overdue = len(overdue_tickets())
        avg_res = conn.execute("""
            SELECT AVG(
                (julianday(resolved_at) - julianday(created_at)) * 24
            ) FROM tickets WHERE resolved_at IS NOT NULL
        """).fetchone()[0]
    return {
        "total": total, "by_status": by_stat,
        "by_priority": by_pri, "overdue": overdue,
        "avg_resolution_hours": round(avg_res or 0, 1)
    }


def display_ticket(ticket: dict) -> None:
    print(f"\n  Ticket #{ticket['id']}: {ticket['title']}")
    print(f"  Priority:  {ticket['priority'].upper()}")
    print(f"  Status:    {ticket['status']}")
    print(f"  Requester: {ticket['requester']}")
    print(f"  Agent:     {ticket['agent'] or 'Unassigned'}")
    print(f"  Category:  {ticket['category']}")
    print(f"  Created:   {ticket['created_at'][:10]}")
    if ticket.get("due_at"):
        due = datetime.fromisoformat(ticket["due_at"])
        overdue = due < datetime.now() and ticket["status"] not in ("resolved","closed")
        print(f"  Due:       {ticket['due_at'][:10]} {'[OVERDUE]' if overdue else ''}")
    if ticket.get("description"):
        print(f"\n  {ticket['description']}")


def display_tickets_list(tickets: list[dict]) -> None:
    if not tickets:
        print("  No tickets found.")
        return
    priority_icons = {"critical": "[!!!]", "high": "[!!]", "medium": "[!]", "low": "[ ]"}
    print(f"\n  {'#':<5} {'Priority':<10} {'Status':<13} {'Requester':<15} {'Title':<35} {'Agent'}")
    print("  " + "-" * 85)
    for t in tickets:
        icon  = priority_icons.get(t["priority"], "[ ]")
        title = t["title"][:33] + ".." if len(t["title"]) > 33 else t["title"]
        print(f"  {t['id']:<5} {icon} {t['priority']:<7} {t['status']:<13} "
              f"{t['requester']:<15} {title:<35} {t['agent'] or '-'}")


def seed_data() -> None:
    count = get_conn().execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    if count > 0: return
    for title, desc, priority, requester, category in [
        ("Login page not working", "Users cannot log in after update", "critical", "Alice", "Bug"),
        ("Update email template",  "Marketing team needs new layout",   "medium",   "Bob",   "Feature"),
        ("Database slow queries",  "Reports take 5+ minutes",           "high",     "Carol", "Performance"),
        ("Add dark mode",          "User request for dark theme",        "low",      "Dave",  "Feature"),
        ("Password reset broken",  "Reset emails not being sent",       "high",     "Alice", "Bug"),
    ]:
        create_ticket(title, desc, priority, requester, category)
    assign_ticket(1, "Dev Team")
    add_comment(1, "Dev Team", "Investigating the authentication module.")
    update_status(3, "in_progress")
    assign_ticket(3, "DBA Team")
    print("  Sample tickets loaded.")


def main():
    init_db()
    seed_data()

    print("=" * 65)
    print("  TICKET MANAGEMENT SYSTEM")
    print("=" * 65)

    while True:
        stats = dashboard_stats()
        print(f"\n  Total: {stats['total']} | Open: {stats['by_status'].get('open',0)} | "
              f"In Progress: {stats['by_status'].get('in_progress',0)} | "
              f"Overdue: {stats['overdue']}")

        print("\n  [1] View Tickets    [2] Create Ticket   [3] View Ticket")
        print("  [4] Assign Ticket   [5] Update Status   [6] Add Comment")
        print("  [7] Overdue Tickets [8] Dashboard       [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            status   = input("  Filter status (blank=all): ").strip() or None
            priority = input("  Filter priority (blank=all): ").strip() or None
            display_tickets_list(list_tickets(status=status, priority=priority))

        elif choice == "2":
            title       = input("  Title: ").strip()
            description = input("  Description: ").strip()
            print(f"  Priorities: {', '.join(p.value for p in Priority)}")
            priority    = input("  Priority [medium]: ").strip() or "medium"
            requester   = input("  Requester name: ").strip()
            category    = input("  Category [General]: ").strip() or "General"
            tid = create_ticket(title, description, priority, requester, category)
            print(f"  Ticket #{tid} created.")

        elif choice == "3":
            try:
                tid    = int(input("  Ticket ID: "))
                ticket = get_ticket(tid)
                if ticket:
                    display_ticket(ticket)
                    comments = get_conn().execute(
                        "SELECT * FROM comments WHERE ticket_id=?", (tid,)
                    ).fetchall()
                    if comments:
                        print("\n  COMMENTS:")
                        for c in comments:
                            print(f"  [{c['created_at'][:10]}] {c['author']}: {c['body']}")
                else:
                    print("  Ticket not found.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "4":
            try:
                tid   = int(input("  Ticket ID: "))
                agent = input("  Assign to: ").strip()
                print("  Assigned." if assign_ticket(tid, agent) else "  Could not assign.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "5":
            try:
                tid        = int(input("  Ticket ID: "))
                print(f"  Statuses: {', '.join(s.value for s in Status)}")
                new_status = input("  New status: ").strip()
                print("  Updated." if update_status(tid, new_status) else "  Not found.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "6":
            try:
                tid    = int(input("  Ticket ID: "))
                author = input("  Your name: ").strip()
                body   = input("  Comment: ").strip()
                add_comment(tid, author, body)
                print("  Comment added.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "7":
            display_tickets_list(overdue_tickets())

        elif choice == "8":
            stats = dashboard_stats()
            print("\n  DASHBOARD")
            print(f"  Total tickets:         {stats['total']}")
            print(f"  By status:             {stats['by_status']}")
            print(f"  By priority:           {stats['by_priority']}")
            print(f"  Overdue:               {stats['overdue']}")
            print(f"  Avg resolution (hrs):  {stats['avg_resolution_hours']}")

        elif choice == "0":
            print("  Goodbye!")
            break


if __name__ == "__main__":
    main()
