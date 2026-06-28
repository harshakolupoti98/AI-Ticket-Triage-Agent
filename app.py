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
st.markdown(
    "Upload customer support tickets, process them with Gemini AI, and analyze the results."
)

st.divider()

# =====================================================
# Upload CSV
# =====================================================

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

# =====================================================
# Process Button
# =====================================================

st.subheader("🤖 AI Ticket Processing")

if st.button("Process Tickets with Gemini", width="stretch"):

    print("\n==============================")
    print("PROCESS BUTTON CLICKED")
    print("==============================")

    if not os.path.exists("data/tickets.csv"):

        st.error("Please upload a CSV first.")

    else:

        ticket_df = pd.read_csv("data/tickets.csv")

        print(f"Tickets Found : {len(ticket_df)}")

        with st.spinner("Gemini is processing tickets..."):

            processed = run_triage(
                input_file="data/tickets.csv",
                output_file="data/processed_tickets.csv"
            )

        print(f"Processed Returned : {len(processed)}")

        st.success(
            f"Successfully processed {len(processed)} tickets!"
        )

        st.rerun()

# =====================================================
# Dashboard
# =====================================================

if (
    os.path.exists("data/tickets.csv")
    and
    os.path.exists("data/processed_tickets.csv")
):

    tickets = pd.read_csv("data/tickets.csv")
    processed = pd.read_csv("data/processed_tickets.csv")

    # Keep only matching rows
    rows = min(len(tickets), len(processed))

    tickets = tickets.iloc[:rows]
    processed = processed.iloc[:rows]

    processed["Ticket"] = tickets["ticket"].values

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

    # =================================================
    # Metrics
    # =================================================

    st.subheader("📊 Dashboard")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Total Tickets",
            len(display_df)
        )

    with c2:
        st.metric(
            "Categories",
            display_df["category"].nunique()
        )

    with c3:
        st.metric(
            "High Priority",
            len(
                display_df[
                    display_df["priority"] == "High"
                ]
            )
        )

    st.divider()

    # =================================================
    # Search & Filters
    # =================================================

    st.subheader("🔍 Search & Filter")

    search = st.text_input("Search Ticket")

    col1, col2 = st.columns(2)

    with col1:

        category = st.selectbox(
            "Category",
            ["All"] + sorted(
                display_df["category"].unique()
            )
        )

    with col2:

        priority = st.selectbox(
            "Priority",
            ["All"] + sorted(
                display_df["priority"].unique()
            )
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

    # =================================================
    # Charts
    # =================================================

    left, right = st.columns(2)

    with left:

        st.subheader("📂 Category Distribution")

        st.bar_chart(
            display_df["category"].value_counts()
        )

    with right:

        st.subheader("🚨 Priority Distribution")

        st.bar_chart(
            display_df["priority"].value_counts()
        )

    st.divider()

    # =================================================
    # Ticket Table
    # =================================================

    st.subheader("📋 Processed Tickets")

    st.dataframe(
        filtered,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # =================================================
    # Download
    # =================================================

    st.download_button(
        "📥 Download Processed CSV",
        processed.to_csv(index=False),
        "processed_tickets.csv",
        "text/csv",
        width="stretch"
    )

else:

    st.info("Upload a CSV and click 'Process Tickets with Gemini'.")