#!/usr/bin/env python3
"""
Dashboard Generator & CLI Engine for ATMOS 2026 Financial Research Agent.
Track C — Consumer, FMCG & Retail.

Includes:
  1. Core Track C (6 Companies): HINDUNILVR, BRITANNIA, TATACONSUM, NESTLEIND, DABUR, TRENT
  2. Broader Consumer-Retail (2 Companies): TITAN, ASIANPAINT
  3. Generic On-the-spot Judge Investigation workflow for ANY eligible NSE company.
"""

import sys
import json
import os
from investigator import FinancialInvestigator

# Standard list of 8 primary companies + tie-breaker companies
CORE_TRACK_C = [
    ("HINDUNILVR", "Hindustan Unilever", "FMCG Staples"),
    ("BRITANNIA", "Britannia Industries", "FMCG Foods"),
    ("TATACONSUM", "Tata Consumer", "FMCG Foods & Bev"),
    ("NESTLEIND", "Nestle India", "FMCG Nutrition"),
    ("DABUR", "Dabur India", "FMCG Healthcare"),
    ("TRENT", "Trent (Zudio/Westside)", "Apparel Retail")
]

BROADER_CONSUMER = [
    ("TITAN", "Titan Company", "Jewellery & Watches"),
    ("ASIANPAINT", "Asian Paints", "Consumer Decorative")
]

TIE_BREAKERS = [
    ("V2RETAIL", "V2 Retail (Non-NIFTY 50)", "Value Fashion Retail"),
    ("BIKAJI", "Bikaji Foods (Non-NIFTY 50)", "Packaged Snacks"),
    ("DMART", "Avenue Supermarts", "Hypermarket Retail")
]

def print_banner(ticker: str):
    print("=" * 85)
    print(f"  ARGUS: AUTONOMOUS FINANCIAL DISCOVERY AGENT | TRACK C (FMCG & RETAIL)")
    print(f"  Target Company: {ticker.upper()} | Output Format: Interactive Research Dashboard")
    print("=" * 85)

def build_svg_chart(chart_data: dict) -> str:
    """Builds a pure inline SVG bar chart for quarterly revenue and YoY growth."""
    quarters = chart_data.get("quarters", [])
    sales = chart_data.get("sales_cr", [])
    growth = chart_data.get("yoy_growth_pct", [])
    if not sales:
        return ""

    max_sales = max(sales) if max(sales) > 0 else 1.0
    bar_width = 46
    gap = 26
    chart_h = 140
    total_w = len(quarters) * (bar_width + gap) + 40
    
    svg_bars = ""
    for i, (q, s, g) in enumerate(zip(quarters, sales, growth)):
        x = 25 + i * (bar_width + gap)
        h = int((s / max_sales) * chart_h)
        y = 170 - h
        g_text = f"+{g}%" if g is not None and g > 0 else (f"{g}%" if g is not None else "N/A")
        
        svg_bars += f"""
        <g class="bar-group">
            <rect x="{x}" y="{y}" width="{bar_width}" height="{h}" rx="4" fill="url(#blueGrad)" />
            <text x="{x + bar_width/2}" y="{y - 8}" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="700">₹{s:,.0f}</text>
            <text x="{x + bar_width/2}" y="190" text-anchor="middle" fill="#94a3b8" font-size="10">{q}</text>
            <rect x="{x + 2}" y="200" width="{bar_width - 4}" height="18" rx="9" fill="#0369a1" opacity="0.6"/>
            <text x="{x + bar_width/2}" y="213" text-anchor="middle" fill="#e0f2fe" font-size="9" font-weight="600">{g_text}</text>
        </g>
        """

    svg = f"""
    <svg viewBox="0 0 {total_w} 230" style="width: 100%; max-height: 230px; display: block; overflow: visible;">
        <defs>
            <linearGradient id="blueGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#38bdf8" />
                <stop offset="100%" stop-color="#0284c7" />
            </linearGradient>
        </defs>
        <line x1="10" y1="170" x2="{total_w - 10}" y2="170" stroke="#334155" stroke-width="1.5" />
        {svg_bars}
    </svg>
    """
    return svg

def load_or_fetch_all_reports(primary_ticker: str = "HINDUNILVR", primary_report: dict = None) -> dict:
    """Loads cached reports and ensures primary_ticker and the 8 companies are present."""
    all_reports = {}
    cache_file = "all_reports.json"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                all_reports = json.load(f)
        except Exception:
            all_reports = {}

    if primary_report and primary_ticker:
        all_reports[primary_ticker] = primary_report

    # Ensure all 8 default tickers exist in cache
    required_tickers = [t[0] for t in CORE_TRACK_C] + [t[0] for t in BROADER_CONSUMER]
    for t in required_tickers:
        if t not in all_reports:
            print(f"[*] Pre-computing investigation profile for {t}...")
            inv = FinancialInvestigator(t)
            rep = inv.run_investigation()
            if "error" not in rep:
                all_reports[t] = rep

    # Save back cache
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(all_reports, f, indent=2)
    except Exception:
        pass

    return all_reports

def generate_unified_html(all_reports: dict, default_ticker: str, filepath: str):
    """Generates the interactive multi-company dashboard with instant switcher and on-the-spot search."""
    if default_ticker not in all_reports:
        default_ticker = list(all_reports.keys())[0] if all_reports else "HINDUNILVR"

    report = all_reports[default_ticker]
    json_payload = json.dumps(all_reports)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARGUS Financial Discovery Dashboard - Track C</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0b1120;
            color: #f1f5f9;
            margin: 0;
            padding: 24px 16px;
        }}
        .container {{
            max-width: 1040px;
            margin: 0 auto;
            background: #1e293b;
            border-radius: 12px;
            padding: 28px 32px;
            box-shadow: 0 25px 35px -5px rgba(0, 0, 0, 0.6);
            border: 1px solid #334155;
        }}
        
        /* Company Selector Navigation */
        .selector-box {{
            background: #0f172a;
            border: 1px solid #38bdf8;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 24px;
        }}
        .selector-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #334155;
            padding-bottom: 10px;
            margin-bottom: 12px;
        }}
        .selector-title {{
            font-size: 13px;
            font-weight: 800;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .selector-sub {{
            font-size: 11px;
            color: #94a3b8;
        }}
        .group-row {{
            margin-bottom: 12px;
        }}
        .group-label {{
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: block;
            margin-bottom: 6px;
        }}
        .group-label.core {{ color: #38bdf8; }}
        .group-label.broader {{ color: #a78bfa; }}
        .group-label.judge {{ color: #4ade80; }}

        .btn-wrap {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .comp-btn {{
            background: #1e293b;
            color: #cbd5e1;
            border: 1px solid #475569;
            padding: 7px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease-in-out;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .comp-btn:hover {{
            background: #334155;
            color: #ffffff;
            border-color: #94a3b8;
        }}
        .comp-btn.active {{
            background: #0284c7;
            color: #ffffff;
            border-color: #38bdf8;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
        }}
        .comp-btn.broader.active {{
            background: #7c3aed;
            color: #ffffff;
            border-color: #c084fc;
            box-shadow: 0 0 12px rgba(192, 132, 252, 0.4);
        }}
        .comp-btn .sub-tag {{
            font-size: 9px;
            opacity: 0.75;
            font-weight: 400;
        }}

        /* On-the-spot search */
        .judge-search-bar {{
            display: flex;
            gap: 8px;
            margin-top: 4px;
        }}
        .judge-input {{
            flex: 1;
            max-width: 380px;
            background: #1e293b;
            border: 1px solid #475569;
            color: #ffffff;
            padding: 8px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            outline: none;
        }}
        .judge-input:focus {{
            border-color: #4ade80;
            box-shadow: 0 0 8px rgba(74, 222, 128, 0.3);
        }}
        .btn-investigate {{
            background: #15803d;
            color: #ffffff;
            border: 1px solid #22c55e;
            padding: 8px 18px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-investigate:hover {{
            background: #16a34a;
        }}
        .quick-chip {{
            background: #1e293b;
            color: #86efac;
            border: 1px solid #22c55e;
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 9999px;
            cursor: pointer;
            font-weight: 600;
        }}
        .quick-chip:hover {{
            background: #22c55e;
            color: #0f172a;
        }}

        /* Header bar */
        .header-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #334155;
            padding-bottom: 14px;
            margin-bottom: 20px;
        }}
        .badge {{
            display: inline-block;
            background: #0284c7;
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .strength-badge {{
            background: #f59e0b;
            color: #0f172a;
            font-weight: 800;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 12px;
        }}
        .btn-print {{
            background: #334155;
            color: #e2e8f0;
            border: 1px solid #475569;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-print:hover {{
            background: #475569;
            color: #ffffff;
        }}
        h1 {{
            margin: 6px 0 2px 0;
            font-size: 26px;
            color: #ffffff;
            letter-spacing: -0.01em;
        }}
        .section-box {{
            background: #0f172a;
            border-radius: 8px;
            padding: 18px 20px;
            margin-top: 18px;
            border: 1px solid #334155;
        }}
        .section-title {{
            font-size: 13px;
            font-weight: 800;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 10px;
        }}
        .discovery-banner {{
            background: rgba(14, 165, 233, 0.12);
            border-left: 5px solid #0ea5e9;
            padding: 16px 20px;
            border-radius: 6px;
            font-size: 15px;
            line-height: 1.6;
            color: #e0f2fe;
            margin-top: 16px;
            font-weight: 500;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 18px;
        }}
        @media (max-width: 768px) {{
            .grid-2 {{ grid-template-columns: 1fr; }}
            .judge-search-bar {{ flex-direction: column; }}
        }}
        .metric-pill {{
            background: #1e293b;
            padding: 12px 14px;
            border-radius: 6px;
            border: 1px solid #334155;
        }}
        .metric-val {{
            font-size: 20px;
            font-weight: 800;
            color: #38bdf8;
            margin-top: 2px;
        }}
        .metric-label {{
            font-size: 10px;
            color: #94a3b8;
            text-transform: uppercase;
            font-weight: 700;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        @media print {{
            body {{ background: #ffffff; color: #000000; padding: 0; }}
            .container {{ border: none; box-shadow: none; max-width: 100%; padding: 0; background: #ffffff; color: #000000; }}
            .selector-box, .btn-print {{ display: none; }}
            .section-box, .metric-pill {{ background: #f8fafc; border: 1px solid #cbd5e1; color: #000000; }}
            .discovery-banner {{ background: #f0fdf4; border-left: 5px solid #16a34a; color: #000000; }}
            a {{ color: #2563eb !important; text-decoration: underline !important; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        
        <!-- Interactive Company Switcher Bar -->
        <div class="selector-box">
            <div class="selector-header">
                <span class="selector-title">Select Company Profile &bull; Track C (FMCG & Retail)</span>
                <span class="selector-sub">Generic Autonomous Workflow &bull; Instant Switching</span>
            </div>
            
            <!-- Group 1: Core Track C -->
            <div class="group-row">
                <span class="group-label core">1. Core Track C (FMCG & Retail):</span>
                <div class="btn-wrap">
                    <button class="comp-btn active" data-ticker="HINDUNILVR" onclick="switchCompany('HINDUNILVR')">
                        Hindustan Unilever <span class="sub-tag">(Staples)</span>
                    </button>
                    <button class="comp-btn" data-ticker="BRITANNIA" onclick="switchCompany('BRITANNIA')">
                        Britannia <span class="sub-tag">(Foods)</span>
                    </button>
                    <button class="comp-btn" data-ticker="TATACONSUM" onclick="switchCompany('TATACONSUM')">
                        Tata Consumer <span class="sub-tag">(Beverages)</span>
                    </button>
                    <button class="comp-btn" data-ticker="NESTLEIND" onclick="switchCompany('NESTLEIND')">
                        Nestle India <span class="sub-tag">(Nutrition)</span>
                    </button>
                    <button class="comp-btn" data-ticker="DABUR" onclick="switchCompany('DABUR')">
                        Dabur <span class="sub-tag">(Healthcare)</span>
                    </button>
                    <button class="comp-btn" data-ticker="TRENT" onclick="switchCompany('TRENT')">
                        Trent <span class="sub-tag">(Zudio / Retail)</span>
                    </button>
                </div>
            </div>

            <!-- Group 2: Broader Consumer-Retail -->
            <div class="group-row">
                <span class="group-label broader">2. Broader Consumer-Retail:</span>
                <div class="btn-wrap">
                    <button class="comp-btn broader" data-ticker="TITAN" onclick="switchCompany('TITAN')">
                        Titan Company <span class="sub-tag">(Jewellery & Watches)</span>
                    </button>
                    <button class="comp-btn broader" data-ticker="ASIANPAINT" onclick="switchCompany('ASIANPAINT')">
                        Asian Paints <span class="sub-tag">(Consumer Decorative)</span>
                    </button>
                </div>
            </div>

            <!-- Group 3: On-The-Spot Judge Selection -->
            <div class="group-row" style="margin-bottom: 0;">
                <span class="group-label judge">3. On-The-Spot Judge Selection (Generic Workflow & Tie-Breakers):</span>
                <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 11px; color: #94a3b8;">Quick Non-NIFTY 50 Tie-Breakers:</span>
                    <button class="quick-chip" onclick="switchCompany('V2RETAIL')">V2 Retail (Small-cap Retail)</button>
                    <button class="quick-chip" onclick="switchCompany('BIKAJI')">Bikaji Foods (Mid-cap FMCG)</button>
                    <button class="quick-chip" onclick="switchCompany('DMART')">Avenue Supermarts (DMart)</button>
                </div>
                <div class="judge-search-bar">
                    <input type="text" id="judgeInput" class="judge-input" placeholder="Type ANY eligible company ticker (e.g. MARICO, GODREJCP, BATAINDIA)..." />
                    <button class="btn-investigate" onclick="handleJudgeSearch()">Investigate On-The-Spot 🔍</button>
                </div>
                <div id="searchStatus" style="font-size: 11px; color: #94a3b8; margin-top: 4px;"></div>
            </div>
        </div>

        <!-- Dashboard Header -->
        <div class="header-bar">
            <div>
                <span class="badge" id="trackBadge">{report.get('track')} &bull; {report.get('business_model')}</span>
                <span style="font-size: 12px; color: #94a3b8; margin-left: 10px;">Format: {report.get('output_format')}</span>
            </div>
            <div>
                <span class="strength-badge" id="evidenceStrengthTop">Evidence: {report.get('element_8_evidence_strength', {}).get('rating', 'Moderate')}</span>
                <button class="btn-print" onclick="window.print()" style="margin-left: 10px;">🖨️ Export Executive Memo</button>
            </div>
        </div>

        <h1 id="companyHeading">{report.get('company_name')} ({report.get('ticker')})</h1>
        <div style="color: #94a3b8; font-size: 13px;">Autonomous Financial Research Agent &bull; Non-Obvious Contradiction Discovery</div>

        <!-- Element 1: The Discovery -->
        <div class="discovery-banner">
            <div style="font-size: 12px; text-transform: uppercase; color: #38bdf8; font-weight: 800; margin-bottom: 4px;">1. The Non-Obvious Discovery</div>
            <div id="discoveryText">{report.get('element_1_the_discovery')}</div>
        </div>

        <!-- Element 2: Why It Matters -->
        <div class="section-box">
            <div class="section-title">2. Why It Matters (Operational & Financial Durability)</div>
            <ul id="whyList" style="margin: 0; padding-left: 20px; line-height: 1.6; color: #cbd5e1; font-size: 14px;">
            </ul>
        </div>

        <!-- Element 3 & 4: Numbers, Charts & Timeline -->
        <div class="grid-2">
            <div class="section-box" style="margin-top: 0;">
                <div class="section-title">3. Verified Financial Metrics & Trend Chart</div>
                <div id="metricsGrid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px;">
                </div>
                <div id="chartContainer"></div>
                <div id="mathProvenance" style="margin-top: 10px; font-size: 11px; color: #64748b;"></div>
            </div>

            <div class="section-box" style="margin-top: 0;">
                <div class="section-title">4. Emergence Timeline</div>
                <ul id="timelineList" style="margin: 0; padding-left: 20px; line-height: 1.5; font-size: 13px; color: #cbd5e1;">
                </ul>
            </div>
        </div>

        <!-- Element 5: Triangulated Evidence Trail -->
        <div class="section-box">
            <div class="section-title">5. Triangulated Evidence Trail (Auditable Document Ledger)</div>
            <div id="evidenceContainer" style="margin-top: 10px;"></div>
        </div>

        <!-- Elements 6 & 7: Counterargument & Falsification Condition -->
        <div class="grid-2">
            <div class="section-box">
                <div class="section-title" style="color: #f87171;">6. Strongest Counterargument (Red Team Adversary)</div>
                <p id="counterargumentText" style="margin: 0; font-size: 13.5px; line-height: 1.6; color: #e2e8f0;"></p>
            </div>

            <div class="section-box">
                <div class="section-title" style="color: #4ade80;">7. Falsification Condition (Specific & Measurable)</div>
                <p id="falsificationText" style="margin: 0; font-size: 13.5px; line-height: 1.6; color: #e2e8f0;"></p>
            </div>
        </div>

        <!-- Element 8: Evidence Strength & Rubric Breakdown -->
        <div class="section-box">
            <div class="section-title" style="color: #fbbf24;">8. Evidence Strength & Forensic Rubric Breakdown</div>
            <div style="margin-bottom: 12px;">
                <span class="strength-badge" id="evidenceStrengthRating"></span>
            </div>
            <table style="margin-bottom: 14px;">
                <thead>
                    <tr style="border-bottom: 2px solid #334155; text-align: left;">
                        <th style="padding: 8px 12px; font-size: 11px; color: #38bdf8; text-transform: uppercase;">Rubric Dimension</th>
                        <th style="padding: 8px 12px; font-size: 11px; color: #38bdf8; text-transform: uppercase;">Confidence Level</th>
                        <th style="padding: 8px 12px; font-size: 11px; color: #38bdf8; text-transform: uppercase;">Empirical Evidence</th>
                    </tr>
                </thead>
                <tbody id="rubricTableBody"></tbody>
            </table>
            <p id="synthesisRationale" style="margin: 0; font-size: 12.5px; line-height: 1.6; color: #cbd5e1;"></p>
        </div>

        <!-- Section E: Autonomous Reasoning Pipeline -->
        <div class="section-box">
            <div class="section-title">Section E: Autonomous Forensic Reasoning Pipeline</div>
            <div id="reasoningGrid" style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;"></div>
        </div>

        <div style="margin-top: 24px; text-align: center; font-size: 11px; color: #64748b;">
            ATMOS 2026 Autonomous Research Agent &bull; 100% Public Data &bull; Zero Hardcoding &bull; Zero Investment Advice
        </div>
    </div>

    <!-- Client-side Switcher Logic -->
    <script>
        const ALL_REPORTS = {json_payload};
        let currentTicker = "{default_ticker}";

        function generateSvg(chartData) {{
            const quarters = chartData.quarters || [];
            const sales = chartData.sales_cr || [];
            const growth = chartData.yoy_growth_pct || [];
            if (!sales.length) return "";

            const maxSales = Math.max(...sales) || 1.0;
            const barWidth = 46;
            const gap = 26;
            const chartH = 140;
            const totalW = quarters.length * (barWidth + gap) + 40;

            let barsSvg = "";
            for (let i = 0; i < quarters.length; i++) {{
                const q = quarters[i];
                const s = sales[i];
                const g = growth[i];
                const x = 25 + i * (barWidth + gap);
                const h = Math.round((s / maxSales) * chartH);
                const y = 170 - h;
                const gText = g !== null && g > 0 ? `+${{g}}%` : (g !== null ? `${{g}}%` : "N/A");

                barsSvg += `
                <g class="bar-group">
                    <rect x="${{x}}" y="${{y}}" width="${{barWidth}}" height="${{h}}" rx="4" fill="url(#blueGrad)" />
                    <text x="${{x + barWidth/2}}" y="${{y - 8}}" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="700">₹${{Math.round(s).toLocaleString()}}</text>
                    <text x="${{x + barWidth/2}}" y="190" text-anchor="middle" fill="#94a3b8" font-size="10">${{q}}</text>
                    <rect x="${{x + 2}}" y="200" width="${{barWidth - 4}}" height="18" rx="9" fill="#0369a1" opacity="0.6"/>
                    <text x="${{x + barWidth/2}}" y="213" text-anchor="middle" fill="#e0f2fe" font-size="9" font-weight="600">${{gText}}</text>
                </g>
                `;
            }}

            return `
            <svg viewBox="0 0 ${{totalW}} 230" style="width: 100%; max-height: 230px; display: block; overflow: visible;">
                <defs>
                    <linearGradient id="blueGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="#38bdf8" />
                        <stop offset="100%" stop-color="#0284c7" />
                    </linearGradient>
                </defs>
                <line x1="10" y1="170" x2="${{totalW - 10}}" y2="170" stroke="#334155" stroke-width="1.5" />
                ${{barsSvg}}
            </svg>
            `;
        }}

        function renderReport(report) {{
            if (!report) return;

            // Header info
            document.getElementById("trackBadge").textContent = `${{report.track}} • ${{report.business_model}}`;
            document.getElementById("companyHeading").textContent = `${{report.company_name}} (${{report.ticker}})`;

            const strength = report.element_8_evidence_strength || {{}};
            const ratingText = `Evidence: ${{strength.rating || 'Moderate'}}`;
            document.getElementById("evidenceStrengthTop").textContent = ratingText;
            document.getElementById("evidenceStrengthRating").textContent = `Rating: ${{strength.rating || 'Moderate'}}`;
            document.getElementById("synthesisRationale").innerHTML = `<strong>Synthesis Rationale:</strong> ${{strength.rationale || ''}}`;

            // 1. Discovery
            document.getElementById("discoveryText").textContent = report.element_1_the_discovery || "";

            // 2. Why it matters
            const whyList = document.getElementById("whyList");
            whyList.innerHTML = (report.element_2_why_it_matters || []).map(w => `<li style="margin-bottom: 8px;">${{w}}</li>`).join("");

            // 3. Numbers & SVG Chart
            const nums = report.element_3_numbers || report.element_5_numbers || {{}};
            let metricHtml = "";
            if ("latest_4q_avg_sales_growth_pct" in nums) {{
                metricHtml += `
                <div class="metric-pill">
                    <div class="metric-label">Sales Growth (YoY Avg)</div>
                    <div class="metric-val">+${{nums.latest_4q_avg_sales_growth_pct}}%</div>
                </div>`;
            }}
            if ("dso_recent_days" in nums && nums.dso_recent_days !== null) {{
                metricHtml += `
                <div class="metric-pill">
                    <div class="metric-label">Receivable Days (DSO)</div>
                    <div class="metric-val">${{nums.dso_recent_days}} Days</div>
                </div>`;
            }}
            if ("dio_recent_days" in nums && nums.dio_recent_days !== null) {{
                metricHtml += `
                <div class="metric-pill">
                    <div class="metric-label">Inventory Days (DIO)</div>
                    <div class="metric-val">${{nums.dio_recent_days}} Days</div>
                </div>`;
            }}
            if ("inventory_recent_cr" in nums && nums.inventory_recent_cr !== null) {{
                metricHtml += `
                <div class="metric-pill">
                    <div class="metric-label">Recent Inventory</div>
                    <div class="metric-val">₹${{Math.round(nums.inventory_recent_cr).toLocaleString()}} Cr</div>
                </div>`;
            }}
            document.getElementById("metricsGrid").innerHTML = metricHtml;
            document.getElementById("chartContainer").innerHTML = generateSvg(report.chart_data || {{}});
            document.getElementById("mathProvenance").textContent = `Provenance: ${{nums.calculation_provenance || 'Deterministic Python Math Engine'}}`;

            // 4. Timeline
            const timelineList = document.getElementById("timelineList");
            timelineList.innerHTML = (report.element_4_timeline || []).map(t => `<li style="margin-bottom: 8px;">${{t}}</li>`).join("");

            // 5. Evidence Trail
            const evidenceContainer = document.getElementById("evidenceContainer");
            const evidenceList = report.element_5_evidence_trail || report.element_3_evidence || [];
            evidenceContainer.innerHTML = evidenceList.map(s => `
                <div style="margin-bottom: 14px; padding: 14px; background: #0f172a; border-left: 4px solid #38bdf8; border-radius: 6px; border: 1px solid #334155;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 700; color: #38bdf8; font-size: 12px; text-transform: uppercase;">${{s.source_type || 'Primary Document'}}</span>
                        <span style="background: #1e293b; color: #94a3b8; font-size: 11px; padding: 2px 8px; border-radius: 4px; border: 1px solid #334155;">${{s.publication_date || ''}}</span>
                    </div>
                    <div style="color: #ffffff; font-weight: 600; font-size: 14px;">${{s.document_title || s.title || ''}}</div>
                    <div style="color: #94a3b8; font-size: 12px; margin-top: 3px;"><strong>Section/Page:</strong> ${{s.section_or_page || 'Consolidated Filings'}}</div>
                    <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 4px; margin-top: 6px; font-size: 12.5px; color: #cbd5e1; border-left: 2px solid #64748b;">
                        <strong>Exact Figure / Passage:</strong> ${{s.exact_figure_or_passage || s.data_covered || ''}}
                    </div>
                    <a href="${{s.source_link || s.url}}" target="_blank" rel="noopener noreferrer" style="display: inline-block; margin-top: 8px; font-size: 12px; color: #60a5fa; text-decoration: none; font-weight: 600;">
                        Verify Primary Document &rarr;
                    </a>
                </div>
            `).join("");

            // 6. Counterargument
            document.getElementById("counterargumentText").textContent = report.element_6_counterargument || "";

            // 7. Falsification
            document.getElementById("falsificationText").textContent = report.element_7_falsification_condition || "";

            // 8. Rubric Table
            const rubricTableBody = document.getElementById("rubricTableBody");
            const breakdown = strength.rubric_breakdown || {{}};
            let rubricHtml = "";
            for (const [dim, info] of Object.entries(breakdown)) {{
                const label = dim.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase());
                rubricHtml += `
                <tr style="border-bottom: 1px solid #334155;">
                    <td style="padding: 8px 12px; color: #94a3b8; font-size: 12px; font-weight: 500;">${{label}}</td>
                    <td style="padding: 8px 12px; color: #38bdf8; font-size: 12px; font-weight: 600;">${{info.score || ''}}</td>
                    <td style="padding: 8px 12px; color: #cbd5e1; font-size: 11.5px;">${{info.detail || ''}}</td>
                </tr>`;
            }}
            rubricTableBody.innerHTML = rubricHtml;

            // Section E Reasoning
            const reasoningGrid = document.getElementById("reasoningGrid");
            reasoningGrid.innerHTML = (report.reasoning_process || []).map(r => `
                <div style="background: #1e293b; border-radius: 6px; padding: 10px 12px; border: 1px solid #334155;">
                    <div style="font-size: 10px; text-transform: uppercase; color: #38bdf8; font-weight: 700;">Step ${{r.step}}: ${{r.name}}</div>
                    <div style="font-size: 12px; color: #cbd5e1; margin-top: 3px; line-height: 1.35;">${{r.description}}</div>
                </div>
            `).join("");
        }}

        function switchCompany(ticker) {{
            ticker = ticker.toUpperCase().trim();
            if (ALL_REPORTS[ticker]) {{
                currentTicker = ticker;
                renderReport(ALL_REPORTS[ticker]);

                // Update active button state
                document.querySelectorAll(".comp-btn").forEach(btn => {{
                    if (btn.getAttribute("data-ticker") === ticker) {{
                        btn.classList.add("active");
                    }} else {{
                        btn.classList.remove("active");
                    }}
                }});

                document.getElementById("searchStatus").textContent = `Active Profile: ${{ticker}}`;
            }} else {{
                document.getElementById("searchStatus").innerHTML = `Profile for ${{ticker}} not in offline cache. Use 'Investigate On-The-Spot' or run <code>python3 main.py ${{ticker}}</code> in terminal.`;
            }}
        }}

        async function handleJudgeSearch() {{
            const input = document.getElementById("judgeInput");
            const ticker = (input.value || "").toUpperCase().trim();
            if (!ticker) return;

            const status = document.getElementById("searchStatus");
            if (ALL_REPORTS[ticker]) {{
                switchCompany(ticker);
                return;
            }}

            status.innerHTML = `⏳ Connecting to public filings for <strong>${{ticker}}</strong> via generic workflow...`;

            try {{
                // Try live local server API
                const resp = await fetch(`/api/investigate?ticker=${{ticker}}`);
                if (resp.ok) {{
                    const data = await resp.json();
                    if (data.error) {{
                        status.textContent = `❌ ${{data.error}}`;
                    }} else {{
                        ALL_REPORTS[ticker] = data;
                        renderReport(data);
                        status.innerHTML = `✅ Successfully investigated <strong>${{ticker}}</strong> on the spot!`;
                    }}
                    return;
                }}
            }} catch (e) {{
                // Server not active, instruct judge/user
                status.innerHTML = `Offline mode: To run on-the-spot for <strong>${{ticker}}</strong>, execute <code>python3 main.py ${{ticker}}</code> in your terminal or start <code>python3 server.py</code>!`;
            }}
        }}

        // Initialize on page load
        window.addEventListener("DOMContentLoaded", () => {{
            renderReport(ALL_REPORTS[currentTicker]);
        }});
    </script>
</body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Multi-Company Interactive Dashboard saved: {os.path.abspath(filepath)}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        from server import run_server
        run_server()
        return

    ticker = sys.argv[1] if len(sys.argv) > 1 else "HINDUNILVR"
    ticker = ticker.upper().strip()

    if ticker == "--ALL":
        print("=" * 85)
        print("  ARGUS: PRE-COMPUTING ALL 8 TRACK C & BROADER CONSUMER PROFILES")
        print("=" * 85)
        all_reps = load_or_fetch_all_reports()
        generate_unified_html(all_reps, "HINDUNILVR", "dashboard.html")
        return

    print_banner(ticker)
    print(f"[*] Step 1: Connecting to public regulatory filings for {ticker}...")
    investigator = FinancialInvestigator(ticker)
    
    print(f"[*] Step 2: Harvesting quarterly statements, balance sheet notes & peer data...")
    report = investigator.run_investigation()
    
    if "error" in report:
        print(f"[!] Error: {report['error']}")
        sys.exit(1)

    print(f"[*] Step 3: Executing deterministic financial calculations (DSO, DIO & Growth)...")
    print(f"[*] Step 4: Spawning Red-Team Adversary to challenge findings...")
    print(f"[*] Step 5: Formulating Falsification Condition & Auditable Evidence Ledger...")
    print("\n" + "=" * 85)
    print("  INVESTIGATION COMPLETE: 8-ELEMENT REQUIRED DISCOVERY DASHBOARD")
    print("=" * 85 + "\n")

    print(f"1. THE DISCOVERY:\n   {report['element_1_the_discovery']}\n")
    print("2. WHY IT MATTERS:")
    for point in report['element_2_why_it_matters']:
        print(f"   * {point}")
    print()

    verified_nums = report.get('element_3_numbers', report.get('element_5_numbers', {}))
    print("3. VERIFIED NUMBERS:")
    for k, v in verified_nums.items():
        if k != "calculation_provenance":
            print(f"   - {k}: {v}")
    print(f"   [Math Provenance]: {verified_nums.get('calculation_provenance')}\n")

    print("4. TIMELINE:")
    for t in report['element_4_timeline']:
        print(f"   > {t}")
    print()

    evidence_items = report.get('element_5_evidence_trail', report.get('element_3_evidence', []))
    print("5. AUDITABLE EVIDENCE TRAIL (DOCUMENT LEDGER):")
    for s in evidence_items:
        print(f"   [{s.get('source_type')}]")
        print(f"   Title:   {s.get('document_title', s.get('title'))}")
        print(f"   Date:    {s.get('publication_date')}")
        print(f"   Section: {s.get('section_or_page', 'Consolidated Filings')}")
        print(f"   Passage: {s.get('exact_figure_or_passage', s.get('data_covered'))}")
        print(f"   URL:     {s.get('source_link', s.get('url'))}\n")

    print("6. STRONGEST COUNTERARGUMENT:")
    print(f"   {report['element_6_counterargument']}\n")

    print("7. FALSIFICATION CONDITION:")
    print(f"   {report['element_7_falsification_condition']}\n")

    strength_data = report.get('element_8_evidence_strength', {})
    print("8. EVIDENCE STRENGTH & RUBRIC BREAKDOWN:")
    print(f"   Rating: {strength_data.get('rating')}")
    print("   Rubric Breakdown:")
    for dim, info in strength_data.get("rubric_breakdown", {}).items():
        print(f"     - {dim.replace('_', ' ').title()}: {info.get('score')} | {info.get('detail')}")
    print(f"   Rationale: {strength_data.get('rationale')}\n")

    print("SECTION E: AUTONOMOUS REASONING PIPELINE:")
    for step in report.get("reasoning_process", []):
        print(f"   [{step['step']}] {step['name']}: {step['description']}")
    print()

    # Save artifacts
    json_path = f"output_{ticker}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Load cache and generate unified dashboard
    all_reports = load_or_fetch_all_reports(ticker, report)
    html_path = f"report_{ticker}.html"
    generate_unified_html(all_reports, ticker, html_path)
    generate_unified_html(all_reports, ticker, "dashboard.html")

    print("=" * 85)
    print(f"[+] Output JSON saved: {os.path.abspath(json_path)}")
    print(f"[+] Individual Company Dashboard: {os.path.abspath(html_path)}")
    print(f"[+] Unified Multi-Company Dashboard: {os.path.abspath('dashboard.html')}")
    print("=" * 85)

if __name__ == "__main__":
    main()
