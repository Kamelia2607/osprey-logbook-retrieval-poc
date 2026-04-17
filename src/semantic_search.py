from __future__ import annotations
import json
from typing import List
from sentence_transformers import SentenceTransformer
from search import *
import math



model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    try:
        return model.encode(text)
    except Exception as e:
        print(f"[Embedding Error] Failed to embed text: {text[:50]}")
        raise e

def cosine_similarity(vec1, vec2):
    dot_product = 0
    norm1 = 0
    norm2 = 0

    for i in range(len(vec1)):
        dot_product += vec1[i] * vec2[i]
        norm1 += vec1[i] * vec1[i]
        norm2 += vec2[i] * vec2[i]

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot_product / (math.sqrt(norm1) * math.sqrt(norm2))

def semantic_search(user_query, 
logs,
start_time=None,
end_time=None,
category=None,
level=None, 
k=3,):
    output = logs

    if start_time is not None:
        filtered_logs = []
        for log in output:
            if log["timestamp"] >= start_time:
                filtered_logs.append(log)
        output = filtered_logs

    if end_time is not None:
        filtered_logs = []
        for log in output:
            if log["timestamp"] <= end_time:
                filtered_logs.append(log)
        output = filtered_logs

    if category is not None:
        filtered_logs = []
        category_norm = category.strip().lower()
        for log in output:
            if category_norm in log["categories"]:
                filtered_logs.append(log)
        output = filtered_logs

    if level is not None:
        filtered_logs = []
        level_norm = level.strip().lower()
        for log in output:
            if log["level"] == level_norm:
                filtered_logs.append(log)
        output = filtered_logs

    query_embedding = embed_text(user_query)
    scored_logs = []

    for log in output:
        score = cosine_similarity(query_embedding, log["embedding"])
        scored_logs.append((score, log))

    scored_logs.sort(reverse=True, key=lambda item: item[0])

    formatted_output = []
    count = 0

    for score, log in scored_logs:
        if count >= k:
            break

        formatted_log = {
            "score": score,
            "log_id": log["log_id"],
            "timestamp": log["timestamp"],
            "category": log["category"],
            "level": log["level"],
            "subject": log["subject"],
            "note_excerpt": log["notes"][:300]
        }

        formatted_output.append(formatted_log)
        count += 1

    return formatted_output




if __name__ == "__main__":
    path = "../logbook_250226_anonymized_2024plus (1).jsonl"
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
    
    results = semantic_search(
    user_query="beam issue",
    logs=logs,
    category="vacuum",
    k=3
)

    for log in results:
        print(log["score"])
        print(log["subject"])
        print(log["category"])
        print()
        
   
