from campusflow.tickets import create_ticket

all_tickets = []
campus = 0

while campus != 3:
    print("-------Welcome to Campus-Flow team-------")
    print("1. Create a ticket")
    print("2. View tickets")
    print("3. EXIT")
    try:
        campus = int(input("Enter 1 to create ticket, 2 to view tickets and 3 to Exit menu: "))
    except ValueError:
        print("kindly Enter a Valid Number")
        continue

    if campus == 1:
        print("You selected Create a ticket.")
        title = input("Enter ticket title: ")
        category = input("Enter ticket category: ").title()
        urgency = input("Ticket urgency: ").lower()
        while True:
            try:
                affected_users = int(input("How many users are been affected: "))
                if affected_users > 0:
                    break
                else:
                    print("Please enter a number greater than zero")
            except ValueError:
                print("check your inputs and try again")
                
        ticket = create_ticket(title, category, urgency, affected_users)

        if ticket is not None:
            all_tickets.append(ticket)
            print("Ticket created successfully")
            print(f'Ticket ID: {ticket["id"]}')
            print(f'Title: {ticket["title"]}')
            print(f'Category: {ticket["category"]}')
            print(f'Urgency: {ticket["urgency"]}')
            print(f'Affected users: {ticket["affected_users"]}')
            print(f"Status: {ticket['status']}")
            print(f"Assigned to: {ticket['assigned_to']}")
            print(f'Priority: {ticket["priority"]}')

    elif campus == 2:
        if not all_tickets:
            print("No ticket have been created yet.")
        else:
            for ticket in all_tickets:
                print(f'ID: {ticket["id"]}')
                print(f'Title: {ticket["title"]}')
                print(f'Priority: {ticket["priority"]}')
                print(f'Status: {ticket["status"]}')

    elif campus == 3:
        print("Thank you for using Campus-Flow")

    else:
        print("Enter numbers from 1-3")



