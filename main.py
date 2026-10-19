#!/usr/bin/env python3
"""
Dashboard Generator & CLI Engine for ATMOS 2026 Financial Research Agent.
Track C — Consumer, FMCG & Retail.

Includes:
  1. Header and Selector matching ATMOS design:
     - "Choose from the company list" dropdown with checkmark selection
     - "Search by company name or NSE symbol"
     - Grouping into Core Track C (6 companies) and Broader Consumer-Retail (2 companies)
  2. Generic On-the-spot Judge Investigation workflow for ANY eligible NSE company.
"""

import sys
import json
import os
from investigator import FinancialInvestigator

# Standard list of 8 primary companies + tie-breaker companies
CORE_TRACK_C = [
    ("HINDUNILVR", "Hindustan Unilever", "FMCG Staples"),
    ("BRITANNIA", "Britannia Industries", "FMCG Foods"),
    ("TATACONSUM", "Tata Consumer Products", "FMCG Foods & Bev"),
    ("NESTLEIND", "Nestlé India", "FMCG Nutrition"),
    ("DABUR", "Dabur India", "FMCG Healthcare"),
    ("TRENT", "Trent", "Apparel Retail (Westside/Zudio)")
]

BROADER_CONSUMER = [
    ("TITAN", "Titan Company", "Jewellery & Watches"),
    ("ASIANPAINT", "Asian Paints", "Consumer Decorative"),
    ("ITC", "ITC", "FMCG Diversified")
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

def load_or_fetch_all_reports(primary_ticker: str = "TRENT", primary_report: dict = None) -> dict:
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

    # Ensure all default tickers exist in cache
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
    """Generates the interactive dashboard with the exact ATMOS selector layout."""
    if default_ticker not in all_reports:
        default_ticker = "TRENT" if "TRENT" in all_reports else list(all_reports.keys())[0]

    report = all_reports[default_ticker]
    json_payload = json.dumps(all_reports)

    # Initial display text for dropdown trigger
    disp_names = {
        "HINDUNILVR": "Hindustan Unilever (HINDUNILVR)",
        "BRITANNIA": "Britannia Industries (BRITANNIA)",
        "TATACONSUM": "Tata Consumer Products (TATACONSUM)",
        "NESTLEIND": "Nestlé India (NESTLEIND)",
        "DABUR": "Dabur India (DABUR)",
        "TRENT": "Trent (TRENT)",
        "TITAN": "Titan Company (TITAN)",
        "ASIANPAINT": "Asian Paints (ASIANPAINT)",
        "ITC": "ITC (ITC)",
        "V2RETAIL": "V2 Retail (V2RETAIL)",
        "BIKAJI": "Bikaji Foods (BIKAJI)",
        "DMART": "Avenue Supermarts (DMART)"
    }
    initial_label = disp_names.get(default_ticker, f"{report.get('company_name')} ({default_ticker})")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ATMOS — Financial Research Agent (Track C)</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #000000;
            color: #f1f5f9;
            margin: 0;
            padding: 24px 16px;
        }}
        .container {{
            max-width: 980px;
            margin: 0 auto;
            background: #0d1117;
            border-radius: 14px;
            padding: 30px;
            box-shadow: 0 25px 40px -5px rgba(0, 0, 0, 0.8);
            border: 1px solid #21262d;
        }}
        
        /* ATMOS Card Top Selector (Exact Layout from Screenshot) */
        .atmos-selector-card {{
            background: #010409;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 24px 28px;
            margin-bottom: 24px;
        }}
        .atmos-header-title {{
            font-size: 20px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.01em;
        }}
        .atmos-header-subtitle {{
            font-size: 13.5px;
            color: #8b949e;
            margin-top: 4px;
            margin-bottom: 20px;
        }}
        .select-label {{
            font-size: 14.5px;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 12px;
        }}
        .radio-options {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 18px;
        }}
        .radio-label {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 14px;
            color: #e6edf3;
            cursor: pointer;
            user-select: none;
        }}
        .radio-label input[type="radio"] {{
            appearance: none;
            width: 17px;
            height: 17px;
            border: 2px solid #6e7681;
            border-radius: 50%;
            outline: none;
            cursor: pointer;
            position: relative;
            background: #0d1117;
            margin: 0;
        }}
        .radio-label input[type="radio"]:checked {{
            border-color: #58a6ff;
        }}
        .radio-label input[type="radio"]:checked::after {{
            content: "";
            position: absolute;
            top: 3px;
            left: 3px;
            width: 7px;
            height: 7px;
            background: #ffffff;
            border-radius: 50%;
        }}

        /* Custom Dropdown Trigger */
        .dropdown-wrapper {{
            position: relative;
            margin-bottom: 18px;
        }}
        .custom-select-trigger {{
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 20px;
            padding: 10px 18px;
            font-size: 14px;
            color: #ffffff;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }}
        .custom-select-trigger:hover {{
            border-color: #58a6ff;
        }}
        .chevron-icon {{
            width: 18px;
            height: 18px;
            color: #8b949e;
            transition: transform 0.2s;
        }}
        .chevron-icon.open {{
            transform: rotate(180deg);
        }}

        /* Dropdown Popup Menu */
        .custom-dropdown-menu {{
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            margin-top: 6px;
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.8);
            z-index: 100;
            max-height: 380px;
            overflow-y: auto;
        }}
        .custom-dropdown-menu.show {{
            display: block;
        }}
        .dropdown-category {{
            font-size: 11px;
            font-weight: 700;
            color: #58a6ff;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 10px 16px 4px 16px;
            border-top: 1px solid #21262d;
            background: #13171f;
        }}
        .dropdown-category:first-child {{
            border-top: none;
            border-radius: 12px 12px 0 0;
        }}
        .dropdown-item {{
            padding: 9px 16px;
            font-size: 13.5px;
            color: #e6edf3;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: background 0.15s;
        }}
        .dropdown-item:hover {{
            background: #21262d;
            color: #ffffff;
        }}
        .dropdown-item.active {{
            background: #1f2937;
            color: #58a6ff;
            font-weight: 600;
        }}
        .check-slot {{
            width: 14px;
            display: inline-block;
            font-weight: 700;
            color: #58a6ff;
        }}

        /* Search input mode */
        .search-wrapper {{
            margin-bottom: 18px;
        }}
        .search-input-group {{
            display: flex;
            gap: 8px;
        }}
        .search-input {{
            flex: 1;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 20px;
            padding: 10px 18px;
            font-size: 13.5px;
            color: #ffffff;
            outline: none;
        }}
        .search-input:focus {{
            border-color: #58a6ff;
            box-shadow: 0 0 8px rgba(88, 166, 255, 0.3);
        }}
        .search-btn {{
            background: #238636;
            color: #ffffff;
            border: 1px solid #2ea043;
            border-radius: 20px;
            padding: 10px 20px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
        }}
        .search-btn:hover {{
            background: #2ea043;
        }}

        .validation-note {{
            font-size: 12.5px;
            color: #8b949e;
            line-height: 1.5;
            padding-top: 10px;
            border-top: 1px solid #21262d;
        }}
        .validation-note strong {{
            color: #c9d1d9;
        }}

        /* Dashboard Content Header */
        .header-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #21262d;
            padding-bottom: 14px;
            margin-bottom: 20px;
        }}
        .badge {{
            display: inline-block;
            background: #1f6feb;
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .strength-badge {{
            background: #d29922;
            color: #0d1117;
            font-weight: 800;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 12px;
        }}
        .btn-print {{
            background: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-print:hover {{
            background: #30363d;
            color: #ffffff;
        }}
        h1 {{
            margin: 6px 0 2px 0;
            font-size: 26px;
            color: #ffffff;
            letter-spacing: -0.01em;
        }}
        .section-box {{
            background: #010409;
            border-radius: 8px;
            padding: 18px 20px;
            margin-top: 18px;
            border: 1px solid #21262d;
        }}
        .section-title {{
            font-size: 13px;
            font-weight: 800;
            color: #58a6ff;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 10px;
        }}
        .discovery-banner {{
            background: rgba(56, 189, 248, 0.1);
            border-left: 5px solid #38bdf8;
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
            .search-input-group {{ flex-direction: column; }}
        }}
        .metric-pill {{
            background: #0d1117;
            padding: 12px 14px;
            border-radius: 6px;
            border: 1px solid #21262d;
        }}
        .metric-val {{
            font-size: 20px;
            font-weight: 800;
            color: #58a6ff;
            margin-top: 2px;
        }}
        .metric-label {{
            font-size: 10px;
            color: #8b949e;
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
            .atmos-selector-card, .btn-print {{ display: none; }}
            .section-box, .metric-pill {{ background: #f8fafc; border: 1px solid #cbd5e1; color: #000000; }}
            .discovery-banner {{ background: #f0fdf4; border-left: 5px solid #16a34a; color: #000000; }}
            a {{ color: #2563eb !important; text-decoration: underline !important; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        
        <!-- Exact ATMOS Selector Top Card (Matches Hackathon UI) -->
        <div class="atmos-selector-card">
            <div class="atmos-header-title">ATMOS &mdash; Financial Research Agent</div>
            <div class="atmos-header-subtitle">Track C &middot; Consumer, FMCG &amp; Retail</div>
            
            <div class="select-label">Select a NIFTY 50 company</div>
            
            <div class="radio-options">
                <label class="radio-label">
                    <input type="radio" name="companyMode" id="radioList" value="list" checked onchange="toggleSelectorMode('list')" />
                    <span>Choose from the company list</span>
                </label>
                <label class="radio-label">
                    <input type="radio" name="companyMode" id="radioSearch" value="search" onchange="toggleSelectorMode('search')" />
                    <span>Search by company name or NSE symbol</span>
                </label>
            </div>

            <!-- Mode 1: Custom Dropdown Menu -->
            <div id="listModeWrapper" class="dropdown-wrapper">
                <div class="custom-select-trigger" onclick="toggleDropdown(event)">
                    <span id="selectedCompanyLabel">{initial_label}</span>
                    <svg id="chevronIcon" class="chevron-icon" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
                    </svg>
                </div>
                <div id="customDropdownMenu" class="custom-dropdown-menu">
                    <!-- Core Track C (First 6) -->
                    <div class="dropdown-category">Core Track C (FMCG &amp; Retail)</div>
                    <div class="dropdown-item" data-ticker="HINDUNILVR" onclick="selectCompany('HINDUNILVR')">
                        <span class="check-slot"></span> Hindustan Unilever (HINDUNILVR)
                    </div>
                    <div class="dropdown-item" data-ticker="BRITANNIA" onclick="selectCompany('BRITANNIA')">
                        <span class="check-slot"></span> Britannia Industries (BRITANNIA)
                    </div>
                    <div class="dropdown-item" data-ticker="TATACONSUM" onclick="selectCompany('TATACONSUM')">
                        <span class="check-slot"></span> Tata Consumer Products (TATACONSUM)
                    </div>
                    <div class="dropdown-item" data-ticker="NESTLEIND" onclick="selectCompany('NESTLEIND')">
                        <span class="check-slot"></span> Nestl&eacute; India (NESTLEIND)
                    </div>
                    <div class="dropdown-item" data-ticker="DABUR" onclick="selectCompany('DABUR')">
                        <span class="check-slot"></span> Dabur India (DABUR)
                    </div>
                    <div class="dropdown-item" data-ticker="TRENT" onclick="selectCompany('TRENT')">
                        <span class="check-slot"></span> Trent (TRENT)
                    </div>

                    <!-- Broader Consumer-Retail (2 Companies) -->
                    <div class="dropdown-category">Broader Consumer-Retail</div>
                    <div class="dropdown-item" data-ticker="TITAN" onclick="selectCompany('TITAN')">
                        <span class="check-slot"></span> Titan Company (TITAN)
                    </div>
                    <div class="dropdown-item" data-ticker="ASIANPAINT" onclick="selectCompany('ASIANPAINT')">
                        <span class="check-slot"></span> Asian Paints (ASIANPAINT)
                    </div>
                    <div class="dropdown-item" data-ticker="ITC" onclick="selectCompany('ITC')">
                        <span class="check-slot"></span> ITC (ITC)
                    </div>

                    <!-- Non-NIFTY 50 Tie-Breakers (Generic Workflow) -->
                    <div class="dropdown-category">Non-NIFTY 50 Tie-Breakers (Generic Workflow)</div>
                    <div class="dropdown-item" data-ticker="V2RETAIL" onclick="selectCompany('V2RETAIL')">
                        <span class="check-slot"></span> V2 Retail (V2RETAIL)
                    </div>
                    <div class="dropdown-item" data-ticker="BIKAJI" onclick="selectCompany('BIKAJI')">
                        <span class="check-slot"></span> Bikaji Foods (BIKAJI)
                    </div>
                    <div class="dropdown-item" data-ticker="DMART" onclick="selectCompany('DMART')">
                        <span class="check-slot"></span> Avenue Supermarts (DMART)
                    </div>
                </div>
            </div>

            <!-- Mode 2: Search Input -->
            <div id="searchModeWrapper" class="search-wrapper" style="display: none;">
                <div class="search-input-group">
                    <input type="text" id="judgeSearchInput" class="search-input" placeholder="Search company name or NSE symbol (e.g. DABUR, TITAN, MARICO)..." onkeyup="handleSearchKey(event)" />
                    <button class="search-btn" onclick="executeSearch()">Investigate 🔍</button>
                </div>
                <div id="searchStatus" style="font-size: 11.5px; color: #8b949e; margin-top: 6px;"></div>
            </div>

            <div class="validation-note">
                &bull; <strong>Company validation:</strong> check that the chosen company is in the current NIFTY 50 and is eligible under Track C (Consumer, FMCG &amp; Retail). Dynamic research workflow ready for on-the-spot judge evaluation.
            </div>
        </div>

        <!-- Dashboard Content Header -->
        <div class="header-bar">
            <div>
                <span class="badge" id="trackBadge">{report.get('track')} &bull; {report.get('business_model')}</span>
                <span style="font-size: 12px; color: #8b949e; margin-left: 10px;">Format: {report.get('output_format')}</span>
            </div>
            <div>
                <span class="strength-badge" id="evidenceStrengthTop">Evidence: {report.get('element_8_evidence_strength', {}).get('rating', 'Moderate')}</span>
                <button class="btn-print" onclick="window.print()" style="margin-left: 10px;">🖨️ Export Executive Memo</button>
            </div>
        </div>

        <h1 id="companyHeading">{report.get('company_name')} ({report.get('ticker')})</h1>
        <div style="color: #8b949e; font-size: 13px;">Autonomous Financial Research Agent &bull; Non-Obvious Contradiction Discovery</div>

        <!-- Element 1: The Discovery -->
        <div class="discovery-banner">
            <div style="font-size: 12px; text-transform: uppercase; color: #38bdf8; font-weight: 800; margin-bottom: 4px;">1. The Non-Obvious Discovery</div>
            <div id="discoveryText">{report.get('element_1_the_discovery')}</div>
        </div>

        <!-- Element 2: Why It Matters -->
        <div class="section-box">
            <div class="section-title">2. Why It Matters (Operational & Financial Durability)</div>
            <ul id="whyList" style="margin: 0; padding-left: 20px; line-height: 1.6; color: #c9d1d9; font-size: 14px;">
            </ul>
        </div>

        <!-- Element 3 & 4: Numbers, Charts & Timeline -->
        <div class="grid-2">
            <div class="section-box" style="margin-top: 0;">
                <div class="section-title">3. Verified Financial Metrics & Trend Chart</div>
                <div id="metricsGrid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px;">
                </div>
                <div id="chartContainer"></div>
                <div id="mathProvenance" style="margin-top: 10px; font-size: 11px; color: #6e7681;"></div>
            </div>

            <div class="section-box" style="margin-top: 0;">
                <div class="section-title">4. Emergence Timeline</div>
                <ul id="timelineList" style="margin: 0; padding-left: 20px; line-height: 1.5; font-size: 13px; color: #c9d1d9;">
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
                <div class="section-title" style="color: #f85149;">6. Strongest Counterargument (Red Team Adversary)</div>
                <p id="counterargumentText" style="margin: 0; font-size: 13.5px; line-height: 1.6; color: #e6edf3;"></p>
            </div>

            <div class="section-box">
                <div class="section-title" style="color: #3fb950;">7. Falsification Condition (Specific & Measurable)</div>
                <p id="falsificationText" style="margin: 0; font-size: 13.5px; line-height: 1.6; color: #e6edf3;"></p>
            </div>
        </div>

        <!-- Element 8: Evidence Strength & Rubric Breakdown -->
        <div class="section-box">
            <div class="section-title" style="color: #d29922;">8. Evidence Strength & Forensic Rubric Breakdown</div>
            <div style="margin-bottom: 12px;">
                <span class="strength-badge" id="evidenceStrengthRating"></span>
            </div>
            <table style="margin-bottom: 14px;">
                <thead>
                    <tr style="border-bottom: 2px solid #21262d; text-align: left;">
                        <th style="padding: 8px 12px; font-size: 11px; color: #58a6ff; text-transform: uppercase;">Rubric Dimension</th>
                        <th style="padding: 8px 12px; font-size: 11px; color: #58a6ff; text-transform: uppercase;">Confidence Level</th>
                        <th style="padding: 8px 12px; font-size: 11px; color: #58a6ff; text-transform: uppercase;">Empirical Evidence</th>
                    </tr>
                </thead>
                <tbody id="rubricTableBody"></tbody>
            </table>
            <p id="synthesisRationale" style="margin: 0; font-size: 12.5px; line-height: 1.6; color: #c9d1d9;"></p>
        </div>

        <!-- Section E: Autonomous Reasoning Pipeline -->
        <div class="section-box">
            <div class="section-title">Section E: Autonomous Forensic Reasoning Pipeline</div>
            <div id="reasoningGrid" style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;"></div>
        </div>

        <div style="margin-top: 24px; text-align: center; font-size: 11px; color: #6e7681;">
            ATMOS 2026 Autonomous Research Agent &bull; 100% Public Data &bull; Zero Hardcoding &bull; Zero Investment Advice
        </div>
    </div>

    <!-- Client-side Switcher Logic -->
    <script>
        const ALL_REPORTS = {json_payload};
        const DISPLAY_NAMES = {json.dumps(disp_names)};
        let currentTicker = "{default_ticker}";

        function toggleSelectorMode(mode) {{
            const listWrapper = document.getElementById("listModeWrapper");
            const searchWrapper = document.getElementById("searchModeWrapper");
            if (mode === "search") {{
                listWrapper.style.display = "none";
                searchWrapper.style.display = "block";
                document.getElementById("judgeSearchInput").focus();
            }} else {{
                listWrapper.style.display = "block";
                searchWrapper.style.display = "none";
            }}
        }}

        function toggleDropdown(e) {{
            if (e) e.stopPropagation();
            const menu = document.getElementById("customDropdownMenu");
            const icon = document.getElementById("chevronIcon");
            menu.classList.toggle("show");
            icon.classList.toggle("open");
        }}

        function closeDropdown() {{
            const menu = document.getElementById("customDropdownMenu");
            const icon = document.getElementById("chevronIcon");
            if (menu) menu.classList.remove("show");
            if (icon) icon.classList.remove("open");
        }}

        window.addEventListener("click", (e) => {{
            if (!e.target.closest(".dropdown-wrapper")) {{
                closeDropdown();
            }}
        }});

        function selectCompany(ticker) {{
            ticker = ticker.toUpperCase().trim();
            closeDropdown();
            if (ALL_REPORTS[ticker]) {{
                currentTicker = ticker;
                const labelText = DISPLAY_NAMES[ticker] || `${{ALL_REPORTS[ticker].company_name}} (${{ticker}})`;
                document.getElementById("selectedCompanyLabel").textContent = labelText;

                // Update active state in menu
                document.querySelectorAll(".dropdown-item").forEach(item => {{
                    const itemTicker = item.getAttribute("data-ticker");
                    const checkSlot = item.querySelector(".check-slot");
                    if (itemTicker === ticker) {{
                        item.classList.add("active");
                        if (checkSlot) checkSlot.textContent = "✓";
                    }} else {{
                        item.classList.remove("active");
                        if (checkSlot) checkSlot.textContent = "";
                    }}
                }});

                renderReport(ALL_REPORTS[ticker]);
            }}
        }}

        function handleSearchKey(event) {{
            if (event.key === "Enter") {{
                executeSearch();
            }}
        }}

        async function executeSearch() {{
            const input = document.getElementById("judgeSearchInput");
            const query = (input.value || "").toUpperCase().trim();
            if (!query) return;

            const status = document.getElementById("searchStatus");

            // Check if matches a known ticker directly or by partial name
            let matchedTicker = null;
            if (ALL_REPORTS[query]) {{
                matchedTicker = query;
            }} else {{
                for (const [t, data] of Object.entries(ALL_REPORTS)) {{
                    const name = (data.company_name || "").toUpperCase();
                    if (t === query || name.includes(query)) {{
                        matchedTicker = t;
                        break;
                    }}
                }}
            }}

            if (matchedTicker) {{
                selectCompany(matchedTicker);
                status.innerHTML = `Loaded profile for <strong>${{matchedTicker}}</strong>.`;
                return;
            }}

            status.innerHTML = `⏳ Connecting to public filings for <strong>${{query}}</strong> via generic workflow...`;

            try {{
                const resp = await fetch(`/api/investigate?ticker=${{query}}`);
                if (resp.ok) {{
                    const data = await resp.json();
                    if (data.error) {{
                        status.textContent = `❌ ${{data.error}}`;
                    }} else {{
                        ALL_REPORTS[query] = data;
                        DISPLAY_NAMES[query] = `${{data.company_name}} (${{query}})`;
                        selectCompany(query);
                        status.innerHTML = `✅ Successfully investigated <strong>${{query}}</strong> on the spot!`;
                    }}
                    return;
                }}
            }} catch (e) {{
                status.innerHTML = `Offline mode: To run on-the-spot for <strong>${{query}}</strong>, execute <code>python3 main.py ${{query}}</code> in your terminal or start <code>python3 server.py</code>!`;
            }}
        }}

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
                <div style="margin-bottom: 14px; padding: 14px; background: #010409; border-left: 4px solid #38bdf8; border-radius: 6px; border: 1px solid #21262d;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 700; color: #58a6ff; font-size: 12px; text-transform: uppercase;">${{s.source_type || 'Primary Document'}}</span>
                        <span style="background: #161b22; color: #8b949e; font-size: 11px; padding: 2px 8px; border-radius: 4px; border: 1px solid #30363d;">${{s.publication_date || ''}}</span>
                    </div>
                    <div style="color: #ffffff; font-weight: 600; font-size: 14px;">${{s.document_title || s.title || ''}}</div>
                    <div style="color: #8b949e; font-size: 12px; margin-top: 3px;"><strong>Section/Page:</strong> ${{s.section_or_page || 'Consolidated Filings'}}</div>
                    <div style="background: rgba(13, 17, 23, 0.8); padding: 8px 12px; border-radius: 4px; margin-top: 6px; font-size: 12.5px; color: #c9d1d9; border-left: 2px solid #30363d;">
                        <strong>Exact Figure / Passage:</strong> ${{s.exact_figure_or_passage || s.data_covered || ''}}
                    </div>
                    <a href="${{s.source_link || s.url}}" target="_blank" rel="noopener noreferrer" style="display: inline-block; margin-top: 8px; font-size: 12px; color: #58a6ff; text-decoration: none; font-weight: 600;">
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
                <tr style="border-bottom: 1px solid #21262d;">
                    <td style="padding: 8px 12px; color: #8b949e; font-size: 12px; font-weight: 500;">${{label}}</td>
                    <td style="padding: 8px 12px; color: #58a6ff; font-size: 12px; font-weight: 600;">${{info.score || ''}}</td>
                    <td style="padding: 8px 12px; color: #c9d1d9; font-size: 11.5px;">${{info.detail || ''}}</td>
                </tr>`;
            }}
            rubricTableBody.innerHTML = rubricHtml;

            // Section E Reasoning
            const reasoningGrid = document.getElementById("reasoningGrid");
            reasoningGrid.innerHTML = (report.reasoning_process || []).map(r => `
                <div style="background: #010409; border-radius: 6px; padding: 10px 12px; border: 1px solid #21262d;">
                    <div style="font-size: 10px; text-transform: uppercase; color: #58a6ff; font-weight: 700;">Step ${{r.step}}: ${{r.name}}</div>
                    <div style="font-size: 12px; color: #c9d1d9; margin-top: 3px; line-height: 1.35;">${{r.description}}</div>
                </div>
            `).join("");
        }}

        // Initialize on page load
        window.addEventListener("DOMContentLoaded", () => {{
            selectCompany(currentTicker);
        }});
    </script>
</body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] ATMOS Interactive Dashboard saved: {os.path.abspath(filepath)}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        from server import run_server
        run_server()
        return

    ticker = sys.argv[1] if len(sys.argv) > 1 else "TRENT"
    ticker = ticker.upper().strip()

    if ticker == "--ALL":
        print("=" * 85)
        print("  ARGUS: PRE-COMPUTING ALL 8 TRACK C & BROADER CONSUMER PROFILES")
        print("=" * 85)
        all_reps = load_or_fetch_all_reports()
        generate_unified_html(all_reps, "TRENT", "dashboard.html")
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
    print(f"[+] Unified ATMOS Dashboard: {os.path.abspath('dashboard.html')}")
    print("=" * 85)

if __name__ == "__main__":
    main()
