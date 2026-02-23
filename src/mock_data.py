from datetime import datetime

mock_logs = [
    {
        "log_id": 1,
        "timestamp": datetime(2026, 2, 20, 1, 15),
        "category": "vacuum",
        "level": "ERROR",
        "subject": "Vacuum pump trip",
        "notes": "Vacuum instability detected in sector 3. Pressure spike observed."
    },
    {
        "log_id": 2,
        "timestamp": datetime(2026, 2, 19, 14, 30),
        "category": "rf",
        "level": "WARN",
        "subject": "RF fluctuation",
        "notes": "Minor instability but system recovered automatically."
    },
    {
        "log_id": 3,
        "timestamp": datetime(2026, 2, 18, 9, 5),
        "category": "vacuum",
        "level": "INFO",
        "subject": "Routine vacuum check",
        "notes": "All readings stable."
    }
]