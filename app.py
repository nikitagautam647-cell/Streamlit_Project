import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# =========================
# THEME (PAGE + GRAPH FIX)
# =========================
st.markdown("""
<style>
/* PAGE BACKGROUND (previous chocolate light theme) */
.stApp {
    background: linear-gradient(to right, #8d6e63, #a1887f, #bcaaa4);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #5d4037;
}

/* Cards */
.card {
    background-color: #7b5e57;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
}

/* KPI */
.kpi {
    font-size: 26px;
    font-weight: bold;
    color: #f3e5f5;
}

/* FILTER TEXT */
label, .stSelectbox, .stMultiSelect, .stSlider {
    color: white !important;
}

/* TABS TEXT (BLACK BOLD) */
button[data-baseweb="tab"] {
    color: black !important;
    font-weight: bold !important;
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: white !important;
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
# AUTO DATE COLUMN
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

# ✅ DATE FILTER (BACK AGAIN)
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
# LINKEDIN CONNECT (BACK)
# =========================
st.sidebar.markdown("## 🔗 Connect")
linkedin = st.sidebar.text_input("LinkedIn Profile URL")

if linkedin:
    st.sidebar.markdown(f"[Open LinkedIn Profile]({linkedin})")

# =========================
# KPI CARDS
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"""
<div class="card">
🎯 Orders<br>
<div class="kpi">{len(filtered)}</div>
</div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class="card">
⏱ Avg Delivery<br>
<div class="kpi">{round(filtered["Lead_time_actual"].mean(),2)}</div>
</div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class="card">
💰 Profit<br>
<div class="kpi">{round(filtered["Gross_Profit"].sum(),2)}</div>
</div>
""", unsafe_allow_html=True)

c4.markdown(f"""
<div class="card">
📦 Sales<br>
<div class="kpi">{round(filtered["Sales"].sum(),2)}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# TABS
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "Performance Overview",
    "Delay Risk Analysis",
    "Delivery Efficiency",
    "Smart Recommendations"
])

purple = "#9b5de5"

# =========================
# GRAPH STYLE (OFF WHITE FIX)
# =========================
graph_bg = "#f5f5f5"

# =========================
# TAB 1
# =========================
with tab1:
    st.subheader("Performance Overview")

    fig1 = px.histogram(filtered, x="Lead_time_actual", color_discrete_sequence=[purple])
    fig1.update_layout(
        plot_bgcolor=graph_bg,
        paper_bgcolor=graph_bg,
        font_color="black"
    )
    st.plotly_chart(fig1, use_container_width=True)

# =========================
# TAB 2
# =========================
with tab2:
    st.subheader("Delay Risk Analysis")

    fig2 = px.pie(filtered, names="Dealyed_flag", color_discrete_sequence=[purple, "#d1c4e9"])
    fig2.update_layout(
        plot_bgcolor=graph_bg,
        paper_bgcolor=graph_bg,
        font_color="black"
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# TAB 3
# =========================
with tab3:
    st.subheader("Delivery Efficiency")

    fig3 = px.box(filtered, x="Ship_Mode", y="Lead_time_actual", color_discrete_sequence=[purple])
    fig3.update_layout(
        plot_bgcolor=graph_bg,
        paper_bgcolor=graph_bg,
        font_color="black"
    )
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# TAB 4 (SMART INSIGHTS)
# =========================
with tab4:
    st.subheader("Smart Recommendations (With Reason)")

    if not filtered.empty:

        avg_lead = filtered["Lead_time_actual"].mean()
        high_delay = filtered[filtered["Lead_time_actual"] > avg_lead]

        top_state = high_delay["State_Province"].mode()[0] if not high_delay.empty else "N/A"
        worst_ship = filtered.groupby("Ship_Mode")["Lead_time_actual"].mean().idxmax()
        low_profit = filtered.groupby("State_Province")["Gross_Profit"].sum().idxmin()

        st.markdown(f"""
        <div class="card">

        🚨 <b>High Delay State:</b> {top_state}<br>
        👉 Reason: Orders in this state exceed average delivery time<br><br>

        🚚 <b>Slowest Shipping Mode:</b> {worst_ship}<br>
        👉 Reason: This mode has highest delivery duration<br><br>

        📉 <b>Lowest Profit Region:</b> {low_profit}<br>
        👉 Reason: Low revenue + high logistics cost impact<br><br>

        💡 <b>Action:</b> Improve routing, reduce delay, and optimize cost structure.

        </div>
        """, unsafe_allow_html=True)