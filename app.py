import os
import streamlit as st
import pandas as pd

from agents.triage_agent import run_triage

st.set_page_config(
    page_title="AI Ticket Triage Agent",
    page_icon="🎫",
    layout="wide"
)

st.title("🎫 AI Ticket Triage Agent")
st.markdown("Upload customer support tickets, process them with Gemini AI, and analyze the results.")

st.divider()

# -------------------------------------------------------
# Upload CSV
# -------------------------------------------------------

st.subheader("📤 Upload Ticket CSV")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    with open("data/tickets.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("CSV uploaded successfully!")

st.divider()

# -------------------------------------------------------
# Process Button
# -------------------------------------------------------

st.subheader("🤖 AI Ticket Processing")

if st.button("Process Tickets with Gemini", use_container_width=True):

    if not os.path.exists("data/tickets.csv"):
        st.error("Please upload a CSV first.")

    else:

        with st.spinner("Gemini is processing tickets..."):

            run_triage(
                input_file="data/tickets.csv",
                output_file="data/processed_tickets.csv"
            )

        st.success("Processing completed successfully!")

st.divider()

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

if os.path.exists("data/tickets.csv") and os.path.exists("data/processed_tickets.csv"):

    tickets = pd.read_csv("data/tickets.csv")
    processed = pd.read_csv("data/processed_tickets.csv")

    processed["Ticket"] = tickets["ticket"]

    display_df = processed[
        [
            "ticket_id",
            "Ticket",
            "category",
            "priority",
            "summary",
            "suggested_action"
        ]
    ]

    # ---------------------------------------------------
    # Metrics
    # ---------------------------------------------------

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Tickets",
            len(display_df)
        )

    with col2:
        st.metric(
            "Categories",
            display_df["category"].nunique()
        )

    with col3:
        st.metric(
            "High Priority",
            len(display_df[
                display_df["priority"] == "High"
            ])
        )

    st.divider()

    # ---------------------------------------------------
    # Search
    # ---------------------------------------------------

    st.subheader("🔍 Search & Filter")

    search = st.text_input(
        "Search ticket"
    )

    category = st.selectbox(
        "Category",
        ["All"] + sorted(display_df["category"].unique())
    )

    priority = st.selectbox(
        "Priority",
        ["All"] + sorted(display_df["priority"].unique())
    )

    filtered = display_df.copy()

    if search:

        filtered = filtered[
            filtered["Ticket"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if category != "All":

        filtered = filtered[
            filtered["category"] == category
        ]

    if priority != "All":

        filtered = filtered[
            filtered["priority"] == priority
        ]

    st.divider()

    # ---------------------------------------------------
    # Charts
    # ---------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📂 Category Distribution")

        st.bar_chart(
            display_df["category"].value_counts()
        )

    with col2:

        st.subheader("🚨 Priority Distribution")

        st.bar_chart(
            display_df["priority"].value_counts()
        )

    st.divider()

    # ---------------------------------------------------
    # Ticket Table
    # ---------------------------------------------------

    st.subheader("📋 Processed Tickets")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ---------------------------------------------------
    # Download
    # ---------------------------------------------------

    st.download_button(
        "📥 Download Processed CSV",
        data=processed.to_csv(index=False),
        file_name="processed_tickets.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info("Upload a CSV and process tickets to view the dashboard.")