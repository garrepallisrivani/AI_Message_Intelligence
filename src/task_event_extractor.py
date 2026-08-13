import re

from datetime import datetime, timedelta
def extract_date(text):
    """Extract explicit and relative dates from message text."""

    text_lower = text.lower()

    # 1. Explicit YYYY-MM-DD date
    match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", text)

    if match:
        return match.group(0)

    # Today's date
    today = datetime.today().date()

    # 2. Relative dates
    if re.search(r"\btoday\b", text_lower):
        return today.isoformat()

    if re.search(r"\btomorrow\b", text_lower):
        return (today + timedelta(days=1)).isoformat()

    # 3. Weekdays
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    # Explicit "next Monday", "next Tuesday", etc.
    for day_name, day_number in weekdays.items():

        if re.search(
            rf"\bnext\s+{day_name}\b",
            text_lower
        ):
            days_ahead = (
                day_number - today.weekday()
            ) % 7

            if days_ahead == 0:
                days_ahead = 7
            else:
                days_ahead += 7

            return (
                today + timedelta(days=days_ahead)
            ).isoformat()

    # Plain weekday
    for day_name, day_number in weekdays.items():

        if re.search(
            rf"\b{day_name}\b",
            text_lower
        ):
            days_ahead = (
                day_number - today.weekday()
            ) % 7

            # If weekday is today, use next week's occurrence
            if days_ahead == 0:
                days_ahead = 7

            return (
                today + timedelta(days=days_ahead)
            ).isoformat()

    return None
def has_date_expression(text):
    """Check whether the message contains a recognizable date expression."""

    text_lower = text.lower()

    patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\btoday\b",
        r"\btomorrow\b",
        r"\bmonday\b",
        r"\btuesday\b",
        r"\bwednesday\b",
        r"\bthursday\b",
        r"\bfriday\b",
        r"\bsaturday\b",
        r"\bsunday\b",
        r"\bnext\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    ]

    return any(
        re.search(pattern, text_lower)
        for pattern in patterns
    )

def extract_time(text):
    """Extract a time such as 10:00 or 15:30 if present."""

    match = re.search(r"\b\d{1,2}:\d{2}\b", text)

    if match:
        return match.group(0)

    return None


def extract_person(text):
    """
    Extract a person's name when the message explicitly mentions
    someone.

    Do not guess a person when no name is present.
    """

    # Patterns such as:
    # "Maya asked..."
    # "Please call Maya..."
    # "Ananya will..."
    pattern = re.search(
        r"\b(?:call|contact|email|message|ask|asked|told|with)\s+"
        r"([A-Z][a-z]+)\b",
        text,
    )

    if pattern:
        return pattern.group(1)

    # Pattern: "Maya asked whether..."
    pattern = re.search(
        r"\b([A-Z][a-z]+)\s+(?:asked|said|mentioned|requested)\b",
        text,
    )

    if pattern:
        return pattern.group(1)

    return None
def determine_priority(text, item_type):
    """
    Determine priority from explicit wording.

    Priority is based only on explicit wording.
    """

    text_lower = text.lower()

    high_words = [
        "urgent",
        "asap",
        "immediately",
        "critical",
        "important",
    ]

    low_words = [
        "optional",
        "whenever",
        "when you are free",
    ]

    medium_words = [
        "soon",
        "shortly",
    ]

    # High priority
    if any(word in text_lower for word in high_words):
        return "high"

    # Low priority
    if any(word in text_lower for word in low_words):
        return "low"

    # Medium priority
    if any(word in text_lower for word in medium_words):
        return "medium"

    # Tasks with explicit deadlines are medium
    if item_type == "task":
        if extract_date(text):
            return "medium"

    # Events with a date/time but no explicit priority
    # are treated as medium
    if item_type == "event":
        if extract_date(text) or extract_time(text):
            return "medium"

    return "unresolved"
def extract_title(text, item_type):
    """
    Extract a clean and meaningful title for a task or event.
    """

    # Remove common message prefixes
    cleaned = re.sub(
        r"^(?:hi|hello|fyi|important|quick update|please note|"
        r"just checking|one more thing|for today)\s*[:,—-]?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    # Remove "Can you help?" from the beginning
    cleaned = re.sub(
        r"^can you help\?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    ).strip()

    # =========================================================
    # TASK TITLES
    # =========================================================

    if item_type == "task":

        task_patterns = [

            # Can you review X before DATE?
            r"(?:can you|please)\s+(.+?)"
            r"(?:\s+(?:before|by)\s+\d{4}-\d{2}-\d{2})[?.]?$",

            # I need you to renew X by DATE
            r"i need you to\s+(.+?)"
            r"(?:\s+(?:before|by)\s+\d{4}-\d{2}-\d{2})[?.]?$",

            # Don't forget to pay X; deadline is DATE
            r"(?:don't forget to|do not forget to)\s+(.+?)"
            r"(?:\s*;\s*deadline\s+is\s+\d{4}-\d{2}-\d{2})[?.]?$",

            # Action; deadline is DATE
            r"(.+?)\s*;\s*deadline\s+is\s+\d{4}-\d{2}-\d{2}[?.]?$",

            # Action is due on DATE
            r"(.+?)\s+is due on\s+\d{4}-\d{2}-\d{2}[?.]?$",

            # General action request
            r"(?:can you|please)\s+(.+?)[?.]?$",

            # I need you to do something
            r"i need you to\s+(.+?)[?.]?$",

            # Don't forget to do something
            r"(?:don't forget to|do not forget to)\s+(.+?)[?.]?$",
        ]

        for pattern in task_patterns:

            match = re.search(
                pattern,
                cleaned,
                flags=re.IGNORECASE,
            )

            if match:
                title = match.group(1).strip()

                # Remove deadline information if still present
                title = re.sub(
                    r"\s*;\s*deadline\s+is\s+\d{4}-\d{2}-\d{2}",
                    "",
                    title,
                    flags=re.IGNORECASE,
                )

                title = re.sub(
                    r"\s+(?:before|by)\s+\d{4}-\d{2}-\d{2}",
                    "",
                    title,
                    flags=re.IGNORECASE,
                )

                title = title.strip(" .,!?")

                if title:
                    return title.capitalize()

        # If no pattern matched, use the message itself
        # but remove unnecessary prefixes.
        fallback = cleaned.strip(" .,!?")

        if fallback:
            return fallback.capitalize()

    # =========================================================
    # EVENT TITLES
    # =========================================================

    if item_type == "event":

        event_patterns = [
            # Please confirm the interview slot by DATE
            r"please\s+confirm\s+(?:the\s+)?(.+?)\s+by\s+\d{4}-\d{2}-\d{2}",
            # Technical interview at TIME on DATE
            r"(?:are you available for\s+)?(?:the\s+)?(.+?)\s+at\s+\d{1,2}:\d{2}\s+on\s+\d{4}-\d{2}-\d{2}",

            # Calendar update: team stand-up, DATE at TIME
            r"calendar update:\s*([^,]+)",

            # Reminder: mentor catch-up happens...
            r"reminder:\s*([^,]+?)\s+happens\s+on",

            # Join the internship orientation on DATE
            r"join\s+(?:the\s+)?(.+?)\s+on\s+\d{4}-\d{2}-\d{2}",

            # Product demo is scheduled for DATE
            r"(?:the\s+)?(.+?)\s+is scheduled for\s+\d{4}-\d{2}-\d{2}",

            # Client discussion is scheduled on DATE
            r"(?:the\s+)?(.+?)\s+is scheduled on\s+\d{4}-\d{2}-\d{2}",

            # Something happens on DATE
            r"(?:the\s+)?(.+?)\s+happens\s+on\s+\d{4}-\d{2}-\d{2}",
        ]

        for pattern in event_patterns:

            match = re.search(
                pattern,
                cleaned,
                flags=re.IGNORECASE,
            )

            if match:

                title = match.group(1).strip()

                title = title.rstrip(".,!? ")

                # Remove unnecessary "the"
                title = re.sub(
                    r"^the\s+",
                    "",
                    title,
                    flags=re.IGNORECASE,
                )

                if title:
                    return title.capitalize()

        # Fallback for events that have a recognizable event
        # but don't match the patterns above.
        event_keywords = [
            "webinar",
            "meeting",
            "seminar",
            "appointment",
            "orientation",
            "dinner",
            "stand-up",
            "catch-up",
            "product demo",
            "client discussion",
            "project review",
            "sprint planning",
        ]

        for keyword in event_keywords:
            match = re.search(
                rf"\b(.{{0,60}}{re.escape(keyword)}.{{0,60}})\b",
                cleaned,
                flags=re.IGNORECASE,
            )

            if match:
                title = match.group(1).strip()
                title = title.rstrip(".,!?")
                return title.capitalize()

    return "Unresolved"

def determine_item_type(category, text):
    """
    Decide whether the message represents a clear task or event.
    Do not create task/event records for preferences, information,
    promotions, or actions that the sender says they will perform.
    """

    text_lower = text.lower()

    # ---------------------------------
    # Clear EVENT indicators
    # ---------------------------------

    event_patterns = [
        r"\bmeeting\b",
        r"\bmeet-up\b",
        r"\bmeetup\b",
        r"\bcatch[- ]up\b",
        r"\borientation\b",
        r"\bappointment\b",
        r"\bwebinar\b",
        r"\bconference\b",
        r"\binterview\b",
        r"\bdinner\b",
        r"\bstand[- ]up\b",
        r"\bcalendar update\b",
        r"\bseminar\b",
        r"\bproduct demo\b",
        r"\bclient discussion\b",
        r"\bproject review\b",
        r"\bsprint planning\b",
    ]

    has_date = extract_date(text) is not None
    has_time = extract_time(text) is not None

    if any(
        re.search(pattern, text_lower)
        for pattern in event_patterns
    ):
        if has_date or has_time:
            return "event"

    # Explicit scheduled/happening event
    if (
        has_date
        and has_time
        and any(
            word in text_lower
            for word in [
                "scheduled",
                "happens",
                "join",
                "calendar",
            ]
        )
    ):
        return "event"

    # ---------------------------------
    # Do not create a task when the
    # sender is describing their own action
    # ---------------------------------

    passive_sender_action = re.search(
        r"\b(?:i|we|i'll|i will|we'll|we will)\s+"
        r"(?:send|reply|review|confirm|update|prepare|complete|"
        r"submit|pay|register|renew|respond|call|contact)\b",
        text_lower,
    )

    if passive_sender_action:
        return None

    # ---------------------------------
    # Clear TASK indicators
    # ---------------------------------

    task_patterns = [
        r"\bplease\s+(?:review|send|submit|complete|pay|reply|renew|confirm|upload|prepare|update|call|contact)",
        r"\bcan you\s+(?:review|send|submit|complete|pay|reply|renew|confirm|upload|prepare|update|call|contact)",
        r"\bi need you to\b",
        r"\bdon't forget to\b",
        r"\bdo not forget to\b",
        r"\bremember to\b",
        r"\bis due on\b",
        r"\bdeadline\b",
        r"\bplease call\b",
        r"\bplease contact\b",
        r"\bplease email\b",
    ]

    if any(
        re.search(pattern, text_lower)
        for pattern in task_patterns
    ):
        return "task"

    # ---------------------------------
    # Specific action verbs
    # ---------------------------------

    task_words = [
        "review",
        "submit",
        "renew",
        "send",
        "complete",
        "pay",
        "reply",
        "confirm",
        "upload",
        "prepare",
        "update",
    ]

    # Only classify as task when the category
    # indicates that an action is required.
    if category == "action_required":

        for word in task_words:

            if re.search(
                rf"\b{word}\b",
                text_lower,
            ):
                return "task"

    # ---------------------------------
    # Everything else = no task/event
    # ---------------------------------

    return None
def extract_task_or_event(
    message_id,
    message,
    category,
):
    """
    Extract a task or event from one message.

    Returns None when the message does not represent
    a task or event.
    """

    item_type = determine_item_type(
        category,
        message,
    )

    if item_type is None:
        return None

    date = extract_date(message)
    time = extract_time(message)
    person = extract_person(message)
    priority = determine_priority(
        message,
        item_type,
    )

    title = extract_title(
        message,
        item_type,
    )

    item_id = f"{item_type.upper()}_{message_id.split('_')[1]}"
    return {
        "item_id": item_id,
        "type": item_type,
        "title": title,
        "description": message,
        "date_or_deadline": date,
        "time": time,
        "person": person,
        "priority": priority,
        "source_message_id": message_id,
        "date_status": "resolved" if date else "not_mentioned",
        "priority_status": "resolved" if priority != "unresolved" else "unresolved"
    }