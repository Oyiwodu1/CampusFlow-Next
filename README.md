# CampusFlow Next — Campus Technical Support Ticket Manager

## About the Project

CampusFlow Next is a Python command-line application that helps campus technical
support staff manage incoming support requests: Wi-Fi outages, faulty laptops,
broken development environments, and inaccessible platforms. Informal reports
get lost — CampusFlow Next records every request, calculates its priority,
assigns responsibility, tracks progress through a defined lifecycle, and keeps
structured follow-up notes so work is never lost between shifts.

This is an upgrade of the original CampusFlow sprint project. It adds
multi-filter search, expanded reporting, safe JSON persistence, structured
ticket notes, and an interactive engineering-understanding check, all within
the original learning boundaries: Python standard library only, no web
frameworks, no external databases, no paid APIs.

## Team Members
**Engineer A - Faith Owoicho  
ROLES: Ticket validation and lifecycle safety, notes data model, JSON load validation, CLI menu wiring for notes 
**Engineer B - Omale Moses 
ROLES: Search and combined filtering, extended reports and analytics, interactive engineering-understanding check, notes CLI integration

## Both engineers authored code, wrote automated tests, opened a substantial PR,
and reviewed the other's PR before merge.

## Requirements

- Python 3.10 or later (uses `.casefold()`, f-strings, `unittest`).
- No third-party packages — standard library only (`json`, `unittest`, `os`,
  `pathlib`, `tempfile`).

## Setup

```bash
git clone https://github.com/Oyiwodu1/CampusFlow-Next.git
cd CampusFlow-Next
python3 main.py
On systems where Python is invoked as python:

bash
python main.py
Running the Application
Launch the CLI:

bash
python3 main.py
The menu provides:

text
1.  Create a ticket
2.  View all tickets
3.  Assign or reassign a ticket
4.  Update ticket status
5.  View work queue
6.  Generate ticket report
7.  Search tickets
8.  Detailed ticket report
9.  Engineering Understanding Check
10. Add follow-up note
11. View ticket notes
12. Exit
Menu highlights
Search tickets (7) — case-insensitive substring match on title, combined
with optional exact filters on category, status, and priority. All supplied
filters must match (AND). Leave any prompt blank to skip that filter.

Detailed ticket report (8) — total tickets, counts by status, priority
and category, unresolved count (open + in_progress), resolved count, and
resolution percentage. Empty dataset reports 0% without crashing.

Engineering Understanding Check (9) — six multiple-choice questions about
how CampusFlow behaves. Answers accept A/B/C/D (case-insensitive). Invalid
input is rejected and re-prompted. After scoring, you're asked to reflect on
two answers in your own words — reflections are stored for mentor discussion
and are not auto-graded.

Add follow-up note (10) — attach a note to an open or in_progress ticket.
Author must be non-empty; message length 5–300 characters after trimming.
Resolved tickets reject notes until reopened.

View ticket notes (11) — list all notes for a ticket in ID order
(N001, N002, ...).

## Business Rules:
Priority Calculation: Priority is calculated from urgency and affected_users, checked in this
order; the first matching rule wins:

Condition	Priority
urgency == "high" AND affected_users >= 10	critical
urgency == "high" OR affected_users >= 10	high
urgency == "medium" OR affected_users >= 3	medium
otherwise	low

Ticket Lifecycle:
open → in_progress → resolved
                   ↘
          (reopen) → open
An unassigned ticket cannot move to in_progress.

A resolved ticket cannot be reassigned or modified until it is reopened.

Reopening sets status back to open.

Rules to add note:

Notes can only be added when status is open or in_progress.
A resolved ticket rejects notes until reopened.
A rejected note does not consume a note ID.
Note IDs are per-ticket and sequential: N001, N002, ...
Notes survive resolve, reopen, save, and reload.

Work Queue
The work queue shows only open tickets, sorted by priority
(critical → high → medium → low), with ties broken by numeric ticket ID
(earliest first).

Data Persistence
Tickets are stored in:

text
data/tickets.json
The file is created automatically on first save. Each ticket is a JSON object
with these fields:

json
{
    "id": "T001",
    "title": "Wi-Fi down in ICT",
    "category": "Network",
    "urgency": "high",
    "affected_users": 12,
    "priority": "critical",
    "status": "open",
    "assigned_to": null,
    "notes": [
        {"note_id": "N001", "author": "Mentor A", "message": "Router reboot attempted"}
    ]
}
To start afresh: stop the application and delete data/tickets.json. On next
launch, CampusFlow starts with an empty ticket collection. Ticket IDs and note
IDs generate correctly after reload — they never collide with existing records.

Malformed JSON: if data/tickets.json cannot be parsed, the application
refuses to load and shows a clear error rather than silently erasing data.

Running the Tests:

bash
python3 -m unittest discover -s tests -v

The suite covers:
Priority rules and boundary cases (original CampusFlow regression tests)
Ticket validation: blank title, invalid category/urgency, zero, negative,
float, and boolean affected_users
Lifecycle: unassigned tickets cannot start, resolved tickets cannot skip
reopening, reassignment of resolved tickets is rejected
JSON persistence: missing file, malformed JSON, non-list payloads, non-dict
entries, save/reload round-trip
Search: title substring case-insensitivity, combined AND filters, empty
filters, unknown query, read-only guarantee
Reports: category counts, unresolved count, resolution percentage, empty
dataset (0% without crash), original report shape unchanged
Understanding check: scoring, invalid input handling, question bank shape
Notes: validation, sequential IDs, rejected note does not consume ID,
resolved-ticket rejection, reopen-then-accept, save/reload round-trip

Expected result: Ran 90 tests ... OK.

Project Structure:

CampusFlow-Next/
├── main.py
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── storage.py
│   ├── reports.py
│   ├── search.py
│   ├── notes.py
│   └── understanding_check.py
├── tests/
│   ├── __init__.py
│   ├── test_tickets.py
│   ├── test_workflow.py
│   ├── test_storage_persistence.py
│   ├── test_reports.py
│   ├── test_search.py
│   ├── test_notes.py
│   └── test_understanding_check.py
├── docs/
│   ├── baseline-check.md
│   ├── design-decisions.md
│   ├── ai-learning-log.md
│   └── engineer-b-reflections.md
├── data/
│   └── tickets.json         (gitignored — generated locally)
├── .gitignore
└── README.md


## Known Limitations

Title search is substring-only. No fuzzy matching or typo correction —
typing "wi-fi" will not match "wifi".

load_tickets does not deep-validate note shapes on load. It verifies
the payload is a list of dicts, but not that each ticket's notes entries
have valid note_id/author/message fields.

No concurrency protection. Two simultaneous instances writing to the same
JSON file would race. Out of scope for a single-user CLI.

No timestamps or activity history on tickets or notes.

Future Improvements
Move persistence to SQLite for atomic writes and query support.

Add ticket timestamps and per-ticket history.

Expand search to cover note text and assignee names.

Add a small staff name registry to avoid typos in the assignee field.

Add more comprehensive JSON schema validation on load.

Reviewed Pull Requests
Engineer B feature PR: PR #8 — feat: add search, extended reports, understanding check, and structured notes

Engineer A feature PR: PR #9 — feat: add notes data model validation and get_notes helper

Both PRs were reviewed line-by-line by the other engineer, approved, and merged
into main.


License
No license has been specified for this project. An appropriate license can be added if the team intends to distribute or reuse the software publicly.
