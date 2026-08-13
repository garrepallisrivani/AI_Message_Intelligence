from src.task_event_extractor import extract_task_or_event


def test_task_extraction():

    result = extract_task_or_event(
        "MSG_0002",
        "Can you review the privacy checklist before 2026-09-09?",
        "action_required",
    )

    assert result is not None
    assert result["type"] == "task"
    assert result["title"] == "Review the privacy checklist"
    assert result["date_or_deadline"] == "2026-09-09"
    assert result["source_message_id"] == "MSG_0002"


def test_task_priority():

    result = extract_task_or_event(
        "MSG_0007",
        "For today: Please reply to the client email by 2026-09-04.",
        "action_required",
    )

    assert result is not None
    assert result["type"] == "task"
    assert result["priority"] != "unresolved"


def test_event_extraction():

    result = extract_task_or_event(
        "MSG_0011",
        "Just checking—Please join the internship orientation "
        "on 2026-09-18, 13:00 at Conference Room 2.",
        "meeting_or_event",
    )

    assert result is not None
    assert result["type"] == "event"
    assert result["date_or_deadline"] == "2026-09-18"


def test_calendar_event():

    result = extract_task_or_event(
        "MSG_0023",
        "Hi, Calendar update: team stand-up, "
        "2026-09-04 at 15:00, the college auditorium.",
        "meeting_or_event",
    )

    assert result is not None
    assert result["type"] == "event"
    assert result["date_or_deadline"] == "2026-09-04"
    assert result["time"] == "15:00"


def test_vague_date_is_not_invented():

    result = extract_task_or_event(
        "MSG_0133",
        "Important: Let us meet sometime next week.",
        "general_information",
    )

    # The system should not invent a specific date.
    if result:
        assert result["date_or_deadline"] is None