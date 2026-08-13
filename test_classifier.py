from src.classifier import classify_message


def test_action_required():
    message = "Can you review the privacy checklist before 2026-09-09?"

    result = classify_message(message)

    assert result["category"] == "action_required"
    assert 0 <= result["confidence"] <= 1
    assert result["reason"]


def test_meeting_or_event():
    message = (
        "FYI: Reminder: mentor catch-up happens "
        "on 2026-09-16 at 11:00 in the city clinic."
    )

    result = classify_message(message)

    assert result["category"] == "meeting_or_event"


def test_promotional():
    message = "Special festival discount on clothing. Use code SAVE17."

    result = classify_message(message)

    assert result["category"] == "promotional"


def test_personal_information():
    message = "Remember that I drink coffee without sugar."

    result = classify_message(message)

    assert result["category"] == "personal_information"


def test_sensitive_information():
    message = "My recent test result says vitamin D deficiency."

    result = classify_message(message)

    assert result["category"] == "sensitive_information"