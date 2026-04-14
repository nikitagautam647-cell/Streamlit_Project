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
df = pd.read_excel("streamlit excel.xlsx", index_col=0)

# REMOVE UNWANTED COLUMNS
df = df.loc[:, ~df.columns.str.contains("Unnamed", na=False)]

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip()

# =========================
# DEBUG VIEW (optional)
# =========================
st.write("Columns in dataset:", df.columns.tolist())

# =========================
# REQUIRED COLUMNS CHECK
# =========================
required_cols = [
    "State_province",
    "Ship_mode",
    "Sales",
    "Gross_profit",
    "Lead_time_actual"
]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

state_filter = st.sidebar.multiselect(
    "Select State",
    df["State_province"].dropna().unique()
)

ship_filter = st.sidebar.multiselect(
    "Select Ship Mode",
    df["ship_mode"].dropna().unique()
)

# =========================
# FILTER DATA
# =========================
filtered_df = df.copy()

if state_filter:
    filtered_df = filtered_df[filtered_df["State_province"].isin(state_filter)]

if ship_filter:
    filtered_df = filtered_df[filtered_df["ship_mode"].isin(ship_filter)]

# =========================
# KPIs
# =========================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(filtered_df))
col2.metric("Avg Lead Time", round(filtered_df["lead_time_actual"].mean(), 2))
col3.metric("Total Profit", round(filtered_df["gross_profit"].sum(), 2))

st.markdown("---")

# =========================
# SALES vs PROFIT
# =========================
st.subheader("💰 Sales vs Profit")

fig1 = px.scatter(
    filtered_df,
    x="sales",
    y="gross_profit",
    color="State_province"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# TOP STATES
# =========================
st.subheader("🏆 Top States by Profit")

top_states = (
    filtered_df.groupby("State_province")["gross_profit"]
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
    x="ship_mode",
    y="lead_time_actual"
)

st.plotly_chart(fig2, use_container_width=True)