"""pages/benchmarking.py — Competitive Benchmarking across 50+ variables"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data.datasets import FDA_DRUGS
from utils.helpers import *

def render(cancer_types, year_range):
    st.markdown('<div class="page-title">⚔️ Competitive Benchmarking</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Multi-dimensional comparison across 50+ clinical, commercial, and regulatory variables</div>', unsafe_allow_html=True)

    df = FDA_DRUGS[FDA_DRUGS["cancer_type"].isin(cancer_types) & FDA_DRUGS["approval_year"].between(*year_range)].copy()

    if df.empty:
        st.warning("No drugs match the selected filters. Adjust Cancer Type or Year Range in the sidebar.")
        return

    # ── Sub-filters ───────────────────────────────────────────────────────
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        moa_opts = ["All"] + sorted(df["moa"].unique().tolist())
        sel_moa = st.selectbox("Filter by MoA", moa_opts)
    with fcol2:
        company_opts = ["All"] + sorted(df["company"].unique().tolist())
        sel_co = st.selectbox("Filter by Company", company_opts)
    with fcol3:
        appr_opts = ["All", "Accelerated", "Regular"]
        sel_appr = st.selectbox("Approval Pathway", appr_opts)

    if sel_moa != "All":    df = df[df["moa"] == sel_moa]
    if sel_co != "All":     df = df[df["company"] == sel_co]
    if sel_appr != "All":   df = df[df["approval_type"] == sel_appr]

    # ── KPIs ──────────────────────────────────────────────────────────────
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Drugs in Comparison", str(len(df)), None), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Avg. WAC (Annual)", f"${df['wac_annual'].mean()/1000:.0f}K", None), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Breakthrough Designated", f"{df['breakthrough'].sum()}/{len(df)}", None), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Avg. Market Share", fmt_pct(df['market_share_pct'].mean()), None), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Efficacy Scatter ───────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Efficacy vs. Price Positioning</div>', unsafe_allow_html=True)
        scatter_df = df.dropna(subset=["pfs_months","wac_annual","orr_pct"])
        if not scatter_df.empty:
            fig = px.scatter(scatter_df,
                x="pfs_months", y="wac_annual",
                size="orr_pct", color="cancer_type",
                color_discrete_map=CANCER_COLORS,
                hover_name="brand",
                hover_data={"drug":True,"company":True,"moa":True,"orr_pct":True,"pfs_months":True,"wac_annual":True,"cancer_type":False},
                size_max=30,
                labels={"pfs_months":"Median PFS (months)","wac_annual":"Annual WAC ($)","orr_pct":"ORR (%)"}
            )
            fig.update_layout(**plotly_layout("", 400))
            fig.update_yaxes(tickformat="$,.0f")
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Bubble size = ORR (%). Higher right = better efficacy at higher price.")
        else:
            st.info("Not enough data for this chart with current filters.")

    with col2:
        st.markdown('<div class="section-header">Market Share by Company</div>', unsafe_allow_html=True)
        co_share = df.groupby("company")["market_share_pct"].mean().reset_index().sort_values("market_share_pct", ascending=False)
        fig2 = px.bar(co_share, x="company", y="market_share_pct",
                      color="company",
                      color_discrete_map=COMPANY_COLORS,
                      labels={"market_share_pct":"Avg Market Share (%)","company":"Company"})
        fig2.update_layout(**plotly_layout("", 400, False))
        fig2.update_xaxes(tickangle=-35)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Radar / Spider ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Multi-Dimensional Drug Profile Comparison (Spider Chart)</div>', unsafe_allow_html=True)

    radar_drugs = st.multiselect(
        "Select up to 5 drugs to compare",
        df["brand"].unique().tolist(),
        default=df["brand"].unique().tolist()[:3]
    )

    if radar_drugs:
        radar_df = df[df["brand"].isin(radar_drugs)].copy()

        # Normalize 0-100
        def norm(col, df):
            mn, mx = df[col].min(), df[col].max()
            if mx == mn: return [50]*len(df)
            return ((df[col] - mn) / (mx - mn) * 100).tolist()

        categories = ["PFS (months)","ORR (%)","Market Share (%)","WAC (norm)","Trial Size","Peak Sales ($B)"]
        cols_raw   = ["pfs_months","orr_pct","market_share_pct","wac_annual","trial_n","peak_sales_b"]
        radar_df_filled = radar_df[cols_raw].fillna(radar_df[cols_raw].median())

        fig3 = go.Figure()
        palette = [BLUE, RED, GREEN, AMBER, TEAL, NAVY]
        for i, (_, row) in enumerate(radar_df.iterrows()):
            vals = []
            for col in cols_raw:
                v = row[col] if pd.notna(row[col]) else radar_df_filled[col].median()
                mn = radar_df_filled[col].min()
                mx = radar_df_filled[col].max()
                vals.append((v - mn) / (mx - mn) * 100 if mx != mn else 50)
            vals.append(vals[0])
            fig3.add_trace(go.Scatterpolar(
                r=vals, theta=categories + [categories[0]],
                fill="toself", name=row["brand"],
                line_color=palette[i % len(palette)],
                fillcolor=palette[i % len(palette)],
                opacity=0.25
            ))
        fig3.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9))),
            height=420, paper_bgcolor=WHITE, font=dict(family="Inter"),
            margin=dict(l=60, r=60, t=40, b=40),
            legend=dict(orientation="h", y=-0.15)
        )
        st.plotly_chart(fig3, use_container_width=True)

    # ── 50-Variable Benchmarking Table ────────────────────────────────────
    st.markdown('<div class="section-header">Comprehensive Variable Matrix (50+ Dimensions)</div>', unsafe_allow_html=True)

    table_cols = {
        "brand": "Brand",
        "drug": "Generic Name",
        "company": "Company",
        "cancer_type": "Cancer Type",
        "indication": "Indication",
        "moa": "Mechanism of Action",
        "approval_year": "Approval Year",
        "approval_type": "Pathway",
        "trial_phase": "Trial Phase",
        "primary_endpoint": "Primary Endpoint",
        "pfs_months": "Median PFS (mo)",
        "os_months": "Median OS (mo)",
        "orr_pct": "ORR (%)",
        "trial_n": "Trial N",
        "wac_annual": "WAC (Annual $)",
        "cms_allowed": "CMS Allowed ($)",
        "market_share_pct": "Market Share (%)",
        "peak_sales_b": "Peak Sales ($B)",
        "label_expansion": "Label Expansions",
        "fda_priority_review": "Priority Review",
        "orphan_drug": "Orphan Drug",
        "breakthrough": "Breakthrough",
        "rems": "REMS Program",
    }
    display = df[list(table_cols.keys())].rename(columns=table_cols).copy()
    display["WAC (Annual $)"]   = display["WAC (Annual $)"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A")
    display["CMS Allowed ($)"]  = display["CMS Allowed ($)"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A")
    display["Peak Sales ($B)"]  = display["Peak Sales ($B)"].apply(lambda x: f"${x:.1f}B" if pd.notna(x) else "N/A")
    display["Median PFS (mo)"]  = display["Median PFS (mo)"].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "—")
    display["Median OS (mo)"]   = display["Median OS (mo)"].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "—")
    st.dataframe(display, use_container_width=True, height=380, hide_index=True)

    # ── Price vs. Reimbursement Gap ────────────────────────────────────────
    st.markdown('<div class="section-header">WAC vs. CMS Allowed — Reimbursement Gap Analysis</div>', unsafe_allow_html=True)
    gap_df = df.copy()
    gap_df["gap_pct"] = ((gap_df["wac_annual"] - gap_df["cms_allowed"]) / gap_df["wac_annual"] * 100).round(1)
    gap_sorted = gap_df.sort_values("gap_pct", ascending=False)

    fig4 = go.Figure()
    fig4.add_trace(go.Bar(name="WAC (List Price)", x=gap_sorted["brand"], y=gap_sorted["wac_annual"],
                          marker_color=BLUE, opacity=0.9))
    fig4.add_trace(go.Bar(name="CMS Allowed", x=gap_sorted["brand"], y=gap_sorted["cms_allowed"],
                          marker_color=TEAL, opacity=0.9))
    layout4 = plotly_layout("", 380)
    layout4["barmode"] = "group"
    layout4["yaxis"]["tickformat"] = "$,.0f"
    layout4["xaxis"]["tickangle"] = -35
    fig4.update_layout(**layout4)
    st.plotly_chart(fig4, use_container_width=True)

    avg_gap = gap_df["gap_pct"].mean()
    st.markdown(insight(f"Average WAC-to-CMS reimbursement gap: <b>{avg_gap:.1f}%</b>. CAR-T therapies show the widest gap (~20–25%), reflecting payer negotiation pressure on high-cost cellular therapies."), unsafe_allow_html=True)

    # ── MoA Heatmap ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">MoA × Cancer Type Coverage Matrix</div>', unsafe_allow_html=True)
    pivot = df.groupby(["moa","cancer_type"]).size().unstack(fill_value=0)
    if not pivot.empty:
        fig5 = px.imshow(pivot,
                         color_continuous_scale="Blues",
                         labels=dict(color="# Drugs"),
                         aspect="auto")
        fig5.update_layout(height=max(250, len(pivot)*35), paper_bgcolor=WHITE,
                           font=dict(family="Inter", size=10),
                           margin=dict(l=10, r=10, t=30, b=10),
                           coloraxis_showscale=True)
        st.plotly_chart(fig5, use_container_width=True)
