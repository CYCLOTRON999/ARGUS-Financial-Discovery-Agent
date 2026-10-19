# ARGUS: Autonomous Financial Discovery Agent
**Track C — Consumer, FMCG & Retail**  
**Round 1 Solution Pitch & Architecture** | Team: [Your Team Name]  
**Deliverables:** [GitHub Repository](https://github.com/CYCLOTRON999/ARGUS-Financial-Discovery-Agent) | [2-Minute Loom Demo Video](https://www.loom.com/share/argus-financial-agent-demo)

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

### 3. Sector-Wide Generalization: Handling FMCG & Retail Without Hardcoding
The system contains **zero company-specific logic**. It does not look for specific brand names or pre-written rules. It dynamically identifies whether the company is a **Brand Manufacturer (FMCG)** or a **Retail Chain**, and automatically applies the appropriate investigative lens:

* **For FMCG Manufacturers (e.g., Dabur, Hindustan Unilever, Britannia, Marico):**
  * *The Price vs. Volume Test:* Separates top-line revenue into price hikes vs. actual volume of goods sold.
  * *The Channel Stuffing Test:* Tracks Distributor Receivable Days (DSO). If sales are rising but distributors take longer to pay, goods are sitting unsold on distributor shelves.
* **For Retail Chains (e.g., Trent, Avenue Supermarts / DMart, Shoppers Stop):**
  * *The Metric Fallback:* Retailers do not report volume in kilograms or cases. ARGUS automatically falls back to **Same-Store Sales Growth (SSSG)**, **Store Expansion vs. Revenue**, and **Revenue per Square Foot**. This reveals if top-line growth is genuine or merely an optical illusion caused by opening expensive new stores while old stores slow down.

---

## PAGE 2: VERIFICATION, THE AUDITABLE REPORT, AND ROADMAP

### 4. Triangulation: How Claims are Fact-Checked
ARGUS enforces a strict rule: **No finding can ever rely on a single document.** Every discovery requires a "Three-Legged Stool" of proof:
1. **Leg 1 (The Narrative):** Management's public claim from an investor presentation or concall transcript (e.g., *"Demand is accelerating across our rural distribution network"*).
2. **Leg 2 (The Hard Numbers):** Audited financial figures from regulatory filings (e.g., *Balance sheet shows trade receivables up while volume growth contracted*).
3. **Leg 3 (The External Reality Check):** Reports from at least two direct competitors or sector data for the same quarter (e.g., *Competitor A and Competitor B both reported steady debtor days, proving this issue is specific to the company, not the entire market*).

---

### 5. Self-Falsification: Testing if We Are Wrong
A core reason financial analysts make mistakes is confirmation bias—finding data that only supports their initial hunch. ARGUS eliminates this by embedding two mandatory checks:
* **The Strongest Counterargument:** The system actively searches for legitimate alternative explanations (e.g., *"Input costs for packaging surged sector-wide, forcing all brands to take price increases; distributor credit terms were temporarily relaxed to support a new regional expansion"*).
* **The Falsification Condition:** ARGUS explicitly states the exact future milestone that would disprove its theory (e.g., *"This finding is falsified if the company achieves two consecutive quarters of >4% volume growth with distributor receivable days returning below normal thresholds"*).

---

### 6. Single Output Format: Interactive Financial Research Dashboard
**Chosen Format:** **Interactive Financial Research Dashboard** (Single unified interface featuring inline SVG trend charts, metric cards, and auditable primary document ledger, with built-in one-click `@media print` Executive Memo export for PDF/print generation). It rigorously embeds all **8 Mandatory Discovery Elements**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. THE DISCOVERY: One concise sentence revealing the hidden story.    │
│ 2. WHY IT MATTERS: 3-4 bullets on operational & economic sustainability.│
│ 3. THE NUMBERS: Verified calculations (Price vs Volume split, DSO).    │
│ 4. THE TIMELINE: When the shift started and how it unfolded over time. │
│ 5. EVIDENCE TRAIL: Traceable, clickable links to exact filing passages.│
│ 6. COUNTERARGUMENT: The strongest alternative or macro explanation.    │
│ 7. FALSIFICATION CONDITION: Exact future metrics that disprove this.   │
│ 8. EVIDENCE STRENGTH: [Strong / Moderate / Weak] with rationale.       │
└────────────────────────────────────────────────────────────────────────┘
```
*Zero buy/sell recommendations, zero stock tips. Pure, verifiable corporate reality.*

---

### 7. Working MVP & Path to the Finals (October 25)

* **Current Status (Round 1 MVP Ready):**  
  We have already built an end-to-end working prototype that runs live on any Indian FMCG or Retail ticker in under 5 seconds. The prototype extracts quarterly financials from public sources, calculates DSO and growth splits via deterministic Python, executes the Red-Team counterargument, and renders the complete 8-element evidence trail in an interactive dashboard.
  * **GitHub Repository:** [Link to Repo]
  * **2-Minute Demo Video:** [Link to Demo Video]

* **Milestone Roadmap to Finals (Oct 20 – Oct 25):**
  * **Oct 20–21 (Deeper Concall Parsing):** Ingest full-text PDF concalls to extract direct speaker quotes using fast-inference models.
  * **Oct 22–23 (Broader Peer Scraping):** Expand automated cross-referencing to cover 10+ mid-cap retail and FMCG peers for industry-wide triangulation.
  * **Oct 24 (Stress-Testing):** Run the agent across all NIFTY 50 and non-NIFTY 50 consumer companies to guarantee zero crashes on edge-case filings.
  * **Oct 25 (Finals Live Presentation):** Deliver the 10-minute live demonstration on whichever company the judges select on the spot.
