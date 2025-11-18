# dashboard_uber.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Uber Trip Insights Dashboard", layout="wide")

# -------------------------
# Animated blue-turquoise gradient + glass effect + text styling
# -------------------------
st.markdown(
    """
    <style>
    /* Full-page animated gradient */
    html, body, [class*="css"] {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #0077B6, #0096C7, #00C2CB, #48CAE4);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: #40E0D0;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Subtle overlay to make text readable */
    [class*="css"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(120deg, rgba(0,119,182,0.08), rgba(0,200,203,0.08));
        pointer-events: none;
    }

    /* Main dashboard container */
    .main-container {
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
        padding: 12px;
    }

    /* Glass style cards for KPI & charts */
    .glass {
        background: rgba(255,255,255,0.15);
        padding:12px;
        border-radius:15px;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        margin-bottom:16px;
    }

    .title {
        font-size: 36px;
        text-align: center;
        margin-top: -85px;
        margin-bottom: 6px;
        color: #ff6f61;

        text-shadow: 0 3px 12px rgba(0,0,0,0.35);
        font-family: "Montserrat", sans-serif;
    }

    .subtitle {
        text-align:center;
        margin-bottom:20px;
        font-size:18px;
        color: rgba(255,255,255,0.9);
        font-family: "Lato", sans-serif;
    }

    /* Filters row */
    .filters {
        display:flex;
        gap:12px;
        justify-content:center;
        align-items:center;
        margin-bottom:24px;
        flex-wrap: wrap;
    }

    .filters div {
        flex: 1;
        max-width: 180px;
    }

    input[type=text] {
        padding: 10px 12px;
        font-size: 16px;
        border: 2px solid rgba(255,255,255,0.6);
        border-radius: 10px;
        outline: none;
        width: 100%;
        background: rgba(255,255,255,0.25);
        color: black;  /* typed text color */
    }

    input[type=text]::placeholder {
        color: rgba(255,255,255,0.7);
    }

    .explain {
        color:#ffffff;
        font-size:14px;
        margin-top:6px;
        margin-bottom:14px;
    }
    </style>
    """, unsafe_allow_html=True
)

# -------------------------
# Wrap dashboard
# -------------------------
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# -------------------------
# Load Data
# -------------------------
DATA_PATH = r"C:\Users\anush\OneDrive\Desktop\Documents\uber_trip_project\data\uber_analysis_2015_cleaned.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"CSV not found at:\n{DATA_PATH}")
    st.stop()
except Exception as e:
    st.error(f"Failed to load CSV: {e}")
    st.stop()

expected_cols = {'dispatching_base_number', 'date', 'active_vehicles', 'trips', 'day', 'month', 'weekday'}
missing = expected_cols - set(df.columns)
if missing:
    st.error(f"CSV missing expected columns: {', '.join(missing)}")
    st.stop()

df['month'] = df['month'].astype(int)
df['day'] = df['day'].astype(int)
df['weekday'] = df['weekday'].astype(str)
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# -------------------------
# Header
# -------------------------
st.markdown("<div class='title'>🚖 Uber Trip Insights Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Interactive, recruiter-friendly, animated dashboard</div>", unsafe_allow_html=True)

# -------------------------
# Filters
# -------------------------
month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
months_available = sorted(df['month'].unique())
month_options = [f"{m} - {month_map.get(m,str(m))}" for m in months_available]
day_options = sorted(df['day'].unique())
weekday_options = sorted(df['weekday'].unique(), key=lambda x: ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"].index(x) if x in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] else 0)

st.markdown("<div class='filters'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])

with col1:
    month_input = st.text_input("Month (type to suggest)", key="month_input")
    selected_month = None
    if month_input.strip():
        q = month_input.strip().lower()
        matches = [opt for opt in month_options if q in opt.lower()]
        if matches:
            selected_month_label = st.selectbox("Select month", matches, key="month_select")
            selected_month = int(selected_month_label.split(" - ")[0])

with col2:
    day_input = st.text_input("Date (day number)", key="day_input")
    selected_day = None
    if day_input.strip():
        q = day_input.strip().lower()
        matches = [str(d) for d in day_options if q in str(d)]
        if matches:
            selected_day = int(st.selectbox("Select date", matches, key="day_select"))

with col3:
    weekday_input = st.text_input("Weekday (type to suggest)", key="weekday_input")
    selected_weekday = None
    if weekday_input.strip():
        q = weekday_input.strip().lower()
        matches = [w for w in weekday_options if q in w.lower()]
        if matches:
            selected_weekday = st.selectbox("Select weekday", matches, key="weekday_select")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Apply filters
# -------------------------
filtered = df.copy()
if selected_month: filtered = filtered[filtered['month'] == selected_month]
if selected_day: filtered = filtered[filtered['day'] == selected_day]
if selected_weekday: filtered = filtered[filtered['weekday'].str.lower() == selected_weekday.lower()]
if filtered.empty:
    st.warning("No data matches filters. Showing full dataset.")
    filtered = df.copy()

# -------------------------
# KPI Row
# -------------------------
k1,k2,k3,k4 = st.columns([1.6,1.6,1.6,1.6])
with k1:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("Total Trips")
    st.markdown(f"<h2 style='margin:0'>{int(filtered['trips'].sum()):,}</h2>", unsafe_allow_html=True)
    st.markdown("<small class='explain'>Total trips in selected scope.</small>", unsafe_allow_html=True)

with k2:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("Active Vehicles")
    st.markdown(f"<h2 style='margin:0'>{int(filtered['active_vehicles'].sum()):,}</h2>", unsafe_allow_html=True)
    st.markdown("<small class='explain'>Total active vehicles.</small>", unsafe_allow_html=True)

with k3:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("Unique Bases")
    st.markdown(f"<h2 style='margin:0'>{filtered['dispatching_base_number'].nunique()}</h2>", unsafe_allow_html=True)
    st.markdown("<small class='explain'>Distinct bases contributing trips.</small>", unsafe_allow_html=True)

with k4:
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("Avg Trips / Row")
    st.markdown(f"<h2 style='margin:0'>{round(filtered['trips'].mean(),1)}</h2>", unsafe_allow_html=True)
    st.markdown("<small class='explain'>Average trips per row.</small>", unsafe_allow_html=True)

st.markdown("---")

# -------------------------
# Prepare chart data
# -------------------------
weekday_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
month_order = list(range(1,13))
trips_by_month = filtered.groupby('month')['trips'].sum().reindex(month_order, fill_value=0).reset_index().rename(columns={"month":"Month","trips":"Trips"})
trips_by_weekday = filtered.groupby('weekday')['trips'].sum().reindex(weekday_order, fill_value=0).reset_index().rename(columns={"weekday":"Weekday","trips":"Trips"})
polar_df = trips_by_month.copy()
hist_df = filtered['trips']
heat_df = filtered.groupby(['weekday','month'])['trips'].sum().reset_index()
pivot = heat_df.pivot(index='weekday', columns='month', values='trips').reindex(weekday_order).fillna(0)
for m in month_order:
    if m not in pivot.columns: pivot[m] = 0
pivot = pivot[month_order]
scatter_df = filtered[['trips','active_vehicles']].copy()

# -------------------------
# Charts with 2-line stylish explanations
# -------------------------

row1_col1,row1_col2 = st.columns(2)
row2_col1,row2_col2 = st.columns(2)
row3_col1,row3_col2 = st.columns(2)

# 1) Bar chart: Trips per Month
with row1_col1:
    st.markdown("<div class='glass chart-card'>", unsafe_allow_html=True)
    fig_bar = px.bar(trips_by_month, x='Month', y='Trips', color='Trips', color_continuous_scale=px.colors.sequential.Blues)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("<div class='explain'><b style='color:#40E0D0'>What it shows:Total trips for each month.<br><b style='color:#40E0D0'>How to use:Helps identify peak travel months.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 2) Pie chart: Trips by Weekday
with row1_col2:
    st.markdown("<div class='glass chart-card'>", unsafe_allow_html=True)
    fig_pie = px.pie(trips_by_weekday, names='Weekday', values='Trips', hole=0.38)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("<div class='explain'><b style='color:#40E0D0'>What it shows: Distribution of trips across weekdays.<br><b style='color:#40E0D0'>How to use: See which weekdays are busiest.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 3) Polar chart: Circular Monthly Trend
with row2_col1:
    st.markdown("<div class='glass chart-card'>", unsafe_allow_html=True)
    fig_polar = px.line_polar(polar_df, r='Trips', theta='Month', line_close=True)
    st.plotly_chart(fig_polar, use_container_width=True)
    st.markdown("<div class='explain'><b style='color:#40E0D0'>What it shows:Monthly trips in a circular layout.<br><b style='color:#40E0D0'>How to use: Highlights seasonal patterns visually.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 4) Histogram: Trips Distribution
with row2_col2:
    st.markdown("<div class='glass chart-card'>", unsafe_allow_html=True)
    fig_hist = px.histogram(hist_df, x=hist_df, nbins=25)
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown("<div class='explain'><b style='color:#40E0D0'>What it shows: Frequency of trips across days.<br><b style='color:#40E0D0'>How to use: Check typical trip ranges and outliers.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 5) Heatmap: Weekday vs Month Intensity
with row3_col1:
    st.markdown("<div class='glass chart-card'>", unsafe_allow_html=True)
    if pivot.values.sum() == 0:
        st.info("Not enough data for heatmap.")
    else:
        z = pivot.values
        x = [str(m) for m in pivot.columns]
        y = pivot.index.tolist()
        heatmap = ff.create_annotated_heatmap(z=z, x=x, y=y, colorscale='Viridis', showscale=True, annotation_text=np.array(z, dtype=int))
        st.plotly_chart(heatmap, use_container_width=True)
    st.markdown("<div class='explain'><b style='color:#40E0D0'>What it shows: Intensity of trips for each weekday-month.<br><b style='color:#40E0D0'>How to use: Spot peak periods and low-activity zones.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 6) Scatter: Trips vs Active Vehicles
with row3_col2:
    st.markdown("<div class='glass chart-card'>", unsafe_allow_html=True)
    if scatter_df.empty:
        st.info("No scatter data.")
    else:
        fig_scatter = px.scatter(scatter_df, x='active_vehicles', y='trips', trendline="ols")
        st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("<div class='explain'><b style='color:#40E0D0'>What it shows:Correlation between active vehicles and trips.<br><b style='color:#40E0D0'>How to use: Understand supply-demand relationship.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("---")
st.markdown("<small style='color:white;'>Tips: Type into month/date/weekday boxes to see suggestions. Leave empty for full data.</small>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # end main container
