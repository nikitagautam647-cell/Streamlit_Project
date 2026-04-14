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

# DEBUG
st.write("Columns in dataset:", df.columns.tolist())

# =========================
# REQUIRED COLUMNS CHECK (FIXED)
# =========================
required_cols = [
    "State_Province",
    "Ship_Mode",
    "Sales",
    "Gross_Profit",
    "Lead_time_actual"
]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

# =========================
# SIDEBAR FILTERS (FIXED)
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
# KPIs (FIXED)
# =========================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(filtered_df))
col2.metric("Avg Lead Time", round(filtered_df["Lead_time_actual"].mean(), 2))
col3.metric("Total Profit", round(filtered_df["Gross_Profit"].sum(), 2))

st.markdown("---")

# =========================
# SALES vs PROFIT (FIXED)
# =========================
st.subheader("💰 Sales vs Profit")

fig1 = px.scatter(
    filtered_df,
    x="Sales",
    y="Gross_Profit",
    color="State_Province"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# TOP STATES (FIXED)
# =========================
st.subheader("🏆 Top States by Profit")

top_states = (
    filtered_df.groupby("State_Province")["Gross_Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_states)

# =========================
# SHIPPING ANALYSIS (FIXED)
# =========================
st.subheader("🚚 Ship Mode vs Lead Time")

fig2 = px.box(
    filtered_df,
    x="Ship_Mode",
    y="Lead_time_actual"
)

st.plotly_chart(fig2, use_container_width=True)