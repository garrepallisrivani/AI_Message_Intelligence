# AI Message Intelligence
# 1. Project Overview

**AI Message Intelligence** is a Python-based message processing system developed as part of an AI/ML Engineer Intern assignment.

The system processes a chronological CSV dataset containing 900 messages and converts unstructured messages into structured information.

The system performs the following operations:

- Message classification into six mandatory categories
- Classification confidence scoring
- Classification reason generation
- Sensitive information detection
- Sensitive information masking
- Sensitive information risk assessment
- Recommended security action generation
- Task extraction
- Event extraction
- Date and deadline extraction
- Time extraction
- Person extraction
- Priority determination
- Resolved/unresolved information tracking
- Structured JSON output generation
- Output validation

The six required message categories are:

1. `action_required`
2. `meeting_or_event`
3. `personal_information`
4. `general_information`
5. `promotional`
6. `sensitive_information`

The current implementation uses an **explainable rule-based approach using keywords and regular expressions**.

The main goal is to organize real-world messages into meaningful categories, extract actionable tasks and events, and protect sensitive information before it is stored in processed output.

# 2. Problem Statement

Modern users receive a large number of messages containing different types of information.

Messages may contain:

- General information
- Promotional content
- Personal information
- Meetings and events
- Tasks requiring action
- Deadlines
- Sensitive information
- Passwords
- OTPs
- Card numbers
- Phone numbers
- Email addresses
- Login credentials

Manually identifying and organizing this information can be time-consuming and error-prone.

For example, a message such as:

```text
Please join the AI workshop on 2026-09-08 at 15:00 in Conference Room 2.
```

contains useful information about an event, date, and time.

Similarly:

```text
Please send the document soon.
```

represents a task that requires action.

Another message such as:

```text
Your OTP is 482913.
```

contains sensitive information that should not be stored directly in the processed output.

This project provides an automated pipeline that analyzes each message, extracts useful structured information, and protects sensitive information by masking it.

---

# 3. Objectives

The main objectives of this project are:

1. Process all messages in chronological order.
2. Classify every message into one of the six mandatory categories.
3. Generate a confidence score for every classification.
4. Provide a short reason explaining every classification decision.
5. Detect sensitive information such as OTPs, passwords, payment details, phone numbers, and email addresses.
6. Mask sensitive values before storing processed message content.
7. Assign a risk level to detected sensitive information.
8. Generate a recommended security action.
9. Identify tasks and events from messages.
10. Extract task/event titles and descriptions.
11. Extract dates and deadlines when explicitly available.
12. Extract time information when explicitly available.
13. Extract people involved when identifiable.
14. Determine priority without guessing missing information.
15. Mark unclear or missing information as unresolved or null.
16. Generate structured JSON output.
17. Validate the generated results.
18. Provide explainable and reproducible processing.

---

# 4. Features
## 4.1 Message Classification

Every message is classified into exactly one of the six categories specified in the assignment:

1. `action_required`
2. `meeting_or_event`
3. `personal_information`
4. `general_information`
5. `promotional`
6. `sensitive_information`

The classifier uses predefined keywords, pattern matching, and rule-based scoring.

Each classification produces:

- Message ID
- Predicted category
- Confidence score
- Short explanation/reason

Example:

```json
{
  "message_id": "MSG_001",
  "category": "action_required",
  "confidence": 0.91,
  "reason": "The message asks the recipient to complete an action."
}
```
---

## 4.2 Sensitive Information Detection

The system detects different types of sensitive information using patterns and regular expressions.

Examples include:

- Passwords
- OTPs
- Card numbers
- Phone numbers
- Email addresses
- Login credentials

The purpose of sensitive-information detection is to prevent private information from being exposed in the final processed output.

### Example

Input:

```text
Your OTP is 482913.
```

The system detects the OTP as sensitive information.

---

## 4.3 Sensitive Information Masking

After sensitive information is detected, the system masks the sensitive values before writing the processed message to the output.

For example:

### Original Message

```text
Your OTP is 482913.
```

### Masked Message

```text
Your OTP is [MASKED].
```

Masking helps ensure that sensitive information is not unnecessarily exposed in the generated JSON output.

---

## 4.4 Risk Assessment

The system assigns a risk level to messages containing sensitive information.

The risk level is determined based on the type and presence of sensitive information.

Possible risk levels include:

- `low`
- `medium`
- `high`

The risk assessment helps identify messages that may require additional attention.

---

## 4.5 Recommended Action

For messages containing sensitive information, the system can generate a recommended action.

Examples of actions include:

- Review
- Secure
- Avoid sharing
- Verify
- Take appropriate security precautions

This provides an additional layer of interpretation beyond simply detecting sensitive information.

---

# 5. Task and Event Extraction

One of the main components of the project is extracting actionable information from messages.

The system identifies whether a message represents a:

- Task
- Event

The extracted information is stored in a structured format.

---

## 5.1 Task Extraction

A task represents an action that the recipient is expected to perform.

Examples:

```text
Please call Maya when you are free.
```

```text
Could you send the report soon?
```

```text
Please confirm the interview slot by 2026-09-05.
```

The system identifies these messages as tasks and attempts to extract relevant information.

---

## 5.2 Event Extraction

An event represents a scheduled activity such as:

- Meeting
- Workshop
- Interview
- Seminar
- Orientation
- Appointment
- Project review
- Product demo
- Team stand-up
- Family dinner

### Example

```text
Please join the AI workshop on 2026-09-08, 15:00 at Conference Room 2.
```

The system can identify:

```text
Type : event
Date : 2026-09-08
Time : 15:00
```

---

# 6. Date and Deadline Extraction

The system extracts explicit dates from messages using pattern-based rules.

### Example

Input:

```text
Please confirm the interview slot by 2026-09-05.
```

Extracted information:

```text
date_or_deadline: 2026-09-05
date_status: resolved
```

The system also handles messages where an exact date cannot be determined.

For example:

```text
Please call Maya when you are free.
```

There is no specific date in the message.

Therefore:

```text
date_or_deadline: null
date_status: unresolved
```

The system intentionally does not invent a date.

---

# 7. Time Extraction

The system extracts explicit time information when available.

### Example

Input:

```text
The client discussion is scheduled for 2026-09-07 at 14:00 in Zoom.
```

Extracted information:

```text
date_or_deadline: 2026-09-07
time: 14:00
```

If no time is provided, the time field remains unresolved or empty depending on the processing logic.

---

# 8. Person Extraction

The system attempts to identify people mentioned in task or event messages.

### Example

```text
Please call Maya when you are free.
```

Extracted information:

```text
person: Maya
```

This information can be useful for future task management or reminder functionality.

---

# 9. Priority Determination

The system determines task/event priority using explicit wording in the message.

Priority is not guessed when there is insufficient information.

The system supports:

- `high`
- `medium`
- `low`
- `unresolved`

---

## 9.1 High Priority

High priority is identified using explicit words such as:

```text
urgent
asap
immediately
critical
important
```

Example:

```text
Important: Please call Maya when you are free.
```

Result:

```text
priority: high
```

---

## 9.2 Low Priority

Low priority can be identified using wording such as:

```text
optional
whenever
when you are free
```

Example:

```text
Please call Maya when you are free.
```

Result:

```text
priority: low
```

---

## 9.3 Medium Priority

Medium priority can be identified from wording such as:

```text
soon
could you
please
```

Example:

```text
Could you send the report soon?
```

Result:

```text
priority: medium
```

---

## 9.4 Unresolved Priority

If the message does not contain sufficient explicit wording to determine priority, the system returns:

```text
priority: unresolved
```

For example:

```text
I will send the login details separately.
```

The system does not assume whether the task is high, medium, or low priority.

This approach helps avoid incorrect assumptions.

---

# 10. Structured Task/Event Output

Task and event information is stored using a structured object.

The output contains fields such as:

```text
item_id
type
title
description
date_or_deadline
time
person
priority
source_message_id
date_status
priority_status
```

### Example

```json
{
  "item_id": null,
  "type": "event",
  "title": "AI workshop",
  "description": "Please join the AI workshop on 2026-09-08, 15:00 at Conference Room 2.",
  "date_or_deadline": "2026-09-08",
  "time": "15:00",
  "person": null,
  "priority": "medium",
  "source_message_id": "MSG_0062",
  "date_status": "resolved",
  "priority_status": "resolved"
}
```

---

# 11. Resolved and Unresolved Information

The project explicitly tracks whether important extracted information was successfully resolved.

## Date Status

The `date_status` field can contain:

```text
resolved
unresolved
```

Example:

```json
"date_status": "resolved"
```

This means that a specific date was successfully extracted.

If no reliable date is available:

```json
"date_status": "unresolved"
```

---

## Priority Status

The `priority_status` field can contain:

```text
resolved
unresolved
```

Example:

```json
"priority_status": "resolved"
```

This means that a priority was successfully determined.

If the system cannot determine the priority:

```json
"priority_status": "unresolved"
```

This approach makes the output transparent and prevents the system from silently making assumptions.

---

# 12. Input Data

The system processes messages provided through a CSV file.

The input messages can contain different types of content, including:

```text
General information
Tasks
Events
Promotional messages
Personal information
Sensitive information
```

Each message is processed individually through the classification and extraction pipeline.

---

# 13. Processing Pipeline

The overall processing pipeline can be represented as follows:

```text
CSV Input
   │
   ▼
Read Messages
   │
   ▼
Message Classification
   │
   ├── action_required
   ├── general_information
   ├── meeting_or_event
   ├── personal_information
   ├── promotional
   └── sensitive_information
   │
   ▼
Sensitive Information Detection
   │
   ▼
Sensitive Information Masking
   │
   ▼
Risk Assessment
   │
   ▼
Recommended Action
   │
   ▼
Task/Event Detection
   │
   ├── Task
   └── Event
   │
   ▼
Information Extraction
   │
   ├── Date / Deadline
   ├── Time
   ├── Person
   └── Priority
   │
   ▼
Status Detection
   │
   ├── date_status
   └── priority_status
   │
   ▼
JSON Output
```

---

# 14. Project Structure

The project is organized into separate components for processing messages and storing generated output.

```text
AI_Message_Intelligence/
│
├── src/
│   ├── process_messages.py
│   └── ...
│
├── outputs/
│   └── message_classification.json
│
├── data/
│   └── ...
│
├── .gitignore
├── requirements.txt
└── README.md
```

> The exact files inside `src` and `data` depend on the final project implementation.

The Python virtual environment is created locally and should not be committed to the repository.

---

# 15. Technologies Used

The project is implemented using:

- **Python**
- **Regular Expressions**
- **JSON**
- **CSV**
- **Python Virtual Environment**
- **Rule-based text processing**
- **Structured data extraction**

---

# 16. Python Concepts Used

The project demonstrates several important Python concepts:

- Functions
- Lists
- Dictionaries
- Conditional statements
- Loops
- String processing
- File handling
- JSON handling
- CSV processing
- Regular expressions
- Exception handling
- Modular programming
- Data transformation

---

# 17. Installation

## Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
```

## Step 2: Navigate to the Project

```bash
cd AI_Message_Intelligence
```

## Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

## Step 4: Activate the Virtual Environment

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 18. Running the Project

After activating the virtual environment, run:

```bash
python -m src.process_messages
```

The system processes the input messages and generates the classification output.

A category summary is displayed in the terminal.

Example:

```text
# CATEGORY SUMMARY

action_required           186
general_information       271
meeting_or_event          200
personal_information       53
promotional               100
sensitive_information      90
```

The processed results are saved to:

```text
outputs/message_classification.json
```

---

# 19. Validating the Output

After running the project, the generated JSON file can be checked using Python commands.

## Check Total Task/Event Records

```bash
python -c "import json; d=json.load(open('outputs/message_classification.json')); items=[x for x in d if x.get('task_or_event')]; print('Task/Event records:',len(items))"
```

## Check Unresolved Dates

```bash
python -c "import json; d=json.load(open('outputs/message_classification.json')); items=[x for x in d if x.get('task_or_event') and x['task_or_event']['date_or_deadline'] is None]; print('Unresolved dates:',len(items))"
```

## Check Unresolved Priorities

```bash
python -c "import json; d=json.load(open('outputs/message_classification.json')); items=[x for x in d if x.get('task_or_event') and x['task_or_event']['priority']=='unresolved']; print('Unresolved priorities:',len(items))"
```

---

# 20. Current Processing Results

The current implementation processes the message dataset and generates structured results.

The final processing run successfully processed **900 messages**.

The category summary was:

```text
action_required           186
general_information       271
meeting_or_event          200
personal_information       53
promotional               100
sensitive_information      90
```

The category counts add up to 900 processed messages.

The validation results were:

```text
Task/Event records: 350
Unresolved dates: 11
Unresolved priorities: 0
```

The unresolved values do not necessarily indicate a failure.

They represent messages where the available text does not provide enough reliable information.

For example:

```text
Please call Maya when you are free.
```

does not provide an exact date.

Therefore, the system correctly leaves the date unresolved instead of inventing one.

Similarly:

```text
The review could be Friday afternoon.
```

contains an ambiguous relative date and may remain unresolved depending on the extraction rules.

---

# 21. Example Messages

## Example 1 — Task

### Input

```text
Please call Maya when you are free.
```

### Extracted Information

```text
Type     : task
Person   : Maya
Priority : low
Date     : unresolved
```

---

## Example 2 — Event

### Input

```text
Please join the AI workshop on 2026-09-08, 15:00 at Conference Room 2.
```

### Extracted Information

```text
Type : event
Date : 2026-09-08
Time : 15:00
```

---

## Example 3 — Deadline

### Input

```text
Please confirm the interview slot by 2026-09-05.
```

### Extracted Information

```text
Type        : task/event
Date        : 2026-09-05
Date Status : resolved
```

---

## Example 4 — Ambiguous Date

### Input

```text
The review could be Friday afternoon.
```

### Extracted Information

```text
Date: unresolved
```

The system does not convert "Friday afternoon" into an arbitrary calendar date.

---

## Example 5 — Sensitive Information

### Input

```text
Your OTP is 482913.
```

### Output

```text
Your OTP is [MASKED].
```

The sensitive value is masked before the processed message is stored.

---

# 22. Design Principles

The project follows several important design principles.

## 22.1 Do Not Guess

The system should not invent information that is not explicitly available.

For example, if a message says:

```text
Call me when you are free.
```

the system should not create a specific date.

---

## 22.2 Protect Sensitive Information

Sensitive information should be detected and masked before being written to output.

This reduces the risk of exposing private information.

---

## 22.3 Explainable Processing

The system uses keyword- and rule-based processing rather than an opaque prediction mechanism.

This makes the processing logic easier to understand, debug, and modify.

---

## 22.4 Structured Output

Unstructured messages are converted into structured JSON objects.

This makes the results easier to:

- Search
- Filter
- Store
- Analyze
- Display
- Use in other applications

---

# 23. Advantages

The project provides several advantages:

- Automates message organization.
- Reduces manual message processing.
- Extracts actionable tasks.
- Identifies scheduled events.
- Extracts dates and times.
- Detects sensitive information.
- Protects sensitive values through masking.
- Provides risk assessment.
- Generates recommended actions.
- Produces machine-readable JSON.
- Handles ambiguous information safely.
- Uses an explainable rule-based approach.

---

# 24. Limitations

The current system uses predefined rules, keywords, and regular expressions.

Therefore, some limitations exist:

- Complex natural-language expressions may not always be interpreted correctly.
- Relative dates such as "next Friday" may require additional date-resolution logic.
- Context-dependent priorities may remain unresolved.
- Different wording for the same intent may not always match existing rules.
- The system may require additional rules for new message patterns.
- The current implementation is not a fully trained machine-learning or deep-learning model.

These limitations can be addressed through future improvements.

---

# 25. Future Enhancements

The project can be extended with more advanced capabilities.

### Natural Language Processing

Use NLP models to understand messages beyond predefined keywords.

### Machine Learning Classification

Train a machine-learning model using labeled messages for automated classification.

### Advanced Date Understanding

Support expressions such as:

```text
tomorrow
next Monday
this Friday
next week
in two days
by the end of the week
```

### Entity Recognition

Improve extraction of:

- People
- Organizations
- Locations
- Dates
- Times

### Confidence Scores

Add confidence scores to classification and extraction results.

Example:

```json
{
  "category": "action_required",
  "confidence": 0.94
}
```

### Database Integration

Store processed messages and extracted tasks/events in a database.

### API Integration

Expose the message-processing pipeline through a REST API.

### Calendar Integration

Automatically create calendar events from extracted event information.

### Reminder System

Generate reminders for extracted tasks and deadlines.

### User Interface

Create a web or mobile interface for viewing:

- Messages
- Tasks
- Events
- Deadlines
- Priority
- Sensitive-information alerts

---

# 26. Use Cases

AI Message Intelligence can be used as a foundation for:

- Smart messaging applications
- Email classification systems
- Personal productivity assistants
- Task management systems
- Calendar assistants
- Notification management
- Enterprise communication tools
- Security-aware message processing
- Automated reminder systems
- AI-powered communication assistants

---

# 27. Project Status

**Status: Completed**

The current implementation successfully provides:

- Message classification
- Sensitive information detection
- Sensitive information masking
- Risk assessment
- Recommended action generation
- Task extraction
- Event extraction
- Date extraction
- Deadline extraction
- Time extraction
- Person extraction
- Priority determination
- Resolved/unresolved status tracking
- JSON output generation
- Category summary generation
- Output validation

---

# 28. Conclusion

AI Message Intelligence provides an automated and structured approach to processing unstructured messages.

The system combines classification, sensitive-information detection, masking, risk assessment, action recommendation, and task/event extraction into a single processing pipeline.

A key feature of the system is its ability to distinguish between information that can be reliably extracted and information that remains ambiguous. Instead of guessing missing dates or priorities, the system marks them as unresolved.

This makes the generated output more reliable and provides a strong foundation for future extensions such as NLP, machine learning, calendar integration, reminders, databases, APIs, and user-facing applications.

---

# 29. Author

**Srivani Garrepalli**

B.Tech — Computer Science and Engineering (AI & ML)

# AI-Tool Usage Declaration

AI-assisted development tools were used during the development of this project for guidance, debugging assistance, documentation improvement, and code-review support.

The core message-processing logic, rule definitions, classification approach, sensitive-information handling, task/event extraction, and final project behavior were reviewed and understood by the author.

No raw dataset messages were sent to external AI services for processing. The submitted system processes the supplied messages locally.

The author understands the submitted source code and can explain the design decisions and implementation during the technical discussion.