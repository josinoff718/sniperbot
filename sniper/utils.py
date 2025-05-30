import os
import time
import logging
import random
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
JUPITER_API = "https://quote-api.jup.ag/v6"

positions = {}
history = []

class TradeTracker:
    def __init__(self, mint, entry_price, sol_amount):
        self.mint = mint
        self.entry = entry_price
        self.amount = sol_amount
        self.peak = entry_price
        self.open = True
        self.exit_price = None
        self.reason = ""

    def update_price(self, current_price):
        if current_price > self.peak:
            self.peak = current_price
        gain = (current_price - self.entry) / self.entry
        drop = (self.peak - current_price) / self.peak
        if gain >= 1.0:
            self.reason = '2x Target'
            return 'take_profit'
        if drop >= 0.3:
            self.reason = 'Trailing Stop'
            return 'trailing_stop'
        if gain <= -0.4:
            self.reason = 'Stop Loss'
            return 'stop_loss'
        return 'hold'

def send_telegram_message(msg):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        try:
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                          data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
        except Exception as e:
            logging.error(f"Telegram error: {e}")

def get_smart_wallets():
    return os.getenv("SMART_WALLETS", "").split(",")

def monitor_wallets_and_trade(wallets, daily_limit, debug):
    for wallet in wallets:
        if random.random() > 0.95:
            token_mint = "So11111111111111111111111111111111111111112"
            sol_amount = 0.1
            quote = get_token_quote(token_mint, sol_amount)
            if not quote:
                continue
            entry_price = float(quote.get("outAmount", 0)) / 10**6
            tracker = TradeTracker(token_mint, entry_price, sol_amount)
            positions[token_mint] = tracker
            send_telegram_message(f"[BUY] {sol_amount} SOL → {token_mint} @ {entry_price}")
            time.sleep(2)

    for mint, tracker in positions.items():
        if not tracker.open:
            continue
        price = get_token_price_mock(mint)
        decision = tracker.update_price(price)
        if decision != 'hold':
            tracker.open = False
            tracker.exit_price = price
            history.append(tracker)
            roi = (price - tracker.entry) / tracker.entry * 100
            send_telegram_message(f"[SELL] {mint} - {tracker.reason} @ {price:.4f} (PnL: {roi:+.2f}%)")

def summarize_daily_pnl():
    if not history:
        return
    total = len(history)
    wins = sum(1 for h in history if h.exit_price > h.entry)
    avg_roi = sum((h.exit_price - h.entry) / h.entry for h in history) / total
    best = max((h.exit_price - h.entry) / h.entry for h in history)
    worst = min((h.exit_price - h.entry) / h.entry for h in history)
    win_rate = int((wins / total) * 100)
    msg = (
        "[P&L SUMMARY]\n"
        f"Total Trades: {total}\n"
        f"Wins: {wins} ({win_rate}%)\n"
        f"Avg ROI: {avg_roi*100:+.2f}%\n"
        f"Best Trade: {best*100:+.2f}%\n"
        f"Worst Trade: {worst*100:+.2f}%"
    )
    send_telegram_message(msg)

def get_token_quote(token_mint, sol_amount):
    try:
        params = {
            "inputMint": "So11111111111111111111111111111111111111112",
            "outputMint": token_mint,
            "amount": int(sol_amount * 10**9),
            "slippageBps": 100
        }
        res = requests.get(f"https://quote-api.jup.ag/v6/quote", params=params)
        return res.json()
    except Exception as e:
        logging.error(f"Quote error: {e}")
        return None

def get_token_price_mock(mint):
    return 1.0 + random.uniform(-0.4, 1.5)