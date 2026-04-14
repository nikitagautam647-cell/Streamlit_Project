import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Nassau Dashboard", layout="wide")

st.title("🍬 Nassau Candy Logistics & Sales Dashboard")

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("streamlit excel.xlsx", index_col=0)

df = df.loc[:, ~df.columns.str.contains("Unnamed", na=False)]
df.columns = df.columns.str.strip()

# =========================
# DATE CONVERSION
# =========================
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🎛 Filters")

# Date filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Order_Date"].min(), df["Order_Date"].max()]
)

# State filter
state_filter = st.sidebar.multiselect(
    "Select State",
    df["State_Province"].unique()
)

# Ship mode filter
ship_filter = st.sidebar.multiselect(
    "Ship Mode",
    df["Ship_Mode"].unique()
)

# Lead time slider
lead_filter = st.sidebar.slider(
    "Lead Time Range",
    int(df["Lead_time_actual"].min()),
    int(df["Lead_time_actual"].max()),
    (int(df["Lead_time_actual"].min()), int(df["Lead_time_actual"].max()))
)

# =========================
# APPLY FILTERS
# =========================
filtered_df = df.copy()

# Date filter apply
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Order_Date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["Order_Date"] <= pd.to_datetime(date_range[1]))
    ]

if state_filter:
    filtered_df = filtered_df[filtered_df["State_Province"].isin(state_filter)]

if ship_filter:
    filtered_df = filtered_df[filtered_df["Ship_Mode"].isin(ship_filter)]

filtered_df = filtered_df[
    (filtered_df["Lead_time_actual"] >= lead_filter[0]) &
    (filtered_df["Lead_time_actual"] <= lead_filter[1])
]

# =========================
# KPIs
# =========================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(filtered_df))
col2.metric("Avg Lead Time", round(filtered_df["Lead_time_actual"].mean(), 2))
col3.metric("Total Profit", round(filtered_df["Gross_Profit"].sum(), 2))

st.markdown("---")

# =========================
# ROUTE EFFICIENCY
# =========================
st.subheader("🚚 Route Efficiency Overview")

route_perf = filtered_df.groupby("Routes")["Lead_time_actual"].mean().sort_values()

fig_route = px.bar(
    route_perf,
    color=route_perf.values,
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_route, use_container_width=True)

# =========================
# SHIP MODE COMPARISON
# =========================
st.subheader("📦 Ship Mode Comparison")

fig_ship = px.box(
    filtered_df,
    x="Ship_Mode",
    y="Lead_time_actual",
    color="Ship_Mode",
    color_discrete_sequence=px.colors.sequential.Reds
)

st.plotly_chart(fig_ship, use_container_width=True)

# =========================
# SALES VS PROFIT
# =========================
st.subheader("💰 Sales vs Profit")

fig_sales = px.scatter(
    filtered_df,
    x="Sales",
    y="Gross_Profit",
    color="State_Province",
    color_discrete_sequence=px.colors.sequential.RdPu
)

st.plotly_chart(fig_sales, use_container_width=True)

# =========================
# MAP VISUALIZATION
# =========================
st.subheader("🗺 Geographic Shipping Map")

map_data = filtered_df.groupby("State_Province")["Lead_time_actual"].mean().reset_index()

fig_map = px.choropleth(
    map_data,
    locations="State_Province",
    locationmode="USA-states",
    color="Lead_time_actual",
    scope="usa",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_map, use_container_width=True)

# =========================
# STATE DRILL DOWN
# =========================
st.subheader("🔍 State Level Insights")

state_perf = filtered_df.groupby("State_Province")["Gross_Profit"].sum().sort_values(ascending=False)

st.bar_chart(state_perf)

# =========================
# ORDER LEVEL DATA
# =========================
st.subheader("📋 Order Level Shipment Data")

st.dataframe(filtered_df)