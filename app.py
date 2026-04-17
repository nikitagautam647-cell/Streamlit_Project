import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# =========================
# DARKER CHOCOLATE THEME
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #5d4037, #6d4c41, #8d6e63);
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #4e342e;
}

.card {
    background-color: #5d4037;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.12);
}

.kpi {
    font-size: 26px;
    font-weight: bold;
    color: #ffffff;
}

/* FILTER TEXT */
label, .stSelectbox, .stMultiSelect, .stSlider, .stTextInput {
    color: white !important;
}

/* LINK COLORS */
a, .stSidebar a {
    color: #ffcc80 !important;
    text-decoration: underline !important;
}

/* TABS */
button[data-baseweb="tab"] {
    color: black !important;
    font-weight: bold !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# COMPANY NAME (WHITE)
# =========================
st.markdown("""
<h2 style='color:white; font-weight:bold;'>
🏢 Nassau Candy Specialty Confections & Fine Food: Factory
</h2>
""", unsafe_allow_html=True)

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

# 📅 DATE FILTER ADDED
if date_col:
    date_range = st.sidebar.date_input(
        "Date Range",
        [df[date_col].min(), df[date_col].max()]
    )
else:
    date_range = None
    st.sidebar.info("No date column found. Date filter is currently unavailable.")

lead = st.sidebar.slider(
    "Lead Time Range",
    int(df["Lead_time_actual"].min()),
    int(df["Lead_time_actual"].max()),
    (int(df["Lead_time_actual"].min()), int(df["Lead_time_actual"].max()))
)

# =========================
# LINKEDIN
# =========================
st.sidebar.markdown("## 🔗 LinkedIn Connect")
linkedin = st.sidebar.text_input("Paste LinkedIn profile URL")

if linkedin:
    linkedin_url = linkedin.strip()
    if not linkedin_url.lower().startswith("http"):
        linkedin_url = "https://" + linkedin_url
    st.sidebar.markdown(
        f'<a href="{linkedin_url}" target="_blank">👉 Open LinkedIn Profile</a>',
        unsafe_allow_html=True
    )
else:
    st.sidebar.info("Paste a LinkedIn profile URL to make it visible here.")

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

has_data = not filtered.empty

# =========================
# KPI CARDS
# =========================
c1, c2, c3, c4 = st.columns(4)

order_count = len(filtered)
avg_delivery = round(filtered["Lead_time_actual"].mean(), 2) if has_data else 0
profit_total = round(filtered["Gross_Profit"].sum(), 2) if has_data else 0
sales_total = round(filtered["Sales"].sum(), 2) if has_data else 0

c1.markdown(f"""<div class="card">🎯 Orders<br><div class="kpi">{order_count}</div></div>""", unsafe_allow_html=True)
c2.markdown(f"""<div class="card">⏱ Avg Delivery<br><div class="kpi">{avg_delivery}</div></div>""", unsafe_allow_html=True)
c3.markdown(f"""<div class="card">💰 Profit<br><div class="kpi">{profit_total}</div></div>""", unsafe_allow_html=True)
c4.markdown(f"""<div class="card">📦 Sales<br><div class="kpi">{sales_total}</div></div>""", unsafe_allow_html=True)

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
graph_bg = "#f5f5f5"   # OFF WHITE

# =========================
# TAB 1
# =========================
with tab1:
    c1, c2 = st.columns(2)
    fig1 = px.histogram(filtered, x="Lead_time_actual", color_discrete_sequence=[purple])
    fig1.update_layout(plot_bgcolor=graph_bg, paper_bgcolor=graph_bg, font_color="black")
    c1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        filtered.groupby("State_Province")["Sales"].sum().reset_index().sort_values("Sales", ascending=False),
        x="State_Province",
        y="Sales",
        color_discrete_sequence=[purple]
    )
    fig2.update_layout(plot_bgcolor=graph_bg, paper_bgcolor=graph_bg, font_color="black", xaxis_title="State", yaxis_title="Sales")
    c2.plotly_chart(fig2, use_container_width=True)

# =========================
# TAB 2
# =========================
with tab2:
    c1, c2 = st.columns(2)
    if not has_data:
        st.warning("No data available with the current filter selection. Change the filters to see delay-risk charts.")
    else:
        if "Dealyed_flag" in filtered.columns:
            fig1 = px.pie(filtered, names="Dealyed_flag", color_discrete_sequence=[purple, "#d1c4e9"], title="Delay Status Share")
        else:
            fig1 = px.pie(filtered, names="Ship_Mode", color_discrete_sequence=[purple, "#d1c4e9"], title="Delay Status Share")
        fig1.update_layout(plot_bgcolor=graph_bg, paper_bgcolor=graph_bg, font_color="black")
        c1.plotly_chart(fig1, use_container_width=True)

        fig2 = px.bar(
            filtered.groupby("Ship_Mode")["Lead_time_actual"].mean().reset_index().sort_values("Lead_time_actual", ascending=False),
            x="Ship_Mode",
            y="Lead_time_actual",
            color_discrete_sequence=[purple],
            title="Average Lead Time by Ship Mode"
        )
        fig2.update_layout(plot_bgcolor=graph_bg, paper_bgcolor=graph_bg, font_color="black", xaxis_title="Ship Mode", yaxis_title="Avg Lead Time")
        c2.plotly_chart(fig2, use_container_width=True)

# =========================
# TAB 3
# =========================
with tab3:
    c1, c2 = st.columns(2)
    if not has_data:
        st.warning("No data available with the current filter selection. Change the filters to view delivery-efficiency analytics.")
    else:
        fig1 = px.box(filtered, x="Ship_Mode", y="Lead_time_actual", color_discrete_sequence=[purple], title="Lead-Time Distribution by Ship Mode")
        fig1.update_layout(plot_bgcolor=graph_bg, paper_bgcolor=graph_bg, font_color="black")
        c1.plotly_chart(fig1, use_container_width=True)

        try:
            fig2 = px.scatter(
                filtered,
                x="Sales",
                y="Gross_Profit",
                color="Ship_Mode" if "Ship_Mode" in filtered.columns else None,
                title="Sales vs Gross Profit",
                trendline="ols"
            )
        except Exception:
            fig2 = px.scatter(
                filtered,
                x="Sales",
                y="Gross_Profit",
                color="Ship_Mode" if "Ship_Mode" in filtered.columns else None,
                title="Sales vs Gross Profit"
            )
        fig2.update_layout(plot_bgcolor=graph_bg, paper_bgcolor=graph_bg, font_color="black", xaxis_title="Sales", yaxis_title="Gross Profit")
        c2.plotly_chart(fig2, use_container_width=True)

# =========================
# TAB 4
# =========================
with tab4:
    if not has_data:
        st.warning("No recommendations can be generated because the filtered dataset is empty. Please widen the date range or remove some filters.")
    else:
        avg_lead = filtered["Lead_time_actual"].mean()
        high_delay = filtered[filtered["Lead_time_actual"] > avg_lead]

        top_state = high_delay["State_Province"].mode()[0] if not high_delay.empty else "N/A"
        worst_ship = filtered.groupby("Ship_Mode")["Lead_time_actual"].mean().idxmax()
        low_profit = filtered.groupby("State_Province")["Gross_Profit"].sum().idxmin()

        st.markdown(f"""
        <div class="card">

        🚨 <b>High Delay State:</b> {top_state}<br>
        👉 Reason: This state has more orders with lead time above the overall average.<br><br>

        🚚 <b>Slowest Shipping Mode:</b> {worst_ship}<br>
        👉 Reason: It has the highest average lead time among shipping modes.<br><br>

        📉 <b>Lowest Profit Region:</b> {low_profit}<br>
        👉 Reason: It has the lowest gross profit total for the selected filters.<br><br>

        💡 <b>Recommended Action:</b> Focus on faster carriers and improve operations in the high-delay state.

        </div>
        """, unsafe_allow_html=True)

        rec_fig = px.bar(
            filtered.groupby("State_Province")["Lead_time_actual"].mean().reset_index().sort_values("Lead_time_actual", ascending=False).head(5),
            x="State_Province",
            y="Lead_time_actual",
            color_discrete_sequence=[purple],
            title="Top 5 States by Average Lead Time"
        )
        rec_fig.update_layout(plot_bgcolor=graph_bg, paper_bgcolor=graph_bg, font_color="black", xaxis_title="State", yaxis_title="Avg Lead Time")
        st.plotly_chart(rec_fig, use_container_width=True)