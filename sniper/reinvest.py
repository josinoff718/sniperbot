import os
import json
from datetime import datetime, timedelta

PERSIST_FILE = "wallet_stats.json"
LIMIT_FILE = "daily_limit.json"

def load_wallet_stats():
    if os.path.exists(PERSIST_FILE):
        with open(PERSIST_FILE, "r") as f:
            return json.load(f)
    return {}

def save_daily_limit(value):
    with open(LIMIT_FILE, "w") as f:
        json.dump({"usd_limit": value}, f)

def auto_reinvest(reinvest_pct=0.5):
    stats = load_wallet_stats()
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    total_profit = 0

    for wallet in stats:
        if yesterday in stats[wallet]["days"]:
            total_profit += stats[wallet]["days"][yesterday]["profit"]

    usd_price = get_sol_price_usd()
    if usd_price == 0:
        return "❌ Could not fetch SOL price"

    usd_profit = total_profit * usd_price
    new_limit = round(30 + usd_profit * reinvest_pct, 2)

    save_daily_limit(new_limit)
    return f"💰 Reinvested {int(reinvest_pct * 100)}% of ${usd_profit:.2f} profit → New limit: ${new_limit:.2f}"

def get_sol_price_usd():
    import requests
    try:
        res = requests.get("https://api.coingecko.com/api/v3/simple/price", params={
            "ids": "solana",
            "vs_currencies": "usd"
        })
        return res.json()["solana"]["usd"]
    except:
        return 0