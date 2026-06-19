"""pages/overview.py — Market Overview & Opportunity Sizing"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.datasets import FDA_DRUGS, SEER_DATA, MARKET_OPPORTUNITY, CMS_DATA
from utils.helpers import *

def render(cancer_types, year_range):
    st.markdown('<div class="page-title">🏠 Market Overview & Opportunity Sizing</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Total addressable market, incidence trends, and drug approval landscape across oncology segments</div>', unsafe_allow_html=True)

    df   = FDA_DRUGS[FDA_DRUGS["cancer_type"].isin(cancer_types) & FDA_DRUGS["approval_year"].between(*year_range)]
    seer = SEER_DATA[SEER_DATA["cancer_type"].isin(cancer_types)]
    mkt  = MARKET_OPPORTUNITY[MARKET_OPPORTUNITY["cancer_type"].isin(cancer_types)]
    cms  = CMS_DATA[CMS_DATA["cancer_type"].isin(cancer_types)]

    total_tam   = mkt["tam_b"].sum()
    total_cases = seer["new_cases_2024"].sum()
    total_drugs = len(df)
    avg_wac     = df["wac_annual"].mean()

    # ── KPI Row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Total Addressable Market (TAM)", f"${total_tam:.0f}B", "8.7% CAGR avg", True), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("New Cases (2024 Est.)", f"{total_cases/1e6:.2f}M", "+1.2% YoY", False), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Approved Drugs in Scope", str(total_drugs), f"{year_range[0]}–{year_range[1]}", True), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Avg. Annual WAC", f"${avg_wac/1000:.0f}K", "+5.3% vs prior yr", False), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: TAM Bubble + Approvals by Year ─────────────────────────────
    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.markdown('<div class="section-header">Market Opportunity by Segment (TAM / SAM / SOM)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for _, row in mkt.iterrows():
            color = CANCER_COLORS.get(row["cancer_type"], BLUE)
            fig.add_trace(go.Bar(name=row["cancer_type"], x=[row["cancer_type"]],
                y=[row["tam_b"]], marker_color=color, opacity=0.9,
                customdata=[[row["sam_b"], row["som_b"], row["cagr_pct"], row["key_driver"]]],
                hovertemplate="<b>%{x}</b><br>TAM: $%{y:.1f}B<br>SAM: $%{customdata[0][0]:.1f}B<br>SOM: $%{customdata[0][1]:.1f}B<br>CAGR: %{customdata[0][2]:.1f}%<br>Driver: %{customdata[0][3]}<extra></extra>"))
        for _, row in mkt.iterrows():
            color = CANCER_COLORS.get(row["cancer_type"], BLUE)
            fig.add_trace(go.Bar(showlegend=False, x=[row["cancer_type"]], y=[row["sam_b"]],
                marker_color=color, opacity=0.6))
        for _, row in mkt.iterrows():
            color = CANCER_COLORS.get(row["cancer_type"], BLUE)
            fig.add_trace(go.Bar(showlegend=False, x=[row["cancer_type"]], y=[row["som_b"]],
                marker_color=color, opacity=0.4))
        layout = plotly_layout("", 400, False)
        layout["barmode"] = "overlay"
        layout["yaxis"]["title"] = "Market Size ($B)"
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Bars represent TAM (full) › SAM (darker overlay) › SOM (lightest). Hover for detail.")

    with col2:
        st.markdown('<div class="section-header">FDA Approvals by Year & Type</div>', unsafe_allow_html=True)
        by_yr = df.groupby(["approval_year","approval_type"]).size().reset_index(name="count")
        colors_map = {"Regular":"#1a73e8","Accelerated":"#f9ab00","Breakthrough":"#1e8e3e"}
        fig2 = px.bar(by_yr, x="approval_year", y="count", color="approval_type",
                      color_discrete_map=colors_map, barmode="stack",
                      labels={"count":"# Approvals","approval_year":"Year","approval_type":"Pathway"})
        fig2.update_layout(**plotly_layout("", 400))
        st.plotly_chart(fig2, use_container_width=True)

    # ── Row 2: Incidence Table + CAGR Ranking ─────────────────────────────
    col3, col4 = st.columns([1.3, 0.7])

    with col3:
        st.markdown('<div class="section-header">Cancer Incidence & Survival Landscape (NCI SEER)</div>', unsafe_allow_html=True)
        display = seer[["cancer_type","new_cases_2024","deaths_2024","5yr_survival_pct","biomarker_eligible_pct","us_prevalence"]].copy()
        display.columns = ["Cancer Type","New Cases '24","Deaths '24","5-Yr Survival %","Biomarker Eligible %","US Prevalence"]
        display["New Cases '24"]  = display["New Cases '24"].apply(lambda x: f"{x:,.0f}")
        display["Deaths '24"]     = display["Deaths '24"].apply(lambda x: f"{x:,.0f}")
        display["US Prevalence"]  = display["US Prevalence"].apply(lambda x: f"{x:,.0f}")
        st.dataframe(display, use_container_width=True, height=300, hide_index=True)

    with col4:
        st.markdown('<div class="section-header">Market CAGR Ranking</div>', unsafe_allow_html=True)
        mkt_sorted = mkt.sort_values("cagr_pct", ascending=True)
        fig3 = go.Figure(go.Bar(
            x=mkt_sorted["cagr_pct"], y=mkt_sorted["cancer_type"],
            orientation="h",
            marker_color=[CANCER_COLORS.get(c, BLUE) for c in mkt_sorted["cancer_type"]],
            text=[f"{v:.1f}%" for v in mkt_sorted["cagr_pct"]],
            textposition="outside"
        ))
        layout3 = plotly_layout("", 300, False)
        layout3["xaxis"]["title"] = "CAGR (%)"
        layout3["margin"]["r"] = 40
        fig3.update_layout(**layout3)
        st.plotly_chart(fig3, use_container_width=True)

    # ── CMS Spend Trend ───────────────────────────────────────────────────
    st.markdown('<div class="section-header">CMS Medicare Spend Trend by Cancer Segment (2020–2023)</div>', unsafe_allow_html=True)
    cms_agg = cms.groupby(["year","cancer_type"])["total_spend_m"].sum().reset_index()
    fig4 = px.area(cms_agg, x="year", y="total_spend_m", color="cancer_type",
                   color_discrete_map=CANCER_COLORS,
                   labels={"total_spend_m":"Total Spend ($M)","year":"Year"})
    fig4.update_layout(**plotly_layout("", 320))
    st.plotly_chart(fig4, use_container_width=True)

    # ── Insights ──────────────────────────────────────────────────────────
    top_cagr = mkt.sort_values("cagr_pct", ascending=False).iloc[0]
    largest  = mkt.sort_values("tam_b", ascending=False).iloc[0]
    st.markdown(insight(f"<b>Fastest growing segment:</b> {top_cagr['cancer_type']} at {top_cagr['cagr_pct']}% CAGR — driven by {top_cagr['key_driver']}."), unsafe_allow_html=True)
    st.markdown(insight(f"<b>Largest TAM:</b> {largest['cancer_type']} at ${largest['tam_b']:.1f}B — with an SOM of ${largest['som_b']:.1f}B accessible through targeted launch strategies.", "success"), unsafe_allow_html=True)
    unmet = seer[seer["5yr_survival_pct"] < 30]
    if not unmet.empty:
        types = ", ".join(unmet["cancer_type"].tolist())
        st.markdown(insight(f"<b>High unmet need (5-yr survival <30%):</b> {types} — regulatory pathways and pricing power remain strong.", "warning"), unsafe_allow_html=True)
