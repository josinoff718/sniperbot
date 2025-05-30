import json
import os

PERSIST_FILE = "wallet_stats.json"
TRADE_SIZE_FILE = "wallet_trade_sizes.json"

def load_wallet_stats():
    if os.path.exists(PERSIST_FILE):
        with open(PERSIST_FILE, "r") as f:
            return json.load(f)
    return {}

def save_trade_sizes(sizes):
    with open(TRADE_SIZE_FILE, "w") as f:
        json.dump(sizes, f, indent=2)

def load_trade_sizes():
    if os.path.exists(TRADE_SIZE_FILE):
        with open(TRADE_SIZE_FILE, "r") as f:
            return json.load(f)
    return {}

def update_trade_sizing(base_size=5, max_size=15, min_size=2):
    stats = load_wallet_stats()
    trade_sizes = {}

    for wallet, data in stats.items():
        total_wins = sum(d["wins"] for d in data["days"].values())
        total_losses = sum(d["losses"] for d in data["days"].values())
        total_trades = total_wins + total_losses
        win_rate = (total_wins / total_trades) * 100 if total_trades > 0 else 0

        if total_trades < 3:
            size = base_size
        elif win_rate >= 70:
            size = max_size
        elif win_rate >= 50:
            size = base_size
        else:
            size = min_size

        trade_sizes[wallet] = {"win_rate": win_rate, "trade_size": size}

    save_trade_sizes(trade_sizes)
    return trade_sizes

def generate_leaderboard():
    stats = load_wallet_stats()
    leaderboard = []

    for wallet, data in stats.items():
        total_wins = sum(d["wins"] for d in data["days"].values())
        total_losses = sum(d["losses"] for d in data["days"].values())
        total_profit = sum(d["profit"] for d in data["days"].values())
        total_trades = total_wins + total_losses
        win_rate = (total_wins / total_trades) * 100 if total_trades > 0 else 0

        leaderboard.append((wallet, win_rate, total_trades, total_profit))

    sorted_leaderboard = sorted(leaderboard, key=lambda x: (x[1], x[3]), reverse=True)[:5]
    report = ["🏆 Top Wallets Leaderboard:"]
    for wallet, wr, trades, pnl in sorted_leaderboard:
        report.append(f"{wallet[:6]}... → {wr:.1f}% win rate, {trades} trades, {pnl:.2f} SOL")

    return "\n".join(report)