def create_ticket(title, category, urgency, affected_users, existing_tickets=None):
    if not isinstance(title, str) or title.strip() == "":
        print("Enter a valid ticket title!")
        return None

    has_digit = False
    for char in title:
        if char.isdigit():
            has_digit = True
    if has_digit:
        print("Enter a valid ticket title!")
        return None

    title = title.strip()

    if not isinstance(category, str):
        print("Invalid category.")
        return None

    category = category.strip().title()

    if category not in ["Network", "Hardware", "Software", "Other"]:
        print("Invalid category.")
        return None

    if not isinstance(urgency, str):
        print("Invalid urgency.")
        return None

    urgency = urgency.strip().lower()

    if urgency not in ["low", "medium", "high"]:
        print("Invalid urgency.")
        return None

    if (
        not isinstance(affected_users, int)
        or isinstance(affected_users, bool)
        or affected_users <= 0
    ):
        print("Enter a valid number of affected users.")
        return None

    if urgency == "high" and affected_users >= 10:
        priority = "critical"

    elif urgency == "high" or affected_users >= 10:
        priority = "high"

    elif urgency == "medium" or affected_users >= 3:
        priority = "medium"

    else:
        priority = "low"

    if existing_tickets is None:
        existing_tickets = []

    highest_id = 0

    for existing_ticket in existing_tickets:
        ticket_id = existing_ticket.get("id", "")

        if (
            isinstance(ticket_id, str)
            and ticket_id.startswith("T")
            and ticket_id[1:].isdigit()
        ):
            number = int(ticket_id[1:])

            if number > highest_id:
                highest_id = number

    new_ticket_id = f"T{highest_id + 1:03d}"

    ticket = {
        "id": new_ticket_id,
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "status": "open",
        "assigned_to": None,
        "priority": priority,
        "notes": []
    }

    return ticket