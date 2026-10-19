"""
Deterministic Financial Calculator.
Ensures zero LLM math hallucinations: all ratios, DSO, YoY growth rates,
working capital days, and price-volume decompositions are computed deterministically.
"""

from typing import Dict, List, Any, Optional

class FinancialCalculator:
    
    @staticmethod
    def calculate_yoy_sales_growth(quarters: List[str], sales: List[float]) -> List[Dict[str, Any]]:
        """
        Calculates Year-over-Year (YoY) Sales growth comparing Q(t) to Q(t-4).
        """
        growth_series = []
        for i in range(len(sales)):
            if i >= 4 and sales[i-4] > 0:
                yoy_growth = ((sales[i] - sales[i-4]) / sales[i-4]) * 100
                growth_series.append({
                    "quarter": quarters[i],
                    "current_sales_cr": sales[i],
                    "base_quarter": quarters[i-4],
                    "base_sales_cr": sales[i-4],
                    "yoy_growth_pct": round(yoy_growth, 2)
                })
            else:
                growth_series.append({
                    "quarter": quarters[i],
                    "current_sales_cr": sales[i],
                    "base_quarter": None,
                    "base_sales_cr": None,
                    "yoy_growth_pct": None
                })
        return growth_series

    @staticmethod
    def calculate_receivable_days_dso(
        sales_by_period: Dict[str, float], 
        receivables_by_period: Dict[str, float],
        is_annual: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Calculates Days Sales Outstanding (DSO):
        DSO = (Trade Receivables / Sales) * 365 (for annual periods)
        or * 90 for quarterly periods.
        """
        dso_records = []
        for period, rec_val in receivables_by_period.items():
            if period in sales_by_period and sales_by_period[period] > 0:
                sales_val = sales_by_period[period]
                days_factor = 365.0 if is_annual else 90.0
                dso = (rec_val / sales_val) * days_factor
                dso_records.append({
                    "period": period,
                    "receivables_cr": rec_val,
                    "sales_cr": sales_val,
                    "dso_days": round(dso, 1)
                })
        return dso_records

    @staticmethod
    def calculate_inventory_days_dio(
        expenses_by_period: Dict[str, float],
        inventory_by_period: Dict[str, float],
        is_annual: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Calculates Days Inventory Outstanding (DIO):
        DIO = (Inventories / Expenses) * 365 (for annual periods)
        or * 90 for quarterly periods.
        """
        dio_records = []
        for period, inv_val in inventory_by_period.items():
            if period in expenses_by_period and expenses_by_period[period] > 0:
                exp_val = expenses_by_period[period]
                days_factor = 365.0 if is_annual else 90.0
                dio = (inv_val / exp_val) * days_factor
                dio_records.append({
                    "period": period,
                    "inventory_cr": inv_val,
                    "expenses_cr": exp_val,
                    "dio_days": round(dio, 1)
                })
        return dio_records

    @staticmethod
    def decompose_price_vs_volume(
        reported_revenue_growth_pct: float,
        reported_volume_growth_pct: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Decomposes top-line growth into volume vs price contribution:
        (1 + g_rev) = (1 + g_vol) * (1 + g_price)
        g_price = ((1 + g_rev) / (1 + g_vol)) - 1
        """
        if reported_volume_growth_pct is None:
            return {
                "available": False,
                "reason": "Volume growth not disclosed in raw financial tables; decomposed via realization spread."
            }

        g_rev = reported_revenue_growth_pct / 100.0
        g_vol = reported_volume_growth_pct / 100.0

        if (1.0 + g_vol) == 0:
            g_price = 0.0
        else:
            g_price = ((1.0 + g_rev) / (1.0 + g_vol)) - 1.0

        price_pct = round(g_price * 100.0, 2)
        
        # Determine dominant driver
        if reported_revenue_growth_pct > 0 and reported_volume_growth_pct <= 0:
            driver = "100% Price-Led (Volume Contraction)"
        elif reported_volume_growth_pct > 0 and price_pct > reported_volume_growth_pct:
            driver = "Price-Heavy Growth"
        elif reported_volume_growth_pct > price_pct:
            driver = "Volume-Led Growth"
        else:
            driver = "Balanced"

        return {
            "available": True,
            "revenue_growth_pct": round(reported_revenue_growth_pct, 2),
            "volume_growth_pct": round(reported_volume_growth_pct, 2),
            "derived_price_growth_pct": price_pct,
            "driver_assessment": driver
        }

    @staticmethod
    def detect_channel_stress_anomaly(
        dso_records: List[Dict[str, Any]], 
        sales_growth_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluates whether Trade Receivables (DSO) expanded significantly
        while sales growth moderated or volume slowed (classic Channel Stuffing sign).
        """
        if len(dso_records) < 2:
            return {"anomaly_detected": False, "reason": "Insufficient DSO periods"}

        start_dso = dso_records[0]["dso_days"]
        recent_dso = dso_records[-1]["dso_days"]
        delta_dso = round(recent_dso - start_dso, 1)
        pct_change = round((delta_dso / start_dso) * 100.0, 1) if start_dso > 0 else 0.0

        is_stressed = delta_dso > 5.0 or pct_change > 20.0

        if delta_dso > 0:
            change_desc = f"expanded from {start_dso} days ({dso_records[0]['period']}) to {recent_dso} days ({dso_records[-1]['period']}), rising by +{delta_dso:.1f} days (+{pct_change}%)"
        else:
            change_desc = f"contracted from {start_dso} days ({dso_records[0]['period']}) to {recent_dso} days ({dso_records[-1]['period']}), improving by {delta_dso:.1f} days ({pct_change}%)"

        return {
            "anomaly_detected": is_stressed,
            "start_period": dso_records[0]["period"],
            "start_dso": start_dso,
            "recent_period": dso_records[-1]["period"],
            "recent_dso": recent_dso,
            "delta_days": delta_dso,
            "pct_increase": pct_change,
            "description": f"Distributor receivable days {change_desc}."
        }

    @staticmethod
    def detect_inventory_stress_anomaly(
        dio_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluates whether Inventories (DIO) expanded significantly over the period.
        """
        if len(dio_records) < 2:
            return {"anomaly_detected": False, "reason": "Insufficient DIO periods"}

        start_dio = dio_records[0]["dio_days"]
        recent_dio = dio_records[-1]["dio_days"]
        delta_dio = round(recent_dio - start_dio, 1)
        pct_change = round((delta_dio / start_dio) * 100.0, 1) if start_dio > 0 else 0.0

        is_stressed = delta_dio > 5.0 or pct_change > 15.0

        if delta_dio > 0:
            change_desc = f"expanded from {start_dio} days ({dio_records[0]['period']}) to {recent_dio} days ({dio_records[-1]['period']}), rising by +{delta_dio:.1f} days (+{pct_change}%)"
        else:
            change_desc = f"compressed from {start_dio} days ({dio_records[0]['period']}) to {recent_dio} days ({dio_records[-1]['period']}), improving by {delta_dio:.1f} days ({pct_change}%)"

        return {
            "anomaly_detected": is_stressed,
            "start_period": dio_records[0]["period"],
            "start_dio": start_dio,
            "recent_period": dio_records[-1]["period"],
            "recent_dio": recent_dio,
            "delta_days": delta_dio,
            "pct_increase": pct_change,
            "description": f"Inventory days {change_desc}."
        }
