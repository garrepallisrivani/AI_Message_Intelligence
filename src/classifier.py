import re

from src.sensitive_detector import detect_sensitive_information


# Strong indicators for each category.
CATEGORY_KEYWORDS = {

    "promotional": [
        "discount",
        "sale",
        "offer",
        "deal",
        "coupon",
        "promo",
        "promotion",
        "special price",
        "cashback",
        "premium plan",
        "exclusive benefits",
        "use code",
    ],

    "meeting_or_event": [
        "meeting",
        "meet-up",
        "meetup",
        "catch-up",
        "catch up",
        "orientation",
        "appointment",
        "webinar",
        "conference",
        "interview",
        "dinner",
        "event",
        "stand-up",
        "stand up",
        "calendar update",
        "please join",
        "join the",
        "session",
        "scheduled",
    ],

    "action_required": [
        "please reply",
        "please review",
        "please confirm",
        "please submit",
        "please send",
        "please complete",
        "please update",
        "please prepare",

        "can you review",
        "can you send",
        "can you confirm",
        "can you update",
        "can you complete",
        "can you prepare",
        "can you help",

        "need you to",
        "don't forget",
        "do not forget",
        "remember to",

        "submit",
        "reply",
        "review",
        "confirm",
        "renew",
        "complete",
        "pay",
        "register",
        "respond",
        "update",
        "prepare",
    ],

    "personal_information": [
        "my favourite",
        "my favorite",
        "i prefer",
        "i drink",
        "my emergency contact",
        "my brother",
        "my sister",
        "personal note",
        "for my profile",
    ],

    "general_information": [
        "fyi",
        "for your information",
        "please note",
        "quick update",
        "just so you know",
        "one more thing",
    ],
}


def normalize_text(text):
    """Normalize message text."""
    return re.sub(r"\s+", " ", text.lower().strip())


def find_matches(text, keywords):
    """Return keywords that appear in the message."""
    return [
        keyword
        for keyword in keywords
        if keyword in text
    ]


def classify_message(message):
    """
    Classify a message into one of the six required categories.

    Sensitive information is checked first so that sensitive
    messages are not incorrectly classified as another category.
    """

    text = normalize_text(message)

    # ---------------------------------------------------------
    # 1. Sensitive Information
    # ---------------------------------------------------------

    sensitive_types = detect_sensitive_information(message)

    if sensitive_types:

        return {
            "category": "sensitive_information",
            "confidence": 0.95,
            "reason": (
                "Sensitive information detected: "
                + ", ".join(sensitive_types)
                + "."
            )
        }

    # ---------------------------------------------------------
    # 2. Promotional
    # ---------------------------------------------------------

    promotional_matches = find_matches(
        text,
        CATEGORY_KEYWORDS["promotional"]
    )

    if promotional_matches:

        confidence = min(
            0.80 + 0.05 * (len(promotional_matches) - 1),
            0.95
        )

        return {
            "category": "promotional",
            "confidence": round(confidence, 2),
            "reason": (
                "Promotional language detected: "
                + ", ".join(promotional_matches[:4])
                + "."
            )
        }

    # ---------------------------------------------------------
    # 3. Meeting or Event
    # ---------------------------------------------------------

    event_matches = find_matches(
        text,
        CATEGORY_KEYWORDS["meeting_or_event"]
    )

    has_date = bool(
        re.search(
            r"\b\d{4}-\d{2}-\d{2}\b",
            text
        )
    )

    has_time = bool(
        re.search(
            r"\b\d{1,2}:\d{2}\b",
            text
        )
    )

    # "Please join..." with date/time is an event.
    if event_matches and (has_date or has_time):

        return {
            "category": "meeting_or_event",
            "confidence": 0.90,
            "reason": (
                "Meeting or event language detected: "
                + ", ".join(event_matches[:4])
                + ", with date/time information."
            )
        }

    # Strong event words even without date/time.
    strong_event_words = [
        "meeting",
        "meet-up",
        "meetup",
        "catch-up",
        "catch up",
        "orientation",
        "appointment",
        "webinar",
        "conference",
        "interview",
        "dinner",
        "event",
        "stand-up",
        "stand up",
        "calendar update",
    ]

    strong_event_matches = find_matches(
        text,
        strong_event_words
    )

    if strong_event_matches:

        return {
            "category": "meeting_or_event",
            "confidence": 0.80,
            "reason": (
                "Meeting or event language detected: "
                + ", ".join(strong_event_matches[:4])
                + "."
            )
        }

    # ---------------------------------------------------------
    # 4. Action Required
    # ---------------------------------------------------------

    action_matches = find_matches(
        text,
        CATEGORY_KEYWORDS["action_required"]
    )

    # Avoid false positives such as:
    # "I will send the login details separately."
    #
    # This contains "send", but the recipient is not being
    # asked to perform the action.

    passive_action_only = [
        "send",
        "reply",
        "review",
        "confirm",
        "update",
        "prepare",
        "complete",
        "respond",
        "register",
        "renew",
        "pay",
    ]

    strong_action_matches = [
        match
        for match in action_matches
        if match not in passive_action_only
    ]

    # Explicit request patterns are strong action indicators.
    explicit_action = bool(
        re.search(
            r"\b(?:can you|could you|please|need you to|"
            r"don't forget to|do not forget to|remember to)\b",
            text
        )
    )

    # Also detect direct action + deadline.
    has_deadline = bool(
        re.search(
            r"\b(?:before|by|deadline)\b.*\b\d{4}-\d{2}-\d{2}\b",
            text
        )
    )

    if action_matches and (
        explicit_action
        or strong_action_matches
        or has_deadline
    ):

        confidence = min(
            0.80 + 0.05 * (len(action_matches) - 1),
            0.95
        )

        return {
            "category": "action_required",
            "confidence": round(confidence, 2),
            "reason": (
                "The message asks the recipient to take an action: "
                + ", ".join(action_matches[:4])
                + "."
            )
        }

    # ---------------------------------------------------------
    # 5. Personal Information
    # ---------------------------------------------------------

    personal_matches = find_matches(
        text,
        CATEGORY_KEYWORDS["personal_information"]
    )

    if personal_matches:

        return {
            "category": "personal_information",
            "confidence": 0.80,
            "reason": (
                "The message contains personal information or "
                "a personal preference: "
                + ", ".join(personal_matches[:4])
                + "."
            )
        }

    # ---------------------------------------------------------
    # 6. General Information
    # ---------------------------------------------------------

    general_matches = find_matches(
        text,
        CATEGORY_KEYWORDS["general_information"]
    )

    if general_matches:

        return {
            "category": "general_information",
            "confidence": 0.70,
            "reason": (
                "The message provides information without a "
                "clear required action or event."
            )
        }

    # ---------------------------------------------------------
    # Fallback
    # ---------------------------------------------------------

    return {
        "category": "general_information",
        "confidence": 0.45,
        "reason": (
            "No strong category-specific indicators were detected; "
            "classified as general information with low confidence."
        )
    }