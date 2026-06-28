import os
import json
import pandas as pd
from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# --------------------------------------------------
# Gemini Batch Processing
# --------------------------------------------------

def process_batch(tickets, ticket_count):

    prompt = f"""
You are an AI customer support ticket triage agent.

Analyze ALL tickets below separately.

Tickets:

{tickets}

IMPORTANT RULES:

- You must return exactly {ticket_count} ticket results.
- ticket_id must go from 1 to {ticket_count}.
- Do not stop after one ticket.
- Do not combine tickets.
- Create one result object for every ticket.

Return ONLY valid JSON.

Use this exact structure:

{{
  "results": [
    {{
      "ticket_id": 1,
      "category": "",
      "priority": "",
      "summary": "",
      "suggested_action": ""
    }}
  ]
}}

Continue the same JSON structure until all {ticket_count} tickets have been returned.

Categories MUST be ONLY one of:

Authentication Issue
Account Access
Performance Issue
Application Bug
Notification Issue
Data Issue
Integration Issue
UI Issue
Permission Issue
Security Issue

Priority MUST be ONLY:

High
Medium
Low

No markdown.
No explanation.
Return JSON only.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("\n========================================")
    print("RAW GEMINI RESPONSE")
    print("========================================\n")
    print(response.text)
    print("\n========================================\n")

    cleaned = response.text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

    data = json.loads(cleaned)

    return data["results"]


# --------------------------------------------------
# Main Processing Function
# --------------------------------------------------

def run_triage(
    input_file="data/tickets.csv",
    output_file="data/processed_tickets.csv"
):

    df = pd.read_csv(input_file)

    ticket_column = None

    for col in df.columns:
        if col.lower().strip() == "ticket":
            ticket_column = col
            break

    if ticket_column is None:
        raise Exception("No 'ticket' column found in CSV.")

    df = df.dropna(subset=[ticket_column])

    ticket_count = len(df)

    ticket_text = ""

    for count, ticket in enumerate(df[ticket_column], start=1):

        ticket_text += f"""
Ticket ID: {count}
Ticket: {ticket}

"""

    print(f"Sending {ticket_count} tickets to Gemini...")

    results = process_batch(ticket_text, ticket_count)

    output = pd.DataFrame(results)

    output.to_csv(
        output_file,
        index=False
    )

    print("\nDONE - Gemini batch processing complete")
    print(f"Processed {len(output)} tickets.")
    print(f"Saved to: {output_file}")

    return output


# --------------------------------------------------
# Run from Terminal
# --------------------------------------------------

if __name__ == "__main__":
    run_triage()