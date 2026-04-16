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

    print(len(logs[0]["embedding"]))
    
    query = "vacuum issue"
    query_embedding = embed_text(query)
    print(len(query_embedding)) 
    score = cosine_similarity(query_embedding, logs[0]["embedding"])
    print(score)