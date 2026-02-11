import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(page_title="Coffee Sales Dashboard", layout="wide")

st.title("☕ Coffee Sales Analytics Dashboard")
st.write("Upload your sales Excel file to analyze performance trends.")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file, sheet_name="Transactions")

    # ---------------- SIDEBAR FILTERS ----------------
    st.sidebar.header("Filters")

    locations = st.sidebar.multiselect(
        "Store Location",
        options=df["store_location"].unique(),
        default=df["store_location"].unique()
    )

    days = st.sidebar.multiselect(
        "Day of Week",
        options=df["Day of week"].unique(),
        default=df["Day of week"].unique()
    )

    filtered_df = df[
        (df["store_location"].isin(locations)) &
        (df["Day of week"].isin(days))
    ]

    # ---------------- KPIs ----------------
    total_revenue = filtered_df["Revenue per transaction"].sum()
    avg_revenue = filtered_df["Revenue per transaction"].mean()
    total_transactions = len(filtered_df)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"{total_revenue:,.2f}")
    col2.metric("Average Revenue", f"{avg_revenue:,.2f}")
    col3.metric("Transactions", total_transactions)

    st.divider()

    # ---------------- HOURLY TREND ----------------
    st.subheader("Hourly Revenue Trend")
    hourly = filtered_df.groupby("Hour of Day")["Revenue per transaction"].sum()

    fig1, ax1 = plt.subplots()
    hourly.plot(ax=ax1, marker="o")
    ax1.set_xlabel("Hour")
    ax1.set_ylabel("Revenue")
    st.pyplot(fig1)

    # ---------------- DAY TREND ----------------
    st.subheader("Revenue by Day")
    day = filtered_df.groupby("Day of week")["Revenue per transaction"].sum()

    fig2, ax2 = plt.subplots()
    day.plot(kind="bar", ax=ax2)
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Revenue")
    st.pyplot(fig2)

    # ---------------- STORE COMPARISON ----------------
    st.subheader("Store Performance")
    store = filtered_df.groupby("store_location")["Revenue per transaction"].sum()

    fig3, ax3 = plt.subplots()
    store.plot(kind="bar", ax=ax3)
    ax3.set_xlabel("Store")
    ax3.set_ylabel("Revenue")
    st.pyplot(fig3)

    # ---------------- INSIGHTS ----------------
    st.subheader("Key Insights")

    peak_hour = hourly.idxmax()
    best_day = day.idxmax()
    best_store = store.idxmax()

    st.success(f"""
    Peak Hour: {peak_hour}:00  
    Best Day: {best_day}  
    Top Store: {best_store}
    """)

else:
    st.info("Upload a dataset to start analysis.")
