import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# =========================
# THEME
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
</style>
""", unsafe_allow_html=True)

st.title("🍬 Candy Logistics Intelligence Hub")

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("streamlit excel.xlsx", index_col=0)
df.columns = df.columns.str.strip()

# =========================
# FILTERS
# =========================
st.sidebar.title("Smart Filters")

state = st.sidebar.multiselect("State", df["State_Province"].unique())
ship = st.sidebar.multiselect("Ship Mode", df["Ship_Mode"].unique())

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

filtered = filtered[
    (filtered["Lead_time_actual"] >= lead[0]) &
    (filtered["Lead_time_actual"] <= lead[1])
]

# =========================
# KPI CARDS
# =========================
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"""
<div class="card">
Orders<br>
<div class="kpi">{len(filtered)}</div>
<p class="desc">Total processed shipments</p>
</div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class="card">
Avg Delivery Time<br>
<div class="kpi">{round(filtered["Lead_time_actual"].mean(),2)}</div>
<p class="desc">Average shipping duration</p>
</div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class="card">
Total Profit<br>
<div class="kpi">{round(filtered["Gross_Profit"].sum(),2)}</div>
<p class="desc">Revenue after cost</p>
</div>
""", unsafe_allow_html=True)

c4.markdown(f"""
<div class="card">
Total Sales<br>
<div class="kpi">{round(filtered["Sales"].sum(),2)}</div>
<p class="desc">Overall business volume</p>
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

# =========================
# TAB 1 - OVERVIEW
# =========================
with tab1:
    st.subheader("Performance Overview")

    col1, col2 = st.columns(2)

    fig1 = px.histogram(
        filtered,
        x="Lead_time_actual",
        color_discrete_sequence=["#ff80ab"]
    )
    fig1.update_layout(plot_bgcolor="#4e342e", paper_bgcolor="#4e342e", font_color="white")

    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        filtered.groupby("State_Province")["Gross_Profit"].sum().reset_index(),
        x="State_Province",
        y="Gross_Profit",
        color_discrete_sequence=["#ff80ab"]
    )
    fig2.update_layout(plot_bgcolor="#4e342e", paper_bgcolor="#4e342e", font_color="white")

    col2.plotly_chart(fig2, use_container_width=True)

# =========================
# TAB 2 - DELAY RISK
# =========================
with tab2:
    st.subheader("Delay Risk Analysis")

    fig3 = px.pie(
        filtered,
        names="Dealyed_flag",
        color_discrete_sequence=["#ff80ab", "#8d6e63"]
    )
    fig3.update_layout(plot_bgcolor="#4e342e", paper_bgcolor="#4e342e", font_color="white")

    st.plotly_chart(fig3, use_container_width=True)

# =========================
# TAB 3 - EFFICIENCY
# =========================
with tab3:
    st.subheader("Delivery Efficiency")

    fig4 = px.box(
        filtered,
        x="Ship_Mode",
        y="Lead_time_actual",
        color_discrete_sequence=["#ff80ab"]
    )
    fig4.update_layout(plot_bgcolor="#4e342e", paper_bgcolor="#4e342e", font_color="white")

    st.plotly_chart(fig4, use_container_width=True)

# =========================
# TAB 4 - SMART INSIGHTS
# =========================
with tab4:
    st.subheader("Smart Recommendations")

    avg_lead = filtered["Lead_time_actual"].mean()

    high_delay = filtered[filtered["Lead_time_actual"] > avg_lead]

    top_state = high_delay.groupby("State_Province")["Lead_time_actual"].mean().idxmax()
    worst_ship = filtered.groupby("Ship_Mode")["Lead_time_actual"].mean().idxmax()
    low_profit = filtered.groupby("State_Province")["Gross_Profit"].sum().idxmin()

    st.markdown(f"""
    <div class="card">

    🚨 <b>High Delay State:</b> {top_state}  
    → Needs immediate logistics optimization  
    <br><br>

    🚚 <b>Slowest Shipping Mode:</b> {worst_ship}  
    → Improve delivery efficiency  
    <br><br>

    📉 <b>Lowest Profit Region:</b> {low_profit}  
    → Requires business strategy improvement  
    <br><br>

    ⚡ <b>Recommended Actions:</b><br>
    - Optimize high delay routes<br>
    - Improve slow shipping methods<br>
    - Focus on profitable regions<br>
    - Reduce operational inefficiencies  

    </div>
    """, unsafe_allow_html=True)