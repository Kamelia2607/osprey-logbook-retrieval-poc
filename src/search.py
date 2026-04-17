from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional
import json

# Standardizer:
def normalize_log(raw):
    #standardize ID:
    log_id = raw.get("log_id", raw.get("id"))

    #Convert unix to stand time
    timestamp_raw = raw.get("timestamp")
    if timestamp_raw:
        timestamp = datetime.fromtimestamp(int(timestamp_raw))
    else:
        timestamp = None
    
    #Standardize notes/details/blanks
    notes = raw.get("notes") or raw.get("details") or ""

    #Base fields:
    subject = raw.get("subject", "")
    category = raw.get("category", "")
    level = raw.get("level", "")

    #Split categories/ levels into parsable inputs:
    categories = []
    if category:
        category_options = category.split(",")
        for c in category_options:
            cleaned = c.strip().lower()
            categories.append(cleaned)
    
    if level:
        level = level.lower()
    
    search_text = f"{subject} {notes}".strip()
        
   
    return {
    "log_id": log_id,
    "timestamp": timestamp,
    "category": category,
    "categories": categories,
    "level": level,
    "subject": subject,
    "notes": notes,
    "search_text": search_text
    
   }



#Base search function

def search_logs(
    query: str, 
    logs: list, 
    start_time: Optional[datetime] = None, 
    end_time: Optional[datetime] = None, 
    category: Optional[str] = None,
    level: Optional[str] =None,
    k: int = 3
):
    #Basic filtering POC
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
        for log in output:
            if category.strip().lower() in log["categories"]:
                filtered_logs.append(log)
        output = filtered_logs

    if level is not None:
        filtered_logs = []
        level_norm = level.strip().lower()
        for log in output:
            if log["level"] == level_norm:
                filtered_logs.append(log)
        output = filtered_logs
    
    # Basic Ranking POC
    query_terms = query.lower().split()
    scored_logs =[]

    for log in output:
        text = (log["subject"]+ " " + log["notes"]).lower()
        match = 0
        for t in query_terms: 
            if t in text:
                match +=1
        scored_logs.append((match,log))
    
    #Sort logs by score and extracked them
    scored_logs.sort(reverse=True, key=lambda item: item[0])
    ranked_logs =[]
    for score, content in scored_logs:
        ranked_logs.append(content)
    
    #Removing 0 match logs
    non_zero_ranked = []
    for score,log in scored_logs:
        if score>0:
            non_zero_ranked.append(log)
    ranked_logs = non_zero_ranked

    #Limiting return to desired K amount
    most_relevant_logs =[]
    count = 0

    for log in ranked_logs:
        if count >= k:
            break
        most_relevant_logs.append(log)
        count+=1
       
    
    #Format results 
    formatted_output =[]
    for log in most_relevant_logs:
        formatted_log = {
            "log_id": log["log_id"],
            "timestamp": log["timestamp"],
            "category": log["category"],
            "level": log["level"],
            "subject": log["subject"],
            "note_excerpt": log["notes"][:300]
        }
        formatted_output.append(formatted_log)
    return formatted_output


if __name__ == "__main__":
    path = "../logbook_250226_anonymized_2024plus (1).jsonl"
    logs = []

    with open(path) as f:
        for line in f:
            raw_log = json.loads(line)
            normalized_log = normalize_log(raw_log)
            logs.append(normalized_log)
    

    print(logs[0]["categories"])

    #test:
    print(logs[0]["search_text"])

      
        

    



