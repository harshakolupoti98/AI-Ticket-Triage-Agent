# AI Ticket Triage Dashboard

A deployed AI-powered support ticket triage system that allows users to upload CSV files, automatically classify support issues, assign priority, generate ticket summaries, recommend next actions, and visualize results in an interactive dashboard.

## Live App

https://ai-ticket-triage-dashboard.streamlit.app

## Project Overview

The AI Ticket Triage Dashboard is designed to help support and operations teams reduce manual ticket review time. Users can upload support ticket data in CSV format, and the application processes each record using Gemini AI to generate structured triage results.

The app supports different CSV formats, meaning the uploaded file does not need to follow one fixed column structure. Each row is converted into a support ticket record and analyzed by the AI model.

## Key Features

* Upload CSV support ticket data
* Supports flexible CSV column structures
* Automatically classifies tickets into issue categories
* Assigns priority as High, Medium, or Low
* Generates concise ticket summaries
* Recommends suggested actions for support teams
* Displays dashboard metrics and charts
* Provides search and filter functionality
* Allows users to download processed results
* Supports batch processing for larger CSV files
* Uses session-based processing so users do not see each other’s uploaded data

## Tech Stack

* Python
* Streamlit
* Pandas
* Gemini API
* Google GenAI SDK
* GitHub
* Streamlit Community Cloud

## How It Works

1. User uploads a CSV file.
2. The app reads the uploaded data.
3. Each row is converted into a support ticket record.
4. Tickets are processed in batches using Gemini AI.
5. The AI returns category, priority, summary, and suggested action.
6. Results are displayed in an interactive dashboard.
7. User can download the processed CSV.

## Batch Processing

The system includes batch processing to handle larger CSV files more reliably. Instead of sending all records in one request, the app splits records into manageable batches and combines the results after processing.

Example:

* 100 tickets → 1 batch
* 200 tickets → 1 batch if batch size is 200
* 500 tickets → multiple batches

This improves scalability and reduces the chance of incomplete AI responses.

## User Session Privacy

The app uses Streamlit session state to isolate each user's uploaded and processed data.

This means:

* User A only sees User A’s uploaded file and results
* User B only sees User B’s uploaded file and results
* Processed data is not shared across users

## Local Setup

Clone the repository:

```bash
git clone https://github.com/harshakolupoti98/AI-Ticket-Triage-Agent.git
cd AI-Ticket-Triage-Agent
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

For Windows PowerShell:

```bash
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Run the app locally:

```bash
streamlit run app.py
```

## Deployment

The app is deployed using Streamlit Community Cloud.

Deployment configuration:

```text
Repository: harshakolupoti98/AI-Ticket-Triage-Agent
Branch: main
Main file path: app.py
```

The Gemini API key is stored securely using Streamlit Secrets.

## Author

Developed by Sai Sri Harsha Kolupoti

AI-Powered Support Ticket Triage System
