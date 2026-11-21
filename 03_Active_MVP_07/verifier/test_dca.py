#!/usr/bin/env python3
"""
03_Active_MVP_07/verifier/test_dca.py
Deterministic verification tests for DCA Position Sizer & Profit-Taking Ladder Engine.
"""

import sys

def calculate_dca_basis(buys, default_fee_pct=0.001):
    total_gross_cost = 0.0
    total_fees = 0.0
    total_units = 0.0

    for b in buys:
        price = float(b["price"])
        qty = float(b["qty"])
        fee_pct = float(b.get("fee_pct", default_fee_pct))
        
        gross = price * qty
        fee = gross * fee_pct
        
        total_gross_cost += gross
        total_fees += fee
        total_units += qty

    if total_units <= 0:
        return {"weighted_avg_price": 0, "total_units": 0, "total_investment": 0, "breakeven_price": 0}

    weighted_avg_price = round(total_gross_cost / total_units, 2)
    total_investment = round(total_gross_cost + total_fees, 2)
    
    # Price required to recoup total investment after paying exit fee
    breakeven_price = round(total_investment / (total_units * (1.0 - default_fee_pct)), 2)

    return {
        "total_units": round(total_units, 6),
        "total_gross_cost": round(total_gross_cost, 2),
        "total_fees": round(total_fees, 2),
        "total_investment": total_investment,
        "weighted_avg_price": weighted_avg_price,
        "breakeven_price": breakeven_price
    }

def calculate_profit_ladder(total_units, weighted_avg_price, ladder_tiers, sell_fee_pct=0.001):
    remaining_units = total_units
    total_realized_cash = 0.0
    total_realized_profit = 0.0
    ladder_results = []

    for tier in ladder_tiers:
        target_price = float(tier["target_price"])
        sell_pct = float(tier["sell_pct"]) / 100.0  # percentage of initial total units
        
        units_to_sell = round(total_units * sell_pct, 6)
        if units_to_sell > remaining_units:
            units_to_sell = remaining_units

        gross_proceeds = round(units_to_sell * target_price, 2)
        fee = round(gross_proceeds * sell_fee_pct, 2)
        net_proceeds = round(gross_proceeds - fee, 2)
        
        cost_of_sold_units = round(units_to_sell * weighted_avg_price, 2)
        tier_net_profit = round(net_proceeds - cost_of_sold_units, 2)
        
        remaining_units = round(remaining_units - units_to_sell, 6)
        total_realized_cash = round(total_realized_cash + net_proceeds, 2)
        total_realized_profit = round(total_realized_profit + tier_net_profit, 2)

        ladder_results.append({
            "target_price": target_price,
            "units_sold": units_to_sell,
            "net_proceeds": net_proceeds,
            "tier_net_profit": tier_net_profit,
            "remaining_units": remaining_units
        })

    return {
        "tiers": ladder_results,
        "total_realized_cash": total_realized_cash,
        "total_realized_profit": total_realized_profit,
        "final_moonbag_units": remaining_units
    }

def test_dca_basis_math():
    buys = [
        {"price": 60000, "qty": 1.0, "fee_pct": 0.001},  # $60,000 + $60 fee
        {"price": 50000, "qty": 0.5, "fee_pct": 0.001},  # $25,000 + $25 fee
        {"price": 40000, "qty": 0.5, "fee_pct": 0.001}   # $20,000 + $20 fee
    ]
    res = calculate_dca_basis(buys, 0.001)
    print(f"[+] Multi-Buy DCA: Units={res['total_units']}, Weighted Avg=${res['weighted_avg_price']}, Breakeven=${res['breakeven_price']}")
    
    assert res["total_units"] == 2.0
    assert res["total_gross_cost"] == 105000.00
    assert res["total_fees"] == 105.00
    assert res["total_investment"] == 105105.00
    assert res["weighted_avg_price"] == 52500.00
    assert res["breakeven_price"] == 52605.11

def test_profit_ladder_execution():
    total_units = 2.0
    weighted_avg = 52500.00
    # 4-Tier Exit Strategy:
    # Tier 1: Sell 25% @ $65,000
    # Tier 2: Sell 25% @ $75,000
    # Tier 3: Sell 25% @ $90,000
    # Moonbag: Keep 25% (0.5 units)
    tiers = [
        {"target_price": 65000, "sell_pct": 25},
        {"target_price": 75000, "sell_pct": 25},
        {"target_price": 90000, "sell_pct": 25}
    ]
    res = calculate_profit_ladder(total_units, weighted_avg, tiers, 0.001)
    print(f"[+] Profit Ladder: Realized Cash=${res['total_realized_cash']}, Net Profit=${res['total_realized_profit']}, Moonbag={res['final_moonbag_units']} units")
    
    assert res["final_moonbag_units"] == 0.5
    assert len(res["tiers"]) == 3
    # Tier 1: 0.5 units @ 65000 = $32,500 gross - $32.50 fee = $32,467.50 net proceeds. Cost = $26,250. Profit = $6,217.50
    assert res["tiers"][0]["units_sold"] == 0.5
    assert res["tiers"][0]["tier_net_profit"] == 6217.50
    assert res["total_realized_cash"] > 110000.0
    assert res["total_realized_profit"] > 30000.0

if __name__ == "__main__":
    print("=== RUNNING DCA & PROFIT-TAKING LADDER TESTS ===")
    try:
        test_dca_basis_math()
        test_profit_ladder_execution()
        print("\n=== ALL TESTS PASSED: FORMULAS DETERMINISTIC (EXIT 0) ===")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n[FAIL] Assertion failed: {e}")
        sys.exit(1)
