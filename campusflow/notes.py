"""Rules (CampusFlow Next, Requirement B):
- Each ticket holds a `notes` list, initially empty.
- Each note is a dict: {"note_id": "N001", "author": str, "message": str}.
- Note IDs are per-ticket and sequential: N001, N002, ...
- Notes may only be added while a ticket is open or in_progress.
- A resolved ticket rejects notes until it is reopened.
- A rejected note does NOT consume a note ID.
- Author must be non-empty after stripping.
- Message must be 5-300 characters after stripping.
"""

MIN_MESSAGE_LENGTH = 5
MAX_MESSAGE_LENGTH = 300


def next_note_id(ticket):
    #Return the next sequential note ID (N001, N002, ...) for a ticket. Computed from the existing notes list. A ticket with 2 notes -> N003.
    
    existing = ticket.get("notes", [])
    return f"N{len(existing) + 1:03d}"


def add_note(tickets, ticket_id, author, message):
    """Append a note to the ticket with the given ID. Returns the new note dict.
    Raises ValueError if the ticket is not found, is resolved, has a blank
    author, or has a message shorter than 5 or longer than 300 characters.
    Validation happens BEFORE any mutation, and BEFORE a note ID is generated."""
   
    author = str(author).strip()
    message = str(message).strip()

    if not author:
        raise ValueError("Author cannot be blank.")
    if len(message) < MIN_MESSAGE_LENGTH:
        raise ValueError(
            f"Message must be at least {MIN_MESSAGE_LENGTH} characters."
        )
    if len(message) > MAX_MESSAGE_LENGTH:
        raise ValueError(
            f"Message must be at most {MAX_MESSAGE_LENGTH} characters."
        )

    ticket = None
    for t in tickets:
        if str(t.get("id", "")).strip().upper() == str(ticket_id).strip().upper():
            ticket = t
            break

    if ticket is None:
        raise ValueError(f"Ticket {ticket_id} not found.")

    if str(ticket.get("status", "")).strip().lower() == "resolved":
        raise ValueError("Resolved tickets must be reopened before adding notes.")

    # ID generated only after all validation has passed
    note = {
        "note_id": next_note_id(ticket),
        "author": author,
        "message": message,
    }
    ticket.setdefault("notes", []).append(note)
    return note


def get_notes(tickets, ticket_id):
    #Return the notes list for a ticket, in ID order (N001, N002, ...). Raises ValueError if the ticket is not found.
    
    for each_ticket in tickets:
        if str(each_ticket.get("id", "")).strip().upper() == str(ticket_id).strip().upper():
            return list(each_ticket.get("notes", []))
    raise ValueError(f"Ticket {ticket_id} not found.")