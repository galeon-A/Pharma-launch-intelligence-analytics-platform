"""
data/datasets.py
Realistic simulated datasets for all platform modules.
All numbers are illustrative and drawn from public domain ranges.
"""
import pandas as pd
import numpy as np

np.random.seed(42)

# ─── FDA Drug Approvals ────────────────────────────────────────────────────
FDA_DRUGS = pd.DataFrame([
    # Breast Cancer
    {"drug":"Palbociclib","brand":"Ibrance","company":"Pfizer","cancer_type":"Breast","indication":"HR+/HER2- mBC","moa":"CDK4/6 Inhibitor","approval_year":2015,"approval_type":"Accelerated","trial_phase":"III","primary_endpoint":"PFS","pfs_months":24.8,"os_months":53.9,"orr_pct":42,"trial_n":521,"wac_annual":148000,"cms_allowed":112000,"market_share_pct":38,"peak_sales_b":5.2,"launch_quarter":"Q1 2015","label_expansion":3,"fda_priority_review":True,"orphan_drug":False,"breakthrough":True,"rems":False},
    {"drug":"Ribociclib","brand":"Kisqali","company":"Novartis","cancer_type":"Breast","indication":"HR+/HER2- mBC","moa":"CDK4/6 Inhibitor","approval_year":2017,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"PFS","pfs_months":25.3,"os_months":58.7,"orr_pct":41,"trial_n":668,"wac_annual":156000,"cms_allowed":118000,"market_share_pct":29,"peak_sales_b":3.8,"launch_quarter":"Q1 2017","label_expansion":2,"fda_priority_review":True,"orphan_drug":False,"breakthrough":True,"rems":False},
    {"drug":"Abemaciclib","brand":"Verzenio","company":"Eli Lilly","cancer_type":"Breast","indication":"HR+/HER2- mBC / EBC","moa":"CDK4/6 Inhibitor","approval_year":2017,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"PFS","pfs_months":28.2,"os_months":None,"orr_pct":48,"trial_n":669,"wac_annual":141000,"cms_allowed":107000,"market_share_pct":33,"peak_sales_b":4.1,"launch_quarter":"Q3 2017","label_expansion":2,"fda_priority_review":False,"orphan_drug":False,"breakthrough":True,"rems":False},
    {"drug":"Trastuzumab deruxtecan","brand":"Enhertu","company":"AstraZeneca/Daiichi","cancer_type":"Breast","indication":"HER2+ mBC","moa":"ADC (HER2)","approval_year":2019,"approval_type":"Accelerated","trial_phase":"II","primary_endpoint":"ORR","pfs_months":19.4,"os_months":None,"orr_pct":60,"trial_n":184,"wac_annual":175000,"cms_allowed":132000,"market_share_pct":44,"peak_sales_b":5.6,"launch_quarter":"Q4 2019","label_expansion":3,"fda_priority_review":True,"orphan_drug":False,"breakthrough":True,"rems":False},
    {"drug":"Olaparib","brand":"Lynparza","company":"AstraZeneca/MSD","cancer_type":"Breast","indication":"gBRCA+ HER2- mBC","moa":"PARP Inhibitor","approval_year":2018,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"PFS","pfs_months":7.0,"os_months":19.3,"orr_pct":59,"trial_n":302,"wac_annual":183000,"cms_allowed":138000,"market_share_pct":22,"peak_sales_b":2.9,"launch_quarter":"Q1 2018","label_expansion":2,"fda_priority_review":True,"orphan_drug":False,"breakthrough":True,"rems":False},
    # Lung Cancer
    {"drug":"Osimertinib","brand":"Tagrisso","company":"AstraZeneca","cancer_type":"Lung (NSCLC)","indication":"EGFR T790M+ NSCLC","moa":"EGFR TKI (3rd gen)","approval_year":2015,"approval_type":"Accelerated","trial_phase":"III","primary_endpoint":"PFS","pfs_months":18.9,"os_months":38.6,"orr_pct":71,"trial_n":419,"wac_annual":178000,"cms_allowed":134000,"market_share_pct":52,"peak_sales_b":6.8,"launch_quarter":"Q4 2015","label_expansion":3,"fda_priority_review":True,"orphan_drug":False,"breakthrough":True,"rems":False},
    {"drug":"Alectinib","brand":"Alecensa","company":"Genentech/Roche","cancer_type":"Lung (NSCLC)","indication":"ALK+ NSCLC","moa":"ALK Inhibitor (2nd gen)","approval_year":2015,"approval_type":"Accelerated","trial_phase":"III","primary_endpoint":"PFS","pfs_months":34.8,"os_months":None,"orr_pct":83,"trial_n":303,"wac_annual":162000,"cms_allowed":122000,"market_share_pct":41,"peak_sales_b":3.2,"launch_quarter":"Q4 2015","label_expansion":1,"fda_priority_review":True,"orphan_drug":False,"breakthrough":True,"rems":False},
    {"drug":"Pembrolizumab","brand":"Keytruda","company":"Merck","cancer_type":"Lung (NSCLC)","indication":"PD-L1≥50% NSCLC 1L","moa":"PD-1 Inhibitor","approval_year":2016,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"OS","pfs_months":10.3,"os_months":26.3,"orr_pct":45,"trial_n":305,"wac_annual":164000,"cms_allowed":124000,"market_share_pct":58,"peak_sales_b":17.2,"launch_quarter":"Q4 2016","label_expansion":8,"fda_priority_review":True,"orphan_drug":False,"breakthrough":True,"rems":False},
    {"drug":"Sotorasib","brand":"Lumakras","company":"Amgen","cancer_type":"Lung (NSCLC)","indication":"KRAS G12C+ NSCLC","moa":"KRAS G12C Inhibitor","approval_year":2021,"approval_type":"Accelerated","trial_phase":"II","primary_endpoint":"ORR","pfs_months":6.8,"os_months":12.5,"orr_pct":37,"trial_n":126,"wac_annual":187000,"cms_allowed":141000,"market_share_pct":28,"peak_sales_b":0.9,"launch_quarter":"Q2 2021","label_expansion":1,"fda_priority_review":True,"orphan_drug":False,"breakthrough":False,"rems":False},
    {"drug":"Atezolizumab","brand":"Tecentriq","company":"Genentech","cancer_type":"Lung (SCLC)","indication":"ES-SCLC 1L","moa":"PD-L1 Inhibitor","approval_year":2019,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"OS","pfs_months":5.2,"os_months":12.3,"orr_pct":60,"trial_n":403,"wac_annual":158000,"cms_allowed":119000,"market_share_pct":18,"peak_sales_b":1.2,"launch_quarter":"Q1 2019","label_expansion":1,"fda_priority_review":False,"orphan_drug":False,"breakthrough":False,"rems":False},
    # CRC
    {"drug":"Encorafenib","brand":"Braftovi","company":"Pfizer","cancer_type":"CRC","indication":"BRAF V600E+ mCRC","moa":"BRAF Inhibitor","approval_year":2020,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"OS","pfs_months":4.2,"os_months":9.0,"orr_pct":26,"trial_n":665,"wac_annual":130000,"cms_allowed":98000,"market_share_pct":34,"peak_sales_b":0.7,"launch_quarter":"Q2 2020","label_expansion":1,"fda_priority_review":True,"orphan_drug":False,"breakthrough":False,"rems":False},
    {"drug":"Pembrolizumab","brand":"Keytruda","company":"Merck","cancer_type":"CRC","indication":"MSI-H/dMMR mCRC 1L","moa":"PD-1 Inhibitor","approval_year":2020,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"PFS","pfs_months":16.5,"os_months":None,"orr_pct":44,"trial_n":307,"wac_annual":164000,"cms_allowed":124000,"market_share_pct":48,"peak_sales_b":2.1,"launch_quarter":"Q2 2020","label_expansion":2,"fda_priority_review":True,"orphan_drug":False,"breakthrough":False,"rems":False},
    {"drug":"Sotorasib","brand":"Lumakras","company":"Amgen","cancer_type":"CRC","indication":"KRAS G12C+ mCRC","moa":"KRAS G12C Inhibitor","approval_year":2023,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"OS","pfs_months":5.6,"os_months":None,"orr_pct":26,"trial_n":345,"wac_annual":187000,"cms_allowed":141000,"market_share_pct":15,"peak_sales_b":0.3,"launch_quarter":"Q1 2023","label_expansion":0,"fda_priority_review":False,"orphan_drug":False,"breakthrough":False,"rems":False},
    # Leukemia
    {"drug":"Venetoclax","brand":"Venclexta","company":"AbbVie/Roche","cancer_type":"Leukemia","indication":"CLL/AML","moa":"BCL-2 Inhibitor","approval_year":2016,"approval_type":"Accelerated","trial_phase":"III","primary_endpoint":"PFS","pfs_months":None,"os_months":None,"orr_pct":79,"trial_n":389,"wac_annual":153000,"cms_allowed":115000,"market_share_pct":45,"peak_sales_b":4.6,"launch_quarter":"Q2 2016","label_expansion":4,"fda_priority_review":True,"orphan_drug":True,"breakthrough":True,"rems":False},
    {"drug":"Ibrutinib","brand":"Imbruvica","company":"J&J/AbbVie","cancer_type":"Leukemia","indication":"CLL/MCL 1L","moa":"BTK Inhibitor","approval_year":2013,"approval_type":"Accelerated","trial_phase":"III","primary_endpoint":"PFS","pfs_months":44.1,"os_months":None,"orr_pct":90,"trial_n":391,"wac_annual":148000,"cms_allowed":112000,"market_share_pct":38,"peak_sales_b":9.1,"launch_quarter":"Q4 2013","label_expansion":7,"fda_priority_review":True,"orphan_drug":True,"breakthrough":True,"rems":False},
    {"drug":"Acalabrutinib","brand":"Calquence","company":"AstraZeneca","cancer_type":"Leukemia","indication":"CLL 1L","moa":"BTK Inhibitor (2nd gen)","approval_year":2017,"approval_type":"Accelerated","trial_phase":"III","primary_endpoint":"PFS","pfs_months":38.4,"os_months":None,"orr_pct":93,"trial_n":533,"wac_annual":156000,"cms_allowed":118000,"market_share_pct":29,"peak_sales_b":2.5,"launch_quarter":"Q4 2017","label_expansion":2,"fda_priority_review":True,"orphan_drug":True,"breakthrough":True,"rems":False},
    # Lymphoma
    {"drug":"Axicabtagene ciloleucel","brand":"Yescarta","company":"Kite/Gilead","cancer_type":"Lymphoma","indication":"r/r LBCL","moa":"CAR-T (CD19)","approval_year":2017,"approval_type":"Regular","trial_phase":"II","primary_endpoint":"ORR","pfs_months":None,"os_months":None,"orr_pct":72,"trial_n":101,"wac_annual":373000,"cms_allowed":299000,"market_share_pct":35,"peak_sales_b":1.1,"launch_quarter":"Q4 2017","label_expansion":2,"fda_priority_review":True,"orphan_drug":True,"breakthrough":True,"rems":True},
    {"drug":"Tisagenlecleucel","brand":"Kymriah","company":"Novartis","cancer_type":"Lymphoma","indication":"r/r DLBCL / ALL","moa":"CAR-T (CD19)","approval_year":2017,"approval_type":"Regular","trial_phase":"II","primary_endpoint":"ORR","pfs_months":None,"os_months":None,"orr_pct":52,"trial_n":93,"wac_annual":475000,"cms_allowed":380000,"market_share_pct":22,"peak_sales_b":0.5,"launch_quarter":"Q3 2017","label_expansion":1,"fda_priority_review":True,"orphan_drug":True,"breakthrough":True,"rems":True},
    {"drug":"Mosunetuzumab","brand":"Lunsumio","company":"Roche","cancer_type":"Lymphoma","indication":"r/r FL","moa":"Bispecific (CD20xCD3)","approval_year":2022,"approval_type":"Accelerated","trial_phase":"II","primary_endpoint":"CR rate","pfs_months":None,"os_months":None,"orr_pct":80,"trial_n":90,"wac_annual":280000,"cms_allowed":224000,"market_share_pct":12,"peak_sales_b":0.4,"launch_quarter":"Q4 2022","label_expansion":0,"fda_priority_review":True,"orphan_drug":True,"breakthrough":True,"rems":False},
    # Myeloma
    {"drug":"Daratumumab","brand":"Darzalex","company":"J&J","cancer_type":"Myeloma","indication":"NDMM & RRMM","moa":"CD38 Monoclonal Ab","approval_year":2015,"approval_type":"Accelerated","trial_phase":"III","primary_endpoint":"PFS","pfs_months":None,"os_months":None,"orr_pct":93,"trial_n":706,"wac_annual":161000,"cms_allowed":122000,"market_share_pct":55,"peak_sales_b":8.7,"launch_quarter":"Q4 2015","label_expansion":6,"fda_priority_review":True,"orphan_drug":True,"breakthrough":True,"rems":False},
    {"drug":"Carfilzomib","brand":"Kyprolis","company":"Amgen","cancer_type":"Myeloma","indication":"RRMM","moa":"Proteasome Inhibitor","approval_year":2012,"approval_type":"Accelerated","trial_phase":"III","primary_endpoint":"PFS","pfs_months":18.7,"os_months":47.6,"orr_pct":77,"trial_n":792,"wac_annual":116000,"cms_allowed":88000,"market_share_pct":32,"peak_sales_b":2.3,"launch_quarter":"Q3 2012","label_expansion":3,"fda_priority_review":True,"orphan_drug":True,"breakthrough":False,"rems":False},
    # Ovarian
    {"drug":"Bevacizumab","brand":"Avastin","company":"Genentech/Roche","cancer_type":"Ovarian","indication":"Stage III/IV OC","moa":"VEGF Inhibitor","approval_year":2018,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"PFS","pfs_months":14.1,"os_months":None,"orr_pct":38,"trial_n":1873,"wac_annual":88000,"cms_allowed":66000,"market_share_pct":44,"peak_sales_b":1.7,"launch_quarter":"Q2 2018","label_expansion":1,"fda_priority_review":False,"orphan_drug":False,"breakthrough":False,"rems":False},
    {"drug":"Niraparib","brand":"Zejula","company":"GSK","cancer_type":"Ovarian","indication":"HRD+ OC maintenance","moa":"PARP Inhibitor","approval_year":2017,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"PFS","pfs_months":21.9,"os_months":None,"orr_pct":None,"trial_n":553,"wac_annual":174000,"cms_allowed":131000,"market_share_pct":31,"peak_sales_b":1.1,"launch_quarter":"Q1 2017","label_expansion":2,"fda_priority_review":True,"orphan_drug":False,"breakthrough":False,"rems":False},
    # Melanoma
    {"drug":"Nivolumab + Ipilimumab","brand":"Opdivo + Yervoy","company":"BMS","cancer_type":"Melanoma","indication":"Unresectable Melanoma 1L","moa":"PD-1 + CTLA-4 combo","approval_year":2015,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"PFS","pfs_months":11.5,"os_months":72.1,"orr_pct":58,"trial_n":945,"wac_annual":256000,"cms_allowed":192000,"market_share_pct":42,"peak_sales_b":4.5,"launch_quarter":"Q4 2015","label_expansion":5,"fda_priority_review":True,"orphan_drug":False,"breakthrough":True,"rems":False},
    {"drug":"Dabrafenib + Trametinib","brand":"Tafinlar + Mekinist","company":"Novartis","cancer_type":"Melanoma","indication":"BRAF V600+ Melanoma","moa":"BRAF+MEK combo","approval_year":2014,"approval_type":"Regular","trial_phase":"III","primary_endpoint":"PFS","pfs_months":11.4,"os_months":25.1,"orr_pct":64,"trial_n":423,"wac_annual":196000,"cms_allowed":148000,"market_share_pct":38,"peak_sales_b":3.2,"launch_quarter":"Q1 2014","label_expansion":3,"fda_priority_review":False,"orphan_drug":False,"breakthrough":True,"rems":False},
])

# ─── CMS Medicare Claims (simulated) ──────────────────────────────────────
def get_cms_data():
    drugs = FDA_DRUGS["drug"].unique()
    years = [2020, 2021, 2022, 2023]
    rows = []
    np.random.seed(99)
    for drug in drugs:
        row = FDA_DRUGS[FDA_DRUGS["drug"] == drug].iloc[0]
        base_claims = np.random.randint(8000, 120000)
        base_spend = row["cms_allowed"] * base_claims / 12
        for yr in years:
            growth = np.random.uniform(0.04, 0.22)
            rows.append({
                "drug": drug,
                "brand": row["brand"],
                "company": row["company"],
                "cancer_type": row["cancer_type"],
                "year": yr,
                "total_claims": int(base_claims * (1 + growth) ** (yr - 2020)),
                "total_beneficiaries": int(base_claims * 0.85 * (1 + growth) ** (yr - 2020)),
                "total_spend_m": round(base_spend * (1 + growth) ** (yr - 2020) / 1e6, 2),
                "avg_cost_per_claim": round(row["cms_allowed"] / 12, 2),
                "avg_cost_per_beneficiary": round(row["cms_allowed"] * np.random.uniform(0.9, 1.1), 2),
            })
    return pd.DataFrame(rows)

# ─── NCI SEER Cancer Incidence ────────────────────────────────────────────
SEER_DATA = pd.DataFrame([
    {"cancer_type":"Breast",        "new_cases_2024":310000,"deaths_2024":42000,"5yr_survival_pct":91,"incidence_rate_per100k":128.1,"trend_pct":1.1,"stage_iv_pct":6,"biomarker_eligible_pct":68,"us_prevalence":3800000},
    {"cancer_type":"Lung (NSCLC)",  "new_cases_2024":200000,"deaths_2024":125000,"5yr_survival_pct":28,"incidence_rate_per100k":51.8,"trend_pct":-2.4,"stage_iv_pct":57,"biomarker_eligible_pct":30,"us_prevalence":520000},
    {"cancer_type":"Lung (SCLC)",   "new_cases_2024":35000, "deaths_2024":31000,"5yr_survival_pct":7,"incidence_rate_per100k":9.1,"trend_pct":-3.1,"stage_iv_pct":70,"biomarker_eligible_pct":10,"us_prevalence":48000},
    {"cancer_type":"CRC",           "new_cases_2024":153000,"deaths_2024":52000,"5yr_survival_pct":65,"incidence_rate_per100k":38.7,"trend_pct":0.5,"stage_iv_pct":22,"biomarker_eligible_pct":20,"us_prevalence":1400000},
    {"cancer_type":"Leukemia",      "new_cases_2024":60000, "deaths_2024":24000,"5yr_survival_pct":65,"incidence_rate_per100k":15.1,"trend_pct":0.8,"stage_iv_pct":None,"biomarker_eligible_pct":60,"us_prevalence":490000},
    {"cancer_type":"Lymphoma",      "new_cases_2024":90000, "deaths_2024":21000,"5yr_survival_pct":73,"incidence_rate_per100k":22.8,"trend_pct":1.2,"stage_iv_pct":35,"biomarker_eligible_pct":40,"us_prevalence":800000},
    {"cancer_type":"Myeloma",       "new_cases_2024":36000, "deaths_2024":13000,"5yr_survival_pct":59,"incidence_rate_per100k":7.2,"trend_pct":0.7,"stage_iv_pct":95,"biomarker_eligible_pct":90,"us_prevalence":160000},
    {"cancer_type":"Ovarian",       "new_cases_2024":20000, "deaths_2024":13000,"5yr_survival_pct":49,"incidence_rate_per100k":10.8,"trend_pct":-0.9,"stage_iv_pct":58,"biomarker_eligible_pct":45,"us_prevalence":220000},
    {"cancer_type":"Melanoma",      "new_cases_2024":100000,"deaths_2024":8000, "5yr_survival_pct":93,"incidence_rate_per100k":24.6,"trend_pct":1.8,"stage_iv_pct":4,"biomarker_eligible_pct":50,"us_prevalence":1400000},
])

# ─── Clinical Trials Pipeline ──────────────────────────────────────────────
TRIALS = pd.DataFrame([
    {"nct_id":"NCT04519034","drug":"Inavolisib","sponsor":"Genentech/Roche","cancer_type":"Breast","phase":"III","moa":"PI3Kα Inhibitor","primary_endpoint":"PFS","enrollment":850,"start_year":2021,"est_completion":2025,"status":"Active, not recruiting","biomarker":"PIK3CA mutant","combo":"+ Palbociclib + Fulvestrant","idn_potential":"High"},
    {"nct_id":"NCT04685135","drug":"Capivasertib","sponsor":"AstraZeneca","cancer_type":"Breast","phase":"III","moa":"AKT Inhibitor","primary_endpoint":"PFS","enrollment":708,"start_year":2021,"est_completion":2024,"status":"Completed","biomarker":"PIK3CA/AKT/PTEN alt","combo":"+ Fulvestrant","idn_potential":"High"},
    {"nct_id":"NCT05432388","drug":"Datopotamab deruxtecan","sponsor":"AstraZeneca/Daiichi","cancer_type":"Breast","phase":"III","moa":"ADC (TROP2)","primary_endpoint":"PFS/OS","enrollment":990,"start_year":2022,"est_completion":2026,"status":"Recruiting","biomarker":"TROP2 expressing","combo":"Monotherapy","idn_potential":"Very High"},
    {"nct_id":"NCT03600883","drug":"Amivantamab","sponsor":"J&J","cancer_type":"Lung (NSCLC)","phase":"III","moa":"EGFR/MET Bispecific","primary_endpoint":"PFS","enrollment":1074,"start_year":2019,"est_completion":2024,"status":"Completed","biomarker":"EGFR Exon 20 ins","combo":"+ Lazertinib","idn_potential":"High"},
    {"nct_id":"NCT04487080","drug":"Adagrasib","sponsor":"Mirati/BMS","cancer_type":"Lung (NSCLC)","phase":"III","moa":"KRAS G12C Inhibitor","primary_endpoint":"OS","enrollment":790,"start_year":2020,"est_completion":2025,"status":"Active, not recruiting","biomarker":"KRAS G12C","combo":"vs Docetaxel","idn_potential":"High"},
    {"nct_id":"NCT04949399","drug":"Patritumab deruxtecan","sponsor":"Daiichi/AstraZeneca","cancer_type":"Lung (NSCLC)","phase":"III","moa":"ADC (HER3)","primary_endpoint":"PFS","enrollment":830,"start_year":2022,"est_completion":2026,"status":"Recruiting","biomarker":"HER3 expressing","combo":"Monotherapy","idn_potential":"Very High"},
    {"nct_id":"NCT05585996","drug":"Tarlatamab","sponsor":"Amgen","cancer_type":"Lung (SCLC)","phase":"III","moa":"BiTE (DLL3xCD3)","primary_endpoint":"OS","enrollment":440,"start_year":2022,"est_completion":2026,"status":"Recruiting","biomarker":"DLL3 expressing","combo":"vs Topotecan/Amrubicin","idn_potential":"Very High"},
    {"nct_id":"NCT04009577","drug":"Divarasib","sponsor":"Genentech/Roche","cancer_type":"CRC","phase":"III","moa":"KRAS G12C Inhibitor","primary_endpoint":"PFS","enrollment":550,"start_year":2022,"est_completion":2025,"status":"Recruiting","biomarker":"KRAS G12C","combo":"+ Cetuximab","idn_potential":"High"},
    {"nct_id":"NCT03274895","drug":"Zanubrutinib","sponsor":"BeiGene","cancer_type":"Leukemia","phase":"III","moa":"BTK Inhibitor (2nd gen)","primary_endpoint":"PFS","enrollment":652,"start_year":2018,"est_completion":2024,"status":"Completed","biomarker":"CLL/SLL","combo":"vs Ibrutinib","idn_potential":"High"},
    {"nct_id":"NCT04082936","drug":"Epcoritamab","sponsor":"AbbVie/Genmab","cancer_type":"Lymphoma","phase":"III","moa":"Bispecific (CD20xCD3)","primary_endpoint":"PFS","enrollment":780,"start_year":2020,"est_completion":2025,"status":"Active, not recruiting","biomarker":"DLBCL","combo":"+ R-CHOP","idn_potential":"Very High"},
    {"nct_id":"NCT04613167","drug":"Glofitamab","sponsor":"Roche/Genentech","cancer_type":"Lymphoma","phase":"III","moa":"Bispecific (CD20xCD3)","primary_endpoint":"OS","enrollment":620,"start_year":2021,"est_completion":2025,"status":"Active, not recruiting","biomarker":"DLBCL r/r","combo":"+ GemOx","idn_potential":"High"},
    {"nct_id":"NCT04557098","drug":"Teclistamab","sponsor":"J&J","cancer_type":"Myeloma","phase":"III","moa":"Bispecific (BCMAxCD3)","primary_endpoint":"PFS","enrollment":590,"start_year":2021,"est_completion":2025,"status":"Recruiting","biomarker":"RRMM (3+ prior lines)","combo":"vs Physician's choice","idn_potential":"Very High"},
    {"nct_id":"NCT03478891","drug":"Olutasidenib","sponsor":"Forma/Novo Nordisk","cancer_type":"Leukemia","phase":"III","moa":"IDH1 Inhibitor","primary_endpoint":"CR+CRh","enrollment":372,"start_year":2019,"est_completion":2024,"status":"Completed","biomarker":"IDH1 mutant AML","combo":"Monotherapy","idn_potential":"Moderate"},
    {"nct_id":"NCT05119088","drug":"Mirvetuximab soravtansine","sponsor":"ImmunoGen/AbbVie","cancer_type":"Ovarian","phase":"III","moa":"ADC (FRα)","primary_endpoint":"PFS","enrollment":453,"start_year":2021,"est_completion":2025,"status":"Active, not recruiting","biomarker":"FRα high OC","combo":"vs Investigator's choice","idn_potential":"Very High"},
    {"nct_id":"NCT04552223","drug":"Fianlimab","sponsor":"Regeneron","cancer_type":"Melanoma","phase":"III","moa":"LAG-3 Inhibitor","primary_endpoint":"PFS","enrollment":706,"start_year":2021,"est_completion":2025,"status":"Recruiting","biomarker":"Untreated Melanoma","combo":"+ Cemiplimab","idn_potential":"High"},
])

# ─── Physician Adoption Curves ─────────────────────────────────────────────
def get_adoption_data():
    rows = []
    drugs_subset = FDA_DRUGS[["drug","brand","cancer_type","approval_year","market_share_pct"]].head(12)
    for _, row in drugs_subset.iterrows():
        base = row["market_share_pct"]
        for month in range(0, 37, 3):
            # Sigmoid-like adoption
            pct = base * (1 / (1 + np.exp(-0.15 * (month - 12)))) * np.random.uniform(0.92, 1.08)
            rows.append({
                "drug": row["drug"],
                "brand": row["brand"],
                "cancer_type": row["cancer_type"],
                "month": month,
                "adoption_pct": round(min(pct, base * 1.05), 1)
            })
    return pd.DataFrame(rows)

# ─── Revenue Forecast ─────────────────────────────────────────────────────
def get_forecast_data(cancer_filter=None):
    rows = []
    df = FDA_DRUGS.copy()
    if cancer_filter:
        df = df[df["cancer_type"].isin(cancer_filter)]
    for _, row in df.iterrows():
        peak = row["peak_sales_b"]
        launch_yr = row["approval_year"]
        for yr in range(launch_yr, 2030):
            age = yr - launch_yr
            # Revenue ramp then LOE
            if age <= 2:
                rev = peak * (0.15 + 0.35 * age)
            elif age <= 5:
                rev = peak * (0.85 + 0.03 * (age - 2))
            elif age <= 8:
                rev = peak * (0.94 - 0.05 * (age - 5))  # patent pressure
            else:
                rev = peak * 0.4 * (0.85 ** (age - 8))  # biosimilar/generic
            noise = np.random.uniform(0.93, 1.07)
            rows.append({
                "drug": row["drug"],
                "brand": row["brand"],
                "company": row["company"],
                "cancer_type": row["cancer_type"],
                "year": yr,
                "revenue_b": round(rev * noise, 3),
                "is_forecast": yr >= 2025
            })
    return pd.DataFrame(rows)

# ─── Market Opportunity ────────────────────────────────────────────────────
MARKET_OPPORTUNITY = pd.DataFrame([
    {"cancer_type":"Breast",       "tam_b":24.1,"sam_b":14.8,"som_b":6.2,"cagr_pct":8.4,"key_driver":"CDK4/6 + ADC expansion"},
    {"cancer_type":"Lung (NSCLC)", "tam_b":21.8,"sam_b":16.3,"som_b":7.8,"cagr_pct":11.2,"key_driver":"Biomarker-driven TKIs + IO"},
    {"cancer_type":"Lung (SCLC)",  "tam_b":4.1, "sam_b":2.9, "som_b":1.1,"cagr_pct":14.1,"key_driver":"BiTE antibodies (DLL3)"},
    {"cancer_type":"CRC",          "tam_b":12.6,"sam_b":7.4, "som_b":2.9,"cagr_pct":6.8,"key_driver":"KRAS G12C + MSI-H IO"},
    {"cancer_type":"Leukemia",     "tam_b":18.4,"sam_b":11.7,"som_b":5.4,"cagr_pct":9.3,"key_driver":"BTK 2nd gen + BCL-2"},
    {"cancer_type":"Lymphoma",     "tam_b":15.2,"sam_b":9.8, "som_b":4.1,"cagr_pct":12.8,"key_driver":"CAR-T + Bispecifics"},
    {"cancer_type":"Myeloma",      "tam_b":22.7,"sam_b":14.3,"som_b":6.8,"cagr_pct":10.6,"key_driver":"BCMA bispecifics + ADCs"},
    {"cancer_type":"Ovarian",      "tam_b":7.3, "sam_b":4.6, "som_b":1.8,"cagr_pct":9.1,"key_driver":"PARP + ADC (FRα)"},
    {"cancer_type":"Melanoma",     "tam_b":9.8, "sam_b":6.4, "som_b":2.9,"cagr_pct":7.2,"key_driver":"IO combos + LAG-3"},
])

CMS_DATA = get_cms_data()
ADOPTION_DATA = get_adoption_data()
