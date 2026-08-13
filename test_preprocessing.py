from src.preprocessing import load_messages


def test_load_messages():

    df = load_messages("data/messages.csv")

    assert len(df) == 900

    required_columns = {
        "message_id",
        "timestamp",
        "sender",
        "message",
    }

    assert required_columns.issubset(df.columns)


def test_message_ids_are_present():

    df = load_messages("data/messages.csv")

    assert df["message_id"].notna().all()


def test_messages_are_not_empty():

    df = load_messages("data/messages.csv")

    assert df["message"].notna().all()
    assert (df["message"].str.strip() != "").all()