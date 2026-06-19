# 💊 Pharma Launch Intelligence Platform
### Oncology Competitive Market Assessment

A production-ready end-to-end **Drug Launch Intelligence Platform** for oncology market analysis, built for portfolio demonstration and real-world healthcare analytics use cases.

---

## 🚀 Live Deployment on Streamlit Cloud

---

## 📦 Project Structure

```
pharma_platform/
├── app.py                          # Main entry point & navigation
├── requirements.txt                # Dependencies
├── .streamlit/
│   └── config.toml                 # Theme configuration
├── pages/
│   ├── overview.py                 # Market Overview & TAM/SAM/SOM
│   ├── benchmarking.py             # Competitive Benchmarking (50+ vars)
│   ├── forecasting.py              # Launch Forecasting 2015–2029
│   ├── pipeline.py                 # Clinical Trial Pipeline Intelligence
│   └── executive.py                # Executive Summary & Strategy
├── data/
│   └── datasets.py                 # All simulated datasets (FDA, CMS, SEER, Trials)
└── utils/
    └── helpers.py                  # Plotly theme, color palettes, components
```

---

## 🔬 Platform Modules

| Module | Description |
|--------|-------------|
| **Market Overview** | TAM/SAM/SOM sizing, NCI SEER incidence, FDA approval trends, CMS spend |
| **Competitive Benchmarking** | 50+ variable matrix, efficacy vs. price scatter, spider charts, MoA heatmap |
| **Launch Forecasting** | Revenue ramp modeling, patent cliff waterfall, scenario planning (Bull/Base/Bear) |
| **Clinical Trial Pipeline** | Gantt timeline, disruption scoring, enrollment analysis, strategic alerts |
| **Executive Summary** | Opportunity-risk matrix, SWOT, portfolio prioritization, regulatory pathway guide |

---

## 📊 Data Sources (Simulated)

All data is **realistically simulated** based on publicly available ranges from:
- **FDA openFDA**: Drug approval metadata, trial phase, endpoints
- **CMS Medicare**: Drug spending, claims, beneficiary counts (2020–2023)
- **NCI SEER**: Cancer incidence, survival rates, prevalence
- **ClinicalTrials.gov**: Phase III pipeline trials, enrollment, completion

> ⚠️ This platform uses simulated data for portfolio/research demonstration. Numbers are illustrative and drawn from public domain ranges.

---

## 💻 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.32+
- **Visualization**: Plotly 5.18+
- **Data**: Pandas + NumPy
- **Deployment**: Streamlit Community Cloud (free)


---

## 📌 Key Analytics Capabilities

- Market segmentation across 9 cancer types
- 24 approved drugs with 23+ clinical/commercial variables each
- 15 Phase III pipeline trials with competitive threat scoring
- Revenue forecasting 2015–2029 with LOE/patent cliff modeling
- Consulting-style strategic recommendation framework

---

*Built as a portfolio demonstration of healthcare marketplace analytics, data science, and commercial strategy capabilities.*
