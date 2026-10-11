"""
CampusFlow Ticket Reports

This module generates summary reports for support tickets.
"""


def generate_ticket_report(tickets):
    """Generate a summary of tickets by status and priority."""

    report = {
        "total_tickets": len(tickets),
        "open": 0,
        "in_progress": 0,
        "resolved": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]

        # Count tickets by status.
        if status == "open":
            report["open"] += 1
        elif status == "in_progress":
            report["in_progress"] += 1
        elif status == "resolved":
            report["resolved"] += 1

        # Count tickets by priority.
        if priority == "critical":
            report["critical"] += 1
        elif priority == "high":
            report["high"] += 1
        elif priority == "medium":
            report["medium"] += 1
        elif priority == "low":
            report["low"] += 1

    return report