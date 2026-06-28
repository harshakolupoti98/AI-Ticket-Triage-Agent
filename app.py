import os
import hashlib
import streamlit as st
import pandas as pd

from agents.triage_agent import run_triage

st.set_page_config(
    page_title="AI Ticket Triage Dashboard",
    page_icon="🎫",
    layout="wide"
)

st.title("🎫 AI Ticket Triage Dashboard")

st.caption("Developed by Sai Sri Harsha Kolupoti | AI-Powered Support Ticket Triage System")

st.markdown(
    "Upload support ticket data to automatically classify issues, assign priority, generate summaries, and recommend next actions."
)

st.divider()

# =====================================================
# Upload CSV
# =====================================================

st.subheader("📤 Upload Support Ticket Data")

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    os.makedirs("data", exist_ok=True)

    file_bytes = uploaded_file.getvalue()
    file_hash = hashlib.md5(file_bytes).hexdigest()

    previous_file_hash = st.session_state.get("uploaded_file_hash")

    if previous_file_hash != file_hash:

        with open("data/tickets.csv", "wb") as f:
            f.write(file_bytes)

        if os.path.exists("data/processed_tickets.csv"):
            os.remove("data/processed_tickets.csv")

        st.session_state["uploaded_file_hash"] = file_hash

        st.success("File uploaded successfully.")
        st.info("Review the data preview below, then start AI processing.")

    else:

        st.success("File already uploaded.")

    preview_df = pd.read_csv("data/tickets.csv")

    st.subheader("Data Preview")
    st.dataframe(
        preview_df.head(10),
        width="stretch",
        hide_index=True
    )

st.divider()

# =====================================================
# Process Button
# =====================================================

st.subheader("🤖 AI Processing")

if st.button("Analyze Tickets", width="stretch"):

    print("\n==============================")
    print("PROCESS BUTTON CLICKED")
    print("==============================")

    if not os.path.exists("data/tickets.csv"):

        st.error("Please upload a CSV file first.")

    else:

        try:
            ticket_df = pd.read_csv("data/tickets.csv")

            print(f"CSV Rows Found : {len(ticket_df)}")

            with st.spinner("Analyzing tickets with AI..."):

                processed = run_triage(
                    input_file="data/tickets.csv",
                    output_file="data/processed_tickets.csv"
                )

            print(f"Processed Returned : {len(processed)}")

            st.success(
                f"Analysis complete. {len(processed)} tickets processed successfully."
            )

            st.rerun()

        except Exception as e:

            st.error(str(e))
            print(f"ERROR: {e}")

# =====================================================
# Dashboard
# =====================================================

if os.path.exists("data/processed_tickets.csv"):

    processed = pd.read_csv("data/processed_tickets.csv")

    display_df = processed.copy()

    st.subheader("📊 Ticket Insights Dashboard")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Total Tickets",
            len(display_df)
        )

    with c2:
        st.metric(
            "Issue Categories",
            display_df["category"].nunique()
        )

    with c3:
        st.metric(
            "High Priority Tickets",
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

    st.subheader("🔍 Search and Filter Tickets")

    search = st.text_input("Search by ticket details, summary, or action")

    col1, col2 = st.columns(2)

    with col1:

        category = st.selectbox(
            "Filter by Category",
            ["All"] + sorted(
                display_df["category"].dropna().unique()
            )
        )

    with col2:

        priority = st.selectbox(
            "Filter by Priority",
            ["All"] + sorted(
                display_df["priority"].dropna().unique()
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
            |
            filtered["summary"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            filtered["suggested_action"].str.contains(
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

        st.subheader("📂 Tickets by Category")

        st.bar_chart(
            display_df["category"].value_counts()
        )

    with right:

        st.subheader("🚨 Tickets by Priority")

        st.bar_chart(
            display_df["priority"].value_counts()
        )

    st.divider()

    # =================================================
    # Ticket Table
    # =================================================

    st.subheader("📋 Processed Ticket Details")

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
        "📥 Download Processed Results",
        display_df.to_csv(index=False),
        "processed_tickets.csv",
        "text/csv",
        width="stretch"
    )

else:

    st.info("Upload a CSV file and click 'Analyze Tickets' to generate the dashboard.")