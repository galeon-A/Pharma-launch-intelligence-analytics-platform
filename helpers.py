"""utils/helpers.py — shared Plotly theme & formatting helpers"""
import plotly.graph_objects as go
import plotly.express as px

# ── Brand palette ─────────────────────────────────────────────────────────
NAVY      = "#0a2342"
BLUE      = "#1a73e8"
LIGHT_BLUE= "#4a90d9"
TEAL      = "#00897b"
GREEN     = "#1e8e3e"
AMBER     = "#f9ab00"
RED       = "#d93025"
GREY      = "#5f6368"
BG        = "#f7f9fc"
WHITE     = "#ffffff"

CANCER_COLORS = {
    "Breast":       "#e91e8c",
    "Lung (NSCLC)": "#1a73e8",
    "Lung (SCLC)":  "#4a90d9",
    "CRC":          "#00897b",
    "Leukemia":     "#9c27b0",
    "Lymphoma":     "#7c4dff",
    "Myeloma":      "#f4511e",
    "Ovarian":      "#f9ab00",
    "Melanoma":     "#0f9d58",
}

COMPANY_COLORS = {
    "Pfizer":              "#003087",
    "Novartis":            "#e11931",
    "Eli Lilly":           "#d52b1e",
    "AstraZeneca":         "#6f3091",
    "AstraZeneca/MSD":     "#6f3091",
    "AstraZeneca/Daiichi": "#6f3091",
    "Merck":               "#009A44",
    "Genentech/Roche":     "#2c75b5",
    "Genentech":           "#2c75b5",
    "Amgen":               "#0068b8",
    "J&J":                 "#cc0000",
    "J&J/AbbVie":          "#cc0000",
    "AbbVie/Roche":        "#071d49",
    "AbbVie":              "#071d49",
    "BMS":                 "#ff6600",
    "Kite/Gilead":         "#00b0ca",
    "GSK":                 "#f36d21",
    "BeiGene":             "#1b4f72",
    "Mirati/BMS":          "#ff8c42",
    "Roche/Genentech":     "#2c75b5",
    "Regeneron":           "#4cb8c4",
    "ImmunoGen/AbbVie":    "#071d49",
}

MOA_COLORS = {
    "CDK4/6 Inhibitor":    "#1a73e8",
    "PARP Inhibitor":      "#9c27b0",
    "ADC (HER2)":          "#e91e8c",
    "ADC (TROP2)":         "#f06292",
    "ADC (FRα)":           "#f8bbd0",
    "EGFR TKI (3rd gen)":  "#00897b",
    "ALK Inhibitor (2nd gen)": "#4db6ac",
    "PD-1 Inhibitor":      "#ff6600",
    "PD-L1 Inhibitor":     "#ffa040",
    "KRAS G12C Inhibitor": "#f9ab00",
    "BCL-2 Inhibitor":     "#0f9d58",
    "BTK Inhibitor":       "#7c4dff",
    "BTK Inhibitor (2nd gen)":"#651fff",
    "CAR-T (CD19)":        "#d50000",
    "Bispecific (CD20xCD3)":"#c62828",
    "Bispecific (BCMAxCD3)":"#e53935",
    "CD38 Monoclonal Ab":  "#1565c0",
    "BRAF Inhibitor":      "#558b2f",
    "BRAF+MEK combo":      "#33691e",
    "PD-1 + CTLA-4 combo": "#e65100",
    "VEGF Inhibitor":      "#37474f",
    "PARP Inhibitor":      "#9c27b0",
    "Proteasome Inhibitor":"#4a148c",
}

def plotly_layout(title="", height=420, legend=True):
    return dict(
        title=dict(text=title, font=dict(size=14, color=NAVY, family="Inter"), x=0),
        height=height,
        paper_bgcolor=WHITE,
        plot_bgcolor=BG,
        font=dict(family="Inter", size=12, color=GREY),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0,
            font=dict(size=10)
        ) if legend else dict(visible=False),
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(showgrid=False, linecolor="#e0e0e0", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="#f0f0f0", linecolor="#e0e0e0", tickfont=dict(size=10)),
    )

def fmt_b(val):
    if val is None: return "N/A"
    return f"${val:.1f}B"

def fmt_pct(val):
    if val is None: return "N/A"
    return f"{val:.1f}%"

def fmt_k(val):
    if val is None: return "N/A"
    if val >= 1000: return f"{val/1000:.0f}K"
    return str(int(val))

def kpi_card(label, value, delta=None, delta_pos=True):
    delta_html = ""
    if delta:
        cls = "delta-pos" if delta_pos else "delta-neg"
        arrow = "▲" if delta_pos else "▼"
        delta_html = f'<span class="{cls}">{arrow} {delta}</span>'
    return f"""
    <div class="kpi-card">
        <h2>{value}</h2>
        <p>{label}</p>
        {delta_html}
    </div>
    """

def insight(text, kind="info"):
    cls = {"info":"insight-box","warning":"warning-box","success":"success-box"}.get(kind,"insight-box")
    icon = {"info":"💡","warning":"⚠️","success":"✅"}.get(kind,"💡")
    return f'<div class="{cls}">{icon} {text}</div>'
