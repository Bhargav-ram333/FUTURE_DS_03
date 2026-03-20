import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(page_title="Funnel Dashboard", layout="wide")

st.title("🎯 Funnel Analysis Dashboard")
st.write("Bank Marketing Campaign Analysis")

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv("bank-full.csv", sep=";")
    df["y"] = df["y"].map({"yes": 1, "no": 0})
    return df

df = load_data()

# ============================================
# SIDEBAR FILTERS (FIXED)
# ============================================
st.sidebar.header("Filters")

job_options = sorted(df["job"].dropna().unique().tolist())
edu_options = sorted(df["education"].dropna().unique().tolist())

jobs = st.sidebar.multiselect(
    "Job",
    options=job_options,
    default=job_options
)

education = st.sidebar.multiselect(
    "Education",
    options=edu_options,
    default=edu_options
)

age_range = st.sidebar.slider(
    "Age Range",
    int(df["age"].min()),
    int(df["age"].max()),
    (int(df["age"].min()), int(df["age"].max()))
)

# ============================================
# FILTER DATA
# ============================================
filtered = df[
    (df["job"].isin(jobs)) &
    (df["education"].isin(education)) &
    (df["age"].between(age_range[0], age_range[1]))
]

if filtered.empty:
    st.warning("No data available")
    st.stop()

# ============================================
# FUNNEL CALCULATIONS (SAFE)
# ============================================
total = len(filtered)
leads = filtered[filtered["duration"] > 0].shape[0]
customers = filtered[filtered["y"] == 1].shape[0]

contact_to_lead = (leads / total) * 100 if total > 0 else 0
lead_to_customer = (customers / leads) * 100 if leads > 0 else 0
overall = (customers / total) * 100 if total > 0 else 0

drop1 = 100 - contact_to_lead
drop2 = 100 - lead_to_customer

# ============================================
# KPI METRICS
# ============================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Contacts", f"{total:,}")
col2.metric("Leads", f"{leads:,}")
col3.metric("Customers", f"{customers:,}")
col4.metric("Conversion Rate", f"{overall:.2f}%")

# ============================================
# FUNNEL CHART
# ============================================
st.subheader("📉 Funnel Analysis")

funnel_fig = go.Figure()
funnel_fig.add_trace(go.Funnel(
    y=["Contacts", "Leads", "Customers"],
    x=[total, leads, customers],
    textinfo="value+percent previous"
))

st.plotly_chart(funnel_fig, use_container_width=True)

# ============================================
# DROP-OFF ANALYSIS
# ============================================
st.subheader("🚨 Drop-off Analysis")

drop_df = pd.DataFrame({
    "Stage": ["Contact → Lead", "Lead → Customer"],
    "Drop-off (%)": [drop1, drop2]
})

fig_drop = px.bar(drop_df, x="Stage", y="Drop-off (%)", text="Drop-off (%)")
st.plotly_chart(fig_drop, use_container_width=True)

# ============================================
# CHANNEL ANALYSIS
# ============================================
st.subheader("📡 Channel Performance")

channel = (
    filtered.groupby("contact")
    .agg(Total=("y", "count"), Customers=("y", "sum"))
    .reset_index()
)

channel["Conversion (%)"] = (channel["Customers"] / channel["Total"]) * 100

fig_channel = px.bar(channel, x="contact", y="Conversion (%)", text="Conversion (%)")
st.plotly_chart(fig_channel, use_container_width=True)

# ============================================
# MONTHLY ANALYSIS
# ============================================
st.subheader("📅 Monthly Conversion")

monthly = (
    filtered.groupby("month")
    .agg(Total=("y", "count"), Customers=("y", "sum"))
    .reset_index()
)

monthly["Conversion (%)"] = (monthly["Customers"] / monthly["Total"]) * 100

fig_month = px.line(monthly, x="month", y="Conversion (%)", markers=True)
st.plotly_chart(fig_month, use_container_width=True)

# ============================================
# INSIGHTS
# ============================================
st.subheader("💡 Insights")

if drop1 > drop2:
    st.warning("Biggest drop-off at Contact → Lead stage")
else:
    st.warning("Biggest drop-off at Lead → Customer stage")

best_channel = channel.sort_values("Conversion (%)", ascending=False).iloc[0]
st.success(f"Best channel: {best_channel['contact']} ({best_channel['Conversion (%)']:.2f}%)")

st.info("Focus on high-performing channels and improve conversion strategy.")
