
import time
from utils.axiom_signals import fetch_trending_token
from utils.trader import execute_trade
from utils.telegram import send_telegram_update

def run_bot():
    send_telegram_update("🚀 Sniper bot started and scanning Axiom...")
    while True:
        token_info = fetch_trending_token()
        if token_info:
            trade_result = execute_trade(token_info)
            send_telegram_update(f"💰 Trade executed: {trade_result}")
        else:
            print("[BOT] No valid Axiom signal. Waiting...")
        time.sleep(60)
