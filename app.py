import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Nassau Dashboard", layout="wide")

# =========================
# CUSTOM THEME (POWER BI STYLE)
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #d6c28a;  /* golden background */
    color: white;
}
h1, h2, h3 {
    color: #4e342e;
}
[data-testid="stMetric"] {
    background-color: #6d4c41;
    color: white;
    padding: 12px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🍬 Nassau Candy Logistics & Sales Dashboard")

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("streamlit excel.xlsx", index_col=0)

df = df.loc[:, ~df.columns.str.contains("Unnamed", na=False)]
df.columns = df.columns.str.strip()

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# =========================
# SIDEBAR
# =========================
st.sidebar.header("🎛 Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Order_Date"].min(), df["Order_Date"].max()]
)

state_filter = st.sidebar.multiselect(
    "State",
    df["State_Province"].unique()
)

ship_filter = st.sidebar.multiselect(
    "Ship Mode",
    df["Ship_Mode"].unique()
)

lead_filter = st.sidebar.slider(
    "Lead Time",
    int(df["Lead_time_actual"].min()),
    int(df["Lead_time_actual"].max()),
    (int(df["Lead_time_actual"].min()), int(df["Lead_time_actual"].max()))
)

# =========================
# FILTER
# =========================
filtered_df = df.copy()

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
# KPI
# =========================
st.subheader("📊 Key Metrics")

c1, c2, c3 = st.columns(3)

c1.metric("Orders", len(filtered_df))
c2.metric("Avg Lead Time", round(filtered_df["Lead_time_actual"].mean(), 2))
c3.metric("Profit", round(filtered_df["Gross_Profit"].sum(), 2))

st.markdown("---")

# =========================
# COMMON GRAPH STYLE
# =========================
graph_layout = dict(
    plot_bgcolor="#2b2b2b",
    paper_bgcolor="#2b2b2b",
    font=dict(color="white")
)

# =========================
# ROUTE
# =========================
st.subheader("🚚 Route Efficiency")

route = filtered_df.groupby("Routes")["Lead_time_actual"].mean().sort_values()

fig1 = px.bar(route, color=route.values,
              color_continuous_scale=["#f4c27a", "#5d4037"])

fig1.update_layout(graph_layout, height=400)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# SHIP MODE
# =========================
st.subheader("📦 Ship Mode Comparison")

fig2 = px.box(
    filtered_df,
    x="Ship_Mode",
    y="Lead_time_actual",
    color="Ship_Mode",
    color_discrete_sequence=["#f4c27a", "#8d6e63", "#3e2723"]
)

fig2.update_layout(graph_layout, height=400)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# SALES VS PROFIT
# =========================
st.subheader("💰 Sales vs Profit")

fig3 = px.scatter(
    filtered_df,
    x="Sales",
    y="Gross_Profit",
    color="Region",
    color_discrete_sequence=["#ffcc80", "#bcaaa4", "#6d4c41"]
)

fig3.update_layout(graph_layout, height=450)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# MAP
# =========================
st.subheader("🗺 Shipping Map")

map_data = filtered_df.groupby("State_Province")["Lead_time_actual"].mean().reset_index()

fig4 = px.choropleth(
    map_data,
    locations="State_Province",
    locationmode="USA-states",
    color="Lead_time_actual",
    scope="usa",
    color_continuous_scale=["#fff3e0", "#5d4037"]
)

fig4.update_layout(graph_layout, height=500)

st.plotly_chart(fig4, use_container_width=True)

# =========================
# TOP STATES
# =========================
st.subheader("🏆 Top States")

top_states = filtered_df.groupby("State_Province")["Gross_Profit"].sum().sort_values(ascending=False).head(10)

fig5 = px.bar(
    top_states,
    color=top_states.values,
    color_continuous_scale=["#ffe0b2", "#4e342e"]
)

fig5.update_layout(graph_layout, height=400)

st.plotly_chart(fig5, use_container_width=True)

# =========================
# TABLE
# =========================
st.subheader("📋 Detailed Data")

st.dataframe(filtered_df, use_container_width=True)