# CampusFlow — Design Decisions

## 1. Project Overview

CampusFlow is a Python command-line helpdesk ticket management application. It helps campus staff record technical problems, calculate ticket priorities, assign tickets to staff, manage ticket status, generate reports, and store ticket records using JSON.

The project uses Python's standard library and a modular structure so that ticket creation, workflow, reports, storage, and the command-line interface can be developed and tested separately.

## 2. Team Responsibilities

The project uses shared ownership for integration and clearly divided feature responsibilities.

### Engineer A — Ticket Creation and Validation

Engineer A is responsible for:
- Creating tickets with unique identifiers.
- Validating ticket titles, categories, urgency levels, and affected-user counts.
- Normalizing valid category and urgency inputs.
- Calculating ticket priority according to the assessment rules.
- Writing and running unit tests for ticket creation and validation.

### Engineer B — Workflow and Reports

Engineer B is responsible for:
- Assigning and reassigning tickets to staff members.
- Managing ticket status transitions and reopening resolved tickets.
- Implementing the work queue and reports.
- Writing and running matching workflow and reporting tests.

### Shared Responsibilities

Both engineers are responsible for:
- Agreeing on shared data structures and function contracts.
- Integrating JSON persistence and the command-line interface.
- Reviewing each other's pull requests before merging.
- Testing the complete application after integration.
- Maintaining the design documentation and individual AI learning logs.

## 3. Project Structure

The project is organized into modules with separate responsibilities.

- `main.py` — provides the command-line menu and connects user actions to the application functions.
- `campusflow/tickets.py` — creates tickets, validates inputs, calculates priority, and generates ticket IDs.
- `campusflow/workflow.py` — assigns tickets, updates ticket status, and reopens resolved tickets.
- `campusflow/reports.py` — provides reporting and related ticket summaries.
- `campusflow/storage.py` — handles reading and writing ticket data using JSON.
- `tests/test_tickets.py` — tests ticket creation, input validation, normalization, and priority calculation.
- `tests/test_workflow.py` — tests ticket assignment, reassignment, status changes, and reopening.
- `tests/test_reports.py` — tests reporting behaviour.
- `tests/test_storage_persistence.py` — tests JSON storage and persistence behaviour.

This structure separates application responsibilities and makes the individual features easier to test and maintain.

## 4. Ticket Data Structure

Each ticket is represented as a Python dictionary. The agreed ticket fields are:

- `id` — a unique identifier such as `T001`.
- `title` — a description of the reported problem.
- `category` — the type of technical problem.
- `urgency` — the reported urgency level.
- `affected_users` — the positive integer number of users affected.
- `priority` — the calculated priority level.
- `status` — the ticket's current lifecycle status.
- `assigned_to` — the assigned staff member's name, or `None` when unassigned.

New tickets start with `status` set to `"open"` and `assigned_to` set to `None`.

The ticket collection is a list of ticket dictionaries. Functions that operate on existing tickets receive the shared collection instead of creating a separate collection.

Ticket IDs must remain unique, including when previously saved tickets are loaded after the application restarts.

## 5. Input Validation and Priority Rules

The ticket-creation function validates input before returning a new ticket.

The accepted categories are:
- `Network`
- `Hardware`
- `Software`
- `Other`

The accepted urgency levels are:
- `low`
- `medium`
- `high`

Valid category and urgency inputs are normalized to a consistent format. A blank title is rejected. The number of affected users must be a positive integer; zero, negative values, decimals, text, and Boolean values must not be accepted as valid affected-user counts.

The priority calculation follows the exact order specified in the assessment:

1. If urgency is `high` and at least 10 users are affected, priority is `critical`.
2. Otherwise, if urgency is `high` or at least 10 users are affected, priority is `high`.
3. Otherwise, if urgency is `medium` or at least 3 users are affected, priority is `medium`.
4. All remaining valid tickets receive `low` priority.

The order matters because the first matching rule determines the priority.

For invalid ticket input, the ticket-creation function returns `None` and displays an appropriate validation message. For valid input, it returns the created ticket dictionary.

## 6. Workflow and Status Decisions

The ticket lifecycle uses the following statuses:

- `open`
- `in_progress`
- `resolved`

The supported workflow is:

`open → in_progress → resolved`

An unassigned ticket cannot be moved to `in_progress`. A ticket must be assigned before work can begin.

Only an `in_progress` ticket can be resolved. A resolved ticket cannot move directly to another status. It must first be explicitly reopened, which changes its status back to `open`.

Unknown ticket IDs and invalid status transitions are rejected with useful messages. These rules help prevent invalid changes to ticket records.

Ticket assignment requires a non-empty staff name. If a ticket is assigned to another staff member, the new assignee replaces the previous assignee, consistent with the implemented reassignment behaviour.

Workflow functions receive the ticket collection and modify the relevant ticket dictionary in place.

## 7. Work Queue and Reporting Decisions

The work queue is intended to show open, unresolved tickets in priority order:

`critical → high → medium → low`

Tickets with equal priority should be ordered by their numeric ticket ID, with the earlier ticket ID first.

Reports should provide the total number of tickets and breakdowns by status and priority. Reports must also handle an empty ticket collection without failing.

Reporting operations should not unexpectedly modify the original ticket records.

The complete queue and reporting behaviour must be checked against these requirements during integration.

## 8. JSON Persistence Decisions

The storage module is responsible for JSON persistence so that file-handling logic is not duplicated across the application.

The intended persistence behaviour is:

- Load previously saved tickets when the application starts.
- Start with an empty ticket list when the storage file does not exist.
- Save ticket records in JSON format.
- Reload saved ticket records without losing their data.
- Produce a clear error when the JSON file is malformed rather than silently discarding existing data.
- Validate that loaded JSON has the expected structure.
- Preserve unique ticket IDs when creating additional tickets after reloading saved data.

The command-line interface and workflow functions should use the same loaded ticket collection. Successful changes to ticket records must be saved so that they are retained after the application exits.

The storage module is the central place for JSON read and write operations. Its function names and exact save timing should match the implementation agreed upon by both engineers.

## 9. Command-Line Interface Decisions

CampusFlow uses a text-based command-line interface rather than a graphical interface or website.

The CLI acts as the entry point for users and connects the ticket, workflow, reporting, and storage modules.

The menu should continue running until the user selects Exit. Invalid menu choices should display a message rather than unexpectedly terminate the program.

The complete menu should make all required features accessible:
- Create and view tickets.
- Assign or reassign tickets.
- Update ticket status and reopen resolved tickets.
- View the work queue.
- Generate reports.
- Exit the application.

The menu must use the shared ticket collection and coordinate with the storage module so that changes persist after the program closes.

## 10. Testing and Verification

Automated tests are written using Python's `unittest` framework. The tests cover normal behaviour, invalid inputs, workflow rules, report generation, and JSON persistence.

The most recent full test command run after integrating the changes was:

`python3 -m unittest discover -s tests -v`

The observed result was:

`Ran 29 tests ... OK`

This confirms that all 29 tests discovered in that run passed. It does not, by itself, prove that every end-to-end requirement is satisfied.

The remaining integration checks are:
- Run the complete CLI from a clean start.
- Verify that the CLI exposes every required feature.
- Create, save, and reload tickets through the application.
- Verify that ticket IDs remain unique after reloading saved records.
- Confirm that the work queue uses priority and numeric ticket ID ordering.
- Run the full test suite again after any integration changes.

## 11. Git and Pull Request Decisions

Both engineers work on feature branches to keep individual contributions traceable.

Each engineer authors a pull request for their feature work, reviews the other engineer's pull request, and runs the relevant tests where practical. Changes are merged only after review and the resolution of blocking issues.

When one feature branch falls behind `main`, it should be updated from the latest `main` branch. Conflicts must be resolved carefully, and the affected tests must be run again before the updated work is considered ready.

The team should use meaningful commit messages and ensure that the final integrated application is tested on the latest `main` branch.

## 12. Known Limitations and Follow-up

The 29 passing tests are evidence of successful tests in the integrated working branch, but end-to-end CLI verification is still required.

Before final submission, the team should verify the complete menu, JSON persistence across application restarts, unique ticket IDs after reload, and work queue ordering. The final README should explain how to run the application and tests, how data is stored, and any remaining