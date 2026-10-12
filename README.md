# CampusFlow — Campus Technical Support Ticket Manager

## About the Project

CampusFlow is a Python-based command line application designed to help campus technical support teams manage technical support requests efficiently.
The application allows users to create support tickets, calculate their priority, assign tickets to staff members, track their progress, organize a work queue, generate reports, and save ticket records for future use.
Common problems managed by CampusFlow include Wi-Fi is down, broken laptops, software issues, and inaccessible development platforms.

This project was developed as part of an engineering sprint to demonstrate problem-solving, modular programming, workflow management, data persistence, automated testing, and collaborative software development.

## Project Objectives
The main objectives of CampusFlow are to:

- Record technical support requests in a structured format.
- Generate unique identifiers for tickets.
- Calculate ticket priority based on urgency and the number of affected users.
- Assign tickets to responsible staff members.
- Track ticket progress through defined statuses.
- Organize open tickets by priority.
- Generate reports showing ticket statistics.
- Save ticket information using JSON persistence.
- Load previously saved tickets when the application starts.
- Validate user input and handle errors appropriately.
- Apply software engineering practices, including testing and version control.

## Features

## 1. Ticket Creation

Users can create support tickets by providing the following information:

- Ticket title
- Ticket category
- Urgency level
- Number of affected users

Each ticket receives a unique ticket ID.

### 2. Automatic Priority Calculation

CampusFlow calculates ticket priority using the urgency level and the number of affected users.

The supported priority levels are:

- **Critical**
- **High**
- **Medium**
- **Low**

This helps support teams identify and prioritize important issues.

### 3. Ticket Assignment and Reassignment

Tickets can be assigned to staff members responsible for resolving reported problems.

Existing assignments can also be changed when responsibility needs to be transferred.

### 4. Ticket Status Management

CampusFlow supports three ticket statuses:

- open — The ticket has been created and is awaiting work.
- in_progress — A staff member is working on the ticket.
- resolved — The reported issue has been resolved.
Resolved tickets can be reopened when further work is required.

### 5. Priority-Based Work Queue
The work queue organizes open tickets according to priority.
Tickets are arranged in the following order:

1. Critical
2. High
3. Medium
4. Low
When tickets have the same priority, their numeric ticket IDs determine their order.

### 6. Ticket Reports
The reporting feature summarizes ticket information, including:

- Total number of tickets
- Number of open tickets
- Number of in-progress tickets
- Number of resolved tickets
- Number of critical-priority tickets
- Number of high-priority tickets
- Number of medium-priority tickets
- Number of low-priority tickets
These reports help users understand the current state of the support workload.

### 7. JSON Data Persistence

CampusFlow stores ticket records in JSON format.

The application loads previously saved tickets when it starts and saves ticket changes so that records remain available after the application closes.
If the data file does not exist, the application starts with an empty collection of tickets.

### 8. Input Validation and Error Handling
The application validates ticket information to reduce invalid entries.
It also handles invalid menu selections and reports problems encountered when loading saved JSON data.

### 9. Automated Testing
CampusFlow uses Python's built-in unittest framework to test application functionality and help identify errors.

## Technologies Used
- **Python 3:** Main programming language.
- **JSON:** Format for storing ticket records.
- **unittest:** Framework for automated testing.
- **Git:** Version control system.
- **GitHub:** Platform for collaborative development and code hosting.
- **Visual Studio Code:** Development environment.

## Project Structure

CampusFlow-team/
│
├── main.py
│
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   ├── storage.py
│   └── reports.py
│
├── tests/
│   ├── __init__.py
│   ├── test_tickets.py
│   ├── test_workflow.py
│   ├── test_storage.py
│   ├── test_reports.py
│   └── test_storage_persistence.py
│
├── data/
│   └── tickets.json
│
├── docs/
│
├── .gitignore
└── README.md

**Note:** The data/ directory may be generated locally when the application saves tickets. It is excluded from version control to avoid committing local runtime data.

## Requirements
To run CampusFlow, you need:
- Python 3 installed on your computer.
- A terminal or command-line interface.
- Git, if you want to clone the repository and contribute to development.
The application uses Python's standard library and does not require third-party packages for its core functionality.

## Installation and Setup

### Step 1: Clone the Repository

Clone the team's GitHub repository:

bash
git clone https://github.com/ZachOG10/CampusFlow-team.git

### Step 2: Navigate to the Project Directory

bash
cd CampusFlow-team


### Step 3: Run the Application

On Linux and macOS, run:

bash
python3 main.py

On systems where Python is invoked using python, you can run:

bash
python main.py

### Step 4: Use the Application

Follow the menu displayed in the terminal to:

1. Create a ticket.
2. View all tickets.
3. Assign or reassign a ticket.
4. Update a ticket's status or reopen a resolved ticket.
5. View the work queue.
6. Generate a ticket report.
7. Exit the application.

## Running the Tests

CampusFlow uses Python's built-in unittest framework.

To run the complete test suite, execute:

bash
python3 -m unittest discover -s tests -v

The -v option enables verbose output, displaying individual test results.

A successful test run should finish with:

text

OK

The number of tests may change as additional tests are added to the project.

## Data Persistence

CampusFlow stores ticket records in:

text
data/tickets.json

The application loads saved records at startup and saves changes during use.

The storage component supports the following behavior:
- Load previously saved tickets.
- Start with an empty ticket collection when the data file is missing.
- Save ticket records in JSON format.
- Report invalid JSON data instead of silently ignoring it.

The data/ directory is excluded from version control because it contains locally generated application data.

## Team Members

### 1. Aondowase Zachariah

**Role:** Software Engineering Fellow

**Email:** [aondowasezachariahog@gmail.com](mailto:aondowasezachariahog@gmail.com)

**Areas of Contribution:**
- Ticket assignment and reassignment.
- Ticket status transitions and reopening.
- Priority-based work queue.
- Ticket reporting.
- JSON persistence integration.
- Application integration and testing.

### 2. Faith Owoicho

**Role:** Software Engineering Fellow

**Email:** [phatewodu@gmail.com](mailto:phatewodu@gmail.com)

**Areas of Contribution:**
- Ticket creation and validation.
- Ticket data structure.
- Automatic priority calculation.
- Supporting application components and testing.

## Learning Outcomes

The development of CampusFlow provides practical experience in:
- Computational thinking and problem decomposition.
- Python functions and modules.
- Lists and dictionaries.
- Conditional statements and loops.
- Input validation and exception handling.
- File handling and JSON serialization.
- Data persistence.
- Automated unit testing.
- Version control with Git.
- Collaborative software development.
- Debugging and application integration.

## Future Improvements

Possible future enhancements include:
- A graphical user interface or web application.
- Staff authentication and account management.
- Ticket search and filtering.
- Ticket creation timestamps and activity history.
- Additional reporting and analytics.
- More comprehensive validation of saved ticket records.
- Database integration.
- Improved protection against duplicate IDs when multiple application instances create tickets simultaneously.
- Expanded automated test coverage

## Project Status

CampusFlow is a command line technical support ticket management application developed as an engineering sprint project.

It brings together ticket creation, priority calculation, assignment, workflow management, reporting, automated testing, and JSON-based data persistence.

The application provides a foundation for future improvements and additional support-management features.

## License

No license has been specified for this project. An appropriate license can be added if the team intends to distribute or reuse the software publicly.
