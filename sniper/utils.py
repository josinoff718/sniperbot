import os
import time
import logging
import random
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
JUPITER_API = "https://quote-api.jup.ag/v6"
positions = {}

class TradeTracker:
    def __init__(self, mint, entry_price, sol_amount):
        self.mint = mint
        self.entry = entry_price
        self.amount = sol_amount
        self.peak = entry_price
        self.open = True

    def update_price(self, current_price):
        if current_price > self.peak:
            self.peak = current_price
        gain = (current_price - self.entry) / self.entry
        drop = (self.peak - current_price) / self.peak
        if gain >= 1.0: return 'take_profit'
        if drop >= 0.3: return 'trailing_stop'
        if gain <= -0.4: return 'stop_loss'
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
            positions[token_mint] = TradeTracker(token_mint, entry_price, sol_amount)
            send_telegram_message(f"📈 BUY: {sol_amount} SOL → {token_mint} @ {entry_price}")
            time.sleep(5)

    for mint, tracker in positions.items():
        if not tracker.open:
            continue
        price = get_token_price_mock(mint)
        decision = tracker.update_price(price)
        if decision != 'hold':
            send_telegram_message(f"💰 SELL: {mint} - {decision.upper()} @ {price} (Entry: {tracker.entry})")
            tracker.open = False

def get_token_quote(token_mint, sol_amount):
    try:
        params = {
            "inputMint": "So11111111111111111111111111111111111111112",
            "outputMint": token_mint,
            "amount": int(sol_amount * 10**9),
            "slippageBps": 100
        }
        res = requests.get(f"{JUPITER_API}/quote", params=params)
        return res.json()
    except Exception as e:
        logging.error(f"Quote error: {e}")
        return None

def get_token_price_mock(mint):
    # Simulate price oscillation
    base = 1.0
    return base + random.uniform(-0.5, 1.5)

def summarize_daily_pnl():
    wins = sum(1 for t in positions.values() if not t.open and t.peak >= t.entry * 2)
    total = len(positions)
    send_telegram_message(f"📊 Daily Summary: Trades: {total}, Wins: {wins}, Win Rate: {100 * wins/total:.0f}%")