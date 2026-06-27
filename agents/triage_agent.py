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

def process_batch(tickets):

    prompt = f"""
You are an AI customer support ticket triage agent.

Analyze ALL tickets below separately.

Tickets:

{tickets}

IMPORTANT RULES:

- You must return exactly 20 ticket results.
- ticket_id must go from 1 to 20.
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
    }},
    {{
      "ticket_id": 2,
      "category": "",
      "priority": "",
      "summary": "",
      "suggested_action": ""
    }}

    ...

    {{
      "ticket_id": 20,
      "category": "",
      "priority": "",
      "summary": "",
      "suggested_action": ""
    }}
  ]
}}

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

    # Read input CSV
    df = pd.read_csv(input_file)

    # Detect ticket column automatically
    ticket_column = None

    for col in df.columns:
        if col.lower().strip() == "ticket":
            ticket_column = col
            break

    if ticket_column is None:
        raise Exception("No 'ticket' column found in CSV.")

    # Remove empty tickets
    df = df.dropna(subset=[ticket_column])

    # TESTING ONLY
    # Process first 20 tickets
    df = df.head(20)

    ticket_text = ""

    for count, ticket in enumerate(df[ticket_column], start=1):

        ticket_text += f"""
Ticket ID: {count}
Ticket: {ticket}

"""

    print(f"Sending {len(df)} tickets to Gemini...")

    # Process with Gemini
    results = process_batch(ticket_text)

    # Convert to DataFrame
    output = pd.DataFrame(results)

    # Save results
    output.to_csv(
        output_file,
        index=False
    )

    print("\nDONE - Gemini batch processing complete")
    print(f"Processed {len(output)} tickets.")
    print(f"Saved to: {output_file}")

    # Return DataFrame (used later by Streamlit)
    return output


# --------------------------------------------------
# Run from Terminal
# --------------------------------------------------

if __name__ == "__main__":
    run_triage()