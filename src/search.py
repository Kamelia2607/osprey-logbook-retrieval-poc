from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional



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
            if log["category"] == category:
                filtered_logs.append(log)
        output = filtered_logs

    if level is not None:
        filtered_logs = []
        for log in output:
            if log["level"] == level:
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
    from mock_data import mock_logs

    mock_output = search_logs(
        query="Has there been any vaccum instability",
        logs = mock_logs,
        start_time=datetime(2026,2,19),
        k=2
    )
    for log in mock_output:
        print(f"Log ID: {log['log_id']}")
        print(f"Time: {log['timestamp']}")
        print(f"Category: {log['category']}")
        print(f"Level: {log['level']}")
        print(f"Subject: {log['subject']}")
        print(f"Notes: {log['note_excerpt']}")
        print()

    

    



