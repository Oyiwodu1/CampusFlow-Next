import unittest

from campusflow.reports import generate_ticket_report


class TestTicketReports(unittest.TestCase):

    def test_generate_ticket_report(self):
        tickets = [
            {
                "id": 1,
                "status": "open",
                "priority": "critical",
            },
            {
                "id": 2,
                "status": "in_progress",
                "priority": "high",
            },
            {
                "id": 3,
                "status": "resolved",
                "priority": "medium",
            },
            {
                "id": 4,
                "status": "open",
                "priority": "low",
            },
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(report["total_tickets"], 4)
        self.assertEqual(report["open"], 2)
        self.assertEqual(report["in_progress"], 1)
        self.assertEqual(report["resolved"], 1)
        self.assertEqual(report["critical"], 1)
        self.assertEqual(report["high"], 1)
        self.assertEqual(report["medium"], 1)
        self.assertEqual(report["low"], 1)

    def test_empty_ticket_list(self):
        report = generate_ticket_report([])

        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(report["open"], 0)
        self.assertEqual(report["in_progress"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["critical"], 0)
        self.assertEqual(report["high"], 0)
        self.assertEqual(report["medium"], 0)
        self.assertEqual(report["low"], 0)

    def test_all_tickets_have_same_status_and_priority(self):
        tickets = [
            {
                "id": 1,
                "status": "open",
                "priority": "high",
            },
            {
                "id": 2,
                "status": "open",
                "priority": "high",
            },
        ]

        report = generate_ticket_report(tickets)

        self.assertEqual(report["total_tickets"], 2)
        self.assertEqual(report["open"], 2)
        self.assertEqual(report["in_progress"], 0)
        self.assertEqual(report["resolved"], 0)
        self.assertEqual(report["high"], 2)

    def test_report_does_not_modify_tickets(self):
        tickets = [
            {
                "id": 1,
                "status": "resolved",
                "priority": "critical",
            }
        ]

        original_tickets = [ticket.copy() for ticket in tickets]

        generate_ticket_report(tickets)

        self.assertEqual(tickets, original_tickets)


if __name__ == "__main__":
    unittest.main()