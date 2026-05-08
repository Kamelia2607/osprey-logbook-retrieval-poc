import os
from semantic_search import *
from summarize import *
from search import *
import json
import pickle

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def load_logs(path):
    cache_path = "embeddings_cache.pkl"

    if os.path.exists(cache_path):
        print("Loading cached embeddings...")
        with open(cache_path, "rb") as f:
            logs = pickle.load(f)
        return logs

    logs = []

    with open(path) as f:
        for line in f:
            raw_log = json.loads(line)
            normalized_log = normalize_log(raw_log)
            logs.append(normalized_log)

    texts = [log["subject"] + " " + log["notes"] for log in logs]

    print("Computing embeddings (one-time cost)...")
    embeddings = model.encode(texts)

    for i in range(len(logs)):
        logs[i]["embedding"] = embeddings[i]

    with open(cache_path, "wb") as f:
        pickle.dump(logs, f)

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

    print("Initializing logbook retrieval system...")
    logs = load_logs(path)
    print(f"Loaded {len(logs)} logs.\n")

    while True:
        user_query = input("Enter operator query (or 'quit'): ")

        if user_query.lower() in ["quit", "exit"]:
            print("Exiting system.")
            break

        if not user_query.strip():
            print("Please enter a valid query.\n")
            continue

        retrieved_logs = semantic_search(
            user_query=user_query,
            logs=logs,
            k=3
        )

        print(f"\nQuery: {user_query}")
        print(f"Retrieved {len(retrieved_logs)} relevant logs.\n")

        if not retrieved_logs:
            print("No relevant logs found.\n")
            continue

        print("--- Retrieved Logs ---\n")

        for log in retrieved_logs:
            print(f"Score: {log['score']:.3f}")
            print(f"Log ID: {log['log_id']}")
            print(f"Timestamp: {log['timestamp']}")
            print(f"Category: {log['category']}")
            print(f"Level: {log['level']}")
            print(f"Subject: {log['subject']}")
            print(f"Notes: {log['note_excerpt']}")
            print("-" * 50)

        try:
            summary = summarize_logs(user_query, retrieved_logs)

         
            print("\n LLM Summary\n")
            print(summary)

        except Exception as e:
            print("\nLLM summary failed.")
            print(f"Error: {e}")

        print("\n" + "_" * 60 + "\n")