"""pages/forecasting.py — Launch Forecasting & Revenue Projections"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data.datasets import FDA_DRUGS, SEER_DATA, MARKET_OPPORTUNITY, get_forecast_data
from utils.helpers import *

def render(cancer_types, year_range):
    st.markdown('<div class="page-title">📈 Launch Forecasting & Revenue Projections</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Revenue ramp modeling, patent lifecycle analysis, and launch scenario planning through 2029</div>', unsafe_allow_html=True)

    df_drugs = FDA_DRUGS[FDA_DRUGS["cancer_type"].isin(cancer_types)].copy()
    df_fc    = get_forecast_data(cancer_types)

    # ── Scenario Controls ─────────────────────────────────────────────────
    with st.expander("⚙️ Forecast Scenario Controls", expanded=True):
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            market_growth = st.slider("Market Growth Adj. (%)", -20, +40, 0, 5)
        with sc2:
            price_erosion = st.slider("Price Erosion on LOE (%)", 0, 60, 20, 5)
        with sc3:
            adoption_speed = st.selectbox("Adoption Speed", ["Slow (18 mo peak)", "Base (12 mo peak)", "Fast (6 mo peak)"], index=1)
        with sc4:
            scenario_name = st.selectbox("Scenario", ["Base Case", "Bull Case (+15%)", "Bear Case (-15%)"])

    scenario_mult = {"Base Case": 1.0, "Bull Case (+15%)": 1.15, "Bear Case (-15%)": 0.85}[scenario_name]
    growth_adj    = 1 + market_growth / 100

    df_fc = df_fc.copy()
    df_fc["revenue_adj"] = df_fc["revenue_b"] * scenario_mult * growth_adj

    # ── KPI Row ───────────────────────────────────────────────────────────
    hist  = df_fc[~df_fc["is_forecast"] & (df_fc["year"] == 2024)]
    fcast = df_fc[df_fc["is_forecast"] & (df_fc["year"] == 2029)]
    total_2024  = hist["revenue_adj"].sum()
    total_2029  = fcast["revenue_adj"].sum()
    cagr_calc   = ((total_2029 / total_2024) ** (1/5) - 1) * 100 if total_2024 > 0 else 0
    peak_drug   = df_drugs.sort_values("peak_sales_b", ascending=False).iloc[0]

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Projected 2024 Revenue", f"${total_2024:.1f}B", f"{scenario_name}", True), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Projected 2029 Revenue", f"${total_2029:.1f}B", f"CAGR {cagr_calc:.1f}%", True), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Highest Peak Sales Drug", peak_drug["brand"], f"${peak_drug['peak_sales_b']:.1f}B", True), unsafe_allow_html=True)
    with c4:
        loe_count = len(df_drugs[(df_drugs["approval_year"] <= 2017)])
        st.markdown(kpi_card("Drugs Near Patent Cliff", str(loe_count), "Approved ≤2017", False), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Portfolio Revenue Trend ───────────────────────────────────────────
    col1, col2 = st.columns([1.4, 0.6])

    with col1:
        st.markdown('<div class="section-header">Portfolio Revenue Trajectory — Historical vs. Forecast</div>', unsafe_allow_html=True)

        # Pick top drugs by peak sales
        top_brands = df_drugs.sort_values("peak_sales_b", ascending=False).head(8)["brand"].tolist()
        fc_top = df_fc[df_fc["brand"].isin(top_brands)].copy()

        fig = go.Figure()
        palette = [BLUE, RED, GREEN, AMBER, TEAL, "#9c27b0", "#f4511e", "#00897b"]
        for i, brand in enumerate(top_brands):
            sub = fc_top[fc_top["brand"] == brand].sort_values("year")
            hist_sub = sub[~sub["is_forecast"]]
            fore_sub = sub[sub["is_forecast"]]
            color = palette[i % len(palette)]
            if not hist_sub.empty:
                fig.add_trace(go.Scatter(x=hist_sub["year"], y=hist_sub["revenue_adj"],
                    name=brand, mode="lines+markers", line=dict(color=color, width=2),
                    marker=dict(size=4)))
            if not fore_sub.empty:
                bridge = pd.concat([hist_sub.tail(1), fore_sub])
                fig.add_trace(go.Scatter(x=bridge["year"], y=bridge["revenue_adj"],
                    name=f"{brand} (F)", mode="lines",
                    line=dict(color=color, dash="dot", width=1.5),
                    showlegend=False))

        # Shade forecast region
        fig.add_vrect(x0=2024.5, x1=2029.5, fillcolor="rgba(26,115,232,0.04)",
                      line_width=0, annotation_text="Forecast →", annotation_position="top left")
        fig.add_vline(x=2024.5, line_dash="dash", line_color=GREY, line_width=1)
        fig.update_layout(**plotly_layout("", 440))
        fig.update_yaxes(tickprefix="$", ticksuffix="B")
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Solid lines = historical actuals. Dotted = model forecast. Shaded = projection zone.")

    with col2:
        st.markdown('<div class="section-header">2029 Revenue by Cancer Segment</div>', unsafe_allow_html=True)
        seg_2029 = df_fc[df_fc["year"] == 2029].groupby("cancer_type")["revenue_adj"].sum().reset_index()
        fig2 = px.pie(seg_2029, names="cancer_type", values="revenue_adj",
                      color="cancer_type", color_discrete_map=CANCER_COLORS,
                      hole=0.45)
        fig2.update_traces(textposition="inside", textinfo="label+percent",
                           hovertemplate="<b>%{label}</b><br>$%{value:.1f}B<extra></extra>")
        fig2.update_layout(height=440, paper_bgcolor=WHITE,
                           font=dict(family="Inter", size=10),
                           margin=dict(l=0, r=0, t=30, b=0),
                           showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Launch Timing Analysis ─────────────────────────────────────────────
    st.markdown('<div class="section-header">Launch Timing & Year-1 Revenue Ramp Analysis</div>', unsafe_allow_html=True)

    ramp_data = []
    for _, drug in df_drugs.sort_values("peak_sales_b", ascending=False).head(10).iterrows():
        sub = df_fc[df_fc["brand"] == drug["brand"]].sort_values("year")
        for offset in [0, 1, 2, 3]:
            row = sub[sub["year"] == drug["approval_year"] + offset]
            if not row.empty:
                ramp_data.append({
                    "brand": drug["brand"],
                    "cancer_type": drug["cancer_type"],
                    "year_post_launch": f"Year {offset+1}",
                    "revenue_b": row["revenue_adj"].values[0],
                    "pct_of_peak": row["revenue_adj"].values[0] / drug["peak_sales_b"] * 100
                })

    ramp_df = pd.DataFrame(ramp_data)
    if not ramp_df.empty:
        fig3 = px.bar(ramp_df, x="brand", y="pct_of_peak", color="year_post_launch",
                      barmode="group",
                      labels={"pct_of_peak":"% of Peak Sales","brand":"Drug"},
                      color_discrete_sequence=[LIGHT_BLUE, BLUE, NAVY, "#4a148c"])
        fig3.update_layout(**plotly_layout("", 360))
        fig3.update_xaxes(tickangle=-35)
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Breakthrough-designated therapies (e.g., Tagrisso, Yescarta) show steeper Year-1 ramps due to early access programs.")

    # ── Patent Cliff Waterfall ────────────────────────────────────────────
    st.markdown('<div class="section-header">Patent Expiry Risk — Revenue at Risk 2025–2029</div>', unsafe_allow_html=True)

    loe_df = df_drugs.copy()
    loe_df["loe_year"] = loe_df["approval_year"] + np.random.randint(10, 14, len(loe_df))
    loe_df["revenue_at_risk_b"] = loe_df["peak_sales_b"] * (1 - price_erosion / 100)
    loe_risk = loe_df[loe_df["loe_year"].between(2025, 2029)].sort_values("loe_year")

    if not loe_risk.empty:
        fig4 = go.Figure(go.Waterfall(
            name="Revenue Impact",
            orientation="v",
            measure=["relative"] * len(loe_risk),
            x=[f"{r['brand']} ({r['loe_year']})" for _, r in loe_risk.iterrows()],
            y=[-r["revenue_at_risk_b"] for _, r in loe_risk.iterrows()],
            connector={"line": {"color": GREY}},
            decreasing={"marker": {"color": RED}},
        ))
        fig4.update_layout(**plotly_layout("", 360, False))
        fig4.update_yaxes(tickprefix="$", ticksuffix="B")
        fig4.update_xaxes(tickangle=-30)
        st.plotly_chart(fig4, use_container_width=True)

    total_risk = loe_risk["revenue_at_risk_b"].sum() if not loe_risk.empty else 0
    st.markdown(insight(f"<b>${total_risk:.1f}B</b> in portfolio revenue is exposed to LOE/biosimilar entry by 2029 under {price_erosion}% price erosion assumption. CDK4/6 and BTK inhibitors face the earliest biosimilar competition.", "warning"), unsafe_allow_html=True)
    st.markdown(insight(f"<b>Scenario: {scenario_name}</b> — 2029 projected oncology portfolio revenue of <b>${total_2029:.1f}B</b> with implied {cagr_calc:.1f}% CAGR from 2024. IO expansion (PD-1/PD-L1) and ADC platforms drive the upside.", "success"), unsafe_allow_html=True)
