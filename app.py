import streamlit as st

st.set_page_config(
    page_title="Pharma Launch Intelligence Platform",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── fonts & base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a2342 0%, #0d2d5a 60%, #0f3a70 100%);
    border-right: 1px solid #1a3a6b;
}
[data-testid="stSidebar"] * { color: #e8f0fe !important; }
[data-testid="stSidebar"] .stRadio label { color: #c5d8f5 !important; }

/* ── main background ── */
.main .block-container {
    background: #f7f9fc;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ── cards ── */
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 2px 8px rgba(10,35,66,0.08);
    border-left: 4px solid #1a73e8;
    margin-bottom: 0;
}
.kpi-card h2 { margin: 0; font-size: 2rem; font-weight: 700; color: #0a2342; }
.kpi-card p  { margin: 4px 0 0 0; font-size: 0.82rem; color: #5f6368; font-weight: 500; }
.kpi-card .delta-pos { color: #1e8e3e; font-size: 0.78rem; font-weight: 600; }
.kpi-card .delta-neg { color: #d93025; font-size: 0.78rem; font-weight: 600; }

/* ── section headers ── */
.section-header {
    font-size: 1.1rem; font-weight: 600; color: #0a2342;
    border-bottom: 2px solid #e8f0fe; padding-bottom: 8px; margin-bottom: 16px;
}

/* ── insight box ── */
.insight-box {
    background: #e8f4fd;
    border-left: 4px solid #1a73e8;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.88rem;
    color: #1a3a6b;
}
.warning-box {
    background: #fff8e1;
    border-left: 4px solid #f9ab00;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.88rem;
    color: #4a3700;
}
.success-box {
    background: #e6f4ea;
    border-left: 4px solid #1e8e3e;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.88rem;
    color: #0d4e26;
}

/* ── page title ── */
.page-title {
    font-size: 1.65rem; font-weight: 700; color: #0a2342; margin-bottom: 4px;
}
.page-subtitle { font-size: 0.9rem; color: #5f6368; margin-bottom: 24px; }

/* ── table styling ── */
.dataframe thead th {
    background: #0a2342 !important; color: white !important;
    font-size: 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-size:1.6rem;'>💊</div>
        <div style='font-size:0.95rem; font-weight:700; color:#e8f0fe; letter-spacing:0.5px;'>
            Launch Intelligence
        </div>
        <div style='font-size:0.7rem; color:#8ab4f8; margin-top:2px;'>
            Oncology · Competitive Intel
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.72rem; color:#8ab4f8; font-weight:600; letter-spacing:1px; margin-bottom:8px;'>NAVIGATION</div>", unsafe_allow_html=True)

    page = st.radio(
        "",
        [
            "🏠  Market Overview",
            "⚔️  Competitive Benchmarking",
            "📈  Launch Forecasting",
            "🔬  Clinical Trial Pipeline",
            "📋  Executive Summary",
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#8ab4f8; font-weight:600; letter-spacing:1px; margin-bottom:8px;'>DATA SOURCES</div>
    <div style='font-size:0.75rem; color:#c5d8f5; line-height:1.8;'>
        ✅ FDA Drug Approvals (simulated)<br>
        ✅ CMS Medicare Claims (simulated)<br>
        ✅ NCI SEER Incidence Data<br>
        ✅ ClinicalTrials.gov Pipeline<br>
        ✅ Physician Prescribing Intel
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem; color:#8ab4f8; font-weight:600; letter-spacing:1px; margin-bottom:6px;'>FILTERS</div>
    """, unsafe_allow_html=True)

    cancer_types = st.multiselect(
        "Cancer Type",
        ["Breast", "Lung (NSCLC)", "Lung (SCLC)", "CRC", "Leukemia", "Lymphoma", "Myeloma", "Ovarian", "Melanoma"],
        default=["Breast", "Lung (NSCLC)", "CRC", "Leukemia"],
        key="global_cancer_filter"
    )

    year_range = st.slider("Approval Year Range", 2015, 2024, (2018, 2024), key="global_year")

    st.markdown("---")
    st.markdown("<div style='font-size:0.68rem; color:#5f7999; text-align:center;'>v2.1.0 · Data as of Q4 2024<br>For portfolio & research use</div>", unsafe_allow_html=True)

# ── Route to pages ──────────────────────────────────────────────────────────
if "Overview" in page:
    from pages import overview
    overview.render(cancer_types, year_range)
elif "Benchmarking" in page:
    from pages import benchmarking
    benchmarking.render(cancer_types, year_range)
elif "Forecasting" in page:
    from pages import forecasting
    forecasting.render(cancer_types, year_range)
elif "Pipeline" in page:
    from pages import pipeline
    pipeline.render(cancer_types, year_range)
elif "Executive" in page:
    from pages import executive
    executive.render(cancer_types, year_range)
