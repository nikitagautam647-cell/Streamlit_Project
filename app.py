import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE SETUP
st.set_page_config(page_title="Nassau Dashboard", layout="wide")
st.title("📦 Nassau Candy Logistics & Sales Dashboard")

# LOAD DATA
df = pd.read_excel("Nassau Candy Distributor main sheet.xlsx")

# CLEAN COLUMNS
df.columns = (
    df.columns.str.strip()
    .str.replace(" ", "_")
    .str.replace("/", "_")
)

# SAFETY CHECK
if "State_Province" not in df.columns:
    st.error("State_Province column not found in Excel file")
    st.write(df.columns)
    st.stop()

# FILTERS
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

# KPIs
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(filtered_df))
col2.metric("Avg Lead Time", round(filtered_df["Lead_Time"].mean(), 2))
col3.metric("Total Profit", round(filtered_df["Profit"].sum(), 2))

st.markdown("---")

# SALES CHART
st.subheader("💰 Sales vs Profit")

fig1 = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="State_Province"
)

st.plotly_chart(fig1, use_container_width=True)

# TOP STATES
st.subheader("🏆 Top States by Profit")

top_states = (
    filtered_df.groupby("State_Province")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_states)

# LOGISTICS
st.subheader("🚚 Ship Mode Analysis")

fig2 = px.box(
    filtered_df,
    x="Ship_Mode",
    y="Lead_Time"
)

st.plotly_chart(fig2, use_container_width=True)
