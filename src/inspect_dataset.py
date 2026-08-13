import pandas as pd

from preprocessing import load_messages
from sensitive_detector import mask_sensitive_information


DATA_PATH = "../data/messages.csv"


def main():

    df = load_messages(DATA_PATH)

    print("=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)

    print("Total messages:", len(df))

    print("\nColumns:")
    print(list(df.columns))

    print("\nUnique senders:", df["sender"].nunique())

    print("\nSender counts:")
    print(df["sender"].value_counts())

    print("\nDate range:")
    print("Start:", df["timestamp"].min())
    print("End:", df["timestamp"].max())

    print("\nFirst 30 messages:")
    print("-" * 60)

    for _, row in df.head(30).iterrows():

        safe_message = mask_sensitive_information(
            row["message"]
        )

        print(
            f"{row['message_id']} | "
            f"{row['timestamp']} | "
            f"{row['sender']} | "
            f"{safe_message}"
        )


if __name__ == "__main__":
    main()