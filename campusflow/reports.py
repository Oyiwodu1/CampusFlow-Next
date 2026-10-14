def generate_ticket_report(tickets):
    report = {
        "total_tickets": len(tickets),
        "open": 0,
        "in_progress": 0,
        "resolved": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]
        if status == "open":
            report["open"] += 1
        elif status == "in_progress":
            report["in_progress"] += 1
        elif status == "resolved":
            report["resolved"] += 1
        if priority == "critical":
            report["critical"] += 1
        elif priority == "high":
            report["high"] += 1
        elif priority == "medium":
            report["medium"] += 1
        elif priority == "low":
            report["low"] += 1

    return report

#new modification
def count_by_category(tickets):
 #Return a dict of category -> count.
    counts = {}
    for ticket in tickets:
        category = ticket.get("category", "Unknown")
        counts[category] = counts.get(category, 0) + 1
    return counts


def resolution_percentage(tickets):
 #Percent of tickets resolved, rounded to 2 decimal places. 0.0 if no tickets.
    total = len(tickets)
    if total == 0:
        return "0.0"
    resolved = sum(1 for t in tickets if t.get("status") == "resolved")
    return round((resolved / total) * 100, 2)


def generate_detailed_report(tickets):
 #Enhanced report: base summary + unresolved, categories, resolution %.
    base = generate_ticket_report(tickets)
    base["unresolved_tickets"] = base["open"] + base["in_progress"]
    base["resolved_tickets"] = base["resolved"]
    base["categories"] = count_by_category(tickets)
    base["resolution_percentage"] = resolution_percentage(tickets)
    return base
