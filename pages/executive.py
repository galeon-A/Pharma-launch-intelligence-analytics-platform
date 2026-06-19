"""pages/executive.py — Executive Summary & Strategic Recommendations"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.datasets import FDA_DRUGS, SEER_DATA, MARKET_OPPORTUNITY, TRIALS, get_forecast_data
from utils.helpers import *

def render(cancer_types, year_range):
    st.markdown('<div class="page-title">📋 Executive Summary & Strategic Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Consulting-style integrated assessment — market positioning, competitive risk, and launch strategy framework</div>', unsafe_allow_html=True)

    df_drugs = FDA_DRUGS[FDA_DRUGS["cancer_type"].isin(cancer_types)].copy()
    df_seer  = SEER_DATA[SEER_DATA["cancer_type"].isin(cancer_types)].copy()
    df_mkt   = MARKET_OPPORTUNITY[MARKET_OPPORTUNITY["cancer_type"].isin(cancer_types)].copy()
    df_trial = TRIALS[TRIALS["cancer_type"].isin(cancer_types)].copy()
    df_fc    = get_forecast_data(cancer_types)

    total_tam  = df_mkt["tam_b"].sum()
    total_som  = df_mkt["som_b"].sum()
    total_cases= df_seer["new_cases_2024"].sum()
    high_disr  = df_trial[df_trial["idn_potential"].isin(["Very High","High"])]
    avg_cagr   = df_mkt["cagr_pct"].mean()
    rev_2029   = df_fc[df_fc["year"]==2029]["revenue_b"].sum()

    # ── Executive KPI Dashboard ───────────────────────────────────────────
    st.markdown("### 📊 Integrated Market Scorecard")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(kpi_card("Total Addressable Market", f"${total_tam:.0f}B", f"{avg_cagr:.1f}% CAGR", True), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Serviceable Opp. (SOM)", f"${total_som:.1f}B", "Addressable now", True), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Annual Incident Patients", f"{total_cases/1e6:.2f}M", "2024 Estimate", None), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("High-Threat Pipeline Trials", str(len(high_disr)), "Very High + High", False), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card("2029 Portfolio Revenue", f"${rev_2029:.0f}B", "Base scenario", True), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Opportunity-Risk Matrix ────────────────────────────────────────────
    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.markdown('<div class="section-header">Strategic Opportunity–Risk Matrix</div>', unsafe_allow_html=True)
        threat_by_ct = df_trial.groupby("cancer_type")["idn_potential"].apply(
            lambda x: (x.isin(["Very High","High"])).sum() / len(x) * 100
        ).reset_index()
        threat_by_ct.columns = ["cancer_type","threat_pct"]
        matrix_df = df_mkt.merge(threat_by_ct, on="cancer_type", how="left").fillna({"threat_pct": 20})
        matrix_df["cases"] = matrix_df["cancer_type"].map(
            df_seer.set_index("cancer_type")["new_cases_2024"].to_dict()
        )

        fig = px.scatter(matrix_df,
            x="threat_pct", y="tam_b",
            size="som_b", color="cancer_type",
            color_discrete_map=CANCER_COLORS,
            text="cancer_type",
            size_max=45,
            labels={"threat_pct":"Competitive Threat Score (%)","tam_b":"TAM ($B)","som_b":"SOM ($B)"},
            hover_data={"cagr_pct":True,"som_b":True,"key_driver":True}
        )
        fig.update_traces(textposition="top center", textfont_size=9)
        # Quadrant shading
        fig.add_shape(type="rect", x0=0, x1=50, y0=df_mkt["tam_b"].mean(), y1=df_mkt["tam_b"].max()*1.1,
                      fillcolor="rgba(30,142,62,0.06)", line_width=0)  # High mkt, low threat
        fig.add_shape(type="rect", x0=50, x1=105, y0=df_mkt["tam_b"].mean(), y1=df_mkt["tam_b"].max()*1.1,
                      fillcolor="rgba(217,48,37,0.05)", line_width=0)  # High mkt, high threat
        fig.add_annotation(x=20, y=df_mkt["tam_b"].max()*1.05, text="★ Priority Segments", showarrow=False,
                           font=dict(color=GREEN, size=10, family="Inter"))
        fig.add_annotation(x=75, y=df_mkt["tam_b"].max()*1.05, text="⚠ High Stakes / Defend", showarrow=False,
                           font=dict(color=RED, size=10, family="Inter"))
        layout = plotly_layout("", 440)
        layout["showlegend"] = False
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Bubble size = Serviceable Obtainable Market. X-axis = % of pipeline trials with High/Very High disruption potential.")

    with col2:
        st.markdown('<div class="section-header">CAGR vs. Unmet Need Heatmap</div>', unsafe_allow_html=True)
        heat_df = df_mkt.copy()
        heat_df["survival"] = heat_df["cancer_type"].map(
            df_seer.set_index("cancer_type")["5yr_survival_pct"].to_dict()
        )
        heat_df["unmet_score"] = 100 - heat_df["survival"].fillna(50)
        heat_df = heat_df.sort_values("cagr_pct", ascending=False)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="Market CAGR", x=heat_df["cancer_type"], y=heat_df["cagr_pct"],
            marker_color=[CANCER_COLORS.get(c, BLUE) for c in heat_df["cancer_type"]],
            yaxis="y", opacity=0.85,
            hovertemplate="<b>%{x}</b><br>CAGR: %{y:.1f}%<extra></extra>"
        ))
        fig2.add_trace(go.Scatter(
            name="Unmet Need Score", x=heat_df["cancer_type"], y=heat_df["unmet_score"],
            mode="lines+markers", yaxis="y2", line=dict(color=RED, dash="dash", width=2),
            marker=dict(size=7, color=RED),
            hovertemplate="<b>%{x}</b><br>Unmet Need: %{y:.0f}<extra></extra>"
        ))
        fig2.update_layout(
            height=440, paper_bgcolor=WHITE, plot_bgcolor=BG,
            font=dict(family="Inter", size=10),
            margin=dict(l=10, r=60, t=40, b=60),
            yaxis=dict(title="Market CAGR (%)", tickfont=dict(size=9), gridcolor="#f0f0f0"),
            yaxis2=dict(title="Unmet Need Score", overlaying="y", side="right", tickfont=dict(size=9), showgrid=False),
            legend=dict(orientation="h", y=1.08),
            xaxis=dict(tickangle=-30, tickfont=dict(size=9))
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Strategic Recommendations ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🎯 Strategic Recommendations Framework")

    # Identify top priority segment
    priority = df_mkt.sort_values(["cagr_pct","tam_b"], ascending=False).iloc[0]
    defend   = df_mkt.merge(threat_by_ct if 'threat_by_ct' in dir() else df_mkt.assign(threat_pct=50),
                             on="cancer_type", how="left").sort_values("threat_pct", ascending=False).iloc[0]

    rec_tab1, rec_tab2, rec_tab3, rec_tab4 = st.tabs([
        "🚀 Launch Strategy", "🛡️ Competitive Defense", "💊 Portfolio Prioritization", "📑 Regulatory Pathway"
    ])

    with rec_tab1:
        st.markdown("#### Launch Strategy Imperatives")
        st.markdown(insight(
            f"<b>Priority Launch Segment: {priority['cancer_type']}</b> — ${priority['tam_b']:.1f}B TAM with {priority['cagr_pct']:.1f}% CAGR. "
            f"Key commercial driver: {priority['key_driver']}. Recommend phased launch starting with biomarker-selected population to maximize reimbursement coverage.",
            "success"
        ), unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Pre-Launch (T-18 to T-6 months)**")
            for item in [
                "Initiate KOL engagement and advisory boards in top 50 oncology centers",
                "File for Breakthrough Therapy or Priority Review designation where eligible",
                "Build health-economics dossier for payer pre-launch negotiations",
                "Establish patient support programs and biomarker testing access",
                "Submit for NCCN guideline inclusion — critical for formulary access",
            ]:
                st.markdown(f"• {item}")
        with col_b:
            st.markdown("**Launch (T-0 to T+12 months)**")
            for item in [
                "Target top 500 high-prescribers — oncology is concentrated (top 20% write 80% Rx)",
                "Prioritize academic medical centers and NCI-designated cancer centers in Year 1",
                "Negotiate value-based contracts with top 5 commercial payers and Part D sponsors",
                "Deploy MSL network for clinical pull-through at tumor boards",
                "Activate real-world evidence collection from Day 1 for label expansion strategy",
            ]:
                st.markdown(f"• {item}")

    with rec_tab2:
        st.markdown("#### Competitive Defense Priorities")
        high_threat = df_trial[df_trial["idn_potential"] == "Very High"]
        if not high_threat.empty:
            for _, t in high_threat.iterrows():
                st.markdown(insight(
                    f"<b>Threat: {t['drug']} ({t['sponsor']})</b> — {t['cancer_type']} | {t['moa']} | "
                    f"Targeting: {t['biomarker']} | Estimated readout: {t['est_completion']} | "
                    f"Recommended response: initiate label expansion trial in same biomarker space, accelerate switching studies.",
                    "warning"
                ), unsafe_allow_html=True)

        st.markdown("**Defense Playbook by MoA:**")
        defense_map = {
            "CDK4/6 Inhibitor": "Accelerate combination studies (CDK4/6 + PI3Kα) to differentiate from class; pursue EBC label expansion",
            "BTK Inhibitor": "2nd-gen BTK entry (Zanubrutinib) is approved; compete on tolerability (A-fib profile) and CLL 1L combo data",
            "PD-1/PD-L1 Inhibitor": "IO market commoditizing; differentiate through biomarker enrichment (TMB, PD-L1 CPS) and novel combo strategies",
            "ADC Platform": "Patent filing on linker/payload combinations; file for HER2-low and TROP2-low expansions to extend franchise",
        }
        for moa_key, rec in defense_map.items():
            moa_drugs = df_drugs[df_drugs["moa"].str.contains(moa_key.split(" ")[0], na=False)]
            if not moa_drugs.empty:
                st.markdown(f"**{moa_key}:** {rec}")

    with rec_tab3:
        st.markdown("#### Portfolio Prioritization Matrix")
        port_data = []
        for _, row in df_mkt.iterrows():
            ct = row["cancer_type"]
            drug_ct = df_drugs[df_drugs["cancer_type"] == ct]
            trial_ct = df_trial[df_trial["cancer_type"] == ct]
            score = (
                row["cagr_pct"] * 0.3 +
                row["som_b"] * 0.4 +
                len(trial_ct[trial_ct["idn_potential"].isin(["Very High","High"])]) * (-2) +
                (100 - df_seer[df_seer["cancer_type"]==ct]["5yr_survival_pct"].values[0] if ct in df_seer["cancer_type"].values else 50) * 0.1
            )
            port_data.append({"Segment": ct, "CAGR (%)": row["cagr_pct"], "SOM ($B)": row["som_b"],
                               "CAGR (%)": row["cagr_pct"], "Key Driver": row["key_driver"],
                               "Priority Score": round(score, 1),
                               "Recommendation": "Invest & Accelerate" if score > 12 else "Maintain & Defend" if score > 6 else "Selective Investment"})
        port_df = pd.DataFrame(port_data).sort_values("Priority Score", ascending=False)

        def color_rec(val):
            return {"Invest & Accelerate": "background-color:#e6f4ea;color:#1e8e3e",
                    "Maintain & Defend": "background-color:#fff8e1;color:#c07000",
                    "Selective Investment": "background-color:#fce8e6;color:#c5221f"}.get(val, "")

        styled = port_df.style.applymap(color_rec, subset=["Recommendation"])
        st.dataframe(styled, use_container_width=True, hide_index=True)

    with rec_tab4:
        st.markdown("#### Regulatory Pathway Optimization")
        reg_col1, reg_col2 = st.columns(2)
        with reg_col1:
            st.markdown("**Accelerated Approval Candidates**")
            for item in [
                "SCLC (DLL3 BiTEs): High unmet, interim ORR likely sufficient for AA",
                "Ovarian (FRα ADCs): Phase II CR data supports accelerated pathway",
                "AML (IDH1/IDH2): Confirmatory trial ongoing — track CRh endpoint",
                "r/r DLBCL (Bispecifics): Surrogate endpoint established by CAR-T",
            ]:
                st.markdown(f"• {item}")
        with reg_col2:
            st.markdown("**Breakthrough Therapy Designation Strategy**")
            for item in [
                "File BTD for any asset with >30% improvement over SOC in PFS or OS",
                "Prioritize BTD in indications with 5-yr survival <35% (SCLC, OC, AML)",
                "BTD confers rolling review — 2–4 months faster to approval",
                "Leverage Fast Track for any first-in-class MoA in rare oncology (≤200K pts)",
                "Orphan Drug Designation available for all indications <200K US prevalence",
            ]:
                st.markdown(f"• {item}")

    # ── Integrated SWOT ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔎 Integrated Market SWOT Analysis")

    sw1, sw2 = st.columns(2)
    with sw1:
        st.markdown("""
        <div style='background:#e6f4ea;border-radius:10px;padding:16px;margin-bottom:12px;'>
            <div style='font-weight:700;color:#1e8e3e;margin-bottom:8px;'>💪 STRENGTHS</div>
            <ul style='color:#0d4e26;font-size:0.85rem;line-height:1.8;margin:0;padding-left:18px;'>
                <li>Biomarker-driven precision oncology enabling premium pricing ($150–$475K WAC)</li>
                <li>Breakthrough/Accelerated designations compressing time-to-market by 18–24 months</li>
                <li>ADC & bispecific platforms creating durable IP moats beyond small molecules</li>
                <li>CDK4/6 and BTK franchise incumbency with deep prescriber loyalty</li>
                <li>CMS reimbursement established — Part B/D coverage reducing payer friction</li>
            </ul>
        </div>
        <div style='background:#fce8e6;border-radius:10px;padding:16px;'>
            <div style='font-weight:700;color:#c5221f;margin-bottom:8px;'>⚡ WEAKNESSES</div>
            <ul style='color:#7f0000;font-size:0.85rem;line-height:1.8;margin:0;padding-left:18px;'>
                <li>Accelerated approvals vulnerable to confirmatory trial failures (AA withdrawal risk)</li>
                <li>Significant WAC-to-net discount (~35–45%) compressing realized revenue</li>
                <li>CAR-T logistical complexity limiting commercial scalability</li>
                <li>REMS programs (Yescarta, Kymriah) restricting distribution channels</li>
                <li>IRA drug pricing negotiation eroding long-term revenue for established drugs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with sw2:
        st.markdown("""
        <div style='background:#e8f0fe;border-radius:10px;padding:16px;margin-bottom:12px;'>
            <div style='font-weight:700;color:#1a73e8;margin-bottom:8px;'>🚀 OPPORTUNITIES</div>
            <ul style='color:#0d2a6b;font-size:0.85rem;line-height:1.8;margin:0;padding-left:18px;'>
                <li>KRAS G12C in CRC/NSCLC: 15–30K eligible patients/yr, only 1 approved agent</li>
                <li>DLL3 BiTEs in SCLC: $4.1B TAM with minimal competition — first-mover advantage</li>
                <li>HER3/TROP2 ADC expansion: pan-tumor opportunity across 5+ indications</li>
                <li>BCMA bispecifics in myeloma: displacing CAR-T with off-the-shelf convenience</li>
                <li>Earlier lines of therapy (1L/adjuvant) unlocking 3–5x larger patient populations</li>
            </ul>
        </div>
        <div style='background:#fff8e1;border-radius:10px;padding:16px;'>
            <div style='font-weight:700;color:#c07000;margin-bottom:8px;'>⚠️ THREATS</div>
            <ul style='color:#4a3700;font-size:0.85rem;line-height:1.8;margin:0;padding-left:18px;'>
                <li>IRA Medicare price negotiation: 10 drugs selected 2025, expanding annually</li>
                <li>Patent cliffs for CDK4/6 (2025–2028) opening $8–12B to biosimilar erosion</li>
                <li>BTK inhibitor class crowding: 3rd-gen non-covalent BTKi (Pirtobrutinib) approved</li>
                <li>PD-1/PD-L1 IO market saturation in NSCLC — differentiation increasingly difficult</li>
                <li>CAR-T reimbursement pressure: CMS episodic payment model under evaluation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Bottom Line ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📌 Bottom Line Assessment")
    st.markdown(insight(
        f"The oncology market across the {len(cancer_types)} selected segments represents a <b>${total_tam:.0f}B TAM</b> growing at "
        f"<b>{avg_cagr:.1f}% CAGR</b>, with a realistically addressable opportunity of <b>${total_som:.1f}B</b>. "
        f"The highest-priority launch segments are <b>{priority['cancer_type']}</b> (growth) and "
        f"<b>SCLC</b> (unmet need). The pipeline carries <b>{len(high_disr)} high-disruption threats</b> that require "
        f"proactive label expansion and switching-study investment to defend incumbency. "
        f"Regulatory strategy should prioritize Breakthrough Therapy Designation and accelerated confirmatory design "
        f"to sustain 2025–2029 franchise value of <b>${rev_2029:.0f}B</b>.",
        "success"
    ), unsafe_allow_html=True)
