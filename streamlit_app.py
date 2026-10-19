import streamlit as st
import json
import os
import pandas as pd
from typing import Dict, Any, Optional

# Set Page Config
st.set_page_config(
    page_title="ARGUS: Autonomous Financial Discovery Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Financial Research UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff !important;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        border: 1px solid #334155;
    }
    .track-tag {
        background: #0284c7;
        color: #ffffff !important;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: inline-block;
        margin-bottom: 8px;
    }
    .discovery-box {
        background: #062b1f !important;
        border: 1px solid #047857 !important;
        border-left: 6px solid #10b981 !important;
        padding: 18px 22px;
        border-radius: 8px;
        margin: 16px 0;
        font-size: 15.5px;
        line-height: 1.65;
        color: #ecfdf5 !important;
    }
    .discovery-box strong {
        color: #6ee7b7 !important;
        font-size: 16px;
    }
    .metric-card {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        color: #f8fafc !important;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 800;
        color: #ffffff !important;
    }
    .metric-label {
        font-size: 11px;
        font-weight: 600;
        color: #94a3b8 !important;
        text-transform: uppercase;
        margin-top: 4px;
    }
    .counter-box {
        background: #2a1215 !important;
        border: 1px solid #7f1d1d !important;
        border-left: 5px solid #ef4444 !important;
        padding: 18px 20px;
        border-radius: 8px;
        margin-bottom: 12px;
        color: #fecdd3 !important;
        font-size: 14.5px;
        line-height: 1.6;
    }
    .counter-box strong {
        color: #fda4af !important;
        font-size: 15px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .falsify-box {
        background: #0f291e !important;
        border: 1px solid #166534 !important;
        border-left: 5px solid #22c55e !important;
        padding: 18px 20px;
        border-radius: 8px;
        margin-bottom: 12px;
        color: #dcfce7 !important;
        font-size: 14.5px;
        line-height: 1.6;
    }
    .falsify-box strong {
        color: #86efac !important;
        font-size: 15px;
        display: inline-block;
        margin-bottom: 6px;
    }
    .evidence-card {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        color: #f8fafc !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper: Load all pre-computed reports
@st.cache_data
def load_all_reports() -> Dict[str, Any]:
    json_path = os.path.join(os.path.dirname(__file__), "all_reports.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

reports_data = load_all_reports()

# Header Banner
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span class="track-tag">Track C: Consumer, FMCG & Retail</span>
        <span style="font-size: 13px; color: #94a3b8; font-weight: 600;">Team: <strong>Who cares</strong> &bull; ATMOS 2026</span>
    </div>
    <h1 style="margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.02em;">ARGUS: Autonomous Financial Discovery Agent</h1>
    <p style="margin: 6px 0 0 0; font-size: 15px; color: #38bdf8; font-weight: 500;">
        The agent finds where reported company growth separates from real business reality, then proves or disproves it.
    </p>
    <div style="margin-top: 14px; font-size: 13px; display: flex; gap: 18px;">
        <a href="https://github.com/CYCLOTRON999/ARGUS-Financial-Discovery-Agent" target="_blank" style="color: #60a5fa; text-decoration: none; font-weight: 600;">⭐ GitHub Repository</a>
        <a href="https://www.loom.com/share/argus-financial-agent-demo" target="_blank" style="color: #60a5fa; text-decoration: none; font-weight: 600;">🎥 2-Minute Demo Video</a>
        <span style="color: #94a3b8;">Round 1 Submission Package</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Company Categories
CORE_TRACK_C = [
    ("HINDUNILVR", "Hindustan Unilever Ltd", "FMCG / Staples"),
    ("BRITANNIA", "Britannia Industries Ltd", "Packaged Foods"),
    ("TATACONSUM", "Tata Consumer Products Ltd", "Beverages & Foods"),
    ("NESTLEIND", "Nestle India Ltd", "FMCG / Dairy"),
    ("DABUR", "Dabur India Ltd", "Ayurvedic & FMCG"),
    ("TRENT", "Trent Ltd (Westside / Zudio)", "Retail Apparel"),
]

BROADER_CONSUMER = [
    ("TITAN", "Titan Company Ltd (Tanishq / Fastrack)", "Jewellery & Watches"),
    ("ASIANPAINT", "Asian Paints Ltd", "Paints & Home Decor"),
]

OTHER_PEERS = [
    ("DMART", "Avenue Supermarts Ltd (DMart)", "Grocery Retail"),
    ("V2RETAIL", "V2 Retail Ltd", "Value Fashion Retail"),
    ("BIKAJI", "Bikaji Foods International Ltd", "Ethnic Snacks"),
    ("ITC", "ITC Ltd", "Diversified FMCG"),
]

# Company Selection Controls
col_mode, col_select = st.columns([1, 2])

with col_mode:
    selection_mode = st.radio(
        "Selection Mode:",
        ["Choose from the company list", "Search by company name or NSE symbol"],
        index=0,
        label_visibility="collapsed"
    )

selected_ticker = "HINDUNILVR"

if selection_mode == "Choose from the company list":
    with col_select:
        options = []
        labels_map = {}
        
        # Populate categorized options
        for t, name, desc in CORE_TRACK_C:
            opt = f"{t} — {name} [Core Track C]"
            options.append(opt)
            labels_map[opt] = t
            
        for t, name, desc in BROADER_CONSUMER:
            opt = f"{t} — {name} [Broader Consumer-Retail]"
            options.append(opt)
            labels_map[opt] = t
            
        for t, name, desc in OTHER_PEERS:
            opt = f"{t} — {name} [Peer Tie-Breaker]"
            options.append(opt)
            labels_map[opt] = t
            
        selected_option = st.selectbox(
            "Select Company to Inspect:",
            options,
            index=0,
            help="Choose from 8 eligible Track C companies or regional consumer peers"
        )
        selected_ticker = labels_map[selected_option]

else:
    with col_select:
        sub_c1, sub_c2 = st.columns([3, 1])
        with sub_c1:
            custom_input = st.text_input(
                "Enter NSE Symbol / Ticker:",
                value="TRENT",
                help="E.g. HINDUNILVR, BRITANNIA, TRENT, MARICO, COLPAL, GODREJCP"
            ).upper().strip()
        with sub_c2:
            st.write("")
            st.write("")
            run_btn = st.button("🚀 Investigate", use_container_width=True)
            
        selected_ticker = custom_input if custom_input else "HINDUNILVR"

# Fetch Report Data
report = reports_data.get(selected_ticker)

# If ticker not in pre-computed reports, run live investigator
if not report:
    st.info(f"Ticker `{selected_ticker}` is not pre-cached. Running live autonomous investigation...")
    try:
        from investigator import FinancialInvestigator
        with st.spinner(f"Investigating public filings and concall data for {selected_ticker}..."):
            inv = FinancialInvestigator(selected_ticker)
            report = inv.run_investigation()
            if "error" in report:
                st.error(report["error"])
                report = None
    except Exception as e:
        st.error(f"Error running autonomous investigation: {e}")
        report = None

if report:
    company_name = report.get("company_name", selected_ticker)
    ticker = report.get("ticker", selected_ticker)
    b_model = report.get("business_model", "Consumer Company")
    strength = report.get("element_8_evidence_strength", {}).get("rating", "Moderate")
    
    badge_bg = "#064e3b" if strength.lower() == "strong" else "#78350f"
    badge_border = "#10b981" if strength.lower() == "strong" else "#f59e0b"
    badge_color = "#6ee7b7" if strength.lower() == "strong" else "#fde68a"
    
    # Meta header bar
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid rgba(148, 163, 184, 0.25); padding-bottom: 12px; margin-top: 14px; margin-bottom: 20px;">
        <div>
            <h2 style="margin: 0; font-size: 26px; font-weight: 800; color: #ffffff !important; letter-spacing: -0.01em;">{company_name} <span style="color: #38bdf8;">({ticker})</span></h2>
            <span style="font-size: 13.5px; color: #94a3b8 !important; font-weight: 600;">Model: <strong style="color: #e2e8f0;">{b_model}</strong> &bull; Output: 8-Element Discovery Schema</span>
        </div>
        <div>
            <span style="background: {badge_bg}; border: 1px solid {badge_border}; color: {badge_color} !important; padding: 5px 14px; border-radius: 9999px; font-size: 12px; font-weight: 800; letter-spacing: 0.03em;">
                Evidence Strength: {strength.upper()}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Tabs
    tab_discovery, tab_dashboard, tab_submission, tab_export = st.tabs([
        "🔍 Verified Discovery (8 Elements)",
        "🖥️ Standalone HTML Dashboard",
        "📄 Round 1 Submission Pitch (2 Pages)",
        "💾 Export Data & Memo"
    ])
    
    with tab_discovery:
        # Element 1: The Discovery
        st.markdown("#### 1. The Discovery (Quantified Core Finding)")
        discovery_text = report.get("element_1_the_discovery", "")
        st.markdown(f"""
        <div class="discovery-box">
            <strong>Finding:</strong> {discovery_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Element 2: Why It Matters
        st.markdown("#### 2. Why It Matters (Operational & Economic Durability)")
        bullets = report.get("element_2_why_it_matters", [])
        for b in bullets:
            st.markdown(f"&bull; {b}")
            
        st.markdown("---")
        
        # Element 3: The Numbers & Inline Chart
        st.markdown("#### 3. Key Numbers & Deterministic Calculations")
        numbers = report.get("element_3_numbers", {})
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            avg_growth = numbers.get("latest_4q_avg_sales_growth_pct", 0)
            st.metric("4Q Avg Sales Growth", f"{avg_growth:+.1f}%")
        with m2:
            dso = numbers.get("dso_recent_days", 0)
            dso_chg = numbers.get("dso_pct_change", 0)
            st.metric("DSO (Trade Debtor Days)", f"{dso:.1f} days", f"{dso_chg:+.1f}%")
        with m3:
            dio = numbers.get("dio_recent_days", 0)
            dio_chg = numbers.get("dio_pct_change", 0)
            st.metric("DIO (Inventory Days)", f"{dio:.1f} days", f"{dio_chg:+.1f}%")
        with m4:
            q_cnt = numbers.get("quarters_analyzed_count", 13)
            st.metric("Quarters Harvested", f"{q_cnt} Quarters", "Audited")
            
        # Chart Data
        chart_data = report.get("chart_data", {})
        quarters = chart_data.get("quarters", [])
        sales_cr = chart_data.get("sales_cr", [])
        yoy_pct = chart_data.get("yoy_growth_pct", [])
        
        if quarters and sales_cr:
            st.write("")
            chart_df = pd.DataFrame({
                "Quarter": quarters,
                "Sales (₹ Cr)": sales_cr,
                "YoY Growth (%)": yoy_pct
            }).set_index("Quarter")
            
            c_chart1, c_chart2 = st.columns(2)
            with c_chart1:
                st.caption("📈 Reported Quarterly Revenue (₹ Crores)")
                st.bar_chart(chart_df["Sales (₹ Cr)"], color="#0284c7")
            with c_chart2:
                st.caption("📊 YoY Growth Rate (%)")
                st.line_chart(chart_df["YoY Growth (%)"], color="#16a34a")
                
        st.markdown(f"<span style='font-size: 11px; color: #64748b;'><em>Provenance: {numbers.get('calculation_provenance', 'Python FinancialCalculator')}</em></span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Element 4: Timeline
        st.markdown("#### 4. Evolution Timeline")
        timeline = report.get("element_4_timeline", [])
        for t in timeline:
            st.markdown(f"&bull; **{t}**")
            
        st.markdown("---")
        
        # Element 5: Evidence Trail
        st.markdown("#### 5. Evidence Trail (Three-Legged Triangulation)")
        st.caption("Every finding is cross-checked against independent public sources, audited filings, and peer data where available.")
        
        evidence = report.get("element_5_evidence_trail", [])
        for idx, ev in enumerate(evidence, 1):
            with st.expander(f"Leg {idx}: {ev.get('source_type', 'Source')} — {ev.get('document_title', 'Document')}", expanded=True):
                st.markdown(f"**Publication Period / Date:** {ev.get('publication_date', 'N/A')}")
                st.markdown(f"**Section / Page:** {ev.get('section_or_page', 'N/A')}")
                st.markdown(f"**Verified Passage / Figure:** *\"{ev.get('exact_figure_or_passage', 'N/A')}\"*")
                link = ev.get('source_link') or ev.get('url')
                if link:
                    st.markdown(f"🔗 [Open Original Regulatory Document / Filing]({link})")
                    
        st.markdown("---")
        
        # Element 6 & 7: Counterargument & Falsification
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown("#### 6. Strongest Counterargument (Devil's Advocate)")
            counter = report.get("element_6_counterargument", "")
            st.markdown(f"""
            <div class="counter-box">
                <strong>Alternative Explanation:</strong><br>{counter}
            </div>
            """, unsafe_allow_html=True)
            
        with c_right:
            st.markdown("#### 7. Falsification Condition (Disproof Rule)")
            falsify = report.get("element_7_falsification_condition", "")
            st.markdown(f"""
            <div class="falsify-box">
                <strong>Disproof Milestone:</strong><br>{falsify}
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Element 8: Evidence Strength Breakdown
        st.markdown("#### 8. Evidence Strength & Rubric Audit")
        strength_info = report.get("element_8_evidence_strength", {})
        st.markdown(f"**Overall Rating:** `{strength_info.get('rating', 'Moderate')}` &mdash; {strength_info.get('rationale', '')}")
        
        rubric = strength_info.get("rubric_breakdown", {})
        r_cols = st.columns(4)
        
        rubric_items = [
            ("Triangulation", rubric.get("multi_source_triangulation", {})),
            ("Deterministic Math", rubric.get("mathematical_reproducibility", {})),
            ("Primary Fidelity", rubric.get("primary_source_fidelity", {})),
            ("Falsifiability", rubric.get("falsifiability_coverage", {}))
        ]
        
        for c, (title, data) in zip(r_cols, rubric_items):
            with c:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 13px; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.04em;">{title}</div>
                    <div style="font-size: 13px; font-weight: 700; color: #ffffff !important; margin: 6px 0;">{data.get('score', 'Pass')}</div>
                    <div style="font-size: 11.5px; color: #cbd5e1 !important; line-height: 1.45;">{data.get('detail', '')}</div>
                </div>
                """, unsafe_allow_html=True)

    with tab_dashboard:
        st.markdown("#### Embedded Interactive Dashboard View")
        st.caption("Full responsive dashboard featuring inline SVG visuals, real-time calculations, and one-click Executive Memo printing.")
        
        dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.html")
        if os.path.exists(dashboard_path):
            with open(dashboard_path, "r", encoding="utf-8") as f:
                dashboard_html = f.read()
            st.components.v1.html(dashboard_html, height=1000, scrolling=True)
        else:
            st.warning("`dashboard.html` not found.")

    with tab_submission:
        st.markdown("#### Round 1 Submission Pitch (2-Page PDF)")
        st.caption("Official Track C Pitch Document: Concept, 5-Step Architecture, Triangulation, and Roadmap.")
        
        pdf_path = os.path.join(os.path.dirname(__file__), "WhoCares_TrackC_Round1.pdf")
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="📥 Download Submission Pitch PDF (WhoCares_TrackC_Round1.pdf)",
                data=pdf_bytes,
                file_name="WhoCares_TrackC_Round1.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
        st.markdown("""
        ##### PDF Architecture Summary:
        - **Page 1:** The Breakthrough (Why AI summarizers fail), Stack & Architecture (Deterministic Math, Screener.in, BSE Concalls), 5-Step Process, and Company-Agnostic Track C Universe (FMCG Brands vs Retail Non-Volume Disclosers).
        - **Page 2:** Evidence Triangulation (3-Legged Model), Self-Falsification (Devil's Advocate + Disproof Rule), Single Interactive Dashboard Wireframe (All 8 Elements), and Build Plan & Milestones to Oct 25.
        """)

    with tab_export:
        st.markdown("#### Export Discovery Report")
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            st.markdown("##### Download JSON Data")
            json_str = json.dumps(report, indent=2)
            st.download_button(
                label=f"📥 Download {ticker}_Discovery.json",
                data=json_str,
                file_name=f"{ticker}_Discovery.json",
                mime="application/json",
                use_container_width=True
            )
            
        with col_exp2:
            st.markdown("##### Download Markdown Memo")
            md_content = f"""# ARGUS Discovery Memo: {company_name} ({ticker})
**Track C: Consumer, FMCG & Retail** | Team: Who cares

## 1. The Discovery
{discovery_text}

## 2. Why It Matters
{chr(10).join(f"- {b}" for b in bullets)}

## 3. Key Numbers
- 4Q Avg Sales Growth: {avg_growth:+.1f}%
- DSO (Receivable Days): {dso:.1f} days ({dso_chg:+.1f}%)
- DIO (Inventory Days): {dio:.1f} days ({dio_chg:+.1f}%)

## 4. Timeline
{chr(10).join(f"- {t}" for t in timeline)}

## 5. Counterargument & Falsification
- **Counterargument:** {counter}
- **Falsification Condition:** {falsify}

## 6. Evidence Rating
- **Strength:** {strength}
"""
            st.download_button(
                label=f"📥 Download {ticker}_Memo.md",
                data=md_content,
                file_name=f"{ticker}_Memo.md",
                mime="text/markdown",
                use_container_width=True
            )

# Sidebar
with st.sidebar:
    st.markdown("### ⚡ ARGUS Research Agent")
    st.markdown("""
    **Track C: Consumer, FMCG & Retail**  
    **Hackathon:** ATMOS 2026 (BITS Pilani)  
    **Team:** Who cares  
    **Lead Author:** Abhay Singh & Team  
    """)
    
    st.markdown("---")
    st.markdown("### 🛠️ Core Technology")
    st.markdown("""
    - **Data Harvester:** Scrapes 12-13 quarters of P&L, balance sheet notes & concalls from Screener & BSE India.
    - **Math Engine:** 100% deterministic Python arithmetic (0% AI math error).
    - **Investigator:** Detects narrative-vs-numbers divergence.
    - **Adversary:** Stress-tests findings against macro counter-theses.
    - **Output:** Strict 8-Element auditable schema.
    """)
    
    st.markdown("---")
    st.markdown("### 📌 Important Rules")
    st.markdown("""
    - **Zero Stock Tips:** No buy/sell ratings or price targets.
    - **100% Free Public Data:** No login credentials or paid terminals.
    - **Company-Agnostic:** Works on any listed consumer ticker.
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("""
    - [GitHub Code Repository](https://github.com/CYCLOTRON999/ARGUS-Financial-Discovery-Agent)
    - [2-Minute Loom Demo](https://www.loom.com/share/argus-financial-agent-demo)
    - [PDF Submission Pitch](https://github.com/CYCLOTRON999/ARGUS-Financial-Discovery-Agent/blob/main/WhoCares_TrackC_Round1.pdf)
    """)
