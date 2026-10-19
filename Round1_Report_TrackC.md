# ARGUS: Autonomous Financial Discovery Agent
**Track C — Consumer, FMCG & Retail**  
**Round 1 Solution Pitch & Architecture** | Team: Who cares  
**Deliverables:** [GitHub Repository](https://github.com/CYCLOTRON999/ARGUS-Financial-Discovery-Agent) | [2-Minute Demo Video](https://drive.google.com/file/d/10lt3R-c5_Bp3dLwjYmn5JHsBGtueg4HE/view?usp=sharing)

> **"ARGUS autonomously investigates public filings, tests competing explanations, and produces auditable financial discoveries."**

---

## PAGE 1: THE BREAKTHROUGH, HOW IT THINKS, & SECTOR INTELLIGENCE

### 1. The Core Problem: Why AI Summarizers Miss the Real Story
Every standard AI finance tool today is a passive summarizer. You feed it a 30-page quarterly earnings call, and it highlights what management chose to say. 

The fundamental problem? **Corporate executives are paid to present the most optimistic narrative.** The real financial story is almost never found in speeches or press releases; it is hidden in the gap between:
1. What management claims on the earnings call (the narrative),
2. What the audited balance sheet footnotes and cash flows disclose (the economic reality), and
3. What competing companies and suppliers in the same sector report at the exact same time.

**ARGUS is not a chatbot, a summarizer, or a stock broker.** It issues no buy/sell ratings or price targets. Instead, it operates like an autonomous investigative journalist. Given any company in Consumer, FMCG & Retail, ARGUS independently investigates public records, derives hard mathematical relationships, stress-tests its own findings against counter-arguments, and produces an auditable, non-obvious discovery.

---

### 2. How the System Thinks: The 5-Step Autonomous Workflow

```
[ Company Ticker (e.g. DABUR / TRENT) ]
                   │
                   ▼
1. HYPOTHESIZE ──► Selects smart investigative angles (Sales Quality, Channel Health)
                   │
                   ▼
2. HARVEST     ──► Pulls public reports, 12 quarters of statements, concalls & peers
                   │
                   ▼
3. CALCULATE   ──► Deterministic Python math (DSO, YoY growth, Price vs. Volume)
                   │
                   ▼
4. RED-TEAM    ──► Plays Devil's Advocate: hunts for alternative macro explanations
                   │
                   ▼
5. PROVE       ──► Produces a verified, 3-source evidence trail with a disproof rule
```

* **Step 1: Hypothesize (Deciding What to Investigate)**  
  Instead of aimless search, ARGUS tests established financial vulnerability angles: *Is revenue growth coming from selling more units, or just hiking prices? Are distributors taking longer to pay? Are new store openings masking weaker sales at older stores?*
* **Step 2: Autonomous Public Data Harvesting**  
  ARGUS locates public documents without pre-cleaned datasets: 12 quarters of P&L and Balance Sheet tables, investor presentations, BSE earnings call transcripts, and peer disclosures.
* **Step 3: Deterministic Math (No AI Math Hallucinations)**  
  A major trap in AI finance is letting language models calculate numbers in their prompt. ARGUS forces a dedicated Python code engine to do 100% of the arithmetic. Every percentage, ratio, and growth rate is mathematically verified with a direct calculation trail.
* **Step 4: The Red-Team Challenge (Self-Falsification)**  
  Before confirming any finding, a dedicated adversarial module asks: *"Could this be explained by an industry-wide raw material price surge or a bad monsoon rather than company failure?"*
* **Step 5: Auditable 8-Point Synthesis**  
  ARGUS formats its conclusion into an 8-element standard report where every claim links directly to primary sources.

---

### 3. Company-Agnostic Research: Eligible Track C Universe
The research pipeline uses company-agnostic analysis rules for eligible NIFTY 50 companies in Track C. It can extend to other consumer-sector peers where permitted and where comparable public data is available:

* **For Factory Brands / FMCG Makers (e.g., Hindustan Unilever, Britannia, Dabur, Marico, Nestle, Bikaji):**
  * *The Price vs. Volume Test:* Separates top-line revenue into price hikes vs. actual volume of goods sold.
  * *The Channel Stuffing Test:* Tracks Distributor Receivable Days (DSO). If sales are rising but distributors take longer to pay, goods are sitting unsold on distributor shelves.
* **For Retail Stores & Jewellery (e.g., Trent, Titan, Avenue Supermarts / DMart, V2 Retail):**
  * *The Metric Fallback:* Retailers do not report volume in kilograms or cases. ARGUS tracks whether opening new stores creates an illusion of growth while older stores experience maturing sales throughput.

---

## PAGE 2: EVIDENCE TRIANGULATION, COUNTERARGUMENT & ROADMAP

### 4. Evidence Triangulation: How Claims are Fact-Checked
Claims are cross-checked against independent public sources, financial filings and peer or industry evidence where available. Missing evidence and unresolved contradictions are explicitly reported:
1. **Leg 1 (Leadership Story):** Management's public claim from an investor presentation or concall transcript (e.g., *"Demand is accelerating across our retail network"*).
2. **Leg 2 (Audited Math):** Audited financial figures from regulatory filings (e.g., *Balance sheet shows inventory expansion of +68.2% / ₹2,289 Cr locking up working capital*).
3. **Leg 3 (Industry Rivals):** Reports from direct competitors or sector data for the same quarter where available (e.g., *Peer disclosures show steady inventory velocity, indicating that inventory stretch is company-specific rather than a macro slowdown*).

---

### 5. Counterargument & Falsification: Testing if We Are Wrong
A core reason financial analysts make mistakes is confirmation bias—finding data that only supports their initial hunch. ARGUS eliminates this by embedding two mandatory checks:
* **The Strongest Counterargument (Devil's Advocate):** The system actively searches for legitimate alternative explanations (e.g., *"Did inventory rise because management bought inventory early to support new store openings or protect against upcoming inflation?"*).
* **The Falsification Condition (Measurable & Time-Bound):** ARGUS explicitly states the exact future milestone that would disprove its theory (e.g., *"This finding is falsified if the company achieves two consecutive quarters of >8% sales growth with stock turnover returning below 50 days"*).

---

### 6. Single Output Format: Interactive Dashboard
**Chosen Format:** **Interactive Financial Research Dashboard** (Single unified interface featuring inline SVG trend charts, metric cards, and auditable primary document ledger, with built-in one-click `@media print` Executive Memo export for PDF/print generation). It rigorously embeds all **8 Mandatory Discovery Elements**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. THE DISCOVERY (Illustrative example — not a verified company finding):
│    Trent Ltd reports headline revenue expansion (+16.9% YoY), yet growth
│    is driven by new store additions while network inventory expanded +68.2%
│    (₹2,289 Cr), masking maturing sales productivity at older locations.
│ 2. WHY IT MATTERS: 3-5 bullets on operational & economic sustainability.
│ 3. THE NUMBERS: Verified calculations (Growth +16.9%, Stock Days 61.2d).
│ 4. THE TIMELINE: When the shift started and how it unfolded over time.
│ 5. EVIDENCE TRAIL: Traceable, clickable links to exact filing passages.
│ 6. COUNTERARGUMENT: The strongest alternative or macro explanation.
│ 7. FALSIFICATION CONDITION: Exact future metrics that disprove this.
│ 8. EVIDENCE STRENGTH: [Strong / Moderate / Weak] with rationale.
└────────────────────────────────────────────────────────────────────────┘
```
*Zero buy/sell recommendations, zero stock tips. Pure, verifiable corporate reality.*

---

### 7. Build Plan & Milestones to 25 Oct

* **Oct 19, 2026 (Today) — BUILT & TESTED:**  
  Automates source collection, deterministic calculations and evidence-based hypothesis testing, with explicit handling of missing or conflicting data. Full 8-element interactive dashboard with company selection, SVG trend visuals, and printable memo.
  * **GitHub Repository:** [https://github.com/CYCLOTRON999/ARGUS-Financial-Discovery-Agent](https://github.com/CYCLOTRON999/ARGUS-Financial-Discovery-Agent)
  * **2-Minute Demo Video:** [https://drive.google.com/file/d/10lt3R-c5_Bp3dLwjYmn5JHsBGtueg4HE/view?usp=sharing](https://drive.google.com/file/d/10lt3R-c5_Bp3dLwjYmn5JHsBGtueg4HE/view?usp=sharing)

* **Oct 20–21 — IN PROGRESS:**  
  Deeper concall parsing: Ingest full-text PDF concalls to extract direct speaker quotes and executive statements with high-speed local keyword search.

* **Oct 22–23 — PLANNED:**  
  Broader peer scraping: Expand automated cross-referencing from 3 peers to 10+ mid-cap retail and FMCG peers for industry-wide triangulation where public data permits.

* **Oct 24–25 — PLANNED:**  
  Finals live presentation preparation and stress-testing across all eligible consumer companies. Deliver a live 10-minute demonstration on whichever company the judges select on the spot.
