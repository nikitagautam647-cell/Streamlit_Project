import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nassau Dashboard", layout="wide")

st.title("📦 Nassau Candy Logistics & Sales Dashboard")

# Load file
df = pd.read_excel("Nassau Candy Distributor main sheet.xlsx")

# Clean columns
df.columns = df.columns.str.strip().str.replace(" ", "_")

st.sidebar.header("Filters")

state = st.sidebar.multiselect("State", df["State_Province"].dropna().unique())
ship = st.sidebar.multiselect("Ship Mode", df["Ship_Mode"].dropna().unique())

filtered = df.copy()

if state:
    filtered = filtered[filtered["State_Province"].isin(state)]

if ship:
    filtered = filtered[filtered["Ship_Mode"].isin(ship)]

# KPIs
st.subheader("📊 KPIs")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(filtered))
col2.metric("Avg Lead Time", round(filtered["Lead_Time"].mean(), 2))
col3.metric("Total Profit", round(filtered["Profit"].sum(), 2))

st.markdown("---")

# Sales vs Profit
st.subheader("Sales vs Profit")

fig = px.scatter(filtered, x="Sales", y="Profit", color="State_Province")
st.plotly_chart(fig, use_container_width=True)

# Top States
st.subheader("Top States by Profit")

top = filtered.groupby("State_Province")["Profit"].sum().sort_values(ascending=False).head(10)

st.bar_chart(top)