import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

PERSIST_FILE = "wallet_stats.json"

# Load wallet stats
def load_wallet_stats():
    if os.path.exists(PERSIST_FILE):
        with open(PERSIST_FILE, "r") as f:
            return json.load(f)
    return {}

# Save wallet stats
def save_wallet_stats(stats):
    with open(PERSIST_FILE, "w") as f:
        json.dump(stats, f, indent=2)

# Update stats
def record_trade(wallet, profit):
    stats = load_wallet_stats()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    if wallet not in stats:
        stats[wallet] = {"days": {}}
    if today not in stats[wallet]["days"]:
        stats[wallet]["days"][today] = {"wins": 0, "losses": 0, "profit": 0}
    if profit > 0:
        stats[wallet]["days"][today]["wins"] += 1
    else:
        stats[wallet]["days"][today]["losses"] += 1
    stats[wallet]["days"][today]["profit"] += profit
    save_wallet_stats(stats)

# Generate daily report
def generate_daily_report():
    stats = load_wallet_stats()
    report_lines = ["📊 Daily Wallet PnL Report"]
    for wallet, data in stats.items():
        total_wins, total_losses, total_profit = 0, 0, 0
        for day in data["days"]:
            total_wins += data["days"][day]["wins"]
            total_losses += data["days"][day]["losses"]
            total_profit += data["days"][day]["profit"]
        total_trades = total_wins + total_losses
        win_rate = (total_wins / total_trades) * 100 if total_trades else 0
        report_lines.append(f"{wallet[:6]}... → Win rate: {win_rate:.1f}%, PnL: {total_profit:.2f} SOL")
    return "\n".join(report_lines)