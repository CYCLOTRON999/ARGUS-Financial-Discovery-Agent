#!/usr/bin/env python3
"""
Interactive Local Server for ATMOS 2026 ARGUS Dashboard.
Allows live on-the-spot investigation of ANY Indian company ticker selected by judges.

Usage:
    python3 server.py
    (or python3 main.py --serve)
Opens on: http://localhost:8000
"""

import http.server
import socketserver
import urllib.parse
import json
import os
from investigator import FinancialInvestigator

PORT = 8000

class ArgusRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # Route: API for live judge query
        if parsed.path == "/api/investigate":
            params = urllib.parse.parse_qs(parsed.query)
            ticker = params.get("ticker", ["DABUR"])[0].upper().strip()
            
            print(f"[ARGUS Server] Live judge investigation requested for ticker: {ticker}")
            investigator = FinancialInvestigator(ticker)
            report = investigator.run_investigation()
            
            # Save artifacts locally
            if "error" not in report:
                with open(f"output_{ticker}.json", "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2)
            
            response_bytes = json.dumps(report).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response_bytes)
            return

        # Default route to dashboard.html
        if parsed.path in ["", "/"]:
            self.path = "/dashboard.html"
            
        return super().do_GET()

def run_server(port=PORT):
    # Ensure current directory is workspace
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), ArgusRequestHandler) as httpd:
        print("=" * 80)
        print(f"  ARGUS INTERACTIVE DISCOVERY DASHBOARD SERVER RUNNING")
        print(f"  URL: http://localhost:{port}/")
        print(f"  Core Track C & Broader Consumer Profiles Pre-Loaded")
        print(f"  Live on-the-spot judge investigations active via /api/investigate")
        print("=" * 80)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()
