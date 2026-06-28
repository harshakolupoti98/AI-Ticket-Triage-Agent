import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Settings
# --------------------------------------------------

BATCH_SIZE = 200
REQUEST_DELAY_SECONDS = 15


# --------------------------------------------------
# Get Gemini API Key
# --------------------------------------------------

def get_gemini_api_key():

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        import streamlit as st

        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]

    except Exception:
        pass

    raise Exception(
        "GEMINI_API_KEY not found. Add it in .env locally or Streamlit Secrets after deployment."
    )


client = genai.Client(
    api_key=get_gemini_api_key()
)


# --------------------------------------------------
# Convert Any CSV Row Into Ticket Text
# --------------------------------------------------

def row_to_ticket_text(row):

    parts = []

    for column_name, value in row.items():

        if pd.isna(value):
            continue

        value = str(value).strip()

        if value == "":
            continue

        parts.append(f"{column_name}: {value}")

    return "\n".join(parts)


def convert_csv_to_tickets(df):

    df = df.dropna(how="all")

    tickets = []

    for _, row in df.iterrows():

        ticket_text = row_to_ticket_text(row)

        if ticket_text.strip() != "":
            tickets.append(ticket_text)

    if len(tickets) == 0:
        raise Exception("The uploaded CSV does not contain any usable data.")

    return tickets


# --------------------------------------------------
# Clean Gemini JSON Response
# --------------------------------------------------

def clean_json_response(response_text):

    cleaned = response_text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start != -1 and end != -1:
        cleaned = cleaned[start:end + 1]

    return cleaned


# --------------------------------------------------
# Gemini Batch Processing
# --------------------------------------------------

def process_batch(batch_text, batch_count, batch_number, total_batches):

    prompt = f"""
You are an AI customer support ticket triage agent.

Analyze ALL records below separately.

Each record may come from any CSV format.
Column names may be different.
Use the available row information to understand the customer issue.

Records:

{batch_text}

IMPORTANT RULES:

- You must return exactly {batch_count} results.
- Do not stop early.
- Do not combine records.
- Create one result object for every record.
- Use the Record ID shown for each record as the ticket_id.
- If a record has extra fields like customer name, email, date, status, product, source, or ID, use them only as context.
- Your output must focus on the customer support issue.

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
Billing Issue
General Support Issue

Priority MUST be ONLY:

High
Medium
Low

No markdown.
No explanation.
Return JSON only.
"""

    print(f"\nProcessing batch {batch_number} of {total_batches}...")
    print(f"Records in this batch: {batch_count}")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    cleaned = clean_json_response(response.text)

    data = json.loads(cleaned)

    return data["results"]


# --------------------------------------------------
# Main Processing Function From DataFrame
# --------------------------------------------------

def run_triage_from_dataframe(df):

    ticket_list = convert_csv_to_tickets(df)

    total_tickets = len(ticket_list)

    print(f"Total records found: {total_tickets}")
    print(f"Batch size: {BATCH_SIZE}")

    all_results = []

    total_batches = (total_tickets + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_index in range(total_batches):

        start_index = batch_index * BATCH_SIZE
        end_index = min(start_index + BATCH_SIZE, total_tickets)

        batch_tickets = ticket_list[start_index:end_index]

        batch_text = ""

        for global_index, ticket in enumerate(batch_tickets, start=start_index + 1):

            batch_text += f"""
Record ID: {global_index}
Record Details:
{ticket}

"""

        batch_results = process_batch(
            batch_text=batch_text,
            batch_count=len(batch_tickets),
            batch_number=batch_index + 1,
            total_batches=total_batches
        )

        for result_index, result in enumerate(batch_results):

            global_ticket_id = start_index + result_index + 1
            result["ticket_id"] = global_ticket_id

            all_results.append(result)

        print(f"Batch {batch_index + 1} complete.")
        print(f"Total processed so far: {len(all_results)}")

        if batch_index < total_batches - 1:
            print(f"Waiting {REQUEST_DELAY_SECONDS} seconds before next batch...")
            time.sleep(REQUEST_DELAY_SECONDS)

    output = pd.DataFrame(all_results)

    rows = min(len(output), len(ticket_list))

    output = output.iloc[:rows].copy()

    output["Ticket"] = ticket_list[:rows]

    output = output[
        [
            "ticket_id",
            "Ticket",
            "category",
            "priority",
            "summary",
            "suggested_action"
        ]
    ]

    print("\nDONE - Gemini batch processing complete")
    print(f"Processed {len(output)} records.")

    return output


# --------------------------------------------------
# Optional Local File Processing
# --------------------------------------------------

def run_triage(
    input_file="data/tickets.csv",
    output_file="data/processed_tickets.csv"
):

    df = pd.read_csv(input_file)

    output = run_triage_from_dataframe(df)

    output.to_csv(
        output_file,
        index=False
    )

    print(f"Saved to: {output_file}")

    return output


# --------------------------------------------------
# Run from Terminal
# --------------------------------------------------

if __name__ == "__main__":
    run_triage()