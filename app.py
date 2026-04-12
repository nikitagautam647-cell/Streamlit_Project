import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="Nassau Dashboard", layout="wide")

st.title("📦 Nassau Candy Logistics & Sales Dashboard")

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("nassau_data.xlsx", header=0)

# =========================
# CLEAN COLUMNS (standardize)
# =========================
df.columns = df.columns.str.strip()

# =========================
# RENAME (IMPORTANT STEP)
# =========================
df = df.rename(columns={
    "State_province": "State_Province",
    "ship_mode": "Ship_Mode",
    "sales": "Sales",
    "gross_profit": "Profit",
    "lead_time_actual": "Lead_Time"
})

# =========================
# SAFETY CHECK
# =========================
required_cols = ["State_Province", "Ship_Mode", "Sales", "Profit", "Lead_Time"]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.write("Available columns:", df.columns)
    st.stop()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

state_filter = st.sidebar.multiselect(
    "Select State",
    df["State_Province"].dropna().unique()
)

ship_filter = st.sidebar.multiselect(
    "Select Ship Mode",
    df["Ship_Mode"].dropna().unique()
)

# =========================
# FILTER DATA
# =========================
filtered_df = df.copy()

if state_filter:
    filtered_df = filtered_df[filtered_df["State_Province"].isin(state_filter)]

if ship_filter:
    filtered_df = filtered_df[filtered_df["Ship_Mode"].isin(ship_filter)]

# =========================
# KPIs
# =========================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(filtered_df))
col2.metric("Avg Lead Time", round(filtered_df["Lead_Time"].mean(), 2))
col3.metric("Total Profit", round(filtered_df["Profit"].sum(), 2))

st.markdown("---")

# =========================
# SALES vs PROFIT
# =========================
st.subheader("💰 Sales vs Profit")

fig1 = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="State_Province"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# TOP STATES
# =========================
st.subheader("🏆 Top 10 States by Profit")

top_states = (
    filtered_df.groupby("State_Province")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_states)

# =========================
# SHIPPING ANALYSIS
# =========================
st.subheader("🚚 Ship Mode vs Lead Time")

fig2 = px.box(
    filtered_df,
    x="Ship_Mode",
    y="Lead_Time"
)

st.plotly_chart(fig2, use_container_width=True)