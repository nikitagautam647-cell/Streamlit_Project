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
df = pd.read_excel("Nassau Candy Distributor main sheet.xlsx")

# CLEAN COLUMN NAMES (IMPORTANT FIX)
df.columns = (
    df.columns.str.strip()
    .str.replace(" ", "_")
    .str.replace("/", "_")
)

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

# FILTER DATA
filtered_df = df.copy()

if state_filter:
    filtered_df = filtered_df[filtered_df["State_Province"].isin(state_filter)]

if ship_filter:
    filtered_df = filtered_df[filtered_df["Ship_Mode"].isin(ship_filter)]

# =========================
# KPIs
# =========================
st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(filtered_df))
col2.metric("Avg Lead Time", round(filtered_df["Lead_Time"].mean(), 2))
col3.metric("Total Profit", round(filtered_df["Profit"].sum(), 2))

st.markdown("---")

# =========================
# SALES ANALYSIS
# =========================
st.subheader("💰 Sales Analysis")

fig1 = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="State_Province",
    title="Sales vs Profit"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# TOP STATES
# =========================
st.subheader("🏆 Top Performing States")

top_states = (
    filtered_df.groupby("State_Province")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_states)

# =========================
# LOGISTICS ANALYSIS
# =========================
st.subheader("🚚 Logistics Analysis")

fig2 = px.box(
    filtered_df,
    x="Ship_Mode",
    y="Lead_Time",
    title="Lead Time by Ship Mode"
)

st.plotly_chart(fig2, use_container_width=True)