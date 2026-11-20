#!/usr/bin/env python3
"""
03_Active_MVP_05/verifier/test_roi.py
Deterministic verification tests for Freelancer Connects-ROI & Proposal Win-Rate Engine.
"""

import sys

def calculate_proposal_financials(contract_value, connects_spent, connect_price=0.15, platform_fee_pct=0.15, estimated_hours=10):
    connects_cost = round(connects_spent * connect_price, 2)
    platform_fee = round(contract_value * platform_fee_pct, 2)
    net_payout = round(contract_value - platform_fee - connects_cost, 2)
    
    if contract_value > 0:
        net_margin_pct = round((net_payout / contract_value) * 100, 1)
    else:
        net_margin_pct = 0.0
        
    if estimated_hours > 0:
        effective_hourly_rate = round(net_payout / estimated_hours, 2)
    else:
        effective_hourly_rate = 0.0
        
    max_breakeven_connects = int((contract_value * (1.0 - platform_fee_pct)) / connect_price) if connect_price > 0 else 0
    
    return {
        "connects_cost": connects_cost,
        "platform_fee": platform_fee,
        "net_payout": net_payout,
        "net_margin_pct": net_margin_pct,
        "effective_hourly_rate": effective_hourly_rate,
        "max_breakeven_connects": max_breakeven_connects
    }

def calculate_portfolio_metrics(proposals, connect_price=0.15, platform_fee_pct=0.15):
    total = len(proposals)
    if total == 0:
        return {"win_rate": 0, "total_connects": 0, "total_spend": 0, "net_revenue": 0}
        
    won_proposals = [p for p in proposals if p["status"] == "Won"]
    interviewed = [p for p in proposals if p["status"] in ["Interviewed", "Won"]]
    
    total_connects = sum(p["connects"] for p in proposals)
    total_connects_spend = round(total_connects * connect_price, 2)
    
    total_gross = sum(p["contract_value"] for p in won_proposals)
    total_fees = round(total_gross * platform_fee_pct, 2)
    net_earnings = round(total_gross - total_fees - total_connects_spend, 2)
    
    win_rate_pct = round((len(won_proposals) / total) * 100, 1)
    interview_rate_pct = round((len(interviewed) / total) * 100, 1)
    cac = round(total_connects_spend / len(won_proposals), 2) if len(won_proposals) > 0 else total_connects_spend
    
    return {
        "total_proposals": total,
        "won_count": len(won_proposals),
        "win_rate_pct": win_rate_pct,
        "interview_rate_pct": interview_rate_pct,
        "total_connects": total_connects,
        "total_connects_spend": total_connects_spend,
        "total_gross": total_gross,
        "net_earnings": net_earnings,
        "cac": cac
    }

def test_single_proposal_math():
    # Scenario: $500 fixed-price contract, 50 connects bid ($7.50), 15% Upwork fee ($75), 10 hours work
    res = calculate_proposal_financials(500.0, 50, 0.15, 0.15, 10)
    print(f"[+] Single Proposal: Contract=$500, Connects=50 -> Net Payout=${res['net_payout']}")
    assert res["connects_cost"] == 7.50
    assert res["platform_fee"] == 75.00
    assert res["net_payout"] == 417.50
    assert res["net_margin_pct"] == 83.5
    assert res["effective_hourly_rate"] == 41.75
    assert res["max_breakeven_connects"] == 2833

def test_high_boost_burn_edge_case():
    # Scenario: Small $50 task, 100 connects boosted ($15.00), 15% fee ($7.50)
    # Gross $50 - Fee $7.50 - Connects $15.00 = $27.50 (Burned 30% of contract on connects!)
    res = calculate_proposal_financials(50.0, 100, 0.15, 0.15, 2)
    print(f"[+] High-Boost Alert: $50 gig with 100 connects -> Margin={res['net_margin_pct']}%")
    assert res["net_payout"] == 27.50
    assert res["net_margin_pct"] == 55.0

def test_portfolio_funnel():
    proposals = [
        {"id": 1, "status": "Won", "connects": 40, "contract_value": 1000},
        {"id": 2, "status": "Lost", "connects": 60, "contract_value": 0},
        {"id": 3, "status": "Interviewed", "connects": 50, "contract_value": 0},
        {"id": 4, "status": "Lost", "connects": 30, "contract_value": 0},
        {"id": 5, "status": "Won", "connects": 50, "contract_value": 600}
    ]
    # Total proposals = 5, Won = 2 (Win rate = 40%)
    # Total connects = 40+60+50+30+50 = 230 connects * $0.15 = $34.50
    # Total gross = $1600. Platform fee (15%) = $240.
    # Net earnings = $1600 - $240 - $34.50 = $1325.50
    # CAC per won client = $34.50 / 2 = $17.25
    summary = calculate_portfolio_metrics(proposals)
    print(f"[+] Portfolio Summary: Win Rate={summary['win_rate_pct']}%, Net=${summary['net_earnings']}, CAC=${summary['cac']}")
    assert summary["total_proposals"] == 5
    assert summary["won_count"] == 2
    assert summary["win_rate_pct"] == 40.0
    assert summary["total_connects"] == 230
    assert summary["total_connects_spend"] == 34.50
    assert summary["net_earnings"] == 1325.50
    assert summary["cac"] == 17.25

if __name__ == "__main__":
    print("=== RUNNING FREELANCER CONNECTS ROI TESTS ===")
    try:
        test_single_proposal_math()
        test_high_boost_burn_edge_case()
        test_portfolio_funnel()
        print("\n=== ALL TESTS PASSED (EXIT CODE 0) ===")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Assertion failed: {e}")
        sys.exit(1)
