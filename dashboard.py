import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Funnel Analysis Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Page background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Header */
.dashboard-header {
    background: linear-gradient(90deg, rgba(99,102,241,0.25) 0%, rgba(139,92,246,0.15) 100%);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
}
.dashboard-header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #818cf8, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.dashboard-header p {
    color: #94a3b8;
    font-size: 0.97rem;
    margin: 6px 0 0 0;
}

/* KPI Cards */
.kpi-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 20px 22px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(99,102,241,0.25);
}
.kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 2.1rem;
    font-weight: 700;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 6px;
}

/* Section headers */
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #c7d2fe;
    margin: 6px 0 16px 0;
    border-left: 3px solid #818cf8;
    padding-left: 12px;
}

/* Recommendations */
.rec-card {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.rec-card.warning {
    background: rgba(245,158,11,0.08);
    border-color: rgba(245,158,11,0.25);
}
.rec-card.info {
    background: rgba(56,189,248,0.08);
    border-color: rgba(56,189,248,0.25);
}
.rec-title {
    font-weight: 600;
    font-size: 0.92rem;
    margin-bottom: 4px;
}
.rec-desc {
    font-size: 0.82rem;
    color: #94a3b8;
    line-height: 1.5;
}

/* Drop-off badges */
.drop-badge {
    display: inline-block;
    background: rgba(239,68,68,0.2);
    border: 1px solid rgba(239,68,68,0.4);
    color: #fca5a5;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* Plotly chart backgrounds */
.stPlotlyChart {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA LOADING & PROCESSING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), "bank-full.csv")
    df = pd.read_csv(csv_path, sep=";")
    df["y"] = df["y"].map({"yes": 1, "no": 0})
    return df


@st.cache_data
def compute_funnel(df):
    total = len(df)
    leads = df[df["duration"] > 0].shape[0]
    customers = df[df["y"] == 1].shape[0]

    contact_to_lead = (leads / total) * 100
    lead_to_customer = (customers / leads) * 100
    overall = (customers / total) * 100

    drop1 = 100 - contact_to_lead
    drop2 = 100 - lead_to_customer

    return {
        "total": total,
        "leads": leads,
        "customers": customers,
        "contact_to_lead": contact_to_lead,
        "lead_to_customer": lead_to_customer,
        "overall": overall,
        "drop1": drop1,
        "drop2": drop2,
    }


MONTH_ORDER = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")

    all_jobs = sorted(df["job"].unique().tolist())
    sel_jobs = st.multiselect("Job Type", all_jobs, default=all_jobs, key="job_filter")

    all_edu = sorted(df["education"].unique().tolist())
    sel_edu = st.multiselect("Education Level", all_edu, default=all_edu, key="edu_filter")

    age_min, age_max = int(df["age"].min()), int(df["age"].max())
    sel_age = st.slider("Age Range", age_min, age_max, (age_min, age_max))

    st.markdown("---")
    st.markdown("**📌 About**")
    st.markdown(
        "<span style='font-size:0.8rem;color:#64748b;'>Bank Marketing Funnel Analysis<br>Data: bank-full.csv</span>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────
filtered = df[
    (df["job"].isin(sel_jobs)) &
    (df["education"].isin(sel_edu)) &
    (df["age"] >= sel_age[0]) &
    (df["age"] <= sel_age[1])
]

if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your filters.")
    st.stop()

metrics = compute_funnel(filtered)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="dashboard-header">
    <h1>🎯 Funnel Analysis Dashboard</h1>
    <p>Bank Marketing Campaign · Contacts → Leads → Customers · Drop-off Insights & Recommendations</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, label, value, sub, color="#a78bfa"):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{color};">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

kpi(k1, "Total Contacts", f"{metrics['total']:,}", "Campaign reach", "#a78bfa")
kpi(k2, "Leads", f"{metrics['leads']:,}", "Duration > 0s", "#38bdf8")
kpi(k3, "Customers", f"{metrics['customers']:,}", "Subscribed", "#34d399")
kpi(k4, "Contact → Lead", f"{metrics['contact_to_lead']:.1f}%", "Engagement rate", "#fb923c")
kpi(k5, "Overall Conversion", f"{metrics['overall']:.1f}%", "Contact → Customer", "#f472b6")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 1 — FUNNEL + DROP-OFF
# ─────────────────────────────────────────────
col_funnel, col_drop = st.columns([1.2, 1], gap="large")

with col_funnel:
    st.markdown('<p class="section-title">📉 Marketing Funnel</p>', unsafe_allow_html=True)

    stages   = ["Total Contacts", "Leads (Engaged)", "Customers (Converted)"]
    counts   = [metrics["total"], metrics["leads"], metrics["customers"]]
    pcts     = [100.0,
                round(metrics["contact_to_lead"], 1),
                round(metrics["overall"], 1)]
    colors   = ["#818cf8", "#38bdf8", "#34d399"]

    fig_funnel = go.Figure()

    max_val = max(counts)
    bar_height = 0.55
    gap = 0.12

    for i, (stage, count, pct, color) in enumerate(zip(stages, counts, pcts, colors)):
        half_w = (count / max_val) * 0.5
        y_pos = (len(stages) - 1 - i) * (bar_height + gap)

        # Trapezoid connector
        if i < len(stages) - 1:
            next_half = (counts[i + 1] / max_val) * 0.5
            next_y = y_pos - bar_height - gap
            fig_funnel.add_shape(
                type="path",
                path=f"M {0.5-half_w} {y_pos} L {0.5+half_w} {y_pos} "
                     f"L {0.5+next_half} {next_y+bar_height} L {0.5-next_half} {next_y+bar_height} Z",
                fillcolor="rgba(255,255,255,0.04)",
                line_color="rgba(255,255,255,0.05)",
                layer="below",
            )

        fig_funnel.add_shape(
            type="rect",
            x0=0.5 - half_w, x1=0.5 + half_w,
            y0=y_pos, y1=y_pos + bar_height,
            fillcolor=color,
            opacity=0.85,
            line_color="white",
            line_width=0.5,
        )
        fig_funnel.add_annotation(
            x=0.5, y=y_pos + bar_height / 2,
            text=f"<b>{stage}</b>  |  {count:,}  ({pct}%)",
            showarrow=False,
            font=dict(color="white", size=13),
            xref="paper", yref="y",
        )

    n = len(stages)
    total_h = n * (bar_height + gap) - gap
    fig_funnel.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[-0.05, total_h + 0.05]),
        showlegend=False,
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

with col_drop:
    st.markdown('<p class="section-title">🚨 Drop-off at Each Stage</p>', unsafe_allow_html=True)

    drop_stages = ["Contact → Lead", "Lead → Customer"]
    drop_vals   = [round(metrics["drop1"], 1), round(metrics["drop2"], 1)]
    drop_colors = ["#f59e0b", "#ef4444"]
    conv_vals   = [round(metrics["contact_to_lead"], 1), round(metrics["lead_to_customer"], 1)]

    fig_drop = go.Figure()

    fig_drop.add_trace(go.Bar(
        x=drop_stages,
        y=drop_vals,
        name="Drop-off %",
        marker_color=drop_colors,
        text=[f"{v}% lost" for v in drop_vals],
        textposition="outside",
        textfont=dict(color="white", size=13),
        width=0.4,
    ))
    fig_drop.add_trace(go.Bar(
        x=drop_stages,
        y=conv_vals,
        name="Conversion %",
        marker_color=["rgba(52,211,153,0.6)", "rgba(56,189,248,0.6)"],
        text=[f"{v}% converted" for v in conv_vals],
        textposition="outside",
        textfont=dict(color="white", size=13),
        width=0.4,
    ))
    fig_drop.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=10, r=10, t=10, b=30),
        font=dict(color="#e2e8f0"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.07)",
            zeroline=False,
            title="Percentage (%)",
        ),
        xaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_drop, use_container_width=True)

    # Drop-off summary pills
    biggest_drop = "Contact → Lead" if metrics["drop1"] > metrics["drop2"] else "Lead → Customer"
    st.markdown(
        f"⚠️ **Biggest drop-off:** <span class='drop-badge'>{biggest_drop} — "
        f"{max(metrics['drop1'], metrics['drop2']):.1f}% lost</span>",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 2 — CHANNEL + MONTHLY TREND
# ─────────────────────────────────────────────
col_ch, col_mo = st.columns(2, gap="large")

with col_ch:
    st.markdown('<p class="section-title">📡 Conversion by Contact Channel</p>', unsafe_allow_html=True)

    channel = (
        filtered.groupby("contact")
        .agg(Total=("y", "count"), Customers=("y", "sum"))
        .reset_index()
    )
    channel["Conversion (%)"] = (channel["Customers"] / channel["Total"] * 100).round(2)
    channel["Drop-off (%)"] = (100 - channel["Conversion (%)"]).round(2)
    channel = channel.sort_values("Conversion (%)", ascending=True)

    fig_ch = go.Figure()
    fig_ch.add_trace(go.Bar(
        y=channel["contact"],
        x=channel["Conversion (%)"],
        orientation="h",
        marker=dict(
            color=channel["Conversion (%)"],
            colorscale=[[0,"#4338ca"],[0.5,"#818cf8"],[1,"#34d399"]],
            showscale=False,
        ),
        text=[f"{v:.1f}%" for v in channel["Conversion (%)"]],
        textposition="outside",
        textfont=dict(color="white"),
    ))
    fig_ch.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=10, r=50, t=10, b=10),
        font=dict(color="#e2e8f0"),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.07)",
            title="Conversion Rate (%)",
        ),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig_ch, use_container_width=True)

    # Best channel callout
    best_ch = channel.iloc[-1]
    st.info(f"📌 **Best channel:** {best_ch['contact'].title()} with **{best_ch['Conversion (%)']:.1f}%** conversion ({best_ch['Customers']:,} customers from {best_ch['Total']:,} contacts)")

with col_mo:
    st.markdown('<p class="section-title">📅 Monthly Conversion Trend</p>', unsafe_allow_html=True)

    monthly = (
        filtered.groupby("month")
        .agg(Total=("y","count"), Customers=("y","sum"))
        .reset_index()
    )
    monthly["Conversion (%)"] = (monthly["Customers"] / monthly["Total"] * 100).round(2)
    monthly["month_num"] = monthly["month"].apply(
        lambda m: MONTH_ORDER.index(m.lower()) if m.lower() in MONTH_ORDER else 99
    )
    monthly = monthly.sort_values("month_num")

    fig_mo = go.Figure()
    fig_mo.add_trace(go.Scatter(
        x=monthly["month"].str.capitalize(),
        y=monthly["Conversion (%)"],
        mode="lines+markers+text",
        line=dict(color="#818cf8", width=2.5),
        marker=dict(
            size=10,
            color=monthly["Conversion (%)"],
            colorscale=[[0,"#f59e0b"],[0.5,"#818cf8"],[1,"#34d399"]],
            showscale=False,
            line=dict(width=1.5, color="white"),
        ),
        text=[f"{v:.1f}%" for v in monthly["Conversion (%)"]],
        textposition="top center",
        textfont=dict(size=11, color="white"),
        fill="tozeroy",
        fillcolor="rgba(129,140,248,0.12)",
    ))
    best_month = monthly.loc[monthly["Conversion (%)"].idxmax()]
    fig_mo.add_annotation(
        x=best_month["month"].capitalize(),
        y=best_month["Conversion (%)"],
        text=f"🏆 Peak: {best_month['Conversion (%)']:.1f}%",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#34d399",
        font=dict(color="#34d399", size=11),
        bgcolor="rgba(0,0,0,0.4)",
        bordercolor="#34d399",
    )
    fig_mo.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(color="#e2e8f0"),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.07)",
            title="Conversion Rate (%)",
            zeroline=False,
        ),
    )
    st.plotly_chart(fig_mo, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 3 — AGE / JOB / EDUCATION BREAKDOWN
# ─────────────────────────────────────────────
col_job, col_age = st.columns(2, gap="large")

with col_job:
    st.markdown('<p class="section-title">💼 Conversion by Job Type</p>', unsafe_allow_html=True)

    job_conv = (
        filtered.groupby("job")
        .agg(Total=("y","count"), Customers=("y","sum"))
        .reset_index()
    )
    job_conv["Conversion (%)"] = (job_conv["Customers"] / job_conv["Total"] * 100).round(2)
    job_conv = job_conv.sort_values("Conversion (%)", ascending=True)

    fig_job = px.bar(
        job_conv,
        x="Conversion (%)",
        y="job",
        orientation="h",
        color="Conversion (%)",
        color_continuous_scale=["#4338ca", "#818cf8", "#34d399"],
        text="Conversion (%)",
    )
    fig_job.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textfont_color="white")
    fig_job.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        margin=dict(l=10, r=50, t=10, b=10),
        font=dict(color="#e2e8f0"),
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.07)", title="Conversion Rate (%)"),
        yaxis=dict(showgrid=False, title=""),
    )
    st.plotly_chart(fig_job, use_container_width=True)

with col_age:
    st.markdown('<p class="section-title">👤 Conversion by Age Group</p>', unsafe_allow_html=True)

    filtered_copy = filtered.copy()
    bins   = [17, 25, 35, 45, 55, 65, 100]
    labels = ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
    filtered_copy["age_group"] = pd.cut(filtered_copy["age"], bins=bins, labels=labels)

    age_conv = (
        filtered_copy.groupby("age_group", observed=True)
        .agg(Total=("y","count"), Customers=("y","sum"))
        .reset_index()
    )
    age_conv["Conversion (%)"] = (age_conv["Customers"] / age_conv["Total"] * 100).round(2)

    fig_age = go.Figure()
    fig_age.add_trace(go.Bar(
        x=age_conv["age_group"].astype(str),
        y=age_conv["Total"],
        name="Total",
        marker_color="rgba(99,102,241,0.35)",
        yaxis="y2",
    ))
    fig_age.add_trace(go.Scatter(
        x=age_conv["age_group"].astype(str),
        y=age_conv["Conversion (%)"],
        name="Conversion %",
        mode="lines+markers",
        line=dict(color="#34d399", width=2.5),
        marker=dict(size=9, color="#34d399", line=dict(width=1.5, color="white")),
        text=[f"{v:.1f}%" for v in age_conv["Conversion (%)"]],
        textposition="top center",
        textfont=dict(color="white", size=11),
        yaxis="y",
    ))
    fig_age.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(color="#e2e8f0"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            title="Conversion Rate (%)",
            gridcolor="rgba(255,255,255,0.07)",
            zeroline=False,
        ),
        yaxis2=dict(
            title="Total Contacts",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        barmode="overlay",
    )
    st.plotly_chart(fig_age, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROW 4 — ACTIONABLE RECOMMENDATIONS
# ─────────────────────────────────────────────
st.markdown('<p class="section-title">💡 Key Drop-off Insights & Actionable Recommendations</p>', unsafe_allow_html=True)

# Build dynamic insights from data
best_channel_name = channel.iloc[-1]["contact"].title()
best_channel_conv = channel.iloc[-1]["Conversion (%)"]
worst_channel_name = channel.iloc[0]["contact"].title()
worst_channel_conv = channel.iloc[0]["Conversion (%)"]

best_month_name = best_month["month"].capitalize()
best_month_conv = best_month["Conversion (%)"]

best_job = job_conv.iloc[-1]
worst_job = job_conv.iloc[0]

biggest_drop_stage = "Contact → Lead" if metrics["drop1"] > metrics["drop2"] else "Lead → Customer"
biggest_drop_val   = max(metrics["drop1"], metrics["drop2"])

recommendations = [
    {
        "type": "success",
        "icon": "📡",
        "title": f"Double down on {best_channel_name} contact channel",
        "desc": (
            f"The {best_channel_name} channel drives a {best_channel_conv:.1f}% conversion rate, "
            f"significantly outperforming {worst_channel_name} ({worst_channel_conv:.1f}%). "
            f"Reallocate budget and outreach effort toward this high-performing channel."
        ),
    },
    {
        "type": "warning",
        "icon": "🚨",
        "title": f"Address the {biggest_drop_stage} drop-off urgently",
        "desc": (
            f"{biggest_drop_val:.1f}% of prospects are lost at the **{biggest_drop_stage}** stage. "
            + (
                "Focus on improving initial targeting and call quality to convert more contacts into engaged leads."
                if biggest_drop_stage == "Contact → Lead"
                else "Improve the sales pitch, follow-up cadence, and offer personalization to close more leads."
            )
        ),
    },
    {
        "type": "info",
        "icon": "📅",
        "title": f"Concentrate campaigns in peak months (around {best_month_name})",
        "desc": (
            f"Conversion peaks at {best_channel_conv:.1f}% during {best_month_name}. "
            f"Plan high-intensity outreach and promotions ahead of historically strong months. "
            f"Reduce spend in consistently low-conversion months."
        ),
    },
    {
        "type": "success",
        "icon": "💼",
        "title": f"Target high-converting job segments: {best_job['job'].title()}",
        "desc": (
            f"Customers in the '{best_job['job'].title()}' category convert at {best_job['Conversion (%)']:.1f}%, "
            f"versus only {worst_job['Conversion (%)']:.1f}% for '{worst_job['job'].title()}'. "
            f"Personalize messaging and product packaging for top-performing segments."
        ),
    },
    {
        "type": "info",
        "icon": "🔁",
        "title": "Re-engage previously contacted prospects",
        "desc": (
            f"With an overall conversion of only {metrics['overall']:.1f}%, "
            f"there is a large pool of non-converting contacts. Implement follow-up sequences, "
            f"retargeting, and tiered offers to recover previously lost opportunities."
        ),
    },
]

type_colors = {"success": "", "warning": "warning", "info": "info"}

r1, r2 = st.columns(2, gap="large")
for i, rec in enumerate(recommendations):
    col = r1 if i % 2 == 0 else r2
    css_cls = f"rec-card {type_colors[rec['type']]}"
    col.markdown(
        f"""
        <div class="{css_cls}">
            <div class="rec-title">{rec['icon']} {rec['title']}</div>
            <div class="rec-desc">{rec['desc']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#475569; font-size:0.78rem; border-top:1px solid rgba(255,255,255,0.07); padding-top:20px;">
    Funnel Analysis Dashboard · Bank Marketing Campaign · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
