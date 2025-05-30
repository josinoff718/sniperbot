import json
import os
from datetime import datetime, timedelta

PERSIST_FILE = "wallet_stats.json"
PROMO_FILE = "wallet_changes.json"

def load_wallet_stats():
    if os.path.exists(PERSIST_FILE):
        with open(PERSIST_FILE, "r") as f:
            return json.load(f)
    return {}

def save_wallet_stats(stats):
    with open(PERSIST_FILE, "w") as f:
        json.dump(stats, f, indent=2)

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

def evaluate_wallet_performance():
    stats = load_wallet_stats()
    promotions, drops = [], []
    for wallet, data in stats.items():
        total_wins, total_losses, total_profit = 0, 0, 0
        recent_losses = 0
        for day in sorted(data["days"].keys(), reverse=True):
            total_wins += data["days"][day]["wins"]
            total_losses += data["days"][day]["losses"]
            total_profit += data["days"][day]["profit"]
            if data["days"][day]["profit"] < 0:
                recent_losses += 1
            else:
                break  # stop counting loss streak on first non-loss day

        total_trades = total_wins + total_losses
        win_rate = (total_wins / total_trades) * 100 if total_trades else 0

        if total_trades >= 3 and win_rate > 60 and total_profit > 0.5:
            promotions.append(wallet)
        elif total_trades >= 5 and (win_rate < 30 or recent_losses >= 3):
            drops.append(wallet)

    with open(PROMO_FILE, "w") as f:
        json.dump({"promotions": promotions, "drops": drops}, f, indent=2)

    return promotions, drops

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
        report_lines.append(f"{wallet[:6]}... → Win rate: {win_rate:.1f}%, Trades: {total_trades}, PnL: {total_profit:.2f} SOL")

    promotions, drops = evaluate_wallet_performance()
    if promotions:
        report_lines.append("\n🚀 Promotions:")
        for w in promotions:
            report_lines.append(f"  ↑ {w[:6]}... promoted to higher tier")

    if drops:
        report_lines.append("\n🔻 Drops:")
        for w in drops:
            report_lines.append(f"  ↓ {w[:6]}... dropped due to poor performance")

    return "\n".join(report_lines)