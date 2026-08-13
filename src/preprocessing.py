import pandas as pd


REQUIRED_COLUMNS = [
    "message_id",
    "timestamp",
    "sender",
    "message"
]


def load_messages(file_path):
    """
    Load and validate the message dataset.
    """

    # Load CSV
    df = pd.read_csv(file_path)

    # Check required columns
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # Clean text fields
    df["message"] = (
        df["message"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["sender"] = (
        df["sender"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Process messages chronologically
    df = (
        df.sort_values(
            by="timestamp",
            kind="stable"
        )
        .reset_index(drop=True)
    )

    return df