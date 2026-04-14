import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# COLORS (POWER BI MATCH)
# =========================
PRIMARY = "#d81b60"   # pink/magenta (United wala)
DARK = "#880e4f"
BLUE = "#1f77b4"      # filter blue
BG = "#f7f6f3"

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Nassau Dashboard", layout="wide")

# =========================
# CUSTOM CSS
# =========================
st.markdown(f"""
<style>
.stApp {{
    background-color: {BG};
}}

/* Titles */
h1, h2, h3 {{
    color: {DARK};
}}

/* KPI Cards */
[data-testid="stMetric"] {{
    background-color: {PRIMARY};
    color: white;
    padding: 15px;
    border-radius: 12px;
}}

/* Sidebar background */
section[data-testid="stSidebar"] {{
    background-color: white;
}}

/* FILTER COLOR (BLUE) */
div[data-baseweb="select"] > div {{
    border-color: {BLUE} !important;
}}

div[data-baseweb="slider"] span {{
    background-color: {BLUE} !important;
}}

div[data-baseweb="slider"] div {{
    background-color: {BLUE} !important;
}}

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
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

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
# FILTER DATA
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
st.subheader("Key Metrics")

c1, c2, c3 = st.columns(3)

c1.metric("Orders", len(filtered_df))
c2.metric("Avg Lead Time", round(filtered_df["Lead_time_actual"].mean(), 2))
c3.metric("Profit", round(filtered_df["Gross_Profit"].sum(), 2))

st.markdown("---")

# =========================
# GRAPH STYLE
# =========================
layout = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#333")
)

# =========================
# ROUTE
# =========================
st.subheader("Route Efficiency")

route = filtered_df.groupby("Routes")["Lead_time_actual"].mean().sort_values()

fig1 = px.bar(route, color=route.values,
              color_continuous_scale=["#f8bbd0", PRIMARY])

fig1.update_layout(layout)
st.plotly_chart(fig1, use_container_width=True)

# =========================
# SHIP MODE (IMPORTANT FIX)
# =========================
st.subheader("Ship Mode Comparison")

fig2 = px.box(
    filtered_df,
    x="Ship_Mode",
    y="Lead_time_actual",
    color="Ship_Mode",
    color_discrete_sequence=[PRIMARY, "#f06292", "#ad1457"]
)

fig2.update_layout(layout)
st.plotly_chart(fig2, use_container_width=True)

# =========================
# SALES VS PROFIT
# =========================
st.subheader("Sales vs Profit")

fig3 = px.scatter(
    filtered_df,
    x="Sales",
    y="Gross_Profit",
    color="Region",
    color_discrete_sequence=[PRIMARY, "#f06292", "#ad1457"]
)

fig3.update_layout(layout)
st.plotly_chart(fig3, use_container_width=True)

# =========================
# TOP STATES (IMPORTANT FIX)
# =========================
st.subheader("Top States")

top_states = filtered_df.groupby("State_Province")["Gross_Profit"].sum().sort_values(ascending=False).head(10)

fig5 = px.bar(
    top_states,
    color=top_states.values,
    color_continuous_scale=["#f8bbd0", PRIMARY]
)

fig5.update_layout(layout)
st.plotly_chart(fig5, use_container_width=True)

# =========================
# TABLE
# =========================
st.subheader("Detailed Data")

st.dataframe(filtered_df, use_container_width=True)