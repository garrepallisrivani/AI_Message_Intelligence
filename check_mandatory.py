import csv
import json

with open("data/mandatory_demo_ids.csv", encoding="utf-8-sig") as f:
    ids = [row["message_id"] for row in csv.DictReader(f)]

with open("outputs/message_classification.json", encoding="utf-8") as f:
    results = json.load(f)

results_by_id = {
    item["message_id"]: item
    for item in results
}

print("=" * 90)
print("15 MANDATORY DEMO MESSAGES")
print("=" * 90)

for number, message_id in enumerate(ids, 1):

    item = results_by_id[message_id]

    print()
    print("-" * 90)
    print(f"{number}. MESSAGE ID: {message_id}")
    print("-" * 90)

    print(f"Category       : {item['category']}")
    print(f"Confidence     : {item['confidence']}")
    print(f"Reason         : {item['reason']}")

    print()
    print("SENSITIVE INFORMATION")
    print(f"Sensitive      : {item['sensitive']}")
    print(f"Types          : {item['sensitivity_types']}")
    print(f"Risk           : {item['sensitivity_risk']}")
    print(f"Recommended    : {item['recommended_action']}")
    print(f"Masked message : {item['masked_message']}")

    print()
    print("TASK / EVENT")

    task = item.get("task_or_event")

    if task:
        print(f"Type           : {task['type']}")
        print(f"Title          : {task['title']}")
        print(f"Description    : {task['description']}")
        print(f"Date/Deadline  : {task['date_or_deadline']}")
        print(f"Time           : {task['time']}")
        print(f"Person         : {task['person']}")
        print(f"Priority       : {task['priority']}")
        print(f"Date status    : {task['date_status']}")
        print(f"Priority status: {task['priority_status']}")
    else:
        print("None")

print()
print("=" * 90)
print("END OF MANDATORY MESSAGE CHECK")
print("=" * 90)
