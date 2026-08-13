import json
import os

from src.preprocessing import load_messages
from src.classifier import classify_message
from src.sensitive_detector import (
    detect_sensitive_information,
    mask_sensitive_information,
    get_sensitivity_metadata
)
from src.task_event_extractor import extract_task_or_event

DATA_PATH = "data/messages.csv"
OUTPUT_DIR = "outputs"


def process_messages():

    # Load messages
    df = load_messages(DATA_PATH)

    # Make sure messages are chronological
    df = df.sort_values("timestamp").reset_index(drop=True)

    results = []

    for _, row in df.iterrows():

        message_id = row["message_id"]
        timestamp = row["timestamp"]
        sender = row["sender"]
        message = row["message"]

        # Detect sensitive information
        sensitive_types = detect_sensitive_information(message)

        # Get risk and recommended action
        sensitivity_metadata = get_sensitivity_metadata(
        sensitive_types
        )
        # Mask message before storing/processing output
        masked_message = mask_sensitive_information(message)

        # Classification
        classification = classify_message(message)
        task_or_event = extract_task_or_event(
            message_id,
            message,
            classification["category"]
        )

        result = {
            "message_id": message_id,
            "timestamp": str(timestamp),
            "sender": sender,
            "category": classification["category"],
            "confidence": classification["confidence"],
            "reason": classification["reason"],
            "sensitive": bool(sensitive_types),
            "sensitivity_types": sensitive_types,
            "sensitivity_risk": sensitivity_metadata["risk"],
            "recommended_action": sensitivity_metadata["recommended_action"],
            "masked_message": masked_message,
            "task_or_event": task_or_event
        }

        results.append(result)

    return results


def save_results(results):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(
        OUTPUT_DIR,
        "message_classification.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)

    print("Messages processed:", len(results))
    print("Output:", output_path)

def print_summary(results):

    print()
    print("=" * 60)
    print("CATEGORY SUMMARY")
    print("=" * 60)

    counts = {}

    for result in results:
        category = result["category"]
        counts[category] = counts.get(category, 0) + 1

    required_categories = [
        "action_required",
        "meeting_or_event",
        "personal_information",
        "general_information",
        "promotional",
        "sensitive_information"
    ]

    for category in required_categories:
        print(
            f"{category:25} {counts.get(category, 0)}"
        )

    print("-" * 60)
    print(f"{'Total messages':25} {len(results)}")

def main():

    results = process_messages()

    save_results(results)

    print_summary(results)


if __name__ == "__main__":
    main()