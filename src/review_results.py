import json
from collections import Counter


RESULT_PATH = "outputs/message_classification.json"


def load_results():

    with open(
        RESULT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def main():

    results = load_results()

    print("=" * 70)
    print("CLASSIFICATION QUALITY REVIEW")
    print("=" * 70)

    # ---------------------------------------------------------
    # Category counts
    # ---------------------------------------------------------

    counts = Counter(
        result["category"]
        for result in results
    )

    print("\nCATEGORY COUNTS")
    print("-" * 70)

    for category, count in sorted(counts.items()):

        print(
            f"{category:25} {count}"
        )

    # ---------------------------------------------------------
    # Examples from every category
    # ---------------------------------------------------------

    print("\n\nEXAMPLES FROM EACH CATEGORY")
    print("-" * 70)

    categories = sorted(counts.keys())

    for category in categories:

        print(f"\n[{category.upper()}]")

        category_results = [
            result
            for result in results
            if result["category"] == category
        ]

        for result in category_results[:5]:

            print(
                f"{result['message_id']} | "
                f"confidence={result['confidence']} | "
                f"{result['masked_message']}"
            )

    # ---------------------------------------------------------
    # Lowest confidence
    # ---------------------------------------------------------

    print("\n\nLOWEST CONFIDENCE RESULTS")
    print("-" * 70)

    low_confidence = sorted(
        results,
        key=lambda result: result["confidence"]
    )

    for result in low_confidence[:20]:

        print(
            f"{result['message_id']} | "
            f"{result['category']} | "
            f"{result['confidence']} | "
            f"{result['masked_message']}"
        )

    # ---------------------------------------------------------
    # Sensitive information
    # ---------------------------------------------------------

    print("\n\nSENSITIVE INFORMATION")
    print("-" * 70)

    sensitive_results = [
        result
        for result in results
        if result["sensitive"]
    ]

    print(
        "Total sensitive messages:",
        len(sensitive_results)
    )

    for result in sensitive_results[:20]:

        print(
            f"{result['message_id']} | "
            f"{result['sensitivity_types']} | "
            f"{result['masked_message']}"
        )


if __name__ == "__main__":
    main()