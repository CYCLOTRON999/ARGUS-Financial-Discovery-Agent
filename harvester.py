"""
Public Financial Data Harvester for Indian Consumer, FMCG & Retail Companies.
Retrieves quarterly statements, balance sheet schedules, dynamic peers,
and concall/presentation links without proprietary databases or API keys.
"""

import re
import urllib.parse
from typing import Dict, List, Any, Optional
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

class PublicFinancialHarvester:
    BASE_URL = "https://www.screener.in"

    def __init__(self, ticker: str):
        self.ticker = ticker.upper().strip()
        self.company_id: Optional[str] = None
        self.warehouse_id: Optional[str] = None
        self.company_name: str = self.ticker
        self.sector: str = ""
        self.industry: str = ""
        self.html: str = ""

    def fetch_company_page(self) -> bool:
        """Fetches the primary consolidated page for the company."""
        url = f"{self.BASE_URL}/company/{self.ticker}/consolidated/"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=12)
            if resp.status_code == 200:
                self.html = resp.text
            else:
                # Fallback to standalone if consolidated not available
                url_standalone = f"{self.BASE_URL}/company/{self.ticker}/"
                resp = requests.get(url_standalone, headers=HEADERS, timeout=12)
                if resp.status_code == 200:
                    self.html = resp.text
                else:
                    return False

            # Extract IDs
            cid_match = re.search(r'data-company-id=\"([^\"]+)\"', self.html)
            if cid_match:
                self.company_id = cid_match.group(1)

            wid_match = re.search(r'data-warehouse-id=\"([^\"]+)\"', self.html)
            if wid_match:
                self.warehouse_id = wid_match.group(1)

            name_match = re.search(r'<h1[^>]*>(.*?)</h1>', self.html, re.DOTALL)
            if name_match:
                self.company_name = re.sub(r'<[^>]+>', '', name_match.group(1)).strip()

            sec_match = re.search(r'title=\"Sector\"[^>]*>([^<]+)</a>', self.html)
            if sec_match:
                self.sector = sec_match.group(1).strip()

            ind_match = re.search(r'title=\"(?:Broad Industry|Industry)\"[^>]*>([^<]+)</a>', self.html)
            if ind_match:
                self.industry = ind_match.group(1).strip()

            return True
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
            return False

    def extract_quarterly_results(self) -> Dict[str, Any]:
        """Extracts the last 8-12 quarters of Sales, Expenses, OPM, and Net Profit."""
        if not self.html:
            return {}

        pos = self.html.find('id="quarters"')
        if pos == -1:
            return {}

        table_end = self.html.find('</table>', pos)
        table_html = self.html[pos:table_end + 8]

        # Extract headers (Quarter dates)
        thead_match = re.search(r'<thead>(.*?)</thead>', table_html, re.DOTALL)
        if not thead_match:
            return {}

        quarters = [re.sub(r'<[^>]+>', '', th).strip() for th in re.findall(r'<th[^>]*>(.*?)</th>', thead_match.group(1), re.DOTALL)]
        quarters = [q for q in quarters if q]

        # Extract table rows
        tbody_match = re.search(r'<tbody>(.*?)</tbody>', table_html, re.DOTALL)
        if not tbody_match:
            return {}

        rows: Dict[str, List[float]] = {}
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>', tbody_match.group(1), re.DOTALL):
            cells = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)]
            if cells:
                raw_name = cells[0].replace('&nbsp;', ' ').replace('+', '').strip()
                cleaned_vals = []
                for v in cells[1:]:
                    v_clean = v.replace(',', '').replace('%', '').strip()
                    try:
                        cleaned_vals.append(float(v_clean))
                    except ValueError:
                        cleaned_vals.append(0.0)
                rows[raw_name] = cleaned_vals

        return {
            "quarters": quarters,
            "metrics": rows,
            "source_url": f"{self.BASE_URL}/company/{self.ticker}/consolidated/#quarters"
        }

    def extract_annual_results(self) -> Dict[str, Any]:
        """Extracts annual P&L results (Sales, Expenses, OPM, Net Profit) for FY comparisons."""
        if not self.html:
            return {}

        pos = self.html.find('id="profit-loss"')
        if pos == -1:
            return {}

        table_end = self.html.find('</table>', pos)
        table_html = self.html[pos:table_end + 8]

        thead_match = re.search(r'<thead>(.*?)</thead>', table_html, re.DOTALL)
        if not thead_match:
            return {}

        years = [re.sub(r'<[^>]+>', '', th).strip() for th in re.findall(r'<th[^>]*>(.*?)</th>', thead_match.group(1), re.DOTALL)]
        years = [y for y in years if y]

        tbody_match = re.search(r'<tbody>(.*?)</tbody>', table_html, re.DOTALL)
        if not tbody_match:
            return {}

        rows: Dict[str, List[float]] = {}
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>', tbody_match.group(1), re.DOTALL):
            cells = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)]
            if cells:
                raw_name = cells[0].replace('&nbsp;', ' ').replace('+', '').strip()
                cleaned_vals = []
                for v in cells[1:]:
                    v_clean = v.replace(',', '').replace('%', '').strip()
                    try:
                        cleaned_vals.append(float(v_clean))
                    except ValueError:
                        cleaned_vals.append(0.0)
                rows[raw_name] = cleaned_vals

        return {
            "years": years,
            "metrics": rows,
            "source_url": f"{self.BASE_URL}/company/{self.ticker}/consolidated/#profit-loss"
        }

    def fetch_balance_sheet_schedule(self, parent: str = "Other Assets") -> Dict[str, Any]:
        """Fetches detailed sub-items like Trade Receivables, Inventories, etc."""
        if not self.company_id:
            return {}

        parent_encoded = urllib.parse.quote(parent)
        url = f"{self.BASE_URL}/api/company/{self.company_id}/schedules/?parent={parent_encoded}&section=balance-sheet&consolidated="
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                # Clean and parse values
                cleaned_schedule: Dict[str, Dict[str, float]] = {}
                for item_name, period_dict in data.items():
                    if isinstance(period_dict, dict):
                        cleaned_schedule[item_name] = {}
                        for period, val in period_dict.items():
                            if period == "isExpandable":
                                continue
                            try:
                                cleaned_schedule[item_name][period] = float(str(val).replace(',', '').strip())
                            except ValueError:
                                continue
                return {
                    "schedule_name": parent,
                    "data": cleaned_schedule,
                    "source_url": url
                }
        except Exception as e:
            print(f"Error fetching balance sheet schedule: {e}")
        return {}

    def fetch_dynamic_peers(self) -> List[Dict[str, str]]:
        """Extracts listed peers dynamically from the sector table."""
        if not self.warehouse_id:
            return []

        url = f"{self.BASE_URL}/api/company/{self.warehouse_id}/peers/"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                peer_matches = re.findall(r'<a href=\"/company/([A-Z0-9]+)/[^\"]*\"[^>]*>(.*?)</a>', resp.text)
                peers = []
                for ticker, name in peer_matches:
                    clean_name = re.sub(r'<[^>]+>', '', name).replace('&amp;', '&').strip()
                    if ticker != self.ticker and ticker not in [p['ticker'] for p in peers]:
                        peers.append({
                            "ticker": ticker,
                            "name": clean_name,
                            "url": f"{self.BASE_URL}/company/{ticker}/consolidated/"
                        })
                return peers[:5]
        except Exception as e:
            print(f"Error fetching peers: {e}")
        return []

    def extract_concall_transcripts(self) -> List[Dict[str, str]]:
        """Extracts clickable links to Concall transcripts and Investor Presentations."""
        if not self.html:
            return []

        docs: List[Dict[str, str]] = []
        pos = self.html.find('documents concalls')
        if pos != -1:
            snippet = self.html[pos:pos + 8000]
            li_blocks = re.findall(r'<li[^>]*>(.*?)</li>', snippet, re.DOTALL)
            for li in li_blocks:
                date_match = re.search(r'<div class=\"ink-600[^\"]*\"[^>]*>([^<]+)</div>', li)
                date_str = date_match.group(1).strip() if date_match else "Recent"
                
                # Links in this li - match both href before or after class
                links = re.findall(r'<a[^>]*href=\"([^\"]+)\"[^>]*>([^<]+)</a>', li)
                for href, title in links:
                    title_clean = title.strip()
                    if any(kw in title_clean.lower() for kw in ['transcript', 'ppt', 'notes']):
                        docs.append({
                            "period": date_str,
                            "type": title_clean,
                            "url": href if href.startswith('http') else f"{self.BASE_URL}{href}"
                        })

        # Prioritize Transcripts over PPTs/Notes
        docs.sort(key=lambda d: 0 if 'transcript' in d['type'].lower() else 1)
        return docs[:6]
