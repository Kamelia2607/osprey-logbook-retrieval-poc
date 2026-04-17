from semantic_search import *
from summarize import *
from search import *
import json

def load_logs(path):
    logs = []

    with open(path) as f:
        for line in f:
            raw_log = json.loads(line)
            normalized_log = normalize_log(raw_log)
            logs.append(normalized_log)

    texts = []
    for log in logs:
        text = log["subject"] + " " + log["notes"]
        texts.append(text)

    embeddings = model.encode(texts)

    for i in range(len(logs)):
        logs[i]["embedding"] = embeddings[i]

    return logs


def write_report(user_query, retrieved_logs, summary, output_path="report.txt"):
    with open(output_path, "w") as f:
        f.write(f"Operator Query: {user_query}\n\n")
        f.write("Retrieved Logs:\n\n")

        for log in retrieved_logs:
            f.write(f"Score: {log['score']}\n")
            f.write(f"Log ID: {log['log_id']}\n")
            f.write(f"Timestamp: {log['timestamp']}\n")
            f.write(f"Category: {log['category']}\n")
            f.write(f"Level: {log['level']}\n")
            f.write(f"Subject: {log['subject']}\n")
            f.write(f"Notes: {log['note_excerpt']}\n")
            f.write("\n")

        f.write("Summary:\n\n")
        f.write(summary)
        f.write("\n")


if __name__ == "__main__":
    path = "../logbook_250226_anonymized_2024plus (1).jsonl"
    logs = load_logs(path)

    user_query = input("Enter operator query: ")

    retrieved_logs = semantic_search(
        user_query=user_query,
        logs=logs,
        k=3
    )

    summary = summarize_logs(user_query, retrieved_logs)

    print("\n--- Retrieved Logs ---\n")
    for log in retrieved_logs:
        print(log["score"])
        print(log["subject"])
        print(log["category"])
        print()

    print("\n--- Summary ---\n")
    print(summary)

    write_report(user_query, retrieved_logs, summary)
    print("\nReport saved to report.txt")