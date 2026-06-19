"""pages/pipeline.py — Clinical Trial Pipeline Intelligence"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data.datasets import TRIALS, FDA_DRUGS
from utils.helpers import *

STATUS_COLOR = {
    "Recruiting":               "#1e8e3e",
    "Active, not recruiting":   "#1a73e8",
    "Completed":                "#5f6368",
    "Not yet recruiting":       "#f9ab00",
}

IDN_COLOR = {
    "Very High":  "#d93025",
    "High":       "#f9ab00",
    "Moderate":   "#1a73e8",
    "Low":        "#5f6368",
}

def render(cancer_types, year_range):
    st.markdown('<div class="page-title">🔬 Clinical Trial Pipeline Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Phase III oncology pipeline tracking, competitive threat scoring, and commercialization readiness</div>', unsafe_allow_html=True)

    df = TRIALS[TRIALS["cancer_type"].isin(cancer_types)].copy()

    if df.empty:
        st.warning("No trials match the selected cancer types. Adjust filters in the sidebar.")
        return

    # ── Sub-filters ───────────────────────────────────────────────────────
    f1, f2, f3 = st.columns(3)
    with f1:
        phase_opts = ["All"] + sorted(df["phase"].unique().tolist())
        sel_phase = st.selectbox("Phase", phase_opts)
    with f2:
        status_opts = ["All"] + sorted(df["status"].unique().tolist())
        sel_status = st.selectbox("Status", status_opts)
    with f3:
        idn_opts = ["All", "Very High", "High", "Moderate", "Low"]
        sel_idn = st.selectbox("Disruption Potential", idn_opts)

    if sel_phase  != "All": df = df[df["phase"]  == sel_phase]
    if sel_status != "All": df = df[df["status"] == sel_status]
    if sel_idn    != "All": df = df[df["idn_potential"] == sel_idn]

    # ── KPIs ──────────────────────────────────────────────────────────────
    recruiting = df[df["status"] == "Recruiting"]
    completing = df[df["est_completion"] <= 2025]
    high_risk  = df[df["idn_potential"].isin(["Very High", "High"])]
    total_pts  = df["enrollment"].sum()

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Trials in Pipeline", str(len(df))), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Actively Recruiting", str(len(recruiting)), f"{len(recruiting)/len(df)*100:.0f}% of pipeline", True), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("High Disruption Potential", str(len(high_risk)), f"{len(high_risk)/len(df)*100:.0f}% of pipeline", False), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Total Patients Enrolled", f"{total_pts:,.0f}", "Phase III only"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Gantt / Timeline ──────────────────────────────────────────────────
    st.markdown('<div class="section-header">Trial Timeline & Competitive Readout Schedule</div>', unsafe_allow_html=True)

    gantt_df = df.sort_values("est_completion").copy()
    gantt_df["start"] = pd.to_datetime(gantt_df["start_year"].astype(str) + "-01-01")
    gantt_df["end"]   = pd.to_datetime(gantt_df["est_completion"].astype(str) + "-12-31")
    gantt_df["label"] = gantt_df["drug"] + " — " + gantt_df["sponsor"]

    fig = px.timeline(gantt_df, x_start="start", x_end="end", y="label",
                      color="idn_potential",
                      color_discrete_map=IDN_COLOR,
                      hover_data={"nct_id":True,"moa":True,"biomarker":True,"enrollment":True,"combo":True},
                      labels={"idn_potential":"Disruption Potential","label":"Trial"})
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=max(380, len(gantt_df) * 32),
        paper_bgcolor=WHITE, plot_bgcolor=BG,
        font=dict(family="Inter", size=10),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", y=1.05)
    )
    fig.add_vline(x="2025-01-01", line_dash="dash", line_color=NAVY,
                  annotation_text="Today", annotation_position="top")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Red = Very High disruption potential (near-term commercial threat). Hover over bars for trial details.")

    # ── Pipeline by Cancer + MoA ──────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Pipeline Depth by Cancer Type</div>', unsafe_allow_html=True)
        ct_count = df.groupby(["cancer_type","idn_potential"]).size().reset_index(name="count")
        fig2 = px.bar(ct_count, x="cancer_type", y="count", color="idn_potential",
                      color_discrete_map=IDN_COLOR, barmode="stack",
                      labels={"count":"# Trials","cancer_type":"Cancer Type","idn_potential":"Disruption"})
        fig2.update_layout(**plotly_layout("", 340))
        fig2.update_xaxes(tickangle=-25)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Mechanism of Action Distribution</div>', unsafe_allow_html=True)
        moa_count = df["moa"].value_counts().reset_index()
        moa_count.columns = ["moa","count"]
        fig3 = px.bar(moa_count, x="count", y="moa", orientation="h",
                      color="count", color_continuous_scale="Blues",
                      labels={"count":"# Trials","moa":"Mechanism"})
        fig3.update_layout(**plotly_layout("", 340, False))
        fig3.update_coloraxes(showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    # ── Enrollment Bubble ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">Trial Enrollment Scale vs. Completion Timeline</div>', unsafe_allow_html=True)
    fig4 = px.scatter(df, x="est_completion", y="enrollment",
                      size="enrollment", color="cancer_type",
                      color_discrete_map=CANCER_COLORS,
                      hover_name="drug",
                      hover_data={"sponsor":True,"moa":True,"status":True,"idn_potential":True,"biomarker":True},
                      size_max=40,
                      labels={"est_completion":"Estimated Completion Year","enrollment":"Enrollment (n)"})
    fig4.update_layout(**plotly_layout("", 360))
    st.plotly_chart(fig4, use_container_width=True)

    # ── Full Pipeline Table ────────────────────────────────────────────────
    st.markdown('<div class="section-header">Complete Pipeline Registry</div>', unsafe_allow_html=True)
    table = df[["nct_id","drug","sponsor","cancer_type","phase","moa","biomarker","combo",
                "enrollment","start_year","est_completion","status","primary_endpoint","idn_potential"]].copy()
    table.columns = ["NCT ID","Drug","Sponsor","Cancer Type","Phase","MoA","Biomarker","Combo / Arm",
                     "N","Start","Est. End","Status","Primary EP","Disruption"]

    # Color the disruption column via styling
    def color_idn(val):
        colors = {"Very High":"background-color:#fce8e6;color:#c5221f",
                  "High":"background-color:#fff8e1;color:#c07000",
                  "Moderate":"background-color:#e8f0fe;color:#1a73e8",
                  "Low":"background-color:#f1f3f4;color:#5f6368"}
        return colors.get(val, "")

    styled = table.style.applymap(color_idn, subset=["Disruption"])
    st.dataframe(styled, use_container_width=True, height=400, hide_index=True)

    # ── Strategic Alerts ──────────────────────────────────────────────────
    st.markdown("### 🚨 Pipeline Intelligence Alerts")
    very_high = df[df["idn_potential"] == "Very High"]
    for _, row in very_high.iterrows():
        st.markdown(insight(
            f"<b>{row['drug']} ({row['sponsor']})</b> — {row['cancer_type']} | {row['moa']} | "
            f"Biomarker: {row['biomarker']} | Est. readout: <b>{row['est_completion']}</b> | "
            f"Arm: {row['combo']}"
        ), unsafe_allow_html=True)

    completing_soon = df[df["est_completion"] <= 2025]
    if not completing_soon.empty:
        names = ", ".join(completing_soon["drug"].tolist())
        st.markdown(insight(f"<b>Near-term readouts (≤2025):</b> {names} — monitor for FDA submission timelines and potential label overlaps.", "warning"), unsafe_allow_html=True)
