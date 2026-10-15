import unittest
import os
import sys
import tempfile

# Allow the test runner to resolve the campusflow package from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from campusflow.notes import add_note, get_notes, next_note_id
from campusflow.storage import save_tickets, load_tickets


def make_ticket(ticket_id="T001", status="open", notes=None):
    return {
        "id": ticket_id,
        "title": "Wi-Fi down in ICT",
        "category": "Network",
        "urgency": "high",
        "affected_users": 12,
        "priority": "critical",
        "status": status,
        "assigned_to": None,
        "notes": notes if notes is not None else [],
    }


class TestAddNote(unittest.TestCase):

    def setUp(self):
        self.tickets = [make_ticket("T001")]

    def test_add_note_returns_note_with_id_n001(self):
        note = add_note(self.tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Mentor A")
        self.assertEqual(note["message"], "Wi-Fi router reboot attempted")

    def test_note_is_appended_to_ticket(self):
        add_note(self.tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        #Corrected list index mapping target
        self.assertEqual(len(self.tickets[0]["notes"]), 1)
        self.assertEqual(self.tickets[0]["notes"][0]["note_id"], "N001")

    def test_second_note_gets_next_sequential_id(self):
        add_note(self.tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        note = add_note(self.tickets, "T001", "Mentor B", "Investigating switch ports")
        self.assertEqual(note["note_id"], "N002")

    def test_author_and_message_are_stripped(self):
        note = add_note(self.tickets, "T001", "  Mentor A  ", "  Wi-Fi reboot attempted  ")
        self.assertEqual(note["author"], "Mentor A")
        self.assertEqual(note["message"], "Wi-Fi reboot attempted")

    def test_blank_author_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "   ", "Wi-Fi router reboot attempted")
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_message_too_short_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Mentor A", "ok")
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_message_too_long_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Mentor A", "x" * 301)
        self.assertEqual(self.tickets[0]["notes"], [])

    def test_unknown_ticket_rejected(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T999", "Mentor A", "Wi-Fi router reboot attempted")

    def test_note_on_resolved_ticket_rejected(self):
        tickets = [make_ticket("T001", status="resolved")]
        with self.assertRaises(ValueError):
            add_note(tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        self.assertEqual(tickets[0]["notes"], [])

    def test_note_accepted_after_reopen(self):
        tickets = [make_ticket("T001", status="resolved")]
        tickets[0]["status"] = "open"
        note = add_note(tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        self.assertEqual(note["note_id"], "N001")

    def test_rejected_note_does_not_consume_id(self):
        with self.assertRaises(ValueError):
            add_note(self.tickets, "T001", "Mentor A", "ok")
        note = add_note(self.tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        self.assertEqual(note["note_id"], "N001")


class TestGetNotes(unittest.TestCase):

    def test_returns_empty_list_for_ticket_with_no_notes(self):
        tickets = [make_ticket("T001")]
        self.assertEqual(get_notes(tickets, "T001"), [])

    def test_returns_notes_in_id_order(self):
        tickets = [make_ticket("T001")]
        add_note(tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        add_note(tickets, "T001", "Mentor B", "Investigating switch ports")
        notes = get_notes(tickets, "T001")
        self.assertEqual([n["note_id"] for n in notes], ["N001", "N002"])

    def test_unknown_ticket_raises(self):
        tickets = [make_ticket("T001")]
        with self.assertRaises(ValueError):
            get_notes(tickets, "T999")

    def test_returned_list_is_a_copy(self):
        tickets = [make_ticket("T001")]
        add_note(tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        notes = get_notes(tickets, "T001")
        notes.append({"note_id": "N999"})
        self.assertEqual(len(tickets[0]["notes"]), 1)


class TestNextNoteId(unittest.TestCase):

    def test_empty_notes_gives_n001(self):
        self.assertEqual(next_note_id({"notes": []}), "N001")

    def test_two_notes_gives_n003(self):
        ticket = {"notes": [{"note_id": "N001"}, {"note_id": "N002"}]}
        self.assertEqual(next_note_id(ticket), "N003")

    def test_missing_notes_key_gives_n001(self):
        self.assertEqual(next_note_id({}), "N001")


class TestNotesPersistence(unittest.TestCase):

    def test_notes_survive_save_and_reload(self):
        tickets = [make_ticket("T001")]
        add_note(tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        add_note(tickets, "T001", "Mentor B", "Investigating switch ports")

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "tickets.json")
            save_tickets(tickets, file_path=path)
            reloaded = load_tickets(file_path=path)

        # Added structured 0-index list references
        self.assertEqual(len(reloaded[0]["notes"]), 2)
        self.assertEqual(reloaded[0]["notes"][0]["note_id"], "N001")
        self.assertEqual(reloaded[0]["notes"][1]["note_id"], "N002")

    def test_next_id_after_reload_is_correct(self):
        tickets = [make_ticket("T001")]
        add_note(tickets, "T001", "Mentor A", "Wi-Fi router reboot attempted")
        add_note(tickets, "T001", "Mentor B", "Investigating switch ports")

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "tickets.json")
            save_tickets(tickets, file_path=path)
            reloaded = load_tickets(file_path=path)

        new_note = add_note(reloaded, "T001", "Mentor C", "Replacing faulty switch")
        self.assertEqual(new_note["note_id"], "N003")


if __name__ == "__main__":
    unittest.main()
