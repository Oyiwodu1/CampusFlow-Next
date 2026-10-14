all_tickets = []
def set_tickets(tickets):
    global all_tickets
    all_tickets = tickets

def add_note(ticket_id, author, message):
    ticket_found = None

    for ticket in all_tickets:
        if ticket["id"] == ticket_id:
            ticket_found = ticket
            break

    if ticket_found is None:
        print("Ticket not found!")
        return

    if ticket_found["status"] == "resolved":
        print("Resolved tickets must be reopened before adding notes")
        return

    