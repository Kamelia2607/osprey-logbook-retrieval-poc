from openai import OpenAI

#PUT YOUR KEY IN HERE:
client = OpenAI(api_key="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")


def summarize_logs(user_query, retrieved_logs):
    prompt = (
        "You are assisting an operator in troubleshooting high-stakes ALS problems.\n"
        "Use only the provided logs.\n"
        "Do not make conjectures.\n"
        "If the evidence is weak or incomplete, say so clearly.\n"
        "Keep the response concise and operator-friendly.\n\n"
        f"Operator query:\n{user_query}\n\n"
        "Retrieved logs:\n"
        "Do not use markdown formatting (no bold, no asterisks). Return plain text."
    )

    for log in retrieved_logs:
        prompt += f"- Log ID: {log['log_id']}\n"
        prompt += f"  Timestamp: {log['timestamp']}\n"
        prompt += f"  Category: {log['category']}\n"
        prompt += f"  Level: {log['level']}\n"
        prompt += f"  Subject: {log['subject']}\n"
        prompt += f"  Notes: {log['note_excerpt']}\n\n"

    prompt += (
        "Task:\n"
        "1. Summarize what likely happened.\n"
        "2. Mention any recurring pattern or likely issue only if supported by the logs.\n"
        "3. Reference log IDs, timestamps, or subjects when useful.\n"
        "4. Do not invent missing information.\n"
    )

    response = client.responses.create(
        model="gpt-5.4",
        input=prompt,
    )

    return response.output_text


if __name__ == "__main__":
    sample_logs = [
        {
            "log_id": "164431",
            "timestamp": "2024-09-06 16:27:51",
            "category": "EPS, Operations, Vacuum",
            "level": "info",
            "subject": "Beam Loss Root Cause",
            "note_excerpt": "Vacuum spike and related beam loss were observed in sector 3."
        },
        {
            "log_id": "164450",
            "timestamp": "2024-09-06 17:02:10",
            "category": "Operations, Vacuum",
            "level": "warn",
            "subject": "Vacuum spike detected",
            "note_excerpt": "Pressure briefly rose in sector 3 before beam was lost."
        }
    ]

    summary = summarize_logs("beam issue", sample_logs)
    print(summary)