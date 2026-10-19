# ARGUS: Autonomous Financial Research Agent (ATMOS 2026)
**Track C — Consumer, FMCG & Retail**  
**Team: Who cares** | **Deliverables:** [GitHub Repository](https://github.com/CYCLOTRON999/ARGUS-Financial-Discovery-Agent) &bull; [2-Minute Demo Video](https://www.loom.com/share/argus-financial-agent-demo)

ARGUS is an autonomous financial research agent that uncovers non-obvious, evidence-backed financial discoveries across Indian Consumer, FMCG, and Retail companies. It replaces passive AI summarizers with an active investigative workflow that cross-checks corporate narratives against audited financial realities and sector benchmarks.

---

## Key Capabilities

* **Interactive Research Dashboard:** Single-screen dashboard with inline SVG trend charts, metric cards, and auditable primary document ledger.
* **8 Selectable Company Profiles:**
  * **Core Track C (6 Companies):** Hindustan Unilever (`HINDUNILVR`), Britannia (`BRITANNIA`), Tata Consumer (`TATACONSUM`), Nestle India (`NESTLEIND`), Dabur (`DABUR`), Trent (`TRENT`).
  * **Broader Consumer-Retail (2 Companies):** Titan Company (`TITAN`), Asian Paints (`ASIANPAINT`).
* **Generic On-The-Spot Judge Investigation:** Works out of the box on **any** listed company selected by judges, including non-NIFTY 50 tie-breakers (`V2RETAIL`, `BIKAJI`, `DMART`), with zero company-specific hardcoding.
* **Zero Math Hallucination:** 100% deterministic Python math engine for YoY growth, Days Sales Outstanding (DSO), and Days Inventory Outstanding (DIO).
* **Three-Legged Triangulation:** Every claim is verified across at least 3 independent sources: Audited Financial Statements, BSE India Concall Transcripts, and Competitor Peer Disclosures.
* **Dedicated Red-Team Adversary:** Actively formulates macroeconomic counterarguments and an explicit, measurable, time-bound falsification condition (*"Two consecutive quarters of..."*).
* **Zero Investment Recommendations:** 100% public data, zero stock price targets, and no buy/sell ratings.

---

## Architecture Flow

```
[ Ticker Input (e.g. HINDUNILVR, TRENT, or Any Custom Ticker) ]
                  │
                  ▼
 1. Public Harvester      ──► Scrapes Screener.in & BSE India for 12 quarters
                  │
 2. Financial Calculator  ──► Computes YoY growth, DSO, DIO & inventory in Python
                  │
 3. Investigator Engine   ──► Detects narrative vs numbers divergence
                  │
 4. Red-Team Adversary    ──► Formulates counterargument & falsification rule
                  │
 5. Report Generator      ──► Produces 8-element terminal log, JSON & HTML dashboard
```

---

## Quickstart

### Prerequisites
* Python 3.9+
* `requests` library

```bash
git clone https://github.com/CYCLOTRON999/ARGUS-Financial-Discovery-Agent.git
cd ARGUS-Financial-Discovery-Agent
pip install requests
```

### 1. Run the Interactive Streamlit Web App (Local or Cloud)
Launch the Streamlit app locally:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

#### ☁️ 1-Click Streamlit Cloud Deployment:
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Select repository: `CYCLOTRON999/ARGUS-Financial-Discovery-Agent`.
3. Main file path: `streamlit_app.py`.
4. Click **Deploy!**

### 2. View the Standalone HTML Dashboard
Open the standalone interactive dashboard with all 8 selectable profiles in your browser:

```bash
open dashboard.html
```

### 3. Run an Autonomous Investigation for Any Ticker
Run the generic pipeline on any NIFTY 50 or non-NIFTY 50 stock:

```bash
# Core Track C FMCG:
python3 main.py HINDUNILVR
python3 main.py DABUR
python3 main.py BRITANNIA

# Core Track C Retail:
python3 main.py TRENT

# Broader Consumer-Retail:
python3 main.py TITAN
python3 main.py ASIANPAINT

# Non-NIFTY 50 Tie-Breakers:
python3 main.py V2RETAIL
python3 main.py BIKAJI
```

### 4. Launch the Zero-Dependency Judge Server (Optional)
To investigate any company live on the spot from the web interface:

```bash
python3 server.py
# Open http://localhost:8000 in your browser
```

---

## Required 8-Element Output Schema

1. **The Discovery:** One concise sentence summarizing the non-obvious finding.
2. **Why It Matters:** Exactly 3–5 bullet points analyzing operational and financial durability.
3. **Verified Numbers:** Mathematically validated metrics and inline SVG charts with tracked provenance.
4. **Timeline:** Chronological evolution of the trend over 8–13 quarters.
5. **Evidence Trail:** Direct, clickable links to audited statements, BSE concalls, and peer filings.
6. **Strongest Counterargument:** The Red-Team's macroeconomic and sector-wide defense.
7. **Falsification Condition:** Explicit, measurable future benchmarks that would disprove the thesis.
8. **Evidence Strength:** Categorized as Strong, Moderate, or Weak with full 4-dimension rubric breakdown.

---

## Deliverables
* **Submission Pitch PDF:** `WhoCares_TrackC_Round1.pdf`
* **Streamlit Web Application:** `streamlit_app.py` & `requirements.txt`
* **Interactive Dashboard:** `dashboard.html`
* **Primary Python Agent:** `main.py`, `investigator.py`, `harvester.py`, `calculator.py`

