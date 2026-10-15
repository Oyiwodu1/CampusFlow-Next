from campusflow.tickets import create_ticket
from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import (
    assign_ticket,
    update_ticket_status,
    reopen_ticket,
    get_work_queue,
)
from campusflow.reports import generate_ticket_report
from campusflow.search import search_tickets                #added imports
from campusflow.reports import generate_detailed_report
from campusflow.understanding_check import QUESTIONS, score_answers

def display_ticket_report(tickets):
    report = generate_ticket_report(tickets)

    print("\n------- TICKET REPORT -------")
    print(f"Total tickets: {report['total_tickets']}")

    print("\nTickets by status:")
    print(f"Open: {report['open']}")
    print(f"In progress: {report['in_progress']}")
    print(f"Resolved: {report['resolved']}")

    print("\nTickets by priority:")
    print(f"Critical: {report['critical']}")
    print(f"High: {report['high']}")
    print(f"Medium: {report['medium']}")
    print(f"Low: {report['low']}")


def display_all_tickets(tickets):
    if not tickets:
        print("No tickets have been created yet.")
        return

    for ticket in tickets:
        print("\n------------------------------")
        print(f"ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Category: {ticket['category']}")
        print(f"Urgency: {ticket['urgency']}")
        print(f"Affected users: {ticket['affected_users']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")
        print(f"Assigned to: {ticket['assigned_to']}")

def search_tickets_cli(tickets):
    #Interactive search over tickets using combined filters
    print("\n==== SEARCH TICKETS ====")
    print("Press Enter on any prompt to skip that filter.\n")

    query = input("Title contains: ").strip() or None
    category = input("Category (Network/Hardware/Software/Other): ").strip() or None
    status = input("Status (open/in_progress/resolved): ").strip() or None
    priority = input("Priority (critical/high/medium/low): ").strip() or None

    results = search_tickets(
        tickets,
        search_word=query,
        category=category,
        status=status,
        priority=priority,
    )

    if not results:
        print("\nNo tickets matched your search.")
        return

    print(f"\n{len(results)} ticket(s) matched:")
    for ticket in results:
        print("\n------------------------------")
        print(f"ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Category: {ticket['category']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")
        print(f"Assigned to: {ticket['assigned_to']}")


def detailed_report_cli(tickets):
    #Print the extended report: category counts, unresolved, resolution %.
    report = generate_detailed_report(tickets)

    print("\n------- DETAILED TICKET REPORT -------")
    print(f"Total tickets: {report['total_tickets']}")

    print("\nTickets by status:")
    print(f"Open: {report['open']}")
    print(f"In progress: {report['in_progress']}")
    print(f"Resolved: {report['resolved']}")
    print(f"Unresolved (open + in progress): {report['unresolved_tickets']}")
    print(f"Resolved: {report['resolved_tickets']}")

    print("\nTickets by priority:")
    print(f"Critical: {report['critical']}")
    print(f"High: {report['high']}")
    print(f"Medium: {report['medium']}")
    print(f"Low: {report['low']}")

    print("\nTickets by category:")
    for category, count in report["categories"].items():
        print(f"{category}: {count}")

    print(f"\nResolution: {report['resolution_percentage']}%")


def understanding_check_cli():
    # Run the six-question Engineering Understanding Check.
    print("\n------- ENGINEERING UNDERSTANDING CHECK -------")
    print("Answer each question with A, B, C or D.")

    answers = []
    for index, question in enumerate(QUESTIONS, start=1):
        print(f"\nQ{index}. {question['prompt']}")
        
    # Always deisplay options in A, B, C, D order, regardless of dict insertion order
        for letter in sorted(question["options"].keys()):
            text = question["options"][letter]
            print(f"{letter}. {text}")

        while True:
            choice = input("Your answer (A/B/C/D): ").strip().upper()
            if choice in ("A", "B", "C", "D"):
                answers.append(choice)
                break
            print("Invalid choice. Please enter A, B, C or D.")

    score, per_question = score_answers(answers)
    total = len(QUESTIONS)
    print(f"\nYou scored {score} out of {total}.")

    print("\nReview:")
    for entry in per_question:
        mark = "correct" if entry["is_correct"] else "wrong"
        print(f"\n  {entry['id']} - {mark}")
        print(f"Your answer: {entry['submitted']}")
        print(f"Correct answer: {entry['correct']}")
        print(f"{entry['explanation']}")


def main():
    try:
        all_tickets = load_tickets()
    except ValueError as error:
        print(f"Unable to load saved tickets: {error}")
        return

    campus = 0

    while campus != 7:
        print("\n======= WELCOME TO CAMPUSFLOW =======")
        print("1. Create a ticket")
        print("2. View all tickets")
        print("3. Assign or reassign a ticket")
        print("4. Update ticket status")
        print("5. View work queue")
        print("6. Generate ticket report")
        print("7. Exit")

        try:
            campus = int(input("Choose an option (1-7): "))
        except ValueError:
            print("Kindly enter a valid number.")
            continue

        if campus == 1:
            print("\nYou selected Create a ticket.")

            title = input("Enter ticket title: ")
            has_digit = False
            for char in title:
                if char.isdigit():
                    has_digit = True
            while title.strip() == "" or has_digit:
                print("Enter a valid ticket title!")
                title = input("Enter ticket title: ")
                has_digit = False
                for char in title:
                    if char.isdigit():
                        has_digit = True

            category = input("Enter ticket category(software/Hardware/Network/other): ")
            while category.strip() == "" or category.strip().title() not in ["Network", "Hardware", "Software", "Other"]:
                print("Invalid category.")
                category = input("Enter ticket category(software/Hardware/Network/other): ")

            urgency = input("Enter urgency (low/medium/high): ")
            while urgency.strip().lower() not in ["low", "medium", "high"]:
                print("Invalid urgency.")
                urgency = input("Enter urgency (low/medium/high): ")

            while True:
                try:
                    affected_users = int(
                        input("How many users are being affected?: ")
                    )
                    if affected_users > 0:
                        break

                    print("Please enter a number greater than zero.")

                except ValueError:
                    print("Check your input and try again.")

            ticket = create_ticket(
                title,
                category,
                urgency,
                affected_users,
                all_tickets,
            )

            if ticket is not None:
                all_tickets.append(ticket)
                save_tickets(all_tickets)

                print("Ticket created successfully.")
                print(f"Ticket ID: {ticket['id']}")
                print(f"Title: {ticket['title']}")
                print(f"Category: {ticket['category']}")
                print(f"Urgency: {ticket['urgency']}")
                print(f"Affected users: {ticket['affected_users']}")
                print(f"Status: {ticket['status']}")
                print(f"Assigned to: {ticket['assigned_to']}")
                print(f"Priority: {ticket['priority']}")

        elif campus == 2:
            display_all_tickets(all_tickets)

        elif campus == 3:
            assign_ticket(all_tickets)
            save_tickets(all_tickets)

        elif campus == 4:
            print("\n1. Update status")
            print("2. Reopen a resolved ticket")

            status_choice = input("Choose an option: ").strip()

            if status_choice == "1":
                update_ticket_status(all_tickets)
                save_tickets(all_tickets)

            elif status_choice == "2":
                reopen_ticket(all_tickets)
                save_tickets(all_tickets)

            else:
                print("Invalid choice.")

        elif campus == 5:
            work_queue = get_work_queue(all_tickets)
            if not work_queue:
                print("There are no open tickets in the work queue.")
            else:
                print("\n------- WORK QUEUE -------")
                
                for ticket in work_queue:
                    print("\n------------------------------")
                    print(f"ID: {ticket['id']}")
                    print(f"Title: {ticket['title']}")
                    print(f"Priority: {ticket['priority']}")
                    print(f"Status: {ticket['status']}")
                    print(f"Assigned to: {ticket['assigned_to']}")

        elif campus == 6:
            display_ticket_report(all_tickets)

        elif campus == 7:
            save_tickets(all_tickets)
            print("Thank you for using CampusFlow!")

        else:
            print("Enter a number from 1 to 7.")

if __name__ == "__main__":
    main()