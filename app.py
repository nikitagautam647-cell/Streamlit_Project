import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# =========================
# ORIGINAL PAGE THEME (RESTORED)
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #2b1d0e, #3e2723, #4e342e);
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #1b0f08;
}

.card {
    background-color: #4e342e;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.kpi {
    font-size: 26px;
    font-weight: bold;
    color: #ff80ab;
}

.desc {
    font-size: 13px;
    color: #fce4ec;
}

/* Tabs text */
button[data-baseweb="tab"] {
    color: black !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# COMPANY NAME
# =========================
st.markdown(
    "<h2 style='color:white;'>🏢 Nassau Candy Specialty Confections & Fine Food: Factory</h2>",
    unsafe_allow_html=True
)

st.title("🍬 Candy Logistics Intelligence Hub")

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("streamlit excel.xlsx", index_col=0)
df.columns = df.columns.str.strip()

# =========================
# DATE COLUMN AUTO DETECT
# =========================
date_col = None
for col in df.columns:
    if "date" in col.lower():
        date_col = col
        break

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

# =========================
# FILTERS
# =========================
st.sidebar.title("Smart Filters")

state = st.sidebar.multiselect("State", df["State_Province"].unique())
ship = st.sidebar.multiselect("Ship Mode", df["Ship_Mode"].unique())

# Date filter (BACK)
if date_col:
    date_range = st.sidebar.date_input(
        "Date Range",
        [df[date_col].min(), df[date_col].max()]
    )
else:
    date_range = None

lead = st.sidebar.slider(
    "Lead Time Range",
    int(df["Lead_time_actual"].min()),
    int(df["Lead_time_actual"].max()),
    (5, 20)
)

# =========================
# LINKEDIN FIXED (VISIBLE NOW)
# =========================
st.sidebar.markdown("## 🔗 LinkedIn Connect")
linkedin = st.sidebar.text_input("Enter LinkedIn Profile URL")

if linkedin:
    st.sidebar.markdown(
        f"<a href='{linkedin}' target='_blank'>👉 Open LinkedIn Profile</a>",
        unsafe_allow_html=True
    )

# =========================
# FILTER APPLY
# =========================
filtered = df.copy()

if state:
    filtered = filtered[filtered["State_Province"].isin(state)]

if ship:
    filtered = filtered[filtered["Ship_Mode"].isin(ship)]

if date_col and len(date_range) == 2:
    filtered = filtered[
        (filtered[date_col] >= pd.to_datetime(date_range[0])) &
        (filtered[date_col] <= pd.to_datetime(date_range[1]))
    ]

filtered = filtered[
    (filtered["Lead_time_actual"] >= lead[0]) &
    (filtered["Lead_time_actual"] <= lead[1])
]

# =========================
# KPI CARDS
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='card'>🎯 Orders<br><div class='kpi'>{len(filtered)}</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'>⏱ Avg Lead<br><div class='kpi'>{round(filtered['Lead_time_actual'].mean(),2)}</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'>💰 Profit<br><div class='kpi'>{round(filtered['Gross_Profit'].sum(),2)}</div></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='card'>📦 Sales<br><div class='kpi'>{round(filtered['Sales'].sum(),2)}</div></div>", unsafe_allow_html=True)

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "Performance",
    "Delay Risk",
    "Efficiency",
    "Smart Insights"
])

purple = "#9b5de5"
graph_bg = "#f5f5f5"

# =========================
# TAB 1
# =========================
with tab1:
    fig = px.histogram(filtered, x="Lead_time_actual", color_discrete_sequence=[purple])
    fig.update_layout(plot_bgcolor=graph_bg, paper_bgcolor=graph_bg)
    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 2
# =========================
with tab2:
    fig = px.pie(filtered, names="Dealyed_flag", color_discrete_sequence=[purple, "#d1c4e9"])
    fig.update_layout(plot_bgcolor=graph_bg, paper_bgcolor=graph_bg)
    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 3
# =========================
with tab3:
    fig = px.box(filtered, x="Ship_Mode", y="Lead_time_actual", color_discrete_sequence=[purple])
    fig.update_layout(plot_bgcolor=graph_bg, paper_bgcolor=graph_bg)
    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 4 (IMPROVED INSIGHTS)
# =========================
with tab4:
    if not filtered.empty:

        avg = filtered["Lead_time_actual"].mean()
        high_delay = filtered[filtered["Lead_time_actual"] > avg]

        top_state = high_delay["State_Province"].mode()[0] if not high_delay.empty else "N/A"
        worst_ship = filtered.groupby("Ship_Mode")["Lead_time_actual"].mean().idxmax()
        low_profit = filtered.groupby("State_Province")["Gross_Profit"].sum().idxmin()

        st.markdown(f"""
        <div class="card">

        🚨 <b>High Delay State:</b> {top_state}<br>
        👉 More orders exceed average delivery time in this region.<br><br>

        🚚 <b>Slow Shipping Mode:</b> {worst_ship}<br>
        👉 This mode consistently shows higher delivery time.<br><br>

        📉 <b>Low Profit Region:</b> {low_profit}<br>
        👉 Revenue is low compared to operational cost.<br><br>

        💡 <b>Action:</b> Optimize routing + reduce shipping delay + cost control.

        </div>
        """, unsafe_allow_html=True)